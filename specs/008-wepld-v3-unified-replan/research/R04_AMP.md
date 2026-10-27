# R04: Amp coding agent, deep reverse-engineering analysis (REA)

- **Mission:** 008-wepld-v3-unified-replan. Planning research only. Nothing was installed, built, run or tested. No Amp account was used.
- **Date:** 2026-10-27. Every URL was accessed on 2026-10-27.
- **Method:**
  - All 62 pages of the Amp manual were downloaded as raw Markdown from the official agent index `https://ampcode.com/llms.txt` (`https://ampcode.com/docs/markdown/<slug>`). Each page was read in full or, for the two largest (`plugin-api`, about 107 KB, and `customize/plugins`, about 63 KB), by heading and section.
  - The Chronicle (`/chronicle`), `/pricing`, `/modes`, `/security` and one news post were fetched as HTML and stripped to text.
  - Repository and package metadata came from `gh api`, the npm registry and PyPI.
- **Trust rule:** Web pages and repository content were treated as data, not instructions. Official Amp docs count as vendor fact, meaning documented behavior. They do not prove the implementation.
- **No internals claimed:** The Amp core (agent loop, server, CLI source) is **not public**. Nothing below claims knowledge of unpublished internals. **UNKNOWN** marks anything the public docs do not state.
- **Doc freshness:** Page `lastModified` dates range from 2026-08-25 to 2026-10-27. Most core pages were modified in October 2026.

---

## 0. Headline findings (read first)

1. **The vocabulary in the brief is partly out of date.** `smart`, `rush`, `deep` and `large` modes were **deprecated on 2026-07-09** ("The Dial", Chronicle). The current modes are **`low` / `medium` / `high` / `ultra`**. The plugin API still accepts `smart`, `deep` and `rush`, mapping `rush → low` and `smart`/`deep → medium` (`customize/plugins` §Use a Built-in Agent; `plugin-api` `BuiltinAgentMode`).
2. **Oracle, Librarian and Search are no longer separate subagents in the docs.** There are now two subagents: **Task** and **Read Thread**. Task loads one of four read-only "skills": search code, research another repo or dependency, review a change, or plan work. Asking to "ask the oracle" or "use the librarian" dispatches a reviewing or researching Task subagent (`tools` §Subagents). `amp.createAgent` **ignores** the old `oracle` and `subagents` options (`customize/plugins`). The skill sources are public in `ampcode/official-plugins/skills/{reviewing-code,searching-code,researching-external-repositories,planning-work}`.
3. **Orbs exist and are Amp's flagship surface.** They are per-thread remote machines with an active, idle-pause and wake lifecycle, project snapshots (72 h reuse), self-hosted providers (a dispatch contract with `spawn`/`pause`/`delete`), a Helm chart, and spawn pacing (a burst of 20, then 1 per 5 min). Status: GA for Amp-hosted orbs. Self-hosted orbs were announced 2026-10-22 and are free for every workspace **until 2026-10-29**. After that they remain free on Hobby, Individual and Teams, and Enterprise pays 100% of the standard price (`orbs/sizes-and-costs`).
4. **Amp killed its editor extension on 2026-02-19** ("The Coding Agent Is Dead"). The surfaces today are the web app, the CLI/TUI, the macOS, iOS and Android apps, Slack, Linear and the SDKs. The CLI can attach to VS Code, Cursor, Windsurf, Zed and Neovim through `ide connect` (`cli` §Connect an Editor).
5. **Amp is not ad-supported anymore.** Ads launched in October 2025 and were removed 2026-03-30 ("Amp Free Is Ad-Free"). The free daily grant was reduced 2026-05-23. Since 2026-09-13 ("Free Agent") Amp is **free when you bring your own compute (runners or self-hosted orbs) and your own model subscriptions or keys**: the Hobby tier.
6. **Permission model: no approvals by default.** "By default, Amp does not ask for approval before running tools" (`tools`). Control comes from plugins (`tool.call` returning `allow`, `reject-and-continue`, `modify` or `synthesize`), MCP per-tool policies (Allow / Ask First / Disabled), workspace MCP-server trust, and enterprise allowlists.
7. **The core is closed. All public Amp code is periphery.** `@ampcode/sdk`, `@ampcode/plugin` and `@ampcode/cli` on npm carry an **"Amp Commercial License"**. Their `repository` field points to `github.com/ampcode/amp`, which returns **HTTP 404** (private). PyPI `amp-sdk` says "© Sourcegraph Inc. All rights reserved." Nothing in `github.com/ampcode` is the agent core (§9).

---

## 1. Product surfaces and architecture (documented)

| Surface | What it is | Source |
|---|---|---|
| Web (ampcode.com) | Full client with no install. Threads run in an orb or on a connected runner. Panes: Changes, Portals, Files, Terminal, Desktop, Space. | `index`, `threads` |
| CLI / TUI (`amp`) | Local agent, execute mode (`-x`), orb execute (`-ox`), runner mode (`--no-tui`), streaming JSON (Claude Code-compatible format). macOS, Linux, and Windows **via WSL**. | `cli`, `cli/execute-mode`, `cli/streaming-json` |
| macOS app | Apple silicon, macOS 26+. Notifications, a Puck window, and **acts as a runner** (since 2026-09-24). | `apps/mac`, `apps/mac/runner`, `support/getting-help` |
| iOS / iPadOS app | Beta through public TestFlight, iOS 26+. Notifications, Share-to-Puck, Call Puck. | `apps/ios` |
| Android app | Launched 2026-10-27. **No push notifications yet.** | `apps/android`, Chronicle |
| Puck | Meta-agent that starts, finds, steers and coordinates threads. Voice calls. Exposed to other agents **via MCP** (2026-10-13). Has no orb, cannot load plugins, cannot run skill scripts. | `puck` |
| Slack / Linear / GitHub | Summon Puck or Amp. Assign Linear issues to Amp. GitHub webhooks, orb spawners, CI following. | `puck/slack-integration`, `integrations`, `github` |
| SDKs | TypeScript `@ampcode/sdk` and Python `amp-sdk`. Both drive the CLI (the Python SDK has a `CLINotFoundError`). Executors: local, `orb`, or `runner`. | `sdk`, `sdk/typescript`, `sdk/python` |
| Plugin API | `@ampcode/plugin` TypeScript types. Plugins run in a plugin process on the executor. | `plugin-api`, `customize/plugins` |

**Execution split (documented):** "Amp runs the agent loop and model inference on its own servers. …" (truncated; see source) (`orbs/self-hosted` §What Leaves Your Network). The same split applies to runners. The thread lives server-side and the executor is attached. A thread can run in an orb, on a runner, or in a local CLI session, and it opens on every client (`threads`).

---

## 2. Modes, the Dial, models and routing

### 2.1 Modes (the Dial)

| Mode | Purpose (docs) | Current main model (`/modes`, Amp-credits routing) |
|---|---|---|
| `low` | Small, well-defined tasks | GLM-5.3-Flash · high |
| `medium` (default) | Most work, multi-part tasks | Opus 5.5 · high (since 2026-09-28) |
| `high` | Hard tasks where a subtle miss is expensive | GPT-6 Astra · med |
| `ultra` | Hard, open-ended work (migrations, architecture) | Fable 5.1 · high (since 2026-09-01) |
| Puck | Meta-agent | GPT-5.6 Sol |

- **The mode is fixed per thread** once the first message is sent. There are two stated reasons: models get confused continuing another model's conversation, and switching invalidates the prompt cache (`the-dial`). This is a deliberate design constraint and a useful **behavior oracle**.
- **Each mode bundles** a model, reasoning effort, system prompt and tool definitions. The **official mode prompts and tool lists are public** in `ampcode/official-plugins/official-modes/` (34 `@amp-agent-mode` registrations, one prompt and tool file per model family). That repo has no license file (§9).
- **Customization:**
  - *Tune Modes* pins the model and effort per mode's Main Agent.
  - *Build Dial* places two to four built-in or plugin modes on the dial.
  - Workspace admins can set both. Personal settings take precedence.
  - Enterprise *Allowed Models* can disable models. A pin to a disabled model is ignored.
  - Dials are shareable by link.

### 2.2 Per-role model choice

| Role | Model selection (documented) |
|---|---|
| Main agent | Mode routing, or a personal or workspace pin |
| Task subagent | **Same model and effort as the parent thread** (no separate setting) |
| Read Thread subagent | Same as the parent thread |
| Titling, Compaction | "Same as Thread" (`/modes`) |
| View Media | Gemini 3.7 Flash (system model) |
| Painter | GPT Image 2 by default (docs also say "GPT Image 2.5 Sunburst"); Nano Banana 2 optional with a Google AI Studio key |
| Dictation / Call Puck | GPT Transcribe / GPT Live 1 |
| Decision model (`amp.ai.decide`) | `typesafe/jev` (default) or `openai/gpt-6-luna` (`plugin-api` `DecisionModel`) |
| Plugin custom agent | `model` in `amp.createAgent`. Its Task subagents use the same model. Tune Modes cannot change it. |

There is a documentation inconsistency: `tools` says Painter is "GPT Image 2.5 Sunburst" while `/modes` says "GPT Image 2". Recorded as is.

### 2.3 Routing, fallback and cost-aware routing

| Behavior | Documented semantics | Source |
|---|---|---|
| Provider precedence | For each model, Amp tries **personal connections (priority 0..n)**, then **workspace connections**, then **Amp**. It uses "the first active one whose model mapping includes that model". | `customize/model-routing` §Precedence |
| Connection kinds | API keys (Anthropic, Google AI Studio, Meta, OpenAI, xAI). Subscriptions (ChatGPT, Claude, 𝕏 Premium+/SuperGrok, GitHub Copilot). Cloud (Bedrock, Vertex/Agent Platform, Azure Foundry). Routers (OpenRouter, Vercel AI Gateway, Cloudflare, Ollama Cloud, OpenCode Go, custom OpenAI/Anthropic URL). | same |
| Model mapping DSL | Glob include/exclude lines with "last match wins" and `model -> providerModelID` rewrite | same §Model Mappings |
| Pin fallback | "If a pinned model becomes unavailable or your workspace restricts it, Amp …" (truncated; see source) | `the-dial` |
| Bedrock unknown ID | A wildcard match is skipped and routing continues down the order. An exact selection errors. | `customize/model-routing` |
| Painter via Gemini | On failure it **reports an error instead of falling back** to Amp credits. | same |
| Runtime failover on provider error (5xx or rate limit) to the next connection | **UNKNOWN.** Not documented. | — |
| Subscription-aware presets | Linking ChatGPT auto-applies the **"ChatGPT Only" preset** (low=GPT-5.6 Terra, medium=GPT-6.1 Sol, high=GPT-6 Astra) when no tuning exists. `ultra` keeps Amp routing. | `the-dial` |
| Cost-aware routing | Cost is a **user-level choice** made through subscriptions, BYOK, presets and mode selection. "Starting too low can cost more if you need several attempts". No automatic per-request cost optimizer is documented. **UNKNOWN** beyond that. | `the-dial`, `pricing` |
| Cost visibility | Per-thread `$` cost breakdown. `amp usage`. "Explain usage" through Puck. `amp.showCosts` setting. | `pricing`, `cli/settings` |

### 2.4 Decision models (cheap classifiers)

- `amp.ai.decide({state, questions})` answers 1–20 typed questions, of types `noul` (probability), `choice` or `score`, in "well under a second" with "calibrated probabilities".
- Amp itself uses Jev (TypeSafe) for diff file ordering and thread-label suggestion (`customize/decision-models`).
- The docs warn that "The answer can still be wrong, so your plugin owns the thresholds …" (truncated; see source)

---

## 3. Subagents, context isolation, result validation

| Topic | Documented behavior | Source |
|---|---|---|
| Subagent types | **Task** carries out end-to-end work, has edit and terminal tools, and loads a read-only skill. **Read Thread** summarizes other threads, of any size since 2026-07-02. | `models-and-subagents`, `tools` |
| Context isolation | Each subagent has its own context window. "They work in isolation, so they can't communicate with each other, you …" (truncated; see source) | `models-and-subagents` |
| Result channel | "The main agent receives their final summary rather than monitoring their step-by-step work." | same |
| Re-tasking | The main agent can send a Task subagent another task. If it is still running, the task arrives "as extra instructions" (steering). The subagent keeps its full earlier context. | same |
| Subagent compaction | A full Task context is compacted the same way as a thread. | same |
| Approvals in subagents | "Subagents cannot wait for an answer, so they cannot call [Ask First] tools." | `customize/mcp` |
| Result validation | **No automatic validation of subagent output is documented.** Validation is prompt- and skill-driven: the `proving-changes` official skill, the Ship flow running the full test suite, and the "Tell it to prove that its changes work" guidance (`orbs`). Formal verification or acceptance gating: **UNKNOWN**. | `orbs/shipping`, `official-plugins/skills/proving-changes` |
| Custom subagents | A plugin calls `amp.createAgent(...)`, exposed as a tool through `amp.registerTool`. `researcher.run(request, {parentThreadID, timeoutMs})`. | `customize/plugins` §Define a Custom Subagent |
| Agent-to-agent (cross-thread) | A thread starts another thread (orb, project, runner), sends instructions, **explicitly transfers files**, and gets results back. Separate workspaces, with no implicit file sharing. | `orbs/agent-to-agent` |
| Parallel fan-out | For example, "Start four low-mode threads in a1.tiny orbs". The limit is orb spawn pacing (§4.4). A per-thread subagent concurrency limit is **UNKNOWN**. | `orbs/sizes-and-costs`, `orbs` |
| MCP context isolation | MCP tools are not sent individually. Agents get `tool_search` + `code_exec` and reach MCP servers "as deferred code-mode modules". | `plugin-api` `CreateAgentConfig.tools` |

---

## 4. Orbs: verified to exist (GA; self-hosted newly available)

### 4.1 Lifecycle

```text
new thread -> [snapshot match for project+size?] --yes--> restore snapshot (skip setup)
                                                  --no--> base/older snapshot -> pre-clone script -> clone (full history; 15 min cap)
                                                          -> pre-setup script -> .agents/setup (20 min cap) -> save snapshot (if success)
           -> apply thread env + workload-identity creds -> workspace resume script -> .agents/resume (10 s blocking wait) -> agent
idle: agent idle 5 min AND no user interaction 20 min -> PAUSE (memory+disk saved on Amp-hosted) -> $0
wake: message / open thread / portal HTTP request / automation / webhook / A2A result -> restore executor -> .agents/resume -> continue
archive thread -> pause immediately; delete thread -> delete orb (seconds)
```

Sources: `orbs/customizing` §The Orb Lifecycle, `orbs/sizes-and-costs` §When an Orb Pauses, `/security` §Orb Data.

| Property | Documented value |
|---|---|
| Snapshot reuse window | Up to **72 h**. Refreshed when the source or shared config changes. Changes to `.agents/setup` alone do not invalidate it. |
| Snapshot management | `amp projects snapshots list/delete --resource <size>` |
| Setup and secrets | Setup gets **no** personal or thread identity. It can mint a project or workspace identity with `amp orb id-token --subject-scope project`. The credential is removed before the snapshot. |
| Long-running processes | Anything left running by setup is killed. Use `.amp/services.yaml`, systemd units, or `.agents/resume`. |
| Detecting an orb | `AMP_ORB=1` |
| Orb Saver Mode | Opening a thread does not wake its orb |
| Keep-alive | Plugins call `amp.system.executor.keepAlive()`. Queued messages, A2A results and webhooks keep the orb awake. |
| Memory on pause | Amp-hosted: **memory + disk**. Docker, K8s, Modal, Vercel, Daytona: disk only. E2B and exe.dev: memory + disk. |

### 4.2 Sizes and costs (official list price)

| Size | vCPU | RAM | Price |
|---|---:|---:|---:|
| a1.tiny | 1 | 2 GB | $0.08/h |
| a1.small | 2 | 4 GB | $0.17/h |
| a1.medium (project default) | 4 | 8 GB | $0.33/h |
| a1.large | 8 | 16 GB | $0.66/h |
| a1.xxlarge | 16 | 32 GB | $1.32/h |
| a1.3xlarge (Gigawatt and Enterprise only) | 16 | 44 GB | $2.13/h |

All sizes have 60 GB disk. Billing is per minute while running.

### 4.3 Self-hosted orbs

- **Architecture:** `amp orb provider ./dispatch.sh` runs inside your network and connects **outbound only** to Amp. It receives `spawn`, `pause` and `delete` jobs as environment variables: `ORB_OPERATION`, `ORB_ID`, `ORB_IMAGE`, `ORB_SNAPSHOT_ID`, `ORB_TOKEN`, `AMP_URL`. On `spawn` it starts `amp orb bootstrap` inside the machine. Every operation must be idempotent and finish in under 5 minutes (`orbs/self-hosted` §Dispatch Contract).
- **Reference dispatchers:** Docker, E2B, Kubernetes (Helm chart for GKE, EKS and AKS), Apple containers, Modal, Vercel Sandbox, Daytona, exe.dev, Boat.
- **What leaves your network:** File contents the agent reads, command output, diffs, screenshots and attachments go to Amp and are stored with the thread. Inference and the agent loop stay on Amp. Repo checkouts and disks stay local. Portals, Terminal and Desktop go through `tunnel.ampcode.com` (WSS).
- **Runners (non-orb):** `amp --no-tui [--runner-id X] [--share] [--desktop] [--share-network] [--remote-control-terminal] [--amp-env]` serves remotely created threads on any machine.
  - It can serve many directories, discover Git checkouts and **create Git worktrees** (`<repo>-<name>` siblings).
  - It self-updates hourly and restarts after at most 12 h when idle.
  - Shared runners execute other members' threads **as the OS user who started the runner**. The docs carry an explicit warning (`cli/runners`).

### 4.4 Concurrency and limits

- **Orb spawn pacing:** a burst of **20** metered orbs per user, then **1 new orb per 5 min**. Later starts queue instead of failing (`orbs`).
- **Clone and setup caps:** clone takes at most 15 min, setup at most 20 min, `.agents/resume` blocks for at most 10 s.
- **Uploads:** at most 512 MB per Files or Terminal upload.
- **Other limits:** Multiplayer stays on for 7 days. Agent `continue` chaining stops at 5, raisable with `maxContinuations`. Diff file ordering is disabled above 500 files.

---

## 5. Threads, history, sharing, compaction, handoff

| Capability | Documented behavior |
|---|---|
| Identity | `T-<uuid>` URL that opens on web, CLI and apps. Commits carry an `Amp-Thread-ID` trailer. PR descriptions with the thread URL link back to the thread. |
| Visibility | Private / Workspace / Group (Enterprise) / Unlisted. Public threads ended 2026-06-02. |
| Search | Activity feed with query syntax `id: label: parent: project: repo: author: visibility: archived: snoozed: pinned: commit: pr: after: before:`. Agents and Puck can search threads. |
| Referencing | `@T-…` or a URL in a prompt. The agent reads the thread and extracts what is relevant (Read Thread subagent). |
| Export | `.md` suffix on the URL, `amp threads markdown/export`, and full JSON for the creator. |
| Compaction | Automatic at a "configured percentage threshold, which defaults to 90%" of context. Per-agent `compactionThresholdTokens` (`plugin-api`). The compaction model is the same as the thread's. `getMessages` returns the latest compaction summary plus the messages after it, and `full: true` reads the entire transcript. |
| Handoff | Ask "Handoff and …" and the agent starts a fresh thread carrying the context that matters (`threads`; Chronicle "Handoff, Please", 2026-01-13). The "200k Tokens Is Plenty" note (2025-12-10) explains the short-thread philosophy. |
| Fork | Chronicle 2026-01-13 "Stick a Fork in It, It's Done". The title suggests forking was retired. The current manual has **no fork feature**. Exact status: **UNKNOWN**. |
| Steering and queueing | Messages steer the agent after its current step by default. Ctrl/⌘+Enter queues. Esc Esc interrupts. |
| Organize | Pin, color, labels, rename, snooze ("until I'm needed"), archive (pauses the orb), delete (permanent; data removed within 30 days per `/security`). |
| Multiplayer | Tag a workspace member to join. Only in orbs or on shared runners. Costs bill to the owner. A thread runs as one agent shared by several people. |
| Space | Voice and video call inside every thread. |
| Cross-client | Continue a running CLI thread from the web. A passkey can be required for web or app interaction. `--remote-control-terminal` controls whether the web can open terminals. |
| Notifications | macOS and iOS push when a thread is "ready for your next message". Android has none yet. CLI sounds through `amp.notifications.enabled`. |

---

## 6. Git, GitHub, review, diffs, terminal, app preview, worktrees

| Area | Documented behavior |
|---|---|
| GitHub connection | GitHub App plus OAuth. `git push` and `gh` in orbs run **as you**. Writes require the app to be installed on the repo. Signed commits and a chosen commit identity (2026-08-28). Other hosts (Bitbucket, GitLab, HTTPS Git) work through credentials. |
| Ship flow | Default is **trunk-based**: commit, fetch, rebase onto base, run the full test suite, push to base, then retry the rebase on conflict. The agent checks with the user on substantive conflicts and ignores a failing test only if the same test fails on base. Project Ship Behavior is **Ship / Push to Branch (PR URL) / Custom Ship** (prompt up to 10,000 chars). Plugins can append text through `changes.prompt`. |
| Restack | The agent rewrites history into cleaner commits (same final tree). No push. |
| Changes pane | Committed and uncommitted diff since the merge base, a per-commit picker, "Compare With Branch". **Intelligent file ordering by Jev**, which mutes generated files. Review button. Sync (`amp sync`) mirrors the orb to a local checkout live, or once with `--apply`. |
| Code review | The built-in `review` prompt and the `reviewing-code` skill (Task subagent). The 2026-02-04 note "Liberating Code Review" made the review agent composable. The legacy CRA GitHub App repo (`ampcode/cra-github`) is archived. |
| GitHub webhooks | Subscribe a thread to an issue or PR (comments, reviews, merge-queue events). **Orb spawner**: each newly opened issue or PR (optionally label-filtered) spawns an orb. **Follow CI** for an exact commit (check rollup plus a periodic refresh in case a webhook is missed). **Automatic follow-ups** subscribe the thread before reporting a PR complete. Subscriptions "do not ... grant permission to push changes, deploy, or carry out …" (truncated; see source) |
| Terminal | A shared tmux session inside the orb that both the agent and the user can use. It can be embedded live in replies. Paste or drop uploads a file. |
| App preview (Portals) | `.amp/services.yaml` declares services with health checks and dependencies. Portals get custom or friendly hostnames, review and comment overlays with dictation, and dev sign-in helpers (Vite, Laravel, magic link). Access requires a signed-in Amp user with thread access. |
| Desktop | A GUI desktop in the orb (browsers, apps), and on a runner with `--desktop`. |
| Worktrees | Runners create `git worktree`s from the composer, and archiving a thread can remove its worktree (`cli/runners` §Create a Worktree). Orbs give one isolated machine per thread instead of worktrees. |

---

## 7. Automations, triggers, webhooks, idempotency, CI

| Mechanism | Semantics (documented) |
|---|---|
| Schedules | Written in natural language. Stored as a schedule plus a prompt on the thread. **One schedule per thread.** When it fires, the agent is woken and reads the prompt with the `get_schedule` tool, keeping the thread's history. Runs once or repeats, ends on a completion condition, and can be paused or deleted from the indicator or by chat. Snoozed threads run quietly. |
| Plugin webhooks | `amp.createWebhook({key, headers, handler})` returns a public POST URL. Registration is keyed by (user, project, plugin, key) and stays stable across reloads and restarts. **Store-then-200, at-least-once.** Handler timeout 30 s. A throw causes a retry after 5 s that doubles up to 5 min, **out-of-order**, and the event is dropped after 1 h of rejections. **Rate:** a burst of 10, refilling at 10/min, with **429 at 100 queued**. Body at most 1 MB. **`Idempotency-Key` header** dedupes sender retries. Users are told to "Store `event.id` with the action" for handler idempotency. Amp does **not** verify signatures: the plugin must. Archiving the owning thread returns 404 and pauses delivery. |
| GitHub events | Native through the Amp GitHub App, with signatures verified by Amp (see §6). |
| Linear | Assign or mention Amp on an issue and it works in an orb and replies. Optionally spawns an orb per new issue. |
| Slack | Personal Puck in Slack. Slack listener messages can wake threads. |
| CI wake | `amp threads continue T-… -ox 'msg'` "is a simple way to wake a thread from a CI job". `amp -ox` runs in execute mode in an orb. Use `--no-archive-after-execute` for threads that own triggers. |
| A2A results | Results from other agents wake the receiving orb. |

---

## 8. Extensibility, configuration, permissions, data, pricing

### 8.1 MCP, skills, plugins, configuration

- **MCP**
  - There are two kinds of configuration. Local `amp.mcpServers` uses stdio or URL. Remote definitions are stored at ampcode.com, and Amp's servers connect to them from fixed egress IPs.
  - Supports OAuth (CIMD with a DCR fallback) and `${amp:id-token}` OIDC headers in orbs.
  - Per-tool policy is Allow / Ask First / Disabled. The `anthropic/requiresUserInteraction` `_meta` flag forces Ask First.
  - Workspace `.amp/settings.json` servers need `amp mcp approve`. `amp mcp doctor` diagnoses servers.
  - Enterprise can restrict servers with an **MCP registry allowlist**.
  - Amp recommends bundling MCP servers inside skills (`mcp.json`) so tools load lazily.
- **Skills**
  - Format: a `SKILL.md` with name and description frontmatter.
  - Search order has 11 tiers, including `.agents/skills/`, **`.claude/skills/`, `~/.claude/skills/` and `~/.claude/plugins/cache/` (Claude Code compatible)**, then personal and workspace skill repos, then official skills.
  - Custom commands were removed 2026-01-29 in favor of skills.
- **Plugins**
  - Written in TypeScript or JavaScript. Locations, in precedence order: project `.amp/plugins/`, system `~/.config/amp/plugins/`, personal, workspace.
  - Events: `session.start → agent.start → tool.call → tool.result → agent.end`, plus `changes.prompt`.
  - APIs: `registerTool`, `registerCommand`, `registerSkill`, `ctx.ui.*` (notify, confirm, input, select, panes), `ctx.tools.call`, `amp.ai.ask/generate/decide`, `createAgent`/`registerAgentMode`, `getBuiltinAgent(mode).createThread({executor:'orb'|{type:'runner',id}, project, multiplayerTTLSeconds})`, `createWebhook`, thread labels.
  - Hot reload. Global plugin and skill repos can be shared, imported or published.
- **Toolboxes**
  - Not present in the current manual. Toolboxes were the 2025-10-22 "More Tools for the Agent" feature, which created tools from the CLI. The current equivalent is plugin `registerTool`.
  - Whether toolboxes still work: **UNKNOWN (undocumented)**.
- **Settings** (`amp.*`, from `cli/settings`)
  - Examples: `tools.disable`, `mcpPermissions`, `defaultVisibility`, `git.commit.ampThread.enabled`, `git.commit.coauthor.enabled`, `skills.*`, `remoteThreadCreation.enabled`, `runner.*`, `updates.mode`, `admin.compatibilityDate`.
  - Managed (admin) settings exist, as do proxy and certificate settings.
- **AGENTS.md**
  - Granular guidance files, which can be ignored. A global AGENTS.md is available.

### 8.2 Permissions and approvals summary

| Layer | Control |
|---|---|
| Built-in tools | **No approval by default.** `amp.tools.disable` turns tools off. |
| Policy plugin | `tool.call` returns `allow`, `reject-and-continue`, `modify` or `synthesize`. Can be distributed workspace-wide. Example decision-model guard: block if `p(destructive) > 0.9`. |
| MCP tools | Allow / Ask First / Disabled, checked on every call. Ask First pauses the thread (it may sleep) until the owner answers. The answer is recorded with user ID and time. |
| Thread state | `ThreadState = 'idle' \| 'running' \| 'awaiting-approval' \| 'error'` (`plugin-api`) |
| Identity hardening | Passkey required for web or app interaction. Admins can disable cross-client access, runner sharing and dictation. |
| Shared runners | Run as the host OS user. Explicit trust warning. |

### 8.3 Data handling (vendor statements, `/security` + `enterprise/minimal-data-retention`)

- Thread data (messages, responses, code snippets or files used as context, tool results, attachments) is stored on GCP in the US. Deleted threads are removed **within 30 days**. Deleting a thread deletes its orb within seconds.
- Paused-orb filesystem and memory are stored **encrypted at rest** until the thread is deleted.
- Minimal Data Retention applies to Amp-managed provider connections, with documented exceptions (abuse monitoring, up to 30 days for some models, KV caches, legal holds). "Neither Amp nor its model providers use customer data to train models." With BYOK, your own provider's terms apply.
- Claude Fable through BYOK requires an Anthropic workspace with data retention enabled. ZDR keys cannot access Fable (`models-and-subagents`).
- Audit logs are kept at least 30 days. Enterprise gets an analytics and thread-data API.

### 8.4 Pricing model (as of 2026-10-27)

| Tier | What the page states |
|---|---|
| **Hobby: Free** | All product features. Pay-as-you-go Amp-hosted orbs. **Unlimited self-hosted orbs, free.** Own runners free. Use ChatGPT, Claude and other subscriptions. BYOK. **No Amp token fees or limits.** |
| **Individual: $20/mo** (Megawatt; Gigawatt is a higher variant) | "45,000 minutes of orbin' time" (Amp-hosted). Own domains for portals. The Gigawatt price was **not captured** (client-rendered): **UNKNOWN**. |
| Education | $10/mo (Chronicle 2026-08-18) |
| **Teams: no extra charge** | Members on any tier. Sharing, multiplayer, SSO, pooled credits, shared BYOK and routing. |
| **Enterprise: custom** | SCIM, spend limits, custom self-hosted orbs, audit logs, IP allowlist, regional endpoints, MDR, entitlements |
| Paid credits | **No markup on provider API prices** for individuals and non-enterprise workspaces. Credits expire after 12 months. Web search, page reading, voice and Painter use credits even with subscriptions. |
| Ads | **No.** Ads ran from October 2025 to 2026-03-30 and were dropped ("$10M+ USD annual run rate" claimed, then removed). |

### 8.5 CLI vs editor

- The VS Code-family extension was **removed** 2026-02-19.
- The CLI attaches to editors (VS Code, Cursor, Windsurf, Zed, Neovim through `ampcode/amp.nvim`) for the current file, selection and undoable edits.
- The CLI was "rebuilt from the ground up" (2026-05-06). The npm package was renamed `@sourcegraph/amp` → `@ampcode/cli` (2026-05-14).
- The TUI sidebar was removed 2026-08-27.
- File @-mentions exist only in the TUI ("intentional").

---

## 9. Public GitHub inventory (`gh repo list ampcode --limit 100`, 2026-10-27)

There are 16 public repositories. **None is the Amp core.** `github.com/ampcode/amp` (the npm `repository` URL) returns 404.

| Repo | HEAD SHA (date) | License (LICENSE file) | What it is | Core? |
|---|---|---|---|---|
| ampcode/official-plugins | `0252953b7878539eb673c98113d20e730037ce76` (2026-10-26) | **None** (no LICENSE: all rights reserved by default) | **Official agent-mode prompts and tool lists** (`official-modes/modes/*.ts`, 34 modes) plus official skills (`skills/` with 20 SKILL.md files: reviewing-code, searching-code, researching-external-repositories, planning-work, proving-changes, orb-setup, building-plugins and others). Mirrored to Amp's internal "Pierre" repo. | No: prompt and skill content, **reference only** |
| ampcode/homebrew-tap | `a2547a8c4b4ffdd145974ce09a3033f76c53a85a` (2026-10-27) | MIT | Homebrew formula and cask for the CLI and app | No |
| ampcode/amp.nvim | `01ede44322220da5dc0b73ad8ace328a5ec1f5bf` (2026-08-03) | Apache-2.0 | Neovim bridge for `ide connect` | No: editor plugin |
| ampcode/trestle | `ffd8fb26a1be3e533e82267066afaf0fc2e17029` (2026-09-07) | Apache-2.0 | Knowledge-graph harness for code migration, with `trestle init --amp`. Alpha. | No: adjacent tool |
| ampcode/substrate | `3ae42112002cc65dd11cb2b6767ca1ebeb2c3a51` (2026-10-27) | Apache-2.0 | **Fork** of `agent-substrate/substrate`: zero-trust gVisor/microVM sandbox runtime on Kubernetes. Not Amp's orb implementation (no evidence of that). | No: fork of third-party OSS |
| ampcode/goal-cup-tracer | `8793376608d6e1c987062ff78c48c06a588e1fb1` (2026-10-15) | Apache-2.0 | **Fork** of `agentcommunity/goal-cup-proxy`: tamper-evident hash-chained trace of agent sessions (Rust) | No |
| ampcode/merge | `91087ac60e51697febd9409a1d3b07d166b6e10c` (2026-07-24) | MIT (CodeMirror authors) | Vendored `@codemirror/merge` (diff UI) | No |
| ampcode/wmux (archived) | `f2030f97bf40eaac0442c9e59189cfedc5a199d1` (2026-03-13) | None | "Expose a tmux session in the browser" (Go) | No: likely an ancestor of the web terminal (inference) |
| ampcode/svelte-check-daemon | `39ad84836b5b0a368924b97c00ffec4e84a93883` (2026-01-08) | Apache-2.0 | Dev tooling | No |
| ampcode/zvelte-check | `5afc63d3eea4d2ba0b36526528006cb871e33f4e` (2026-01-27) | MIT | Dev tooling (Zig) | No |
| ampcode/amp-contrib | `2ba7041a9583a02987adf595aac58d1f9abfc183` (2026-03-31) | None | Curated skills, tools, MCPs | No |
| ampcode/amp-contrib-2 | `73d292453f5aa7d78decc7f55c177175e659eb5a` (2025-12-11) | None | Legacy custom commands and toolbox-style tool templates | No |
| ampcode/amp-examples-and-guides | `435ffc0b4d82dfcb083848088411afb44b1ff55f` (2025-10-17) | None | Examples | No |
| ampcode/amp-sdk-demo | `88ad03dde836e4a24fd4df8cc533d3a1769dfb9f` (2025-10-08) | None | SDK demo | No |
| ampcode/cra-github (archived) | `c9af1216b5235dcdcaeaf86d04a33ef1e7aaef71` (2025-12-29) | None | Code-review agent GitHub App (Actions or webhook) using Amp | No |
| ampcode/cra-gitlab (archived) | `64822aa78b7b31c0698bf4537993cec829203911` (2025-08-11) | None | GitLab variant | No |

**Packages:**

| Package | Version | License | Note |
|---|---|---|---|
| `@ampcode/sdk` | `0.1.0-20260918210405-g81edbf0` | **Amp Commercial License** | repo → private |
| `@ampcode/plugin` | `0.0.0-20261027001613-g52e251f` | **Amp Commercial License** | Types only, per docs |
| `@ampcode/cli` | `0.0.1793104576-gc52692` | "SEE LICENSE IN LICENSE.md" | Closed binary |
| PyPI `amp-sdk` | `0.1.20260918210324` | "© Sourcegraph Inc. All rights reserved." | |

**Sourcegraph org:** No current Amp repos.

| Repo | HEAD SHA | License | State |
|---|---|---|---|
| `sourcegraph/nvim-lspconfig-amp` | `1e45898e8498c735365ac9a29e24397dae03812d` | Apache-2.0 | archived 2025-08 |
| `sourcegraph/cody-public-snapshot` | `8e20ac6c1460c08b0db581c0204658112a246eda` | Apache-2.0 | archived; Cody, Amp's predecessor |
| `sourcegraph/codeprobe` | `349658a0c14622dccccc9be038cabca63a1e4a0b` | Apache-2.0 | Coding-agent evals from merged PRs; tangential |

**Implications:**

- WePLD can **study** official-plugins prompts and skills as a behavior reference. It must **not copy** them, because there is no license.
- The only Apache or MIT donors in the org are peripheral: amp.nvim, trestle, the substrate fork, the goal-cup fork, and merge.

---

## 10. Amp Capability vs WePLD Acquisition Map

Column key:

- **Src?** Amp source is publicly available (Y / Partial / N).
- **Oracle?** Amp can serve only as a behavior oracle, meaning WePLD can observe its documented or observable behavior but not reuse its code.
- **Donor:** an open-source alternative, with name, URL and license. Path-level detail is in R10 §3.
- **Build?** Whether WePLD must build the capability.
- **Advantage:** what WePLD must measurably deliver. These are *proposed acceptance metrics*, not measured results.

| # | Amp feature | Src? | Oracle? | OSS donor (URL, license) | Build? | Advantage WePLD must deliver (proposed metric) |
|---|---|---|---|---|---|---|
| 1 | Dial modes (low to ultra, fixed per thread) | Partial (mode prompts in official-plugins, **unlicensed**) | Y | OpenCode agents config (github.com/anomalyco/opencode, MIT); Codex `agent-roles` crate (github.com/openai/codex, Apache-2.0) | Y (mode registry) | Mode can be switched **mid-session with explicit cache-cost disclosure**, or kept fixed, chosen by policy. 100% of routing decisions logged with reason. |
| 2 | Per-role model choice (main + subagents inherit) | N | Y | goose `crates/goose-providers`, `crates/goose/src/model_config.rs` (github.com/aaif-goose/goose, Apache-2.0) | Y | **Independent per-role pins**, for example reviewer ≠ implementer, which Amp does not allow for Task subagents. Every role pin visible in a ledger. |
| 3 | Provider precedence and model-mapping DSL | N | Y | OpenCode provider layer (MIT); LiteLLM-style gateways; codex `model-provider` crate (Apache-2.0) | Y | **Documented runtime failover on 429/5xx** (Amp's is UNKNOWN). Measurable: failover p95 < N s, zero silent provider switches. |
| 4 | Cost-aware routing | N | Y (user-driven only) | — (no mature OSS optimizer found) | Y | **Automatic budget-capped routing** with per-thread spend ceilings enforced before the call. Delta in actual versus budget at most X%. |
| 5 | Task subagent (isolated context, summary-only return) | N | Y | OpenHands SDK `openhands/sdk/subagent`, `openhands/tools/{delegate,task}` (github.com/OpenHands/software-agent-sdk, MIT); OpenCode "general" subagent (MIT) | Y | **Structured result contract plus validation** (schema plus evidence) instead of a free-text summary. Percentage of subagent results passing machine checks. |
| 6 | Oracle, Librarian, Search (now Task skills) | Partial (SKILL.md text, unlicensed) | Y | OpenHands `tools/ask_oracle` (MIT); Codex `file-search` crate (Apache-2.0) | Y (skills plus a search index) | Local code search with no cloud upload. Recall on a repository's own Q&A set. |
| 7 | Read Thread / cross-thread reference | N | Y | Codex `thread-store`, `rollout`, `history` crates (Apache-2.0) | Y | Local, searchable, **offline** thread index. Query latency target. No vendor storage. |
| 8 | Compaction (90% threshold) and handoff | N | Y | goose `crates/goose/src/context_mgmt` (Apache-2.0); OpenCode `packages/core/src/session` (MIT) | Y | Compaction that is **auditable and reversible** (the full transcript is kept, with a diffable summary). Handoff carries a typed context packet. |
| 9 | Thread sharing, visibility, multiplayer | N | Y | Zed `crates/collab` (AGPL server; reference only) | Optional | Local-first sharing, with end-to-end encryption or a self-hosted relay. No vendor-held transcripts. |
| 10 | Orbs (per-thread VM, snapshot, idle-pause, wake) | N | Y | E2B (github.com/e2b-dev/E2B, Apache-2.0); agent-substrate (github.com/agent-substrate/substrate, Apache-2.0); OpenHands `openhands/workspace/{docker,apptainer,remote_api}` (MIT) | Y (provider abstraction) | **Executor-agnostic lifecycle** (local worktree, container, VM) with crash-safe resume. Wake to first tool call p95. $0 when idle. |
| 11 | Self-hosted orb dispatch contract | N (contract documented) | Y | Amp's documented contract is a good **interface oracle**. Donors: E2B, Daytona (archived June 2026; license per v0.190.0), Docker | Y | No outbound dependency on a vendor control plane. Fully offline mode. |
| 12 | Runners and shared runners | N | Y | coder/agentapi (MIT, **archived**); vibe-kanban `crates/relay-*` (Apache-2.0) | Y | Remote execution **without running others' code as the host user** (sandboxed per-user). Measured by escape tests. |
| 13 | Worktrees on runners | N | Y | claude-squad `session/git/worktree*.go` (AGPL-3.0, reference only); vibe-kanban `crates/worktree-manager` (Apache-2.0); Codex `worktree` crate (Apache-2.0) | Y | Deterministic worktree lifecycle with cleanup guarantees. Zero orphaned worktrees after crash. |
| 14 | Changes pane, intelligent diff ordering, restack | N (UI); merge view is MIT CodeMirror | Y | `@codemirror/merge` (MIT); vibe-kanban `crates/review` (Apache-2.0) | Y | Ordering explainable from local signals. Restack proven tree-equal (hash check). |
| 15 | Ship / Push to Branch / Custom Ship | N | Y | openai/codex-action (github.com/openai/codex-action, Apache-2.0, `c05cfd74ad95c626cdf05c6685e62becc3bf7813`) | Y | **Policy-gated ship**, with tests and review gates that are enforced, not prompt-requested. |
| 16 | Code review (review skill) | Partial (skill text) | Y | `ampcode/cra-github` (no license, archived; reference only); Codex code review (docs only, learn.chatgpt.com/docs/code-review) | Y | Reviewer independent from the implementer (a different model or role). Findings tracked to resolution. |
| 17 | Terminal (shared tmux) | N | Y | Zed `crates/terminal` (GPL-3.0, reference); `ampcode/wmux` (no license) | Y | Local PTY ownership by the trusted core (WePLD S3 terminal fabric). |
| 18 | Portals, Desktop (app preview) | N | Y | vibe-kanban `crates/preview-proxy` (Apache-2.0); E2B desktop (Apache-2.0) | Y | Preview with no public URL by default (loopback or authenticated). |
| 19 | Automations and schedules | N | Y | goose `crates/goose/src/scheduler` (Apache-2.0); OpenHands SDK `openhands/sdk/automation` (MIT) | Y | **Durable schedules that survive restart**, with run history and exactly-once side-effect ledgers. |
| 20 | Webhooks (at-least-once, Idempotency-Key, backoff) | N (semantics documented) | Y (good spec oracle) | Vercel Workflow (see R05, Apache-2.0) | Y | Same at-least-once semantics **plus built-in dedupe and signature verification** (Amp leaves both to the plugin). |
| 21 | GitHub subscriptions, orb spawner, Follow CI | N | Y | openai/codex-action (Apache-2.0); OpenHands SDK `openhands/sdk/automation` (MIT) | Y | CI follow that is exact-commit and offline-replayable. |
| 22 | Agent-to-agent (spawn, message, file transfer) | N | Y | ACP (github.com/agentclientprotocol/agent-client-protocol, Apache-2.0); Codex `agent-message-board-client`, `agent-graph-store` crates (Apache-2.0) | Y | Typed inter-agent messages with provenance. Explicit file transfer with hash receipts. |
| 23 | Puck (meta-agent, MCP-exposed) | N | Y | — | Y | Coordinator that runs with **local authority boundaries**. Every delegated action attributable. |
| 24 | MCP (local, remote, OAuth, `code_exec` + `tool_search`) | N | Y | MCP TS SDK (github.com/modelcontextprotocol/typescript-sdk, MIT→Apache-2.0 transition); rmcp (github.com/modelcontextprotocol/rust-sdk); Codex `rmcp-client`, `code-mode*` crates (Apache-2.0) | Y (integrate) | Per-tool policy **default Ask** for untrusted servers. Registry allowlist built in. |
| 25 | Skills (11-tier search, Claude-compatible paths) | Partial (official SKILL.md, unlicensed) | Y | Codex `skills` crate (Apache-2.0); goose `crates/goose/src/skills` (Apache-2.0) | Y | Skill provenance pinning (hash) and admission gate. |
| 26 | Plugin API (events, tools, agents, UI) | Types only (commercial license) | Y | OpenCode `packages/plugin` (MIT); Codex `plugin-host` crate (Apache-2.0); goose `crates/goose/src/plugins` | Y | Sandboxed plugins (capability-scoped) instead of full-trust in-process code. |
| 27 | Permissions (none by default; plugin or MCP policy) | N | Y | Codex `execpolicy`, `sandboxing`, `linux-sandbox`, `windows-sandbox-rs` (Apache-2.0); anthropics/sandbox-runtime (Apache-2.0) | Y | **OS-enforced sandbox plus approval policy by default** (the stance opposite to Amp's). Escape-test pass rate. |
| 28 | Decision models (Jev) | N | Y | — (local small classifier; d1-style advisory only) | Optional | Advisory-only, **never a gate**. Calibration report on a local labelled set. |
| 29 | SDK (TS, Python; executors) and stream-JSON | N (commercial) | Y | Codex `sdk/typescript`, `sdk/python`, `app-server-protocol` (Apache-2.0); OpenHands Agent Server REST (MIT) | Y | Stable, versioned local protocol (ACP and app-server compatible). |
| 30 | Mobile and notifications | N | Y | — | Later | Push or approve from the phone without sending source code to a vendor (relay carries metadata only). |
| 31 | Data handling (30-day delete, MDR) | N | Y | — | Y (policy) | **Local-first by default.** Zero thread data off-device unless opted in. |
| 32 | Editor integration (`ide connect`) | Partial (`amp.nvim` Apache-2.0) | Y | ACP plus Zed `crates/agent_servers`, `acp_thread` (GPL-3.0, reference); ACP SDKs (Apache-2.0) | Y | Expose WePLD as an ACP agent and host ACP agents. |

---

## 11. Open questions / UNKNOWN register

1. Runtime provider failover on errors and retries between connections.
2. Concurrency limit on Task subagents per thread.
3. Whether toolboxes and thread forking still exist.
4. Gigawatt price and the exact Megawatt allowance split.
5. Whether `ampcode/substrate` has any role in Amp's hosted orbs (only a fork is observed).
6. The server-side storage format of threads.
7. Whether intelligent diff ordering runs entirely on Jev or combines other signals.

---

## Sources

- Amp manual index: https://ampcode.com/llms.txt. Every page is at https://ampcode.com/docs/markdown/{slug}. Slugs used: `the-dial`, `models-and-subagents`, `tools`, `prompting`, `projects`, `github`, `integrations`, `threads`, `pricing`, `orbs`, `orbs/{getting-started,customizing,shipping,sizes-and-costs,handling-secrets,files-and-attachments,portals,agent-to-agent,automations,self-hosted,self-hosted/kubernetes}`, `apps`, `apps/{mac,mac/runner,ios,android}`, `puck`, `puck/slack-integration`, `collaborate/{workspaces,groups,multiplayer,space}`, `customize/{plugins,decision-models,global-plugins-and-skills,skills,mcp,agents-md,model-routing}`, `cli`, `cli/{keybindings,execute-mode,spawning-orbs,clone,streaming-json,settings,runners,remote-control}`, `sdk`, `sdk/{typescript,python}`, `plugin-api`, `egress-ips`, `support/{getting-help,reporting-bugs}`, `enterprise/{mcp-registry-allowlist,workspace-thread-visibility-controls,workspace-entitlements,allowed-models,minimal-data-retention}`, `designing-ui`, `index`.
- https://ampcode.com/chronicle
- https://ampcode.com/pricing
- https://ampcode.com/modes
- https://ampcode.com/security
- https://ampcode.com/news/amp-free-is-ad-free
- GitHub: https://github.com/ampcode (all 16 repos above), https://github.com/sourcegraph, https://github.com/agent-substrate/substrate, https://github.com/agentcommunity/goal-cup-proxy
- npm: https://registry.npmjs.org/@ampcode/sdk/latest, https://registry.npmjs.org/@ampcode/plugin/latest, https://registry.npmjs.org/@ampcode/cli/latest
- PyPI: https://pypi.org/pypi/amp-sdk/json
