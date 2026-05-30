# 04 — ADM1 Preparation Policy

ADM1 is **prepared but inactive**.

## Prepared elements

```json
[
  "adm1_profile_schema",
  "geometry_provenance_schema",
  "adm_boundary_source_policy",
  "outputs_adm1_prepared_directory",
  "cli_stub",
  "future_migration_notes"
]
```

## Boundary source strategy

```json
{
  "primary_source": "geoBoundaries",
  "rendering_and_lightweight_fallback": "Natural Earth",
  "restricted_research_fallback": "GADM"
}
```

## GADM policy

GADM must not be default.

```json
{
  "usage": "research_internal_fallback_only",
  "commercial_output_allowed": false,
  "redistribution_allowed": false,
  "must_track_license": true
}
```
