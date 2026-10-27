# 03C — Claude Code CLI, Desktop and Agent SDK: Protocol REA (synthesis)

```text
FULL_REA = research/R03C_CLAUDE_CODE.md (all flags/subcommands, ~120 slash commands, 33 hook events, SDK surface)
OBSERVED = local claude.exe 2.1.291 --help (read-only); npm latest 2.1.311; stable 2.1.308 (2026-10-27)
SOURCE_STATUS = CLI closed ("All rights reserved"); TS Agent SDK 0.3.311 proprietary; Python SDK 0.2.174 MIT source
                (Commercial Terms govern use); claude-code-action MIT; @agentclientprotocol/claude-agent-acp 0.97.0 Apache-2.0
```

## 1. What WePLD needs from Claude Code, and how it gets it

| Need | Claude Code mechanism (public) | WePLD route | Phase |
|---|---|---|---|
| Drive Claude as a worker | Agent SDK `query()` streaming mode (T3 already does: `ClaudeAdapterV2.ts`) | **INTEGRATE** via T3 adapter; ACP adapter as generic alternative | 2 |
| Pre-decision on every tool call | `PreToolUse` hook (allow/deny/ask/**defer**); `canUseTool` for residual prompts | **ADAPT**: hook → Core `effect.propose`; deny rules compiled into `disallowedTools`/managed settings as floor | 3 |
| Completion gating | `Stop` / `SubagentStop` hooks can block | **ADAPT**: block stop until Core `completion.evaluate` passes | 5 |
| Session identity | `sessionId` option, `resume` + `forkSession`, `parent_tool_use_id` | **ADAPT**: UUIDv5(task_attempt) mapping stored in T3 + Core | 2 |
| Hermetic launch | `--bare` / `settingSources: []`, `strictMcpConfig`, `managedSettings`, per-tenant `CLAUDE_CONFIG_DIR` | **ADAPT** (R03C §10.2 profile) | 3 |
| Structured hand-back | `outputFormat` JSON schema | **ADAPT** | 4 |
| Telemetry | OTel metrics/events | **INTEGRATE** into a WePLD **local-only** OTel sink (observational, `TELEMETRY_SPAN != EVIDENCE`; P2 removes donor egress telemetry, P6 adds the local sink) | 6 |
| Skills/plugins/subagents/output styles/CLAUDE.md | file formats (SKILL.md, plugin.json, `.claude/agents`) | **COPY formats** (open), load into any worker where supported | 5 |
| MCP (stdio/http/sse, OAuth) | `mcp` subcommands, scopes | **ADAPT** via T3 `/mcp` + rmcp/TS SDK | 5 |
| Worktrees, checkpoints/rewind | `--worktree`, checkpoints | T3 owns worktrees/checkpoints (git authority); Claude checkpointing off or convenience only | 2 |
| Desktop Code tab features (parallel sessions, diff + inline comments, PR/CI, preview, terminal, editor, side chats, tasks, schedules, remote control) | Closed app | **REIMPLEMENT FROM OBSERVED BEHAVIOR** on the T3 fork (most already exist in T3) | 2–6 |
| Cloud sessions / teleport / Remote Control | Anthropic-hosted | **DEFER**; WePLD equivalent = self-hosted runner + T3 remote clients | 10 |

## 2. Permission relay contract (WePLD-owned authority)

1. PreToolUse hook → Core `effect.propose`; on allow the hook also calls `effect.dispatch` (fsynced) **before** returning
   allow, so a kill mid-Edit leaves a dispatch record and CC-T02 can derive UNKNOWN (hook `deny` holds even in bypass;
   `onFailure: block` ≥2.1.295).
2. Compiled deny floor in managed settings (survives hook failure).
3. `canUseTool` → Core `APPROVAL_REQUIRED` → Inbox → `approval.resolve` (use `defer` for waits longer than the process).
4. PostToolUse → Core `effect.report` (outcome evidence).
5. Never launch with `bypassPermissions`/`--dangerously-skip-permissions` outside a disposable VM; never treat Claude's
   `auto` classifier as WePLD authority. Caveat: bare-tool allow rules shadow `canUseTool` — forbid them.

## 3. Authentication posture (binding)

API key / Bedrock / Vertex / Foundry for any WePLD-initiated Claude usage. The Agent SDK is **not bundled** in the installer
until G4 (08 P2 task); `claude-agent-acp` depends on the same SDK and does not avoid this. Optional user-owned unmodified `claude`
binary in a WePLD terminal (user signs in through Anthropic's own flow; WePLD never reads `.credentials.json` or tokens).
Subscription-backed SDK orchestration: **UNKNOWN**, blocked until written confirmation (G4). Branding: "powered by
Claude", never "Claude Code Agent". Policy summary (paraphrased, with sources) in R03C §10.5.

## 4. Gaps between local CLI and docs (observed)

Local 2.1.291 lacks `daemon`, `remote-control`, `self-hosted-runner` subcommands and some documented flags
(`--max-turns`, `--permission-prompt-tool`, `--init`, `--teammate-mode`, `--channels`) → WePLD must feature-detect via
the SDK `system/init` capabilities and pin versions with contract tests on upgrade.

## 5. Parity tests (excerpt; full list in 03F)

| Test | Assertion |
|---|---|
| CC-T01 | A Claude worker under WePLD cannot write outside its worktree even when the model requests it (hook deny + floor) |
| CC-T02 | Killing the Claude process mid-Edit yields a Core `EFFECT_OUTCOME_UNKNOWN` or a reconciled result by file hash |
| CC-T03 | Retry of a task attempt resumes the same Claude session (`resume`) or forks with a recorded parent edge |
| CC-T04 | No OAuth token or `.credentials.json` content is ever read by WePLD processes (file-access audit) |
| CC-T05 | Stop is blocked while required gates are failing; unblocked when Core returns `COMPLETED_TRUSTED` |
