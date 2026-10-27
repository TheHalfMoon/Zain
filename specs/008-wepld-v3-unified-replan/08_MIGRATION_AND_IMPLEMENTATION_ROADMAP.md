# 08 — Migration and Implementation Roadmap (Phases P−1 … P10)

```text
STATUS = PROPOSED, revision 2 (estimates rebuilt bottom-up after adversarial finding H4; tiers corrected H5;
         break-glass phase added C3).
OWNER = founder (solo) + AI implementers under 12_*; reviewer route ≠ builder route (ADR-011)
ESTIMATES = person-weeks (pw), ESTIMATE class, derived from R02 §14 work packages and 06 donor rows
TIERS = T0 docs-only · T1 UI/product code with no effect, CI, supply-chain or authority change · T2 everything else
        (Core, effects, permissions, CI/workflows, installer/updater, donor ingestion, process spawning, hooks)
```

## Phase overview and totals

| Phase | User-visible outcome | ESTIMATE pw | Basis | Tier |
|---|---|---|---|---|
| P−1 Break-glass repair | (none) integrity workflow can run on the private repo | 0.1–0.2 | one workflow permission line | T2 (break-glass record) |
| P0 Governance reset | one stable checker; protected paths; founder-signed co-sign | 1–2 | ADR-011 | T2 |
| P1 Donor baseline (VM) | T3/Orca measured; nothing changed | 1–2 | — | T2 (executes donor install scripts, isolated) |
| P2 Fork, strip, rebrand | "WePLD" app: chat + code sessions (Codex, ACP, Claude via API key), worktrees, diff, terminal, browser | 8–14 | WP0 3–5 + WP1 2–4 + SDK/installer gates 0.5–1 + WP8 2–4 | T2 |
| P3 Trusted Core | Core-decided approvals with WebAuthn; ledger; UNKNOWN outcomes; containment floor; no Full access | 17–32 | WP2 2–3 + WP3 4–8 + WP4/S4b 2–4 + WP5 3–6 + policy engine 2–4 + Inbox/permission UI 2–3 + WebAuthn 1–2 + floor 1–2 | T2 |
| P4 Missions + Brain | projects remember; missions wait for CI/schedules; context survives model switch | 5–9 | own build | T2 |
| P5 Review, Completion, Connections | independent reviewer; completion decisions; MCP/skills/plugins with grants | 5–9 | own + PR-Agent wrap | T2 |
| **v1 = P−1…P5** | | **≈ 37–68** | | |
| P6 IDE breadth + benchmarks | Monaco + diff comments, Design Mode capture, CLI agents, Linear, benchmark harness | 13–26 | 06 D7 4–8 + D2 3–6 + D3 3–5 + D5 2–4 + D23 1–2 (+ B-suite) | T2 (spawns processes, hooks) |
| P7 Design Studio v1 | canvas, comments → proposals, DTCG tokens, handoff, exports | 8–14 | D19 1–2 + D20 3–5 + D21 1 + canvas/comments/export 3–6 | T1/T2 |
| P8 Containment | providers in OS sandbox (Windows first); Full-access lane only inside sandbox | 4–10 | D9 | T2 |
| P9 General agent work | documents, research, browser agent, computer use (gated) | 6–12 | D6 + own | T2 |
| P10 Remote + runner | runner as project home; phone/web approvals via passkey | 4–8 | T3 remote + own | T2 |
| **All phases** | | **≈ 72–138** | | |

**What this means for a solo founder (stated, not hidden):** at assumption A-1 (~1 pw of AI-assisted output per
calendar week) and an ongoing fork/adapter upkeep of 1.1–1.85 pw/month once P2 lands (≈25–43% of capacity, `10_*` §3),
**v1 (P−1…P5) is roughly 12–26 calendar months; the full plan is 2–4 years.** Two earlier stopping points are useful
products on their own: **P2 exit** (~10–18 pw from start: a WePLD-branded multi-agent workbench) and **P3 exit**
(~27–50 pw: the authority differentiator). Scope cuts, if slippage exceeds 50%: drop P9 computer use, P7 PPTX export,
P10 mobile, then P6 Linear.

Comparison basis: R02's "22–38 pw" covered only WP0–WP5 + WP8 + minimal editor — it excluded Brain, missions,
completion, WebAuthn and policy UI, which is why v1 here is larger. Option D (own platform) was 60–120 pw **to donor
parity excluding trust work**, so Option A remains materially cheaper.

---

## P−1 — Break-glass repair (C3)

`main` fails `foundation-integrity` on every run (compare API 403 on the private repo, run 36589753362), so no PR —
including this package and P0 — can pass the current gate.

- **Record (committed before the change):** `docs/governance/BREAK_GLASS_2026-xx-xx.md` with: founder signature (signed
  commit/tag with the founder-only SSH signing key, ADR-011), exact base SHA and head SHA, the single bypassed check and
  why, one-time scope = change `permissions: {}` → `permissions: contents: read` in the integrity workflow(s) only (or the
  ADR-010 alternative), Build Learning entry.
- **Then:** merge this planning package under the repaired v72 gate (it is admissible: docs `.md` only); then P0.
- **Negative test:** a second PR touching any other path under the break-glass label is rejected by the repaired gate.

## P0 — Governance reset

- **Work:** one stable `governance_check.py` executed from the **base** commit (workflow uses `pull_request_target`
  with no candidate checkout — the data-only pattern already proven by `s1-admission-integrity` — or a base-SHA checkout
  of the checker with the candidate read as data); `PROTECTED_PATHS` manifest (AGENTS.md, canonical docs, workflows,
  checker, allowed-signers file); protected-path changes require a **founder-signed commit or tag** verified against
  `allowed_signers` (a label is not proof — any agent with the founder's `gh` token can add one); exact-head merge guard;
  archive v1–v72 scripts read-only under `docs/historical/`.
- **Tests:** positive docs PR passes; negative: protected-path change without founder signature fails; negative: PR
  editing the checker or workflow cannot change the checker that judges it; negative: forged label without signature fails.
- **DoD:** main green; three negative oracles demonstrated on throwaway PRs.

## P1 — Donor baseline (isolated)

- **Isolation:** Windows Sandbox or a VM (not the founder's main profile) because donor installs execute third-party
  postinstall scripts; delete after (10 §5).
- **Work:** build/run T3 @36d4d711 and Orca @e310a636; run T3 suites, record pass/fail/skip; measure B1–B4; measure T3
  receipt-table write latency with `synchronous=FULL` (07 §5); confirm Electron/Node versions; mirror pinned tarballs
  privately (A-2).
- **Exit (G2):** T3 builds/runs; numbers committed. If not achievable in 2 pw → reopen ADR-001.

## P2 — Fork, strip, rebrand

- **Acquisition:** D1 + D4. **Strip:** mobile, marketing, relay/T3 Connect, Clerk, PostHog, `.repos/`, unused providers,
  V1 importer. **Seam additions now:** `ThreadSettlementService` changed to cosmetic auto-archive only (never a completion
  signal; label "archived", not "settled/done") — H9.
- **SDK task (H6):** remove `@anthropic-ai/claude-agent-sdk` (and its platform-binary packages) from `server.asar`;
  load from a user-consented location (user installs it, or install-on-consent showing Anthropic terms); installer-content
  CI gate fails if `claude-agent-sdk*` is bundled. Claude sessions in P2 work only when the user has provided the SDK and an
  API key/cloud credential.
- **Identity:** rename register (06 §4); Core binary → `wepld-core` and S2 commands move under it in the same change.
- **Tests:** T3 suites at P1 ratio; donor-identifier + installer-content gates; no network egress at idle; protocol
  mismatch with T3 clients → 426.
- **Budget:** B1/B2/B3 ≤ P1 T3 baseline + 10%.
- **DoD:** installable unsigned/dev-signed `WePLD-Setup.exe`; Codex + ACP + (user-provided) Claude sessions work.

## P3 — Trusted Core (differentiator)

- **G3 spike first (1–2 pw, inside the estimate):** ACP `fs/write` (S3) and Codex approval (S2) through Core with ledger
  receipts; kill -9 between dispatch and report → `EFFECT_OUTCOME_UNKNOWN`.
- **Work:** CoreBridge; protocol v2 (direction-tagged ids, chunking, fencing epoch, data-root lock); ledger; seams S1,
  S3, S2, **S4 + S4b recovery gating** (07 §5), S5 (per-run aggregate link), S6, S7, S8; WebAuthn approvals + credential
  registration; permission UI (Manual/Auto/Skip × per-tool) compiled to Core policy; trust indicator; containment floor
  (data-root deny in all provider profiles, Job Objects, Full access removed); Claude relay: **PreToolUse hook calls
  `effect.propose` and, on allow, `effect.dispatch` (fsynced) before returning allow**; PostToolUse → `effect.report` (M5).
- **Release builds compile out `OBSERVE` mode** (H8); dev builds allow it only via a WebAuthn-signed `core.mode` record
  with a persistent red banner.
- **Positive tests:** every mediated effect class has a receipt; approval round-trip with assertion; adapters.
- **Negative tests (each must also be run with Core disabled and must then FAIL — mutation control):**
  forged approval from a compromised renderer or Server without assertion → rejected; second Server on same data root →
  no authority; stale epoch frame → rejected; T3 recovery attempts to auto-continue a `NEVER` effect → blocked;
  Skip cannot override Blocked; Full access not selectable; agent writes to data root → denied by profile floor;
  agent rewrites ledger file and recomputes chain → detected at next `ledger.anchor` comparison (documented limitation
  before P8); agent sets `WEPLD_CORE_ENFORCE=observe` → no effect in release build; Claude kill mid-Edit → UNKNOWN or
  reconciled by file hash (CC-T02).
- **Durability:** R1 sweep 20 effects × 5 kill points; W1, W2, W2b (T3 receipt rollback → un-acked fire reconciled,
  not re-fired), W9 (T3 recovery vs Core reconcile race).
- **Budgets (absolute, not %):** Core decision p95 ≤ 5 ms; ledger fsync append p95 ≤ 10 ms on the founder's NVMe
  (measured in P1); per mediated effect added latency p95 ≤ 25 ms (3 fsyncs).
- **Rollback:** dev-only observe mode; tagged pre-P3 build.

## P4 — Missions, Brain, continuations

- Mission/continuation APIs with two-phase fires; Brain as **index over repo specs** + memory notes; preferences
  `CANDIDATE → QUALIFIED` by user action; capsule injection + `brain.query` MCP tool; compaction capsule capture; CI-wait.
- **Tests:** model switch keeps decisions (measured on **non-pinned** decisions recorded during work, not only verbatim
  pinned facts); incognito → zero Brain writes; duplicate fire suppressed; laptop off at schedule → one fire on wake.
- **Budget:** capsule ≤ 2k tokens; Brain query p95 ≤ 50 ms at 100k entries.

## P5 — Review, Trusted Completion, Connections

- Reviewer route ≠ builder route; findings schema; completion rules 1–10 + `UNMEDIATED` handling (07 §6); MCP
  (local/remote OAuth), Agent Skills (hash-pinned), plugins, MCPB with manifest review.
- **Tests:** completion blocked by UNKNOWN effect; merge ≠ completion; reviewer = builder → refused; skill update
  widening tools → disabled until re-approved; revoked OAuth → `blocked_on_auth`.
- **DoD:** the Astro "first complete loop" runs locally end to end.

## P6–P10

As in the overview table, each with phase spec, tests-first, budgets and T2 review. P6 CLI-agent hooks use per-launch
config overlays and an authenticated loopback endpoint (M4); P10 implements the project-home rule (07 §5) and passkey
approvals for phone/web.

## Feature parity checklist (exit)

| Area | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | P10 |
|---|---|---|---|---|---|---|---|---|---|
| Multi-provider chat/code sessions, worktrees, diff, terminal, preview | ✓ | | | | | | | | |
| Core-decided approvals (WebAuthn) + receipts + floor | | ✓ | | | | | | | |
| Missions / continuations / Brain | | | ✓ | | | | | | |
| Independent review + Trusted Completion + MCP/skills | | | | ✓ | | | | | |
| Monaco, Design Mode, CLI agents, benchmarks | | | | | ✓ | | | | |
| Design Studio | | | | | | ✓ | | | |
| OS sandbox, Full-access lane in sandbox | | | | | | | ✓ | | |
| Documents, research, browser/computer use | | | | | | | | ✓ | |
| Runner as project home, phone/web approvals | | | | | | | | | ✓ |

## Rollback principle

Every phase lands as separable commits behind dev flags; the Tauri S1 host stays buildable until P3 exit proves the Core
sidecar under the new shell; release builds never ship observe mode.
