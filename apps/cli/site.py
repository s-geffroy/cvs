"""civvec site [build|preview] subcommands."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import typer

from apps.basis_builder.paths import REPO_ROOT
from apps.site_builder.builder import render_all
from apps.site_builder.guards import scan_directory_for_gadm

app = typer.Typer(no_args_is_help=True)

DIST_DIR = REPO_ROOT / "dist"


@app.command("build")
def build(
    strict: bool = typer.Option(True, "--strict/--no-strict", help="Pass --strict to mkdocs."),
    clean: bool = typer.Option(True, "--clean/--no-clean", help="Wipe dist/ before building."),
) -> None:
    """Render Phase 1b pages then run `mkdocs build`."""
    if clean and DIST_DIR.exists():
        for entry in DIST_DIR.iterdir():
            if entry.is_dir():
                shutil.rmtree(entry)
            else:
                entry.unlink()
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    typer.echo("[site] rendering templates...")
    render_all()

    mkdocs_cmd: list[str] = ["mkdocs", "build"]
    if strict:
        mkdocs_cmd.append("--strict")
    mkdocs_cmd.extend(["-d", str(DIST_DIR)])
    typer.echo("[site] running: " + " ".join(mkdocs_cmd))
    result = subprocess.run(mkdocs_cmd, cwd=str(REPO_ROOT), check=False)
    if result.returncode != 0:
        raise typer.Exit(code=result.returncode)

    typer.echo("[site] scanning dist/ for forbidden GADM geometries...")
    offenders = scan_directory_for_gadm(DIST_DIR)
    if offenders:
        for path in offenders:
            typer.echo(f"  ✗ {path}")
        raise typer.Exit(code=2)

    typer.echo(f"[site] built into {DIST_DIR}")


@app.command("preview")
def preview(
    port: int = typer.Option(8080, "--port", help="Port for nginx preview."),
) -> None:
    """Print the docker command to preview the built site via nginx."""
    if not DIST_DIR.exists():
        typer.echo("dist/ missing — run `civvec site build` first.")
        raise typer.Exit(code=1)
    typer.echo(
        f"docker run --rm -p {port}:80 -v {DIST_DIR}:/usr/share/nginx/html:ro nginx:alpine"
    )
    typer.echo(f"then open http://localhost:{port}")
    sys.exit(0)
