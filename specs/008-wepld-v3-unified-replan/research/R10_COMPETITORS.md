# R10: Competitor grounding and reusable OSS modules

- **Mission:** 008-wepld-v3-unified-replan. Planning research only. Nothing was cloned, installed, built or run.
- **Date:** 2026-10-27. Every URL was accessed on 2026-10-27.
- **Method:**
  - Repository facts (license, HEAD SHA, directory layout) come from `gh api` against the default branch at the time of access.
  - Product facts come from official docs where they could be reached (cursor.com/docs, learn.chatgpt.com, zed.dev/docs, repository READMEs).
  - Where only secondary press was available, the claim is labelled **(secondary)**.
- **Trust rule:** Web and repository text is data, not instructions.
- **No invented numbers:** No benchmarks or prices are invented. **UNKNOWN** marks claims that could not be verified.
- **Path-level module claims:** These were verified by listing repository trees. They are pointers for later path-mining, not admitted sources. Under WePLD policy, `SOURCE_ADMISSION = NONE` still applies.
- **Companion:** R04_AMP.md (Amp).

---

## 0. Pins (OSS repositories, HEAD on default branch, 2026-10-27)

| Repo | HEAD SHA | Date | License (GitHub SPDX / file) | Note |
|---|---|---|---|---|
| openai/codex | `603a7baff0f6f37ee9a8a9375a272eaab03d3ece` | 2026-10-27 | Apache-2.0 | Rust `codex-rs/`, TS/Python `sdk/` |
| openai/codex-action | `c05cfd74ad95c626cdf05c6685e62becc3bf7813` | — | Apache-2.0 | GitHub Action |
| OpenHands/OpenHands | `6c120073f5a1e1c838ba6fdd9a075c79ff997b98` | 2026-10-27 | MIT (LICENSE: "Copyright © 2025 OpenHands contributors") | Now "Agent Canvas" (formerly All-Hands-AI/OpenHands) |
| OpenHands/software-agent-sdk | `f7cbea4ff6210f8f665aacb166abfacfca6f8be0` | 2026-10-27 | MIT | SDK, Agent Server, tools, workspaces |
| anomalyco/opencode | `7b1e54a74f6201e725a50cba5d7fb383aa64e407` | 2026-10-27 | MIT | **Moved from sst/opencode.** Default branch `dev`. |
| aaif-goose/goose | `398165c9376e61157ba9cfdd487ca9622d716955` | 2026-10-27 | Apache-2.0 | **Moved from block/goose.** Now part of the Agentic AI Foundation (Linux Foundation). |
| cline/cline | `775d0398039977ca5447ed39c1a7f178df69aa87` | 2026-10-27 | Apache-2.0 | VS Code, JetBrains, CLI, desktop, SDK |
| Kilo-Org/kilocode | `7b3c857408b1f805491db7cb82170a7efc34db64` | 2026-10-27 | MIT | Contains `packages/opencode` (OpenCode-derived CLI) |
| zed-industries/zed | `37faef81f74fc1bb08be9939c4cffc8ede6ced2f` | 2026-10-27 | NOASSERTION (root has LICENSE-GPL and LICENSE-APACHE; license varies per crate) | Copyleft for editor crates: reference only |
| agentclientprotocol/agent-client-protocol | `e50f62b4a1ca8d794a4c97210acd8a0d833b05c5` | 2026-10-27 | Apache-2.0 | ACP spec and schema |
| agentclientprotocol/rust-sdk | `644377ad2654415c76c979c795d6c568e17a6d62` | 2026-10-26 | Apache-2.0 | |
| agentclientprotocol/typescript-sdk | `bca8e49199927e167fab74db4dd76dec4743bb49` | 2026-10-26 | Apache-2.0 | |
| agentclientprotocol/python-sdk | `2ad204bb86111da9594bfe13f4a560249603feea` | 2026-10-22 | Apache-2.0 | |
| agentclientprotocol/claude-agent-acp | `4324dce4be877c55385b3389cebac1c63d08f456` | 2026-10-27 | Apache-2.0 | Claude Agent SDK as an ACP agent |
| agentclientprotocol/codex-acp | `582e545eb1868763645ea59b1a2c106e50d5d471` | 2026-10-27 | NOASSERTION (verify before use) | Codex as an ACP agent |
| modelcontextprotocol/typescript-sdk | `b415e60bdf0e8dd5d6cbe7e6353abfb982b06dd2` | 2026-10-26 | NOASSERTION: **MIT → Apache-2.0 transition**. New code is Apache-2.0. Older contributions without relicensing consent stay MIT. | |
| modelcontextprotocol/python-sdk | `d7845c073a2b9ba5ab2817ecf93d3e45ef24cd14` | 2026-10-27 | MIT | |
| modelcontextprotocol/rust-sdk (rmcp) | `cd88056ffdc97756fbd98e5a12bbeb41758f0ce8` | 2026-10-26 | NOASSERTION (assumed to follow the same transition: verify) | |
| BloopAI/vibe-kanban | `a019cebf0693f787ef0f8dc2bb8d37edd35527ac` | 2026-10-26 | Apache-2.0 | Rust crates, multi-agent worktree manager |
| smtg-ai/claude-squad | `ce1ffb4392b01f38e2c4599c7c84d2a93973b138` | 2026-08-20 | **AGPL-3.0** | Reference only |
| stravu/crystal | `1e18e0bc981225f75b5226f82a300fa741970c6f` | 2026-02-26 | MIT | "Crystal is now Nimbalyst". Stale. |
| e2b-dev/E2B | `ee355b765ac0e884fbeaa69e4b44f4c7c58ed6b1` | 2026-10-26 | Apache-2.0 | Sandbox SDKs. The infrastructure is a separate repo (not checked). |
| daytonaio/daytona | `ec4c21b2d597091ac09ecc278f3bcc172575a987` | 2026-06-25 | Repo field NONE. README points to the v0.190.0 LICENSE. | **Archived.** "As of June 2026, Daytona's core development has moved to a private codebase." |
| anthropics/sandbox-runtime | `98a4016d27609ed34dd1fb43d23ed6efb6eeeb77` | 2026-10-25 | Apache-2.0 | Filesystem and network restriction wrapper |
| agent-substrate/substrate | `a11540ae7ae01f647e9aea6c35443845fbdcf118` | 2026-10-27 | Apache-2.0 | gVisor and microVM actor runtime on K8s (Amp keeps a fork) |
| coder/agentapi | `7c468d5b25ec9d3d76c41313cf4e08904ff5968d` | 2026-09-13 | MIT | **Archived.** HTTP API over Claude Code, Goose, Aider, Gemini, Amp and Codex. |

---

## 1. Competitor matrix

The license column describes source availability. "Durable session" means resume after a client or process restart. "Remote" means agents running off the user's machine.

| Product | Source / license | Surfaces | Durable session / recovery | Multi-agent / worktrees | Remote / mobile | Permission model | Self-hosting | Cost model |
|---|---|---|---|---|---|---|---|---|
| **Amp** (baseline, see R04) | Closed core. Periphery repos (§R04-9). | Web, CLI/TUI, macOS, iOS and Android apps, Slack, Linear, SDKs | Server-side threads. Orbs pause with memory and disk, then wake. | Task subagents, agent-to-agent threads, runner worktrees | Orbs, runners, all apps. Push on macOS and iOS. | **No approvals by default.** Plugin or MCP policies. | Self-hosted orbs (dispatch contract). Runners. Inference stays on Amp. | Free Hobby with BYO compute and keys. $20/mo tier. Credits at cost. |
| **Cursor** (desktop + cloud agents) | **Closed** | Desktop IDE with the **Agents Window (Cursor 3.0, 2026-04-02)**; cursor.com/agents web; iOS; Android PWA; Slack, GitHub, Bitbucket and Linear `@cursor`; API | Cloud agents run in VMs and keep running without the local machine. Sessions **move cloud ↔ local** (secondary). Local persistence details: **UNKNOWN**. | Parallel agents. `/worktree`, `/apply-worktree`, **`/best-of-n`** (one task × several models in separate worktrees). Await tool for subagents. | Cloud VMs with full dev environments, remote desktop takeover, artifacts (screenshots, video, logs). Remote SSH environments. | Cloud: branch-only pushes, team-scoped secrets, admin outbound-domain restrictions, Tailscale. `.cursor/hooks.json` runs in the cloud. Local approval model not re-verified: **UNKNOWN**. | **"Self-Hosted Machines"**: tool execution on your hardware, inference in Cursor's cloud (docs mention; details UNKNOWN). | Plan usage at model rates. Cloud agents need Premium or higher, Teams, Enterprise or a legacy paid plan (not Free or Plus). Spend limit prompt. |
| **OpenAI Codex** (CLI, IDE, ChatGPT desktop app, cloud) | **CLI, core and SDK are open: Apache-2.0** (`openai/codex`). The desktop app and cloud are closed. | Codex CLI; IDE extension; **ChatGPT desktop app** (macOS, Windows, Linux guide) with Codex inside (the standalone Codex app, launched February 2026, was folded into ChatGPT around 2026-07-09: **(secondary)**); Codex Cloud (web, mobile, desktop); **Codex on mobile** controlling a connected computer; App Server protocol; SDK (TS, Python); GitHub Action; Slack and Teams | Local thread and rollout persistence with TUI resume (`codex-rs/{rollout,thread-store,history}`, `codex-rs/tui/src/app/resume_*.rs`). Cloud tasks continue "while your computer is asleep". | Worktree chats ("Use Git worktrees in Codex to run chats in parallel"). Subagents and custom agents. Crates `agent-graph-store` and `agent-message-board-client`. | Codex Cloud environments (published, reusable saved state, per-task workspace). Mobile start, approve and review. | **Strongest local model:** OS sandbox (`read-only`, `workspace-write` and others) plus an approval policy (`on-request` and others). Network off by default. `execpolicy` rules. Destructive MCP calls always need approval. The `untrusted` policy is retired. Asynchronous safety monitoring can pause tasks. | CLI fully local with gateways (Bedrock, LiteLLM). Cloud is OpenAI-hosted. | Included in ChatGPT plans (Plus, Pro, Business, Edu, Enterprise per docs) or API key. Workspace credit controls. |
| **OpenHands** (Agent Canvas + Software Agent SDK) | **MIT** (both repos) | Agent Canvas web UI (local stack: `agent-canvas`, Docker, Electron dir present), CLI (separate repo OpenHands-CLI), Python, TS and REST SDK, OpenHands Cloud and Enterprise (commercial) | Each container mounts the conversation workspace and persisted state, so "workspace files and conversation history survive container replacement". | Multiple agents per Agent Server. Subagent and delegate tools. Runs **third-party agents through ACP** (Claude Code, Codex, Gemini, Pi, OpenCode). | Backends: local, Docker, VMs, OpenHands Cloud. Canvas switches between backends. | Security module (`openhands/sdk/security`), hooks, secret redaction in the Agent Server. Loopback-only bind by default. | **Yes: first-class.** Self-hosting guide, Helm dir, multiple Agent Servers. | OSS free. Cloud and Enterprise priced separately (**UNKNOWN** here). |
| **OpenCode** | **MIT** (`anomalyco/opencode`) | TUI and CLI (`@opencode/cli`), **desktop app (beta, macOS and Windows)**, client/server split (`packages/server`, `packages/sdk`), web, ACP (`packages/cli/src/acp`) | Local sessions (`packages/core/src/session*`). SQLite via `effect-drizzle-sqlite` (inferred from the package name). Snapshots (`packages/core/src/snapshot.ts`). | Built-in "general" subagent. Worktree module (`packages/core/src/worktree*`). | Server mode allows remote clients. Hosted share links: **UNKNOWN** this pass. | Permission module (`packages/core/src/permission*`). The plan agent "Asks permission before running bash commands". | Fully local. BYO provider. | Free OSS. Optional OpenCode Go router (referenced by Amp model-routing docs). |
| **Goose** | **Apache-2.0** (`aaif-goose/goose`, AAIF / Linux Foundation) | Desktop (macOS, Linux, Windows), CLI, API. ACP server and client. Custom distributions. | `crates/goose/src/session`, `session_context.rs` | Recipes, subagents (**UNKNOWN** depth), scheduler | Remote: **UNKNOWN** (crate `goose-roaming` exists; purpose unverified) | `crates/goose/src/permission`, `security`, `tool_inspection.rs`, `action_required_manager.rs` | Fully local. Local inference crate (`goose-local-inference`, llama.cpp). | Free OSS. BYO keys or subscriptions **via ACP** (Claude, ChatGPT, Gemini). |
| **Cline** | **Apache-2.0** | VS Code, JetBrains, CLI (`apps/cli`, ACP at `apps/cli/src/acp`), **desktop app (macOS, Windows) with scheduled routines**, SDK (`sdk/packages/{agents,core,llms,sdk,shared,ui}`), cline-hub | **UNKNOWN** this pass (checkpoints not re-verified) | Kanban (`.kanban`, `apps/cli/src/kanban-migration`). `.worktreeinclude` present. | **UNKNOWN** | Approval-based by default (historical; not re-verified: **UNKNOWN**) | Local | Free OSS plus BYO keys. Hosted provider optional. |
| **Kilo Code** | **MIT** | VS Code, JetBrains, CLI (`@kilocode/cli`, OpenCode-derived `packages/opencode`), **Cloud Agent** (app.kilo.ai/cloud), Marketplace | Inherits OpenCode session design (inferred) | Agents marketplace. Sandbox package `packages/kilo-sandbox`, memory package `packages/kilo-memory`. | Cloud Agent on the web | `--auto` auto-approves unless a rule denies | Local CLI | Free OSS plus Kilo gateway (`packages/kilo-gateway`). Pricing **UNKNOWN**. |
| **Zed** (agent panel, ACP) | Mixed GPL-3.0, Apache-2.0 and AGPL. **Copyleft: reference only.** | Editor agent panel and threads sidebar. **External agents via ACP**: Claude, Codex, OpenCode, Copilot, Cursor, Pi, Gemini CLI, Poolside. ACP Registry. | Thread history. External-agent threads can be imported and restored. | Multiple threads. Crates `acp_thread`, `agent_servers`, `agent_ui`. | Remote dev (`crates/remote*`). Mobile: none. | Per agent | Editor is local | "Zed does not charge for External Agents." Zed AI pricing not checked: **UNKNOWN**. |
| **Conductor** (Melty Labs) | **Closed**, Mac app | Mac app (Apple silicon, secondary); "Conductor Cloud" announced on the site | **UNKNOWN** | **One git worktree + branch per workspace**, running parallel Claude Code, Codex (and Cursor) agents. Diff review and merge. | Conductor Cloud (details **UNKNOWN**) | Delegated to the wrapped agents | No | App free, bring your own agent subscriptions (secondary) |
| **Crystal → Nimbalyst** | MIT (Crystal repo, stale since 2026-02-26) | Electron app (`main/`, `frontend/`) | Local | Parallel Codex and Claude Code sessions in git worktrees | No | Delegated | Local | Free |
| **vibe-kanban** | **Apache-2.0** | Tauri app, `npx` CLI, web | DB-backed (`crates/db`) | **Executors for amp, claude, codex, copilot, cursor, droid, gemini, opencode, qwen and ACP** (`crates/executors/src/executors/*`). `crates/worktree-manager`, `workspace-manager`, `review`. | **Relay** stack (`relay-*`, `relay-webrtc`, `embedded-ssh`, `preview-proxy`) | Delegated | Local plus relay | Free OSS |
| **claude-squad** | **AGPL-3.0** | TUI plus daemon plus web | tmux-backed sessions (`session/tmux`, `session/storage.go`) | git worktree per session (`session/git/worktree*.go`) | **UNKNOWN** | Delegated | Local | Free |

### 1.1 Observations relevant to WePLD

1. **Convergence on three primitives.** Products converge on: (a) isolated workspace per task (worktree, container or VM), (b) a server-held or locally durable thread that any client can attach to, and (c) parallel agents with diff review and a ship step. Amp (orbs), Cursor (cloud agents and the Agents Window), Codex (worktree, local and cloud modes), OpenHands (Agent Server backends) and Conductor and vibe-kanban (worktree managers) all fit this shape.
2. **ACP is the de facto agent ↔ client standard.** Zed, OpenHands Canvas, Goose, OpenCode (`packages/cli/src/acp`), Cline CLI (`apps/cli/src/acp`), vibe-kanban (`executors/acp`) and Amp's `ide connect` all speak or wrap agents through ACP. Apache-2.0 SDKs exist in Rust, TypeScript, Python, Kotlin and Java. **WePLD should be both an ACP host and an ACP agent.**
3. **Permission stances diverge sharply.**
   - Codex: OS sandbox plus approval by default.
   - Amp: no approvals, policy by plugin.
   - Kilo: `--auto`.
   - A local-first, trust-gated control plane (WePLD) has a defensible position only if its default is **sandboxed and approval-gated with low friction**. That means donor code from `codex-rs/{sandboxing,linux-sandbox,windows-sandbox-rs,execpolicy}` and `anthropics/sandbox-runtime`.
4. **Self-hosting is becoming table stakes.** Amp self-hosted orbs, Cursor Self-Hosted Machines and OpenHands self-hosting all split execution (customer) from inference and orchestration (vendor). WePLD's advantage is **no vendor orchestration at all**, with the control plane on the desktop.
5. **Durability is underspecified everywhere.** No competitor documents exactly-once side effects or crash-consistent event logs. Amp documents at-least-once webhooks and tells users to dedupe. This is WePLD's clearest measurable gap to own (see R05 for Vercel Workflow-style durable execution).
6. **Windows is a weak spot for Amp.** The CLI runs only via WSL and the macOS app requires Apple silicon. Codex ships a native Windows sandbox (`windows-sandbox-rs`, `windows-sandbox-service`) and a Windows app. WePLD (a Tauri desktop app) can target native Windows directly.

---

## 2. Licensing guidance for reuse

| Class | Repos | Use in WePLD |
|---|---|---|
| Permissive (Apache-2.0 / MIT) | codex, codex-action, OpenHands, software-agent-sdk, opencode, goose, cline, kilocode, ACP spec and SDKs, MCP python-sdk, vibe-kanban, E2B, sandbox-runtime, agent-substrate, crystal, agentapi | Candidate donors after normal admission: NOTICE, attribution, pinned SHA |
| Transitional / NOASSERTION | MCP typescript-sdk and rust-sdk (MIT → Apache-2.0 split), codex-acp, zed repo-level | Verify per-file license before any copy |
| Copyleft | zed editor crates (GPL-3.0), zed collab (AGPL), claude-squad (AGPL-3.0) | **Behavior reference only. No code transplant.** |
| No license / proprietary | Amp core, `@ampcode/*` (Amp Commercial License), ampcode/official-plugins (no LICENSE), Cursor, Conductor, ChatGPT desktop app, Codex Cloud | Behavior oracle only |
| Archived | daytona (moved private June 2026), coder/agentapi, crystal (stale) | Pin-and-fork only, with no upstream support |

---

## 3. Concrete reusable OSS modules for WePLD gaps (path-level)

WePLD context, from STATUS_LEDGER: a Rust and Tauri desktop app (`crates/core`, `crates/contracts`, `apps/desktop/src-tauri`), with S3 terminal fabric and trusted process ownership pending. Rust-native donors are therefore ranked first. All paths were verified to exist at the SHA in §0.

### 3.1 Agent adapters (drive external agents)

| Gap | Module (path @ repo) | License | Why |
|---|---|---|---|
| Multi-agent executor adapters | `crates/executors/src/executors/{amp.rs,claude.rs,codex.rs,opencode.rs,cursor.rs,gemini.rs,copilot.rs,droid.rs,qwen.rs,acp/}` @ BloopAI/vibe-kanban | Apache-2.0 | Rust. Already wraps **Amp** (stream-JSON), Claude Code, Codex and others, plus a generic ACP executor. Closest fit to a WePLD "agent fabric". |
| Claude via ACP | `src/` @ agentclientprotocol/claude-agent-acp | Apache-2.0 | Exposes the Claude Agent SDK as an ACP agent |
| Codex via ACP | @ agentclientprotocol/codex-acp | NOASSERTION: verify | |
| Codex embed protocol | `codex-rs/{app-server,app-server-protocol,app-server-transport,app-server-client}` @ openai/codex | Apache-2.0 | Versioned JSON-RPC protocol for embedding Codex in a host app |
| HTTP wrapper pattern | `internal/`, `lib/` @ coder/agentapi | MIT (archived) | Terminal-screen-scrape HTTP API over agent TUIs. Pattern reference. |
| Amp stream-JSON compatibility | Amp `cli/streaming-json` documents a Claude Code-compatible stream format | — | A single parser can serve both Claude Code and Amp |

### 3.2 ACP (host and agent sides)

| Module | License | Use |
|---|---|---|
| `agent-client-protocol-schema/`, `schema/` @ agentclientprotocol/agent-client-protocol | Apache-2.0 | Canonical schema to generate WePLD contract types (`crates/contracts`) |
| agentclientprotocol/rust-sdk | Apache-2.0 | Rust host and agent implementation for Tauri |
| agentclientprotocol/typescript-sdk | Apache-2.0 | Webview side if needed |
| agentclientprotocol/acp-tck (repo exists; not pinned this pass) | **UNKNOWN** license | Conformance tests: use for an ACP compliance gate |
| `crates/{acp_thread,agent_servers,agent_ui}` @ zed-industries/zed | GPL-3.0 (verify per crate) | **Reference only**: best production example of an ACP host UI |
| `crates/goose/src/acp`, `crates/goose-acp-macros` @ aaif-goose/goose | Apache-2.0 | Rust ACP agent-side implementation |
| `openhands-agent-server/openhands/agent_server/acp_router.py` @ OpenHands/software-agent-sdk | MIT | ACP over REST bridging pattern |

### 3.3 MCP

| Module | License | Use |
|---|---|---|
| `crates/rmcp`, `crates/rmcp-macros` @ modelcontextprotocol/rust-sdk | Verify (transition) | Rust MCP client and server |
| `codex-rs/{rmcp-client,codex-mcp,connectors}` @ openai/codex | Apache-2.0 | Production MCP client wrapper, OAuth and connector handling |
| `codex-rs/{code-mode,code-mode-host,code-mode-runtime,code-mode-protocol}` @ openai/codex | Apache-2.0 | **Code-mode MCP**: the same pattern as Amp's `tool_search` + `code_exec`, which keeps large MCP catalogs out of context |
| `packages/{client,server,core}` @ modelcontextprotocol/typescript-sdk | MIT/Apache-2.0 split | TS side |
| `src/` @ modelcontextprotocol/python-sdk | MIT | Python tooling and tests |
| `crates/goose-mcp`, `crates/goose/src/mcp_utils.rs` @ aaif-goose/goose | Apache-2.0 | Built-in MCP extensions |

### 3.4 Sandboxing and execution isolation

| Module | License | Use |
|---|---|---|
| `codex-rs/{sandboxing,linux-sandbox,bwrap,windows-sandbox-rs,windows-sandbox-service,mxc-sandbox,process-hardening,execpolicy,network-proxy}` @ openai/codex | Apache-2.0 | **Top donor.** OS sandboxes for Linux (`bwrap` and `linux-sandbox` crates; exact kernel mechanisms not re-verified) and native Windows, an exec policy rules engine, and a network proxy. Directly fills WePLD S3 "trusted process ownership". |
| `src/` @ anthropics/sandbox-runtime | Apache-2.0 | Filesystem and network restriction wrapper for arbitrary processes |
| agent-substrate/substrate (`pkg/`, `internal/`, `docs/security.md`) | Apache-2.0 | gVisor or Cloud Hypervisor actors, SPIFFE identity, egress credential injection. A pattern for future remote "orbs". |
| `packages/{js-sdk,python-sdk,desktop-js}` @ e2b-dev/E2B | Apache-2.0 | Remote sandbox provider. Pause and resume with memory, per Amp's table. |
| `openhands-workspace/openhands/workspace/{docker,apptainer,remote_api,agent_sandbox,cloud}` @ OpenHands/software-agent-sdk | MIT | Workspace provider abstraction: local, Docker, Apptainer, remote. **Interface model for a WePLD executor trait.** |
| `packages/kilo-sandbox` @ Kilo-Org/kilocode | MIT | TS sandbox package (contents not inspected) |
| Amp self-hosted dispatch contract (`spawn`/`pause`/`delete` plus env vars) | Docs only | **Interface oracle** for a provider-agnostic remote executor |

### 3.5 Durable sessions, memory and search

| Module | License | Use |
|---|---|---|
| `codex-rs/{rollout,rollout-trace,thread-store,history,message-history,state,memories,attachment-store,file-search}` @ openai/codex | Apache-2.0 | Durable thread and rollout storage, memories, fuzzy file search (Rust) |
| `crates/goose/src/{session,context_mgmt,scheduler,recipe}` @ aaif-goose/goose | Apache-2.0 | Sessions, compaction or context management, scheduler (Rust) |
| `packages/core/src/{session*,snapshot.ts,worktree*,permission*}` @ anomalyco/opencode | MIT | TS reference for sessions, snapshots, worktree and permission |
| `openhands-sdk/openhands/sdk/{conversation,context,event,critic,automation,subagent,hooks}` @ OpenHands/software-agent-sdk | MIT | Event-sourced conversation model, critic or result validation, automations, subagents |
| `packages/kilo-memory` @ Kilo-Org/kilocode | MIT | Memory package (contents not inspected) |
| ampcode/goal-cup-tracer (`crates/`) | Apache-2.0 | **Hash-chained, tamper-evident session trace** with an offline verifier. Fits WePLD's evidence and integrity culture. |
| `crates/db` @ BloopAI/vibe-kanban | Apache-2.0 | Task, attempt and session DB schema for multi-agent runs |

### 3.6 Worktrees and multi-agent orchestration

| Module | License | Use |
|---|---|---|
| `crates/{worktree-manager,workspace-manager,git,git-host}` @ BloopAI/vibe-kanban | Apache-2.0 | Rust worktree lifecycle, the closest donor |
| `codex-rs/{worktree,git-utils,agent-graph-store,agent-message-board-client,message-board,agent-roles}` @ openai/codex | Apache-2.0 | Worktrees plus **agent graph and message board** for inter-agent coordination |
| `session/git/{worktree.go,worktree_ops.go,worktree_branch.go}`, `session/tmux/` @ smtg-ai/claude-squad | AGPL-3.0 | **Reference only** |
| `main/`, `frontend/` @ stravu/crystal | MIT | Electron worktree session manager (stale) |
| Amp runner worktree semantics (`<repo>-<name>` siblings, upstream fast-forward, archive removes worktree) | Docs | Behavior oracle |

### 3.7 Review, diff and ship

| Module | License | Use |
|---|---|---|
| `crates/review` @ BloopAI/vibe-kanban | Apache-2.0 | Review flow over agent diffs |
| ampcode/merge (`@codemirror/merge`) | MIT | Side-by-side and unified diff view for a webview |
| openai/codex-action | Apache-2.0 | CI-triggered agent runs and PR review |
| `openhands-sdk/openhands/sdk/critic` @ OpenHands/software-agent-sdk | MIT | Automated critique or validation of agent output |
| `crates/{preview-proxy,relay-*,embedded-ssh}` @ BloopAI/vibe-kanban | Apache-2.0 | App preview and remote access (Amp Portals analogue) |

### 3.8 Recommended shortlist for WePLD path-mining (priority order)

1. **openai/codex `codex-rs/{sandboxing,linux-sandbox,windows-sandbox-rs,execpolicy,network-proxy}`** fills S3 trusted process ownership and gives a sandboxed-by-default stance.
2. **ACP rust-sdk plus the schema** make WePLD an ACP host and agent. This covers editor integration and lets one adapter fit many agents.
3. **BloopAI/vibe-kanban `crates/{executors,worktree-manager,review}`** provide Rust agent adapters (including Amp) and worktrees.
4. **openai/codex `codex-rs/{rollout,thread-store,app-server-protocol}`** provide a durable thread format and an embedding protocol.
5. **rmcp plus codex `code-mode*`** give MCP with lazy tool loading.
6. **goal-cup-tracer** provides a tamper-evident run trace for WePLD evidence.
7. **OpenHands `openhands-workspace` interfaces** inform the executor trait for local, container and remote backends.

---

## 4. UNKNOWN register

1. Cursor: local session persistence, local approval model, Self-Hosted Machines setup, exact plan prices.
2. Codex: the official date of the Codex-into-ChatGPT merger. Only secondary sources (Wikipedia, The New Stack, Addigy, TechRadar) report it. Official docs now live under learn.chatgpt.com and describe a "ChatGPT desktop app" containing Codex.
3. OpenCode: hosted share and cloud features. Desktop app maturity beyond "BETA".
4. Goose: the purpose of `goose-roaming`. Subagent depth.
5. Cline and Kilo: checkpoint and approval defaults (not re-verified). Kilo pricing.
6. Zed: AI pricing. Exact per-crate license of `acp_thread`, `agent_servers` and `agent_ui`.
7. Conductor: Conductor Cloud capabilities. Durability.
8. License text for MCP rust-sdk, codex-acp and acp-tck.

---

## Sources

- Cursor:
  - https://cursor.com/docs/cloud-agent
  - https://cursor.com/changelog/3-0
  - https://forum.cursor.com/t/can-i-still-start-cloud-agents-worktrees-from-the-sidebar/157427 (secondary)
  - https://www.spotdev.co.uk/blog/cursor-agents-window-cli-cloud-agents (secondary)
- OpenAI Codex:
  - https://learn.chatgpt.com/llms.txt
  - https://learn.chatgpt.com/docs/app.md
  - https://learn.chatgpt.com/docs/cloud.md
  - https://learn.chatgpt.com/docs/agent-approvals-security.md
  - https://learn.chatgpt.com/docs/features.md
  - https://developers.openai.com/codex (308 redirect to learn.chatgpt.com)
  - https://github.com/openai/codex
  - https://github.com/openai/codex-action
- Codex merger, secondary:
  - https://en.wikipedia.org/wiki/OpenAI_Codex_(AI_agent)
  - https://thenewstack.io/openai-codex-work-atlas/
  - https://support.addigy.com/hc/en-us/articles/53439709931155-ChatGPT-and-Codex-Desktop-App-Merger-What-This-Means-for-Your-Fleet
  - https://techradar.com/ai-platforms-assistants/christ-almighty-this-is-so-bad-chatgpts-big-app-update-brings-huge-changes-to-your-workflows-and-users-seem-to-hate-it
  - https://decrypt.co/361925/openai-superapp-chatgpt-codex-atlas-merger-anthropic
  - https://www.businesstoday.in/technology/news/story/openai-launches-new-dedicated-codex-app-for-macos-to-supercharge-ai-driven-software-development-514353-2026-02-03
- OpenHands:
  - https://github.com/OpenHands/OpenHands (README)
  - https://github.com/OpenHands/software-agent-sdk (README)
- OpenCode: https://github.com/anomalyco/opencode (README)
- Goose: https://github.com/aaif-goose/goose (README)
- Cline: https://github.com/cline/cline (README)
- Kilo Code: https://github.com/Kilo-Org/kilocode (README)
- Zed:
  - https://zed.dev/docs/ai/external-agents
  - https://github.com/zed-industries/zed
- Conductor:
  - https://www.conductor.build
  - https://conductor.build/docs/concepts/git-worktrees
  - https://www.morphllm.com/conductor-ai-coding (secondary)
  - https://codepick.dev/en/guides/conductor-build-intro/ (secondary)
- ACP: https://github.com/agentclientprotocol (agent-client-protocol, rust-sdk, typescript-sdk, python-sdk, claude-agent-acp, codex-acp, registry)
- MCP: https://github.com/modelcontextprotocol (typescript-sdk, python-sdk, rust-sdk)
- Worktree managers and orchestration:
  - https://github.com/BloopAI/vibe-kanban
  - https://github.com/smtg-ai/claude-squad
  - https://github.com/stravu/crystal
- Sandboxes, runtimes and wrappers:
  - https://github.com/e2b-dev/E2B
  - https://github.com/daytonaio/daytona (README archive notice)
  - https://github.com/anthropics/sandbox-runtime
  - https://github.com/agent-substrate/substrate
  - https://github.com/coder/agentapi
