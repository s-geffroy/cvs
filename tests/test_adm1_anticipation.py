"""ADM1 prepared-not-active enforcement."""
from __future__ import annotations

import json
import subprocess

from apps.basis_builder.paths import SCHEMAS_DIR


def test_adm1_schema_v2_present_and_valid() -> None:
    schema_path = SCHEMAS_DIR / "adm1_profile.v2.schema.json"
    assert schema_path.exists()
    schema = json.loads(schema_path.read_text())
    assert schema["properties"]["unit_type"]["const"] == "adm1"
    assert schema["properties"]["activation_status"]["const"] == "prepared_not_active"


def test_cli_rejects_adm1_with_prepared_not_active() -> None:
    result = subprocess.run(
        ["python", "-m", "apps.cli.main", "score", "FRA", "--unit-type", "adm1"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "prepared_not_active" in (result.stdout + result.stderr)
