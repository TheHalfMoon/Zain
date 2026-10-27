# 03D — Orca IDE Source-Level REA (synthesis)

```text
DONOR = stablyai/orca @ e310a63624c86c0e91e9d77df71f038b91d79ea0 (2026-10-27), MIT (Lovecast Inc.)
SUPERSEDES = prior WePLD pin b5b727bd (5,577 commits stale)
FULL_REA = research/R03D_ORCA.md (785 lines)
RIGHTS = PUBLIC_OPEN_SOURCE (MIT) + FOUNDER-ATTESTED; carry Apache-2.0 notices (agent-browser, serve-sim, sherpa-onnx);
         modules importing @anthropic-ai/claude-agent-sdk inherit Anthropic's terms
ROLE_IN_V3 = MODULE DONOR (ports into WePLD-owned packages) + REFERENCE SPECIFICATIONS. Not the foundation.
```

## 1. What Orca is (verified)

Electron 43 + React 19 renderer with one zustand store (~50 slices); ≥392 IPC channels and 778 RPC methods; a terminal
daemon (node-pty, protocol v52) that survives app restarts; headless `orcad`; **three SQLite stores** (profile-state,
agent-session-journal, orchestration v43) and no single authoritative log; ~2.13M production LOC in `src/` plus 2.94M
test LOC; ~45 TUI CLI agents via PTY plus structured Claude/Codex/ACP/Pi sessions; Monaco (no LSP); embedded browser with
Design Mode and 91 automation methods; computer use (macOS/Windows/Linux); GitHub/GitLab/Jira/Linear; SSH worktrees;
mobile via the Stably relay. Churn ≈150 commits/day; 4,194 open issues incl. 421 Windows-labelled (R03D §0–§13).

## 2. Decision-critical hypotheses from the brief

| Hypothesis | Verified? | Evidence |
|---|---|---|
| T3 has the stronger server-led orchestrator / event log / remote-client model | **Yes** | T3 single EventSink transaction + receipts + outbox vs Orca's three stores (R03D §6.4, §16.1) |
| Orca has the stronger IDE/editor/terminal/browser/worktree foundation | **Partly** | Stronger editor (Monaco), browser/Design Mode, computer use, TUI-agent breadth, Linear, worktree-removal safety; terminal roughly equal; both lack LSP |
| Orca modules can be extracted | **Only the small ones** | Store-bound UIs: terminal 150 store importers, editor 95, browser 54 |

## 3. Port list (Option A) in value ÷ effort order

| # | Module | Path @e310a636 | LOC | Extractability | ESTIMATE pw | Target in WePLD |
|---|---|---|---|---|---|---|
| 1 | Design Mode guest scripts + payload clamp | `src/main/browser/grab-*.ts`, `browser-grab-payload.ts`, `src/shared/browser-grab-types` | ~1.1k | High | 3–6 | Browser pane → composer; Design Studio element targeting |
| 2 | TUI agent catalog | `src/shared/tui-agent-config*.ts` | 443 | High (data) | with #3 | "CLI agents" in terminal |
| 3 | Hook listener + OSC 7501 status | `src/shared/agent-hook-listener`, `src/shared/program-status` | 9.5k | Medium-High | 3–5 | agent status for PTY agents |
| 4 | Process host (Windows tree-kill, quoting, shims) | `src/packages/process-host/src` | 1.9k | High (package) | 1–2 | Server process runner |
| 5 | Linear client | `src/main/linear` | 6.8k | High | 2–4 | Connections |
| 6 | Computer-use sidecar | `src/main/computer`, `native/computer-use-*` | 4.1k + native | Medium-High | 3–6 | Phase 9, gated by Core |
| 7 | Monaco surface + diff comments | `src/renderer/src/components/{editor,diff-comments}` | 62k / 2.6k | Low-Medium / High | 4–8 | Editor, rebound to T3 state |
| — | Terminal daemon, worktree-removal safety, wire-compat rules, persistence quarantine | `src/main/daemon`, `src/main/worktree*`, `docs/reference/remote-wire-compatibility.md@b5b727bd` (deleted at HEAD) | — | Reference only | — | design specifications |

## 4. Never ship (privacy / identity)

`onorca.dev` endpoints, the PostHog host/key, the `stablyai/orca` update feed (silent cross-update risk),
`com.stablyai.orca`, `orca://`, `~/.orca`, `x-orca-*` hook headers written into users' `~/.claude` / `~/.codex`,
daemon pipe names, 583 `ORCA_*` env vars. A CI grep gate is mandatory (R03D §15, §17).

## 5. Options verdict

A (T3 + Orca modules) **chosen**. B rejected (≥30–60 pw + ≥1 FTE upkeep, a fourth store, the Windows bug load).
C (`orcad` sidecar) is a time-boxed bridge only (6–10 pw per capability, doubled RAM). D (own platform) is the fallback
(60–120 pw).
