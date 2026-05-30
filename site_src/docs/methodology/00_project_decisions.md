# 00 — Project Decisions

## Core choice

The project builds a civilizational affiliation vector, but V1 is now **State-first**.

## Active V1

```json
{
  "unit_type": "state",
  "data_sources": "public_aggregate_sources_only",
  "implementation": "python_library_cli_streamlit_reviewer",
  "runtime": "docker",
  "storage": "sqlite_index_plus_json_artifacts",
  "exports": ["json", "markdown", "geojson"]
}
```

## Prepared but inactive

```json
{
  "adm1_profiles": true,
  "adm1_geometries": true,
  "adm1_geometry_provenance": true,
  "adm1_source_comparability": true,
  "adm1_cli_stub": true
}
```

## Explicit override

Earlier planning considered ADM1 profile outputs in V1. This package supersedes that: **ADM1 will come later**.
