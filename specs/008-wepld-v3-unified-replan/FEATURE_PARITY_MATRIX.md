# Feature Parity Matrix — Zain current vs donors vs target

Legend: ✓ verified present · ◐ partial/light · ✗ absent · ? UNKNOWN · (src) where verified. Target column = planned
phase. Nothing in the Target column is implemented yet.

| Capability | Zain now (main 0a843a2) | T3 @36d4d711 | Orca @e310a636 | Claude Desktop / Code / Design | Amp | Target Zain |
|---|---|---|---|---|---|---|
| Desktop app | ◐ Tauri status window | ✓ Electron | ✓ Electron | ✓ (Win/mac; Linux beta) | ✓ macOS app; CLI (Win via WSL) | P2 |
| Multi-provider agents | ✗ | ✓ Claude, Codex, ACP, OpenCode, Pi, Cursor… | ✓ ~45 CLIs + structured | ✗ Claude only | ✗ Amp-routed models | P2 |
| Durable orchestration log | ✗ | ✓ (compacting) | ◐ three stores | ? closed | ? closed | P2 (inherit) |
| Effect-time authority (policy per effect) | ✗ (design only) | ✗ relay | ✗ relay | ◐ modes + per-tool rules + admin ceilings | ✗ none by default | **P3** |
| Unknown-outcome receipts / reconciliation | ✗ (design only) | ✗ cancel-only | ✗ | ? | ✗ | **P3** |
| Hash-chained evidence ledger | ◐ S2 evidence generations | ✗ | ✗ | ✗ | ✗ | **P3** |
| Project identity / Doctor | ✓ S2 | ◐ | ◐ | ✗ | ✗ | keep |
| Worktrees + parallel sessions | ◐ read-only topology | ✓ | ✓ | ✓ (Code) | ✓ (orbs/runners) | P2 |
| Checkpoints / revert | ✗ | ✓ hidden refs | ◐ | ✓ checkpoints/rewind | ? | P2 |
| Diff review + inline comments | ✗ | ✓ | ✓ (Monaco) | ✓ | ✓ changes pane | P2/P6 |
| PR / CI tracking | ✗ | ✓ 7 forges | ✓ GitHub/GitLab/… | ✓ | ✓ follow CI | P2 + P4 continuation |
| Terminal | ✗ | ✓ libghostty + node-pty | ✓ xterm WebGL + daemon | ✓ | ✓ shared tmux | P2 |
| Code editor | ✗ | ◐ light | ✓ Monaco (no LSP) | ✓ built-in editor | ✗ (attach to IDE) | P6 |
| In-app browser / preview | ✗ | ✓ | ✓ + Design Mode + 91 automation methods | ✓ preview; Chrome extension | ✓ portals | P2 + P6 |
| Computer use | ✗ | ✗ | ✓ | ◐ beta (Pro/Max) | ✗ | P9 (gated) |
| Design canvas (Claude Design-class) | ✗ | ✗ | ◐ Design Mode capture only | ✓ (preview→GA in convos) | ✗ | **P7** |
| Documents/slides/dashboards | ✗ | ◐ previews | ◐ previews | ✓ Artifacts family | ✗ | P9 |
| Missions / schedules / wait-for-CI | ✗ | ◐ restart continuations | ◐ coordinator | ✓ scheduled tasks | ✓ schedules, webhooks | **P4** |
| Project memory that outlives models | ✗ | ◐ context handoff | ✗ | ✓ (Claude-only) | ✓ threads (vendor-hosted) | **P4** |
| Independent review + Trusted Completion | ✗ | ✗ | ✗ | ◐ code review / security review | ◐ review skill | **P5** |
| Skills / plugins / MCP | ✗ | ✓ MCP; ◐ skills via providers | ✓ | ✓ | ✓ | P5 |
| OS sandbox for agents | ✗ | ✗ | ✗ | ◐ (not native Windows) | ◐ orbs (remote) | **P8** |
| Remote / mobile control | ✗ | ✓ web/mobile/relay | ✓ mobile via relay | ✓ | ✓ | P10 (no hosted relay) |
| Self-hosted runner | ✗ | ✓ `t3 serve` (no Win service) | ✓ `orca serve` | ✗ | ✓ self-hosted orbs | P10 |
| Offline/local-first core | ✓ (by design) | ✓ (local server) | ✓ | ✗ (cloud) | ✗ | keep |
| Telemetry off by default | ✓ | ✗ PostHog | ✗ PostHog | ✗ | ✗ | P2 |

Source rows: R02, R03, R03B, R03C, R03D, R04, R10; Zain column from `01_LIVE_WEPLD_AUDIT.md`.

## Founder-amendment components (2026-10-28)

| Capability | Zain now | T3 | Orca | Claude | Amp | Target Zain |
|---|---|---|---|---|---|---|
| Code review with findings, dispositions, fix apply + undo | ✗ | ◐ diff annotations | ◐ diff comments | ◐ Code Review / security review | ◐ review skill | **P5** (Zain Code Review) |
| Engineering loop with E2E verification evidence | ✗ | ✗ | ✗ | ◐ (skills/plugins) | ◐ | **P5** (Engineering System) |
| Enforced read-only Plan Mode with durable artifacts | ✗ | ◐ plan mode (enforcement unverified) | ✗ | ✓ plan mode (Claude Code) | ✗ | P2 unenforced → **P3/P5** |
| Browser control with receipts, redirect gating, isolated profiles | ✗ | ◐ automation, no pre-request gate, cookie import | ◐ 91 methods, cookie import | ✓ Claude in Chrome (behavior ref.) | ✗ | P2 hardening → **P5** → P9 |
| Desktop/terminal tools for agents (DeskGate) | ✗ | ◐ terminal tools | ◐ | ✓ Desktop Commander-like via MCP | ◐ | **P3** local, P10 remote |
