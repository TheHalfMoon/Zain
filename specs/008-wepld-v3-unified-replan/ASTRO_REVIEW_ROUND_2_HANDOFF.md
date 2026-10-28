# Astro Review — Round 2 Handoff

```text
REVIEWER = Astro (independent). Challenge the repair; do not endorse it.
REPOSITORY = https://github.com/TheHalfMoon/Zain (PUBLIC)
BRANCH = docs/v3-unified-replan-20261027
PLANNING_COMMIT = 024ed89ac08e91eba8b98f92a874d880a4156b7f   (revision 3.1: round-1 repair + first-working-build split)
REPAIR_COMMIT = add02fbc596dfa461e73f8acbd9a005010ad4f0f   (line numbers in ASTRO_FINDINGS_DISPOSITION.md refer to it)
HANDOFF_COMMIT = the commit that adds this file; it changes only this file, STATUS_LEDGER.md and README.md
ROUND_1 = b94505988e05c15a55f7e2e1c9bf19bc23bed121 — DO NOT APPROVE (1 C, 12 H, 4 M, 1 L)
BASE = main @ 0a843a2c0913236d9c93b31abb0d54bbdb023f23
SCOPE = planning documents only; nothing implemented, built or run; no runtime claim is made
DO_NOT = modify the repository, open/merge PRs, trigger hosted reviewers, touch TheHalfMoon/Zain-LLM
APPROVAL_ASKED = (a) R0a/R0b source-based builds with the narrow claims in 24 §5; (b) R1 "Zain Trusted Starter" scope +
                 exact claims (21 §3) — not the whole roadmap
```

## 1. What changed since round 1

| Area | New / changed artifact |
|---|---|
| Dependency/test graph | `23_ACCEPTANCE_TEST_REGISTRY.md` (338 tests with prerequisites and phase); `tools/plan_graph.py` (validator + generator); `GENERATED_PLAN_REPORT.md`; `15_TRACEABILITY_MATRIX.md` regenerated |
| Trust boundaries | `17_TRUST_BOUNDARY_SPEC.md` (reconciliation contracts, coverage, ProcessHost, approvals, ledger envelope, operation ids) |
| Providers | `18_PROVIDER_ENFORCEMENT_MATRIX.md` |
| Browser / review / files | `19_COMPONENT_SECURITY_REVISIONS.md` |
| Governance | `20_GOVERNANCE_EQUIVALENCE.md` |
| Releases / cost / calendar | `21_RELEASE_TIERS_AND_COST.md`; 14 §16 release membership; PD paid track |
| Sources | `22_SOURCE_ADMISSION_QUALIFICATION.md` |
| Tasks | 14: C-00, C-23..C-27, H-08, Y-10, K-10, K-11, X-01, G-08, N-05, F-19, I-12; K/Y/C rows rewritten |
| Decisions | ADR-020..024 + amendments to ADR-007/011/014/015/018/019 |
| Dispositions | `ASTRO_FINDINGS_DISPOSITION.md` (all 18 findings, evidence lines, re-review criteria) |
| Time to first build (rev 3.1) | `24_FIRST_WORKING_BUILD.md`: R0a First Working Build (Q-01..Q-05), R0b Tester Build, R0 Qualified; 45-task audit; double counting removed; Monaco/C-00/Core packaging moved to R1 |

Reported statuses: 16 RESOLVED (several design-level with an early feasibility gate C-00 and a pre-declared weaker
claim), 2 DEFERRED WITH EXPLICIT GATE (H-10 full governance inventory = G-08; M-1 post-v1 source closures), 0 BLOCKED.

## 2. Deterministic checks to run first

```bash
python -I specs/008-wepld-v3-unified-replan/tools/plan_graph.py --check
```

Expected at PLANNING_COMMIT: exit 0; `tasks=170 tests=343 errors=0 coverage={'REGISTERED': 98, 'FREE_TEXT_ONLY': 0, 'GAP': 0}`.
The script is read-only in `--check` mode. Suggested adversarial checks: add W2b to C-20's tests (expect a prerequisite
error); give Y-08 the test BRW-AT-23 (expect an execution-phase error); make a mandatory task depend on F-19 (expect a PD
error); delete a guard cell in a negative row of 23 (expect an error).

## 3. Questions requiring independent verification

1. **Graph completeness:** does the registry capture every *implicit* prerequisite? A test may need a capability not
   named in its prerequisites (the validator only checks what is declared). Sample 20 registry rows against their source
   suites (R14 §8, R15 §9, R16 §8, R17 §11, R18 §5, 09).
2. **Coverage model (17 §2):** is tree provenance a sound and useful basis for `COMPLETED_TRUSTED` before P8? Can an
   UNMEDIATED write survive replay-equality (e.g. a write identical to a mediated one)? Is "declared critical scope"
   gameable by omission?
3. **Provider matrix (18):** verify the cited lines (Claude canUseTool L9265–9536; Codex L687–727, L5039–5396;
   OpenCode L632–655; Pi L1251–1259, L2701–2702) at t3code@36d4d711 and challenge every ENFORCED cell, especially Claude
   PreToolUse ordering and Codex known-safe auto-run.
4. **Reconciliation contracts (17 §1):** find a counterexample to any NOT_APPLIED rule (concurrent writers, monotonicity
   of merge state, leased-push semantics).
5. **ProcessHost (17 §3):** is `PROC_THREAD_ATTRIBUTE_JOB_LIST` + `KILL_ON_JOB_CLOSE` with ConPTY feasible and sufficient on
   Windows 11? Are the listed escapes complete? Is the quiescence attestation sound under PID reuse?
6. **Approvals (17 §4):** is a Core-owned native window calling webauthn.dll a real improvement over the renderer, given
   Core is spawned by the Server? Is the A1/A2/A3 versioning honest in every claim?
7. **Browser egress (19 §1):** does a Chromium session proxy with `<-loopback>` capture every request source listed
   (service workers, beacons, prefetch, WebSocket)? Is connecting to the validated IP achievable for HTTPS CONNECT? Are the
   residuals (domain fronting, DNS prefetch) correctly bounded?
8. **Review confidentiality (19 §2):** can any OCR tool or delegated-reviewer path read outside the snapshot manifest?
9. **fs-gate (19 §3):** is the Windows design (NtCreateFile relative opens, reparse rejection, rename by handle) correct,
   including ADS and 8.3 names?
10. **Ledger (17 §5):** does the envelope cover every authoritative field; are anchor/interval claims exact?
11. **Governance (20):** is the seed inventory faithful to v72 L650–785; is the co-sign binding sufficient; is deferring
    the full inventory to G-08 acceptable given no retirement before GV-18?
12. **Releases and claims (21):** is R1 the smallest release with defensible claims? Is every R1 claim (21 §3) backed by
    an R1 task and registered test? Is anything outside R1 implied?
13. **Numbers:** recompute from 14 independently; check the calendar formula and the upkeep assumption (35–60%).
14. **Zero-cost path:** can any mandatory gate require payment (reviewers, signing, counsel, models)?
15. **Preservation:** confirm no founder-requested capability (T3 + Orca IDE, Code Review incl. OCR and Continue rule
    import, PStack + E2E, AI Hero skills in Plan Mode, Zain Browser, DeskGate, Trusted Core + Brain, Claude-equivalent
    capabilities) was dropped rather than scheduled.
16. **Honesty:** anything presented as verified that is documentation- or reading-only?
17. **First Working Build (24 §1–§4):** is the upstream evidence (daily Windows installers from T3's release.yml, cross-built
    on Ubuntu with a Windows verify job) correctly characterized, and are conditions C1–C6 complete? Is anything in Q-01..Q-05
    missing that is genuinely required for the app to run?
18. **Task audit (24 §6):** challenge each TEST/QUAL/DEFER classification of the 45 former R0 tasks; in particular whether
    G-05 must precede F-01, whether F-14 belongs in qualified R0, and whether any DEFER weakens a claim actually made.
19. **Double counting (24 §8):** are the reductions justified (F-13 → 0, B-03, F-01, F-02, F-03, F-12), or is work now
    missing rather than de-duplicated?
20. **Claims per milestone (24 §5):** are R0a/R0b claims narrow enough; are public-repo CI artifacts (≤ 1 day, SDKs excluded)
    a redistribution risk; does R1 keep every round-1 security requirement unchanged?

## 4. Report format

Same as round 1 (ASTRO_REVIEW_HANDOFF.md §10): ID, severity, location (file:line at PLANNING_COMMIT), finding, evidence,
impact, fix; then what is solid; then a verdict on the R1 scope specifically.
