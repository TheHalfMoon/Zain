# Astro Round-2 Findings — Disposition (revision 4)

```text
REVIEWED_COMMIT = 024ed89ac08e91eba8b98f92a874d880a4156b7f (handoff 529c1016); Astro: 15 findings (11 High, 4 Medium);
                  original C-1 reopened; verdicts R0a CONDITIONAL, R0b DO NOT APPROVE, R0 CONDITIONAL, R1 DO NOT APPROVE
INPUT = ASTRO_ROUND_2_REVIEW.md and validator-adversarial-results.json (founder's Windows outputs; read in full)
REPAIR = planning documents + validator + mutation regressions only; nothing built or run; no T3 build executed
STATUS_VALUES = RESOLVED (plan defect removed; evidence named; runtime still unproven unless stated) ·
                DEFERRED WITH EXPLICIT GATE · BLOCKED WITH EVIDENCE
EXECUTED_CHECKS (actual results at the repair commit):
  python -I tools/plan_graph.py --check           → exit 0; tasks=176 tests=383 suites=1 errors=0; 99 REGISTERED, 0 GAP
  python -I tools/test_plan_graph_mutations.py    → exit 0; 26 cases (baseline + 18 Astro + 7 new), 0 failures
LIMIT = the validator checks declared structure; it does not infer capabilities from fixture prose (semantic sampling stays
        an independent-review task).
```

## Summary

| ID | Sev | Status | Correction (where) | Regression evidence |
|---|---|---|---|---|
| A2-01 | H | RESOLVED (plan); runtime gated by Q-04/Q-05 | full build DAG with donor-secret/relay/WSL/repository-guard nodes; provider-disabled bundling before packaging (24 §1, §3; Q-04) | PKG-01, CI-02 |
| A2-02 | H | RESOLVED | public artifacts = distribution; R0a local/private only; R0b removals (F-20) and license gate before distribution; access-controlled channel (22 §5; F-11; Q-00) | PKG-02, LIC-01, LIC-02; GOV-14 |
| A2-03 | M | RESOLVED | Q-00..Q-06 all T2 with independent review; Q-00 admission record (14 PF) | validator tier check (T0/T1/T2 enumerated) |
| A2-04 | M | RESOLVED (plan); completeness proven at Q-02 | identity/runtime-path and donor-egress inventories incl. profile migration, CLI env, protocol, lock, endpoint discovery, WSL; paired provider control; estimate cap removed (24 §4) | FWB-02..04, EGR-02, EGR-03 |
| A2-05 | H | RESOLVED | validator rewritten fail-closed; release-set closure and cumulative nesting; drift check; permanent mutations (tools/) | all 8 previously accepted mutations now rejected |
| A2-06 | H | RESOLVED (declared graph) | V1-17 = suite of CC-T01..CC-T04 (CC-T05 stays V-04/R2); CC-T04 registered; A11Y-02 split (A11Y-04 R1); PEM-GEN moved to R1 via C-28; R1 review advisory only; ES-AT-06/08 split | mutations V1_17_add_actual_CC_T05_prereq, R1_require_generic_revocation, suite_cycle, suite_member_unregistered |
| A2-07 | H | RESOLVED (claim narrowed) | R1 enumerated surface per provider; ENFORCED = target until PEM passes; claim generated from passing cells; response-form normalization; pinned runtimes; isolated ambient config (18 §4; 21 §3; C-09, C-28, X-01) | PEM-CLA-05, PEM-CDX-05/06, PEM-GEN-01..04, CLM-01 |
| A2-08 | H | RESOLVED (design); Codex/ACP not qualified as confidential reviewer routes in R1 | read broker + all built-in tools disabled + scrubbed HOME/config/history + review proxy for model egress; git symlinks never followed (19 §2; K-08) | ZCR-T29..T33 |
| A2-09 | H | RESOLVED (design) | execution outcome separated from content observation; operation-unique object identity / reflog / responses; pending remote ops stay UNKNOWN; stale reads rejected (17 §1; C-26) | REC-06..REC-10, W6 oracle |
| A2-10 | H | RESOLVED | "tree provenance" → authorized-content equivalence (content only); mandatory scopes from Core policy; `COMPLETED_CONTENT_EQUIVALENT`; R1 makes no completion decision (17 §2.2–2.3; C-05, C-23) | COV-08, COV-09 |
| A2-11 | H | RESOLVED | agent browser tools disabled through R1; R2 proxy adds coalescing, revocation, headless parity, fail-closed, hostile-localhost and port-authorization tests (19 §1; Y-01, Y-10) | BRW-P01, BRW-AT-30..35 |
| A2-12 | H | RESOLVED (design) — Windows prevention; Linux/macOS detect-only stated; gate FG-04 | object-authority fs-gate: fresh-file replacement vs hardlinks, ancestors held without FILE_SHARE_DELETE, name rules, final-target check, no truncation (19 §3; H-08) | FSG-05..FSG-09 |
| A2-13 | M | RESOLVED | level-specific claim templates; A3 makes no user-presence claim; downgrade needs assertion (17 §4.5; C-13; 21 §3 item 3) | APR-08, APR-09, CLM-02 |
| A2-14 | M | RESOLVED | standard SSH-signed tag verified by `git verify-tag` (namespace git); canonical payload; replay ledger (20 §3) | GV-21, GV-22, GV-23; GV-09 guard text corrected |
| A2-15 | M | RESOLVED | PASS requires install, launch, terminal, worktree, diff, real provider turn; separate FEASIBILITY_COMPLETE_WITH_FAILURES and PARTIAL_SMOKE_NO_CREDENTIALS; Q-06 fix-to-pass (24 §5) | FWB-01 |

Not BLOCKED: none. DEFERRED gates inside RESOLVED items are explicit: C-00 FG-01..05 (Windows mechanisms), Q-04/Q-05 (build
DAG feasibility), Q-02 (inventory completeness).

## Detail

### A2-01 — build dependency chain and SDK removal
- **Evidence (Astro):** release.yml L503, L704; release-desktop.yml L217, L383; build-desktop-artifact.ts L977;
  ClaudeAdapterV2.ts L24; cli-external-packages.ts L3; apps/server/vite.config.ts L106. Re-read here: release.yml
  L51–55 (repository guard), L102–135 (task-cache secret), L388–459 (`relay_public_config`, Cloudflare secret), L502–590
  (`build_bundle`, `js-bundle`), L706–728 (Windows caller); release-desktop.yml L196–220, L377–436, L444–458, L505–506, L660–690.
- **Correction:** Q-04 is now the five-node DAG in 24 §3 (install → sanitized bundle → staging → verify → private artifact)
  with relay/tracing/task-cache/guard/publish removed and WSL disabled for R0a (re-enabled with overlays in R0). Claude and
  Cursor providers are disabled at registration **before** bundling; F-20 makes the SDK optional for R0b.
- **Regression:** PKG-01 inspects bundle module provenance, unpacked ASAR and nested archives and requires boot with the
  providers absent; CI-02 records cold-cache resources.

### A2-02 — distribution and license sequencing
- **Correction:** 22 §5 defines distribution (public artifacts/logs count; expiry is not access control). R0a never leaves
  the machine or a private repository; Q-00 records the shipped closure before the first build; R0b requires F-20 removals,
  LIC-01 over the packaged closure, N-01 and an access-controlled channel before any tester receives a build.
- **Regression:** PKG-02, LIC-01, LIC-02; new requirement GOV-14.

### A2-03 — tiers
- **Correction:** Q-00..Q-06 are T2; independent T2 review is an R0a approval condition (R0A_FEASIBILITY_READINESS A3, A7).

### A2-04 — identity and egress inventories
- **Correction:** 24 §4 lists every known site (DesktopStatePaths L13/L19, DesktopUserData L34, DesktopCliShim L53,
  ElectronProtocol L16–17, publicConfig.ts L85, scripts/lib/public-config.ts L26) plus inventory items (lock, endpoint
  discovery, child env, WSL); no estimate cap. Forbidden-sink tests are paired with a positive provider control.

### A2-05 — validator fail-open
- **Correction:** tools/plan_graph.py: unknown ID-like tokens rejected; dependency and test ranges validated (missing,
  reversed, mixed prefixes); duplicate task/test ids; enumerated kinds and tiers; negative specification completeness;
  free-text negative wording anywhere; release definitions must be cumulative; every release set closed under effective
  dependencies; `--check` regenerates outputs in memory and fails on drift; deterministic tie-breaking (a nondeterministic
  critical-path tie found during this repair was fixed).
- **Executed regression:** 26/26 cases behave as required (tools/test_plan_graph_mutations.py output at the repair commit).

### A2-06 — hidden cycle and late R1 tests
- **Correction:** registry "Suite composition" with nested prerequisites; V1-17 excludes CC-T05; CC-T04 registered;
  A11Y-04 (C-14, R1); C-28 brings PEM-GEN into R1; ZCR-Q stays R2 and R1 review is advisory only (21 §3 item 8); ES-AT-06
  depends on V-04; ES-AT-08 split from ship enforcement (ES-AT-17).

### A2-07 — provider claim
- **Correction:** 18 §4 enumerates what Core decides in R1 per provider and what it does not; 21 §3 item 1 is generated
  from passing cells only; C-09 pins runtimes, isolates CODEX_HOME/CLAUDE_CONFIG_DIR/MCP config and normalizes all approval
  response forms; C-28 qualifies grant lifecycle in R1.

### A2-08 — reviewer read boundary
- **Correction:** 19 §2: Claude reviewer with built-in tools disabled and a manifest-only read broker, scrubbed environment,
  loopback review proxy for model egress (cloud only with per-run approval). Codex and ACP are not confidential reviewer routes
  in R1.

### A2-09 — reconciliation
- **Correction:** 17 §1 rules R-1..R-3; object-identity-based outcomes for fs ops (fresh-file replacement gives an
  operation-unique file id), reflog entries for refs, responses/markers for PRs, pinned-sha merge logic, stale-read rule.

### A2-10 — provenance and scopes
- **Correction:** 17 §2.2–2.3 as summarized; C-05 holds mandatory scopes; C-23 tests COV-08/09.

### A2-11 — browser
- **Correction:** 19 §1 claims table and R2 policies; Y-01 disables agent browser tools in R1.

### A2-12 — fs-gate
- **Correction:** 19 §3 object-authority table; H-08 acceptance; FG-04 must include FSG-05..09 fixtures.

### A2-13 — approval claims
- **Correction:** 17 §4.5 templates; C-13 acceptance; APR-08/09; CLM-02.

### A2-14 — co-sign format
- **Correction:** 20 §3 (git verify-tag, canonical payload, replay ledger); GV-21..23.

### A2-15 — working build definition
- **Correction:** 24 §5 status semantics; Q-05/Q-06; FWB-01 strict oracle.

## Reassessment of the original 18 round-1 findings (after revision 4)

| Original | Astro round 2 | Revision 4 | Current status |
|---|---|---|---|
| C-1 | Not resolved | A2-05/06 repairs; mutations C20_add_W2b, Y08_add_BRW23, V1-17 and PEM-GEN cases rejected | RESOLVED for the declared graph; semantic completeness remains review work |
| H-1 | Partial | ACE vs provenance; policy-owned scopes | RESOLVED (design) |
| H-2 | Not resolved | enumerated R1 surface; C-28 in R1 | RESOLVED (claim narrowed); cells unproven until PEM pass |
| H-3 | Partial | agents disabled in R1; R2 policies | RESOLVED for R1; R2 gated by FG-05/BRW-AT-25..35 |
| H-4 | Not resolved | 17 §1 rewritten | RESOLVED (design) |
| H-5 | Acceptable, gated | unchanged design; FG-01 hard gate | DEFERRED WITH EXPLICIT GATE (C-00 FG-01, PH-01..07) |
| H-6 | Partial | claim templates | RESOLVED (design); A1 availability gated by FG-02/03 |
| H-7 | Not resolved | read boundary per route | RESOLVED (design) for Claude route; other routes not qualified |
| H-8 | Partial | object-authority semantics | RESOLVED (design); Windows prevention gated by FG-04 |
| H-9 | Plan-level accepted | unchanged; canonical encoding and latest-anchor discovery noted for C-03/C-19 admission | RESOLVED (plan) |
| H-10 | Deferral acceptable | signature format fixed | DEFERRED WITH EXPLICIT GATE (G-08/G-05/GV-18) |
| H-11 | Partial | private-repo or local build at $0; provider-route note; public-distribution rules consistent | RESOLVED (plan) |
| H-12 | Arithmetic accepted, confidence limited | MEASURE tasks; weeks display; lower bounds | RESOLVED (arithmetic); confidence still limited |
| M-1 | Reopen early tiers | Q-00 + F-20 + 22 §5 | RESOLVED for R0a/R0b; later closures DEFERRED WITH EXPLICIT GATE |
| M-2 | Plan-level accepted | client key persisted before dispatch (17 §6 unchanged) | RESOLVED (plan) |
| M-3 | Partial | unchanged accounting; semantic sampling stays manual | DEFERRED WITH EXPLICIT GATE (per-phase admission review) |
| M-4 | Partial | parser bypasses closed; ZCR-T29..33; reviewer quality stays R2 with advisory R1 | RESOLVED (plan) |
| L-1 | Resolved | — | RESOLVED |
