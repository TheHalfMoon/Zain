# 03 — Claude Ecosystem: Complete Feature REA (synthesis)

```text
REGISTER = research/R03_CLAUDE_CENSUS.md — 339 rows, 18 columns, families A–F (canonical feature register, see 03E)
DEPTH_COMPANIONS = research/R03B_CLAUDE_DESIGN.md (Design), research/R03C_CLAUDE_CODE.md (Code CLI/Desktop/SDK)
EVIDENCE = official sources only (claude.com, support.claude.com 364 articles, code.claude.com, release notes); 2026-10-27
OBSERVATION = No UI hands-on tests performed (all rows NOT_OBSERVED). Claude Code CLI 2.1.291 --help OBSERVED (R03C §0.1).
DISAMBIGUATION = "Claude Design" is a creation feature. WePLD replicates capabilities, never Anthropic's UI styling or trade dress.
```

## 1. The current shape of the Claude product (October 2026)

| Surface | State (2026-10-27) | Key fact | Register |
|---|---|---|---|
| Unified conversation (Chat + Cowork) | BETA rollout from 2026-09-16; Enterprise default 2026-11-16 | One thread for quick answers and long agentic tasks; no mode picker; switch is one-way | CL-A-001, CL-C-001..006 |
| Cowork execution | Pro/Max tasks run in the **cloud by default** since 2026-10-06; local files via desktop app; "Only on your computer" option removed for Pro/Max | Desktop vs cloud vs mobile steering differ | CL-C-* |
| Artifacts family | Docs, Slides, Design on all plans; Dashboards beta; Motion beta (Team/Enterprise); "Artifacts that use Claude" billed to viewer; 20 MB persistent storage; view/comment/edit sharing | Legacy chat artifacts can no longer be created | CL-B-001..056 |
| Claude Design | Launched 2026-04-17 (preview); since 2026-09-16 inside conversations/Code/Artifacts on all plans; standalone claude.ai/design closes 2026-12-14 | See `03B` | CL-B-*, R03B |
| Claude Code | CLI 2.1.311 (npm latest), Desktop Code tab (Linux beta), web/cloud sessions, VS Code, JetBrains (beta), GitHub Actions, Slack→"Claude Tag" | See `03C` | CL-D-*, R03C |
| Extensibility | Agent Skills (SKILL.md), plugins + marketplaces, remote MCP connectors (OAuth), MCP Apps, MCPB desktop extensions, developer portal (2026-09-25) | Open formats worth matching | CL-E-* |
| Memory | Editable memory topics, opt-in sensitive topics, per-project memory isolation, per-chat memory off, incognito | | CL-A-032..037 |
| Permissions | Manual / Auto (with safety review) / Skip; per-tool Always/Needs approval/Blocked; admin ceilings; Chrome extension hard-blocks payments/account creation | Strong template | CL-C-011/012/042, CL-E-018/038/039 |
| Enterprise | custom roles, 180-day audit logs, Compliance API, retention ≥30 d, OpenTelemetry from Cowork, SSO/SCIM, inference hooks | | CL-E-* |
| Distribution | Web; Windows/macOS desktop; Linux (beta for Cowork/Desktop); iOS/Android; Chrome extension; Office/Google add-ins | Download page **does** list Android (pass-1 error retracted) | CL-F-* |

Removed/renamed/preview items are listed in `R03 §4` (e.g. Dispatch closed to new users; Haiku 4.5 leaves picker
2026-10-29; Claude in Slack → Claude Tag; Code routines → cloud scheduled tasks).

## 2. Binding constraints discovered

1. **Authentication policy (CL-E-096, R03C §10.5).** Third-party products may not offer claude.ai login or route
   requests through users' Free/Pro/Max credentials; products must use API keys or cloud providers; a user may sign
   into the *unmodified* Claude Code binary with their own subscription. Whether WePLD driving that user-owned CLI via
   the SDK counts as "ordinary use" is **UNKNOWN** → WePLD default: API key / Bedrock / Vertex / Foundry; optional
   "run your own `claude` in a WePLD terminal" (Orca-style CLI agent) with no credential handling by WePLD; seek written
   confirmation before marketing a subscription-backed mode (GO condition G4).
2. **SDK licensing.** `@anthropic-ai/claude-agent-sdk` (TS) is proprietary (Commercial Terms); the Python SDK is MIT
   source but governed by Commercial Terms; `@agentclientprotocol/claude-agent-acp` is Apache-2.0 but built on the SDK.
   Redistribution terms inside a desktop installer: **UNKNOWN** → prefer resolving the SDK from the user's environment
   or an install-time fetch with terms shown (decision in `ADR-007`).
3. **Data retention on Mythos-class models (CL-E-076).** ≥30-day retention, no ZDR — must be shown in WePLD's
   provider picker when such models are selected via API.
4. **Windows sandbox gap (R03C).** Claude's Bash sandbox does not run on native Windows → WePLD's own isolation
   (Phase 8) is needed for Windows-first.

## 3. Route totals (from the 339-row register)

| Route | Rows | Meaning in V3 |
|---|---|---|
| ADAPT | 110 | Build in WePLD using a donor implementation (T3/Orca/OSS) shaped by Claude's observed behavior |
| USE VIA OFFICIAL INTEGRATION | 64 | Call Claude through API/SDK/MCP/connector as one replaceable provider |
| REIMPLEMENT FROM OBSERVED BEHAVIOR | 35 | No source; reproduce the workflow from public docs |
| COPY | 5 | Open formats/specs only (e.g. SKILL.md, MCP, MCPB manifest) — never Anthropic product code |
| DEFER | 121 | Accounted for; not in v1 (enterprise admin breadth, education, mobile-specific, Motion, Duet, etc.) |
| REJECT | 4 | Agentic payments, browser-cookie import, health data, Cyber Verification Program |

Feature coverage ≠ source availability ≠ proven parity: no Anthropic product source is available or used; COPY applies
only to published open formats.

## 4. WePLD priorities derived from Claude (top 10, ranked by user value × feasibility)

1. Unified composer that escalates chat → task with plan/steer/subagents/parallel tasks/resume (Phase 2–4).
2. Permission model: Manual / Auto-with-review / Skip **mapped onto Nawat** (Skip never bypasses hard denials) (Phase 3).
3. Projects with instructions, knowledge files and isolated memory → WePLD Projects + Brain (Phase 4).
4. Scheduled and condition-triggered tasks with missed-run policy (Phase 4).
5. Artifacts: private-by-default documents/slides/dashboards/designs as project files with export (Phase 7/9).
6. Design (canvas, comments, design systems, code handoff) → Design Studio (Phase 7).
7. Skills/plugins/MCP/MCPB compatibility so the Claude ecosystem's open extensions load in WePLD (Phase 5).
8. Code surface: worktrees, diff review with inline comments, PR/CI tracking, preview browser — already in T3 (Phase 2).
9. "Record a skill" (programming by demonstration) — differentiating; DEFER to Phase 9+ after computer-use gating.
10. Enterprise controls (roles, audit, OTel export) — DEFER; seams (principal/scope) designed in Phase 3.

## 5. Coverage statement (honest)

`COVERAGE_COMPLETE_FOR_MANDATORY_SCOPE`: every article in the two mandatory collections (Features and capabilities 36/36;
Cowork 14/14) and the mandatory pages were read in full; all 364 Help Center articles were fetched; 257 non-mandatory
articles were reviewed at gate-digest depth (opening + every plan/beta/retention/region/admin sentence).
`DEPTH_INCOMPLETE` for: platform.claude.com API references, code.claude.com beyond the areas in R03C, changelog
line-by-line, and any hands-on UI observation. 8 discrepancies remain open (R03 §3). These are listed in
`ASSUMPTIONS_AND_UNKNOWNS.md` with closure tasks.

**Study-depth ledger:** exactly which Claude features have not been studied hands-on (all of them) or in full (321 of 339
rows) is enumerated row by row in `CLAUDE_STUDY_COVERAGE_GAPS.md` (2026-10-27).
