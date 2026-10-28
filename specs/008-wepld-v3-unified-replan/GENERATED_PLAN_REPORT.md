# Generated Plan Report

```text
GENERATED_BY = tools/plan_graph.py (deterministic; do not hand-edit; --check fails on drift)
INPUTS = 14_TASK_CATALOG.md, 23_ACCEPTANCE_TEST_REGISTRY.md, 13_REQUIREMENTS_REGISTER.md
TASK_ROWS = 180 (live 176, superseded 4)
REGISTERED_TESTS = 383; SUITES = 1; TEST_REFERENCES = 517
DECLARED_DEP_EDGES = 384; EFFECTIVE_EDGES = 405
UNMEASURED_TASKS = 2 (estimate 'MEASURE'; excluded from sums)
ESTIMATE_CLASS = reading-based ESTIMATE; nothing was built or run; this is not semantic verification
```

## 1. Validation

Fail-closed checks: see tools/plan_graph.py docstring; regression mutations in tools/test_plan_graph_mutations.py.

- No validation errors.

## 2. Effort by phase (person-weeks, ESTIMATE)

| Phase | Live tasks | Low | High | Unmeasured tasks |
|---|---|---|---|---|
| P−1′ | 2 | 0.15 | 0.15 | 0 |
| PF | 7 | 2.8 | 7.6 | 1 |
| P0 | 8 | 2.45 | 3.95 | 0 |
| P1 | 10 | 2.85 | 4.2 | 0 |
| P2-N | 3 | 0.4 | 0.4 | 0 |
| P2 | 23 | 11.9 | 20.35 | 1 |
| P3 | 37 | 40.9 | 63.65 | 0 |
| P4 | 9 | 6.2 | 10.2 | 0 |
| P5 | 31 | 36.9 | 57.1 | 0 |
| P6 | 19 | 36.75 | 65.25 | 0 |
| P7 | 8 | 9.2 | 14.7 | 0 |
| P8 | 6 | 10.3 | 17.8 | 0 |
| P9 | 5 | 13.5 | 22.5 | 0 |
| P10 | 5 | 4.7 | 9.3 | 0 |
| PD | 3 | 1 | 2 | 0 |

## 3. Release tiers (cumulative; 14 §16)

| Release | Tasks | Effort low–high (pw) | Unmeasured tasks | Elapsed low–high (weeks) | Critical path low–high (pw) |
|---|---|---|---|---|---|
| R0a | 7 | 2.8–7.6 | 1 | 2.8–7.6 | 2.3–6.1 |
| R0b | 17 | 6.1–12.9 | 2 | 6.1–12.9 | 3.8–8.35 |
| R0 | 44 | 15.15–29.15 | 2 | 15.2–29.1 | 6.3–12.8 |
| R1 | 84 | 60.3–97.3 | 2 | 84.6–199.5 | 24.35–40.4 |
| R2 | 130 | 104.55–167.6 | 2 | 152.7–375.3 | 29.3–49.6 |
| R3 | 149 | 141.3–232.85 | 2 | 209.2–538.4 | 30.05–49.6 |
| R4 | 157 | 150.5–247.55 | 2 | 223.4–575.1 | 30.05–49.6 |
| R5 | 163 | 160.8–265.35 | 2 | 239.2–619.6 | 30.05–49.6 |
| R6 | 168 | 174.3–287.85 | 2 | 260.0–675.9 | 31.3–53.6 |
| R7 | 173 | 179–297.15 | 2 | 267.2–699.1 | 31.3–53.6 |

Elapsed weeks = (effort inside R0) + (effort after R0)/(1 − u), A-1 capacity 1 pw per week, u = 0.35/0.60.
Tasks marked MEASURE are excluded: a release with unmeasured tasks has a LOWER BOUND, not an envelope.

## 4. Critical paths (high estimate, effective graph)

- **R0a**: `Q-00 → Q-01 → Q-02 → Q-04 → Q-05`
- **R0b**: `Q-00 → Q-01 → Q-02 → Q-04 → F-20 → F-06 → F-11`
- **R0**: `Q-00 → Q-01 → Q-02 → Q-04 → F-20 → F-02 → F-03 → F-14 → F-16 → L-01`
- **R1**: `Q-00 → Q-01 → Q-02 → Q-04 → F-20 → F-02 → F-03 → F-14 → F-16 → F-13 → C-01 → C-02 → C-03 → C-04 → C-10 → C-09 → C-20 → C-22 → V-01 → K-04 → K-08 → X-01`
- **R2**: `Q-00 → Q-01 → Q-02 → Q-04 → F-20 → F-02 → F-03 → F-14 → F-16 → F-13 → C-01 → C-02 → C-03 → C-04 → C-05 → Y-01 → Y-02 → Y-10 → Y-03 → Y-04 → Y-08 → E-03 → E-04 → E-07 → V-08`
- **R3**: `Q-00 → Q-01 → Q-02 → Q-04 → F-20 → F-02 → F-03 → F-14 → F-16 → F-13 → C-01 → C-02 → C-03 → C-04 → C-10 → C-09 → C-20 → C-22 → V-01 → K-04 → K-08 → K-07 → K-02 → K-03 → K-10 → K-11 → K-09`
- **R4**: `Q-00 → Q-01 → Q-02 → Q-04 → F-20 → F-02 → F-03 → F-14 → F-16 → F-13 → C-01 → C-02 → C-03 → C-04 → C-10 → C-09 → C-20 → C-22 → V-01 → K-04 → K-08 → K-07 → K-02 → K-03 → K-10 → K-11 → K-09`
- **R5**: `Q-00 → Q-01 → Q-02 → Q-04 → F-20 → F-02 → F-03 → F-14 → F-16 → F-13 → C-01 → C-02 → C-03 → C-04 → C-10 → C-09 → C-20 → C-22 → V-01 → K-04 → K-08 → K-07 → K-02 → K-03 → K-10 → K-11 → K-09`
- **R6**: `Q-00 → Q-01 → Q-02 → Q-04 → F-20 → F-02 → F-03 → F-14 → F-16 → F-13 → C-01 → C-02 → C-03 → C-04 → C-05 → Y-01 → Y-02 → Y-10 → Y-03 → Y-04 → Y-08 → E-03 → E-04 → E-07 → V-08 → W-01 → W-02`
- **R7**: `Q-00 → Q-01 → Q-02 → Q-04 → F-20 → F-02 → F-03 → F-14 → F-16 → F-13 → C-01 → C-02 → C-03 → C-04 → C-05 → Y-01 → Y-02 → Y-10 → Y-03 → Y-04 → Y-08 → E-03 → E-04 → E-07 → V-08 → W-01 → W-02`

## 5. Components

| Component | Tasks | Total pw | Inside R2 pw |
|---|---|---|---|
| Zain Code Review | 11 | 13.25–19.75 | 8–11.5 |
| Zain Engineering System | 8 | 11.2–17.2 | 9.2–14.2 |
| Zain Plan Mode | 10 | 7.1–11.5 | 7.1–11.5 |
| Zain Browser | 11 | 17–27 | 12.5–20 |
| DeskGate | 9 | 6.5–11 | 5.1–8.2 |

## 6. Optional distribution track (PD)

| Task | Title | Est |
|---|---|---|
| F-19 | Windows code signing for public distribution (OV/EV certificate + cloud HSM, jsign) | 0.5–1 |
| I-12 | macOS notarization (Apple Developer Program, paid) | 0.3–0.5 |
| N-05 | Trademark counsel opinion + SAIP filing for the product name (paid; required before public | 0.2–0.5 |

## 7. Traceability summary

REGISTERED 99 · FREE_TEXT_ONLY 0 · GAP 0 (details: 15)
