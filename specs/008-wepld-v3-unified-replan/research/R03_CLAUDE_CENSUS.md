# R03 - Claude Product Feature Census (official sources only)

- Census date / access date: **2026-10-27**
- Scope: current official Claude product surface (claude.ai web, Claude Desktop, Claude mobile, Cowork, Artifacts family, extensions/add-ins, connectors/skills/plugins, Team/Enterprise admin, distribution). Claude Code and Claude Design are summary/pointer rows only (covered in depth by other agents).
- Revision: **pass 2 (2026-10-27)**, in place over pass 1. Pass 2 fetched the live Help Center navigation tree and all 364 articles as raw page text, read the 16 mandatory-collection articles not read in pass 1 in full, gate-reviewed the remaining 257, re-checked plan/retention/security rows against live text (short quotes marked `Q:` in plan_gate), resolved the four pass-1 UNKNOWNs, retracted one wrong pass-1 discrepancy, and added a coverage proof (section 7). A copy of pass 1 was kept outside the repository.
- Method: pass 1 used WebFetch of official pages (support.claude.com, claude.com product/download/pricing, code.claude.com overview, release notes) plus one WebSearch restricted to official doc domains. Pass 2 used direct HTTP fetches of the same official hosts and local text extraction. Every page body was treated as data, not instructions. Non-quoted wording is paraphrase.
- No hands-on product testing was performed. **observed_test is NOT_OBSERVED for every row.** "VERIFIED SHIPPING" means "an official page states it is available now", not "independently observed".
- No unpublished internals are claimed. Where a page was silent, the unknowns column says so.

## Legend

- **SC** prefix in URLs = `https://support.claude.com/en/articles/` (each Help Center article ID resolves on its own; full slugs are listed in section 2).
- **Plans**: F = Free, P = Pro, M = Max, T = Team, E = Enterprise (seat-based or usage-based), API = Claude Platform.
- **evidence_date**: "pg yyyy-mm-dd" = live "last updated" date from the article page data (pass 2); "acc 2026-10-27" = access date where no page date applies; "RN yyyy-mm-dd" = dated Claude apps release-note entry; "pg yyyy-mm-dd" = date printed on the page.
- **shipped_status**: VERIFIED SHIPPING (official page states GA/available) / BETA-PREVIEW (labelled beta, research preview, or gradual rollout) / RESTRICTED (waitlist, approved orgs, existing users only, or private preview) / NOT AVAILABLE (removed, closing, or explicitly unsupported) / UNKNOWN.
- **WePLD_route** (provisional; assumes WePLD is a third-party product that may integrate Claude only through official APIs/open standards and must not copy proprietary UI or code): COPY = adopt an open, published format/spec verbatim for compatibility (license still to be verified); ADAPT = take the documented pattern and fit it to WePLD; USE VIA OFFICIAL INTEGRATION = call Anthropic's API/SDK/MCP/official app rather than rebuild; REIMPLEMENT FROM OBSERVED BEHAVIOR = build our own version from public documentation (behaviour was documented, not observed, in this census); DEFER = not needed for WePLD v3; REJECT = out of scope or unsafe (for example agentic payments, health data).
- **WePLD thesis note**: `wepld/AGENTS.md` describes WePLD as desktop-first, Windows-first, local-authoritative, air-gap-capable and model-agnostic. Routes of USE VIA OFFICIAL INTEGRATION therefore mean an optional, replaceable adapter, never a required dependency.
- **confidence**: H = stated explicitly on a current official page; M = stated but with conflicting or partial evidence; L = inferred, or title-level evidence only (article not opened).

## 1. Feature register

### Family A - Chat, reasoning, research, memory, personalization, mobile interactions

| feature_id | family | exact_feature | source_product | platform_surface | user_flow (short) | official_evidence_url | evidence_date | observed_test | shipped_status | plan_gate | region_or_OS_gate | data_storage_and_permissions | access_to_source_or_public_API | WePLD_route | user_value | confidence | unknowns |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CL-A-001 | A | Unified conversation: chat and Cowork merged; Claude decides when to run an agentic task; no mode picker | Claude (new experience) | web, desktop, mobile | Type any request; quick questions answered inline, multi-step work escalates to a cloud task | SC16761823 | RN 2026-09-16; acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW (gradual rollout) | P/M rolling out; T beta; E via "Chat and Cowork unified" setting | none stated | Chats, tasks, projects, settings carry over; switch is one-way | No public API for the consumer app; API analogues: Managed Agents, Agent SDK | REIMPLEMENT FROM OBSERVED BEHAVIOR | One entry point, no mode switching | H | Routing heuristic chat vs task; metering differences during rollout |
| CL-A-002 | A | Model selector ("More models"): Haiku 5.5, Sonnet 5.5, Opus 5.5, Fable 5.1, Opus 5, Sonnet 5, Fable 5, Opus 4.8/4.7/4.6, Sonnet 4.6 | Claude | web, desktop, mobile | Click model name next to send; change mid-chat, applies to next reply | SC8664678 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All; Fable paid only; E admins can restrict per role | none | Per-chat setting | API exposes the same model families | USE VIA OFFICIAL INTEGRATION | Pick cost/quality trade-off | H | Exact Free-plan model list |
| CL-A-003 | A | Effort levels Low / Medium / High / Extra high (xhigh) / Max, per-model default | Claude | web, desktop, mobile, API | Hover "Effort" in model menu | SC8664678 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All (E admins can cap per role) | none | Per-chat | API effort parameter | USE VIA OFFICIAL INTEGRATION | Control depth vs usage | H | Free-plan effort access |
| CL-A-004 | A | Thinking / "Extended" toggle; always on for Opus 5.5 and Fable 5.1; expandable reasoning summary; thinking may stop early on safety flag | Claude | web, desktop, mobile, API | Toggle "Thinking" under Effort | SC8664678 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Thinking shown as summary | API thinking params (between_tools for Sonnet 5.5) | USE VIA OFFICIAL INTEGRATION | Transparency on hard problems | H | Summary vs raw fidelity |
| CL-A-005 | A | Automatic model switching when safety classifiers block a request (Fable 5/5.1, Opus 5/5.5, Sonnet 5.5); fallback to a non-Mythos model; user can manage switching | Claude | web, desktop, mobile | Blocked request falls back to another model with notice | SC15363606; SC16049681; SC17161993 | pg 2026-09-28; pg 2026-09-24 | NOT_OBSERVED | VERIFIED SHIPPING | All with those models; Q: "fall back to a non-Mythos model, currently Opus 5" | none | Sonnet 5.5 and Opus 5 noted ZDR-compatible | API returns classifier behaviour separately | DEFER | Continuity under safeguards | H | Exact classifier scope per domain |
| CL-A-006 | A | Efficient mode (restrict to Sonnet/Haiku; default Sonnet 5.5 low effort) | Claude Enterprise | web, desktop, mobile | Owner enables org-wide or per custom role | SC17444462 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | E (unified experience) | none | Admin policy | Analytics/Admin APIs report usage | DEFER | Cost control | M | Availability outside unified experience |
| CL-A-007 | A | Chat file upload: PDF, DOCX, CSV, TXT, HTML, ODT, RTF, EPUB, JSON, XLSX; JPEG/PNG/GIF/WebP; 500 MB/file; 20 files/chat; 8000x8000 px | Claude | web, desktop, mobile | "+" > Add files or photos; drag-drop; paste | SC8241126 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All (XLSX needs code execution on) | none | Stored with chat | API Files API / content blocks | USE VIA OFFICIAL INTEGRATION | Bring own material | H | Mobile-specific limits |
| CL-A-008 | A | PDF handling: visual analysis up to 100 pages; text-only 101-1000; reject above 1000; PDFs over 30 MB processed in sandbox | Claude | web, desktop, mobile | Upload PDF and ask | SC8241126; SC12111783 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | With chat | API PDF support | USE VIA OFFICIAL INTEGRATION | Reports with charts | H | Two different per-file limits (500 MB vs 30 MB) |
| CL-A-009 | A | Image understanding including screenshots and screen-region capture | Claude | web, desktop, mobile, Quick Entry, iOS controls | Attach image or capture region | SC8241126; SC12626668 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | Quick Entry macOS only | With chat | API vision | USE VIA OFFICIAL INTEGRATION | Visual Q&A | H | none |
| CL-A-010 | A | No image generation; Claude builds diagrams/charts/interactive visuals in HTML and SVG (beta) and analyses uploaded images | Claude | web, desktop | Ask for a visual; upload image | SC9002504 | pg 2026-03-16 | NOT_OBSERVED | NOT AVAILABLE (photo/illustration generation); BETA-PREVIEW (HTML/SVG visuals) | All; Q: "Claude doesn't generate photos or illustrations" | Visuals web and desktop only | n/a | None | DEFER | Sets expectations | H | none |
| CL-A-011 | A | Math: Claude processes equations and calculations; advises verifying mission-critical results with specialised software | Claude | web, desktop, mobile | Ask math | SC10366421; SC11095361 | pg 2026-03-16 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | None | ADAPT (add verification nudge) | Correct math | H | Rendering (LaTeX) behaviour not documented |
| CL-A-012 | A | Web search: automatic in new experience; "+" toggle in legacy UI | Claude | web, desktop, mobile | Claude searches when useful | SC10684626; SC16761823 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All; T/E owner enables org-wide | Approx. location from IP for localisation | Results stored with chat | API web search tool | USE VIA OFFICIAL INTEGRATION | Current info | H | Region exclusions not listed |
| CL-A-013 | A | Web fetch of a user-provided URL | Claude | web, desktop, mobile, Cowork | Paste URL | SC10684626; SC13345190 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Server-side; limited to search results and user-shared URLs | API web fetch tool | USE VIA OFFICIAL INTEGRATION | Read specific pages | H | none |
| CL-A-014 | A | Citations with source links and quotes on search answers | Claude | web, desktop, mobile | Automatic | SC10684626 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | API citations | ADAPT | Verifiability | H | none |
| CL-A-015 | A | Image results inside web search (Bing, with source links) | Claude | web, desktop | Automatic | SC10684626 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Third party Bing | None | DEFER | Visual answers | M | Mobile rendering |
| CL-A-016 | A | Research (multi-step deep investigation over web and connectors; runs on Opus 5.5, fallback Opus 4.8) | Claude | web, desktop, mobile (web-only sources on mobile) | "+" > Research, or /deep-research in new experience | SC11088861; SC16761823 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | Research reports deleted with conversation (unified E) | No direct API product | REIMPLEMENT FROM OBSERVED BEHAVIOR | Sourced long-form reports | H | Duration, output format |
| CL-A-017 | A | Research auto-calls connector tools without per-call approval; no local MCP | Claude | web, desktop | Enable connectors then Research | SC11088861; SC11175166 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | Advises disabling write tools first | n/a | ADAPT (keep approval guard) | Breadth | H | none |
| CL-A-018 | A | Guidance: web search for 1-2 tool-call facts; extended thinking for reasoning without web; Research for 5+ tool calls over 1-3 minutes | Claude | docs | Read | SC11095361 | pg 2026-06-02 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | n/a | ADAPT (routing heuristic) | Feature selection | H | none |
| CL-A-019 | A | Chat search ("Search and reference chats"): RAG over past chats, shown as tool call, citations to originals; no cross-project search | Claude | web, desktop, mobile | Ask about earlier chats | SC11817273 | RN 2025-08-11; acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | Own chats only; toggle in Settings > Your Claude | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Continuity | H | Older Cowork tasks not searchable in unified UI |
| CL-A-020 | A | Recents: one list for chats and Cowork tasks | Claude | web, desktop, mobile | Sidebar | SC16761823 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | Unified-experience users | none | Account | None | ADAPT | One history | H | none |
| CL-A-021 | A | Delete or rename a conversation; deleted chats leave history immediately and backend within 30 days (consumer) | Claude | web, desktop, mobile | Conversation menu | SC8230524 | pg 2026-08-10 | NOT_OBSERVED | VERIFIED SHIPPING | F/P/M (consumer article); Q: "deleted from our back-end systems within 30 days" | none | Derived memory not deleted with chat (SC11817273) | None | ADAPT | Hygiene | H | T/E deletion governed by org retention |
| CL-A-022 | A | Branching by editing an earlier message (separate version incl. its artifacts) | Claude | web, desktop | Edit prior message; switch versions | SC17153992; SC16761823 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING (legacy UI) / NOT AVAILABLE (unified UI) | All | none | Versions inside chat | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Explore alternatives | M | Return date for unified UI |
| CL-A-023 | A | Share chat with specific people by email (snapshot, view-only, invite expires 30 days, daily cap) | Claude | web (not mobile) | Share > People with access > Send | SC16762496 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All (T/E own domain only) | none | Excludes attachments (unless in-org) and raw tool data | None | ADAPT | Controlled sharing | H | Cap value |
| CL-A-024 | A | Public links for shared chats (anyone with link, no account, noindex, snapshot); legacy "Share and unshare chats" flow | Claude | web | Share > General access | SC16762437; SC10593882 | pg 2026-06-15 | NOT_OBSERVED | VERIFIED SHIPPING | F/P/M only; Q: "Team and Enterprise plans can only share chats with other members" | none | Attachments excluded; revocable | None | ADAPT | Lightweight publishing | H | none |
| CL-A-025 | A | Org-scoped chat sharing ("Anyone at [org]"); admin disable/revoke; audit log | Claude T/E | web | Share > General access | SC16762496 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | none | In-org only | None | DEFER | Team sharing | H | none |
| CL-A-026 | A | Shared-chats review (Settings > Privacy > Shared chats) | Claude | web | Review/turn off per chat | SC16762496 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | None | ADAPT | Revocation | H | none |
| CL-A-027 | A | Personal data export (emailed link, 24h validity; not from mobile) | Claude | web, desktop | Settings > Privacy > Export data | SC9450526 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | F/P/M; T/E if owner allows | none | Memory included (per SC11817273) | None | ADAPT | Portability | H | File format |
| CL-A-028 | A | Projects: workspace with own chats, knowledge files, instructions; visibility options on T/E | Claude | web, desktop, mobile | Create project; upload knowledge; set instructions | SC9517075; SC9519177 | pg 2026-10-14 | NOT_OBSERVED | VERIFIED SHIPPING | All; Q: "Free users can create a maximum of five projects" | none | Project files 30 MB each | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Context containers | H | Free-plan instruction conflict (SC10185728) |
| CL-A-029 | A | Project RAG mode (auto near context limit, up to 10x capacity) | Claude | web, desktop, mobile | Automatic | SC9517075; SC11473015 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | Index location unstated | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Large knowledge bases | H | Retrieval internals |
| CL-A-030 | A | Project sharing (Can view / Can edit, bulk email, org-wide, "Shared with me") | Claude T/E | web, desktop | Share project | SC9517075; SC9519189; SC9927533 | RN 2025-08-01 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | none | Admin can disable sharing/public projects | None | DEFER | Collaboration | H | none |
| CL-A-031 | A | New projects (beta): one conversation fanning out parallel cloud threads; Library; migration of some P/M projects | Claude Code first | claude.ai/code, desktop Code tab | Sidebar Projects; waitlist | SC9517075 | acc 2026-10-27 | NOT_OBSERVED | RESTRICTED (select P/M, waitlist) | Select P/M | none | Threads run with laptop closed | None | DEFER | Parallel long work | M | Conflicts with Cowork projects article |
| CL-A-032 | A | Memory as individual topics saved during chats (role, people, preferences, technical, projects) | Claude | web, desktop, mobile | Automatic; "remember X" | SC11817273 | RN 2026-07-10; acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | F/P/M default on; T/E owner enables, user opts in | New memory not for HIPAA/public-sector orgs | Encrypted at rest; in exports; owners cannot read members' memory | None (API memory tool not assessed) | REIMPLEMENT FROM OBSERVED BEHAVIOR | Personal continuity | H | Storage region |
| CL-A-033 | A | Memory topics view: open, edit, delete | Claude | web, desktop, mobile | Settings > Your Claude | SC11817273 | RN 2026-08-25 | NOT_OBSERVED | VERIFIED SHIPPING | As CL-A-032 | none | User-editable | None | ADAPT | Control | H | none |
| CL-A-034 | A | "Include sensitive topics in memory" opt-in; never stores gov IDs, criminal history, financial accounts, immigration status | Claude | web, desktop, mobile | Setting or in-chat notice | SC11817273 | RN 2026-08-25 | NOT_OBSERVED | VERIFIED SHIPPING | As CL-A-032 | Older mobile versions skip | Declining deletes sensitive memories | None | ADAPT | Privacy by default | H | none |
| CL-A-035 | A | Project memory isolation; "Use account memory" per-project toggle | Claude | web, desktop, mobile, Cowork | Project page toggle | SC11817273; SC14116274 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All with memory | none | Project memory deleted with project | None | ADAPT | Context separation | H | none |
| CL-A-036 | A | Per-chat memory off ("+" > Memory before first message) | Claude | web, desktop, mobile, voice | Toggle; locked after first message | SC11817273 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All with memory | none | Chat stays in history | None | ADAPT | Selective privacy | H | none |
| CL-A-037 | A | Pause memory / Reset memory (irreversible, incl. project memories) | Claude | web, desktop | Settings | SC11817273 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All with memory | none | Reset deletes all | None | ADAPT | Control | H | none |
| CL-A-038 | A | Import and export memory to/from other AI providers | Claude | web, desktop | Memory import flow | SC12123587; SC8114491 | pg 2026-10-23 | NOT_OBSERVED | VERIFIED SHIPPING | F/P/M/T/E; Q: "available for Free, Pro, Max, Team, and Enterprise plans" | Web and Desktop only | Imported non-work personal details may not be retained | None | ADAPT | Lower switching cost | H | Export file format |
| CL-A-039 | A | Legacy memory (24h synthesized summary + project summaries) for some T/E orgs | Claude T/E | web, desktop | Manage memory modal | SC11817273 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING (legacy) | Some T/E | none | Deleted chats drop from synthesis within 24h | None | DEFER | n/a | H | Old memory may be deleted 14 days after unified switch (SC17444462) |
| CL-A-040 | A | Incognito chats (ghost icon; not in history or memory; not for training; 30-day retention) | Claude | web, desktop, mobile | Ghost icon on new non-project chat | SC12260368 | RN 2025-09-11 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | 30 days (E custom longer); in T/E exports; E Compliance API | None | ADAPT | Private one-offs | H | Unified UI opens legacy chat without files/code |
| CL-A-041 | A | Instructions for Claude (account-wide; absorbed Cowork "Global instructions") | Claude | web, desktop | Settings > Your Claude > Instructions | SC10185728; SC16761823 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Account | API system prompt | ADAPT | Persistent preferences | H | Length limit |
| CL-A-042 | A | Project instructions | Claude | web, desktop, mobile | Project settings | SC10185728; SC9517075 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All (one page says paid only) | none | Project | API system prompt | ADAPT | Per-workspace behaviour | M | Free-plan conflict |
| CL-A-043 | A | Custom styles (profile-level response styles) referenced; Claude Code has "Explanatory"/"Learning" output styles | Claude; Claude Code | web, desktop; CLI | Unknown for chat; /config in Code | SC12260368; SC14554000 | pg 2026-09-30; pg 2026-10-16 | NOT_OBSERVED | VERIFIED SHIPPING (referenced only) | Unknown; Q: "profile information (custom styles, personal preferences, etc.)" | Unknown | Profile data, available in incognito | None | DEFER | Tone control | M | No dedicated current Help Center article; chat management UI undocumented |
| CL-A-044 | A | Context windows: 1M chat for Opus 5.5/5, Sonnet 5.5/5, Haiku 5.5, Fable 5.1; 500K older; 200K for unlisted | Claude | chat, Code, Cowork | Automatic per model | SC8606394 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | Paid plans | none | n/a | API context windows | USE VIA OFFICIAL INTEGRATION | Long documents | H | Free-plan window |
| CL-A-045 | A | Automatic compaction (summarise earlier turns near limit; full history kept) | Claude | web, desktop, mobile | Automatic | SC8606394 | RN 2025-11-24 | NOT_OBSERVED | VERIFIED SHIPPING | Paid plans with code execution on | none | History preserved | API-side equivalent not assessed | ADAPT | Effectively unbounded chats | H | Thresholds |
| CL-A-046 | A | Voice mode (hands-free or push-to-talk, preset voices, connectors in voice, non-English beta) | Claude | iOS, Android, desktop, web | Sound-wave icon | SC11101966 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | All (Free 1 connector in voice) | Fable not in voice; not in Cowork/Code | Transcripts saved to history; E disable via Support | None public | DEFER | Hands-free use | H | Voice list, latency |
| CL-A-047 | A | Mobile dictation (12 languages; non-English beta; audio deleted after transcription) | Claude | iOS, Android | Mic button | SC10065434 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | Not on Linux desktop | Audio not retained | None | ADAPT | Faster input | H | Desktop dictation only via Quick Entry (macOS 14+) |
| CL-A-048 | A | Interface language: English, French, German, Hindi, Indonesian, Italian, Japanese, Korean, Portuguese (BR), Spanish (LatAm, Spain) | Claude | web, desktop | Profile > Language | SC10769299 | pg 2026-10-23 | NOT_OBSERVED | VERIFIED SHIPPING | All | 11 UI languages | n/a | None | ADAPT | Localisation | H | Mobile UI language list |
| CL-A-049 | A | Appearance: Light/Dark/System; chat font incl. Dyslexic Friendly | Claude | web, desktop | Settings > Appearance | SC8887527 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | None | ADAPT | Accessibility | H | Mobile parity |
| CL-A-050 | A | Accessibility: artifacts by keyboard/screen reader; Docs shortcuts (Cmd/Ctrl+/); Slides F6 navigation; VoiceOver caveat on Chrome 150-152 | Claude | web, desktop | Keyboard | SC17457950; SC17458093; SC17153992; SC16923645 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | Chrome 153+ advised | n/a | None | ADAPT | Inclusive UX | H | No WCAG conformance statement found |
| CL-A-051 | A | Interactive inputs (clickable multiple choice, multi-select, ranking) | Claude | web, desktop, mobile | Options shown above input | SC13641943 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | No third parties | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Faster clarification | H | none |
| CL-A-052 | A | Weather widget (Google Maps data) | Claude | web, desktop (text on mobile) | Ask weather | SC13641943 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All (needs web search) | none | Google Maps | None | DEFER | Convenience | H | none |
| CL-A-053 | A | Recipe cards with servings/units and "Get cooking" mode | Claude | web, desktop (text on mobile) | Ask for recipe | SC13641943 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All (needs web search) | none | Bing images | None | DEFER | Consumer delight | H | none |
| CL-A-054 | A | Sports scores/standings/schedules (text only) | Claude | all | Ask | SC13641943 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | None | DEFER | Consumer info | H | none |
| CL-A-055 | A | Edit drafts in place (highlight > "Edit with Claude") | Claude | web, desktop, Cowork | Highlight, request change | SC17153992; SC13345190 | RN 2026-06-12 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Precise revisions | H | none |
| CL-A-056 | A | Push notifications when a task finishes or needs input | Claude | iOS, Android, desktop | Automatic | SC15520349; SC13947068 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | Cowork users | none | n/a | None | ADAPT | Async work | H | Notification settings |
| CL-A-057 | A | Monthly recap (topics, activity stats, AI-fluency observations) | Claude | web, desktop | Settings > Wellbeing > Reflect | SC15672559 | RN 2026-07-09 | NOT_OBSERVED | BETA-PREVIEW | F/P/M (memory required) | All regions | Excludes incognito, health, Cowork, Code | None | DEFER | Reflection | H | none |
| CL-A-058 | A | Break reminders and quiet hours (soft friction) | Claude | set on web/desktop; applies to mobile | Settings > Wellbeing | SC15672868 | RN 2026-07-09 | NOT_OBSERVED | BETA-PREVIEW | F/P/M | none | n/a | None | DEFER | Wellbeing | H | none |
| CL-A-059 | A | Usage limits: rolling five-hour session window plus weekly limits on paid plans; shared pool across web, desktop, mobile, Code | Claude | all | Settings > Usage | claude.com/pricing (raw text); SC11647753; SC8114491 | acc 2026-10-27; pg 2026-10-13 | NOT_OBSERVED | VERIFIED SHIPPING | All; Q: "reset on a rolling five-hour session window, and paid plans add weekly limits" | none | n/a | None | DEFER | Predictability | H | Exact quotas unpublished |
| CL-A-060 | A | Usage credits (pay-as-you-go after limits; Pro, Max 5x, Max 20x; Max has separate weekly Fable limit; separate from API credits) | Claude | all | Enable under Settings > Usage | SC12429409; SC12005970 | pg 2026-10-08; pg 2026-09-04 | NOT_OBSERVED | VERIFIED SHIPPING | P/M; T and seat-based E (not usage-based E) | none | n/a | None | DEFER | Burst capacity | H | none |
| CL-A-061 | A | Usage bundles ($50/$250/$1000 at 10/20/30% off) | Claude | all | Settings > Usage > Buy usage | SC14246112 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T | none | One pool across Claude, Code, Cowork, third-party apps | None | DEFER | Cost | H | none |
| CL-A-062 | A | Limit reset ("Reset for free") given occasionally to eligible plans; not on mobile or in Claude Code terminal/IDE | Claude | web, desktop | Settings > Usage > Resets | SC17007452 | pg 2026-09-22 | NOT_OBSERVED | VERIFIED SHIPPING | Eligible plans (unspecified) | Not mobile | n/a | None | DEFER | Relief from limits | H | Eligibility rules |
| CL-A-063 | A | iOS integrations: draft Messages/Mail (incl. WhatsApp, Signal, Gmail, Outlook), Calendar, Reminders, Location/Maps | Claude iOS | iOS | Ask; approve OS permission | SC11869619 | RN 2025-09-03 | NOT_OBSERVED | VERIFIED SHIPPING | All (location not T/E) | iOS | OS permissions Allow once/Always/Don't | None | DEFER | Mobile productivity | H | none |
| CL-A-064 | A | Health data (Apple Health / Android Health Connect read-only, native charts) | Claude mobile | iOS, Android 14+ | Per-category permission | SC11869619; SC11869629 | RN 2026-01-12 | NOT_OBSERVED | BETA-PREVIEW | P/M | US only | Not saved to memory unless sensitive-topics on | None | REJECT | Health insight | H | none |
| CL-A-065 | A | iOS App Intents (Ask Claude via Siri/Spotlight/Share), Shortcuts action, widget | Claude iOS | iOS 18+ | Siri "Ask Claude"; Shortcuts | SC10263469 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | iOS 18+ | Counts toward usage | None | DEFER | OS-level access | H | none |
| CL-A-066 | A | iOS Lock Screen, Control Center, Action button access | Claude iOS | iOS 18+ | Add control | SC10302511 | pg 2026-07-09 | NOT_OBSERVED | VERIFIED SHIPPING | All | iOS 18+ | n/a | None | DEFER | Quick capture | H | none |
| CL-A-067 | A | Android home-screen widget (new chat, image capture, dictation) | Claude Android | Android 8.0+ | Add widget | SC10534883 | pg 2026-07-09 | NOT_OBSERVED | VERIFIED SHIPPING | All | Android 8.0 Oreo+ | n/a | None | DEFER | Quick access | H | none |
| CL-A-068 | A | Android integrations: draft messages/email, calendar read/create, Google Maps, alarms and timers | Claude Android | Android | Ask | SC11869629 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All (location not T/E) | Android | OS permissions | None | DEFER | Mobile productivity | H | No reminders/contacts on Android |
| CL-A-069 | A | claude:// URL scheme: open Desktop to a chat, Cowork, or Code session; mobile links open Code tab/prefill composer | Claude | macOS, Windows, Linux desktop; iOS; Android | Click claude:// link | SC14729294; SC14898120 | pg 2026-06-30; pg 2026-05-06 | NOT_OBSERVED | VERIFIED SHIPPING | All (mobile links need Claude Code access) | none | Only first folder value applied | Documented URL parameters | ADAPT (deep-link hand-off from WePLD) | Hand-off from other tools | H | none |
| CL-A-070 | A | Active sessions list and "log out of all sessions"; web session lasts 28 days, refreshed hourly; E/Console admins can shorten session length | Claude | web, desktop, mobile | Settings > Account | SC13124001; SC10310342; SC13163631 | pg 2026-10-23; 2026-10-24; 2026-10-15 | NOT_OBSERVED | VERIFIED SHIPPING | All; shortened sessions E admins and Console admins | none | E options 1/7/14/28 days | None | ADAPT | Account security | H | none |
| CL-A-071 | A | Crisis helpline banner surfaced by a separate detection system (ThroughLine, Koko partnership) | Claude | all | Automatic; dismissible | SC13171706 | pg 2026-10-24 | NOT_OBSERVED | VERIFIED SHIPPING | All | Helplines vary by country | n/a | None | ADAPT (if WePLD is consumer-facing) | User safety | H | Detection criteria |
| CL-A-072 | A | Age 18+ requirement and age assurance (verify when under-18 signals detected; pass/fail only to Anthropic) | Claude | all; mobile app-store age signals in some US states | Confirm age at signup; verify if flagged | SC15171100; SC13117299 | pg 2026-05-18; pg 2026-03-16 | NOT_OBSERVED | VERIFIED SHIPPING | All; Q: "only available to people over 18 years" | Some US states app-store age laws | No ID stored by Anthropic | None | ADAPT | Compliance | H | none |
| CL-A-073 | A | Identity and business verification for certain capabilities (Persona) | Claude | all | Verification prompt | SC14328960 | pg 2026-08-11 | NOT_OBSERVED | BETA-PREVIEW (rolling out for a few use cases) | Unspecified | Unspecified | ID and selfie held by Persona, not Anthropic | None | DEFER | Abuse prevention | H | Which capabilities trigger it |
| CL-A-074 | A | Permanent account deletion (web and mobile); email address cannot be changed | Claude | web, iOS, Android | Settings | SC9028421; SC8452276 | pg 2026-08-19; pg 2026-03-16 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Deletion permanent; some cases need Support | None | ADAPT | Data control | H | none |
| CL-A-075 | A | Model knowledge cutoffs published per model (e.g. Haiku 5.5 data to June 2026) | Claude | docs | Read | SC8114494 | pg 2026-10-07 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | Platform model docs | USE VIA OFFICIAL INTEGRATION | Expectation setting | H | none |
| CL-A-076 | A | Consumer data use: model training is opt-out on Free/Pro/Max; reviewed data de-linked from user ID | Claude | all | Settings > Privacy | claude.com/pricing (raw text); SC8325621 | acc 2026-10-27; pg 2026-05-22 | NOT_OBSERVED | VERIFIED SHIPPING | F/P/M; Q: "Model training Opt-out" (pricing table); T/E not trained by default | none | De-linked before review | None | ADAPT (privacy defaults) | Trust | H | none |
| CL-A-077 | A | Phone number verification at signup from supported locations | Claude | all | Enter SMS code | SC8287232 | pg 2026-08-17 | NOT_OBSERVED | VERIFIED SHIPPING | All | Supported locations only | Phone used only for verification | None | DEFER | Abuse prevention | H | none |
| CL-A-078 | A | Support channels by plan (Fin AI support bot for all; human Product Support for Pro/Max, T/E owners, Console admins; no phone or live chat) | Claude | web, desktop | Help > Get help | SC9015913; SC15263885 | pg 2026-10-08 | NOT_OBSERVED | VERIFIED SHIPPING | Human support: P/M, T/E owners, Console admins | none | n/a | None | DEFER | Support model benchmark | H | none |

### Family B - Creation: Artifacts, Docs, Slides, Design, Dashboards, Motion, visuals, files, Office and Google add-ins

| feature_id | family | exact_feature | source_product | platform_surface | user_flow (short) | official_evidence_url | evidence_date | observed_test | shipped_status | plan_gate | region_or_OS_gate | data_storage_and_permissions | access_to_source_or_public_API | WePLD_route | user_value | confidence | unknowns |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CL-B-001 | B | Artifacts (documents, code, single-page sites, images, diagrams, dashboards, small tools) in a side window; saved in Artifacts tab | Claude | web, desktop, mobile, Code, Cowork | Ask, or "Output" > template, or Artifacts tab template | SC17153992 | RN 2026-09-16; acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Saved to account; start private | None for consumer artifacts | REIMPLEMENT FROM OBSERVED BEHAVIOR | Durable, editable outputs | H | Size limits |
| CL-B-002 | B | "Output" menu in message box and template gallery (Docs, Slides, Design, Dashboards, Motion) | Claude | web, desktop | Output > pick template | SC17153992; SC17454700; SC17454997 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All (template gates vary) | none | n/a | None | ADAPT | Discoverability | H | none |
| CL-B-003 | B | Artifact creation heuristic (>15 lines, self-contained, reusable) and prerequisite "Code execution and file creation" on | Claude | web, desktop | Automatic | SC17153992 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Settings > Capabilities | None | ADAPT | Predictable output form | H | none |
| CL-B-004 | B | Artifact versions via editing an earlier message | Claude | web, desktop | Edit message | SC17153992 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING (legacy UI) | All | none | n/a | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Safe iteration | M | Branching unavailable in unified UI (SC16761823) |
| CL-B-005 | B | Direct editing in template artifacts (type in Docs, edit Slides, move Design elements) with live updates | Claude | web, desktop, mobile (edit) | Click and edit | SC17153992 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Autosave | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | WYSIWYG control | H | none |
| CL-B-006 | B | Targeted edits: highlight > "Edit with Claude"; queued multi-file Markdown edits applied in one pass | Claude | web, desktop | Highlight; queue edits | SC17153992 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Precise revisions to skills/plugins | H | none |
| CL-B-007 | B | "Try fixing with Claude" on artifact errors | Claude | web, desktop | Click near error | SC17153992 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Sends error details to Claude | None | ADAPT | Self-repair | H | none |
| CL-B-008 | B | Artifact sharing: Only you / specific people (email, beta) / org / groups (E) / anyone with link | Claude | web, desktop (not changeable on mobile) | Share > Who has access | SC9547008 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING (email invites BETA) | All; link on T/E only if owner enables External sharing | none | Start private; viewers use their own connectors | None | ADAPT | Distribution | H | Exact plan matrix (table hard to read) |
| CL-B-009 | B | Access levels Can view / Commenter / Can edit and comments (incl. ask Claude in comments) | Claude | web, desktop | Share > access level | SC9547008 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Outside invitees: no mentions, no Claude, no connectors | None | ADAPT | Review workflows | H | none |
| CL-B-010 | B | Outside-org email invitations (cap 50 per artifact, 30-day pending expiry, report invitation) | Claude | web, desktop | Invite by email | SC9547008 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | P/M/T/E (T on, E off by default) | none | Requires Claude account with that email | None | DEFER | External collaboration | H | Not for Docs |
| CL-B-011 | B | Publish legacy chat artifacts to public link (no account to view) | Claude | web, desktop | Publish | SC9547008 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING (legacy) | F/P/M | none | Public | None | ADAPT | Shareable mini-apps | H | none |
| CL-B-012 | B | Embed published artifacts with "Get embed code" and allowed-domain list | Claude | web, desktop | Publish > Get embed code | SC9547008 | RN 2025-08-21 | NOT_OBSERVED | VERIFIED SHIPPING (legacy) | F/P/M | none | Domain allowlist | Embed code only | USE VIA OFFICIAL INTEGRATION | Embed in sites | H | New-artifact embed support |
| CL-B-013 | B | Unpublish (permanent; deletes personal and shared storage; cannot republish same artifact) | Claude | web, desktop | Unpublish | SC9547008 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | F/P/M | none | Storage deleted | None | ADAPT | Revocation | H | none |
| CL-B-014 | B | Remix published artifacts (copy to new chat) | Claude | web, desktop | Copy and describe changes | SC17153992 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING (legacy only) | F/P/M | none | Separate copy | None | DEFER | Reuse | H | none |
| CL-B-015 | B | AI-powered artifacts ("Artifacts that use Claude"): viewers sign in and use their own plan usage; no API key | Claude | web, desktop | Build app that calls Claude; first-use permission prompt | SC17153992 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All (T/E members no cost to owner) | none | Usage billed to viewer | No public API for the artifact runtime | REIMPLEMENT FROM OBSERVED BEHAVIOR | Shareable AI mini-apps without keys | H | Runtime API surface |
| CL-B-016 | B | Artifacts with connectors (read/write connected apps; per-tool off persists; no per-action-approval tools) | Claude | web, desktop | First use prompts approval | SC17153992 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | Each viewer connects own apps; T/E owners can disable | MCP connectors | ADAPT | Live data apps | H | none |
| CL-B-017 | B | Artifact persistent storage: personal and shared, 20 MB text-only per artifact | Claude | web, desktop | Automatic; shared-storage confirmation | SC17153992 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | Shared storage visible to all users; unpublish deletes | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Stateful mini-apps | H | Retention outside unpublish |
| CL-B-018 | B | Legacy chat artifacts (created before 2026-09-16): still work, cannot create new | Claude | web, desktop | n/a | SC17153992 | acc 2026-10-27 | NOT_OBSERVED | NOT AVAILABLE (for new creation) | All | none | n/a | None | DEFER | Back-compat | H | Sunset date |
| CL-B-019 | B | Cowork live artifacts (created before 2026-08-19): open/share, not editable; republish to edit | Cowork | desktop only | Share > republish | SC14729249 | acc 2026-10-27 | NOT_OBSERVED | NOT AVAILABLE (for new creation; still used by CMEK/ZDR/HIPAA orgs) | Cowork users | none | Org-only links; viewer's access to data | None | DEFER | Back-compat | H | Data refresh behaviour |
| CL-B-020 | B | Claude Code session output published as live page at private URL; docs/design from Code (/design) | Claude Code | desktop side panel, terminal link | Ask in session | SC17153992; SC16923645 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | Plans with Claude Code | none | Private URL | Claude Code docs | USE VIA OFFICIAL INTEGRATION | Shareable dev reports | M | Code-side details (other agent) |
| CL-B-021 | B | Claude Docs: rich-text living docs, clarifying questions, explanatory comments, /docs | Claude Docs | web, desktop, mobile (edit), Code | "/docs" or Output > Docs | SC16923645 | RN 2026-09-16 | NOT_OBSERVED | VERIFIED SHIPPING (E default-on 2026-10-15) | All | none | Saved to account (Artifacts tab) | None documented in sources read | REIMPLEMENT FROM OBSERVED BEHAVIOR | Collaborative writing with AI | H | Doc size limits |
| CL-B-022 | B | Docs real-time co-editing with attribution per person or Claude; Claude acts with requester's permissions | Claude Docs | web, desktop | Share with editors | SC16923645 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Every change attributed | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Multiplayer docs | H | Conflict resolution model |
| CL-B-023 | B | Docs comments with @Claude edit requests; "Send to Claude" checkbox | Claude Docs | web, desktop | Select text > comment | SC16923645 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Review loop with AI | H | none |
| CL-B-024 | B | Docs tabs (multiple tabs per doc) and version history | Claude Docs | web, desktop | Tab bar; history panel | SC16923645 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | None | ADAPT | Structure | M | Version-history details |
| CL-B-025 | B | Docs charts/diagrams/timelines from connected apps (no auto-refresh; ask Claude to refresh) | Claude Docs | web, desktop | Ask for chart | SC16923645 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Pulls from connectors | None | ADAPT | Data-backed docs | H | none |
| CL-B-026 | B | Docs export: Word, PDF, Markdown, Google Docs; convert to Slides | Claude Docs | web, desktop | Export menu | SC16923645 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | None | ADAPT | Interop | H | none |
| CL-B-027 | B | Docs sharing: viewer/editor only (no comment-only); F/P/M anyone-with-link; T/E people/groups/org, no external; no email invitations; delete permanent | Claude Docs | web, desktop | Share | SC16923645 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Doc activity not yet in Compliance API | None | ADAPT | Controlled sharing | H | none |
| CL-B-028 | B | Claude Slides: build from notes/chat; present mode; export PowerPoint, PDF, editable Google Slides; keyboard navigation | Claude Slides | web, desktop, mobile (edit) | Output > Slides | SC17153992; SC17457950; SC14604406 | RN 2026-09-16; pg 2026-10-08 | NOT_OBSERVED | VERIFIED SHIPPING (E default-on 2026-10-15) | All; Q: "Presentations now have their own tool, Claude Slides" | none | Saved to account | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Decks fast | H | No dedicated Slides getting-started article in Help Center |
| CL-B-029 | B | Claude Design (pointer): designs, prototypes, one-pagers; standalone claude.ai/design read-only after 2026-12-14; project/design-system migration into Artifacts | Claude Design | web, desktop, mobile, Code (/design) | Output > Design; Move to Claude | SC14604416; SC17440474; SC14604406 | pg 2026-10-23 | NOT_OBSERVED | VERIFIED SHIPPING (standalone closing) | All; Q: "will close on December 14, 2026" | ZDR and HIPAA orgs cannot move projects | Chats/comments stay in standalone, later deleted | None | DEFER (see Design agent) | Visual work | H | See R03B |
| CL-B-030 | B | Claude Dashboards: plain-language question to dashboard; each chart runs own SQL with visible query and last-refresh time | Claude Dashboards | web, desktop (others unstated) | Output > Dashboards | SC17454700 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | P/M/T/E (E off by default) | none | Queries against user's warehouses; starts private | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Self-serve analytics | H | Refresh schedule, row limits |
| CL-B-031 | B | Dashboards data sources: Redshift, BigQuery, ClickHouse, Databricks, Snowflake, plus connected apps (e.g. Salesforce) | Claude Dashboards | web, desktop | Connect source first | SC17454700 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | As CL-B-030 | none | Via connectors | MCP connectors | USE VIA OFFICIAL INTEGRATION | Warehouse access | H | none |
| CL-B-032 | B | Claude Motion: code-built animations (explainers, animated charts, walkthroughs); MP4 export only | Claude Motion | web, desktop (unstated) | Output > Motion | SC17454997 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | T/E only (E off by default) | none | Saved as artifact; private by default | None | DEFER | Video explainers | H | Platforms; length limits |
| CL-B-033 | B | Custom visuals inline (HTML diagrams, flowcharts, interactive charts; sliders; full screen) | Claude | web, desktop (not iOS/Android) | Claude decides or "draw this" | SC13979539; SC13641943 | pg 2026-04-22; RN 2026-03-12 | NOT_OBSERVED | BETA-PREVIEW | All | none | Ephemeral unless saved | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Explain visually | H | none |
| CL-B-034 | B | Save custom visual: copy as image, download .svg/.html, save as artifact | Claude | web, desktop | Visual menu | SC13979539 | pg 2026-04-22 | NOT_OBSERVED | BETA-PREVIEW | All | none | n/a | None | ADAPT | Keep visuals | H | none |
| CL-B-035 | B | Explorable chart from uploaded CSV | Claude | web, desktop | Upload CSV | SC13979539; SC13641943 | pg 2026-04-22 | NOT_OBSERVED | BETA-PREVIEW | All | none | n/a | None | ADAPT | Quick data exploration | H | none |
| CL-B-036 | B | Click inside visual sends follow-up prompt (chat only, not Cowork) | Claude | web, desktop | Click element | SC13979539 | pg 2026-04-22 | NOT_OBSERVED | BETA-PREVIEW | All | none | n/a | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Interactive drill-down | H | none |
| CL-B-037 | B | Interactive apps rendered inline on mobile | Claude mobile | iOS, Android | Use interactive connector | RN (SC12138966) | RN 2026-03-25 | NOT_OBSERVED | VERIFIED SHIPPING | All | iOS, Android | n/a | MCP Apps | USE VIA OFFICIAL INTEGRATION | Mobile parity | M | Custom visuals still not on mobile per SC13979539 |
| CL-B-038 | B | File creation: .xlsx (working formulas), .pptx, .docx, .pdf; also Python, PNG charts, HTML, React, Markdown, Mermaid, SVG | Claude | web, desktop, mobile | Ask; download or save to Google Drive | SC12111783 | RN 2025-09-09, 2025-09-29 | NOT_OBSERVED | VERIFIED SHIPPING | All (default on; new E orgs vary) | none | 30 MB per file up/down | API code execution tool + Agent Skills | USE VIA OFFICIAL INTEGRATION | Finished deliverables | H | none |
| CL-B-039 | B | Code execution sandbox (Python/JS, isolated container per user, capped resources) | Claude | web, desktop, mobile | Automatic | SC12111783 | RN 2025-08-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Never shared between users | API code execution tool | USE VIA OFFICIAL INTEGRATION | Compute in chat | H | Exact caps |
| CL-B-040 | B | Network egress levels: Off / Package managers only / + specific domains / All domains; approved package domains list | Claude | web, desktop | Settings > Capabilities (org: Organization settings) | SC12111783 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All (domain allowlist E) | none | MCP calls bypass egress setting | n/a | ADAPT | Safe package installs | H | none |
| CL-B-041 | B | Format conversion (e.g. Word to PowerPoint, Excel to Word report) | Claude | web, desktop, mobile | Ask | SC12111783 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | Agent Skills (docx/xlsx/pptx/pdf) | USE VIA OFFICIAL INTEGRATION | Interop | H | none |
| CL-B-042 | B | Prompt-injection classifier stops sandbox execution; public sharing disabled for consumer chats with file artifacts | Claude | web, desktop | Automatic | SC12111783 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | F/P/M (sharing rule) | none | n/a | None | ADAPT | Safety | H | Classifier details |
| CL-B-043 | B | Claude for Excel add-in (cell Q&A, assumption updates, model building, pivot tables, conditional formatting) | Claude for Microsoft 365 | Excel | Sidebar | claude.com/claude-for-microsoft-365; RN | RN 2025-11-24, 2026-02-05 | NOT_OBSERVED | VERIFIED SHIPPING | All paid | none | Edits reviewable before save | Microsoft Marketplace add-in | USE VIA OFFICIAL INTEGRATION | Spreadsheet copilot | H | Admin deployment detail |
| CL-B-044 | B | Claude for PowerPoint add-in (template-aware slides, native charts) | Claude for Microsoft 365 | PowerPoint | Sidebar | claude.com/claude-for-microsoft-365 | RN 2026-02-05 | NOT_OBSERVED | VERIFIED SHIPPING | All paid | none | n/a | Microsoft Marketplace | USE VIA OFFICIAL INTEGRATION | Deck copilot | H | none |
| CL-B-045 | B | Claude for Word add-in (tracked-change edits, comment replies, company styles) | Claude for Microsoft 365 | Word | Sidebar | claude.com/claude-for-microsoft-365 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All paid | none | n/a | Microsoft Marketplace | USE VIA OFFICIAL INTEGRATION | Doc copilot | H | No Help Center article located |
| CL-B-046 | B | Claude for Outlook add-in (triage, drafts, scheduling; drafts open in compose form) | Claude for Microsoft 365 | Outlook | Sidebar | claude.com/claude-for-microsoft-365; claude.com/download | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | All paid | none | Nothing sent without approval | Microsoft Marketplace | USE VIA OFFICIAL INTEGRATION | Email copilot | H | none |
| CL-B-047 | B | Shared context across Excel/PowerPoint/Word/Outlook; skills usable in add-ins; dictation in sidebar | Claude for Microsoft 365 | Office apps | Drop file in one sidebar, reference in another | claude.com/claude-for-microsoft-365; RN | RN 2026-03-11 | NOT_OBSERVED | VERIFIED SHIPPING | All paid | none | n/a | n/a | ADAPT | Cross-app continuity | H | none |
| CL-B-048 | B | Office add-ins via cloud providers / LLM gateways (Bedrock, Vertex AI/Gemini Enterprise Agent Platform, Foundry) | Claude for Microsoft 365 | Office apps | Sign in via cloud provider | claude.com/claude-for-microsoft-365; RN | RN 2026-03-11 | NOT_OBSERVED | VERIFIED SHIPPING | Cloud-provider customers | none | Provider terms | Cloud provider APIs | USE VIA OFFICIAL INTEGRATION | Enterprise procurement path | M | Product page omits "LLM gateway" wording that RN uses |
| CL-B-049 | B | Custom OpenTelemetry collector for Office agents (full audit telemetry to own collector) | Claude for Microsoft 365 | Office apps | Admin config | SC14447276 | pg 2026-08-05 | NOT_OBSERVED | VERIFIED SHIPPING | E; direct-provider deployments (Bedrock, Vertex, gateway) | none | office_agent.* counters route to Anthropic only | OTLP | ADAPT | Observability | H | none |
| CL-B-050 | B | Claude for Google Workspace add-on: sidebar in Docs/Sheets/Slides; edits open file in place | Claude for Google Workspace | Google Docs, Sheets, Slides (Chrome/Edge/Safari) | Extensions > Claude > Open Claude | SC16951679 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | P/M/T/E | Not Firefox | Sees only open file; history stored locally in browser per file; deleted within 30 days | Google Workspace Marketplace | USE VIA OFFICIAL INTEGRATION | Edit in place | H | none |
| CL-B-051 | B | Google add-on edit modes "Ask before edits" (default) / "Accept all edits"; cannot share files or load arbitrary pages; 6-minute task timeout | Claude for Google Workspace | Docs/Sheets/Slides | Mode toggle | SC16951679 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | P/M/T/E | none | No ZDR, HIPAA, Bedrock/Vertex/Foundry | n/a | ADAPT | Safe editing | H | none |
| CL-B-052 | B | Google Docs/Sheets/Slides connectors with live editing pane beside chat | Claude | web (Chrome), desktop (built-in browser) | Ask to edit Google file | SC10166901 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All (T/E owner enables) | none | Mirrors Google permissions; no training on connector data | Google APIs via connector | USE VIA OFFICIAL INTEGRATION | Edit Google files from Claude | H | Cannot add charts to Slides |
| CL-B-053 | B | Artifacts admin settings (turn on artifacts, choose templates incl. Docs/Slides/Design/Dashboards/Motion, control access, external sharing) | Claude T/E | admin | Organization settings > Artifacts | SC16994751; SC9547008 | pg 2026-10-23 | NOT_OBSERVED | VERIFIED SHIPPING | T/E; Owners, Primary Owners, or custom roles with admin permission | none | Offboarding and Compliance API covered | Compliance API | DEFER | Governance | H | none |
| CL-B-054 | B | Artifacts on mobile: create, view in Artifacts tab, edit; sharing settings only on web/desktop | Claude mobile | iOS, Android | Artifacts tab | SC17153992 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | None | ADAPT | On-the-go review | H | none |
| CL-B-055 | B | Maps and image search results on Team/Enterprise (third-party data sharing) | Claude T/E | web, desktop | Admin toggle in Capabilities | SC13663666 | pg 2026-03-16 | NOT_OBSERVED | VERIFIED SHIPPING | T on by default; E off by default | none | Data shared with Google/Bing | None | DEFER | Rich answers | H | none |
| CL-B-056 | B | Design systems (extract colours, type, components from codebases/decks; publish org default; /design-sync from Code) | Claude Design / Artifacts | web, desktop, Code | Ask in chat or /design-sync | SC14604397; SC17457950 | pg 2026-10-26 | NOT_OBSERVED | BETA-PREVIEW | P/M/T/E (on by default P/M/T; E off); Q: "Design systems are available in beta on Pro, Max, Team, and Enterprise" | none | Artifact; subject to artifact retention | None | DEFER (Design agent) | Brand consistency | H | none |
| CL-B-057 | B | Skills inside Microsoft 365 add-ins ("/" in sidebar; template-exact loading in Excel/PowerPoint) | Claude for Microsoft 365 | Excel, PowerPoint, Word, Outlook | Type / in sidebar | SC12512180 | pg 2026-10-23 | NOT_OBSERVED | VERIFIED SHIPPING | Paid plans with add-ins | none | Uses account skills | Agent Skills | ADAPT | Consistent workflows | H | none |

### Family C - Cowork and agentic apps (tasks, planning, steering, scheduling, folders, browser, computer use, Dispatch, Duet, Tag, Science)

| feature_id | family | exact_feature | source_product | platform_surface | user_flow (short) | official_evidence_url | evidence_date | observed_test | shipped_status | plan_gate | region_or_OS_gate | data_storage_and_permissions | access_to_source_or_public_API | WePLD_route | user_value | confidence | unknowns |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CL-C-001 | C | Cowork whole-task delegation (multi-step work: search, read files, run code, assemble deliverables) | Claude Cowork | desktop, web, mobile, Chrome side panel | Select "Cowork" (legacy) or just describe task (unified) | SC13345190; SC16761823 | RN 2026-04-09 (GA desktop); acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING (desktop GA) / BETA-PREVIEW (web, mobile, Linux) | P/M/T/E (paid only) | Desktop macOS/Windows; Linux beta | Sessions and files saved to account | Managed Agents / Agent SDK are API analogues | USE VIA OFFICIAL INTEGRATION (Agent SDK/Managed Agents) + REIMPLEMENT UX | Hand off real work | H | none |
| CL-C-002 | C | Planning: Claude analyses request, writes plan, splits into subtasks; progress indicators per step | Claude Cowork | all Cowork surfaces | Automatic | SC13345190 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | n/a | Agent SDK | REIMPLEMENT FROM OBSERVED BEHAVIOR | Transparency | H | Plan approval UI specifics |
| CL-C-003 | C | Steering mid-task and answering Claude's questions from any surface | Claude Cowork | desktop, web, mobile | Type into running task; stop/redirect | SC13345190; SC15520349 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | n/a | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Human-in-the-loop | H | none |
| CL-C-004 | C | Sub-agents and parallel workstreams within a task | Claude Cowork | all | Automatic | SC13345190 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | n/a | Agent SDK subagents | USE VIA OFFICIAL INTEGRATION | Speed on big tasks | H | Concurrency caps |
| CL-C-005 | C | Several tasks running at once ("Parallel tasks") | Claude | all | Start multiple tasks | SC16761823; claude.com/product/overview | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | n/a | None | ADAPT | Throughput | H | Limits |
| CL-C-006 | C | Cloud execution by default (P/M since 2026-10-06; "Only on your computer" removed; one-way migration) | Claude Cowork | desktop, web, mobile | Automatic | SC15520349 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M (T default on; E opt-in) | none | Per-session sandbox on Anthropic infra, destroyed at end; session-scoped tokens; mandatory egress proxy | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Runs with laptop closed | H | Sandbox spec |
| CL-C-007 | C | Local sessions in isolated Linux VM (Apple Virtualization.framework / Hyper-V); legacy for P/M pre-2026-10-06 tasks | Claude Cowork | desktop | Existing local tasks only (P/M); T/E local still available | SC14479288; SC15520349 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING (T/E) / NOT AVAILABLE (new P/M) | T/E; legacy P/M | macOS, Windows; Linux needs KVM/QEMU, 8 GB RAM, 25 GB disk | Agent loop native; code in VM; app-layer permission checks | None | DEFER | Local privacy | H | none |
| CL-C-008 | C | Connected local folders ("Trusted folders"); read/write without upload; cloud tasks fetch only needed file copies | Claude Cowork | desktop (web/mobile via desktop bridge) | Grant folder | SC13345190; SC15520349; SC16761823 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | Desktop app must be open | Copies deleted with session; each local call checked vs permissions | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Work on real files | H | Copy retention specifics |
| CL-C-009 | C | Folder instructions (per-folder context file Claude can update) | Claude Cowork | desktop | Select folder; edit instructions | SC13345190 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | desktop | Stored in folder (implied) | None | ADAPT | Project context | M | File name/location |
| CL-C-010 | C | Explicit permission before permanent file deletion | Claude Cowork | desktop | Permission prompt | SC13345190; SC16761823 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | n/a | None | ADAPT | Safety | H | none |
| CL-C-011 | C | Permission modes: Manual (ask each action) / Auto (safety review, read-only auto-approved) / Skip (no checks) | Claude Cowork, Chrome | all | Message-box setting per conversation | SC13345190; SC16761823; SC12902446 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | Default Auto on P/M/T, Manual on E; admins can disable Auto/Skip | none | Safety review checks exfiltration and prompt injection | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Autonomy vs control | H | Classifier details |
| CL-C-012 | C | Connector tool permissions per tool: Always allow / Needs approval / Blocked; org "Allow 'Always allow' for connector tools" off by default | Claude Cowork + chat | all | Customize > Connectors | SC13345190; SC11176164; SC13455879 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All (admin overrides T/E) | none | Admin settings are ceilings | None | ADAPT | Least privilege | H | none |
| CL-C-013 | C | Scheduled tasks (/schedule or "Scheduled" sidebar; hourly, daily, weekly, weekdays, on demand) | Claude Cowork | desktop, web, mobile | Describe cadence or set up manually | SC13854387 | RN 2026-02-25 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E (admin toggle) | Cloud runs need no device; local-file tasks run locally | Each run is its own session | None (Code has cloud scheduled tasks) | REIMPLEMENT FROM OBSERVED BEHAVIOR | Recurring automation | H | Notifications on run, limits |
| CL-C-014 | C | Scheduled-task management: edit, pause, resume, delete, run now, run history | Claude Cowork | desktop, web, mobile | Scheduled view | SC13854387 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | n/a | None | ADAPT | Control | H | none |
| CL-C-015 | C | Cowork projects (instructions, scheduled tasks, context: local folder/linked chat project/URL, project memory) | Claude Cowork | desktop all paid; web/mobile P/M, T beta, E opt-in | "+" next to Projects | SC14116274 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | Saved to account; folder files stay local | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Organised long work | H | Bulk import unsupported |
| CL-C-016 | C | Folder-based projects migrated into account (name, instructions, memory copy; files stay local) | Claude Desktop | desktop | Automatic | SC14116274 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M (T/E only with unified) | none | Nothing uploaded or deleted | None | DEFER | Continuity | H | none |
| CL-C-017 | C | Built-in browser in Claude Desktop (side panel; open, read, click, type, fill forms) | Claude Cowork | desktop; web/mobile while desktop online | Automatic for web tasks | SC16607400 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING (rolling out) | P/M; T/E unless owner disables | macOS, Windows, Linux beta | Logins persist per computer; high-risk sites blocked; per-site first-use permission | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Web automation without extension | H | Sign-in data retention |
| CL-C-018 | C | Cookie import per site into built-in browser (banking/email/SSO unchecked by default) | Claude Cowork | desktop | First-use dialog | SC16607400 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | As CL-C-017 | macOS: Chrome/Edge/Firefox; Windows/Linux: Firefox; no Safari | Stored on that computer | None | REJECT | Stay signed in | H | none |
| CL-C-019 | C | Preferred browser setting (built-in vs Claude in Chrome; fallback rules) | Claude Cowork | desktop | Settings > Cowork | SC16607400; SC12012173 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | n/a | None | ADAPT | Choice | H | none |
| CL-C-020 | C | Computer use (click, type, open apps when no connector fits; background windows on macOS 15+; "Full control" option) | Claude Cowork, Claude Code (desktop) | desktop | Settings > Capabilities > Enable computer use; approve each app | SC14128542 | RN 2026-03-23 | NOT_OBSERVED | BETA-PREVIEW | P/M only (not T/E) | macOS, Windows; not Linux | Screenshots of screen; no sandbox between Claude and apps | API computer-use tool | DEFER | Automate apps without APIs | H | Admin controls none |
| CL-C-021 | C | Computer-use app permissions: per-app approval, default-blocked trading/crypto apps, user blocklist | Claude Cowork | desktop | Approval prompts | SC14128542 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | P/M | macOS, Windows | n/a | None | ADAPT (if ever built) | Safety | H | none |
| CL-C-022 | C | Tool priority order: connectors, then browser, then screen control | Claude Cowork | all | Automatic | SC14128542 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | n/a | None | ADAPT | Reliability | H | none |
| CL-C-023 | C | Dispatch: one persistent thread across phone and desktop; routes dev work to Code and knowledge work to Cowork | Claude Cowork | desktop + iOS/Android | Cowork > Dispatch setup | SC13947068; code.claude.com/docs/en/overview | RN 2026-03-17, 2026-03-23 | NOT_OBSERVED | RESTRICTED (limited beta; not for new users) | Some P/M | Desktop must be awake; no computer use on Linux | n/a | None | DEFER | Remote delegation | H | End-of-life date |
| CL-C-024 | C | Cowork on web and mobile (remote sessions; start, steer, review, resume) | Claude Cowork | web, iOS, Android | Home tab / app | SC15520349 | RN 2026-07-07 | NOT_OBSERVED | BETA-PREVIEW | P/M; T beta; E owner-enabled | none | Sessions synced via account | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Work from anywhere | H | none |
| CL-C-025 | C | Desktop bridge for cloud sessions: local files, local connectors/plugins, browser use, computer use only while desktop app open | Claude Desktop | desktop + any surface | Keep desktop open | SC15520349; SC14479288 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | Anthropic-brokered connection; per-call permission check | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Hybrid local/cloud | H | Protocol unpublished |
| CL-C-026 | C | Offline behaviour: stable internet required; local-dependent steps fail when desktop offline; cloud tasks continue | Claude Cowork | all | n/a | SC13345190; SC14479288 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | n/a | None | ADAPT | Expectation setting | H | No offline mode documented |
| CL-C-027 | C | Download task data, /port-task-data into Claude Code; "Export your Cowork data" | Claude Cowork | desktop | Home card / task menu | SC15520349 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M | none | Zip export | None | ADAPT | Portability | H | Export format |
| CL-C-028 | C | Task deletion (immediate removal from history; backend removal within 30 days) | Claude Cowork | all | Task menu | SC13345190 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | 30-day purge | None | ADAPT | Data control | H | none |
| CL-C-029 | C | Memory in cloud Cowork (shared with chat; per-task memory off before first message; local sessions use no memory) | Claude Cowork | cloud sessions | "+" > Memory | SC13345190; SC11817273 | RN 2026-08-25 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | As memory | None | ADAPT | Continuity | H | none |
| CL-C-030 | C | Cowork deliverables (xlsx with formulas, pptx, docs, charts) and share individual artifacts (not sessions) | Claude Cowork | all | Preview/download | SC13345190 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | Sessions cannot be shared | None | ADAPT | Finished work | H | none |
| CL-C-031 | C | Plugin "Customize" in Cowork (Cowork task that edits plugin skills/connectors) | Claude Cowork | desktop, web | Customize on installed plugin | SC13837440 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | n/a | None | ADAPT | Self-serve tailoring | H | none |
| CL-C-032 | C | Cowork admin toggles: enable org, run in cloud, built-in browser, network access, web search, Auto-mode defaults, plugin availability | Claude Cowork T/E | admin console | Organization settings > Cowork/Capabilities | SC13455879 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | none | Cloud off by default on E | n/a | DEFER | Governance | H | none |
| CL-C-033 | C | Cloud network policy and mandatory egress proxy; no private/metadata addresses; E default no network | Claude Cowork | cloud | Admin policy | SC14479288 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | T/E (policy) | none | Connector tokens never enter sandbox | None | ADAPT | Security posture | H | Proxy allowlist format |
| CL-C-034 | C | Trusted Devices and recent sign-in required for cloud sessions / Remote Control | Claude Cowork, Claude Code | desktop, web, mobile | Admin requires; device enrols | SC14479288; SC17444462; RN | RN 2026-06-25 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | none | Device verification | None | DEFER | Zero-trust | M | Enrolment flow not read |
| CL-C-035 | C | Cowork OpenTelemetry export (prompts, tool/MCP calls, file access, approvals, API cost; content capture via otlpContentCapture policy) | Claude Cowork | desktop, web, mobile | Organization settings > Cowork > OTLP endpoint | SC14477985 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | Desktop 1.22209.3+ (cloud), 1.1.4173+ (local) | Auth headers encrypted; content off by default | OTLP HTTP/JSON or protobuf | ADAPT | Observability | H | none |
| CL-C-036 | C | Cowork captured in Compliance API (web/mobile remote sessions and local; HIPAA local 30 days) | Claude Cowork | all | API pull | SC13364135; SC14479288; SC13455879 | pg 2026-10-23 | NOT_OBSERVED | VERIFIED SHIPPING | E; Q: "Cowork via mobile and web is captured in Compliance API" | none | Audit trail per user | Compliance API | DEFER | Compliance | H | Compliance API article itself does not mention Cowork |
| CL-C-037 | C | EDR cannot inspect VM or cloud sessions (documented limitation) | Claude Cowork | desktop, cloud | n/a | SC14479288 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | n/a | none | n/a | None | ADAPT (note for security docs) | Planning input | H | none |
| CL-C-038 | C | Cowork on HIPAA-ready plans: local mode only after Primary Owner applies HIPAA configuration; no cloud Cowork, no built-in browser | Claude Cowork | desktop | Admin config | SC13455879; SC17318731 | RN 2026-07-14 | NOT_OBSERVED | RESTRICTED | E HIPAA | none | BAA coverage conditional | None | DEFER | Regulated use | H | none |
| CL-C-039 | C | Chrome side panel runs as a Cowork session (history synced; skills, plugins, connectors) | Claude in Chrome + Cowork | Chrome | Open side panel | SC12012173; SC15520349 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW (rolling out; classic panel fallback) | M/T; P rolling; E admin-enabled | Chrome only | Synced to account | None | DEFER | Browser-native agent | H | none |
| CL-C-040 | C | Unified experience for Enterprise: chat to sandbox VM escalation; sandbox idle snapshot encrypted; sandboxes expire 30 days; default-on 2026-11-16 | Claude Enterprise | web, desktop, mobile | Owner toggles "Chat and Cowork unified" | SC17444462 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW (opt-in until 2026-11-16) | E | Not for ZDR, HIPAA, CMEK orgs | Custom retention covers chats; not direct Cowork sessions/scheduled tasks | Analytics API object chat_cowork_unified_metrics | DEFER | Simplified enterprise UX | H | none |
| CL-C-041 | C | Cowork usage accounting (agentic steps consume more; Settings > Usage) | Claude Cowork | all | n/a | SC13345190; SC16761823 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | n/a | None | DEFER | Cost awareness | H | Rates |
| CL-C-042 | C | Use Cowork safely: read/write tool risk model, trust boundary, content classifiers, auto-mode action screening, deletion protection, scheduled-task cautions, cross-app data flow in Office add-ins | Claude Cowork | all | Read guidance; choose permission mode | SC13364135 | pg 2026-10-23 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | User responsible for actions; report to usersafety@anthropic.com | n/a | ADAPT (risk model and UX copy) | Safety UX | H | none |
| CL-C-043 | C | Browser use admin setup for Cowork: built-in browser and Claude in Chrome toggles; shared allow/blocklist; preferred-browser fallback | Claude Cowork T/E | admin | Organization settings > Cowork / Claude in Chrome | SC16635803 | pg 2026-10-23 | NOT_OBSERVED | VERIFIED SHIPPING | T on by default; E on unless disabled; HIPAA off | Built-in browser unavailable under HIPAA local config | Same safety layers both browsers | n/a | DEFER | Governance | H | none |
| CL-C-044 | C | Claude Duet: proactive agent app on its own cloud computer; morning brief; Tasks and Make tabs; channels sharing memory | Claude Duet | iOS, Android app | Waitlist invite; message by text or voice | SC17631495; claude.com/product/overview | RN 2026-10-21 | NOT_OBSERVED | RESTRICTED (research preview, waitlist waves) | P/M only | US accounts only | Uses Claude memory, skills, connectors; asks before sending/paying/signing/deleting | None | DEFER | Proactive assistant | H | Expansion timeline to T/E |
| CL-C-045 | C | Duet cloud browser for sites without connectors (cannot be watched/taken over; passwords via separate form) | Claude Duet | cloud | Automatic | SC17631495 | RN 2026-10-21 | NOT_OBSERVED | RESTRICTED | P/M | US | n/a | None | DEFER | Reach long tail sites | H | none |
| CL-C-046 | C | Duet payments via Link by Stripe and Shop Pay (approval per purchase, one-time card) | Claude Duet | mobile | Approve purchase | SC17631495; SC17666484; SC17666489 | RN 2026-10-21 | NOT_OBSERVED | RESTRICTED | P/M | US | One-time card per purchase; no trading/money movement | None | REJECT | Agentic commerce | H | none |
| CL-C-047 | C | Claude Tag (Claude in Slack): tag in channels, DMs, AI assistant panel; own identity; per-channel memory; follow-ups | Claude Tag | Slack | Owner sets up identity, tools, channels; members @-mention | SC15594475; claude.com/product/overview | RN 2026-06-23; switch 2026-08-03 | NOT_OBSERVED | BETA-PREVIEW | T/E | Slack only | Slack conversations separate from chat history; deleted within 30 days of uninstall | Slack app | DEFER | Team-shared agent | H | none |
| CL-C-048 | C | Claude Tag consumption billing: org cap, per-channel limits, 75/95% alerts; Activity page; GitHub App commits link back to thread | Claude Tag | Slack, admin | Admin settings | SC15594475 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | T/E | none | Owners view/edit/delete channel memory | n/a | DEFER | Spend control | H | none |
| CL-C-049 | C | Claude Science desktop app (sandboxed code, scientific DB connectors, own compute clusters, versioned artifacts with provenance) | Claude Science | macOS 13+, Windows 11 x64, Linux x64 | Download; describe research task | SC16563838; claude.com/download | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | P/M/T/E (T/E owner enables) | OS list as stated | Storage not stated on page | None | DEFER | Research automation | H | Data storage, changelog location |
| CL-C-050 | C | Record a skill: screen, clicks, typing and voice recording (about 10 minutes) turned into a proposed skill | Claude Cowork | Claude for Mac | "+" > Record a skill | SC12512198 | pg 2026-10-15 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T only; Q: "isn't available in chat, on Windows, or on Free and Enterprise plans" | macOS only (Accessibility, Screen recording permissions) | Video/audio not retained; screenshots kept in task | None | REIMPLEMENT FROM OBSERVED BEHAVIOR | Programming by demonstration | H | none |

### Family D - Claude Code surfaces (summary rows only; CLI flags and depth covered by other agents)

| feature_id | family | exact_feature | source_product | platform_surface | user_flow (short) | official_evidence_url | evidence_date | observed_test | shipped_status | plan_gate | region_or_OS_gate | data_storage_and_permissions | access_to_source_or_public_API | WePLD_route | user_value | confidence | unknowns |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CL-D-001 | D | Claude Code terminal CLI (pointer; native installer, Homebrew, WinGet, apt/dnf/apk; /model, --model, env vars; API-key vs subscription precedence) | Claude Code | terminal (macOS, Linux, WSL, Windows) | Install; run `claude` | code.claude.com/docs/en/overview; SC11940350; SC12304248 | acc 2026-10-27; pg 2026-10-07 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E or Console/API key; third-party providers | none | Local; settings files | CLI + Agent SDK documented | USE VIA OFFICIAL INTEGRATION | Agentic coding | H | See Code agent (R03C) |
| CL-D-002 | D | Desktop app Code tab (visual diffs, parallel sessions, scheduled tasks, cloud sessions) | Claude Code | Claude Desktop | Click Code tab | code.claude.com/docs/en/overview | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | Paid plans | macOS, Windows x64/ARM64; Linux beta | Local + account | n/a | USE VIA OFFICIAL INTEGRATION | GUI coding | H | none |
| CL-D-003 | D | Claude Code on the web / cloud sessions (claude.ai/code; isolated VM per task; PR at end; `claude --cloud`) | Claude Code | web, desktop, mobile | Pick repo, describe task | SC12618689; code.claude.com/docs/en/overview | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | Paid plans (article silent) | none | GitHub creds via proxy, not in VM | GitHub | USE VIA OFFICIAL INTEGRATION | Async coding | M | Plan gate not stated |
| CL-D-004 | D | Claude Code in mobile app | Claude Code | iOS, Android | Start/monitor cloud tasks | code.claude.com/docs/en/overview | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | Paid | none | n/a | n/a | DEFER | Mobile oversight | M | none |
| CL-D-005 | D | VS Code / Cursor extension (inline diffs, @-mentions, plan review) | Claude Code | VS Code, Cursor | Install extension | code.claude.com/docs/en/overview | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | Plan or Console; third-party providers | none | Local | Extension | USE VIA OFFICIAL INTEGRATION | IDE integration | H | none |
| CL-D-006 | D | JetBrains plugin (requires CLI) | Claude Code | IntelliJ family | Install plugin | code.claude.com/docs/en/overview; claude.com/download | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | As CLI | none | Local | Plugin | USE VIA OFFICIAL INTEGRATION | IDE integration | H | none |
| CL-D-007 | D | GitHub Actions and GitLab CI/CD integration | Claude Code | CI | Configure workflow | code.claude.com/docs/en/overview | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | API key or plan | none | CI runner | Documented actions | USE VIA OFFICIAL INTEGRATION | Automated PR work | H | none |
| CL-D-008 | D | GitHub Code Review (fleet of agents posts inline PR findings) | Claude Code | GitHub | Set up Code Review | SC14233555 | pg 2026-10-20 | NOT_OBSERVED | VERIFIED SHIPPING | T/E only; Q: "Code Review is available on Team and Enterprise plans" | Not with ZDR | GitHub App | GitHub App | USE VIA OFFICIAL INTEGRATION | Review quality | H | none |
| CL-D-009 | D | Slack @Claude routing bug reports to PRs | Claude Code / Claude Tag | Slack | Mention @Claude | code.claude.com/docs/en/overview; claude.com/download | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | T/E (Tag) | none | Slack | Slack app | DEFER | ChatOps | M | Relationship to Claude Tag |
| CL-D-010 | D | Remote Control (continue local session from phone/browser) | Claude Code | desktop/CLI + mobile/web | Enable remote control | code.claude.com/docs/en/overview; SC17444462 | RN 2026-06-25 | NOT_OBSERVED | VERIFIED SHIPPING | Paid | none | Admin can disable; Trusted Devices | n/a | DEFER | Mobility | M | none |
| CL-D-011 | D | Channels (push Telegram, Discord, iMessage, webhooks into a session) | Claude Code | CLI | Configure channel | code.claude.com/docs/en/overview | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING (status not stated) | Unknown | none | n/a | Documented | DEFER | Event-driven sessions | L | Status |
| CL-D-012 | D | Cloud scheduled tasks (formerly routines; API/GitHub triggers), desktop scheduled tasks, /loop | Claude Code | web, desktop, CLI | /schedule | code.claude.com/docs/en/overview | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | Paid | none | Cloud | API trigger documented | USE VIA OFFICIAL INTEGRATION | Automation | H | none |
| CL-D-013 | D | Session handoff: `claude --teleport`, `/desktop` | Claude Code | CLI, desktop, web | Command | code.claude.com/docs/en/overview | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | claude.ai subscription | /desktop macOS and x64 Windows | n/a | n/a | DEFER | Continuity | H | none |
| CL-D-014 | D | Agent SDK (build custom agents on Claude Code tools); usage counts against plan when signed in with plan | Claude Agent SDK | developer | Install SDK | code.claude.com/docs/en/overview; SC15036540 | pg update 2026-06-15 | NOT_OBSERVED | VERIFIED SHIPPING | Plan or API key (Max/Team API credits) | none | Developer-controlled | Public SDK | USE VIA OFFICIAL INTEGRATION | Build WePLD agents on official harness | H | Terms for embedding in third-party products |
| CL-D-015 | D | Automated security reviews (/security-review, GitHub Action); Claude Code Security Center (beta) | Claude Code | CLI, GitHub | Command/Action | SC11932705; SC14503520 | pg 2026-03-16 | NOT_OBSERVED | VERIFIED SHIPPING (/security-review) / BETA-PREVIEW (Security Center) | Individual paid plans named (P/M); org use via Action | none | n/a | GitHub Action | USE VIA OFFICIAL INTEGRATION | Secure code | M | Security Center scope |
| CL-D-016 | D | Claude Security (continuous repo scanning, threat model, validated findings, fix via Claude Code; API, MCP connector, webhooks) | Claude Security | web | Owner enables; connect repos | SC14661296 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW (public beta) | E only, premium seats, usage credits | No ZDR | Up to 8 repos per project; roles Full/Triage/View | Claude Security API + MCP | DEFER | AppSec | H | none |
| CL-D-017 | D | Claude in Xcode 26 (Intelligence settings sign-in) | Apple Xcode + Claude | macOS Xcode 26 | Sign in in Xcode | SC12293051 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M; T/E premium seats | macOS | Shared usage limits | Apple integration | DEFER | iOS dev | M | Page names Sonnet 4 (may be stale) |
| CL-D-018 | D | Claude Code usage analytics (productivity and adoption metrics) | Claude Code | admin, Console | Dashboard | SC12157520 | pg 2026-10-20 | NOT_OBSERVED | VERIFIED SHIPPING | T Owners; E Owners/Admins (needs Chat+Code or Premium seat); Console Admin/Billing/Developer | none | n/a | Analytics API | DEFER | Adoption tracking | H | none |
| CL-D-019 | D | Claude Code changelog and weekly "What's new" digests (pointer) | Claude Code | docs | Read | code.claude.com/docs/en/changelog | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | n/a | n/a | n/a | RSS feed | USE VIA OFFICIAL INTEGRATION (monitor) | Change tracking | H | Not read in depth |
| CL-D-020 | D | Plugin sync from Claude account to Claude Code (v2.1.273+, one-way; `syncClaudeAiPlugins`) | Claude Code | CLI | Sign in with same account | SC13837440 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | No sync with API key/Bedrock | Plugins run locally | n/a | ADAPT | Consistent tooling | H | none |
| CL-D-021 | D | Claude Code screen reader mode (plain sequential output) | Claude Code | terminal | Enable mode | SC15924927 | pg 2026-07-13 | NOT_OBSERVED | VERIFIED SHIPPING | All Code users | Claude Code 2.1.181+ | n/a | n/a | ADAPT | Accessibility | H | none |
| CL-D-022 | D | Dynamic workflows (large migrations/audits in one Claude Code session) | Claude Code | CLI | Run workflow | SC12386420; code.claude.com/docs/en/overview | pg 2026-10-15 | NOT_OBSERVED | VERIFIED SHIPPING | E; Q: "Dynamic workflows (available for Claude Enterprise plans)" | none | n/a | Claude Code docs | DEFER (Code agent) | Large-scale changes | H | none |
| CL-D-023 | D | Claude Code included in Team seats and the single Enterprise seat; Pro/Max via Desktop Code tab recommended | Claude Code | desktop, CLI | Sign in with plan | SC11845131; SC11145838; SC9266767 | pg 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E; Q: "Claude Code is included with every Team plan seat" | none | n/a | n/a | DEFER | Packaging benchmark | H | none |
| CL-D-024 | D | Console-to-Enterprise migration for Claude Code (CLI history local; switch login) | Claude Code | admin | Provision E accounts; users re-login | SC14128775 | pg 2026-10-16 | NOT_OBSERVED | VERIFIED SHIPPING | E | none | CLI sessions stored locally | n/a | DEFER | Procurement path | H | none |
| CL-D-025 | D | Claude Code launch guides (first day, models/limits, troubleshooting, CLAUDE.md, cheatsheet, FAQs, power tips, use cases, comms and champion kits) | Claude Code | docs | Read | SC14552382; SC14552983; SC14552646; SC14553240; SC14553413; SC14554922; SC14554000; SC14553517; SC14555877; SC14555399 | pg 2026-04-15..2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | n/a | Node 18+ noted for install | n/a | n/a | ADAPT (enablement playbook pattern) | Adoption | H | Depth covered by Code agent |

### Family E - Tools and extensibility (skills, plugins, connectors, MCP, extensions, Chrome) and Enterprise administration

| feature_id | family | exact_feature | source_product | platform_surface | user_flow (short) | official_evidence_url | evidence_date | observed_test | shipped_status | plan_gate | region_or_OS_gate | data_storage_and_permissions | access_to_source_or_public_API | WePLD_route | user_value | confidence | unknowns |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CL-E-001 | E | Skills: folders of instructions/scripts/resources loaded by progressive disclosure | Claude | web, desktop, Cowork, Code, API | Automatic when relevant; "/" to invoke | SC12512176; SC12512180 | RN 2025-12-18 | NOT_OBSERVED | VERIFIED SHIPPING | All (code execution required) | none | Account | Agent Skills spec + API (beta via code execution tool) | COPY (Agent Skills format) | Reusable know-how | H | none |
| CL-E-002 | E | Anthropic skills (Excel, Word, PowerPoint, PDF creation) auto-invoked | Claude | all | Automatic | SC12512176 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | API skills | USE VIA OFFICIAL INTEGRATION | Quality documents | H | License of skill contents |
| CL-E-003 | E | Custom skills (Markdown, optional scripts), upload and edit | Claude | web, desktop | Customize > Skills > "+" | SC12512198; SC12512176 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Account | Agent Skills format | COPY (format) | Personal automation | H | Size limits |
| CL-E-004 | E | Organization-provisioned skills (on/off by default for all members) | Claude T/E | web, desktop | Admin provisions | SC12512176; SC13119606 | RN 2025-12-18 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | none | Org library | n/a | ADAPT | Standardisation | H | none |
| CL-E-005 | E | Partner skills (Notion, Figma, Atlassian) in Skills Directory | Claude | web, desktop | Browse skills | SC12512176 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | View-only installs | n/a | USE VIA OFFICIAL INTEGRATION | Ready-made workflows | H | none |
| CL-E-006 | E | Agent Skills open standard (agentskills.io) with reference Python SDK | Anthropic standard | cross-platform | Implement spec | SC12512176 | RN 2025-12-18 | NOT_OBSERVED | VERIFIED SHIPPING | n/a | none | n/a | Public spec + SDK | COPY | Interoperable skills in WePLD | H | Spec license terms not checked |
| CL-E-007 | E | Skill sharing with people / groups; org publishing ("Open" or "Requires review") | Claude T/E | web, desktop | Share or Publish to org | SC13837440; SC14328846 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING (groups E only) | T/E | none | Shared items view-only | n/a | ADAPT | Team reuse | H | none |
| CL-E-008 | E | Skill and plugin security scanning (pass/warn/fail; "Allow anyway" per version) | Claude Enterprise | web, desktop, Cowork, marketplaces | Automatic on upload/edit | SC15927065 | RN 2026-08-06; pg 2026-10-21 | NOT_OBSERVED | VERIFIED SHIPPING (article has no beta label; RN said beta) | E; Q: "on by default for Enterprise organizations that hadn't chosen a setting before October 2" | Not CMEK/ZDR/HIPAA | Hooks scanned; MCP servers not scanned | n/a | ADAPT | Supply-chain safety | M | Beta status conflict |
| CL-E-009 | E | Plugins: bundles of skills, connectors, sub-agents, commands, hooks, local MCP servers; saved to account | Claude | web Chat, desktop Chat, Cowork, Code | Customize > Plugins > Discover > Add; upload file | SC13837440 | RN 2026-02-24 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | Hooks/sub-agents/local MCP not in chat | Local MCP runs with user permissions | Plugin format (Claude Code plugins) | ADAPT | Packaged capabilities | H | none |
| CL-E-010 | E | Plugin Create (build from scratch or Anthropic templates); knowledge-work-plugins on GitHub | Claude | web, desktop | Plugin Create | SC13837440 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | none | n/a | GitHub repo anthropics/knowledge-work-plugins | ADAPT (check license before any COPY) | Faster authoring | H | Repo license not checked |
| CL-E-011 | E | Plugin marketplaces (Knowledge Work default; Life Sciences, Financial Services, Legal; add GitHub/GitLab/Bitbucket repo) | Claude | web, desktop, Code | Add marketplace by URL | SC13837440 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E (org may restrict) | none | Public repos only | Marketplace repo format | ADAPT | Ecosystem | H | none |
| CL-E-012 | E | Org plugin publishing with review (Available / Installed by default / Required), per-group assignment (E) | Claude T/E | admin | Publish to org | SC13837440; SC13837433 | RN 2026-02-24 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | none | Required plugins cannot be disabled | n/a | DEFER | Governance | H | none |
| CL-E-013 | E | Developer portal for submitting plugins/remote connectors to directory, review tracking, usage analytics | Claude directory | web | Submit | RN (SC12138966); SC10949351 | RN 2026-09-25 | NOT_OBSERVED | VERIFIED SHIPPING | Developers | none | Directory policy/terms apply | Submission portal | USE VIA OFFICIAL INTEGRATION | Distribution channel for WePLD connector | M | Portal URL not captured |
| CL-E-014 | E | Unified directory under Customize (Skills, Connectors, Plugins tabs; "Your organization" tab) | Claude | web, desktop, Cowork, Code | Customize > tab > Discover | SC14328846 | pg 2026-09-25 | NOT_OBSERVED | VERIFIED SHIPPING | All (org tab T/E) | Mobile not mentioned | n/a | n/a | ADAPT | One place to extend | H | Mobile |
| CL-E-015 | E | Connectors Directory (prebuilt; read/write capability labels; "Interactive" badge) | Claude | web, desktop, mobile | Customize > Connectors | SC11176164; SC11596036 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Third-party processing under their terms | MCP | USE VIA OFFICIAL INTEGRATION | Integrations | H | none |
| CL-E-016 | E | Custom connectors via remote MCP (URL; auth Sign in now/when needed/none; OAuth client: Claude published identity, auto registration, own client; fixed headers) | Claude | web, desktop, Cowork (mobile uses ones added elsewhere) | Customize > Connectors > Add > Custom > Web | SC11175166; SC11176164 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All (Free: 1 custom connector) | Server must be reachable from Anthropic IP ranges | Fixed credentials encrypted; shared credential = shared access | MCP open protocol | USE VIA OFFICIAL INTEGRATION | Expose WePLD to Claude | H | Transport version not stated |
| CL-E-017 | E | Per-conversation connector toggles ("+" > Connectors) | Claude | all | Toggle | SC11176164 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | n/a | ADAPT | Context control | H | none |
| CL-E-018 | E | Tool access modes: Auto (default) / Always available / On demand (tool search) | Claude | web, desktop, Cowork, mobile | "+" > Connectors > Tool access | SC13730515 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | API tool search (not assessed) | ADAPT | Scale to many tools | H | none |
| CL-E-019 | E | Connector revocation (disconnect in Customize or in third-party security settings) | Claude | all | Disconnect | SC11176164; SC11175166 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Retrieved data stays with chat until chat deleted | n/a | ADAPT | Control | H | none |
| CL-E-020 | E | Interactive connectors / MCP Apps (inline cards, fullscreen apps; Amplitude, Asana, Box, Canva, Clay, Figma, Hex, Slack) | Claude | web, desktop, Cowork, iOS, Android | Enabled with connector | SC13454812 | RN 2026-03-25 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | Sandboxed iframes, strict CSP, JSON-RPC, predeclared domains | MCP Apps open extension | COPY (MCP Apps spec) | Rich UI inside Claude | H | none |
| CL-E-021 | E | Connector suggestions (Claude proposes connected apps; no paid placement; confirms before transactions) | Claude | web, desktop, mobile | Automatic | SC14730684 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | Unstated | Mobile install beta | App data not used for training | n/a | DEFER | Discovery | H | none |
| CL-E-022 | E | Enterprise-managed authorization for connectors via IdP (Okta at launch; 10 connectors) | Claude T/E | admin | Organization settings > Connectors > Managed authorization | SC15537633; SC11176164 | pg 2026-08-24; pg 2026-10-16 | NOT_OBSERVED | VERIFIED SHIPPING per SC15537633 / BETA-PREVIEW per SC11176164 | T/E; Q: "This feature is generally available for Team and Enterprise plans" | none | Token lifetimes per IdP | Public Enterprise-Managed Authorization spec | ADAPT | SSO for tools | M | Conflict: SC11176164 says "available in beta" |
| CL-E-023 | E | Member connector requests (approve/decline/block) | Claude T/E | admin | Organization settings > Notifications > Requests | SC11176164 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | T on / E off by default | none | n/a | n/a | DEFER | Governance | H | none |
| CL-E-024 | E | Restrict verified-domain connectors to the Enterprise (block personal accounts using company domain for Gmail/Slack etc.) | Claude Enterprise | admin | Admin toggle | SC15402193 | pg 2026-10-20 | NOT_OBSERVED | VERIFIED SHIPPING | E; Owners or Identity & Access managers | Needs at least one verified domain | n/a | n/a | DEFER | Data boundary | H | none |
| CL-E-025 | E | Google Workspace connectors (Gmail send/reply/forward, Calendar CRUD, Drive search/upload/share/trash) with default approvals | Claude | web, desktop | Connect Google | SC10166901 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All (T/E owner enables) | none | Data stored with chat; no training | Google APIs | USE VIA OFFICIAL INTEGRATION | Email/calendar/docs | H | none |
| CL-E-026 | E | GitHub integration ("Add from GitHub" to chats/projects, branch file sync) | Claude | web, desktop | "+" > Add from GitHub | SC10167454 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING (legacy UI) / NOT AVAILABLE (unified UI) | Unstated | none | Only file names/contents synced | GitHub App | DEFER | Code context | M | Plan gate |
| CL-E-027 | E | Microsoft 365 connector (SharePoint, OneDrive, Outlook, Teams read; optional admin-enabled write tools) | Claude | web, desktop | Connect M365 | SC15183774; SC12542951; SC12684923 | RN 2026-07-07 | NOT_OBSERVED | VERIFIED SHIPPING | All (Entra work account) | Entra tenant consent | Teams posts always confirmed; no Sites.Selected | Microsoft Graph | USE VIA OFFICIAL INTEGRATION | Office data | H | none |
| CL-E-028 | E | 1Password for Claude (credential fill in Claude in Chrome; Claude never sees secrets) | 1Password + Claude in Chrome | Chrome on macOS | Approve with biometrics | SC15936181 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | P/M/T/E (T/E off by default) | macOS only | Logins/TOTP only; no cards | 1Password | DEFER | Safe sign-in | H | none |
| CL-E-029 | E | Salesforce in Claude plugin (37 sales skills, Salesforce + Slack connectors, per-user link) | Salesforce plugin | chat, Cowork (web, desktop) | Admin connects; user links | SC16952186; SC16952184 | RN 2026-09-15 | NOT_OBSERVED | RESTRICTED (beta, Salesforce-approved orgs) | All paid | none | Respects Salesforce permissions; write approvals | Plugin | DEFER | CRM workflows | H | none |
| CL-E-030 | E | Enterprise search ("Ask Your Org" project across Slack, M365, Gmail, Drive, SharePoint) | Claude T/E | web, desktop (not mobile) | Owner setup; users authenticate | SC12489464 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | none | Live MCP calls; not indexed by Anthropic | MCP | REIMPLEMENT FROM OBSERVED BEHAVIOR | Org knowledge Q&A | H | none |
| CL-E-031 | E | Desktop extensions (.mcpb local MCP servers; directory; custom install; built-in Node.js; secrets in OS keychain); only in Desktop and Claude Code, not web/mobile | Claude Desktop | macOS, Windows, Linux | Settings > Desktop app > Extensions | SC10949351; SC11725091; SC12702546 | pg 2026-10-23 | NOT_OBSERVED | VERIFIED SHIPPING | All desktop (pricing table: Free to Max "Yes"); admin controls T/E | none | Sensitive manifest fields encrypted via OS keychain | MCPB format + `mcpb pack` | COPY (MCPB manifest) | Local tools | H | .dxt legacy name not on current pages |
| CL-E-032 | E | Local MCP servers via claude_desktop_config.json (local network; not in Cowork cloud or claude.ai) | Claude Desktop | desktop | Edit config | SC11175166; SC10949351 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All desktop | none | Runs with user permissions | MCP | USE VIA OFFICIAL INTEGRATION | Local integrations | H | none |
| CL-E-033 | E | Desktop extension allowlist and custom team extensions upload | Claude Desktop T/E | admin | Organization settings > Connectors > Desktop | SC12592343 | RN 2025-08-21 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | Desktop 0.13.91+ | Enabling removes existing installs | n/a | DEFER | Governance | H | none |
| CL-E-034 | E | MDM/system policy keys (isDesktopExtensionEnabled, isDesktopExtensionDirectoryEnabled, isLocalDevMcpEnabled, isClaudeCodeForDesktopEnabled, disableAutoUpdates, org-restricted login, otlpContentCapture) | Claude Desktop | managed macOS (Jamf, Kandji, Intune) and Windows (registry) | MDM profile / HKLM policies | SC12622667; SC14479288; SC14477985; SC13065128 | pg 2026-10-13 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | macOS, Windows | Machine policy overrides in-app allowlist | n/a | DEFER | Fleet control | H | none |
| CL-E-035 | E | MCP Connector in Claude API (pointer) | Claude Platform | API | API parameter | SC11176164 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | API | none | n/a | Public API | USE VIA OFFICIAL INTEGRATION | Server-side MCP | M | Not read on platform docs |
| CL-E-036 | E | Claude in Chrome extension (navigate, click, type; read DOM/console/network; multi-tab; background work) | Claude in Chrome | Chrome desktop only | Install from Chrome Web Store | SC12012173; SC12902428; SC12902405 | pg 2026-10-05; pg 2026-10-23 | NOT_OBSERVED | BETA-PREVIEW (in the Chrome browser; GA inside Cowork/Code per page wording) | P/M/T/E; Q: "available in Claude Cowork and Claude Code, and in beta in the Chrome browser" | Chrome only | 15 extension permissions incl. debugger | Extension | DEFER | Browser automation | H | none |
| CL-E-037 | E | Chrome workflow recording to shortcuts, "/" shortcuts, scheduled shortcuts (daily/weekly/monthly/annual) | Claude in Chrome | Chrome (classic panel) | Record; schedule via clock icon | SC12012173 | RN 2025-11-24 | NOT_OBSERVED | BETA-PREVIEW | P/M/T/E | Chrome | Stored in extension | n/a | DEFER | Repeatable browser tasks | H | none |
| CL-E-038 | E | Chrome permission modes (Manually approve / Automatically approve / Skip all approvals) and site-level permissions with history | Claude in Chrome | Chrome | Side panel settings | SC12902446 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E | Chrome | Revoke per site; permission history | n/a | ADAPT | Control | H | none |
| CL-E-039 | E | Chrome hard-blocked categories (purchases, account creation, card/ID data, untrusted downloads, permanent deletion, trades, following web instructions) | Claude in Chrome | Chrome | n/a | SC12902446 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | n/a | ADAPT (policy baseline) | Safety | H | none |
| CL-E-040 | E | Chrome admin controls (enable, allowlist/blocklist shared with built-in browser, Workspace/MDM deploy, no ZDR) | Claude in Chrome T/E | admin | Organization settings > Claude in Chrome | SC13065128 | RN 2025-12-18 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | HIPAA orgs off by default | Connects to wss://bridge.claudeusercontent.com | n/a | DEFER | Governance | H | none |
| CL-E-041 | E | Built-in roles: Primary Owner, Owner, Admin, User; Custom (E) | Claude T/E | admin | Members page | SC9267276 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | none | One Primary Owner | n/a | ADAPT | RBAC baseline | M | Role matrix hard to parse |
| CL-E-042 | E | Custom roles RBAC (Capabilities, Permissions by admin area, Connectors per tool, Models with effort caps); additive; "View effective role" | Claude Enterprise | admin | Organization settings > Roles | SC13930458; SC13930452 | RN 2026-04-09, 2026-05-28, 2026-06-02 | NOT_OBSERVED | VERIFIED SHIPPING (Owner access beta) | E | none | Changes propagate up to 15 min | n/a | ADAPT | Fine-grained governance | H | none |
| CL-E-043 | E | Groups (manual or SCIM-synced) and SCIM group-to-role mapping | Claude Enterprise | admin, IdP | Groups page; map to "Custom" | SC13930458; SC14499648 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | E | none | Lockout risk if mapped early | SCIM | ADAPT | Automated access | H | none |
| CL-E-044 | E | Single sign-on with IdP guides (Okta, Microsoft Entra ID, Google Workspace, OneLogin, Ping) and parent organizations | Claude T/E; Console | admin, IdP | Set up SSO; verify domain | SC13132885; SC10276682; SC13917894; SC13917889; SC13917884; SC13917899; SC13917902; SC13443687 | pg 2026-10-13 | NOT_OBSERVED | VERIFIED SHIPPING | T/E/Console; Q: "available for Team plans, Enterprise plans, and Console organizations" | none | One IdP per parent org | SAML/SCIM via IdP | ADAPT | Enterprise sign-in | H | none |
| CL-E-045 | E | JIT provisioning (T/E/Console) and SCIM (E/Console only, via WorkOS); email-mismatch troubleshooting per IdP | Claude T/E; Console | admin, IdP | Set up provisioning | SC13133195; SC14499648; SC13917829; SC13917840; SC13917817; SC13917861; SC13917875 | pg 2026-10-15 | NOT_OBSERVED | VERIFIED SHIPPING | JIT T/E/Console; SCIM E/Console; Q: "SCIM provisioning is available for Enterprise and Console organizations only" | none | Email is primary identifier | SCIM | ADAPT | Lifecycle mgmt | H | none |
| CL-E-046 | E | Domain claiming and migration of personal accounts on verified domains into Enterprise | Claude Enterprise | admin; affected users | Claim domain; users respond | SC14625619; SC14625626; SC9267400 | pg 2026-09-02 | NOT_OBSERVED | VERIFIED SHIPPING | E only (incl. AWS Marketplace purchases) | Not into HIPAA or CMEK orgs | Personal work moves with account | n/a | DEFER | Shadow-IT consolidation | H | none |
| CL-E-047 | E | Audit logs (180-day export; auth, projects, membership, SSO, files, conversations; IDs only) | Claude Enterprise | admin | Organization settings > Data and Privacy | SC9970975 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | E | none | Link valid 24h; CMEK orgs use Compliance API | n/a | ADAPT | Auditability | H | Format |
| CL-E-048 | E | Compliance API (activity feed, chat data, file content, audit events) | Claude Enterprise / Platform | API | Primary Owner enables | SC13015708 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | E; Platform customers | Separate for Claude for Government | Org-level keys | Documented API | USE VIA OFFICIAL INTEGRATION | Compliance export | H | Endpoints not read |
| CL-E-049 | E | Compliance API partner integrations (DLP, SASE, data security, SIEM/SecOps, identity, eDiscovery, AI-SPM, observability) | Claude Enterprise / Platform | partner tools | Configure partner integration | SC15167101 | pg 2026-10-20 | NOT_OBSERVED | VERIFIED SHIPPING | E and Claude Platform; Q: "available to Claude Enterprise plans and Claude Platform customers" | none | Via Compliance API | Compliance API | USE VIA OFFICIAL INTEGRATION | SIEM/DLP coverage | H | Partner list long (12.6k-word page), reviewed at digest level |
| CL-E-050 | E | Custom data retention (min 30 days; chats, projects, artifacts; default indefinite) | Claude Enterprise | admin | Organization settings > Data and Privacy | SC10440198 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | E | none | Excludes standalone Design, Tag, Managed Agents, cloud Code; public-link artifacts not deleted | n/a | ADAPT | Data minimisation | H | none |
| CL-E-051 | E | Usage analytics dashboard and export; Analytics API (E) | Claude T/E | admin, API | Dashboard / API | SC12883420; RN | pg 2026-09-25; RN 2026-02-13 | NOT_OBSERVED | VERIFIED SHIPPING | T Owners; E Owners/Primary/Admins (Admins no Spend) | none | Seat-based E spend shows overage only | Analytics API | DEFER | Adoption | H | none |
| CL-E-052 | E | Analytics chat (ask Claude about org usage, default last 30 days) | Claude Enterprise | admin | Chat in analytics | SC14729354 | pg 2026-07-01 | NOT_OBSERVED | VERIFIED SHIPPING | E; Q: "Analytics chat is available on the Enterprise plan" | none | Same permissions as dashboard | n/a | ADAPT | Insight | H | none |
| CL-E-053 | E | Smart reports (team work, cost, friction, skill opportunities; 10 per month free; not for performance evaluation) | Claude Enterprise | admin | Capabilities toggle; run report | SC16893491; SC16948886 | RN 2026-09-10 | NOT_OBSERVED | BETA-PREVIEW | E | Not CMEK/HIPAA/hybrid | Privacy guardrails always on | n/a | DEFER | Adoption planning | H | none |
| CL-E-054 | E | Enterprise Admin API (spend limits and limit-increase requests; 60 req/min) | Claude Enterprise | API | Admin API key | SC15330651 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW (public beta) | E with usage credits | none | Scoped keys | Documented API | DEFER | Automation | H | none |
| CL-E-055 | E | Group spend limits and pooled group budgets | Claude Enterprise | admin | Organization settings > Groups | SC13799932; SC17005973 | pg 2026-09-25; pg 2026-10-07 | NOT_OBSERVED | VERIFIED SHIPPING (pooled budgets BETA) | E; Q: "Pooled group budgets are in beta for Enterprise plan organizations" | none | Org limit is ceiling | Admin API | DEFER | Cost control | H | none |
| CL-E-056 | E | Model access per org/role, effort caps, default model ("Always start new chats on the default model" beta) | Claude Enterprise | admin | Models page / role Models tab | SC15694740; SC15330088; SC13930458 | pg 2026-10-16 | NOT_OBSERVED | VERIFIED SHIPPING | E; Q: "Haiku models are always available to every member" | none | n/a | n/a | DEFER | Cost/compliance | H | RN 2026-07-01 labelled entitlements beta |
| CL-E-057 | E | Organization instructions (3,000 chars; override individual instructions; up to 1h to apply) | Claude T/E | admin | Owner sets | SC14546867 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | none | Owners only | n/a | ADAPT | Org-wide policy prompts | H | Whether applies in Cowork/Code |
| CL-E-058 | E | Organization surveys (in-product questions, aggregated results) | Claude Enterprise | admin | Admin console | SC16764057 | pg 2026-09-02 | NOT_OBSERVED | BETA-PREVIEW | E; Q: "Surveys are available in beta for Enterprise plans" | Not with CMEK | Aggregated | n/a | ADAPT | Feedback loop | H | none |
| CL-E-059 | E | Desktop deployment: MSIX (Intune, SCCM, Group Policy, PowerShell), macOS .pkg; non-admin installs lack desktop Cowork | Claude Desktop | managed devices | IT deploys | SC12622703; SC12611117; SC12622667; claude.com/download | pg 2026-10-13 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | macOS, Windows | n/a | n/a | DEFER | Fleet rollout | H | none |
| CL-E-060 | E | IP allowlisting | Claude Enterprise | admin | Configure ranges | SC13200993 | pg 2026-10-16 | NOT_OBSERVED | VERIFIED SHIPPING | E; Q: "IP allowlisting is available for Enterprise plans only" | none | n/a | n/a | DEFER | Network control | H | Exact surfaces restricted listed on page (not enumerated here) |
| CL-E-061 | E | Tenant Restrictions (proxy headers block personal accounts on corporate networks) | Claude Enterprise; Console | network | Proxy header overwrite | SC13198485 | pg 2026-10-16 | NOT_OBSERVED | VERIFIED SHIPPING | E and Console | none | n/a | n/a | DEFER | Block personal accounts | H | none |
| CL-E-062 | E | Customer-managed encryption keys (AWS KMS, Google Cloud KMS, Azure Key Vault) | Claude Enterprise / Platform | admin | Configure key | SC15505325 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | Eligible E; Platform | none | Key ops logged in customer cloud | Platform docs | DEFER | Key control | H | Feature limitations listed elsewhere |
| CL-E-063 | E | US-only inference (all apps; 1.1x pricing on newer models) | Claude Enterprise | admin | Organization settings > Data and privacy | SC15422948 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | Usage-based E only | US | Connectors not covered; storage separate | API data residency separate | DEFER | Residency | H | none |
| CL-E-064 | E | Inference hooks (org server allow/deny on prompts, tool calls, file text before Claude acts) | Claude Enterprise | server-side | Owner configures endpoint | SC16059458 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | E | none | Check runs in Claude infra; signed requests | Documented on platform.claude.com | ADAPT (pattern for WePLD policy hooks) | DLP, archival | H | none |
| CL-E-065 | E | HIPAA-ready Enterprise; BAA activation by Primary Owner; HIPAA configuration for local Claude Code and Cowork; Covered Models under BAA | Claude Enterprise | admin | Activate HIPAA, accept BAA | SC13296973; SC17318731; SC8114513; SC15455031 | pg 2026-10-20..23 | NOT_OBSERVED | RESTRICTED | E only; Q: "Standard Claude Enterprise plans do not include BAA coverage without action" | US HIPAA context | Many features off under HIPAA | n/a | DEFER | Regulated industries | H | none |
| CL-E-066 | E | Zero data retention (constraint referenced across features) | Claude Enterprise / Platform | n/a | Contractual | SC14661296; SC16951679; SC17444462 | acc 2026-10-27 | NOT_OBSERVED | RESTRICTED | Contracted orgs | none | ZDR disables several features | n/a | DEFER | Privacy | M | No dedicated ZDR article read |
| CL-E-067 | E | Project sharing controls (by role on E), user feedback settings, designated human-support contacts (E) | Claude T/E | admin | Admin settings | SC9927533; SC10504844; SC15263885 | pg 2026-09-24; 2026-03-16; 2026-08-06 | NOT_OBSERVED | VERIFIED SHIPPING | T/E (role-based and support contacts E) | none | Turning off public projects makes them private | n/a | DEFER | Governance | H | none |
| CL-E-068 | E | Organization data export (Primary Owner) and member self-export toggle | Claude T/E | admin | Organization settings > Data and privacy | SC13346720; SC9450526 | pg 2026-10-23 | NOT_OBSERVED | VERIFIED SHIPPING | T/E; Q: "only available to Team and Enterprise plan Primary Owners" | none | Member exports exclude uploaded files | Compliance API alternative | ADAPT | Portability | H | none |
| CL-E-069 | E | AI-generated content marking (text watermarks; C2PA Content Credentials on PNG/JPEG; Content Checker; watermark detection private preview) | Anthropic | all Claude apps, API, Code, Cowork, Tag | Automatic | SC16266773 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING (detection RESTRICTED) | All | EU AI Act Art. 50(2) code; new EU models from 2026-08-02 | n/a | Content Checker public | ADAPT (label WePLD outputs) | Transparency compliance | H | Supported model list |
| CL-E-071 | E | Self-serve Enterprise purchase; single seat type covering Claude, Code, Cowork; Team Standard/Premium seats | Claude | web | Buy on website | RN; claude.com/pricing | RN 2026-02-12 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | none | n/a | n/a | DEFER | Procurement | H | none |
| CL-E-072 | E | Claude for Education (university SSO setup, enforce-SSO effects, Canvas LTI, Primary Owner owns data) | Claude for Education | web, desktop, mobile, Canvas | Admin setup; LTI keys | SC11139094; SC11139144; SC11725453; SC11732894 | pg 2026-03-16..2026-10-13 | NOT_OBSERVED | VERIFIED SHIPPING | Education plans | Desktop macOS 13+/Win10+; iOS 18+; Android 8+ | Institution Primary Owner controls data | LTI | DEFER | Education market | H | none |
| CL-E-073 | E | Claude for Government support path (FedRAMP boundary; Org/Tenant Admins) | Claude for Government | gov deployments | Admin portal Support | SC13047024; SC13015708 | pg 2026-10-08 | NOT_OBSERVED | RESTRICTED | Gov contracts | US gov | Separate Compliance API | Separate | DEFER | Public sector | H | none |
| CL-E-074 | E | Programs via custom roles / workspaces (e.g. Cyber Verification Program grants, non-GA model access) | Claude Enterprise; Console | admin | Verification Portal; assign to role or workspace | SC17118092; SC16764810 | pg 2026-10-08; pg 2026-10-21 | NOT_OBSERVED | RESTRICTED | E; Console | none | Grants issued by Anthropic | n/a | DEFER | Gated capability rollout | H | none |
| CL-E-075 | E | Cyber Verification Program (reduced cyber classifiers; tiers covering Opus 5.5, Sonnet 5.5, Mythos 5.1) | Anthropic | API, Claude | Apply; review within ~7 business days | SC14604842; SC17202708 | pg 2026-10-26 | NOT_OBSERVED | RESTRICTED | Qualifying security professionals; some tiers need Enterprise Frontier Safeguards | none | Security requirements per access level | n/a | REJECT | Security research | H | none |
| CL-E-076 | E | Covered Models policy (Mythos-class): 30-day minimum retention; ZDR unavailable where Covered Models are accessed | Anthropic | all platforms incl. Bedrock, Google Cloud, Foundry | n/a | SC15425695; SC15425996 | pg 2026-09-01; pg 2026-10-19 | NOT_OBSERVED | VERIFIED SHIPPING | All; Q: "Prompts and model completions are retained for at least 30 days" | none | Consumer plans unaffected (already retained) | n/a | ADAPT (data-handling disclosure if WePLD uses Fable) | Compliance planning | H | none |
| CL-E-077 | E | Data roles: Team/Enterprise customer is Controller; Primary Owner manages member data; removed users' data handling | Claude T/E | n/a | n/a | SC9267385; SC9265372; SC12053672; SC9796617 | pg 2026-10-15; 2026-10-23 | NOT_OBSERVED | VERIFIED SHIPPING | T/E | none | Owners can request permanent deletion of removed users | n/a | ADAPT | Contracts | H | none |
| CL-E-078 | E | Invite links and organization discovery for Team/Enterprise | Claude T/E; Console | signup, admin | Share invite link; discover org at signup | SC13776697; SC13566435; SC14793921 | pg 2026-08-06; 2026-07-21 | NOT_OBSERVED | VERIFIED SHIPPING | T on by default; E off by default; unavailable with SSO | none | n/a | n/a | ADAPT | Low-friction onboarding | H | none |
| CL-E-079 | E | Team to Enterprise migration (keep org, data, roles) | Claude T/E | admin | Upgrade path | SC13779868 | pg 2026-10-07 | NOT_OBSERVED | VERIFIED SHIPPING | T to E | none | Data preserved | n/a | DEFER | Upgrade path | H | none |
| CL-E-080 | E | Claude for Intune (managed iOS app, Microsoft sign-in only) | Claude for Intune | iOS (Intune-managed) | Intune admin center | SC17203415; SC9266462 | pg 2026-10-14 | NOT_OBSERVED | VERIFIED SHIPPING | E; Entra admin consent | iOS | IT controls updates | n/a | DEFER | Mobile MDM | H | none |
| CL-E-081 | E | Claude Console: six roles (User, Claude Code User, Limited Developer, Developer, Billing, Admin), Workspaces, member invites, API key hygiene (rotate, revoke compromised keys), org deletion (restorable 7 days) | Claude Platform Console | web console | Console settings | SC10186004; SC9796807; SC13443764; SC13346458; SC13371040; SC9767949; SC8384961; SC10366376 | pg 2026-08-18..10-21 | NOT_OBSERVED | VERIFIED SHIPPING | Console orgs | none | Workspace-scoped limits | Admin API (not assessed) | USE VIA OFFICIAL INTEGRATION | If WePLD uses API | H | none |
| CL-E-082 | E | Console cost and usage reporting; API invoices; prepaid usage credits; ACH/invoicing for some | Claude Platform Console | web console | Usage page | SC9534590; SC16608069; SC8977456; SC9402418 | pg 2026-10-19 | NOT_OBSERVED | VERIFIED SHIPPING | Console (Developer, Billing, Admin see reports) | none | n/a | Usage/Cost API (not assessed) | USE VIA OFFICIAL INTEGRATION | Cost control | H | No prices recorded here |
| CL-E-083 | E | API rate-limit usage tiers (Start, Build, Scale; Custom) assigned automatically; Team-linked Console orgs at least Build | Claude Platform | API | Automatic | SC8243635; SC8114527; SC10366389 | pg 2026-10-07..13 | NOT_OBSERVED | VERIFIED SHIPPING | API | none | n/a | Public API | USE VIA OFFICIAL INTEGRATION | Capacity planning | H | Tier thresholds on platform docs |
| CL-E-084 | E | Console data retention: ZDR orgs can enable 30-day retention per Workspace (needed for Covered Models); Development Partner Program shares Claude Code tokens | Claude Platform Console | web console | Workspace setting; opt-in program | SC16824617; SC11174108 | pg 2026-10-19 | NOT_OBSERVED | VERIFIED SHIPPING | ZDR API orgs; opt-in program | none | Default: no training on commercial data | n/a | DEFER | Data governance | H | none |
| CL-E-085 | E | Messages API "preserved thinking" anti-distillation change (thinking blocks verified against original context; non-strict opt-in) | Claude Platform | API | Opt in to non-strict | SC16761192 | pg 2026-10-07 | NOT_OBSERVED | VERIFIED SHIPPING | Affected API accounts | none | n/a | Public API change | USE VIA OFFICIAL INTEGRATION (must handle) | API compatibility | H | Affected model list on page |
| CL-E-086 | E | Console Playground (replaced Workbench; no saved history or evals); prompt improver | Claude Platform Console | web console | Open Playground | SC8606378; SC8114533 | pg 2026-10-19 | NOT_OBSERVED | VERIFIED SHIPPING | Console | none | No saved prompt history | n/a | DEFER | Prompt iteration | H | none |
| CL-E-087 | E | Research credit programs: AI for Science, External Researcher Access | Anthropic | API | Apply via form | SC11199177; SC9125743 | pg 2026-03-16 | NOT_OBSERVED | RESTRICTED | Approved researchers | none | n/a | API credits | DEFER | Funding | H | none |
| CL-E-088 | E | Safeguards: warnings and appeals (banned consumer users can still export/delete), model safety bug bounty, public jailbreak reporting, CSAM reporting | Anthropic | all | Forms/appeals | SC8241253; SC12119250; SC11427875; SC9020328; SC12109679 | pg 2026-03-16..10-15 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | n/a | ADAPT (appeal/export-on-ban pattern) | Trust and safety | H | none |
| CL-E-089 | E | Policy guidance: Usage Policy for agents, guidelines for organizations serving minors, child safety, Usage Policy exceptions (gov, ASL-2), API safeguards tools | Anthropic | docs | Read | SC12005017; SC9307344; SC15591275; SC9528712; SC9199617 | pg 2026-03-16..09-14 | NOT_OBSERVED | VERIFIED SHIPPING | API builders | none | n/a | n/a | ADAPT (compliance requirements for WePLD on API) | Compliance | H | none |
| CL-E-090 | E | Site-owner controls: Anthropic crawler robots.txt opt-out; report/remove content from search outputs | Anthropic | web | robots.txt; report form | SC8896518; SC10684638; SC7996906 | pg 2026-04-07; 2026-09-03 | NOT_OBSERVED | VERIFIED SHIPPING | n/a | none | n/a | n/a | DEFER | Publisher control | H | none |
| CL-E-091 | E | Commercial privacy/legal: certifications list, DPA, BAA, government request policy, EU DSA contact, regulator contact, Australian DIS reporting, legal-work privilege guidance, output ownership | Anthropic | docs | Read | SC10015870; SC7996862; SC9519291; SC11595103; SC11174660; SC12335811; SC15707726; SC12326764 | pg 2026-03-16..10-15 | NOT_OBSERVED | VERIFIED SHIPPING | Commercial (T/E/API) and consumer as stated | EU, Australia specific items | Users own Outputs | n/a | DEFER | Procurement due diligence | H | Certification list content not enumerated |
| CL-E-092 | E | Anthropic Software Directory Policy and Terms (rules for submitting MCP servers, skills, plugins); Connectors Directory FAQ moved to developer docs | Anthropic directory | docs | Submit software | SC13145358; SC13145338; SC11596036 | pg 2026-10-24; 2026-03-16; 2026-08-06 | NOT_OBSERVED | VERIFIED SHIPPING | Developers | none | Submitter warrants rights | Submission process | USE VIA OFFICIAL INTEGRATION | Path to list WePLD connector | H | none |
| CL-E-093 | E | Microsoft 365 connector security: Anthropic-hosted, publisher-verified app, delegated permissions, no file caching; needs Entra tenant tied to Microsoft Business plan | Claude | web, desktop | Admin consent | SC12684923; SC12542951 | pg 2026-10-14..15 | NOT_OBSERVED | VERIFIED SHIPPING | All plans; Q: "available on all Claude plans: Free, Pro, Max, Team, and Enterprise" | Entra business tenant | On-demand retrieval only | Microsoft Graph | USE VIA OFFICIAL INTEGRATION | Office data | H | none |
| CL-E-094 | E | Seat management: Team Standard/Premium mix; Enterprise single seat (new plans); usage credits for Team and seat-based Enterprise | Claude T/E | admin | Organization settings > Billing | SC12004354; SC13393991; SC12005970; SC13133750 | pg 2026-10-13..16 | NOT_OBSERVED | VERIFIED SHIPPING | T/E; Owners/Primary Owners only for billing | none | n/a | Admin API (spend) | DEFER | Packaging benchmark | H | No prices recorded |
| CL-E-095 | E | Claude Enterprise consumption guide (managing usage across chat, Code, Cowork, Design, M365, Chrome, Slack) | Claude Enterprise | docs | Read | SC14782391 | pg 2026-10-13 | NOT_OBSERVED | VERIFIED SHIPPING | E | none | n/a | n/a | ADAPT (cost-governance playbook) | Cost control | M | Long article reviewed at digest level |
| CL-E-096 | E | Third-party tool authentication policy: products built for others must use API keys (Console or cloud provider), not subscription OAuth; spoofing or routing third-party traffic against subscription limits prohibited | Anthropic | all | Choose auth method | SC13189465; SC15036540 | pg 2026-10-15 | NOT_OBSERVED | VERIFIED SHIPPING | All plans; Q: "If you're building a product, application, or tool for others, use API key authentication" | none | Paid subscribers with usage credits may be allowed some third-party tools at Anthropic discretion | Claude API keys; cloud providers | USE VIA OFFICIAL INTEGRATION (API key only); REJECT subscription-OAuth routing | Avoid enforcement risk | H | Which third-party tools are allowed is discretionary |

### Family F - Distribution, platforms, plans, regions, models

| feature_id | family | exact_feature | source_product | platform_surface | user_flow (short) | official_evidence_url | evidence_date | observed_test | shipped_status | plan_gate | region_or_OS_gate | data_storage_and_permissions | access_to_source_or_public_API | WePLD_route | user_value | confidence | unknowns |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CL-F-001 | F | claude.ai web app | Claude | browsers | Sign in at claude.ai | claude.com/product/overview | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | Supported countries | Account | n/a | REIMPLEMENT FROM OBSERVED BEHAVIOR | Zero-install access | H | Supported browser list |
| CL-F-002 | F | Claude Desktop for macOS (universal DMG) | Claude Desktop | macOS 13+ | Download DMG | claude.com/download; SC10065433 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | Chat all; Code/Cowork paid | macOS 13 Ventura+ | Local app + account | n/a | ADAPT | Native app, local files | H | none |
| CL-F-003 | F | Claude Desktop for Windows (x64, arm64, Microsoft Store) | Claude Desktop | Windows 10+ | Installer or Store | claude.com/download; SC10065433 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | Chat all; Code/Cowork paid | Windows 10+ | Local + account | n/a | ADAPT | Native app | H | none |
| CL-F-004 | F | Claude Desktop for Linux (Ubuntu 22.04+/Debian 12+, x64/arm64, apt updates; no computer use, no dictation) | Claude Desktop | Linux | apt install per docs | claude.com/download; SC10065433 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | Chat all; Code/Cowork paid | Ubuntu/Debian only; Cowork needs KVM | Local + account | n/a | DEFER | Linux users | H | Other distros |
| CL-F-005 | F | Quick Entry (double-tap Option; screenshot/window capture; Caps Lock dictation) | Claude Desktop | macOS (Linux hotkey: X11, Wayland portal) | Hotkey | SC12626668; claude.com/download | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | macOS 12+ (dictation 14+); not Windows | n/a | n/a | ADAPT | Instant access | H | Download page implies Linux hotkey; article says macOS only |
| CL-F-006 | F | Claude for iOS (App Store) | Claude mobile | iOS | Install | SC9266462; claude.com/download | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | iOS | Account | n/a | DEFER | Mobile access | H | Minimum iOS version |
| CL-F-007 | F | Claude for Android (Google Play) | Claude mobile | Android | Install | SC9612887; claude.com/download (raw text lists Google Play) | pg 2026-07-09 | NOT_OBSERVED | VERIFIED SHIPPING | All | Unsupported regions/devices/Android versions may hide listing | Account | n/a | DEFER | Mobile access | H | Minimum Android version for app (widget needs 8.0) |
| CL-F-008 | F | Phone pairing via code or claude.ai/mobile | Claude | desktop to phone | Scan code | claude.com/download | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | All | none | n/a | n/a | ADAPT | Easy onboarding | M | none |
| CL-F-009 | F | In-app purchase of Pro on iOS/Android; app-store billing managed in store | Claude mobile | iOS, Android | Upgrade to Pro in settings | SC9266495; SC9612892; SC8325618 | pg 2026-03-16; 2026-10-07 | NOT_OBSERVED | VERIFIED SHIPPING | P | none | App-store billing | n/a | DEFER | Monetisation | H | none |
| CL-F-010 | F | Claude in Chrome distribution (Chrome Web Store; also connector inside Desktop) | Claude in Chrome | Chrome | Install extension | claude.com/download; SC12012173 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | P/M/T/E | Chrome only | Extension | n/a | DEFER | Browser agent | M | none |
| CL-F-011 | F | Office add-ins distribution (Microsoft Marketplace: Excel, PowerPoint, Word; Outlook beta) | Claude for Microsoft 365 | Office | Install add-in | claude.com/download | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING (Outlook beta) | Paid | none | n/a | n/a | USE VIA OFFICIAL INTEGRATION | Office users | H | none |
| CL-F-012 | F | Google Workspace Marketplace add-on | Claude for Google Workspace | Google Workspace | Install | claude.com/download; SC16951679 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | P/M/T/E | none | n/a | n/a | USE VIA OFFICIAL INTEGRATION | Google users | H | none |
| CL-F-013 | F | Slack app (Claude Tag; Claude Code in Slack) | Claude Tag | Slack | Install | claude.com/download; SC15594475 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | T/E | none | n/a | n/a | DEFER | Team chat | H | none |
| CL-F-014 | F | Claude Science downloads (Mac Apple Silicon/Intel, Windows x64, Linux x64) | Claude Science | desktop | Download | claude.com/download; SC16563838 | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | P/M/T/E | as listed | n/a | n/a | DEFER | Science users | H | none |
| CL-F-015 | F | Supported countries and regions (about 175); Team plan "certain supported locations"; API "a number of locations" | Claude | all | n/a | SC8461763; SC9266767; SC8116515 | pg 2026-03-16; 2026-10-16 | NOT_OBSERVED | VERIFIED SHIPPING | All | Listed countries only; Q: "currently available in certain supported locations" | n/a | n/a | DEFER | Market reach | H | Explicit exclusions not listed |
| CL-F-016 | F | Minimum age 18 (mobile app-store age signals) and phone verification from supported locations | Claude | mobile, web | Verification | SC13117299; SC8287232; SC15171100 | pg 2026-03-16; 2026-08-17 | NOT_OBSERVED | VERIFIED SHIPPING | All | US-state app-store age laws | n/a | n/a | ADAPT | Compliance | H | none |
| CL-F-017 | F | Plans and list prices (Free, Pro, Max 5x/20x, Team Standard/Premium 2-150 users, Enterprise seat + API-rate usage, 20-seat minimum) | Claude | web | claude.com/pricing | claude.com/pricing (raw text) | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | n/a; Q: "Price and plans are subject to change at Anthropic's discretion" | Prices exclude tax; vary by region | n/a | n/a | DEFER | Benchmark pricing | H | Regional pricing |
| CL-F-018 | F | Plan gate matrix (pricing comparison table): Free has no Opus, Research, Claude Code, Chrome, M365, Dashboards; Projects up to 5; Motion T/E only; Claude Security and inference hooks E only; consumer training opt-out | Claude | web | Compare plans | claude.com/pricing (raw text) | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | As listed; Q: "Projects Up to 5" (Free column) | none | n/a | n/a | DEFER | Packaging benchmark | H | Table may differ from Help Center for new features |
| CL-F-019 | F | Gift subscriptions: purchase currently unavailable; existing gifts redeemable, expire 365 days after purchase | Claude | web | Redeem gift | SC12938627; SC12938695 | pg 2026-10-06; 2026-03-16 | NOT_OBSERVED | NOT AVAILABLE (purchase) | P/M gifts; Q: "Gift subscriptions are currently unavailable to purchase" | none | n/a | n/a | DEFER | Growth | H | Return date |
| CL-F-020 | F | Claude in Amazon Bedrock (access via Bedrock console; AWS support; regions per AWS guide) | Amazon Bedrock | AWS | Request model access | SC7996920; SC10280791; SC7996921; SC7996918; SC10280783; SC10280779 | pg 2026-03-16 | NOT_OBSERVED | VERIFIED SHIPPING | AWS customers | AWS regions per Bedrock guide | AWS terms | Bedrock API | USE VIA OFFICIAL INTEGRATION | Procurement flexibility | H | Model/region matrix lives in AWS docs |
| CL-F-021 | F | Models lineup: Haiku 5.5 (2026-10-07), Sonnet 5.5 (2026-09-28), Opus 5.5 (2026-09-22), Fable 5.1 and Mythos 5.1 (2026-09-01), Opus 5, Sonnet 5, Fable 5 | Anthropic models | all | Model selector / API | SC12138966; claude.com/product/overview | RN dates as listed | NOT_OBSERVED | VERIFIED SHIPPING | Fable paid only | none | n/a | Claude API | USE VIA OFFICIAL INTEGRATION | Model choice for WePLD | H | Mythos consumer availability unclear |
| CL-F-022 | F | Fable models on plans (Max/premium seats up to 50% weekly limit; Pro/standard seats pay-as-you-go credits) | Claude | web, mobile, desktop, Cowork, Code, Design, M365, Tag | Select Fable | SC15424964 | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E (not Free) | Code 2.1.255+ for Fable 5.1 | n/a | API rates | DEFER | Frontier access | H | Mythos not covered on page |
| CL-F-023 | F | Claude Platform / API release notes (pointer) | Claude Platform | docs | Read | platform.claude.com/docs/en/release-notes/overview | acc 2026-10-27 | NOT_OBSERVED | VERIFIED SHIPPING | API | n/a | n/a | Public API | USE VIA OFFICIAL INTEGRATION (monitor) | Change tracking | H | Not read in depth |
| CL-F-024 | F | Claude Managed Agents (pointer; server-hosted agents with managed sandbox) | Claude Platform | API | API | SC14503520; platform.claude.com/docs/en/managed-agents/overview | acc 2026-10-27 | NOT_OBSERVED | BETA-PREVIEW | API; Max/Team API credits apply | none | Not covered by E custom retention | Public API (beta) | USE VIA OFFICIAL INTEGRATION | Hosted agent backend for WePLD | M | Pricing, limits not read |
| CL-F-025 | F | Claude apps release notes (Help Center, Aug 2025 - Oct 2026) | Claude | docs | Read | SC12138966 | latest entry RN 2026-10-21 | NOT_OBSERVED | VERIFIED SHIPPING | n/a | n/a | n/a | n/a | USE VIA OFFICIAL INTEGRATION (monitor) | Change tracking | H | Older history in developer docs |
| CL-F-026 | F | Haiku 4.5 leaves model selector 2026-10-29 (replaced by Haiku 5.5) | Claude | chat, Cowork, Design (F/P/M) | Automatic switch | SC17444146 | acc 2026-10-27 | NOT_OBSERVED | NOT AVAILABLE (from 2026-10-29) | F/P/M | none | Existing chats continue on Haiku 5.5 | API unaffected | DEFER | n/a | H | none |
| CL-F-027 | F | Claude in Microsoft Foundry (MACC-eligible; Python/TypeScript/C# SDKs with Entra auth) | Claude Platform | Azure | Deploy via Foundry | SC12864745 | pg 2026-05-08 | NOT_OBSERVED | VERIFIED SHIPPING (page says public preview for Haiku 4.5, Sonnet 4.5, Opus 4.1) | Azure customers | Azure regions | Provider terms | Foundry API | USE VIA OFFICIAL INTEGRATION | Azure procurement | M | Model list on page appears stale vs Covered Models page listing Foundry for Fable |
| CL-F-028 | F | Claude Team plan for scientists (discounted Team for academic/non-profit labs; Claude Science on by default; per-seat API credits) | Claude | web | Apply/sign up | SC16634237; SC16563838 | pg 2026-10-16 | NOT_OBSERVED | VERIFIED SHIPPING | Eligible research groups | none | n/a | API credits | DEFER | Vertical program | H | Eligibility checks |
| CL-F-029 | F | Claude for Teachers (free for verified US K-12 educators; school/district Enterprise org; K-12 terms) | Claude | web | Verify school email or district setup | SC16559896; SC15926041 | pg 2026-10-15; 2026-10-05 | NOT_OBSERVED | VERIFIED SHIPPING | Verified US K-12; Q: "sign up by June 30, 2027 get a full year of free access" | US | K-12 terms and DPA | n/a | DEFER | Vertical program | H | none |
| CL-F-030 | F | Billing gates: payments non-refundable except per terms; EEA/UK 14-day refund; cancellations at period end; tax/VAT IDs; Japan JCT | Claude | web | Settings > Billing | SC12386328; SC8325617; SC9889408; SC9927624; SC9889428; SC14051822; SC12997130 | pg 2026-03-16..10-07 | NOT_OBSERVED | VERIFIED SHIPPING | P/M/T/E/API | EEA/UK refunds; Japan tax | n/a | n/a | DEFER | Commercial terms benchmark | H | No prices recorded |
| CL-F-031 | F | Team plan requirements: business email, allowed domains, minimum two members; monthly to annual switch | Claude Team | web | Create Team plan | SC9267247; SC12083917; SC9267289; SC12997503; SC16607668; SC9267323 | pg 2026-10-07 | NOT_OBSERVED | VERIFIED SHIPPING | T; Q: "Team plans require a minimum of two members" | Certain supported locations | n/a | n/a | DEFER | Packaging benchmark | H | none |
| CL-F-032 | F | Enterprise billing model: seat fee for access plus usage at API rates; self-serve or sales-assisted; legacy seat types | Claude Enterprise | web | Buy online or via sales | SC9797531; SC11526368 | pg 2026-09-01; 2026-10-13 | NOT_OBSERVED | VERIFIED SHIPPING | E; Q: "the seat fee covers access only, and all usage is billed separately" | none | n/a | n/a | DEFER | Packaging benchmark | H | none |
| CL-F-033 | F | Pro and Max plan definitions (Pro excludes Console API usage; Max 5x/20x, priority access, early features; upgrades prorated) | Claude | web | Upgrade | SC8325606; SC8325609; SC10185996; SC11049741; SC11049752; SC16607638; SC9876003; SC8987223 | pg 2026-10-13 | NOT_OBSERVED | VERIFIED SHIPPING | P/M; Q: "The Pro plan does not include API usage through the Claude Console" | none | n/a | Console separate | DEFER | Packaging benchmark | H | none |
| CL-F-034 | F | Monthly API credits for Max and Team (pooled on Team, capped at $500; not Free/Pro/Enterprise; claim by linking Console) | Claude Platform | Console | Link Console org | SC17154008; SC8114531 | pg 2026-10-19 | NOT_OBSERVED | VERIFIED SHIPPING | M and T (incl. discounted Team); Q: "Free, Pro, and Enterprise plans aren't eligible" | none | Non-refundable | Claude API | USE VIA OFFICIAL INTEGRATION | Cheap prototyping on API | H | none |

## 2. Sources consulted

All accessed 2026-10-27. Full per-article status (364 Help Center articles) is in section 7 (Coverage proof).

### 2.1 Non-Help-Center official pages

- https://claude.com/product/overview (pass 1 WebFetch; pass 2 raw HTML text checked)
- https://claude.com/download (pass 1 WebFetch; pass 2 raw HTML text checked, including FAQ JSON)
- https://claude.com/pricing (pass 1 WebFetch; pass 2 raw HTML text of plan cards and both comparison tables read)
- https://claude.com/claude-for-microsoft-365 (pass 1 WebFetch)
- https://code.claude.com/docs/en/overview (pass 1 WebFetch, full markdown)
- Located via official-domain search only (not read): https://code.claude.com/docs/en/changelog ; https://code.claude.com/docs/en/changelog/rss.xml ; https://platform.claude.com/docs/en/release-notes/overview ; weekly digests such as https://code.claude.com/docs/en/whats-new/2026-w34

### 2.2 Help Center method (pass 2)

- The complete Help Center navigation tree (15 top-level collections, 35 subcollections, 364 articles) was extracted from the site's own embedded navigation data on 2026-10-27, so the list is the live tree rather than a hand-made list.
- All 364 article pages were downloaded and their article bodies extracted (all 364 parsed; 443,470 words in total). Each article carries its live "last updated" date, now used as `evidence_date` (shown as "pg yyyy-mm-dd").
- Read levels used in section 7:
  - **R1-WEBFETCH**: read in pass 1 via WebFetch (whole page processed, summarised by the fetch model); 91 articles. In pass 2, plan/retention/security gates for these were re-checked against the live extracted text and short quotes added where relevant.
  - **R2-FULLTEXT**: full live text read line by line in pass 2; 16 articles (all mandatory-collection articles not read in pass 1).
  - **R3-GATEDIGEST**: full live text fetched; opening sentences plus every sentence matching plan/availability/beta/retention/region/admin keywords reviewed, with targeted pattern searches where a row needed it; 257 articles. This is not a word-by-word read.

## 3. Discrepancies (product pages vs Help Center, and within Help Center)

Pass-2 status in brackets.

1. **Android on the download page** [RETRACTED]: pass 1 reported that claude.com/download omits Android. That was an error in the pass-1 summary: the raw download page text contains Google Play and Android links (5 and 12 occurrences), and the pricing page says "Chat on web, iOS, Android and Desktop".
2. **Projects plan gate** [RESOLVED]: the pricing page lists "Projects" in the Pro card, but its comparison table shows Free "Up to 5", which matches the Help Center (SC9519177: "Free users can create a maximum of five projects"). Remaining in-Help-Center inconsistency: SC10185728 calls project instructions paid-only while projects are open to Free.
3. **Cowork projects vs new projects** [OPEN]: SC14116274 says Cowork projects are not in Claude Code; SC9517075 says the new projects beta starts in Claude Code (claude.ai/code and desktop Code tab).
4. **Enterprise-managed connector auth** [CONFIRMED, verbatim]: SC11176164 says "Enterprise-managed auth is available in beta for Team and Enterprise plans"; SC15537633 says "This feature is generally available for Team and Enterprise plans".
5. **Skill and plugin scanning** [OPEN]: release notes (2026-08-06) say Enterprise beta; SC15927065 (pg 2026-10-21) carries no beta label.
6. **Model entitlements** [OPEN]: release notes (2026-07-01) say beta; SC15694740 and SC15330088 present model access without a beta label (only "Always start new chats on the default model" is marked beta).
7. **Office add-ins via gateways** [PARTLY RESOLVED]: SC14447276 confirms direct-provider deployments (Bedrock, Vertex AI, or a gateway) for Office agents; the Microsoft 365 product page does not mention gateways. Naming differs: "Vertex AI" (Help Center) vs "Gemini Enterprise Agent Platform" (product page) vs "Google Cloud Agent Platform" (Covered Models page).
8. **Quick Entry on Linux** [CONFIRMED]: download page FAQ (raw text) says the Quick Entry hotkey works on X11/Wayland portal; SC12626668 says Quick Entry is macOS-only (likely stale).
9. **Custom visuals on mobile** [OPEN]: SC13979539 says not rendered on iOS/Android; release notes (2026-03-25) say mobile renders interactive app visuals inline.
10. **Web search toggle** [EXPLAINED]: legacy UI still has the toggle (SC10684626); unified experience removed it (SC16761823).
11. **Cowork visual sharing** [OPEN, likely stale]: SC13979539 (pg 2026-04-22) says Cowork visuals cannot be shared because sessions run locally, but Cowork is cloud-first since 2026-10-06.
12. **Xcode model** [OPEN, likely stale]: SC12293051 names Sonnet 4.
13. **Claude in Chrome status** [RESOLVED]: SC12902428 states Claude in Chrome is available in Cowork and Claude Code, "and in beta in the Chrome browser".
14. **Computer use gate** [CONFIRMED]: product overview shows "Computer use (beta)" without noting that Team/Enterprise lack access (SC14128542: "Team and Enterprise plans don't have access to computer use at this time").
15. **Compliance API and Cowork** [EXPLAINED]: SC13015708 does not mention Cowork; SC13364135 and SC14479288 say Cowork is captured.
16. **Claude in Slack naming** [CONFIRMED]: download page lists Slack under Claude Code; Help Center says Claude in Slack became Claude Tag (SC15594475).
17. **Microsoft Foundry model list** [NEW]: SC12864745 (pg 2026-05-08) lists Haiku 4.5, Sonnet 4.5, Opus 4.1 in public preview, while the Covered Models page (pg 2026-09-01) lists Fable 5/5.1 as generally available on Microsoft Foundry.
18. **Claude Code security reviews audience** [NEW]: SC11932705 names "individual paid plans (Pro or Max)" for /security-review, while Claude Security (SC14661296) and Code Review (SC14233555) are Enterprise or Team/Enterprise products; it is unclear whether /security-review is available on Team/Enterprise seats.
19. **Motion plan gate** [CONFIRMED]: pricing comparison table shows Claude Motion "No" for Free, Pro and Max and "Yes" for Team/Enterprise, matching SC17454997.

## 4. Removed, renamed, legacy and preview-only items

- **Removed / closing**: "Only on your computer" Cowork option for Pro/Max (removed 2026-10-06); legacy chat artifact creation (since 2026-09-16); Cowork live-artifact creation (since 2026-08-19); Haiku 4.5 in model selector (2026-10-29); standalone Claude Design at claude.ai/design (closes 2026-12-14, then read-only); Opus 4 and 4.1 deprecated (2026-01-16); web search toggle, "Add from GitHub" and conversation branching absent in unified experience; Dispatch closed to new users; **gift subscription purchases currently unavailable** (SC12938627); **Console Workbench replaced by Playground** (SC8606378); Connectors Directory FAQ moved to developer docs (SC11596036).
- **Renamed**: Cowork "Global instructions" to "Instructions for Claude"; "Ask before acting" to Manual / "Manually approve"; "Act without asking" to Skip / "Skip all approvals"; "AI-powered artifacts" to "Artifacts that use Claude"; Claude Code routines to cloud scheduled tasks; Claude in Slack to Claude Tag (2026-08-03); Settings > Account/Memory to Settings > Your Claude; Settings > Reflect/Time and focus to Settings > Wellbeing; Research also via /deep-research; Microsoft Entra ID (formerly Azure AD) in IdP guides.
- **Suspended then restored**: Fable 5 and Mythos 5 (suspended 2026-06-12, restored 2026-07-01).
- **Beta / research preview / restricted (current)**: unified chat+Cowork (rolling out), Cowork on web/mobile, Cowork and Desktop on Linux, computer use (Pro/Max), Dispatch (existing users), Claude Duet (US waitlist), Claude Tag, Claude Science, Dashboards, Motion, design systems, custom visuals, voice mode, artifact email invites, Google Workspace add-on, Outlook add-in, Claude in Chrome (in Chrome browser), 1Password for Claude, Salesforce in Claude (approved orgs), Claude Security (Enterprise public beta), Claude Code Security Center, Managed Agents, JetBrains plugin, new projects (waitlist), smart reports, Enterprise Admin API, surveys, pooled group budgets, monthly recap, break reminders, health integrations (US, Pro/Max), watermark detection (private preview), identity verification (rolling out), custom-role Owner access, Enterprise project group sharing, mobile connector installs, **Mythos 5 / 5.1 (limited access, approved partners)**, Cyber Verification Program.

## 5. Resolution of pass-1 UNKNOWNs

| Item | Pass-2 finding | Evidence (live text, at most 15 words quoted) | Row |
|---|---|---|---|
| Styles | Referenced but undocumented: profile "custom styles" exist; Claude Code has output styles. No current Help Center article describes managing chat styles. | SC12260368: "profile information (custom styles, personal preferences, etc.)" | CL-A-043 (status VERIFIED SHIPPING, referenced only; confidence M) |
| Image generation | Not offered; Claude builds HTML/SVG diagrams and charts (beta) and analyses uploaded images. | SC9002504: "Claude doesn't generate photos or illustrations the way image-generation tools do." | CL-A-010 (NOT AVAILABLE for image generation) |
| Math rendering | Claude processes equations and calculations; advises verifying mission-critical results. No rendering (LaTeX) detail is published. | SC10366421: "complex or mission-critical calculations should be verified using specialized mathematical software" | CL-A-011 (VERIFIED SHIPPING; rendering detail still undocumented) |
| Mythos consumer availability | Not consumer-available. Mythos 5 and 5.1 are "Limited availability / Limited access (approved partners)"; Fable 5/5.1 are the generally available versions of the same underlying model with extra safeguards. Mythos 5.1 also reachable via Cyber Verification Program tiers; Claude Security scans use Mythos. | SC15425695: "Some Covered Models (such as Claude Mythos 5) are available only to approved partners" | CL-F-021, CL-E-075, CL-E-076, CL-D-016 |

## 6. Most important features for WePLD (planning view)

1. **Unified agentic conversation (CL-A-001, CL-C-001..006)**: one thread for quick answers and long cloud tasks, with plan, steer, sub-agents, parallel tasks and cross-device resume. Reimplement the pattern; back it with the official Agent SDK or Managed Agents (CL-D-014, CL-F-024).
2. **Permission and safety model (CL-C-011, CL-C-012, CL-C-042, CL-E-018, CL-E-038, CL-E-039)**: Manual / Auto (action screening) / Skip, per-tool Always/Needs approval/Blocked, admin ceilings, deletion protection, hard-blocked categories, read-vs-write risk framing.
3. **Open formats to match**: Agent Skills (CL-E-006; SKILL.md with name 64 chars and description 200 chars, zipped folder), remote MCP connectors (CL-E-016), MCP Apps (CL-E-020), MCPB desktop extensions (CL-E-031). Licences still to verify.
4. **Programming by demonstration (CL-C-050)**: "Record a skill" turns a screen recording into a reviewable skill; a differentiating pattern worth reimplementing.
5. **Artifacts family (CL-B-001..028, CL-B-056)**: private-by-default outputs, view/comment/edit sharing, AI-powered artifacts billed to the viewer, persistent storage, connectors inside artifacts, Docs with @Claude comments, design systems.
6. **Memory with isolation (CL-A-032..037)** and consumer privacy defaults (CL-A-076).
7. **Scheduling and hybrid execution (CL-C-013, CL-C-006, CL-C-025, CL-D-012)**.
8. **Distribution of WePLD into Claude**: list a connector/plugin via the developer portal under the Software Directory Policy and Terms (CL-E-013, CL-E-092); deep-link via claude:// (CL-A-069).
9. **API-side obligations if WePLD calls Claude**: preserved-thinking change (CL-E-085), Covered Models 30-day retention/no ZDR (CL-E-076), rate-limit tiers (CL-E-083), Usage Policy for agents (CL-E-089), monthly API credits for Max/Team (CL-F-034); and the third-party authentication policy: a product built for others must use API keys, never subscription OAuth (CL-E-096).
10. **Reject/avoid**: agentic payments (CL-C-046), cookie import (CL-C-018), health data (CL-A-064), Cyber Verification Program (CL-E-075); computer use deferred (CL-C-020).

## 7. Coverage proof

Live Help Center tree on 2026-10-27: 15 top-level collections, 35 subcollections with articles, 364 articles. Read levels: R1-WEBFETCH = 91, R2-FULLTEXT = 16, R3-GATEDIGEST = 257. Every article: fetched = yes.

### 7a. Recursive collection to article list (read status)

Legend: R1-WEBFETCH = read via WebFetch in pass 1 and gates re-checked on live text in pass 2; R2-FULLTEXT = full live text read in pass 2; R3-GATEDIGEST = full text fetched, opening and all gate-keyword sentences reviewed. "rows" = register rows citing the article. Mandatory collections are marked [MANDATORY].


**Claude (4078531)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 12138966 | Release notes | 2026-10-21 | 5715 | R1-WEBFETCH | 4 |

**Claude (4078531) > Get started with Claude (9811058)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 8114491 | Get started with Claude | 2026-09-16 | 800 | R3-GATEDIGEST | 2 |
| 7996845 | What are some things I can use Claude for? | 2026-03-16 | 398 | R3-GATEDIGEST | 0 |
| 8461763 | Where can I access Claude? | 2026-03-16 | 637 | R1-WEBFETCH | 1 |
| 8114494 | How up-to-date is Claude's training data? | 2026-10-07 | 359 | R3-GATEDIGEST | 1 |
| 8114487 | What interfaces can I use to access Claude? | 2026-08-06 | 39 | R3-GATEDIGEST | 0 |
| 8287232 | Verify your phone number | 2026-08-17 | 619 | R3-GATEDIGEST | 2 |
| 12938627 | How to gift a Claude subscription | 2026-10-06 | 327 | R3-GATEDIGEST | 1 |
| 12938695 | How to redeem a Claude gift subscription | 2026-03-16 | 423 | R3-GATEDIGEST | 1 |

**Claude (4078531) > Account management (9811145)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 13189465 | Log in to your Claude account | 2026-10-15 | 1174 | R3-GATEDIGEST | 1 |
| 9015913 | How to get support | 2026-10-08 | 2006 | R3-GATEDIGEST | 1 |
| 8452276 | How do I change the email address associated with my account? | 2026-03-16 | 368 | R3-GATEDIGEST | 1 |
| 8325621 | I would like to input sensitive data into my chats with Claude. Who can view my conversations? | 2026-05-22 | 524 | R3-GATEDIGEST | 1 |
| 10310342 | How do I log out of all active sessions? | 2026-10-24 | 531 | R3-GATEDIGEST | 1 |
| 9450526 | Export your Claude data | 2026-10-14 | 447 | R1-WEBFETCH | 2 |
| 9028421 | Delete your Claude account | 2026-08-19 | 496 | R3-GATEDIGEST | 1 |
| 11107691 | Why is a coupon or promotion not available for my account? | 2026-03-16 | 98 | R3-GATEDIGEST | 0 |
| 13124001 | Managing your active sessions | 2026-10-23 | 532 | R3-GATEDIGEST | 1 |
| 12997130 | Understanding your billing address and tax calculation | 2026-08-06 | 427 | R3-GATEDIGEST | 1 |
| 14051822 | Notice regarding consumption tax (JCT) for Japanese customers | 2026-03-16 | 288 | R3-GATEDIGEST | 1 |
| 13163631 | Configuring session security settings | 2026-10-15 | 549 | R3-GATEDIGEST | 1 |
| 13047024 | How to get support for Claude for Government | 2026-10-08 | 164 | R3-GATEDIGEST | 1 |
| 11408405 | Claude 4 Invite Contest | 2026-03-16 | 1082 | R3-GATEDIGEST | 0 |

**Claude (4078531) > Conversation management (18031977)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 8230524 | Delete or rename a conversation | 2026-08-10 | 673 | R3-GATEDIGEST | 1 |
| 10593882 | Share and unshare chats | 2026-06-15 | 482 | R3-GATEDIGEST | 1 |
| 16762496 | Share a chat with specific people | 2026-09-04 | 1136 | R1-WEBFETCH | 3 |
| 16762437 | Public links for shared chats | 2026-09-04 | 733 | R1-WEBFETCH | 1 |
| 11817273 | Use Claude’s chat search and memory to build on previous context | 2026-10-23 | 5276 | R1-WEBFETCH | 9 |
| 12123587 | Import and export your memory from Claude | 2026-10-23 | 1538 | R3-GATEDIGEST | 1 |
| 12260368 | Use incognito chats | 2026-09-30 | 850 | R1-WEBFETCH | 2 |
| 15363606 | Why Claude switched models in your conversation with Fable 5 or Fable 5.1 | 2026-09-28 | 1673 | R3-GATEDIGEST | 1 |
| 16049681 | Why Claude switched models in your conversation with Opus 5 or Opus 5.5 | 2026-09-24 | 1550 | R3-GATEDIGEST | 1 |
| 17161993 | Why Claude switched models in your conversation with Sonnet 5.5 | 2026-09-28 | 1393 | R3-GATEDIGEST | 1 |
| 17444146 | Claude Haiku 4.5 is leaving the model selector | 2026-10-15 | 279 | R1-WEBFETCH | 1 |

**Claude (4078531) > Features and capabilities (18031719)** [MANDATORY]

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 17153992 | What are artifacts and how do I use them? | 2026-10-23 | 3859 | R1-WEBFETCH | 18 |
| 9547008 | Share artifacts | 2026-09-23 | 2849 | R1-WEBFETCH | 7 |
| 17454700 | Get started with Claude Dashboards | 2026-10-08 | 654 | R1-WEBFETCH | 3 |
| 16923645 | Get started with Claude Docs | 2026-10-08 | 3201 | R1-WEBFETCH | 9 |
| 14604416 | Get started with Claude Design | 2026-10-23 | 3948 | R1-WEBFETCH | 1 |
| 14604397 | Set up your design system in Claude Design | 2026-10-26 | 1309 | R2-FULLTEXT | 1 |
| 17440474 | Move from standalone Claude Design to Claude | 2026-10-23 | 2885 | R2-FULLTEXT | 1 |
| 11095361 | When should I use web search, extended thinking, and research? | 2026-06-02 | 373 | R2-FULLTEXT | 2 |
| 10684626 | Enable and use web search | 2026-10-07 | 1464 | R1-WEBFETCH | 4 |
| 11088861 | Use research on Claude | 2026-10-14 | 453 | R1-WEBFETCH | 2 |
| 9002504 | Can Claude produce images? | 2026-03-16 | 86 | R2-FULLTEXT | 1 |
| 8241126 | Upload files to Claude | 2026-07-23 | 541 | R1-WEBFETCH | 3 |
| 12111783 | Create and edit files with Claude | 2026-10-23 | 2910 | R1-WEBFETCH | 6 |
| 10366421 | How does Claude handle mathematical equations and calculations? | 2026-03-16 | 23 | R2-FULLTEXT | 1 |
| 9517075 | What are projects? | 2026-10-14 | 1182 | R1-WEBFETCH | 5 |
| 11473015 | Retrieval augmented generation (RAG) for projects | 2026-09-10 | 646 | R2-FULLTEXT | 1 |
| 12512176 | What are skills? | 2026-09-22 | 810 | R1-WEBFETCH | 6 |
| 12512180 | Use skills in Claude | 2026-10-23 | 3445 | R2-FULLTEXT | 2 |
| 12512198 | How to create custom skills | 2026-10-15 | 2101 | R2-FULLTEXT | 2 |
| 13837440 | Use plugins in Claude | 2026-10-07 | 2993 | R1-WEBFETCH | 7 |
| 14328846 | Browse skills, connectors, and plugins in one directory | 2026-09-25 | 534 | R1-WEBFETCH | 2 |
| 12293051 | Use Claude in Xcode | 2026-05-19 | 284 | R1-WEBFETCH | 1 |
| 12864745 | Use Claude in Microsoft Foundry | 2026-05-08 | 185 | R2-FULLTEXT | 1 |
| 13641943 | Visual and interactive content | 2026-03-16 | 1079 | R1-WEBFETCH | 6 |
| 13979539 | Custom visuals in chat and Cowork | 2026-04-22 | 1028 | R1-WEBFETCH | 4 |
| 14503520 | Available beta and research preview features | 2026-10-16 | 374 | R1-WEBFETCH | 2 |
| 15672559 | See your monthly recap | 2026-10-23 | 1102 | R1-WEBFETCH | 1 |
| 16563838 | Get started with Claude Science | 2026-10-16 | 171 | R1-WEBFETCH | 3 |
| 16952186 | Use Salesforce in Claude | 2026-09-25 | 558 | R1-WEBFETCH | 1 |
| 16952184 | Set up Salesforce in Claude for your organization | 2026-09-25 | 705 | R2-FULLTEXT | 1 |
| 16951679 | Use Claude in Google Docs, Sheets, and Slides | 2026-10-13 | 4665 | R1-WEBFETCH | 4 |
| 17458093 | Claude Docs keyboard shortcuts | 2026-10-08 | 1750 | R2-FULLTEXT | 1 |
| 17457950 | Use artifacts with a keyboard or screen reader | 2026-10-08 | 2212 | R2-FULLTEXT | 3 |
| 17631495 | Get started with Claude Duet | 2026-10-23 | 2407 | R1-WEBFETCH | 3 |
| 17666484 | How to use Link by Stripe with Claude Duet | 2026-10-21 | 1031 | R2-FULLTEXT | 1 |
| 17666489 | How to use Shop Pay with Claude Duet | 2026-10-21 | 660 | R2-FULLTEXT | 1 |

**Claude (4078531) > Personalization and settings (18031818)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 10185728 | Understanding Claude's personalization features | 2026-10-23 | 594 | R1-WEBFETCH | 2 |
| 8887527 | Customizing your appearance settings | 2026-10-23 | 177 | R1-WEBFETCH | 1 |
| 10769299 | How to use Claude in your preferred language | 2026-10-23 | 200 | R3-GATEDIGEST | 1 |
| 8664678 | Change the model, effort, and thinking settings | 2026-10-07 | 1089 | R1-WEBFETCH | 3 |
| 15672868 | Set break reminders and quiet hours | 2026-10-23 | 451 | R1-WEBFETCH | 1 |

**Claude (4078531) > Troubleshooting (18032037)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 12466728 | Troubleshoot Claude error messages | 2026-10-15 | 786 | R3-GATEDIGEST | 0 |
| 8525154 | Claude is providing incorrect or misleading responses. What’s going on? | 2026-03-16 | 230 | R3-GATEDIGEST | 0 |
| 8241188 | Claude is producing links that don’t work and falsely claiming that it has sent emails or produced external documents. What’s going on? | 2026-03-16 | 49 | R3-GATEDIGEST | 0 |
| 12738598 | Adapt to new model personas after deprecations | 2026-07-10 | 785 | R3-GATEDIGEST | 0 |

**Claude (4078531) > Usage and limits (18031876)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 9797557 | Usage limit best practices | 2026-09-22 | 1678 | R3-GATEDIGEST | 0 |
| 11647753 | How do usage and length limits work? | 2026-10-13 | 1128 | R3-GATEDIGEST | 1 |
| 14246112 | Buy usage bundles | 2026-10-08 | 431 | R1-WEBFETCH | 1 |
| 15036540 | Use the Claude Agent SDK with your Claude plan | 2026-10-27 | 104 | R1-WEBFETCH | 2 |
| 15424964 | Claude Fable models on your plan | 2026-09-02 | 1360 | R1-WEBFETCH | 1 |
| 17007452 | What is a limit reset? | 2026-09-22 | 357 | R3-GATEDIGEST | 1 |

**Pro and Max plans (5953830) > General (9811201)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 8606394 | How large is the context window on paid Claude plans? | 2026-10-07 | 594 | R1-WEBFETCH | 2 |
| 8325618 | Paid plan billing FAQs | 2026-10-07 | 897 | R3-GATEDIGEST | 1 |
| 9402418 | Why was my card declined? | 2026-07-10 | 369 | R3-GATEDIGEST | 1 |
| 9889408 | Add or update your paid Claude account’s tax or VAT ID | 2026-08-06 | 427 | R3-GATEDIGEST | 1 |
| 11818288 | Why am I being asked to verify my payment method? | 2026-03-16 | 53 | R3-GATEDIGEST | 0 |
| 8325617 | Cancel your Pro or Max subscription | 2026-10-07 | 545 | R3-GATEDIGEST | 1 |
| 9519177 | How can I create and manage projects? | 2026-10-14 | 1910 | R3-GATEDIGEST | 1 |
| 12386328 | Request a refund for a paid Claude plan | 2026-10-07 | 969 | R3-GATEDIGEST | 1 |
| 12429409 | Manage usage credits for paid Claude plans | 2026-10-08 | 1520 | R3-GATEDIGEST | 1 |
| 16607638 | Understanding your Pro or Max plan invoices | 2026-10-07 | 872 | R3-GATEDIGEST | 1 |

**Pro and Max plans (5953830) > Pro plan (9811198)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 8325606 | What is the Pro plan? | 2026-10-13 | 690 | R3-GATEDIGEST | 1 |
| 8325609 | How do I sign up for the Pro plan? | 2026-08-06 | 506 | R3-GATEDIGEST | 1 |
| 10185996 | How to change your Pro plan from monthly to annual billing | 2026-03-16 | 274 | R3-GATEDIGEST | 1 |

**Pro and Max plans (5953830) > Max plan (12394590)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 11049741 | What is the Max plan? | 2026-10-13 | 1366 | R3-GATEDIGEST | 1 |
| 11049752 | How do I sign up for the Max plan? | 2026-10-13 | 475 | R3-GATEDIGEST | 1 |

**Team and Enterprise plans (9387370) > Plan overviews (18901829)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 9797531 | What is the Enterprise plan? | 2026-09-01 | 2015 | R3-GATEDIGEST | 1 |
| 9266767 | What is the Team plan? | 2026-10-16 | 1422 | R3-GATEDIGEST | 2 |
| 16634237 | Claude Team plan for scientists | 2026-10-16 | 974 | R3-GATEDIGEST | 1 |

**Team and Enterprise plans (9387370) > Get started (18901835)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 9267247 | Get started with the Team plan | 2026-10-07 | 1110 | R3-GATEDIGEST | 1 |
| 9267400 | Move your personal Claude account to a Team or Enterprise organization | 2026-10-07 | 2162 | R3-GATEDIGEST | 1 |
| 13566435 | Find and join a Team or Enterprise organization | 2026-07-21 | 1233 | R3-GATEDIGEST | 1 |
| 13779868 | Migrate your organization from Team to Enterprise | 2026-10-07 | 1543 | R3-GATEDIGEST | 1 |
| 13776697 | Join an organization via invite link | 2026-08-06 | 731 | R3-GATEDIGEST | 1 |
| 14625626 | Respond to an Enterprise domain claim on your Claude account | 2026-08-17 | 883 | R3-GATEDIGEST | 1 |
| 14128775 | Claude Code on Console to Enterprise migration | 2026-10-16 | 2876 | R3-GATEDIGEST | 1 |
| 16559896 | Set up Claude for Teachers for your school or district | 2026-10-15 | 865 | R3-GATEDIGEST | 1 |

**Team and Enterprise plans (9387370) > Billing (9811436)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 9267289 | How is my Team plan bill calculated? | 2026-10-07 | 562 | R3-GATEDIGEST | 1 |
| 12997503 | Team plan billing FAQs | 2026-10-07 | 758 | R3-GATEDIGEST | 1 |
| 12083917 | Change your Team plan from monthly to annual billing | 2026-08-06 | 186 | R3-GATEDIGEST | 1 |
| 9927624 | Add or update your Team plan's tax or VAT ID | 2026-03-16 | 379 | R3-GATEDIGEST | 1 |
| 9267323 | Cancel your organization's Team plan subscription | 2026-10-07 | 145 | R3-GATEDIGEST | 1 |
| 11526368 | How am I billed for my Enterprise plan? | 2026-10-13 | 2277 | R3-GATEDIGEST | 1 |
| 16607668 | Understanding your Team plan invoices | 2026-10-07 | 929 | R3-GATEDIGEST | 1 |

**Team and Enterprise plans (9387370) > Admin management (9811449)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 9267276 | Roles and permissions | 2026-10-15 | 443 | R1-WEBFETCH | 1 |
| 12004354 | Purchase and manage seats on Team plans | 2026-10-16 | 1736 | R3-GATEDIGEST | 1 |
| 13393991 | Purchase and manage seats on Enterprise plans | 2026-10-16 | 2428 | R3-GATEDIGEST | 1 |
| 13133750 | Manage members on Team and Enterprise plans | 2026-10-13 | 2068 | R3-GATEDIGEST | 1 |
| 14782391 | Claude Enterprise consumption guide | 2026-10-13 | 6325 | R3-GATEDIGEST | 1 |
| 12005970 | Manage usage credits for Team and seat-based Enterprise plans | 2026-09-04 | 1398 | R3-GATEDIGEST | 2 |
| 10504844 | Manage user feedback settings on Team and Enterprise plans | 2026-03-16 | 101 | R3-GATEDIGEST | 1 |
| 9927533 | Control project sharing for your organization | 2026-09-24 | 719 | R3-GATEDIGEST | 2 |
| 13837433 | Manage plugins for your organization | 2026-10-16 | 5815 | R3-GATEDIGEST | 1 |
| 13325567 | Account management FAQs | 2026-10-23 | 401 | R3-GATEDIGEST | 0 |
| 13799932 | Manage groups and group spend limits on Enterprise plans | 2026-09-25 | 2500 | R3-GATEDIGEST | 1 |
| 13930452 | Manage custom roles on Enterprise plans | 2026-10-27 | 5119 | R3-GATEDIGEST | 1 |
| 13930458 | Set up role-based permissions on Enterprise plans | 2026-10-20 | 7060 | R1-WEBFETCH | 3 |
| 14546867 | Set organization instructions | 2026-08-31 | 646 | R1-WEBFETCH | 1 |
| 14604406 | Claude Design admin guide for Team and Enterprise plans | 2026-10-22 | 1489 | R3-GATEDIGEST | 2 |
| 14625619 | Claim and migrate accounts on your domain | 2026-09-02 | 1714 | R3-GATEDIGEST | 1 |
| 15263885 | Designate support contacts for human support | 2026-08-06 | 470 | R3-GATEDIGEST | 2 |
| 15330651 | Claude Enterprise Admin API reference guide | 2026-06-24 | 3580 | R1-WEBFETCH | 1 |
| 15330088 | Set a default model for your organization | 2026-10-16 | 2221 | R3-GATEDIGEST | 1 |
| 15402193 | Restrict verified-domain connectors to your Enterprise | 2026-10-20 | 924 | R3-GATEDIGEST | 1 |
| 15694740 | Manage model access for your organization | 2026-10-16 | 1671 | R3-GATEDIGEST | 1 |
| 16764057 | Create surveys for your organization | 2026-09-02 | 1047 | R3-GATEDIGEST | 1 |
| 17005973 | Manage pooled group budgets on Enterprise plans | 2026-10-07 | 1399 | R3-GATEDIGEST | 1 |
| 17203415 | Set up Claude for Intune | 2026-10-14 | 1895 | R3-GATEDIGEST | 1 |
| 17118092 | Assign a program to custom roles on Enterprise plans | 2026-10-08 | 1075 | R3-GATEDIGEST | 1 |
| 17444462 | Set up and manage the new unified Claude experience for your Enterprise organization | 2026-10-23 | 4008 | R1-WEBFETCH | 5 |

**Team and Enterprise plans (9387370) > Analytics and usage (18901831)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 12883420 | View usage analytics for Team and Enterprise plans | 2026-09-25 | 2182 | R3-GATEDIGEST | 1 |
| 14447276 | Configure a custom OpenTelemetry collector for Office agents | 2026-08-05 | 2362 | R3-GATEDIGEST | 1 |
| 14729354 | Use analytics chat to ask Claude about usage | 2026-07-01 | 1168 | R3-GATEDIGEST | 1 |
| 16893491 | Get started with smart reports | 2026-10-20 | 2857 | R1-WEBFETCH | 1 |
| 16948886 | Let team members run smart reports for specific groups | 2026-09-29 | 1930 | R3-GATEDIGEST | 1 |

**Team and Enterprise plans (9387370) > Capabilities (9811414)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 9519189 | Manage project visibility and sharing | 2026-09-24 | 1737 | R3-GATEDIGEST | 1 |
| 12489464 | Use enterprise search | 2026-10-01 | 2670 | R1-WEBFETCH | 1 |
| 13663666 | Use visual and interactive content on Team and Enterprise plans | 2026-03-16 | 176 | R3-GATEDIGEST | 1 |
| 13119606 | Provision and manage skills for your organization | 2026-10-26 | 4050 | R3-GATEDIGEST | 1 |
| 15594475 | What is Claude Tag? | 2026-09-24 | 1555 | R1-WEBFETCH | 3 |
| 15927065 | Get started with skill and plugin scanning | 2026-10-21 | 1069 | R1-WEBFETCH | 1 |
| 16994751 | Artifacts admin guide for Team and Enterprise plans | 2026-10-23 | 2988 | R3-GATEDIGEST | 1 |
| 17454997 | Get started with Claude Motion | 2026-10-08 | 553 | R1-WEBFETCH | 2 |

**Team and Enterprise plans (9387370) > Security and compliance (10351014)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 9267385 | Does Anthropic Act as a Data Processor or Controller? | 2026-10-15 | 345 | R3-GATEDIGEST | 1 |
| 9796617 | Can you delete data that I sent via Team and Enterprise plans? | 2026-03-16 | 106 | R3-GATEDIGEST | 1 |
| 9267387 | How can I access the personal information that Anthropic has on my account? | 2026-03-16 | 11 | R3-GATEDIGEST | 0 |
| 12053672 | What happens to a user's data when they are removed from a Team or Enterprise organization? | 2026-10-23 | 733 | R3-GATEDIGEST | 1 |
| 13346720 | Export your organization's data | 2026-10-23 | 563 | R3-GATEDIGEST | 1 |
| 9265372 | Who owns and manages the data of my team? | 2026-03-16 | 307 | R3-GATEDIGEST | 1 |
| 13296973 | HIPAA-ready Enterprise plans | 2026-10-20 | 1244 | R3-GATEDIGEST | 1 |
| 17318731 | Use Claude Code (local mode) and Claude Cowork (local mode) on a HIPAA-ready Enterprise plan | 2026-10-20 | 3038 | R3-GATEDIGEST | 2 |
| 15425996 | Data retention practices for Covered Models | 2026-10-19 | 1385 | R3-GATEDIGEST | 1 |
| 10440198 | Configure custom data retention controls for Enterprise plans | 2026-10-27 | 1778 | R1-WEBFETCH | 1 |
| 15422948 | Enable US-only inference for your organization | 2026-06-15 | 563 | R1-WEBFETCH | 1 |
| 9970975 | Access audit logs | 2026-06-15 | 995 | R1-WEBFETCH | 1 |
| 13015708 | Access the Compliance API | 2026-10-16 | 285 | R1-WEBFETCH | 2 |
| 15167101 | Get started with Claude Compliance API integrations | 2026-10-20 | 12598 | R3-GATEDIGEST | 1 |
| 13200993 | Restrict access to Claude with IP allowlisting | 2026-10-16 | 359 | R3-GATEDIGEST | 1 |
| 13198485 | Enforce network-level access control with Tenant Restrictions | 2026-10-16 | 845 | R3-GATEDIGEST | 1 |
| 15505325 | What are customer-managed encryption keys (CMEK)? | 2026-06-15 | 126 | R1-WEBFETCH | 1 |
| 16059458 | Inference hooks overview | 2026-10-19 | 195 | R1-WEBFETCH | 1 |
| 14661296 | Use Claude Security | 2026-10-21 | 3418 | R1-WEBFETCH | 2 |

**Identity management (SSO, JIT, SCIM) (17270717)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 10276682 | Important considerations before enabling single sign-on (SSO) and JIT/SCIM provisioning | 2026-10-15 | 2201 | R3-GATEDIGEST | 1 |
| 13132885 | Set up single sign-on (SSO) | 2026-10-13 | 2415 | R3-GATEDIGEST | 1 |
| 13133195 | Set up JIT or SCIM provisioning | 2026-10-15 | 4180 | R3-GATEDIGEST | 1 |
| 13443687 | Switching to a different Identity Provider (IdP) | 2026-04-10 | 905 | R3-GATEDIGEST | 1 |
| 14499648 | How SCIM sync works for Enterprise organizations | 2026-09-02 | 1529 | R3-GATEDIGEST | 2 |

**Identity management (SSO, JIT, SCIM) (17270717) > Setup by identity provider (19039081)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 13917884 | Google Workspace SSO setup | 2026-08-06 | 778 | R3-GATEDIGEST | 1 |
| 13917889 | Microsoft Entra ID SSO setup | 2026-08-04 | 932 | R3-GATEDIGEST | 1 |
| 13917894 | Okta SSO setup | 2026-09-02 | 1099 | R3-GATEDIGEST | 1 |
| 13917899 | OneLogin SSO setup | 2026-08-06 | 795 | R3-GATEDIGEST | 1 |
| 13917902 | Ping Identity SSO setup | 2026-08-06 | 745 | R3-GATEDIGEST | 1 |

**Identity management (SSO, JIT, SCIM) (17270717) > Troubleshooting by identity provider (19039143)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 13917817 | Google Workspace SSO/SCIM email mismatch | 2026-03-24 | 1879 | R3-GATEDIGEST | 1 |
| 13917829 | Microsoft Entra ID SSO/SCIM email mismatch | 2026-03-24 | 1727 | R3-GATEDIGEST | 1 |
| 13917840 | Okta SSO/SCIM email mismatch | 2026-03-24 | 1782 | R3-GATEDIGEST | 1 |
| 13917861 | OneLogin SSO/SCIM email mismatch | 2026-03-24 | 1800 | R3-GATEDIGEST | 1 |
| 13917875 | Ping Identity SSO/SCIM email mismatch | 2026-03-24 | 1892 | R3-GATEDIGEST | 1 |

**Claude Cowork (19667525)** [MANDATORY]

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 13345190 | Get started with Claude Cowork | 2026-10-23 | 4287 | R1-WEBFETCH | 16 |
| 13364135 | Use Claude Cowork safely | 2026-10-23 | 3147 | R2-FULLTEXT | 2 |
| 15520349 | Use Claude Cowork on web, desktop, and mobile | 2026-10-23 | 2273 | R1-WEBFETCH | 9 |
| 13455879 | Use Claude Cowork on Team and Enterprise plans | 2026-10-23 | 2416 | R1-WEBFETCH | 4 |
| 16607400 | Use the built-in browser in Claude Cowork | 2026-10-23 | 1127 | R1-WEBFETCH | 3 |
| 16635803 | Set up browser use in Claude Cowork for Team and Enterprise plans | 2026-10-23 | 1094 | R2-FULLTEXT | 1 |
| 14729249 | Use live artifacts in Claude Cowork | 2026-10-23 | 503 | R1-WEBFETCH | 1 |
| 13854387 | Schedule recurring tasks in Claude Cowork | 2026-10-23 | 1314 | R1-WEBFETCH | 2 |
| 13947068 | Assign tasks from anywhere in Claude Cowork | 2026-10-23 | 1666 | R1-WEBFETCH | 2 |
| 14116274 | Organize your tasks with projects in Claude Cowork | 2026-10-23 | 1098 | R1-WEBFETCH | 3 |
| 14128542 | Let Claude use your computer in Cowork | 2026-10-23 | 1924 | R1-WEBFETCH | 3 |
| 14477985 | Monitor Claude Cowork activity with OpenTelemetry | 2026-10-23 | 1528 | R1-WEBFETCH | 2 |
| 14479288 | Claude Cowork architecture overview | 2026-10-23 | 1576 | R1-WEBFETCH | 8 |
| 16761823 | Claude Cowork and chat are one Claude | 2026-10-23 | 2145 | R1-WEBFETCH | 12 |

**Claude Code (14445694)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 11940350 | Claude Code model configuration | 2026-10-07 | 1105 | R3-GATEDIGEST | 1 |
| 11145838 | Use Claude Code with your Pro or Max plan | 2026-10-27 | 1946 | R3-GATEDIGEST | 1 |
| 11932705 | Automated Security Reviews in Claude Code | 2026-03-16 | 845 | R3-GATEDIGEST | 1 |
| 11845131 | Use Claude Code with your Team or Enterprise plan | 2026-10-27 | 1117 | R3-GATEDIGEST | 1 |
| 12157520 | Claude Code usage analytics | 2026-10-20 | 1122 | R3-GATEDIGEST | 1 |
| 12304248 | Manage API key environment variables in Claude Code | 2026-05-05 | 712 | R3-GATEDIGEST | 1 |
| 12386420 | Claude Code FAQ | 2026-10-15 | 1497 | R3-GATEDIGEST | 1 |
| 12618689 | Use Claude Code in the cloud | 2026-10-16 | 1992 | R1-WEBFETCH | 1 |
| 14233555 | Set up Code Review for Claude Code | 2026-10-20 | 2370 | R3-GATEDIGEST | 1 |
| 15924927 | Use Claude Code CLI with a screen reader | 2026-07-13 | 639 | R3-GATEDIGEST | 1 |

**Claude Code (14445694) > Launch guides (19407739)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 14552382 | Your first day in Claude Code | 2026-10-27 | 806 | R3-GATEDIGEST | 1 |
| 14552983 | Models, usage, and limits in Claude Code | 2026-09-22 | 1646 | R3-GATEDIGEST | 1 |
| 14552646 | Troubleshoot Claude Code installation and authentication | 2026-10-27 | 628 | R3-GATEDIGEST | 1 |
| 14553240 | Give Claude context: CLAUDE.md and better prompts | 2026-04-15 | 1379 | R3-GATEDIGEST | 1 |
| 14553413 | Claude Code cheatsheet | 2026-08-07 | 1048 | R3-GATEDIGEST | 1 |
| 14554922 | Claude Code user FAQ | 2026-10-27 | 2017 | R3-GATEDIGEST | 1 |
| 14554000 | Claude Code power user tips | 2026-10-16 | 3938 | R3-GATEDIGEST | 2 |
| 14553517 | Claude Code: Common developer use cases | 2026-10-27 | 1408 | R3-GATEDIGEST | 1 |
| 14555877 | Claude Code communications kit | 2026-09-22 | 3884 | R3-GATEDIGEST | 1 |
| 14555399 | Claude Code champion kit | 2026-04-15 | 2692 | R3-GATEDIGEST | 1 |

**Claude Desktop (16163169) > General (17879568)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 10065433 | Install Claude Desktop | 2026-10-23 | 1346 | R1-WEBFETCH | 3 |
| 12622703 | Deploy Claude Desktop for Windows | 2026-10-13 | 1292 | R3-GATEDIGEST | 1 |
| 12611117 | Deploy Claude Desktop for macOS | 2026-03-16 | 239 | R3-GATEDIGEST | 1 |
| 12622667 | Enterprise configuration for Claude Desktop | 2026-10-13 | 588 | R3-GATEDIGEST | 2 |
| 12626668 | Use quick entry with Claude Desktop on Mac | 2026-10-23 | 1385 | R1-WEBFETCH | 2 |
| 14729294 | Open Claude Desktop with a link | 2026-06-30 | 501 | R3-GATEDIGEST | 1 |

**Claude Desktop (16163169) > Desktop extensions (17879657)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 12592343 | Enabling and using the desktop extension allowlist | 2026-03-16 | 796 | R1-WEBFETCH | 1 |
| 12702546 | Deploying enterprise-grade MCP servers with desktop extensions | 2026-08-05 | 434 | R3-GATEDIGEST | 1 |
| 10949351 | Getting Started with Local MCP Servers on Claude Desktop | 2026-10-23 | 1469 | R1-WEBFETCH | 3 |

**Claude Mobile apps (9387080) > General (10788716)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 10065434 | Use dictation on Claude Mobile | 2026-07-23 | 430 | R1-WEBFETCH | 1 |
| 11101966 | Use voice mode | 2026-10-23 | 2091 | R1-WEBFETCH | 1 |
| 13117299 | Minimum age requirement access restriction | 2026-03-16 | 241 | R3-GATEDIGEST | 2 |
| 14898120 | Open the Claude mobile app with a link | 2026-05-06 | 249 | R3-GATEDIGEST | 1 |

**Claude Mobile apps (9387080) > Claude for iOS (9879000)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 9266462 | Install Claude for iOS | 2026-10-05 | 352 | R3-GATEDIGEST | 2 |
| 9266495 | How do I sign up for Claude Pro on the Claude app for iOS? | 2026-03-16 | 47 | R3-GATEDIGEST | 1 |
| 10263469 | Use Claude app intents, shortcuts, and widgets on iOS | 2026-07-09 | 1295 | R1-WEBFETCH | 1 |
| 10302511 | Access Claude for iOS on your Lock Screen, Control Center, and Action button | 2026-07-09 | 326 | R3-GATEDIGEST | 1 |
| 11825384 | How to update Claude for iOS | 2026-10-05 | 145 | R3-GATEDIGEST | 0 |
| 11869619 | Use Claude with iOS apps | 2026-08-25 | 3053 | R1-WEBFETCH | 2 |

**Claude Mobile apps (9387080) > Claude for Android (9879004)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 9612887 | Install Claude for Android | 2026-07-09 | 185 | R3-GATEDIGEST | 1 |
| 9612892 | How do I sign up for Claude Pro on Claude for Android? | 2026-03-16 | 47 | R3-GATEDIGEST | 1 |
| 10534883 | Use the Claude widget on Android | 2026-07-09 | 323 | R3-GATEDIGEST | 1 |
| 11825394 | How to update Claude for Android | 2026-03-16 | 97 | R3-GATEDIGEST | 0 |
| 11869629 | Use Claude with Android apps | 2026-08-25 | 3295 | R1-WEBFETCH | 2 |

**Claude API and Console (5370014) > Use the Claude API and Console (9811457)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 8114521 | How can I access the Claude API? | 2026-08-18 | 96 | R3-GATEDIGEST | 0 |
| 8116515 | Where is the Claude API supported? | 2026-03-16 | 20 | R3-GATEDIGEST | 1 |
| 13371040 | Log in to your Console account | 2026-08-18 | 755 | R3-GATEDIGEST | 1 |
| 8114531 | I created a Claude Console organization - how do I start using the Claude API? | 2026-10-07 | 140 | R3-GATEDIGEST | 1 |
| 8606378 | How do I use the playground? | 2026-10-19 | 859 | R3-GATEDIGEST | 1 |
| 9534590 | Cost and usage reporting in the Claude Console | 2026-10-19 | 872 | R3-GATEDIGEST | 1 |
| 9796807 | Create and manage Workspaces in the Claude Console | 2026-10-21 | 1783 | R3-GATEDIGEST | 1 |
| 9876003 | I have a paid Claude subscription (Pro, Max, Team, or Enterprise plans). Why is Claude API usage billed separately from my paid Claude plan? | 2026-10-07 | 210 | R3-GATEDIGEST | 1 |
| 10186004 | Claude Console roles and permissions | 2026-08-18 | 597 | R3-GATEDIGEST | 1 |
| 10504853 | Manage user feedback settings on Claude Console | 2026-10-19 | 104 | R3-GATEDIGEST | 0 |
| 11174108 | About the Development Partner Program | 2026-10-19 | 675 | R3-GATEDIGEST | 1 |
| 11199177 | Anthropic's AI for Science Program | 2026-03-16 | 1109 | R3-GATEDIGEST | 1 |
| 13346458 | Customize your Console appearance settings | 2026-10-19 | 42 | R3-GATEDIGEST | 1 |
| 13443764 | Invite members to the Claude Console | 2026-10-19 | 298 | R3-GATEDIGEST | 1 |
| 14793921 | Find and join a Console organization | 2026-10-19 | 712 | R3-GATEDIGEST | 1 |
| 16764810 | Assign a program to workspaces in Claude Console | 2026-10-21 | 1446 | R3-GATEDIGEST | 1 |
| 16824617 | Turn on data retention for a Workspace in a zero data retention organization | 2026-10-19 | 870 | R3-GATEDIGEST | 1 |

**Claude API and Console (5370014) > Claude API usage and best practices (9811458)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 8243635 | Our approach to rate limits for the Claude API | 2026-10-13 | 194 | R3-GATEDIGEST | 1 |
| 8241216 | I’m planning to launch a product using the Claude API. What steps should I take to ensure I’m not violating Anthropic’s Usage Policy? | 2026-03-16 | 226 | R3-GATEDIGEST | 0 |
| 8384961 | What should I do if I suspect my API key has been compromised? | 2026-10-19 | 111 | R3-GATEDIGEST | 1 |
| 8114533 | I’ve been using other large language models (LLMs) to power my product. How should I alter my prompts when switching to Claude? | 2026-03-16 | 22 | R3-GATEDIGEST | 1 |
| 9767949 | API key best practices: keep your keys safe and secure | 2026-10-19 | 1683 | R3-GATEDIGEST | 1 |
| 10366389 | How can I get higher rate limits on the Claude API? | 2026-10-07 | 134 | R3-GATEDIGEST | 1 |

**Claude API and Console (5370014) > Pricing and billing (9811459)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 8977456 | How do I pay for my Claude API usage? | 2026-10-19 | 786 | R3-GATEDIGEST | 1 |
| 8114523 | How can I learn more about Claude API pricing? | 2026-03-16 | 10 | R3-GATEDIGEST | 0 |
| 9889428 | Add or update your Claude Console organization's tax or VAT ID | 2026-10-19 | 256 | R3-GATEDIGEST | 1 |
| 16608069 | Understanding your Claude API invoices | 2026-10-19 | 644 | R3-GATEDIGEST | 1 |
| 17154008 | Monthly API credits for Max and Team plans | 2026-10-19 | 1663 | R3-GATEDIGEST | 1 |

**Claude API and Console (5370014) > API troubleshooting (9811460)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 8114490 | Where can I find your API documentation? | 2026-03-16 | 12 | R3-GATEDIGEST | 0 |
| 8114527 | I’m encountering 429 errors, and I’m worried my rate limit is too low. What should I do? | 2026-10-19 | 97 | R3-GATEDIGEST | 1 |
| 8114535 | Where can I go for Claude API support and assistance? | 2026-03-16 | 99 | R3-GATEDIGEST | 0 |
| 10366432 | I'm getting an API connection error. How can I fix it? | 2026-03-16 | 146 | R3-GATEDIGEST | 0 |
| 13403291 | How can I check connectivity to the Claude API? | 2026-03-16 | 175 | R3-GATEDIGEST | 0 |

**Claude API and Console (5370014) > API FAQ (9811463)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 8987223 | Can I have a Claude account and a Console account? | 2026-10-07 | 86 | R3-GATEDIGEST | 1 |
| 8987200 | Can I use the Claude API for individual use? | 2026-03-16 | 38 | R3-GATEDIGEST | 0 |
| 9125743 | What is the External Researcher Access Program? | 2026-03-16 | 2030 | R3-GATEDIGEST | 1 |
| 10366376 | How can I delete my Claude Console account? | 2026-10-19 | 462 | R3-GATEDIGEST | 1 |

**Claude API and Console (5370014) > API prompt design (4078533)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 7996853 | Introduction to prompt design | 2026-03-16 | 69 | R3-GATEDIGEST | 0 |
| 8114518 | Claude’s response to my prompt is too brief. | 2026-03-16 | 50 | R3-GATEDIGEST | 0 |
| 7996857 | My prompt isn’t giving me a helpful answer. | 2026-03-16 | 139 | R3-GATEDIGEST | 0 |

**Claude API and Console (5370014) > API and distillation (19737224)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 16761192 | Preserved thinking: changing how the Messages API handles thinking blocks to protect against distillation | 2026-10-07 | 1145 | R3-GATEDIGEST | 1 |

**Connectors (15399129) > General (17879426)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 11176164 | Use connectors to extend Claude's capabilities | 2026-10-16 | 2719 | R1-WEBFETCH | 8 |
| 11725091 | When to use desktop and web connectors | 2026-10-23 | 441 | R3-GATEDIGEST | 1 |
| 13730515 | Manage Claude’s tool access | 2026-03-16 | 705 | R1-WEBFETCH | 1 |
| 11596036 | Anthropic Connectors Directory FAQ | 2026-08-06 | 24 | R3-GATEDIGEST | 2 |
| 13145358 | Anthropic Software Directory Policy | 2026-10-24 | 1164 | R3-GATEDIGEST | 1 |
| 13145338 | Anthropic Software Directory Terms | 2026-03-16 | 638 | R3-GATEDIGEST | 1 |
| 14730684 | How Claude suggests connected apps | 2026-04-23 | 465 | R1-WEBFETCH | 1 |
| 15537633 | Authorize MCP connectors for your entire organization | 2026-08-24 | 1239 | R1-WEBFETCH | 1 |

**Connectors (15399129) > Pre-Built Connectors (17879307)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 10166901 | Use Google Workspace connectors | 2026-10-23 | 3189 | R1-WEBFETCH | 2 |
| 10167454 | Use the GitHub integration | 2026-10-20 | 1492 | R1-WEBFETCH | 1 |
| 15183774 | Connect to Microsoft 365 | 2026-09-08 | 2680 | R1-WEBFETCH | 1 |
| 12542951 | Set up the Microsoft 365 connector | 2026-10-14 | 4410 | R3-GATEDIGEST | 2 |
| 12684923 | Microsoft 365 connector security guide | 2026-10-15 | 4175 | R3-GATEDIGEST | 2 |
| 13454812 | Use interactive connectors in Claude | 2026-10-23 | 986 | R1-WEBFETCH | 1 |
| 15936181 | Get started with 1Password for Claude | 2026-07-16 | 832 | R1-WEBFETCH | 1 |

**Connectors (15399129) > Custom Connectors (17879441)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 11175166 | Get started with custom connectors using remote MCP | 2026-10-01 | 2652 | R1-WEBFETCH | 4 |

**Claude in Chrome (18031491)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 12012173 | Get started with Claude in Chrome | 2026-10-23 | 2378 | R1-WEBFETCH | 5 |
| 12902446 | Claude in Chrome permissions guide | 2026-10-23 | 1454 | R1-WEBFETCH | 3 |
| 12902428 | Use Claude in Chrome safely | 2026-10-05 | 1867 | R3-GATEDIGEST | 1 |
| 13065128 | Claude in Chrome admin controls | 2026-10-23 | 1666 | R1-WEBFETCH | 2 |
| 12902405 | Claude in Chrome troubleshooting | 2026-10-23 | 1019 | R3-GATEDIGEST | 1 |

**Claude for Education (12630177)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 11139094 | Get started with Claude for Education at your university (for Owners/Admins) | 2026-08-06 | 801 | R3-GATEDIGEST | 1 |
| 11139144 | Use Claude for Education at your university | 2026-10-13 | 1239 | R3-GATEDIGEST | 1 |
| 11725453 | Set up the Claude LTI in Canvas by Instructure | 2026-03-16 | 619 | R3-GATEDIGEST | 1 |
| 11732894 | Who owns and manages the data of my Claude for Education account? | 2026-03-16 | 388 | R3-GATEDIGEST | 1 |

**Privacy and legal (4078534)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 10035659 | Where can I learn more about Anthropic's Privacy practices? | 2026-03-16 | 23 | R3-GATEDIGEST | 0 |
| 8114513 | Business Associate Agreements (BAA) for Commercial Customers | 2026-10-23 | 4288 | R3-GATEDIGEST | 1 |
| 10015870 | What Certifications has Anthropic obtained? | 2026-03-16 | 117 | R3-GATEDIGEST | 1 |
| 9519291 | What is Anthropic’s policy for handling governmental requests for user information? | 2026-03-16 | 314 | R3-GATEDIGEST | 1 |
| 9205721 | Why am I receiving an 'Output blocked by content filtering policy' error? | 2026-03-16 | 173 | R3-GATEDIGEST | 0 |
| 10023646 | I think a user is infringing my copyright or other intellectual property. How do I report it? | 2026-03-16 | 325 | R3-GATEDIGEST | 0 |
| 7996862 | How do I view and sign your Data Processing Addendum (DPA)? | 2026-03-16 | 91 | R3-GATEDIGEST | 1 |
| 10023638 | Why am I receiving an 'Output blocked by content filtering policy' error? | 2026-03-16 | 173 | R3-GATEDIGEST | 0 |
| 9301722 | Updates to our Acceptable Use Policy (now “Usage Policy”), Consumer Terms of Service, and Privacy Policy | 2026-03-16 | 654 | R3-GATEDIGEST | 0 |
| 9264813 | Consumer Terms of Service Updates | 2026-03-16 | 135 | R3-GATEDIGEST | 0 |
| 9190861 | Terms of Service Updates | 2026-03-16 | 288 | R3-GATEDIGEST | 0 |
| 10416553 | Official Anthropic marketing email addresses | 2026-08-24 | 85 | R3-GATEDIGEST | 0 |
| 10684638 | Report, block, and remove content from Claude | 2026-09-03 | 542 | R3-GATEDIGEST | 1 |
| 8896518 | Does Anthropic crawl data from the web, and how can site owners block the crawler? | 2026-04-07 | 653 | R3-GATEDIGEST | 1 |
| 11174660 | Point of Contact for Authorities and Regulators | 2026-10-15 | 74 | R3-GATEDIGEST | 1 |
| 11140763 | Claude 4 Invite Sweepstakes Official Rules | 2026-03-16 | 1131 | R3-GATEDIGEST | 0 |
| 11595103 | Designated point of contact for users in the EU | 2026-05-26 | 143 | R3-GATEDIGEST | 1 |
| 12326764 | Can I use my Outputs to train an AI model? | 2026-03-16 | 398 | R3-GATEDIGEST | 1 |
| 12335811 | Report a concern: Australian DIS Standard compliance | 2026-08-06 | 342 | R3-GATEDIGEST | 1 |
| 13704655 | Unauthorized Anthropic stock sales and investment scams | 2026-06-29 | 804 | R3-GATEDIGEST | 0 |
| 15425695 | Covered Models | 2026-09-01 | 1088 | R3-GATEDIGEST | 1 |
| 15455031 | Covered Models under a Business Associate Agreement (BAA) | 2026-10-19 | 1834 | R3-GATEDIGEST | 1 |
| 15707726 | Using Claude for Legal Work: Privilege, Confidentiality, and How to Think About Configuration | 2026-08-26 | 1606 | R3-GATEDIGEST | 1 |
| 15926041 | Claude for Teachers: your data and our terms | 2026-10-05 | 1381 | R3-GATEDIGEST | 1 |
| 16266773 | How Claude marks AI-generated content | 2026-10-21 | 1976 | R1-WEBFETCH | 1 |

**Safeguards (4078535)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 8106465 | Our Approach to User Safety | 2026-03-16 | 324 | R3-GATEDIGEST | 0 |
| 9528712 | Exceptions to our Usage Policy | 2026-03-16 | 317 | R3-GATEDIGEST | 1 |
| 8241253 | Safeguards warnings and appeals | 2026-10-15 | 403 | R3-GATEDIGEST | 1 |
| 9199617 | API Safeguards Tools | 2026-09-14 | 721 | R3-GATEDIGEST | 1 |
| 9035075 | Law Enforcement Requests | 2026-03-16 | 194 | R3-GATEDIGEST | 0 |
| 9307344 | Responsible Use of Anthropic's Models: Guidelines for Organizations Serving Minors | 2026-03-16 | 398 | R3-GATEDIGEST | 1 |
| 7996906 | Report, block, and remove content from Claude | 2026-09-04 | 542 | R3-GATEDIGEST | 1 |
| 9020328 | CSAM Detection and Reporting | 2026-03-16 | 178 | R3-GATEDIGEST | 1 |
| 11427875 | Public Vulnerability Reporting | 2026-03-16 | 108 | R3-GATEDIGEST | 1 |
| 12005017 | Using Agents According to Our Usage Policy | 2026-03-16 | 580 | R3-GATEDIGEST | 1 |
| 12109679 | Creating a new account after deletion | 2026-03-16 | 79 | R3-GATEDIGEST | 1 |
| 12119250 | Model Safety Bug Bounty Program | 2026-09-08 | 742 | R3-GATEDIGEST | 1 |
| 13171706 | Crisis Helpline Support in Claude | 2026-10-24 | 2202 | R3-GATEDIGEST | 1 |
| 14328960 | Identity verification on Claude | 2026-08-11 | 1117 | R3-GATEDIGEST | 1 |
| 14604842 | Cyber Verification Program | 2026-10-26 | 3854 | R3-GATEDIGEST | 1 |
| 15171100 | Age assurance on Claude | 2026-05-18 | 338 | R3-GATEDIGEST | 2 |
| 15591275 | Child safety guidance for developers | 2026-06-26 | 853 | R3-GATEDIGEST | 1 |
| 17202708 | Cyber Verification Program Security Requirements | 2026-10-06 | 5245 | R3-GATEDIGEST | 1 |

**Amazon Bedrock (4078537)**

| article_id | title | page_updated | words | read_status | rows |
|---|---|---|---|---|---|
| 7996918 | What is Amazon Bedrock? | 2026-03-16 | 138 | R3-GATEDIGEST | 1 |
| 7996920 | How do I get access to Claude in Amazon Bedrock? | 2026-03-16 | 32 | R3-GATEDIGEST | 1 |
| 7996921 | I use Claude in Amazon Bedrock. Who do I contact for customer support inquiries? | 2026-03-16 | 109 | R3-GATEDIGEST | 1 |
| 10280779 | How do I learn more about Amazon and Anthropic’s strategic collaboration? | 2026-03-16 | 7 | R3-GATEDIGEST | 1 |
| 10280783 | Where do I find Claude in Amazon Bedrock documentation? | 2026-03-16 | 8 | R3-GATEDIGEST | 1 |
| 10280791 | What AWS Regions are Claude models available in Amazon Bedrock? | 2026-03-16 | 20 | R3-GATEDIGEST | 1 |

### 7b. Source to feature coverage map

Counts of register rows citing at least one article in each top-level collection, by shipped_status of the row (a row citing several collections is counted in each). "Articles cited" = articles in that collection referenced by at least one row.

| source (top-level collection) | articles | articles cited | rows | VERIFIED SHIPPING | BETA-PREVIEW | RESTRICTED | NOT AVAILABLE | UNKNOWN |
|---|---|---|---|---|---|---|---|---|
| Claude (4078531) | 85 | 76 | 147 | 120 | 16 | 7 | 4 | 0 |
| Pro and Max plans (5953830) | 15 | 14 | 8 | 8 | 0 | 0 | 0 | 0 |
| Team and Enterprise plans (9387370) | 76 | 74 | 66 | 52 | 9 | 5 | 0 | 0 |
| Identity management (SSO, JIT, SCIM) (17270717) | 15 | 15 | 3 | 3 | 0 | 0 | 0 | 0 |
| Claude Cowork (19667525) | 14 | 14 | 53 | 44 | 6 | 2 | 1 | 0 |
| Claude Code (14445694) | 20 | 20 | 10 | 10 | 0 | 0 | 0 | 0 |
| Claude Desktop (16163169) | 9 | 9 | 12 | 11 | 1 | 0 | 0 | 0 |
| Claude Mobile apps (9387080) | 15 | 13 | 15 | 13 | 2 | 0 | 0 | 0 |
| Claude API and Console (5370014) | 41 | 29 | 13 | 11 | 0 | 2 | 0 | 0 |
| Connectors (15399129) | 16 | 16 | 21 | 20 | 1 | 0 | 0 | 0 |
| Claude in Chrome (18031491) | 5 | 5 | 10 | 6 | 4 | 0 | 0 | 0 |
| Claude for Education (12630177) | 4 | 4 | 1 | 1 | 0 | 0 | 0 | 0 |
| Privacy and legal (4078534) | 25 | 15 | 6 | 5 | 0 | 1 | 0 | 0 |
| Safeguards (4078535) | 18 | 16 | 8 | 6 | 1 | 1 | 0 | 0 |
| Amazon Bedrock (4078537) | 6 | 6 | 1 | 1 | 0 | 0 | 0 | 0 |
| Non-Help-Center official pages and release notes | n/a | n/a | 52 | 40 | 10 | 2 | 0 | 0 |
| **All register rows (deduplicated)** | 364 | 326 | 339 | 280 | 41 | 13 | 5 | 0 |

Articles read but not cited by any row (38): judged not to describe a distinct user/admin-facing feature or gate (promotions, generic troubleshooting, prompt tips, marketing addresses, superseded terms notices, duplicates). IDs: 7996845, 8114487, 11107691, 11408405, 12466728, 8525154, 8241188, 12738598, 9797557, 11818288, 13325567, 9267387, 11825384, 11825394, 8114521, 10504853, 8241216, 8114523, 8114490, 8114535, 10366432, 13403291, 8987200, 7996853, 8114518, 7996857, 10035659, 9205721, 10023646, 10023638, 9301722, 9264813, 9190861, 10416553, 11140763, 13704655, 8106465, 9035075.

### 7c. Residual gaps and verdict

**COVERAGE_COMPLETE** (scope: the mandatory discovery sources).

Basis for the verdict:
- Mandatory collection "Features and capabilities" (18031719): 36 of 36 articles read (22 R1-WEBFETCH, 14 R2-FULLTEXT). In the live navigation tree this collection has no subcollections of its own; the 15 collections shown on its page are the site-wide top-level collections, all of which were enumerated and fetched (section 7a).
- Mandatory collection "Claude Cowork" (19667525): 14 of 14 articles read (12 R1-WEBFETCH, 2 R2-FULLTEXT), including SC15520349.
- Mandatory pages: claude.com/product/overview and claude.com/download read (pass 1) and raw-text checked (pass 2); apps release notes SC12138966 read; Claude Code changelog and Platform release-notes pointers recorded.
- All 364 Help Center articles in all 15 top-level collections (incl. API and Console, Safeguards, Amazon Bedrock, Plan overviews, Billing, IdP setup and troubleshooting subcollections) were fetched in full; none failed to parse.
- Register: 339 rows (A 78, B 57, C 50, D 25, E 95, F 34), unique IDs, 18 columns each.

Residual gaps (do not block the verdict above, but limit depth):
1. 257 non-mandatory articles are at R3-GATEDIGEST level (full text fetched; opening and gate sentences reviewed; not read word by word). Longest examples: SC15167101 Compliance API integrations (12.6k words), SC14782391 consumption guide, SC13837433 plugin admin, SC13930452 custom roles, SC17202708 CVP requirements, SC12542951/SC12684923 Microsoft 365 setup and security.
2. Pass-1 R1 articles were read through a summarising fetch tool; their gate rows were re-checked against live text in pass 2, but non-gate details remain summary-derived.
3. Non-Help-Center depth: platform.claude.com (API features, Managed Agents, Compliance/Analytics/Admin API references, CMEK limits, inference-hook spec), code.claude.com beyond the overview, and the changelogs were not read. Claude Code CLI and Claude Design depth are owned by R03C and R03B.
4. Undocumented details: chat "custom styles" management, LaTeX/math rendering, exact usage quotas, Free-plan model list beyond the pricing table, sandbox resource caps, developer-portal URL.
5. No hands-on observation: every row remains NOT_OBSERVED; "VERIFIED SHIPPING" means documented as available on 2026-10-27.
6. Open discrepancies listed in section 3 (items 3, 5, 6, 9, 11, 12, 17, 18) need confirmation from Anthropic or by testing.

