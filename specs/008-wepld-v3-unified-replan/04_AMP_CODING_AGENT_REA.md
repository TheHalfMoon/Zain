# 04 — Amp Coding Agent REA (synthesis)

```text
FULL_REA = research/R04_AMP.md (62 manual pages via ampcode.com/llms.txt, Chronicle, /pricing, /modes, /security;
           16 public ampcode repos inventoried), research/R10_COMPETITORS.md (13 competitors, 26 OSS pins)
SOURCE_STATUS = Amp core CLOSED (private ampcode/amp → 404). @ampcode/sdk, /plugin, /cli = "Amp Commercial License".
                ampcode/official-plugins (mode prompts + skills) has NO LICENSE → study only, never copy.
ROLE_IN_V3 = BEHAVIOR ORACLE + interface oracle (self-hosted orb dispatch contract, webhook semantics). No code reuse.
```

## 1. Brief vs current reality (2026-10-27)

| Brief assumption | Current state | Evidence |
|---|---|---|
| Modes smart/rush (the Dial) | Deprecated 2026-07-09 → `low/medium/high/ultra`, fixed per thread | R04 §2.1 |
| Oracle / Librarian / Search subagents | Folded into **Task** subagent loading read-only skills; plus Read Thread | R04 §3 |
| Orbs | **Exist; flagship.** Per-thread remote machines, 72 h snapshots, idle-pause (agent idle 5 min + user idle 20 min), wake on event; six sizes $0.08–$2.13/h; self-hosted orbs launched 2026-10-22 (spawn/pause/delete contract, Helm chart) | R04 §4 |
| Editor extension | Removed 2026-02-19; CLI attaches to editors | R04 §0 |
| Ad-supported free tier | Ads removed 2026-03-30; free (Hobby) if you bring your own compute + model keys/subscriptions | R04 §8.4 |
| Approval model | **No approvals by default**; control via plugins and per-MCP-tool policy | R04 §8.2 |

## 2. What Zain should learn (adopt as behavior), and what it must beat

| Amp strength | Zain response | Measurable target (proposed, not measured) |
|---|---|---|
| Subagents with isolated context | T3 subagents + structured result contract validated by Core | % subagent results passing schema + evidence checks |
| Thread search/Read Thread | Brain + local thread index (Codex `thread-store` crates as donor, Apache-2.0) | offline query p95; zero vendor storage |
| Orbs lifecycle | Executor abstraction: local worktree → container → self-hosted runner; same Server+Core stack | wake-to-first-tool p95; $0 idle |
| Webhooks at-least-once with Idempotency-Key | Same semantics + built-in dedupe + signature verification (Amp leaves both to plugins) | duplicate logical resumes = 0 |
| Follow CI / GitHub subscriptions | Core continuations on exact commit | exact-commit replayable |
| Plugins (`tool.call` allow/reject/modify/synthesize) | Same hook shape, but decision owned by Core and plugins capability-scoped | plugin escape tests |
| Per-role model choice | Independent per-role pins (reviewer ≠ builder), which Amp's Task subagents cannot do | 100% role pins in ledger |

Where Amp is weak and Zain wins by design: no default approvals; Windows CLI only via WSL; vendor-hosted threads
(30-day deletion policy); routing failover on provider errors undocumented (UNKNOWN).

## 3. Acquisition map summary (32 rows in R04 §10)

All 32 Amp features: **source unavailable** (or unlicensed text) → behavior oracle only. Every row has an OSS donor
candidate or a Zain build. Highest-value donors referenced there and carried into `06_*`:
`openai/codex` crates (sandboxing, windows-sandbox-rs, execpolicy, thread-store, rmcp-client, code-mode, skills,
app-server-protocol; Apache-2.0 @603a7baf), ACP spec/SDKs (Apache-2.0 @e50f62b4), OpenHands software-agent-sdk
(MIT), goose crates (Apache-2.0), vibe-kanban crates (Apache-2.0), OpenCode (MIT).

## 4. Competitive grounding (R10)

ACP has become the de-facto editor↔agent protocol; Codex has the strongest default local safety (OS sandbox +
approvals); Cursor 3.0 added an agents window + `/worktree` + `/best-of-n`; the standalone Codex app was folded into the
ChatGPT desktop app (~2026-07-09, press-reported). **No competitor documents exactly-once side effects or crash-safe
effect logs** — Zain's clearest ownable gap (still to be demonstrated, `09_*`).
