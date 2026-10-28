# Generated Plan Report

```text
GENERATED_BY = tools/plan_graph.py (deterministic; do not hand-edit)
INPUTS = 14_TASK_CATALOG.md, 23_ACCEPTANCE_TEST_REGISTRY.md, 13_REQUIREMENTS_REGISTER.md
TASK_ROWS = 169 (live 165, superseded 4)
REGISTERED_TESTS = 338; TEST_REFERENCES_RESOLVED = 464
DECLARED_DEP_EDGES = 366; EFFECTIVE_EDGES_INCL_TEST_PREREQS = 384
VALIDATION_ERRORS = 0; WARNINGS = 0
ESTIMATE_CLASS = reading-based ESTIMATE; nothing was built or run
```

## 1. Validation

Checks: dependency ids exist; no superseded dependency; acyclic effective graph (declared deps + test
prerequisites); no dependency on a later phase; every coded test reference is registered; every test's
prerequisites are declared ancestors of (or equal to) the task that runs it; registry phase = latest
prerequisite phase; every negative registry entry names guard, mutant, fixture and observable failure; no
free-text negative test anywhere; every release is closed under effective dependencies; no mandatory
task depends on the optional distribution track (PD).

- No validation errors.

## 2. Effort by phase (person-weeks, ESTIMATE)

| Phase | Live tasks | Low | High |
|---|---|---|---|
| P−1′ | 2 | 0.15 | 0.15 |
| P0 | 8 | 2.45 | 3.95 |
| P1 | 10 | 3.15 | 4.75 |
| P2-N | 3 | 0.4 | 0.4 |
| P2 | 22 | 15.65 | 25.1 |
| P3 | 35 | 39.15 | 60.4 |
| P4 | 9 | 6.2 | 10.2 |
| P5 | 31 | 36.65 | 56.6 |
| P6 | 18 | 36.25 | 64.5 |
| P7 | 8 | 9.2 | 14.7 |
| P8 | 6 | 10.3 | 17.8 |
| P9 | 5 | 13.5 | 22.5 |
| P10 | 5 | 4.7 | 9.3 |
| PD | 3 | 1 | 2 |
| **All mandatory (excl. PD)** | 162 | 177.75 | 290.35 |

## 3. Release tiers (cumulative; R-tiers defined in 14 §16)

| Release | Tasks | Effort low–high (pw) | Elapsed low–high (years) | Critical path (high est.) pw |
|---|---|---|---|---|
| R0 | 45 | 21.8–34.35 | 0.4–0.7 | 8.6–13.8 |
| R1 | 77 | 60.05–91.85 | 1.6–3.4 | 25.4–38.9 |
| R2 | 120 | 103.8–161.55 | 2.8–6.8 | 30.6–48.6 |
| R3 | 138 | 140.05–226.05 | 3.9–9.9 | 31.1–48.6 |
| R4 | 146 | 149.25–240.75 | 4.2–10.6 | 31.1–48.6 |
| R5 | 152 | 159.55–258.55 | 4.5–11.4 | 31.1–48.6 |
| R6 | 157 | 173.05–281.05 | 4.9–12.5 | 32.6–52.6 |
| R7 | 162 | 177.75–290.35 | 5.0–13.0 | 32.6–52.6 |

Elapsed time = (effort inside R0) + (effort after R0) / (1 − u), at A-1 capacity of 1 pw per calendar week;
u = upkeep share of capacity = 0.35 (low) / 0.60 (high) per 10 §3–§7. No acceleration, contingency or leave is
included. A-1 is unvalidated until P1–P3 actuals exist; re-run this script with measured capacity.

## 4. Critical paths (computed on the effective graph)

- **R0** (high-estimate chain): `G-08 → G-03 → B-01 → B-02 → B-03 → C-00 → B-07 → F-01 → F-02 → F-03 → F-17 → F-16 → L-01`
- **R1** (high-estimate chain): `G-08 → G-03 → B-01 → B-02 → B-03 → C-00 → B-07 → F-01 → F-02 → F-03 → F-17 → F-16 → C-01 → C-02 → C-03 → C-04 → C-10 → C-09 → C-20 → C-22 → V-01 → K-04 → K-08 → X-01`
- **R2** (high-estimate chain): `G-08 → G-03 → B-01 → B-02 → B-03 → C-00 → B-07 → F-01 → F-02 → F-03 → F-17 → F-16 → C-01 → C-02 → C-03 → C-04 → C-26 → C-12 → Y-01 → Y-02 → Y-10 → Y-03 → Y-04 → Y-08 → E-03 → E-04 → E-07 → V-08`
- **R3** (high-estimate chain): `G-08 → G-03 → B-01 → B-02 → B-03 → C-00 → B-07 → F-01 → F-02 → F-03 → F-17 → F-16 → C-01 → C-02 → C-03 → C-04 → C-26 → C-12 → Y-01 → Y-02 → Y-10 → Y-03 → Y-04 → Y-08 → E-03 → E-04 → E-07 → V-08`
- **R4** (high-estimate chain): `G-08 → G-03 → B-01 → B-02 → B-03 → C-00 → B-07 → F-01 → F-02 → F-03 → F-17 → F-16 → C-01 → C-02 → C-03 → C-04 → C-26 → C-12 → Y-01 → Y-02 → Y-10 → Y-03 → Y-04 → Y-08 → E-03 → E-04 → E-07 → V-08`
- **R5** (high-estimate chain): `G-08 → G-03 → B-01 → B-02 → B-03 → C-00 → B-07 → F-01 → F-02 → F-03 → F-17 → F-16 → C-01 → C-02 → C-03 → C-04 → C-26 → C-12 → Y-01 → Y-02 → Y-10 → Y-03 → Y-04 → Y-08 → E-03 → E-04 → E-07 → V-08`
- **R6** (high-estimate chain): `G-08 → G-03 → B-01 → B-02 → B-03 → C-00 → B-07 → F-01 → F-02 → F-03 → F-17 → F-16 → C-01 → C-02 → C-03 → C-04 → C-26 → C-12 → Y-01 → Y-02 → Y-10 → Y-03 → Y-04 → Y-08 → E-03 → E-04 → E-07 → V-08 → W-01 → W-02`
- **R7** (high-estimate chain): `G-08 → G-03 → B-01 → B-02 → B-03 → C-00 → B-07 → F-01 → F-02 → F-03 → F-17 → F-16 → C-01 → C-02 → C-03 → C-04 → C-26 → C-12 → Y-01 → Y-02 → Y-10 → Y-03 → Y-04 → Y-08 → E-03 → E-04 → E-07 → V-08 → W-01 → W-02`

For a solo founder total effort, not the critical path, drives elapsed time (no parallel capacity).

## 5. Components

| Component | Tasks | Total pw | Inside R2 (v1) pw |
|---|---|---|---|
| Zain Code Review | 11 | 13–19.25 | 8.25–11.75 |
| Zain Engineering System | 8 | 11.2–17.2 | 9.2–14.2 |
| Zain Plan Mode | 10 | 7.1–11.5 | 7.1–11.5 |
| Zain Browser | 11 | 17–27 | 12.5–20 |
| DeskGate | 9 | 6.5–11 | 5.1–8.2 |

## 6. Optional distribution track (PD, paid; never a dependency of a mandatory task)

| Task | Title | Est |
|---|---|---|
| F-19 | Windows code signing for public distribution (OV/EV certificate + cloud HSM, jsign) | 0.5–1 |
| I-12 | macOS notarization (Apple Developer Program, paid) | 0.3–0.5 |
| N-05 | Trademark counsel opinion + SAIP filing for the product name (paid; required before public | 0.2–0.5 |

## 7. Traceability summary

REGISTERED 98 · FREE_TEXT_ONLY 0 · GAP 0 (details: 15)
