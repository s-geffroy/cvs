"""civvec empirical [sensitivity|baseline|validate|all] — empirical analyses for docs 12-14."""
from __future__ import annotations

import typer

from apps.empirical.baseline_clustering import run_baseline_and_write
from apps.empirical.external_validation import run_external_validation_and_write
from apps.empirical.sensitivity import run_all_sensitivity_analyses

app = typer.Typer(no_args_is_help=True)


@app.command("sensitivity")
def sensitivity_command() -> None:
    """LOO on archetypes + softmax beta sweep + hybrid weights sweep."""
    paths_written = run_all_sensitivity_analyses()
    for analysis_name, output_path in paths_written.items():
        typer.echo(f"[empirical/sensitivity] {analysis_name} -> {output_path}")


@app.command("baseline")
def baseline_command() -> None:
    """k-means + HDBSCAN-lite on raw WVS+Hofstede features vs Huntington taxonomy."""
    output_path = run_baseline_and_write()
    typer.echo(f"[empirical/baseline] wrote {output_path}")


@app.command("validate")
def validate_command() -> None:
    """Spearman correlations w_s vs Pew/WGI/FSI with bootstrap 95% CIs."""
    output_path = run_external_validation_and_write()
    typer.echo(f"[empirical/validate] wrote {output_path}")


@app.command("all")
def all_command() -> None:
    """Run sensitivity + baseline + external validation in one go."""
    typer.echo("[empirical] running sensitivity analyses...")
    sensitivity_paths = run_all_sensitivity_analyses()
    for analysis_name, output_path in sensitivity_paths.items():
        typer.echo(f"  {analysis_name} -> {output_path}")
    typer.echo("[empirical] running baseline clustering...")
    baseline_path = run_baseline_and_write()
    typer.echo(f"  baseline -> {baseline_path}")
    typer.echo("[empirical] running external validation...")
    validation_path = run_external_validation_and_write()
    typer.echo(f"  validation -> {validation_path}")
    typer.echo("[empirical] done.")
