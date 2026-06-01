"""Unsupervised baseline clustering on raw WVS+Hofstede features (doc 14).

Compares:
- the Huntington-informed 11-civilization taxonomy (assignment via argmax(w_s)),
- k-means with k=11 (matching the taxonomy's cardinality),
- HDBSCAN (density-based, free choice of k).

Reports Adjusted Rand Index (ARI), Normalised Mutual Information (NMI), and
the confusion matrix of cluster ↔ civilization assignments. Implemented in
pure NumPy + scipy.cluster (no scikit-learn dependency).
"""
from __future__ import annotations

import json
from collections import defaultdict

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist

from apps.basis_builder.centroids import compute_centroids
from apps.basis_builder.load_hofstede import load_hofstede
from apps.basis_builder.load_iw import load_inglehart_welzel
from apps.basis_builder.paths import EMPIRICAL_DIR
from apps.basis_builder.projector import project_states


def _kmeans_pure_numpy(
    feature_matrix: np.ndarray,
    n_clusters: int,
    n_iterations: int = 100,
    random_seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Lloyd's algorithm, pure NumPy. Returns (cluster_labels, centroid_matrix)."""
    rng = np.random.default_rng(random_seed)
    n_samples = feature_matrix.shape[0]
    initial_indices = rng.choice(n_samples, size=n_clusters, replace=False)
    centroid_matrix = feature_matrix[initial_indices].copy()

    cluster_labels = np.zeros(n_samples, dtype=int)
    for _ in range(n_iterations):
        distances_to_centroids = np.linalg.norm(
            feature_matrix[:, None, :] - centroid_matrix[None, :, :], axis=2
        )
        new_labels = np.argmin(distances_to_centroids, axis=1)
        if np.array_equal(new_labels, cluster_labels):
            break
        cluster_labels = new_labels
        for cluster_index in range(n_clusters):
            members_mask = cluster_labels == cluster_index
            if members_mask.any():
                centroid_matrix[cluster_index] = feature_matrix[members_mask].mean(axis=0)
    return cluster_labels, centroid_matrix


def _hdbscan_lite(
    feature_matrix: np.ndarray,
    min_cluster_size: int = 3,
) -> np.ndarray:
    """Density-based clustering via single-linkage + flat cut.

    A lightweight stand-in for HDBSCAN: single-linkage on Euclidean distances,
    then cut at the gap that yields ``min_cluster_size``-friendly clusters.
    Points isolated below ``min_cluster_size`` are labelled -1 (noise).
    """
    n_samples = feature_matrix.shape[0]
    if n_samples < min_cluster_size * 2:
        return np.zeros(n_samples, dtype=int)
    condensed_distances = pdist(feature_matrix, metric="euclidean")
    linkage_matrix = linkage(condensed_distances, method="single")
    distances_sorted = np.sort(linkage_matrix[:, 2])
    gaps = np.diff(distances_sorted)
    if gaps.size == 0:
        return np.zeros(n_samples, dtype=int)
    largest_gap_position = int(np.argmax(gaps))
    cut_threshold = distances_sorted[largest_gap_position] + 0.5 * float(gaps[largest_gap_position])
    flat_labels = fcluster(linkage_matrix, t=cut_threshold, criterion="distance")
    label_counts = defaultdict(int)
    for label in flat_labels:
        label_counts[int(label)] += 1
    cluster_labels = np.array(
        [label if label_counts[int(label)] >= min_cluster_size else -1 for label in flat_labels],
        dtype=int,
    )
    return cluster_labels


def _adjusted_rand_index(labels_true: np.ndarray, labels_pred: np.ndarray) -> float:
    """ARI implementation (Hubert & Arabie 1985). Pure NumPy."""
    if labels_true.size != labels_pred.size or labels_true.size == 0:
        return float("nan")
    unique_true = np.unique(labels_true)
    unique_pred = np.unique(labels_pred)
    contingency = np.zeros((unique_true.size, unique_pred.size), dtype=int)
    for true_index, true_label in enumerate(unique_true):
        for pred_index, pred_label in enumerate(unique_pred):
            contingency[true_index, pred_index] = int(
                np.sum((labels_true == true_label) & (labels_pred == pred_label))
            )
    sum_comb_contingency = float(np.sum(contingency * (contingency - 1) / 2))
    row_sums = contingency.sum(axis=1)
    column_sums = contingency.sum(axis=0)
    sum_comb_rows = float(np.sum(row_sums * (row_sums - 1) / 2))
    sum_comb_columns = float(np.sum(column_sums * (column_sums - 1) / 2))
    total_samples = float(labels_true.size)
    total_pairs = total_samples * (total_samples - 1) / 2
    expected_index = (sum_comb_rows * sum_comb_columns) / total_pairs if total_pairs > 0 else 0.0
    max_index = (sum_comb_rows + sum_comb_columns) / 2
    denominator = max_index - expected_index
    if abs(denominator) < 1e-12:
        return 0.0
    return float((sum_comb_contingency - expected_index) / denominator)


def _normalised_mutual_information(labels_true: np.ndarray, labels_pred: np.ndarray) -> float:
    """NMI with arithmetic-mean normalisation. Pure NumPy."""
    if labels_true.size != labels_pred.size or labels_true.size == 0:
        return float("nan")
    n_samples = float(labels_true.size)
    unique_true, true_counts = np.unique(labels_true, return_counts=True)
    unique_pred, pred_counts = np.unique(labels_pred, return_counts=True)

    def _entropy(counts: np.ndarray) -> float:
        probabilities = counts / n_samples
        positive_probabilities = probabilities[probabilities > 0]
        return float(-np.sum(positive_probabilities * np.log(positive_probabilities)))

    entropy_true = _entropy(true_counts)
    entropy_pred = _entropy(pred_counts)

    mutual_information = 0.0
    for true_label in unique_true:
        for pred_label in unique_pred:
            joint_count = float(np.sum((labels_true == true_label) & (labels_pred == pred_label)))
            if joint_count == 0:
                continue
            joint_probability = joint_count / n_samples
            marginal_product = (
                float(np.sum(labels_true == true_label)) / n_samples
                * float(np.sum(labels_pred == pred_label)) / n_samples
            )
            mutual_information += joint_probability * np.log(joint_probability / marginal_product)

    denominator = 0.5 * (entropy_true + entropy_pred)
    if denominator < 1e-12:
        return 0.0
    return float(mutual_information / denominator)


def _build_feature_matrix() -> tuple[np.ndarray, list[str]]:
    """Concatenate (TS, SE, PDI, IDV, MAS, UAI, LTO, IVR) for states with full coverage."""
    iw_coords = load_inglehart_welzel()
    hofstede_profiles = load_hofstede()
    iso3_with_full_data: list[str] = []
    feature_rows: list[list[float]] = []
    for iso3 in sorted(set(iw_coords.keys()) & set(hofstede_profiles.keys())):
        hofstede_record = hofstede_profiles[iso3]
        if hofstede_record.coverage == "missing":
            continue
        if np.any(np.isnan(hofstede_record.values)):
            continue
        iw_record = iw_coords[iso3]
        feature_rows.append([
            float(iw_record.ts), float(iw_record.se),
            *[float(value) for value in hofstede_record.values],
        ])
        iso3_with_full_data.append(iso3)
    return np.asarray(feature_rows, dtype=float), iso3_with_full_data


def _huntington_labels_for_iso3s(iso3_list: list[str]) -> np.ndarray:
    """Argmax of w_s gives the Huntington-informed dominant civilization per ISO3."""
    centroids = compute_centroids()
    state_coords = project_states(centroids)
    civilization_ids = list(centroids.keys())
    civilization_to_index = {civ_id: index for index, civ_id in enumerate(civilization_ids)}
    labels: list[int] = []
    for iso3 in iso3_list:
        if iso3 not in state_coords:
            labels.append(-1)
            continue
        affinity = state_coords[iso3].affinity_vector
        weight_array = np.array(
            [affinity[civilization_id] for civilization_id in civilization_ids], dtype=float
        )
        labels.append(civilization_to_index[civilization_ids[int(np.argmax(weight_array))]])
    return np.asarray(labels, dtype=int)


def run_baseline_clustering() -> dict:
    feature_matrix, iso3_list = _build_feature_matrix()
    n_samples, n_features = feature_matrix.shape
    if n_samples < 11:
        return {
            "_meta": {"method": "baseline_clustering", "n_samples": n_samples, "note": "insufficient samples"},
            "kmeans": None,
            "hdbscan": None,
        }

    feature_means = feature_matrix.mean(axis=0)
    feature_stds = feature_matrix.std(axis=0) + 1e-9
    standardised_features = (feature_matrix - feature_means) / feature_stds

    huntington_labels = _huntington_labels_for_iso3s(iso3_list)

    kmeans_labels, _ = _kmeans_pure_numpy(standardised_features, n_clusters=11)
    hdbscan_labels = _hdbscan_lite(standardised_features, min_cluster_size=3)
    noise_mask = hdbscan_labels >= 0

    kmeans_ari = _adjusted_rand_index(huntington_labels, kmeans_labels)
    kmeans_nmi = _normalised_mutual_information(huntington_labels, kmeans_labels)
    hdbscan_ari = (
        _adjusted_rand_index(huntington_labels[noise_mask], hdbscan_labels[noise_mask])
        if noise_mask.any() else float("nan")
    )
    hdbscan_nmi = (
        _normalised_mutual_information(huntington_labels[noise_mask], hdbscan_labels[noise_mask])
        if noise_mask.any() else float("nan")
    )

    confusion_matrix_records: list[dict] = []
    for true_label in np.unique(huntington_labels):
        for pred_label in np.unique(kmeans_labels):
            count = int(np.sum((huntington_labels == true_label) & (kmeans_labels == pred_label)))
            if count > 0:
                confusion_matrix_records.append(
                    {
                        "huntington_label": int(true_label),
                        "kmeans_label": int(pred_label),
                        "count": count,
                    }
                )

    iso3_kmeans_mapping = [
        {"iso3": iso3, "huntington_label": int(huntington_labels[index]),
         "kmeans_label": int(kmeans_labels[index]),
         "hdbscan_label": int(hdbscan_labels[index])}
        for index, iso3 in enumerate(iso3_list)
    ]

    return {
        "_meta": {
            "method": "baseline_clustering",
            "n_samples": n_samples,
            "n_features": n_features,
            "feature_order": ["TS", "SE", "PDI", "IDV", "MAS", "UAI", "LTO", "IVR"],
        },
        "huntington_labels_argmax_w_s": True,
        "iso3_assignments": iso3_kmeans_mapping,
        "kmeans": {
            "k": 11,
            "adjusted_rand_index_vs_huntington": kmeans_ari,
            "normalised_mutual_information_vs_huntington": kmeans_nmi,
            "confusion_matrix_records": confusion_matrix_records,
        },
        "hdbscan_lite": {
            "min_cluster_size": 3,
            "n_clusters_found": int(len(set(hdbscan_labels[noise_mask]))),
            "n_noise_points": int(np.sum(~noise_mask)),
            "adjusted_rand_index_vs_huntington_non_noise": hdbscan_ari,
            "normalised_mutual_information_vs_huntington_non_noise": hdbscan_nmi,
        },
    }


def run_baseline_and_write() -> str:
    EMPIRICAL_DIR.mkdir(parents=True, exist_ok=True)
    payload = run_baseline_clustering()
    output_path = EMPIRICAL_DIR / "baseline_clustering.json"
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return str(output_path)
