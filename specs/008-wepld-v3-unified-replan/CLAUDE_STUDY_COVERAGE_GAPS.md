# Claude Features — What Has NOT Been Studied Hands-on or in Full

```text
DATE = 2026-10-27
SCOPE = all 377 rows (after 2026-10-27 depth pass) of research/R03_CLAUDE_CENSUS.md + R03B (Design) + R03C (Claude Code)
METHOD = each row's best evidence = deepest read level among the Help Center articles it cites (R03 §7a)
```

## 1. Headline (no rounding up)

1. **Hands-on: ZERO Claude product features were exercised in a UI.** Every census row is `observed_test = NOT_OBSERVED`.
   "VERIFIED SHIPPING" means *documented as available* on 2026-10-27, not *observed working*. The only hands-on
   observation in the whole Claude track is read-only `claude --help` output from the local CLI 2.1.291 (R03C §0.1) and
   read-only descriptions of the Design / Design System artifact types in this environment (R03B [OBS]).
2. **Fully studied (cited Help Center article read in full via complete-fact extraction): 110 of 377 rows.**
3. **Read through a summarising fetch tool, gates re-checked on live text: 212 rows.**
4. **Gate-digest only: 0 rows** (was 78; all re-read in full on 2026-10-27).
5. **Evidenced by non-Help-Center official pages read live on 2026-10-27 (product pages, release notes, platform/code docs): 55 rows** (§4).
6. **Not studied (remaining):** Managed Agents reference + rate limits, encryption-key/identity-federation admin pages,
   inference-hook spec, MCP tunnel deployment; Claude Code changelog before 2.1.299; platform release notes before
   2026-09-22; the 91 pass-1 summary-read articles were not re-read; mobile-specific interaction details, accessibility behavior, performance characteristics, any
   enterprise admin console behavior.
7. **Claude Design (R03B):** documented features only; no canvas session was run; Figma export, web capture,
   breakpoints, admin edit-lock and true two-way sync remain UNKNOWN.
8. **Claude Code (R03C):** flags/subcommands observed via `--help` only (local 2.1.291 lags npm 2.1.311); no session,
   hook, plugin, MCP, worktree, desktop Code tab, cloud session or GitHub Action was exercised.

## 2. Depth distribution

| depth | rows |
|---|---|
| FULL_TEXT_READ | 110 |
| READ_VIA_SUMMARY_TOOL (gates rechecked on live text) | 212 |
| GATE_DIGEST_ONLY | 0 |
| NON_HELP_CENTER_PAGE_ONLY | 55 |

## 3. Rows whose best evidence is GATE_DIGEST_ONLY (not read in full)

| feature_id | family | feature | status | route | cited articles |
|---|---|---|---|---|---|

## 4. Rows evidenced only by non-Help-Center official pages (product pages, release notes, docs) read in pass 1

| feature_id | family | feature | status | route | evidence |
|---|---|---|---|---|---|
| CL-B-043 | B | Claude for Excel add-in (answers questions about cells, updates assumptions without breaking formulas, builds models fro | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | claude.com/claude-for-microsoft-365; RN |
| CL-B-044 | B | Claude for PowerPoint add-in (builds slides in your template, edits selected content, native charts and diagrams) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | claude.com/claude-for-microsoft-365 |
| CL-B-045 | B | Claude for Word add-in (tracked-change edits, comment-thread replies, company styles) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | claude.com/claude-for-microsoft-365 |
| CL-B-046 | B | Claude for Outlook add-in (inbox triage from one prompt, drafted replies, meeting times across calendars; drafts and inv | BETA-PREVIEW | USE VIA OFFICIAL INTEGRATION | claude.com/claude-for-microsoft-365; cla |
| CL-B-047 | B | Shared context across Excel/PowerPoint/Word/Outlook (changes update every open file; dropped PDFs referenced across apps | VERIFIED SHIPPING | ADAPT | claude.com/claude-for-microsoft-365; RN |
| CL-D-002 | D | Desktop app Code tab (visual diff review, parallel sessions side by side, recurring scheduled tasks, cloud sessions; inc | VERIFIED SHIPPING (Linux d | USE VIA OFFICIAL INTEGRATION | code.claude.com/docs/en/overview; R03C |
| CL-D-005 | D | VS Code / Cursor extension (inline diffs, @-mentions, plan review, conversation history) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | code.claude.com/docs/en/overview |
| CL-D-006 | D | JetBrains plugin for IntelliJ IDEA, PyCharm, WebStorm and others (interactive diff viewing, selection context; requires  | BETA-PREVIEW (marketplace  | USE VIA OFFICIAL INTEGRATION | code.claude.com/docs/en/overview; claude |
| CL-D-007 | D | GitHub Actions and GitLab CI/CD integration (automate code review and issue triage in CI; `claude -p` scripting) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | code.claude.com/docs/en/overview |
| CL-D-009 | D | Slack: mention @Claude with a bug report and get a pull request back (Claude Code in Slack; Claude Tag brand in Help Cen | VERIFIED SHIPPING (Claude  | DEFER | code.claude.com/docs/en/overview; claude |
| CL-D-011 | D | Channels (push events from Telegram, Discord, iMessage or own webhooks into a running session) | BETA-PREVIEW (research pre | DEFER | code.claude.com/docs/en/overview; R03C ( |
| CL-D-012 | D | Cloud scheduled tasks (formerly routines; keep running with computer off; API-call and GitHub-event triggers; create fro | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | code.claude.com/docs/en/overview |
| CL-D-013 | D | Session handoff: `claude --teleport` (web/mobile to terminal), `/desktop` (terminal to Desktop), `claude --cloud` (termi | VERIFIED SHIPPING | DEFER | code.claude.com/docs/en/overview |
| CL-D-019 | D | Claude Code changelog and weekly "What's new" digests (pointer); newest entry read: 2.1.311 (2026-10-26) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION ( | code.claude.com/docs/en/changelog |
| CL-D-028 | D | Claude Code changes 2026-10-14..26 (pointer): idle compaction for idle conversations over 200K tokens; `/auto-mode-setup | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION ( | code.claude.com/docs/en/changelog (2.1.2 |
| CL-E-097 | E | Claude Tag API (`/v1/organizations/claude_tag/`): read and change Claude Tag settings on Slack channels and workspaces,  | BETA-PREVIEW (header `expe | DEFER | platform.claude.com/docs/en/release-note |
| CL-F-001 | F | claude.ai web app (chat, Cowork integrated into Claude.ai, artifacts, connectors, projects, memory) | VERIFIED SHIPPING | REIMPLEMENT FROM OBSERVED BEHA | claude.com/product/overview |
| CL-F-008 | F | Phone pairing: scan QR code or visit claude.ai/mobile; pair desktop and mobile; share a phone task to start it in Cowork | VERIFIED SHIPPING | ADAPT | claude.com/download |
| CL-F-011 | F | Office and Google add-ins distribution: Microsoft Marketplace (Excel, PowerPoint, Word; Outlook beta, separate listing), | VERIFIED SHIPPING (Outlook | USE VIA OFFICIAL INTEGRATION | claude.com/download; claude.com/claude-f |
| CL-F-017 | F | Plans and list prices (Free, Pro, Max 5x/20x, Team Standard/Premium 2-150 seats, Enterprise seat + API-rate usage, 20-se | VERIFIED SHIPPING | DEFER | claude.com/pricing (raw text) |
| CL-F-018 | F | Plan gate matrix (pricing comparison table, re-read 2026-10-27): Free has no Opus, Research, Claude Code, Chrome, M365 a | VERIFIED SHIPPING | DEFER | claude.com/pricing (raw text) |
| CL-F-023 | F | Claude Platform / API release notes (pointer); entries 2026-09-22 to 2026-10-23 read and turned into family G rows | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION ( | platform.claude.com/docs/en/release-note |
| CL-F-035 | F | Claude Models on Google Cloud (Anthropic managed): Claude API operated by Anthropic, reached through a Google Cloud proj | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | platform.claude.com/docs/en/release-note |
| CL-G-001 | G | Messages API tool use: client tools (user-defined with input_schema; Anthropic-schema bash, text editor, memory, compute | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION ( | PD/agents-and-tools/tool-use/overview; P |
| CL-G-002 | G | Computer use tool: client toolset `computer_toolset_20260801` (17 members: screenshot, zoom, clicks, drag, mouse, scroll | VERIFIED SHIPPING (toolset | ADAPT (Zain desktop-automatio | PD/agents-and-tools/tool-use/computer-us |
| CL-G-003 | G | Browser use tool: client toolset `browser_toolset_20260801` (27 default members incl. navigate, read_page, form_input, t | VERIFIED SHIPPING (GA on C | ADAPT (Zain browser-automatio | PD/agents-and-tools/tool-use/browser-use |
| CL-G-004 | G | Web search server tool: `web_search_20250305` / `_20260209` (dynamic filtering via code execution) / `_20260318` (respon | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | PD/agents-and-tools/tool-use/web-search- |
| CL-G-005 | G | Web fetch server tool: `web_fetch_20250910` ... `_20260318` (dynamic filtering, cache bypass, response_inclusion); fetch | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION ( | PD/agents-and-tools/tool-use/web-fetch-t |
| CL-G-006 | G | Code execution server tool: `code_execution_20250825` / `_20260120` (programmatic tool calling, REPL state) / `_20260521 | VERIFIED SHIPPING (GA) | USE VIA OFFICIAL INTEGRATION ( | PD/agents-and-tools/tool-use/code-execut |
| CL-G-007 | G | Programmatic tool calling: Claude calls your tools from code inside the code execution sandbox (requires code_execution_ | VERIFIED SHIPPING (GA) | ADAPT | PD/agents-and-tools/tool-use/programmati |
| CL-G-008 | G | Tool search tool (`tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119`): discover and load deferred tools | VERIFIED SHIPPING (no beta | ADAPT (deferred tool loading i | PD/agents-and-tools/tool-use/tool-search |
| CL-G-009 | G | Advisor tool (`advisor_20260301`): faster executor model consults a higher-intelligence advisor model mid-generation | BETA-PREVIEW (header `advi | DEFER | PD/agents-and-tools/tool-use/advisor-too |
| CL-G-010 | G | Files API (`/v1/files`): upload once, reference by file_id; 500 MB per file, 1 TB per organization, optional expiry 1 ho | VERIFIED SHIPPING (GA) | USE VIA OFFICIAL INTEGRATION ( | PD/build-with-claude/files |
| CL-G-011 | G | MCP connector: connect remote MCP servers from the Messages API (`mcp_servers` + `mcp_toolset`); Streamable HTTP or SSE  | BETA-PREVIEW (header `mcp- | USE VIA OFFICIAL INTEGRATION ( | PD/agents-and-tools/mcp-connector; CL-E- |
| CL-G-012 | G | MCP tunnels (`/v1/tunnels`): reach MCP servers inside a private network over outbound-only connections (cloudflared + An | RESTRICTED (research previ | DEFER | PD/agents-and-tools/mcp-tunnels/overview |
| CL-G-013 | G | Memory tool (`memory_20250818`): client-side file operations under `/memories` that persist across conversations in stor | VERIFIED SHIPPING (no beta | ADAPT (Zain local-authoritati | PD/agents-and-tools/tool-use/memory-tool |
| CL-G-014 | G | Context management: server-side compaction (on demand, at a token threshold, in the background, keep recent turns verbat | BETA-PREVIEW (compaction h | USE VIA OFFICIAL INTEGRATION ( | PD/build-with-claude/compaction; PD/buil |
| CL-G-015 | G | Prompt caching: automatic caching (top-level cache_control) or explicit breakpoints; 5-minute default TTL refreshed on u | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | PD/build-with-claude/prompt-caching; PRN |
| CL-G-016 | G | Message Batches API: asynchronous batches up to 100,000 requests or 256 MB, most done within 1 hour, expire after 24 hou | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | PD/build-with-claude/batch-processing |
| CL-G-017 | G | Citations: document-grounded citations (plain text, PDF, custom content, search_results blocks); cited_text not billed a | VERIFIED SHIPPING (GA) | USE VIA OFFICIAL INTEGRATION | PD/build-with-claude/citations |
| CL-G-018 | G | Structured outputs: JSON outputs (`output_config.format` with JSON Schema) and strict tool use (`strict: true`) via cons | VERIFIED SHIPPING (GA) | USE VIA OFFICIAL INTEGRATION | PD/build-with-claude/structured-outputs |
| CL-G-019 | G | Agent Skills API: pre-built skills (pptx, xlsx, docx, pdf) and custom skills uploaded via `/v1/skills` (versioned, under | BETA-PREVIEW (header `skil | COPY (SKILL.md format) / USE V | PD/agents-and-tools/agent-skills/overvie |
| CL-G-020 | G | Claude Managed Agents: agent (model, prompt, tools, MCP servers, skills) + environment (Anthropic cloud sandbox or self- | BETA-PREVIEW (header `mana | USE VIA OFFICIAL INTEGRATION ( | PD/managed-agents/overview; PD/managed-a |
| CL-G-021 | G | Managed Agents multiagent orchestration: subagents (delegate and read reports), dynamic workflows (`multiagent_20261001` | BETA-PREVIEW | ADAPT (subagent and workflow o | PD/managed-agents/multiagent-orchestrati |
| CL-G-022 | G | Managed Agents memory stores (carry preferences and context across sessions; header `agent-memory-2026-07-22`) and dream | BETA-PREVIEW (memory store | ADAPT (memory consolidation pa | PD/managed-agents/memory; PD/managed-age |
| CL-G-023 | G | Admin API: members, workspaces, invites, API keys, rate limits, service accounts, workload identity federation, CMEK key | VERIFIED SHIPPING (Plugins | DEFER (gate facts only) | PD/manage-claude/admin-api; PRN 2026-09- |
| CL-G-024 | G | Usage and Cost Admin API: historical token usage and cost reports matching Console Usage/Cost pages | VERIFIED SHIPPING | DEFER (gate facts only) | PD/manage-claude/usage-cost-api |
| CL-G-025 | G | Compliance API reference (`/v1/compliance/*`): Activity Feed for Enterprise and Console; for Enterprise also users/roles | VERIFIED SHIPPING (named s | DEFER (gate facts only) | PD/manage-claude/compliance-api; PRN 202 |
| CL-G-026 | G | Analytics APIs: Claude Code Analytics Admin API (Console orgs; daily per-user sessions, lines, commits, PRs, tool accept | VERIFIED SHIPPING | DEFER (gate facts only) | PD/manage-claude/analytics-api; PD/manag |
| CL-G-027 | G | Model deprecations relevant now: claude-sonnet-4-5-20250929 deprecated 2026-09-30, retires 2026-11-30 (replace with Sonn | NOT AVAILABLE (retired mod | USE VIA OFFICIAL INTEGRATION ( | PD/about-claude/model-deprecations; PRN  |
| CL-G-028 | G | API version `2026-10-21` and new major client SDKs (Python 2.0.0, TypeScript 1.0.0, C# 13.0.0, Go 2.0.0, Java 3.0.0, PHP | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | PRN 2026-10-21 |
| CL-G-029 | G | User profiles (`/v1/user_profiles`): tag which end customer each API request is for so safety enforcement can target one | VERIFIED SHIPPING (webhook | ADAPT (if Zain ever brokers A | PRN 2026-10-20; PRN 2026-10-21; PD/manag |
| CL-G-030 | G | OpenTelemetry export (beta): trace Messages API requests and Managed Agents sessions to your observability platform; SDK | BETA-PREVIEW | ADAPT (OTel as Zain audit tra | PRN 2026-10-14; PD/manage-claude/api-and |
| CL-G-031 | G | Fast mode (`speed: "fast"`): faster inference; GA for Opus 5.5 since 2026-10-15 (no beta header, default fast-mode rate  | VERIFIED SHIPPING (Opus 5. | DEFER | PRN 2026-10-15; PRN 2026-10-22 |
| CL-G-032 | G | Pricing pointers (no figures recorded): plan prices at claude.com/pricing; API model, batch, prompt-cache, server-tool ( | VERIFIED SHIPPING | DEFER (pointer) | claude.com/pricing; PD/about-claude/pric |

## 5. Closure plan (no cost, founder-run, read-only observation)

| Gap | Closure | When |
|---|---|---|
| Hands-on for v1-gating features (03F V1-01…V1-18) | founder-run observation scripts in the founder's own Claude account, screenshots + notes stored as evidence | at each phase entry |
| digest-only rows | none remain (all re-read 2026-10-27) | — |
| API platform references | read when a provider adapter needs them (P2 Claude adapter, P5 connectors) | P2/P5 |
| Changelogs | diff-read at each pinned SDK/CLI upgrade | per upgrade |
