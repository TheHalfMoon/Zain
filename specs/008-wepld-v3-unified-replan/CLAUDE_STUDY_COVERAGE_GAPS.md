# Claude Features — What Has NOT Been Studied Hands-on or in Full

```text
DATE = 2026-10-27
SCOPE = all 339 rows of research/R03_CLAUDE_CENSUS.md + R03B (Design) + R03C (Claude Code)
METHOD = each row's best evidence = deepest read level among the Help Center articles it cites (R03 §7a)
```

## 1. Headline (no rounding up)

1. **Hands-on: ZERO Claude product features were exercised in a UI.** Every census row is `observed_test = NOT_OBSERVED`.
   "VERIFIED SHIPPING" means *documented as available* on 2026-10-27, not *observed working*. The only hands-on
   observation in the whole Claude track is read-only `claude --help` output from the local CLI 2.1.291 (R03C §0.1) and
   read-only descriptions of the Design / Design System artifact types in this environment (R03B [OBS]).
2. **Fully studied (full live text of the cited source read line by line): 18 of 339 rows.**
3. **Read through a summarising fetch tool, with plan/beta/retention/region/admin gates re-checked against live text:
   220 rows.** Non-gate details in these rows are summary-derived.
4. **Gate-digest only (full text fetched, only opening + gate sentences reviewed): 78 rows** — listed in §3.
5. **Evidenced only by non-Help-Center official pages read in pass 1 (product pages, release notes, code docs): 23 rows**
   — listed in §4.
6. **Not studied at all:** platform.claude.com API references (Managed Agents, Admin/Compliance/Analytics APIs, CMEK,
   inference-hook spec), line-by-line changelogs (Claude apps, Claude Code, SDKs), code.claude.com pages outside the areas
   in R03C, mobile-specific interaction details, accessibility behavior, performance characteristics, any
   enterprise admin console behavior.
7. **Claude Design (R03B):** documented features only; no canvas session was run; Figma export, web capture,
   breakpoints, admin edit-lock and true two-way sync remain UNKNOWN.
8. **Claude Code (R03C):** flags/subcommands observed via `--help` only (local 2.1.291 lags npm 2.1.311); no session,
   hook, plugin, MCP, worktree, desktop Code tab, cloud session or GitHub Action was exercised.

## 2. Depth distribution

| depth | rows |
|---|---|
| FULL_TEXT_READ | 18 |
| READ_VIA_SUMMARY_TOOL (gates rechecked on live text) | 220 |
| GATE_DIGEST_ONLY | 78 |
| NON_HELP_CENTER_PAGE_ONLY | 23 |

## 3. Rows whose best evidence is GATE_DIGEST_ONLY (not read in full)

| feature_id | family | feature | status | route | cited articles |
|---|---|---|---|---|---|
| CL-A-005 | A | Automatic model switching when safety classifiers block a request (Fable 5/5.1, Opus 5/5.5, Sonnet 5.5); fallback to a n | VERIFIED SHIPPING | DEFER | SC15363606,SC16049681,SC17161993 |
| CL-A-021 | A | Delete or rename a conversation; deleted chats leave history immediately and backend within 30 days (consumer) | VERIFIED SHIPPING | ADAPT | SC8230524 |
| CL-A-038 | A | Import and export memory to/from other AI providers | VERIFIED SHIPPING | ADAPT | SC12123587,SC8114491 |
| CL-A-048 | A | Interface language: English, French, German, Hindi, Indonesian, Italian, Japanese, Korean, Portuguese (BR), Spanish (Lat | VERIFIED SHIPPING | ADAPT | SC10769299 |
| CL-A-059 | A | Usage limits: rolling five-hour session window plus weekly limits on paid plans; shared pool across web, desktop, mobile | VERIFIED SHIPPING | DEFER | SC11647753,SC8114491 |
| CL-A-060 | A | Usage credits (pay-as-you-go after limits; Pro, Max 5x, Max 20x; Max has separate weekly Fable limit; separate from API  | VERIFIED SHIPPING | DEFER | SC12429409,SC12005970 |
| CL-A-062 | A | Limit reset ("Reset for free") given occasionally to eligible plans; not on mobile or in Claude Code terminal/IDE | VERIFIED SHIPPING | DEFER | SC17007452 |
| CL-A-066 | A | iOS Lock Screen, Control Center, Action button access | VERIFIED SHIPPING | DEFER | SC10302511 |
| CL-A-067 | A | Android home-screen widget (new chat, image capture, dictation) | VERIFIED SHIPPING | DEFER | SC10534883 |
| CL-A-069 | A | claude:// URL scheme: open Desktop to a chat, Cowork, or Code session; mobile links open Code tab/prefill composer | VERIFIED SHIPPING | ADAPT (deep-link hand-off from | SC14729294,SC14898120 |
| CL-A-070 | A | Active sessions list and "log out of all sessions"; web session lasts 28 days, refreshed hourly; E/Console admins can sh | VERIFIED SHIPPING | ADAPT | SC13124001,SC10310342,SC13163631 |
| CL-A-071 | A | Crisis helpline banner surfaced by a separate detection system (ThroughLine, Koko partnership) | VERIFIED SHIPPING | ADAPT (if WePLD is consumer-fa | SC13171706 |
| CL-A-072 | A | Age 18+ requirement and age assurance (verify when under-18 signals detected; pass/fail only to Anthropic) | VERIFIED SHIPPING | ADAPT | SC15171100,SC13117299 |
| CL-A-073 | A | Identity and business verification for certain capabilities (Persona) | BETA-PREVIEW (rolling out  | DEFER | SC14328960 |
| CL-A-074 | A | Permanent account deletion (web and mobile); email address cannot be changed | VERIFIED SHIPPING | ADAPT | SC9028421,SC8452276 |
| CL-A-075 | A | Model knowledge cutoffs published per model (e.g. Haiku 5.5 data to June 2026) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | SC8114494 |
| CL-A-076 | A | Consumer data use: model training is opt-out on Free/Pro/Max; reviewed data de-linked from user ID | VERIFIED SHIPPING | ADAPT (privacy defaults) | SC8325621 |
| CL-A-077 | A | Phone number verification at signup from supported locations | VERIFIED SHIPPING | DEFER | SC8287232 |
| CL-A-078 | A | Support channels by plan (Fin AI support bot for all; human Product Support for Pro/Max, T/E owners, Console admins; no  | VERIFIED SHIPPING | DEFER | SC9015913,SC15263885 |
| CL-B-049 | B | Custom OpenTelemetry collector for Office agents (full audit telemetry to own collector) | VERIFIED SHIPPING | ADAPT | SC14447276 |
| CL-B-055 | B | Maps and image search results on Team/Enterprise (third-party data sharing) | VERIFIED SHIPPING | DEFER | SC13663666 |
| CL-D-001 | D | Claude Code terminal CLI (pointer; native installer, Homebrew, WinGet, apt/dnf/apk; /model, --model, env vars; API-key v | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | SC11940350,SC12304248 |
| CL-D-008 | D | GitHub Code Review (fleet of agents posts inline PR findings) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | SC14233555 |
| CL-D-018 | D | Claude Code usage analytics (productivity and adoption metrics) | VERIFIED SHIPPING | DEFER | SC12157520 |
| CL-D-021 | D | Claude Code screen reader mode (plain sequential output) | VERIFIED SHIPPING | ADAPT | SC15924927 |
| CL-D-022 | D | Dynamic workflows (large migrations/audits in one Claude Code session) | VERIFIED SHIPPING | DEFER (Code agent) | SC12386420 |
| CL-D-023 | D | Claude Code included in Team seats and the single Enterprise seat; Pro/Max via Desktop Code tab recommended | VERIFIED SHIPPING | DEFER | SC11845131,SC11145838,SC9266767 |
| CL-D-024 | D | Console-to-Enterprise migration for Claude Code (CLI history local; switch login) | VERIFIED SHIPPING | DEFER | SC14128775 |
| CL-D-025 | D | Claude Code launch guides (first day, models/limits, troubleshooting, CLAUDE.md, cheatsheet, FAQs, power tips, use cases | VERIFIED SHIPPING | ADAPT (enablement playbook pat | SC14552382,SC14552983,SC14552646,SC14553240,SC14553413,SC14554922,SC14554000,SC14553517,SC14555877,SC14555399 |
| CL-E-024 | E | Restrict verified-domain connectors to the Enterprise (block personal accounts using company domain for Gmail/Slack etc. | VERIFIED SHIPPING | DEFER | SC15402193 |
| CL-E-044 | E | Single sign-on with IdP guides (Okta, Microsoft Entra ID, Google Workspace, OneLogin, Ping) and parent organizations | VERIFIED SHIPPING | ADAPT | SC13132885,SC10276682,SC13917894,SC13917889,SC13917884,SC13917899,SC13917902,SC13443687 |
| CL-E-045 | E | JIT provisioning (T/E/Console) and SCIM (E/Console only, via WorkOS); email-mismatch troubleshooting per IdP | VERIFIED SHIPPING | ADAPT | SC13133195,SC14499648,SC13917829,SC13917840,SC13917817,SC13917861,SC13917875 |
| CL-E-046 | E | Domain claiming and migration of personal accounts on verified domains into Enterprise | VERIFIED SHIPPING | DEFER | SC14625619,SC14625626,SC9267400 |
| CL-E-049 | E | Compliance API partner integrations (DLP, SASE, data security, SIEM/SecOps, identity, eDiscovery, AI-SPM, observability) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | SC15167101 |
| CL-E-051 | E | Usage analytics dashboard and export; Analytics API (E) | VERIFIED SHIPPING | DEFER | SC12883420 |
| CL-E-052 | E | Analytics chat (ask Claude about org usage, default last 30 days) | VERIFIED SHIPPING | ADAPT | SC14729354 |
| CL-E-055 | E | Group spend limits and pooled group budgets | VERIFIED SHIPPING (pooled  | DEFER | SC13799932,SC17005973 |
| CL-E-058 | E | Organization surveys (in-product questions, aggregated results) | BETA-PREVIEW | ADAPT | SC16764057 |
| CL-E-059 | E | Desktop deployment: MSIX (Intune, SCCM, Group Policy, PowerShell), macOS .pkg; non-admin installs lack desktop Cowork | VERIFIED SHIPPING | DEFER | SC12622703,SC12611117,SC12622667 |
| CL-E-060 | E | IP allowlisting | VERIFIED SHIPPING | DEFER | SC13200993 |
| CL-E-061 | E | Tenant Restrictions (proxy headers block personal accounts on corporate networks) | VERIFIED SHIPPING | DEFER | SC13198485 |
| CL-E-065 | E | HIPAA-ready Enterprise; BAA activation by Primary Owner; HIPAA configuration for local Claude Code and Cowork; Covered M | RESTRICTED | DEFER | SC13296973,SC17318731,SC8114513,SC15455031 |
| CL-E-067 | E | Project sharing controls (by role on E), user feedback settings, designated human-support contacts (E) | VERIFIED SHIPPING | DEFER | SC9927533,SC10504844,SC15263885 |
| CL-E-072 | E | Claude for Education (university SSO setup, enforce-SSO effects, Canvas LTI, Primary Owner owns data) | VERIFIED SHIPPING | DEFER | SC11139094,SC11139144,SC11725453,SC11732894 |
| CL-E-074 | E | Programs via custom roles / workspaces (e.g. Cyber Verification Program grants, non-GA model access) | RESTRICTED | DEFER | SC17118092,SC16764810 |
| CL-E-075 | E | Cyber Verification Program (reduced cyber classifiers; tiers covering Opus 5.5, Sonnet 5.5, Mythos 5.1) | RESTRICTED | REJECT | SC14604842,SC17202708 |
| CL-E-076 | E | Covered Models policy (Mythos-class): 30-day minimum retention; ZDR unavailable where Covered Models are accessed | VERIFIED SHIPPING | ADAPT (data-handling disclosur | SC15425695,SC15425996 |
| CL-E-077 | E | Data roles: Team/Enterprise customer is Controller; Primary Owner manages member data; removed users' data handling | VERIFIED SHIPPING | ADAPT | SC9267385,SC9265372,SC12053672,SC9796617 |
| CL-E-078 | E | Invite links and organization discovery for Team/Enterprise | VERIFIED SHIPPING | ADAPT | SC13776697,SC13566435,SC14793921 |
| CL-E-079 | E | Team to Enterprise migration (keep org, data, roles) | VERIFIED SHIPPING | DEFER | SC13779868 |
| CL-E-080 | E | Claude for Intune (managed iOS app, Microsoft sign-in only) | VERIFIED SHIPPING | DEFER | SC17203415,SC9266462 |
| CL-E-081 | E | Claude Console: six roles (User, Claude Code User, Limited Developer, Developer, Billing, Admin), Workspaces, member inv | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | SC10186004,SC9796807,SC13443764,SC13346458,SC13371040,SC9767949,SC8384961,SC10366376 |
| CL-E-082 | E | Console cost and usage reporting; API invoices; prepaid usage credits; ACH/invoicing for some | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | SC9534590,SC16608069,SC8977456,SC9402418 |
| CL-E-083 | E | API rate-limit usage tiers (Start, Build, Scale; Custom) assigned automatically; Team-linked Console orgs at least Build | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | SC8243635,SC8114527,SC10366389 |
| CL-E-084 | E | Console data retention: ZDR orgs can enable 30-day retention per Workspace (needed for Covered Models); Development Part | VERIFIED SHIPPING | DEFER | SC16824617,SC11174108 |
| CL-E-085 | E | Messages API "preserved thinking" anti-distillation change (thinking blocks verified against original context; non-stric | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION ( | SC16761192 |
| CL-E-086 | E | Console Playground (replaced Workbench; no saved history or evals); prompt improver | VERIFIED SHIPPING | DEFER | SC8606378,SC8114533 |
| CL-E-087 | E | Research credit programs: AI for Science, External Researcher Access | RESTRICTED | DEFER | SC11199177,SC9125743 |
| CL-E-088 | E | Safeguards: warnings and appeals (banned consumer users can still export/delete), model safety bug bounty, public jailbr | VERIFIED SHIPPING | ADAPT (appeal/export-on-ban pa | SC8241253,SC12119250,SC11427875,SC9020328,SC12109679 |
| CL-E-089 | E | Policy guidance: Usage Policy for agents, guidelines for organizations serving minors, child safety, Usage Policy except | VERIFIED SHIPPING | ADAPT (compliance requirements | SC12005017,SC9307344,SC15591275,SC9528712,SC9199617 |
| CL-E-090 | E | Site-owner controls: Anthropic crawler robots.txt opt-out; report/remove content from search outputs | VERIFIED SHIPPING | DEFER | SC8896518,SC10684638,SC7996906 |
| CL-E-091 | E | Commercial privacy/legal: certifications list, DPA, BAA, government request policy, EU DSA contact, regulator contact, A | VERIFIED SHIPPING | DEFER | SC10015870,SC7996862,SC9519291,SC11595103,SC11174660,SC12335811,SC15707726,SC12326764 |
| CL-E-092 | E | Anthropic Software Directory Policy and Terms (rules for submitting MCP servers, skills, plugins); Connectors Directory  | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | SC13145358,SC13145338,SC11596036 |
| CL-E-093 | E | Microsoft 365 connector security: Anthropic-hosted, publisher-verified app, delegated permissions, no file caching; need | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | SC12684923,SC12542951 |
| CL-E-094 | E | Seat management: Team Standard/Premium mix; Enterprise single seat (new plans); usage credits for Team and seat-based En | VERIFIED SHIPPING | DEFER | SC12004354,SC13393991,SC12005970,SC13133750 |
| CL-E-095 | E | Claude Enterprise consumption guide (managing usage across chat, Code, Cowork, Design, M365, Chrome, Slack) | VERIFIED SHIPPING | ADAPT (cost-governance playboo | SC14782391 |
| CL-F-006 | F | Claude for iOS (App Store) | VERIFIED SHIPPING | DEFER | SC9266462 |
| CL-F-007 | F | Claude for Android (Google Play) | VERIFIED SHIPPING | DEFER | SC9612887 |
| CL-F-009 | F | In-app purchase of Pro on iOS/Android; app-store billing managed in store | VERIFIED SHIPPING | DEFER | SC9266495,SC9612892,SC8325618 |
| CL-F-016 | F | Minimum age 18 (mobile app-store age signals) and phone verification from supported locations | VERIFIED SHIPPING | ADAPT | SC13117299,SC8287232,SC15171100 |
| CL-F-019 | F | Gift subscriptions: purchase currently unavailable; existing gifts redeemable, expire 365 days after purchase | NOT AVAILABLE (purchase) | DEFER | SC12938627,SC12938695 |
| CL-F-020 | F | Claude in Amazon Bedrock (access via Bedrock console; AWS support; regions per AWS guide) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | SC7996920,SC10280791,SC7996921,SC7996918,SC10280783,SC10280779 |
| CL-F-029 | F | Claude for Teachers (free for verified US K-12 educators; school/district Enterprise org; K-12 terms) | VERIFIED SHIPPING | DEFER | SC16559896,SC15926041 |
| CL-F-030 | F | Billing gates: payments non-refundable except per terms; EEA/UK 14-day refund; cancellations at period end; tax/VAT IDs; | VERIFIED SHIPPING | DEFER | SC12386328,SC8325617,SC9889408,SC9927624,SC9889428,SC14051822,SC12997130 |
| CL-F-031 | F | Team plan requirements: business email, allowed domains, minimum two members; monthly to annual switch | VERIFIED SHIPPING | DEFER | SC9267247,SC12083917,SC9267289,SC12997503,SC16607668,SC9267323 |
| CL-F-032 | F | Enterprise billing model: seat fee for access plus usage at API rates; self-serve or sales-assisted; legacy seat types | VERIFIED SHIPPING | DEFER | SC9797531,SC11526368 |
| CL-F-033 | F | Pro and Max plan definitions (Pro excludes Console API usage; Max 5x/20x, priority access, early features; upgrades pror | VERIFIED SHIPPING | DEFER | SC8325606,SC8325609,SC10185996,SC11049741,SC11049752,SC16607638,SC9876003,SC8987223 |
| CL-F-034 | F | Monthly API credits for Max and Team (pooled on Team, capped at $500; not Free/Pro/Enterprise; claim by linking Console) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | SC17154008,SC8114531 |

## 4. Rows evidenced only by non-Help-Center official pages (product pages, release notes, docs) read in pass 1

| feature_id | family | feature | status | route | evidence |
|---|---|---|---|---|---|
| CL-B-043 | B | Claude for Excel add-in (cell Q&A, assumption updates, model building, pivot tables, conditional formatting) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | claude.com/claude-for-microsoft-365; RN |
| CL-B-044 | B | Claude for PowerPoint add-in (template-aware slides, native charts) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | claude.com/claude-for-microsoft-365 |
| CL-B-045 | B | Claude for Word add-in (tracked-change edits, comment replies, company styles) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | claude.com/claude-for-microsoft-365 |
| CL-B-046 | B | Claude for Outlook add-in (triage, drafts, scheduling; drafts open in compose form) | BETA-PREVIEW | USE VIA OFFICIAL INTEGRATION | claude.com/claude-for-microsoft-365; cla |
| CL-B-047 | B | Shared context across Excel/PowerPoint/Word/Outlook; skills usable in add-ins; dictation in sidebar | VERIFIED SHIPPING | ADAPT | claude.com/claude-for-microsoft-365; RN |
| CL-B-048 | B | Office add-ins via cloud providers / LLM gateways (Bedrock, Vertex AI/Gemini Enterprise Agent Platform, Foundry) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | claude.com/claude-for-microsoft-365; RN |
| CL-D-002 | D | Desktop app Code tab (visual diffs, parallel sessions, scheduled tasks, cloud sessions) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | code.claude.com/docs/en/overview |
| CL-D-004 | D | Claude Code in mobile app | VERIFIED SHIPPING | DEFER | code.claude.com/docs/en/overview |
| CL-D-005 | D | VS Code / Cursor extension (inline diffs, @-mentions, plan review) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | code.claude.com/docs/en/overview |
| CL-D-006 | D | JetBrains plugin (requires CLI) | BETA-PREVIEW | USE VIA OFFICIAL INTEGRATION | code.claude.com/docs/en/overview; claude |
| CL-D-007 | D | GitHub Actions and GitLab CI/CD integration | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | code.claude.com/docs/en/overview |
| CL-D-009 | D | Slack @Claude routing bug reports to PRs | VERIFIED SHIPPING | DEFER | code.claude.com/docs/en/overview; claude |
| CL-D-011 | D | Channels (push Telegram, Discord, iMessage, webhooks into a session) | VERIFIED SHIPPING (status  | DEFER | code.claude.com/docs/en/overview |
| CL-D-012 | D | Cloud scheduled tasks (formerly routines; API/GitHub triggers), desktop scheduled tasks, /loop | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION | code.claude.com/docs/en/overview |
| CL-D-013 | D | Session handoff: `claude --teleport`, `/desktop` | VERIFIED SHIPPING | DEFER | code.claude.com/docs/en/overview |
| CL-D-019 | D | Claude Code changelog and weekly "What's new" digests (pointer) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION ( | code.claude.com/docs/en/changelog |
| CL-E-071 | E | Self-serve Enterprise purchase; single seat type covering Claude, Code, Cowork; Team Standard/Premium seats | VERIFIED SHIPPING | DEFER | RN; claude.com/pricing |
| CL-F-001 | F | claude.ai web app | VERIFIED SHIPPING | REIMPLEMENT FROM OBSERVED BEHA | claude.com/product/overview |
| CL-F-008 | F | Phone pairing via code or claude.ai/mobile | VERIFIED SHIPPING | ADAPT | claude.com/download |
| CL-F-011 | F | Office add-ins distribution (Microsoft Marketplace: Excel, PowerPoint, Word; Outlook beta) | VERIFIED SHIPPING (Outlook | USE VIA OFFICIAL INTEGRATION | claude.com/download |
| CL-F-017 | F | Plans and list prices (Free, Pro, Max 5x/20x, Team Standard/Premium 2-150 users, Enterprise seat + API-rate usage, 20-se | VERIFIED SHIPPING | DEFER | claude.com/pricing (raw text) |
| CL-F-018 | F | Plan gate matrix (pricing comparison table): Free has no Opus, Research, Claude Code, Chrome, M365, Dashboards; Projects | VERIFIED SHIPPING | DEFER | claude.com/pricing (raw text) |
| CL-F-023 | F | Claude Platform / API release notes (pointer) | VERIFIED SHIPPING | USE VIA OFFICIAL INTEGRATION ( | platform.claude.com/docs/en/release-note |


## 5. Closure plan (no cost, founder-run, read-only observation)

| Gap | Closure | When |
|---|---|---|
| Hands-on for v1-gating features (03F V1-01…V1-18) | founder-run observation scripts in the founder's own Claude account, screenshots + notes stored as evidence | at each phase entry |
| 78 digest-only rows | full read when the row's phase opens (most are Backlog/Backlog-E) | per phase |
| API platform references | read when a provider adapter needs them (P2 Claude adapter, P5 connectors) | P2/P5 |
| Changelogs | diff-read at each pinned SDK/CLI upgrade | per upgrade |
