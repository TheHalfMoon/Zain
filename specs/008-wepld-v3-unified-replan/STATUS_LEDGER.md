# V3 Replan — Durable Status Ledger

```text
MISSION = Zain full replan (copy-first, deep REA, planning only)
STARTED = 2026-10-27
BRANCH = docs/v3-unified-replan-20261027
BASE_MAIN = 0a843a2 (Merge PR #345) — live main at research start
MODE = PLANNING_ONLY / NO_IMPLEMENTATION / NO_SOURCE_TRANSPLANT / NO_PAID_RESOURCES
AUTHORITY_OF_THIS_PACKAGE = CANDIDATE / UNTRUSTED UNTIL REVIEWED AND MERGED
```

This ledger exists so a context reset does not lose progress. Each row is updated when a track
changes state. Raw research notes live under `research/`; synthesized deliverables live at the
top level of this directory.

## Track state

| Track | Output | State |
|---|---|---|
| Zain live audit | `01_LIVE_WEPLD_AUDIT.md` | DONE |
| T3 Code source REA | `research/R02_T3_CODE.md` → `02_*` | DONE |
| Orca source REA | `research/R03D_ORCA.md` → `03D_*` | DONE |
| Vercel Workflow / durable-harness REA | `research/R05_VERCEL.md` → `05_*` | DONE |
| Claude ecosystem census | `research/R03_CLAUDE_CENSUS.md` → `03_*`, `03E_*` | DONE |
| Claude Design REA | `research/R03B_CLAUDE_DESIGN.md` → `03B_*` | DONE |
| Claude Code CLI / desktop / SDK REA | `research/R03C_CLAUDE_CODE.md` → `03C_*` | DONE |
| Amp + competitors REA | `research/R04_AMP.md`, `research/R10_COMPETITORS.md` | DONE |
| 402-registry live verification | `research/R06_REGISTRY_VERIFICATION.md` | DONE |
| Synthesis 00–12 + ADRs | top-level docs | DONE (revision 2 after review) |
| Adversarial review | `11_PLAN_READINESS_REVIEW.md` | DONE — 28 findings, all dispositioned |
| Publish | branch pushed; **draft PR deliberately NOT opened** | see "Publication decision" below |

## Early verified findings (Zain live audit)

- Live repo is **PRIVATE** (`gh repo view`, 2026-10-27); `CURRENT_STATE.md` (checkpoint 2026-09-12) and
  Astro `EVIDENCE_AND_VALIDATION.md` (2026-09-20) both record **public**. Discrepancy: live wins.
- Last push to the repo: 2026-10-01. Last merged PR: #345 (2026-09-29). 347 PRs total.
- Open PRs: #347 (Graft context, non-draft), #346 (source expansion), #343 (S3 contracts C001–C013, draft),
  #342 (Astro benchmark prereg, draft), and 8 August-era drafts (#1, #73, #81, #88, #136, #159, #162, #164).
- PR #347 body carries a Cubic auto-generated description — another instance of the recorded
  provider-effective-state conflict (`CUBIC_PROVIDER_EFFECTIVE_STATE = CONFLICTING`).
- Product code on main: ~19.1k lines Rust incl. tests (`crates/contracts`, `crates/core`, `apps/desktop/src-tauri`)
  + a 3-file vanilla JS UI. Governance: **169 Python integrity scripts, ~83.6k lines** under `.github/scripts/`.
- S1 implemented; S2 `CLOSED_CANONICAL` with 8 carried limitations; S3 code absent (contracts-only PR #343 open).
- Registry V1: 402 entries, **0 admitted**, 373 `BASELINE_ACCOUNTED_PENDING_PATH_MINING`, 20 enriched, 9 path-mined.
- T3 Code is **absent** from the registry and all specs. Orca is present in Astro `SOURCE_INVENTORY.md` at
  `b5b727bd…` with 6 paths captured (README/manifest-level only). Vercel Workflow / durable-harness absent.
- Admission policy (`wepld_integrity.py:is_common_allowed`) permits new `docs/**.md` and `specs/**.md`
  → a docs-only planning PR under `specs/008-*/` is admissible by the trusted-base check.

## Additional verified findings (synthesis)

- ~~Main CI root cause: `permissions: {}` on a now-private repo~~ — **WITHDRAWN 2026-10-27.** Workflows already use
  `contents: read`; the 403 burst was most probably REST throttling (PROBABLE); Actions jobs are currently blocked by
  billing. See `CI_403_REDIAGNOSIS_2026-10-27.md`.
- Claude official policy: third-party products may not route requests via users' Free/Pro/Max credentials (R03C §10.5).
- `anthropics/sandbox-runtime` is Apache-2.0 (R10 pins) — resolves an R03C unknown.
- Continue repository now states it is read-only / unmaintained (R06) — remove as reviewer/build-tool candidate.
- Census coverage verdict recorded as COVERAGE_COMPLETE_FOR_MANDATORY_SCOPE / DEPTH_PARTIAL_OUTSIDE_IT.

## Continuation session 2026-10-27 (founder instructions: stay private, no auto external review, PR only when safe)

| Item | State | Evidence |
|---|---|---|
| CI 403 re-diagnosis | DONE — earlier diagnosis withdrawn; P−1 permission fix removed | `CI_403_REDIAGNOSIS_2026-10-27.md` |
| Re-run of main integrity (attempt 2) | NOT STARTED by GitHub — billing / spending limit | check-run 122348322500 annotation |
| Cubic provider-level disable | NOT VERIFIABLE from this session; absence of its check suite on today's push is suggestive only | `EGRESS_PREFLIGHT_2026-10-27.md` §2–3 |
| Other auto-triggered integrations | Qodo auto-reacts (billing-paused); CodeRabbit auto-reacted through 10-01; Cursor/Devin/Sentry/Vercel/Claude apps hold access, AI-review state unknown | same |
| Egress record | DONE — verdict EGRESS_BLOCKED | same |
| Draft PR | **NOT OPENED** (conditions E1–E5 are founder-only) | same §4 |
| Claude study-coverage gaps | DONE — 0 hands-on; 18 full-text; 220 summary+gates; 78 digest-only; 23 non-HC-only | `CLAUDE_STUDY_COVERAGE_GAPS.md` |
| Research package | PRESERVED unchanged except one username redaction (R03C) and earlier quote trims | git history |

## Zain master-plan sessions (2026-10-27 / 2026-10-28)

| Item | State | Evidence |
|---|---|---|
| Repository | TheHalfMoon/Zain (ID 1334408699, PUBLIC; renamed from wepld by founder; remote updated) | gh api |
| CI | main GREEN on unchanged re-run (attempt 3) — 403 was transient | CI_403_REDIAGNOSIS §4 |
| Rename WePLD -> Zain | DONE in active docs; history/evidence labelled legacy | ZAIN_NAMING_MIGRATION.md |
| Naming conflicts | DONE — trademark risk HIGH (FO-8) | research/R19 |
| Claude census | 377 rows; 0 hands-on; 110 full-text, 212 summary+gates, 55 non-HC live | CLAUDE_STUDY_COVERAGE_GAPS.md |
| IDE/debug/platform | DONE | research/R13 |
| Components (Code Review, Engineering, Plan Mode, Browser, DeskGate) | DONE | research/R14–R18, 16_*, ADR-015..019, 06 D26–D36 |
| Requirements / tasks / traceability | 90 reqs, 154 task rows, 0 gaps (generated) | 13, 14, 15 |
| Totals | v1 91–141 pw; all 160–259 pw (computed) | 14 §13 |
| Audit 2 | DONE — all Critical/High resolved | 11 §6 |
| File manifests R11 (T3) / R12 (donors) | DONE (API-only, no local clones); corrections in 06 §1c | research/R11, R12 |
| Astro handoff | DONE | ASTRO_REVIEW_HANDOFF.md |
| Disk incident | local disk filled by donor clones; clones deleted; founder instruction: nothing saved locally, only in repo | — |
| Privacy | local-machine details removed from R18 at HEAD (still present in commits c376917 and ef19a3f history) | — |
| Draft PR | NOT opened — founder decision 2026-10-28: Astro reviews the branch directly (no PR); automatic-review rule for installed apps still unproven (EGRESS_PREFLIGHT §5) | — |

## Revision 3 — repair after Astro round 1 (2026-10-28)

| Item | State | Evidence |
|---|---|---|
| Astro round 1 | DO NOT APPROVE @b94505988e05 (1 C, 12 H, 4 M, 1 L) | ASTRO_FINDINGS_DISPOSITION.md |
| Dispositions | 16 RESOLVED (several with early feasibility gates C-00), 2 DEFERRED WITH EXPLICIT GATE (H-10, M-1), 0 BLOCKED | ASTRO_FINDINGS_DISPOSITION.md |
| Deterministic validation | `tools/plan_graph.py --check` exit 0: 165 live tasks, 338 registered tests, 0 errors; 98 requirements REGISTERED, 0 GAP | GENERATED_PLAN_REPORT.md |
| New specs | 17 trust boundary, 18 provider matrix, 19 component security, 20 governance equivalence, 21 releases/cost, 22 source admission, 23 test registry | — |
| Release proposal | R1 Zain Trusted Starter with fixed claims; R0 first usable release; all capabilities preserved in R2–R7 | 21, 14 §16 |
| Not done | nothing implemented, built or run; Windows mechanisms unproven until C-00; full governance inventory is G-08 | — |
| Draft PR | not opened (founder decision: Astro reviews the branch directly) | — |
| Round-2 handoff | planning commit add02fbc596dfa461e73f8acbd9a005010ad4f0f | ASTRO_REVIEW_ROUND_2_HANDOFF.md |

## Revision 3.1 — First Working Build analysis (2026-10-28)

| Item | State | Evidence |
|---|---|---|
| Founder challenge | R0 21.8–34.35 pw too long for a Copy First fork | 24 |
| Upstream build evidence | T3 v0.1.3 + nightlies ship Windows x64 NSIS daily; cross-built on Ubuntu with Windows verify job; Windows tests manual-dispatch | 24 §1 |
| New milestones | R0a First Working Build (Q-01..Q-05), R0b Tester Build, R0 Qualified | 14 PF, §16 |
| Audit | 45 former R0 tasks: 0 needed for first build, 7 before testers, 28 for qualified R0, 10 deferred (R1 6, R2 3, R3 1); none deleted | 24 §6 |
| Double counting removed | F-13 learning, import, build/run, bug fixes, rebrand, strip | 24 §8 |
| Numbers | generated; FWB estimate conditional (C1–C6) | GENERATED_PLAN_REPORT §3 |
| Round-2 handoff updated | planning commit 024ed89ac08e91eba8b98f92a874d880a4156b7f | ASTRO_REVIEW_ROUND_2_HANDOFF.md |
