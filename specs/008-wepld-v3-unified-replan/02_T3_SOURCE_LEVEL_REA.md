# 02 — T3 Code Source-Level REA (synthesis)

```text
DONOR = pingdotgg/t3code @ 36d4d711b79c73eb33131944f73ea4a8c6156484 (2026-10-27), MIT (T3 Tools Inc.)
RELEASE_AT_PIN = v0.1.3 stable / v0.1.4-nightly.20261027.3770
FULL_REA = research/R02_T3_CODE.md (613 lines, path@SHA citations)
RIGHTS = PUBLIC_OPEN_SOURCE (MIT) + FOUNDER-ATTESTED for broader reuse; notices must be retained
ROLE_IN_V3 = FORK FOUNDATION (shell + server + orchestration + providers)
```

## 1. What T3 is (verified)

- pnpm 12 + Vite+, **Effect 4.0.5**, Node built-in `node:sqlite`, Electron 44.9.3, React 19.3. ~1.0M non-test TS LOC
  (server 238k, web 281k, mobile 157k); 1,693 test files incl. 94 replay fixture sets (R02 §2, §8).
- Server-first: execution lives in the environment that owns the workspace; web/desktop/mobile are WebSocket-RPC
  clients (203 RPCs; protocol-version gate with HTTP 426) (R02 §5).
- Churn: 1,429 commits in the week of 2026-10-18; 2,506 open PRs; 1,167 open issues (454 bugs). **A solo founder
  cannot track it → hard fork, cherry-pick only** (R02 §1, §15).

## 2. Ownership boundaries worth keeping

| Module | Path | Keep? | Why |
|---|---|---|---|
| Orchestrator + EventSink + receipts | `apps/server/src/orchestration-v2/{Orchestrator,EventSink,CommandReceiptStore}.ts` | KEEP | single write path; idempotent commands |
| EffectOutbox + EffectWorker | `…/EffectOutbox.ts`, `…/EffectWorker.ts` | KEEP + seam S4 | the one executor; add Core authority + unknown outcome |
| Recovery + maintenance | `ProviderRuntimeRecoveryService.ts`, `EffectOutbox.reconcileAfterProcessLoss`, `ProjectionMaintenance.ts` | KEEP but **gate on Core (seam S4b)**: no requeue/auto-continue before `core.open_dispatches`; exempt the per-run `zain.run-receipts` event from compaction | T3 otherwise cancels/requeues/auto-continues without asking Core |
| Thread settlement | `ThreadSettlementService.ts` | **CHANGE**: cosmetic auto-archive only, never a completion signal | auto-settles on PR merge/close (contradicts Merge != Completion) |
| Provider adapters | `Adapters/ClaudeAdapterV2.ts` (11k), `CodexAdapterV2.ts` (7.5k), `packages/provider-acp*`, `provider-opencode`, `provider-pi` | KEEP these five families | per-provider approval relay = seams S2/S3 |
| VCS / worktrees / checkpoints | `vcs/GitVcsDriver*.ts`, `checkpointing/*` | KEEP + seam S7 (gate `clean -fd`, push, merge) | rename hidden refs to `refs/zain/…` |
| Terminal | `apps/server/src/terminal/*`, libghostty-vt renderer | KEEP (the one PTY host) | |
| In-app browser / preview automation | `apps/web/src/browser`, `mcp/PreviewAutomationBroker.ts` | KEEP; stabilize (#15579, #18165) | |
| `/mcp` server (internal + outside agents) | `apps/server/src/mcp/*` | KEEP + seam S6 | outside agents receive Core-scoped grants |
| Packaging / updater | `scripts/build-desktop-artifact.ts`, `apps/desktop/src/updates/*` | KEEP; re-point feed to Zain releases | |
| Mobile, marketing, relay/T3 Connect, Clerk, PostHog, `.repos/`, Antigravity/Muse/fx/Grok/Cursor, V1 importer | various | **STRIP** | cost, cloud coupling, telemetry |

## 3. Seams for the Rust Trusted Core (priority order, R02 §10)

S1 runtime-mode clamp (`RuntimePolicy.ts`) → S3 ACP fs/terminal PEP (`provider-acp/src/server/clientPolicy.ts`) →
S2 provider approvals (Claude `canUseTool` L9265; Codex handlers L5039–5396; ACP `session/request_permission`) →
S4 EffectWorker authority + unknown outcome (L99–560) and **S4b recovery gating** (`EffectOutbox.ts` L492–530, `ProviderRuntimeRecoveryService.ts` L700–788) → S5 per-run receipt link (EventSink L410–460) → S6 MCP access →
S7 git writes → S8 terminals → S9 provider spawn under sandbox (new work). Precedent: T3 already ships a Rust stdio
sidecar (`native/resource-monitor`).

## 4. Conflicts with "one authoritative log" and the resolution

T3 events are entity snapshots, compacted every 6 h, payloads rewritten for dedupe, no hash chain, outbox outcomes
mutable and pruned after 7 days, `synchronous=NORMAL` (R02 §11, C1–C12). Resolution: **one authority per fact**
(`07_*` §2). T3 = conversation/run truth; Core Ledger = grants/decisions/outcomes/missions/completion,
cross-referenced through one compaction-exempt per-run `zain.run-receipts` event (07 §4).

## 5. Inherited risks (must be budgeted, R02 §13)

DB growth and writer stalls (#21840, #23482, #19780), memory (#18485 11.5 GB nightly; #15579 preview webviews 2.7 GB),
stuck runs (#15197, #22510), Windows startup (#25262), approval bugs (#24882, #21935), client catalog data loss
(#4750, #23470). The default **Full access** permission mode must be removed (S1).

## 6. Effort (ESTIMATE, R02 §14)

R02 figures: MVP fork + Core seams 18–34 pw; + minimal editor 22–38 pw; + real sandbox 26–48 pw; upkeep 0.5–1 pw/month.
These exclude Brain, missions, completion, WebAuthn and policy UI; the bottom-up v1 estimate is generated (GENERATED_PLAN_REPORT.md).

## 7. Verdict

FORK FOUNDATION at the pin, no upstream tracking. Conditional on G2 (build/run/measure on Windows) and G3 (seam spike)
in `00_*` §7.
