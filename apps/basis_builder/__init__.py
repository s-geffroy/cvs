"""Builder for the civilizational vector basis (B_vec).

Reads canonical Inglehart-Welzel and Hofstede data, computes civilization
centroids (mu, sigma) in B_viz and B_score, projects each state, derives the
affinity vector via softmax inverse-distance, and computes the per-state
weighted second moment M(s) of the centroid-state displacements.
"""
