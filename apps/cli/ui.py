"""civvec ui — launch the Streamlit interface."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import typer

app = typer.Typer(no_args_is_help=False, invoke_without_command=True)


@app.callback(invoke_without_command=True)
def launch(
    port: int = typer.Option(8501, "--port", help="Port to bind Streamlit on."),
    host: str = typer.Option("0.0.0.0", "--host", help="Address to bind."),  # nosec
) -> None:
    """Launch the multi-page Streamlit UI from inside the cvs/ container."""
    home_path = Path(__file__).resolve().parents[1] / "ui_streamlit" / "Home.py"
    if not home_path.exists():
        typer.echo(f"Streamlit Home.py not found at {home_path}")
        raise typer.Exit(code=1)
    cmd = [
        "streamlit",
        "run",
        str(home_path),
        "--server.address",
        host,
        "--server.port",
        str(port),
        "--server.headless",
        "true",
    ]
    typer.echo("launching: " + " ".join(cmd))
    os.execvp(cmd[0], cmd)
    sys.exit(0)
