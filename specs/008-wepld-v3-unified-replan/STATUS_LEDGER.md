# V3 Replan — Durable Status Ledger

```text
MISSION = WePLD full replan (copy-first, deep REA, planning only)
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
| WePLD live audit | `01_LIVE_WEPLD_AUDIT.md` | DONE |
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

## Early verified findings (WePLD live audit)

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

- Main CI root cause: v72 `verify-local --remote-baseline` → GitHub compare API HTTP 403 with `permissions: {}` on a
  now-private repo (run 36589753362, 2026-09-29).
- Claude official policy: third-party products may not route requests via users' Free/Pro/Max credentials (R03C §10.5).
- `anthropics/sandbox-runtime` is Apache-2.0 (R10 pins) — resolves an R03C unknown.
- Continue repository now states it is read-only / unmaintained (R06) — remove as reviewer/build-tool candidate.
- Census coverage verdict recorded as COVERAGE_COMPLETE_FOR_MANDATORY_SCOPE / DEPTH_PARTIAL_OUTSIDE_IT.

## Publication decision (2026-10-27)

- Branch `docs/v3-unified-replan-20261027` pushed to `TheHalfMoon/wepld` as a backup of the package.
- **No PR opened.** `EXTERNAL_REVIEW_EGRESS_POLICY.md` classifies unscreened automatic external review of non-public
  content as `PROHIBITED_EGRESS`. The repo is now private, and Cubic has been observed auto-posting on PR creation
  (PR #347, 2026-10-01) despite repository config disabling it (`CUBIC_PROVIDER_EFFECTIVE_STATE = CONFLICTING`).
  Opening a PR would likely transmit this package to Cubic without a recorded preflight.
- To open the PR safely, the founder chooses one: (a) uninstall/suspend the Cubic GitHub App for this repo (verify
  provider-side), then open the PR; or (b) record an egress preflight for this exact docs-only scope (content
  classification, secret screening evidence, provider data-handling decision) and accept Cubic exposure; or (c) make the
  repo public first (ADR-010 a). Independently, the PR's integrity check will fail until P−1 repairs the 403 (08).
- Secret screening performed on the package: regex scan for GitHub/Anthropic/AWS token patterns → 0 hits.
