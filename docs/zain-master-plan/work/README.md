# Session work files (2026-11-07 to 2026-11-08)

One-off scripts and intermediate data used to build this master plan, apply the review fixes, run the Z-03 exposure
scan and record founder decisions. They are kept here for provenance because the founder directed that all work live
in the repository. They are **not maintained tools**: most edit documents by exact string replacement against a past
state and will not re-run cleanly. The maintained tools are in `../tools/`.

Literals that the redaction scripts removed from the plan are replaced in these copies with `<user>` and
`<relay-host>`.

| Files | Purpose |
|---|---|
| `make_registries.py`, `make_registries_part2.py`, `export_v3.py`, `v3_export.json` | First build of the registry CSVs and the V3 task export they mirror |
| `apply_reviews.py`, `apply_reviews2.py`, `doc_edits*.py`, `scope_block.md`, `sec_sections.md`, `stats.py` | Review-fix and document edits; plan statistics |
| `z03_scan.py`, `z03_agg.py`, `z03_detail.py`, `z03_extra.py`, `z03_result.txt` | Z-03 scanner (in-memory, fingerprints only) and its aggregated output (18) |
| `record_*.py` | Status and decision records (Z-03, DEC-16, Z-25, visibility changes) |
