# 03 — Competitor Research (delta to V3 R10)

```text
BASELINE = specs/008-wepld-v3-unified-replan/research/R10_COMPETITORS.md (2026-10-27), R04_AMP.md, 03C_*
THIS     = delta research on 2026-11-08 from official changelogs, docs and repositories (read-only), plus forums
LABELS   = V verified (official docs, changelog, release or source) · R reported (forum, press, issue) · U unverified
LIMITS   = Antigravity's changelog was read only in part; several JetBrains pages returned 403 (snippets only);
           Windsurf/Devin and JetBrains framework details are R; no product was run hands-on
```

## 1. Status changes since 2026-10-27

| Product | Change | Label |
|---|---|---|
| Windsurf | Renamed **Devin Desktop** on 2026-06-02 (Cognition); the Cascade agent was removed in v3.9.19; "Devin Local" is the only local agent; still a VS Code fork on Electron (v3.12.28 on VS Code 1.141.2, Electron 43.8.3) | V |
| Roo Code | Shut down 2026-05-15; repository archived | V (repo), R (reason) |
| Continue | Open-source repository is read-only and unmaintained (README); last release 2.0.0 in June 2026 | V |
| Aider | Maintenance mode; no feature release since August 2025 | V |
| Cursor | Agent SDK GA (10-20), Live Apps cloud builds (11-05), voice chat with agents (11-06); embeddings-based codebase index turned down in favour of a local grep index ("Instant Grep"); **no native Windows terminal sandbox** (staff statements; Windows routes through WSL2) | V / R |
| VS Code + Copilot | 1.145 (11-04): several agent harnesses in one session (Copilot, Claude, Codex), organizations can require sandboxing; Windows sandbox **experimental, off by default**, needs Windows 11 25H2 build 26200.9550+ or 26H1 28000.3086+; open Windows sandbox bugs (#346199, #345713, #338112) | V |
| JetBrains | Air (agent host for Codex, Gemini, Copilot, Claude Agent, Cursor, Junie and ACP agents) in IDE EAP; docs say agents cannot use local models; Air Context is a cloud embeddings service | V / R |
| Google Antigravity | IDE plus a standalone 2.0 agent app; Windows sandbox via AppContainer on Windows 11 24H2 with the August 2026 update; no BYOK or local models documented | V |
| Claude Code | 2.1.314–2.1.319: `blockWritesOutsideWorkingDirectories`, `denyInsteadOfPrompting`; native Windows still unsandboxed; does not support routing to non-Claude models | V |
| Codex | CLI 0.165–0.167; Windows sandbox **on by default** with MXC, elevated and unelevated tiers; local models through `--oss` with Ollama or LM Studio | V |
| OpenCode | v2.2.5–2.2.6 (repository moved to `anomalyco/opencode`), Electron desktop beta with Windows installers; no OS sandbox; cannot detect local-model tool support | V |
| Amp, Factory, Kilo Code, Zed, Cline | Amp: team features, still no native Windows. Factory 1.0 desktop on Windows with sandbox only on macOS/Linux/WSL2. Kilo Desktop beta. Zed v1.27 parallel agents and terminal threads, no sandbox. Cline unchanged since 10-26 | V |

## 2. Capability matrix (Y shipped · P partial or gated · N no · ? unverified)

| Capability | Cursor | Devin Desktop | Antigravity | VS Code | JetBrains | Claude Code | Codex | OpenCode | Zed | **Zain target** |
|---|---|---|---|---|---|---|---|---|---|---|
| Inline edit | Y | Y | Y | Y | Y | N | N | N | Y | R1 (Z-12) |
| Tab completion | Y | Y | Y | Y | Y | N | N | N | Y | R1, local (Z-12) |
| Multi-file agent | Y | Y | Y | Y | Y | Y | Y | Y | Y | R0a |
| Parallel agents | Y | Y | Y | Y | P | Y | Y | Y | Y | R0 |
| Worktree isolation | Y | Y | Y | Y | Y | Y | Y | Y | Y | R0a |
| Checkpoints / rollback | Y (files) | P | P | Y (files) | P | Y (files) | P | Y | Y | R0b with quarantine (Z-27) |
| Plan mode | Y | Y | Y | Y | Y | Y | Y | Y | ? | R0 unenforced; R2 enforced |
| Code review agent | Y | Y | ? | Y | P | Y | Y | ? | N | R1 delegated; R3 engine |
| Browser / preview | Y | Y | Y | P | ? | Y | Y | ? | N | R0b hardening; R2 lanes |
| Computer use | P | P | P | P | ? | P | Y (R) | N | N | R6 |
| Local models | P (chat via vendor servers) | ? | N | P (no completion) | P (chat only) | P (gateway only) | Y | Y | Y | R0 all surfaces (Z-11) |
| Native Windows sandbox | N (WSL2) | N | Y (AppContainer, new builds) | P (experimental, off) | P (Docker only) | N | Y (default on) | N | N | R1 ProcessHost; S-01 R5 or R2 (DEC-06) |
| MCP | Y | Y | Y | Y | Y | Y | Y | Y | Y | R2 (V-05) |
| ACP host | P | Y | P | N (own AHP) | Y | P | P | Y | Y | R0a (inherited from T3) |

Footnotes with URLs are in §5. A "Y" means shipped per official sources, not that it works well.

## 3. Gaps a privacy-first, local-first, Windows-first, provider-neutral IDE can own

1. **Native Windows sandbox, on by default, compatible with PowerShell, git credential helpers and node.** Only Codex
   ships one on by default, and its best tier needs specific builds. VS Code's is experimental. Cursor's routes
   through WSL2 and breaks PowerShell and git for some users (R). Claude Code, Devin and Factory are unsandboxed on
   native Windows (V).
2. **Local models on every surface.** VS Code excludes local models from inline suggestions and needs GitHub for
   semantic search. JetBrains agents cannot use local models. Claude Code does not route to non-Claude models.
3. **One policy layer over every hosted agent.** Devin Desktop, JetBrains Air, Zed and VS Code host third-party
   agents, but each agent keeps its own permission model.
4. **Rollback that admits what it cannot undo.** Competitors restore files and do not track shell side effects. Zain
   should quarantine instead of deleting and report UNKNOWN coverage for shells.
5. **Auditable outbound traffic per agent** with default-deny and a viewable log.
6. **Cost control** with per-task budgets and local metering, independent of vendor quotas.
7. **Portable, open project state** (rules, MCP config, skills, history) after several vendor shutdowns and renames.
8. **A local-only code index** that works offline.

## 4. Table stakes for the first usable release, and how Zain meets them

| Table stake | R0 | Later |
|---|---|---|
| Editor with LSP | **External editor bridge (Z-13)** | Monaco R1 (F-17); LSP R3, or R1 per DEC-05 |
| Tab completion and inline edit | Not in R0 | R1 (Z-12) |
| Multi-file agent with modes and rules files | Yes (T3) | — |
| Per-hunk accept/reject, per-turn checkpoint | Yes (T3) + quarantine (Z-27) | — |
| Parallel sessions in worktrees, background runs | Yes (T3) | Missions R2 |
| MCP client with allowlist | Partial (T3 MCP) | V-05 R2 |
| BYOK, OpenAI-compatible endpoints, Ollama/LM Studio discovery | Z-11 | — |
| Sandboxed commands on native Windows | **No** (supervised approvals only, F-07) | C-25 R1; S-01 later |
| Crash-resumable sessions | Z-21 | — |
| Local code search | Text search (T3) | Local index R1 (Z-28) |
| Browser preview | Yes (T3, hardened Y-00) | Lanes R2 |
| Local review over a diff | No | K-08 R1 |
| ACP host | Yes (T3) | — |
| Import of rules, MCP config, skills | No | V-05/V-06 R2 |

**Honest reading.** R0 is a strong *agent workbench* with a bridge to an external editor. It is not yet a complete
IDE by competitor standards. R1 closes the editor and completion gaps. That is why DEC-05 asks whether to pull LSP
forward.

## 5. Sources (accessed 2026-11-08 unless dated)

Cursor: cursor.com/changelog; cursor.com/docs/agent/security/run-modes; cursor.com/docs/context/semantic-search;
cursor.com/docs/settings/api-keys; forum.cursor.com threads 162520 (2026-06-05) and 165059 (2026-07-07).
Devin Desktop: devin.ai/blog/windsurf-is-now-devin-desktop (2026-06-02); docs.devin.ai/desktop/changelog;
docs.devin.ai/cli/sandbox.md. Antigravity: antigravity.google/docs/changelog; antigravity.google/docs/permissions;
antigravity.google/docs/sandbox. VS Code: code.visualstudio.com/updates/v1_145 (2026-11-04);
code.visualstudio.com/docs/agents/run/agent-sandboxing; code.visualstudio.com/docs/copilot/customization/language-models;
github.com/microsoft/vscode issues 346199, 345713, 338112. JetBrains: jetbrains.com/help/air/execution-environments.html
(2026-10-27); jetbrains.com/help/ai-assistant/use-custom-models.html (2026-10-13); jetbrains.com/help/air/air-context.html
(2026-11-05). Claude Code: github.com/anthropics/claude-code/releases; code.claude.com/docs/en/sandboxing;
code.claude.com/docs/en/llm-gateway. Codex: github.com/openai/codex/releases; learn.chatgpt.com/docs/windows/windows-sandbox.
OpenCode: github.com/anomalyco/opencode/releases; opencode.ai/docs/providers. Others: ampcode.com/chronicle;
docs.factory.com/autonomy-and-safety/sandbox.md; github.com/zed-industries/zed/releases/tag/v1.27.0;
github.com/RooCodeInc/Roo-Code (archived); github.com/continuedev/continue.
