# Astro Review — Round 3 Handoff

```text
REVIEWER = Astro (independent). Challenge the repair; do not endorse it.
REPOSITORY = https://github.com/TheHalfMoon/Zain (PUBLIC) · BRANCH = docs/v3-unified-replan-20261027
PLANNING_COMMIT = 68211bc7d3ff9c62cbe4c476f26b70e9e98f71f1   (revision 4: all repair content)
HANDOFF_COMMIT = the commit adding this file; it changes only this file, STATUS_LEDGER.md and README.md
PREVIOUS = round 2 reviewed 024ed89a (handoff 529c1016); round 1 reviewed b9450598
BASE = main @ 0a843a2c0913236d9c93b31abb0d54bbdb023f23
SCOPE = planning documents, validator and mutation tests only; no product code; no T3 build executed; nothing published
DO_NOT = modify the repository, open/merge PRs, trigger hosted reviewers, touch TheHalfMoon/Zain-LLM
APPROVAL_ASKED = (1) R0A_FEASIBILITY_READINESS.md alone (founder-only feasibility, no distribution);
                 (2) separately, R1 "Zain Trusted Starter" planning with generated claims (21 §3)
DIFF_NOTE = several files were normalized from CRLF to LF; review with `git diff --ignore-cr-at-eol 529c1016 68211bc7`
```

## 1. Commands and actual results at PLANNING_COMMIT (run locally on 2026-10-29)

```bash
python -I specs/008-wepld-v3-unified-replan/tools/plan_graph.py --check
```

Result: exit 0 — `tasks=176 tests=383 suites=1 errors=0 coverage={'REGISTERED': 99, 'FREE_TEXT_ONLY': 0, 'GAP': 0}`
(run three times; deterministic after fixing a hash-order critical-path tie found during the repair).

```bash
python -I specs/008-wepld-v3-unified-replan/tools/test_plan_graph_mutations.py
```

Result: exit 0 — `cases=26 failures=0`: the baseline passes, and every mutation is rejected. The mutations are all 18 from your
round 2 (including the eight that were previously accepted) plus seven new ones: a reversed dependency range, a release
member removed so that closure breaks, an unregistered suite member, a suite cycle, an uppercase negative kind, an
unparseable estimate, and traceability drift. The harness works on temporary copies that are deleted afterwards.

## 2. Changed-file map (529c1016 → 68211bc7)

| File | Change | Findings |
|---|---|---|
| tools/plan_graph.py | rewritten fail-closed: id/range/kind/tier/estimate parsing, suite composition, release-set closure + cumulative nesting, free-text negatives anywhere, drift check, deterministic paths, MEASURE tasks | A2-05, A2-06, C-1 |
| tools/test_plan_graph_mutations.py | new permanent regressions (26 cases) | A2-05 |
| 14_TASK_CATALOG.md | PF rewritten (Q-00..Q-06, T2); F-20, F-21, F-22, C-28 added; F-13 reinstated (R1); dependencies/acceptance for F-01, F-02, F-06, F-11, F-14, F-17, C-05, C-09, C-13, C-23, C-24, C-26, H-08, K-08, Y-01, Y-03, Y-10, X-01, G-03, V-04; §16 releases | A2-01..04, 06..08, 10..15 |
| 23_ACCEPTANCE_TEST_REGISTRY.md | §13 additions (LIC-02, FWB-01..04, EGR-02/03, CI-02, PKG-01/02, CC-T04, A11Y-04, PEM-CLA-05, PEM-CDX-05/06, REC-06..10, COV-08/09, APR-08/09, FSG-05..09, ZCR-T30..33, BRW-AT-30..35, GV-21..23, CLM-01/02); suite composition; revised LIC-01, SEC12-01, A11Y-02, PEM-GEN, ES-AT-06/08, W6, BRW-P01, ZCR-T29, GV-09 | A2-01..15 |
| 17_TRUST_BOUNDARY_SPEC.md | §1 reconciliation (outcome vs content), §2.2–2.3 ACE + policy-owned scopes + COMPLETED_CONTENT_EQUIVALENT, §4.5 claim templates | A2-09, A2-10, A2-13 |
| 18_PROVIDER_ENFORCEMENT_MATRIX.md | status rule; §4 enumerated R1 surface | A2-07 |
| 19_COMPONENT_SECURITY_REVISIONS.md | §1 R1 agents disabled + R2 policies; §2 read boundary per route + review proxy; §3 fs-gate object authority | A2-08, A2-11, A2-12 |
| 20_GOVERNANCE_EQUIVALENCE.md | §3 co-sign format (git verify-tag, canonical payload, replay ledger) | A2-14 |
| 21_RELEASE_TIERS_AND_COST.md | R0a/R0b rows; §3 generated claim templates | A2-02, A2-07, A2-13 |
| 22_SOURCE_ADMISSION_QUALIFICATION.md | §5 distribution rules | A2-02, M-1 |
| 24_FIRST_WORKING_BUILD.md | rewritten: evidence, DAG, inventories, status semantics, claims, audit changes | A2-01..04, A2-15 |
| R0A_FEASIBILITY_READINESS.md | new approval packet | Track A |
| ASTRO_ROUND_2_FINDINGS_DISPOSITION.md | new: 15 findings + reassessment of original 18 | all |
| 13_REQUIREMENTS_REGISTER.md | GOV-14 (no unqualified distribution) | A2-02 |
| 07, ADR.md, 10, FOUNDER_DECISION_RECORD.md (FO-14 revised, FO-15), ZAIN_V3_MASTER_PLAN.md, README.md, STATUS_LEDGER.md | consistency and amendments | D |
| GENERATED_PLAN_REPORT.md, 15_TRACEABILITY_MATRIX.md | regenerated | — |

## 3. Remaining limitations (stated, not hidden)

1. Nothing was built or run. T3 buildability at the pin is unestablished (successful Release runs skipped the build jobs).
2. R0a effort is a lower bound (Q-06 is MEASURE); no date is promised.
3. Windows mechanisms (Job Objects with ConPTY, Core-owned WebAuthn surface, fs-gate semantics, session-proxy coverage)
   are unproven until C-00; the plan states weaker claims for each NO-GO.
4. The validator checks declared structure; it cannot infer missing capabilities from fixture prose.
5. fs-gate prevention of ancestor relocation is Windows-only; Linux/macOS are detect-only (R3).
6. Only the Claude route is planned as a confidential reviewer in R1; Codex/ACP review is not qualified for confidential use.
7. The full governance inventory (G-08) and per-phase semantic admission review remain explicit gates.

## 4. Questions requiring independent verification

1. Does the validator still accept any malformed or semantically inconsistent input? Try new mutations beyond the 26.
2. Is the R0a build DAG (24 §3) complete and buildable without donor secrets and without paid runners? Is disabling WSL
   for R0a acceptable, and is it fully restored later?
3. Does provider-disabled bundling plus PKG-01 (module provenance, ASAR, nested archives) actually prove SDK absence?
4. Are the distribution rules (22 §5, PKG-02, GOV-14) sufficient; is a private build repository on GitHub Free a genuine
   access boundary for R0a?
5. Are the identity/egress inventories (24 §4) complete enough to start, and do EGR-02/03 avoid both leaks and over-blocking?
6. Is the R1 enumerated provider surface (18 §4) accurate at the pin, and are the generated claim templates (21 §3) safe
   when some cells fail?
7. Is the Claude reviewer read boundary (built-in tools disabled, broker, scrubbed environment, review proxy) enforceable
   by the pinned SDK, or can startup or other paths still read outside the manifest?
8. Do the reconciliation rules (17 §1) survive new counterexamples (rename races, file-id reuse, reflog expiry, GitHub
   eventual consistency)?
9. Is ACE with policy-owned scopes (17 §2) free of omission or vacuity gaps?
10. Is disabling agent browser tools in R1 complete (all inherited `preview_*` tools and any other agent-reachable browser
    path)?
11. Is the fs-gate object-authority design (19 §3) correct on Windows (share modes on ancestors, hardlink handling,
    FileRenameInfoEx semantics, 8.3 and case-sensitivity rules)?
12. Is the co-sign format (20 §3) verifiable with stock Git and resistant to replay?
13. Do the release sets (14 §16) still preserve every founder capability with its source, task and acceptance tests?
14. Verdicts requested separately: R0a readiness packet; R0b; qualified R0; R1.

## 5. Report format

As in rounds 1–2: ID, severity, location (file:line at PLANNING_COMMIT), finding, evidence, impact, fix; what is solid;
separate verdicts.
