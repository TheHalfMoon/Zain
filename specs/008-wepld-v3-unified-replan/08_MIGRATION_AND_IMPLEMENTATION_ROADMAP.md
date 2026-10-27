# 08 — Migration and Implementation Roadmap (Phases 0–10)

```text
STATUS = PROPOSED. Replaces V2.3 S3..S10 sequencing if accepted; S1/S2 remain accepted history.
OWNER = founder (solo) + AI implementers under the 12_* prompt; reviewer = independent worker ≠ builder (ADR-011)
ESTIMATES = person-weeks (pw), ESTIMATE class, solo + AI-assisted; ranges overlap; total v1 (P0–P5) ≈ 30–55 pw
GATE_DEPTH = risk-tiered (ADR-011): T0 docs · T1 UI/product · T2 Core/authority/effects/CI/supply-chain
```

## Phase overview

| Phase | User-visible outcome | ESTIMATE | Depends on | Tier |
|---|---|---|---|---|
| P0 Repair + governance reset | (none) main green; one stable checker | 1–2 | — | T2 |
| P1 Donor baseline (no code changes) | T3 runs on founder's Windows box; numbers recorded | 1–2 | P0 | T0/T1 |
| P2 Fork, strip, rebrand | "WePLD" app: chat + code sessions with Claude/Codex/ACP, worktrees, diff, terminal, browser | 4–8 | P1 | T1 |
| P3 Trusted Core integration | Approvals/denials decided by Core; ledger; unknown outcomes visible; no Full access without sandbox | 6–10 | P2 | T2 |
| P4 Missions + Brain + continuations | Projects remember; missions wait for CI/schedules; context survives model switch | 4–8 | P3 | T2 |
| P5 Review, Trusted Completion, Connections | Independent reviewer; completion decisions; skills/plugins/MCP with grants | 4–8 | P4 | T2 |
| P6 IDE breadth + benchmarks | Monaco editor, diff comments, Design Mode capture, CLI agents; benchmark suite public | 4–8 | P2 (parallel with P4/P5 where files don't overlap) | T1 |
| P7 Design Studio v1 | Canvas, comments → agent proposals, DTCG tokens, code handoff | 6–10 | P6 | T1/T2 |
| P8 Containment | Providers run in OS sandbox on Windows/Linux; Full-access lane re-enabled inside sandbox | 4–10 | P3 | T2 |
| P9 General agent work | Documents/artifacts export, research tasks, browser agent, computer use (gated) | 6–12 | P5, P8 | T2 |
| P10 Remote + runner | Self-hosted always-on runner; browser/mobile control | 4–8 | P4 | T2 |

## P0 — Repair and governance reset

- **Acquisition scope:** none.
- **Prerequisite proof:** this package merged as docs-only (T0).
- **Work:** (a) fix `foundation-integrity` 403 on private repo: workflow `permissions: contents: read` (or make repo public
  — founder decision ADR-010); (b) replace successor chain with **one** stable `governance_check.py` + `PROTECTED_PATHS`
  manifest (AGENTS.md, canonical docs, workflows, checker itself) + exact-head merge guard; archive v1–v72 scripts under
  `docs/historical/governance-successors/` (read-only record); (c) record visibility change incident in Build Learning.
- **Tests:** positive = ordinary docs PR passes; negative = PR modifying a protected path without founder co-sign label
  + second reviewer fails; negative = candidate that edits the checker cannot self-approve (checker runs from base).
- **Rollback:** revert workflow commit; v72 chain still in history.
- **DoD:** `main` green; protected-path negative oracle demonstrated on a throwaway PR.

## P1 — Donor baseline (run unmodified, measure)

- **Acquisition scope:** clone T3 @36d4d711 (and Orca @e310a636 for comparison only) into an isolated directory; no
  WePLD repo changes except a results doc.
- **Work:** build + run T3 desktop on Windows 11; run its test suites (`vp test`), record pass/fail/skip ratio; measure
  B1 cold start, B2 idle RSS (all processes), B3 UI input latency, B4 first-token latency (Claude via API key, Codex);
  same for Orca; inventory packaging scripts; confirm `node:sqlite`/Electron versions.
- **Tests:** none new; this phase *produces* the baseline.
- **Exit gate (G2):** T3 builds and runs; ≥ the upstream CI pass ratio on Windows (or documented deltas); numbers committed.
- **Cost:** $0 (+ small API spend for B4 with founder's key, capped e.g. $5).
- **Rollback:** n/a. If T3 cannot be built/run on Windows within 2 pw → re-open ADR-001 (Option D for shell).

## P2 — Fork, strip, rebrand

- **Acquisition scope:** D1 (T3 fork) + D4 (process-host) into new repo layout `wepld/` monorepo:
  `apps/{desktop,web,server}`, `packages/*` (from T3), `crates/{contracts,core}` (existing), `native/` (T3).
- **Work:** strip list (02 §2); rename register (06 §4); remove Full-access default (set Supervised); update feed →
  WePLD releases; telemetry removed; Windows NSIS build; donor-identifier CI gate.
- **Interfaces:** unchanged T3 contracts; protocol version bumped to WePLD-1 to avoid pairing with T3 clients.
- **Tests:** T3 suites green at P1 ratio; + grep gate; + "no network egress at idle" test (pcap/Windows firewall log);
  negative: app refuses to connect to a T3-branded server (protocol mismatch → 426).
- **Performance budget:** ≤ P1 baseline + 10% (B1/B2/B3).
- **Migration:** none (new product; no user data).
- **Rollback:** tag before strip; strip as separate commits.
- **DoD:** installable `WePLD-Setup.exe`; chat + Codex/Claude(API key)/ACP sessions; worktree + diff + terminal work.

## P3 — Trusted Core integration (the differentiator)

- **Acquisition scope:** D11 Cedar (or hand-written Rust rules if Ponytail says smaller), D17 rusqlite, D12 ACP pins.
- **Prerequisite proof (G3 spike, first 1–2 pw):** S3 ACP `fs/write` and S2 Codex approval go through Core with ledger
  receipts; kill -9 between dispatch and report → `EFFECT_OUTCOME_UNKNOWN`.
- **Work:** CoreBridge service (Effect `Context.Service`, S1 framing; precedent `ResourceMonitorBinary.ts`); Core API
  (07 §3); Ledger (07 §4); seams S1, S3, S2, S4, S5, S6, S7, S8 in that order; Inbox UI for approvals/unknown outcomes;
  permission UI (Manual/Auto/Skip × per-tool) compiled to Core policy; Claude hook-based relay (03C §2); trust-claim banner.
- **Schemas:** Spec 006 §19 types serialized in `crates/contracts` (reuse PR #343 descriptors where they fit); ledger
  event kinds; `wepld.receipt-linked` T3 event (compaction-exempt).
- **Tests (positive):** every mediated effect class has a receipt; approvals round-trip; Claude/Codex/ACP adapters.
  **(negative):** Core down → gated effects refused; stale grant → `STALE_TARGET`; replayed command id rejected (S1);
  Skip mode cannot override Blocked; full-access not selectable without sandbox; forged approval from renderer without
  human token rejected; ledger tamper → `ledger.verify` fails.
- **Durability acceptance:** R1 kill-sweep over 20 scripted effects × 5 kill points = 100 runs, invariants I1–I6 hold.
- **Performance budget:** Core decision p95 ≤ 5 ms local; ledger append p95 ≤ 10 ms (fsync, NVMe); overhead on a
  50-effect turn ≤ 3%.
- **Rollback:** feature flag `WEPLD_CORE_ENFORCE=observe|enforce`; observe mode records decisions without blocking.
- **DoD:** G3 + tests + budgets met; independent review (T2) + security review.

## P4 — Missions, Brain, continuations

- **Work:** `mission.*`, `continuation.*`, `brain.*` Core APIs; Missions view; Brain view (entries, provenance,
  supersede); capsule injection at turn start (T3 `injectHistory?`/system prompt) + `brain.query` MCP tool for agents;
  compaction capture; CI-wait continuation; schedules with missed-run policy.
- **Tests:** V1-03..V1-05 (03F); R2 duplicate wakes; R9 compaction recall 100% of pinned facts; model switch
  (Claude → Codex) keeps decisions; incognito writes nothing.
- **Budget:** capsule ≤ 2k tokens default; Brain query p95 ≤ 50 ms at 100k entries.
- **DoD:** a mission "fix failing test and open PR" survives app restart and machine reboot, resumes on CI result.

## P5 — Review, Trusted Completion, Connections

- **Work:** reviewer-worker rule (reviewer route ≠ builder route, recorded); findings schema; completion evaluate/decide
  with rules 1–10 (Spec 006 §20); Connections page: MCP (local/remote OAuth), skills (SKILL.md), plugins, MCPB review.
- **Tests:** completion blocked by an UNKNOWN effect; merge ≠ completion; reviewer = builder → refused; skill requesting
  wider tools → denied; revoked OAuth → `blocked_on_auth`.
- **DoD:** end-to-end "first complete loop" from the Astro plan — open project → plan → authorized work → independent
  review → repair → accept — runs locally.

## P6 — IDE breadth + public benchmarks (parallelizable with P4/P5)

D7 Monaco + diff comments, D2 Design Mode capture → composer, D3 CLI agents catalog/status, D5 Linear; benchmark harness
(09 §3) published with raw data. Budget: editor open 5 MB file ≤ 1 s; idle RSS ≤ P2 + 15%.

## P7 — Design Studio v1

03B primitives; AT-01..AT-15 (P0) green on Windows; preview sandbox isolation tests; DTCG tokens; export HTML/zip/PNG/PDF.

## P8 — Containment

D9 codex sandbox crates into Core launcher (Windows first), D10 as reference; network egress proxy; escape test suite;
then re-enable a "Full access inside sandbox" lane. Trust banner updates its claim only after escape suite passes.

## P9 — General agent work

Documents/artifacts (Markdown/HTML/PDF; PPTX/XLSX via permissive libs after Ponytail), research tasks with citations as
evidence, browser agent (T3 + Orca automation subset), computer use (D6) behind per-session grants and hard-blocked
categories (payments, account creation, credential entry).

## P10 — Remote and runner

`wepld serve` headless runner (Linux service first; Windows service gap), pairing, T3 web client over LAN/Tailscale;
project bundle export/import (05 §4.7); no WePLD-hosted relay.

## Feature parity checklist per phase (exit)

| Area | P2 | P3 | P4 | P5 | P6 | P7 | P9 | P10 |
|---|---|---|---|---|---|---|---|---|
| Multi-provider chat/code sessions | ✓ | | | | | | | |
| Worktrees, diff, terminal, browser preview | ✓ | | | | | | | |
| Core-decided approvals + receipts | | ✓ | | | | | | |
| Missions/continuations/Brain | | | ✓ | | | | | |
| Independent review + Trusted Completion | | | | ✓ | | | | |
| MCP/skills/plugins | | | | ✓ | | | | |
| Monaco editor, Design Mode, CLI agents | | | | | ✓ | | | |
| Design Studio | | | | | | ✓ | | |
| Documents, research, browser/computer use | | | | | | | ✓ | |
| Remote runner + phone/web control | | | | | | | | ✓ |

## Rollback principle

Every phase lands behind flags or as separable commits; Core enforcement has `observe` mode; the Tauri S1 host and
S2 CLI remain buildable until P3 exit proves the Core sidecar under the new shell.
