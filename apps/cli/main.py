"""Civvec CLI entry point."""
from __future__ import annotations

import typer

from . import basis as basis_module
from . import empirical as empirical_module
from . import site as site_module
from . import ui as ui_module

app = typer.Typer(
    name="civvec",
    help="Civilizational Vector State CLI (cvs/ v3 — two bases, second moment M(s), distance algebra).",
    no_args_is_help=True,
)

app.add_typer(basis_module.app, name="basis", help="Build and validate B_vec.")
app.add_typer(ui_module.app, name="ui", help="Launch the Streamlit UI in Docker.")
app.add_typer(site_module.app, name="site", help="Render and build the GitHub Pages site (Phase 1b/2).")
app.add_typer(empirical_module.app, name="empirical", help="Run empirical analyses (sensitivity, baseline, external validation).")


@app.command("score")
def score(
    iso3: str = typer.Argument(..., help="ISO3 of the unit to score."),
    unit_type: str = typer.Option("state", "--unit-type", help="state | adm1"),
) -> None:
    """Score a single unit. ADM1 is intentionally prepared-not-active in V1."""
    if unit_type == "adm1":
        typer.echo(
            "{\"error\": \"prepared_not_active\", "
            "\"see\": \"docs/04_adm1_preparation_policy.md\"}"
        )
        raise typer.Exit(code=2)
    if unit_type != "state":
        typer.echo(f"{{\"error\": \"unknown_unit_type\", \"got\": \"{unit_type}\"}}")
        raise typer.Exit(code=2)
    typer.echo(
        f"score for {iso3} not implemented in V1 — use `civvec basis build` "
        "then inspect packages/civvec_core/basis/state_coordinates.json"
    )


if __name__ == "__main__":
    app()
