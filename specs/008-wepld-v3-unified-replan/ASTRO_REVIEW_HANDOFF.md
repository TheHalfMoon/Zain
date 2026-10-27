# Astro Review Handoff — Zain V3 Master Plan

```text
REVIEWER = Astro (independent). You are asked to CHALLENGE this plan, not endorse it.
REPOSITORY = https://github.com/TheHalfMoon/Zain (ID 1334408699, PUBLIC; formerly TheHalfMoon/wepld)
BRANCH = docs/v3-unified-replan-20261027
PLANNING_COMMIT = the branch tip at review start — record its exact SHA in your report (see STATUS_LEDGER for the
                  last commit written by the planner)
BASE = main @ 0a843a2c0913236d9c93b31abb0d54bbdb023f23
PACKAGE = specs/008-wepld-v3-unified-replan/   (legacy directory name)
SCOPE = planning documents only; no product code was written, copied or transplanted
DO_NOT = modify TheHalfMoon/Zain-LLM (separate private project); trigger hosted reviewers (egress policy); merge anything
```

## 1. Executive summary

Zain (formerly WePLD) is planned as a local-first, multi-vendor desktop IDE + AI workspace whose Rust **Zain Trusted Core**
decides which mediated effects are allowed, records outcomes (including unknown ones), keeps project memory across
models, and decides what counts as done. The plan **forks T3 Code** (shell, server, orchestration, providers), **ports
selected Orca modules**, keeps WePLD's tested Rust core, and adds five first-class components: **Zain Code Review**
(Alibaba OCR fork), **Zain Engineering System** (PStack-derived loop + Playwright E2E), **Zain Plan Mode**
(mattpocock/skills + T3 plan mode + Core read-only profile), **Zain Browser** (one BrowserController, four lanes) and
**DeskGate** (Desktop Commander tools as Core-mediated adapters). Vercel Workflow and durable-harness are patterns only.

Bottom-up ESTIMATE (computed from 154 task rows): **v1 ≈ 91–141 person-weeks; all phases ≈ 160–259**. For one founder this
is multi-year; the plan proposes release tiers R0 Workbench (≈20–30 pw) → R1 Trusted (≈50–76) → R2 v1 (≈91–141).
Verdict: **CONDITIONAL GO** with gates G2–G5 and founder decisions FO-8 (trademark), FO-9 (E2E source), FO-10 (scope).

## 2. Document index

| Area | Documents |
|---|---|
| Entry | `README.md`, `ZAIN_V3_MASTER_PLAN.md`, this file |
| Decision | `00_EXECUTIVE_PRODUCT_DECISION.md`, `FOUNDER_DECISION_RECORD.md`, `ADR.md` (ADR-001…019) |
| Architecture | `07_TARGET_ARCHITECTURE_AND_UX.md`, `05_VERCEL_WORKFLOW_DURABILITY_REA.md`, `16_ZAIN_PRODUCT_COMPONENTS.md` |
| Copy First | `06_SOURCE_TRANSPLANT_MATRIX.md` (D1–D36, §3b notices), `research/R11_T3_FILE_MANIFEST.md`, `research/R12_DONOR_FILE_MANIFEST.md`, `research/R14–R18` (component file tables) |
| Plan | `13_REQUIREMENTS_REGISTER.md` (90), `14_TASK_CATALOG.md` (154 rows, §13 computed totals, §14 critical path, §15 contingencies), `15_TRACEABILITY_MATRIX.md` (generated), `08_MIGRATION_AND_IMPLEMENTATION_ROADMAP.md` |
| Quality | `09_RECOVERY_SECURITY_AND_EVALUATION.md`, `10_COST_RISK_AND_MAINTENANCE.md`, `GAP_LIST.md`, `ASSUMPTIONS_AND_UNKNOWNS.md` |
| Donor REA | `02` T3 (R02), `03D` Orca (R03D), `04` Amp (R04, R10), `05` Vercel (R05), registry (R06), IDE/debug/platform (R13) |
| Claude | `03`, `03B` Design, `03C` Code, `03E` register (R03, 377 rows), `03F` parity/tests, `CLAUDE_STUDY_COVERAGE_GAPS.md` |
| Naming | `ZAIN_NAMING_MIGRATION.md`, `research/R19_ZAIN_NAMING_CONFLICTS.md` |
| History / evidence | `01_LIVE_WEPLD_AUDIT.md`, `CI_403_REDIAGNOSIS_2026-10-27.md`, `EGRESS_PREFLIGHT_2026-10-27.md`, `11_PLAN_READINESS_REVIEW.md` (two prior audits), `STATUS_LEDGER.md` |
| Implementation handoff | `12_IMPLEMENTER_HANDOFF_PROMPT.md` (only after approval) |

## 3. Recommended architecture and rejected alternatives

| Choice | Recommended | Rejected (evidence) |
|---|---|---|
| Foundation | T3 fork @36d4d711 + Orca ports + Rust Core | Orca-first (3 stores, 2.37M LOC, 421 Windows issues); merge both apps; own platform (60–120 pw to parity); unmodified T3 + outside-agent Core (no per-effect authority) |
| Shell | Electron (inherited) | Keep Tauri (UI would be rebuilt; browser/CDP parity lost) |
| State | One authority per fact: T3 log = conversation; Core ledger = grants/outcomes/missions/completion | T3 log as evidence (compacts/deletes); second orchestrator |
| Durability | T3 executor + Core continuations; Vercel patterns | Workflow SDK runtime; durable-harness runtime |
| Review | OCR fork, one engine | PR-Agent second reviewer; Continue code (unmaintained) |
| Browser | One BrowserController, four lanes, pre-request gating | browser-harness, Browser Use, Orca manager or Playwright MCP as extra controllers; donor cookie import |
| Desktop tools | DeskGate adapters through Core | Running DesktopCommanderMCP as its own server; Remote Desktop Commander relay (proprietary) |

## 4. Important architectural decisions to scrutinize

ADR-001 (foundation), ADR-004 (one authority per fact, S4b recovery gating), ADR-007 (Core PDP, WebAuthn approvals,
MEDIATED/UNMEDIATED, containment floor), ADR-011 (governance reset), ADR-014 (cross-platform sandbox), ADR-015…019
(components). Trust claim before P8: authority only over mediated effects — 07 §6.

## 5. Copy First references

Transplant rows: `06` D1–D36 with pins, licenses, destinations, tests; file-level detail R11 (T3), R12 (Orca, Codex,
Cedar, ACP/MCP, editor/canvas libs), R14–R18 (components). Rights: public licenses verified; FOUNDER-ATTESTED recorded but
has no effect on third-party licenses, notices or trademarks (06 §3b). EXCLUDED: remote-desktop-commander relay (all rights
reserved, not public), Amp code, tldraw, AGPL/GPL code.

## 6. Feature completeness assessment

90 requirements → all mapped to a non-superseded task and a test (generated; 0 gaps). Claude census: 377 rows routed and
phased; **no Claude UI feature was exercised hands-on**; depth per row in `CLAUDE_STUDY_COVERAGE_GAPS.md`. LSP and debugging
are post-v1 (P6) — a deliberate scope limitation.

## 7. Unresolved risks and research limitations

1. All effort figures are ESTIMATES from reading code/docs; nothing was built or run (except `--help` and CI re-runs).
2. Calendar math assumes ~1 pw/week and upkeep 25–43%; audit 2 indicates upkeep may be 35–60% (10 §7).
3. E2E donor UNRESOLVED (FO-9). Trademark risk HIGH for "Zain" in KSA/GCC (FO-8).
4. WebAuthn in Electron, OCR Go binary signing, Electron redirect gating and DNS-rebinding defence are unproven (spikes).
5. Installed GitHub Apps (Cursor, Devin, Sentry, Vercel, Claude, Qodo, possibly Cubic) may auto-process PRs; provider-side
   settings unverified (EGRESS_PREFLIGHT).
6. File-manifest completeness: see the completeness statements at the top of R11 and R12.
7. Upstreams move daily; fork-not-track accepted; pins recorded.

## 8. Questions Astro must challenge

1. Is forking a ~1M-LOC Effect-4 codebase maintainable by one founder, versus a smaller foundation? Re-derive from R02.
2. Do seams S1–S8 + S4b really let Core decide every mediated effect without rewriting `Orchestrator.ts`? Which provider
   paths bypass them (R02 §10)?
3. Is "one authority per fact" free of hidden dual writers (receipts vs outbox, continuations vs T3 restart continuations)?
4. Are the replay classes and unknown-outcome handling sufficient for git push, PR merge, browser form submits?
5. Is WebAuthn-verified approval implementable in Electron on Windows, and is the Server-as-TCB claim honest?
6. Is the OCR fork (Go sidecar) the right review engine versus delegated-mode only?
7. Is the browser design (redirect gating, DNS rebinding, hard blocks) adequate before an OS sandbox exists?
8. Is DeskGate truly without its own authority? Can `terminal.input` or interpreter sessions escape mediation?
9. Are licenses/notices correct for every row (Apache §4(b) change notices for OCR; per-dir MIT in PStack; Claude SDK terms)?
10. Are the estimates realistic? Recompute totals from 14 and compare with your own model; is the release tiering right?
11. Is the scope coherent for a solo founder; what would you cut from v1?
12. Does the governance reset (ADR-011) preserve the security properties of the old successor chain?
13. Is anything presented as verified that was only read in documentation?

## 9. Independent review checklist

- [ ] Recompute 14 §13 totals from task rows; verify v1 and per-component sums.
- [ ] Verify the dependency graph is acyclic and v1 tasks depend only on v1-or-earlier tasks.
- [ ] Verify every requirement in 13 has a non-superseded task and a test that could fail (15).
- [ ] Spot-check ≥ 10 pins/licenses in 06 against GitHub.
- [ ] Check R11/R12 for unverifiable or missing paths.
- [ ] Check every negative test has a defined guard and a mutation control.
- [ ] Check no component introduces a second orchestrator, review store, browser controller, PTY host or policy authority.
- [ ] Check naming: no active document uses WePLD except as labelled legacy; Zain-LLM untouched.
- [ ] Check claims of hands-on verification against the evidence actually recorded.
- [ ] Check cost claims against "no mandatory paid services" (10 §7 lists paid items).

## 10. How to report findings

Report each finding as:

```text
ID: <C|H|M|L>-<n>
SEVERITY: Critical | High | Medium | Low
LOCATION: <file>:<line or section>
FINDING: what is wrong (one or two sentences)
EVIDENCE: quote/line refs or recomputation
IMPACT: what breaks if unaddressed
FIX: concrete change
```

- **Critical:** the plan cannot be executed as written, or a security/authority/legal property is violated.
- **High:** materially wrong estimate, ownership, dependency, license or security gap that changes decisions.
- **Medium:** inconsistency or missing detail that would cause rework.
- **Low:** wording, formatting, minor traceability.

Order findings by severity, then list what you found solid. Do not soften findings; an endorsement without challenge is
not useful.
