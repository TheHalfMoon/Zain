# Astro Round-1 Findings — Disposition

```text
REVIEWED_COMMIT = b94505988e05c15a55f7e2e1c9bf19bc23bed121 (verdict: DO NOT APPROVE; 1 C, 12 H, 4 M, 1 L)
REPAIR = planning documents only; nothing implemented, built or run
STATUS_VALUES = RESOLVED (plan defect removed and a deterministic or reviewable artifact proves it) ·
                DEFERRED WITH EXPLICIT GATE (plan corrected; remaining evidence produced by a named task/test before the
                dependent work or claim) · BLOCKED WITH EVIDENCE (cannot be resolved in planning)
VALIDATOR = python -I tools/plan_graph.py --check  → exit 0, errors 0 (165 live tasks, 338 registered tests,
            98 requirements REGISTERED, 0 FREE_TEXT_ONLY, 0 GAP)
LINES = file:line refer to the repair commit named in ASTRO_REVIEW_ROUND_2_HANDOFF.md
```

## Summary

| ID | Status | Primary evidence |
|---|---|---|
| C-1 | RESOLVED | tools/plan_graph.py; 23; 14:105, 14:124, 14:219–220, 14:265–266; GENERATED_PLAN_REPORT §1 |
| H-1 | RESOLVED (design; unimplemented) | 17:53–101; ADR:208; 14:107 (C-23); 23 COV-01..07 |
| H-2 | RESOLVED (plan); OpenCode/Pi EXCLUDED until C-24 | 18:12–60; 14:94 (C-09), 14:108 (C-24); 23 PEM-* |
| H-3 | RESOLVED (claims bounded) with gate FG-05 → Y-10 | 19:11–50; 14:260, 14:267; R17:386; 23 BRW-AT-25..29 |
| H-4 | RESOLVED | 17:24–51; 14:110 (C-26); 09:49; R17 replay row; 23 REC-01..05 |
| H-5 | RESOLVED (design) with early gate C-00 FG-01 | 17:102–126; 14:48 (C-00), 14:109 (C-25); 07 §6 floor; 23 PH-01..07 |
| H-6 | RESOLVED (design); A1 availability gated by C-00 FG-02/03 | 17:127–172; ADR:222; 14:98 (C-13); 23 APR-01..07 |
| H-7 | RESOLVED | 19:51–74; R14:3, R14:260; 14:216, 14:220, 14:222–223; 23 ZCR-T26, T27, T29 |
| H-8 | RESOLVED (design) with gate FG-04 | 19:75–96; 14:281 (H-08); R18:278–290; 23 FSG-01..04, DG-N03, DG-N15 |
| H-9 | RESOLVED | 17:173–188; 07 §4 chain line; 09:26 (T10b); 23 LED-01..06 |
| H-10 | DEFERRED WITH EXPLICIT GATE | 20 (inventory seeded with v72 oracles 1–10); 14:30, 14:32, 14:35 (G-08); 23 GV-01..20 |
| H-11 | RESOLVED | 21:59–74; 10:21; 14:73 (F-11), 14:199–205 (PD); validator PD rule |
| H-12 | RESOLVED | GENERATED_PLAN_REPORT §2–§4; master plan §5 generated block; 21:75–79; 10:51 |
| M-1 | DEFERRED WITH EXPLICIT GATE (v1 decisions made; post-v1 closures gated) | 22:29–49; 14 F-02 acceptance; 23 LIC-01 |
| M-2 | RESOLVED | 17:189–200; 07 §3 propose row; R18:194; 23 OPID-01/02, DG-N16 |
| M-3 | RESOLVED (listed gaps); census remains inventory | 13:16, 13:23, 13:38–39; 03F:53 (§2b); 03F CL-A-008, CL-D-008, CL-D-012 rows; 15 |
| M-4 | RESOLVED | 23 (all negatives: guard, mutant, fixture, failure); validator rule; 13:77 (SEC-17); 09 §1b; ZCR-Q01..Q04; R18 DG-N13 |
| L-1 | RESOLVED | R14:97–439 (`.zainide/review`); ZAIN_NAMING_MIGRATION §2 data-dir row |

No finding is BLOCKED in planning. Findings whose mechanism is unproven on Windows carry an early feasibility gate (C-00,
P1) with a pre-declared weaker claim if the gate fails — the plan never silently assumes the mechanism works.

## Details

### C-1 — Hidden dependency cycles — RESOLVED

- **Astro evidence:** C-20→C-22→M-01→M-02→C-20 via W2b/W3; K-07↔K-08 via ZCR-T16/T17; Y-08↔Y-09 via BRW-AT-23/24.
- **Repair:**
  1. New `23_ACCEPTANCE_TEST_REGISTRY.md`: every coded test (338) has implementation prerequisites and an execution phase.
  2. New `tools/plan_graph.py` builds the effective graph = declared deps + test prerequisites, and rejects cycles,
     prerequisites that are not declared ancestors of the task running the test, tests scheduled before their prerequisites'
     phase, later-phase dependencies, non-closed releases, and dependencies on the paid PD track.
  3. Moves: W2b/W3 → M-02 (14:120), R2/R9 → M-07 (14:124), W7 → V-04 (14:133); C-20 runs only R1, R3–R8, R10, R11, W1, W2,
     W4–W6, W9 (14:105). K-08 delegated mode now precedes K-07, which depends on it (14:219–220). Y-08 runs BRW-AT-01..22,
     25..29; BRW-AT-23/24 run in Y-09 (14:265–266).
  4. The validator found further hidden edges that the declared graph missed, all fixed: I-05 ran AT-01..05 (Design Studio,
     P7) → DM-01..03 (14:148); Y-08 needed Y-03..Y-07; L-02 needed C-08, C-09, C-12, H-08 for N1–N8; C-12 needed C-08 for
     T2; C-20 needed C-09 for R5/R8/R10; Y-01 needed C-12; V-04 needed M-01; H-05 needed C-13; N-04 depended on a later phase.
- **Re-review criteria:** run `python -I tools/plan_graph.py --check` (exit 0); inspect GENERATED_PLAN_REPORT §1; mutate a
  test prerequisite in 23 (e.g. give W2b prerequisite M-02 and add it to C-20) and confirm the validator reports the cycle.

### H-1 — Descendant execution coverage — RESOLVED (design)

- **Repair:** 17 §2 separates launch authorization from coverage per execution context (fs/net/proc ∈ COVERED/CONTAINED/
  UNKNOWN). Shells, interpreters, test runners, CLI agents and provider-internal tools are UNKNOWN (17:57–66). Hash diffs
  are observations, never coverage. `COMPLETED_TRUSTED` requires tree provenance plus known coverage for declared critical
  scopes; otherwise `COMPLETED_WITH_UNKNOWN_COVERAGE` (17:79–94). Plan Mode rule 17 §2.4. DeskGate process tools marked as
  launch authorization only (R18:194). ADR-020. Task C-23 (14:107), V-04 acceptance (14:133), L-03 (COV-07).
- **Re-review criteria:** confirm no remaining text equates MEDIATED launch with coverage (grep "count toward Trusted
  Completion"); confirm R1 claims (21 §3 item 4) state the limitation; check COV-01..07 mutants.

### H-2 — Provider approval bypasses — RESOLVED (plan)

- **Repair:** 18 matrix for Claude, Codex, ACP, OpenCode, Pi × file read/write, shell, network, MCP, subagents, mode
  change, approval caching, plan mode. Pi cache (adapter L1251–1259, L2701–2702) and OpenCode always-allow rules
  (L632–655) cited; both EXCLUDED from the trusted tier until patched and qualified by C-24 (14:108). Core-held grant
  semantics (18 §3). Codex `ApprovedForSession` never sent; Claude relies on PreToolUse with allow rules/permissive modes
  removed. PR-02 reworded (13:16); SEC-23; ADR-021.
- **Re-review criteria:** verify cited adapter lines at t3code@36d4d711; challenge each ENFORCED cell; confirm OpenCode/Pi
  cannot appear in the R1 trusted tier (21 §3 item 1).

### H-3 — Browser egress — RESOLVED (claims bounded), gate FG-05

- **Repair:** 19 §1: partition proxy with `<-loopback>`, proxy-side resolution and connection to the validated IP,
  per-hop redirect validation, WebRTC non-proxied UDP disabled; navigation gate demoted to approval layer. Claims by stage
  (19:37–45): agent lanes loopback-only until BRW-AT-25..29 pass. New task Y-10 (14:267); Y-03 rewritten (14:260); R17 §8.6
  marked superseded (R17:386); SEC-20 reworded. Residuals stated (domain fronting, DNS prefetch).
- **Re-review criteria:** check BRW-AT-25..29 cover fetch/XHR/WS/workers/beacons/subresources/redirects/DNS change; check
  no document claims origin confinement before Y-10.

### H-4 — External-effect reconciliation — RESOLVED

- **Repair:** 17 §1 per-operation contract table (fs, git commit/push, PR create/merge, CI/API calls, idempotency-keyed
  calls, browser classes, process/terminal, model calls, continuation fires) with rules R-1..R-3: absence never inferred
  from current remote state unless monotonic; `browser.input.text` → NEVER; push knowledge vs retry safety separated.
  C-26 (14:110); W6 revised (09:49); REC-01..05.
- **Re-review criteria:** challenge each NOT_APPLIED cell for a counterexample writer.

### H-5 — Windows process fencing — RESOLVED (design), gate C-00 FG-01

- **Repair:** 17 §3: native ProcessHost; Job Object assigned at creation (`PROC_THREAD_ATTRIBUTE_JOB_LIST`), no
  breakaway, restricted handle inheritance, `KILL_ON_JOB_CLOSE`, ConPTY via the same path; quiescence attestation before
  retry; escapes (WMI, Task Scheduler, services) keep effects UNKNOWN; Orca `taskkill` reference only (07 floor (b)
  rewritten; 16 ownership row). C-25 (14:109), C-00 (14:48) with NO-GO fallback; PH-01..07. ADR-024.
- **Re-review criteria:** assess FG-01 as a real feasibility test; check the NO-GO claim text.

### H-6 — WebAuthn trust boundary — RESOLVED (design); A1 gated by FG-02/03

- **Repair:** 17 §4: threats separated (forgery, deceptive display, compromised Server stated as not mitigated), canonical
  binding incl. scope, principal, expiry, epoch, display-text digest, approval level; Core-owned `zain-approve` surface
  with webauthn.dll (A1); enrollment, recovery code, credential add/replace/remove; versioned fallbacks A2/A3 recorded and
  shown (17:162–172). C-13 rewritten (14:98); APR-01..07; ADR-022; FO-13.
- **Re-review criteria:** check APR-01 fixture models a compromised renderer; check level never silently becomes A1.

### H-7 — OCR egress — RESOLVED

- **Repair:** 19 §2: immutable snapshot from git objects (untracked files excluded by construction), secret screen,
  manifest allowlist enforced in delegated mode (PreToolUse) and engine mode (patch Z-P7), disclosure budget,
  local-only default, cloud only via mediated proxy with per-run approval (K-09). "No write tools" rationale withdrawn
  (R14:260). K-04 snapshot builder (14:216); K-08 (14:220); K-10/K-11 (14:222–223); SEC-27; ZCR-T26, T27, T29.
- **Re-review criteria:** confirm every engine tool (not only FileReader) is in Z-P7 scope at K-03 admission.

### H-8 — DeskGate filesystem races — RESOLVED (design), gate FG-04

- **Repair:** 19 §3 fs-gate per OS (Windows NtCreateFile relative to held handles + reparse rejection + final-path check;
  Linux openat2; macOS O_NOFOLLOW walk), handle-relative rename; single write path for ACP fs, DeskGate, Plan Mode,
  review fixes. H-08 (14:281); C-08 depends on it; DG-N03 rewritten to test the final boundary, DG-N15 added
  (R18:278–290); FSG-01..04; ADR-024.
- **Re-review criteria:** check the race tests run an attacker thread during the operation, not between proposal and dispatch.

### H-9 — Ledger integrity — RESOLVED

- **Repair:** 17 §5 envelope hash over v, seq, ts, kind, project_id, subject_id, principal, payload digest, prev_hash;
  partition export boundaries; anchors prove only the anchored prefix; unanchored interval reported as not detectable by
  the chain. 07 §4 chain line superseded; T10b rewritten (09:26); C-03/C-19 (14 rows); LED-01..06; SEC-08.
- **Re-review criteria:** confirm no text claims anchors detect suffix truncation.

### H-10 — Governance equivalence — DEFERRED WITH EXPLICIT GATE

- **Repair:** 20: accepted-PR replay demoted to non-regression (GV-19); property inventory seeded with v72 oracles 1–10
  @0a843a2 L650–785 (GP-01..GP-10); co-sign binding (repo id, base, head, tree, path digest, scope, expiry); negative corpus
  GV-01..GV-18; G-08 inventory task (14:35) before G-03 (14:30); G-05 retires only per property with signed record (14:32).
  GOV-13.
- **Why deferred:** the full inventory of 169 successor scripts is a P0 task (G-08), not done in planning. **Gate:** no
  baseline workflow is retired before G-05 passes GV-18 for every inventoried property.

### H-11 — Zero-cost path — RESOLVED

- **Repair:** 21 §4 table; paid items isolated in PD (N-05 counsel/filing, F-19 signing, I-12 notarization; 14:199–205);
  F-11 is unsigned with documented limits (14:73); N-01 free screening + working-name rule (14:54); 10:21 claim rewritten;
  reviewer route named per phase or `REVIEW_BLOCKED` (FO-12). Validator rejects any mandatory dependency on PD.
- **Re-review criteria:** search for any mandatory task requiring payment.

### H-12 — Effort, calendar, critical path — RESOLVED

- **Repair:** all numbers generated from the 165 live task rows (GENERATED_PLAN_REPORT §2–§6); master plan §5 is a generated
  block; hand-written §13/§14 removed from 14; P6 discrepancy and non-existent edges removed (paths computed from the graph);
  upkeep 35–60% applied after R0 (21 §5; 10:51); 08/00/02/10/FOUNDER numbers replaced by references.
- **Result:** see GENERATED_PLAN_REPORT §3 (values change only by regenerating). Revision 3.1 (24) split R0 into R0a/R0b/R0 and
  removed double counting; the numbers in this disposition are therefore not restated.

### M-1 — Source admission — DEFERRED WITH EXPLICIT GATE

- **Repair:** 22 admission levels L1–L4; v1 decisions: heic-to REMOVE, electron-webauthn REMOVE, @cursor/sdk STRIP, jszip
  MIT election, dompurify Apache-2.0 election, Claude SDK not bundled; codex-core dependency of windows-sandbox-service →
  reference only; bubblewrap not vendored; S-01 raised to 4–8 pw; D7 rewrite (I-02 2–3.5 pw). LIC-01 license gate.
- **Gate:** post-v1 closures (Orca beyond depth 2, native sidecars, codex symbols, Excalidraw fonts, LSP client) at each
  task's admission (22 §3).

### M-2 — DeskGate operation identity — RESOLVED

- **Repair:** 17 §6 durable logical operation ids per principal + mission + client key; attempt ids separate;
  `OPERATION_INPUT_CONFLICT`; R18:194 superseded; 07 §3 propose row; OPID-01/02, DG-N16.

### M-3 — Semantic acceptance gaps — RESOLVED (listed gaps)

- **Repair:** PR-09 terminal now M at P2/P3 with TERM-01/02 (13:23; F-16, C-12); PR-24 split with A11Y-01/02 at P2 and
  PR-24b (13:38–39); PR-02 provider tiers (13:16); scheduling labelled ADAPTATION (03F §2b; CL-D-012 row); PDF row
  (CL-A-008) and CL-D-008 re-routed; census declared inventory (13 §E, 03F §2b); traceability now distinguishes
  REGISTERED vs FREE_TEXT_ONLY (15).
- **Re-review criteria:** sample M requirements and judge whether their registered tests exercise the requirement.

### M-4 — Mutation and reviewer quality — RESOLVED

- **Repair:** SEC-17 reworded (13:77); every negative in 23 names guard, mutant, fixture, observable failure (validator
  rule; free-text negatives anywhere are errors); DG-N13 mutant added; reviewer quality separated into ZCR-Q01..Q04
  (held-out defects, false positives, injection suppression, engine vs delegated); 09 §1b.

### L-1 — Configuration path — RESOLVED

- **Repair:** `.zainide/` everywhere active (R14 Z-P4, verify.json, ZCR-T03); `~/.zain-ide` user dir; `%APPDATA%\Zain`.
