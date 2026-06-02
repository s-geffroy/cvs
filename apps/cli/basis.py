"""civvec basis [build|validate] subcommands."""
from __future__ import annotations

import json
from pathlib import Path

import typer
from jsonschema import validate

from apps.basis_builder.centroids import (
    compute_centroids,
    inject_centroid_coords_into_taxonomy,
    write_centroids,
)
from apps.basis_builder.geometries import (
    NATURAL_EARTH_ADM0_PATH,
    fetch_and_tag_natural_earth_admin0,
)
from apps.basis_builder.moments import compute_all_second_moments, write_second_moments
from apps.basis_builder.paths import (
    BASIS_DIR,
    CIVILIZATION_CENTROIDS_PATH,
    MACRO_CIVILIZATIONS_V2_PATH,
    SCHEMAS_DIR,
    STATE_COORDINATES_PATH,
    STATE_MOMENTS_PATH,
)
from apps.basis_builder.projector import project_states, write_state_coordinates

app = typer.Typer(no_args_is_help=True)


@app.command("build")
def build(
    skip_moments: bool = typer.Option(False, "--skip-moments", help="Do not compute M(s)."),
) -> None:
    """Compute centroids, project states, derive affinity vectors, compute second moments M(s)."""
    typer.echo("[1/4] computing civilization centroids...")
    centroids = compute_centroids()
    write_centroids(centroids)
    typer.echo(f"      wrote {CIVILIZATION_CENTROIDS_PATH.relative_to(BASIS_DIR.parents[2])}")

    typer.echo("[2/4] injecting mu_viz/mu_score into macro_civilizations.v2.json...")
    inject_centroid_coords_into_taxonomy(centroids)

    typer.echo("[3/4] projecting states...")
    state_coords = project_states(centroids)
    write_state_coordinates(state_coords)
    typer.echo(f"      wrote {STATE_COORDINATES_PATH.relative_to(BASIS_DIR.parents[2])}")

    if skip_moments:
        typer.echo("[4/4] skipped second-moment computation (per --skip-moments)")
        return
    typer.echo("[4/4] computing state second moments M(s)...")
    moments = compute_all_second_moments()
    write_second_moments(moments)
    typer.echo(f"      wrote {STATE_MOMENTS_PATH.relative_to(BASIS_DIR.parents[2])}")


@app.command("fetch-geometries")
def fetch_geometries(
    force: bool = typer.Option(False, "--force", help="Re-download even if local file exists."),
) -> None:
    """Fetch Natural Earth ADM0 110m, tag provenance, write data_sources/natural_earth/."""
    target_path = fetch_and_tag_natural_earth_admin0(force_refresh=force)
    typer.echo(f"[geometries] wrote {target_path.relative_to(BASIS_DIR.parents[2])}")
    typer.echo(f"[geometries] expected: {NATURAL_EARTH_ADM0_PATH}")


@app.command("coverage-report")
def coverage_report() -> None:
    """Génère le rapport de couverture des 193 États membres de l'ONU."""
    from apps.basis_builder.coverage_report import write_coverage_report

    json_path, markdown_path = write_coverage_report()
    typer.echo(f"[coverage] wrote {json_path.relative_to(BASIS_DIR.parents[2])}")
    typer.echo(f"[coverage] wrote {markdown_path.relative_to(BASIS_DIR.parents[2])}")


@app.command("validate")
def validate_artefacts() -> None:
    """Validate all generated artefacts against their JSON Schemas."""
    pairs: list[tuple[Path, str, str | None]] = [
        (MACRO_CIVILIZATIONS_V2_PATH, "macro_civilizations.schema.json", None),
    ]
    failures: list[str] = []
    for json_path, schema_name, top_key in pairs:
        schema = json.loads((SCHEMAS_DIR / schema_name).read_text())
        document = json.loads(json_path.read_text())
        document_to_validate = document if top_key is None else document[top_key]
        try:
            validate(instance=document_to_validate, schema=schema)
            typer.echo(f"✓ {json_path.name} valid against {schema_name}")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{json_path.name}: {exc}")
            typer.echo(f"✗ {json_path.name} FAILED: {exc}")
    if failures:
        raise typer.Exit(code=1)
