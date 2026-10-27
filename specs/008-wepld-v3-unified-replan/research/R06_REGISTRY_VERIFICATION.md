# R06 - Registry Verification (live inventory / rights / access)

- Date of verification: 2026-10-27 (GitHub API state as fetched on that date)
- Subject: frozen `WEPLD_MASTER_SOURCE_REGISTRY_2026-08-14_V1` (402 named entries), plus its pin ledger and mining priority matrix
- Spec: `008-wepld-v3-unified-replan`

> **Scope statement - inventory-level verification, NOT a code audit.** This document checks only whether each registry
> entry still exists and is reachable, who owns it now, whether it is archived, which licence the GitHub API (and, where
> that was inconclusive, the root LICENSE text) reports, the default-branch HEAD SHA, and last push time. No source code,
> path-level licence, NOTICE/third-party file, dependency tree, test suite or security property was inspected. A `MINE_DEEP`
> disposition means *worth a path-level mining pass*, not *admitted*: `SOURCE_ADMISSION = NONE` and
> `DEPENDENCY_ADMISSION = NONE` from the pin ledger remain in force. HEAD SHAs below are observation anchors, not pins.

## 1. Method

1. Parsed the registry CSV (402 rows; the JSON `registry` array carries the same 402 records). Text was treated as data.
2. For every row whose URL is on `github.com` with an `owner/repo` path, called `gh api repos/{owner}/{repo}` (redirects followed;
   a returned `full_name` different from the registry path is recorded as `RENAMED`), then
   `gh api repos/{full_name}/commits/{default_branch} --jq .sha` for the HEAD SHA. Org-only URLs (`github.com/{org}`) were
   checked with `gh api users/{org}` and marked `ORG_LEVEL`. Script: `_work/registry_live.py` (4 workers, 0.25 s spacing,
   retry/back-off on rate limit, resumable cache `_work/registry_live.json`).
3. For repos where the API licence was `NOASSERTION` or null (47), fetched the root licence file head via
   `gh api repos/{r}/license` (`_work/registry_license_probe.py` -> `_work/registry_license_heads.json`) and recorded an
   effective licence label. These labels are from the first ~500 characters of the root licence only.
4. Non-GitHub URLs (60 rows, incl. `docs.github.com`; plus 1 bare `https://github.com/` row) were classified by URL type (vendor product page / docs / spec / paper) and 22 were
   spot-checked with an HTTP GET (`curl -L`): 19 returned 200, `lovable.dev` and `hud.io` returned 403 (bot-blocking),
   and the Emacs savannah cgit URL returned 502. Redirects of note: `docs.anthropic.com/en/docs/claude-code` ->
   `code.claude.com/docs`; `docs.cursor.com` -> `cursor.com/docs`; **`docs.windsurf.com` -> `docs.devin.ai/desktop`**.
5. Step-4 named projects that are absent from the registry were probed the same way (`_work/registry_live_extra.py`).
6. Stale = last push before 2025-10-27 (more than 12 months). Copyleft/rights flags: GPL, AGPL, SSPL, BUSL, FSL, Elastic,
   Commons Clause, proprietary sub-trees, and no-licence are flagged; MPL/EPL/LGPL/CDDL are flagged as weak copyleft.
7. Dispositions (`MINE_DEEP` / `KEEP_REFERENCE` / `DEFER` / `REJECT`) are proposals for the v3 replan, derived from: liveness,
   licence class, maintenance, duplication, and relevance to the 15 v3 capability groups. They do not override the
   registry's frozen `disposition_class`; they are input to it.

## 2. Summary statistics

| Measure | Rows (of 402) | Unique targets |
|---|---|---|
| GitHub `owner/repo` URLs | 335 | 330 repos |
| GitHub org-only URLs | 6 | 6 orgs |
| Unresolvable GitHub URL (`https://github.com/`) | 1 | - |
| Non-GitHub URLs | 60 | - |
| LIVE (same path) | 320 | 315 |
| RENAMED / transferred (redirects) | 11 | 11 |
| 404 | 4 | 4 |
| ORG_LEVEL (exists, but no exact repo) | 6 | 6 |
| Archived (read-only) | 6 | 6 |
| Stale (no push > 12 months) | 9 | 9 |
| Private repos | 0 | 0 |
| Duplicate rows (same repo listed twice) | 5 | - |

HEAD SHA was obtained for every live/renamed repo (0 failures).

**404:** `Agent-Hellboy/SkillSpector`, `microsoft/AutoElicit`, `microsoft/RedTeamCUA`, `robert-mcdermott/graphify`

**Renamed / transferred:** `ComposioHQ/agent-orchestrator` -> `OrchestratorInc/agent-orchestrator`; `Helweg/opencode-codebase-index` -> `Helweg/open-codebase-index`; `alibaba/OpenSandbox` -> `opensandbox-group/OpenSandbox`; `badlogic/pi-mono` -> `earendil-works/pi`; `eclipse/openvsx` -> `eclipse-openvsx/openvsx`; `kermitt2/grobid` -> `grobidOrg/grobid`; `mendableai/firecrawl` -> `firecrawl/firecrawl`; `qodo-ai/pr-agent` -> `The-PR-Agent/pr-agent`; `strands-agents/sdk-python` -> `strands-agents/harness-sdk`; `viperproject/prusti-dev` -> `prusti/prusti`; `woodruffw/zizmor` -> `zizmorcore/zizmor`

**Archived:** `21st-dev/1code`, `Azure/PyRIT`, `RooCodeInc/Roo-Code`, `protectai/llm-guard`, `tensorzero/tensorzero`, `voideditor/void`

**Stale (>12 months):** `SALT-NLP/DyLAN` (2024-05-16), `cohere-ai/BinaryVectorDB` (2024-05-17), `cozodb/cozo` (2024-12-04), `fidelity/mabwiser` (2024-09-05), `lm-sys/RouteLLM` (2024-08-10), `testmoapp/junitxml` (2023-01-17), `tree-sitter/tree-sitter-graph` (2024-12-11), `wslong20/G-safeguard` (2025-06-28), `yanweiyue/AgentPrune` (2025-03-23)

**Org-level URLs needing an exact repo:** `anyproto`, `eclipse-oct`, `modelcontextprotocol`, `stryker-mutator`, `swe-bench`, `tavily-ai`

### 2.1 Licence distribution (unique live repos, effective label)

| Licence | Repos |
|---|---|
| Apache-2.0 | 142 |
| MIT | 112 |
| AGPL-3.0 | 10 |
| BSD-3-Clause | 7 |
| NONE | 6 |
| MPL-2.0 | 5 |
| GPL-3.0 | 3 |
| LGPL-2.1 | 3 |
| EPL-2.0 | 3 |
| Unlicense | 2 |
| GPL-2.0 | 2 |
| FSL-1.1-MIT | 2 |
| BUSL-1.1 | 2 |
| Elastic-2.0 | 2 |
| MIT (LICENSE-CODE) + CC-BY-4.0 docs | 1 |
| BSD-style | 1 |
| Apache-2.0 + proprietary ee/ | 1 |
| AGPL-3.0 / Apache-2.0 mixed | 1 |
| CC-BY-4.0 (models mixed) - VERIFY | 1 |
| GPL-2.0-only | 1 |
| GPL-2.0 WITH linking-exception | 1 |
| SSPL-1.0 (Apache-2.0 future) | 1 |
| JetBrains build terms at root (source headers Apache-2.0) - VERIFY | 1 |
| Apache-2.0 + Vim | 1 |
| Mixed: Apache-2.0 / GPL-3.0 / AGPL-3.0 per crate | 1 |
| MIT + proprietary backend dirs | 1 |
| Apache-2.0 (license/ dir, not API-detected) | 1 |
| Apache-2.0 OR MIT (crate manifests; unverified) | 1 |
| Apache-2.0 + CC-BY-4.0 data | 1 |
| MIT OR CC0-1.0 | 1 |
| MIT + Commons Clause | 1 |
| CC-BY-4.0 | 1 |
| ISC | 1 |
| CDDL-1.0 | 1 |
| MIT + proprietary enterprise/ | 1 |
| MPL-2.0 (+ per-crate) | 1 |
| UPL-1.0 | 1 |
| BSD-2-Clause | 1 |
| LGPL-3.0 | 1 |

| Licence class | Repos |
|---|---|
| permissive | 273 |
| strong-copyleft | 19 |
| weak-copyleft | 15 |
| source-available/mixed | 11 |
| no-license | 6 |
| docs-license | 2 |

### 2.2 Copyleft / rights flags (unique live repos)

| Repo | Effective licence | Class | Registry rows |
|---|---|---|---|
| `bingreeky/MaAS` | NONE | no-license | SRC-0372 |
| `testmoapp/junitxml` | NONE | no-license | SRC-0180 |
| `ulab-uiuc/GraphPlanner` | NONE | no-license | SRC-0375 |
| `wangzx1219/AgentDropout` | NONE | no-license | SRC-0373 |
| `wslong20/G-safeguard` | NONE | no-license | SRC-0393 |
| `yanweiyue/AgentPrune` | NONE | no-license | SRC-0374 |
| `Arize-ai/phoenix` | Elastic-2.0 | source-available/mixed | SRC-0340 |
| `BerriAI/litellm` | MIT + proprietary enterprise/ | source-available/mixed | SRC-0323 |
| `charmbracelet/crush` | FSL-1.1-MIT | source-available/mixed | SRC-0056 |
| `eyaltoledano/claude-task-master` | MIT + Commons Clause | source-available/mixed | SRC-0226 |
| `gitbutlerapp/gitbutler` | FSL-1.1-MIT | source-available/mixed | SRC-0122 |
| `JetBrains/intellij-community` | JetBrains build terms at root (source headers Apache-2.0) - VERIFY | source-available/mixed | SRC-0129 |
| `orch8-io/engine` | BUSL-1.1 | source-available/mixed | SRC-0390 |
| `PatrickSys/codebase-context` | Elastic-2.0 | source-available/mixed | SRC-0298 |
| `restatedev/restate` | BUSL-1.1 | source-available/mixed | SRC-0112 |
| `TabbyML/tabby` | Apache-2.0 + proprietary ee/ | source-available/mixed | SRC-0068, SRC-0157 |
| `toeverything/AFFiNE` | MIT + proprietary backend dirs | source-available/mixed | SRC-0151 |
| `AppFlowy-IO/AppFlowy` | AGPL-3.0 | strong-copyleft | SRC-0162 |
| `asciinema/asciinema` | GPL-3.0 | strong-copyleft | SRC-0232 |
| `dagucloud/dagu` | GPL-3.0 | strong-copyleft | SRC-0389 |
| `discourse/discourse` | GPL-2.0 | strong-copyleft | SRC-0072 |
| `giancarloerra/SocratiCode` | AGPL-3.0 | strong-copyleft | SRC-0297 |
| `git/git` | GPL-2.0-only | strong-copyleft | SRC-0100 |
| `grafana/pyroscope` | AGPL-3.0 | strong-copyleft | SRC-0317 |
| `GrammaTech/ddisasm` | AGPL-3.0 | strong-copyleft | SRC-0352 |
| `inngest/inngest` | SSPL-1.0 (Apache-2.0 future) | strong-copyleft | SRC-0111 |
| `kdlbs/kandev` | AGPL-3.0 | strong-copyleft | SRC-0290 |
| `makeplane/plane` | AGPL-3.0 | strong-copyleft | SRC-0277 |
| `mattermost/mattermost` | AGPL-3.0 / Apache-2.0 mixed | strong-copyleft | SRC-0070 |
| `mendableai/firecrawl` | AGPL-3.0 | strong-copyleft | SRC-0344 |
| `qodo-ai/qodo-cover` | AGPL-3.0 | strong-copyleft | SRC-0263 |
| `qundao/mirror-mergiraf` | GPL-3.0 | strong-copyleft | SRC-0103 |
| `renovatebot/renovate` | AGPL-3.0 | strong-copyleft | SRC-0077 |
| `searxng/searxng` | AGPL-3.0 | strong-copyleft | SRC-0345 |
| `universal-ctags/ctags` | GPL-2.0 | strong-copyleft | SRC-0050 |
| `zed-industries/zed` | Mixed: Apache-2.0 / GPL-3.0 / AGPL-3.0 per crate | strong-copyleft | SRC-0143 |
| `cozodb/cozo` | MPL-2.0 | weak-copyleft | SRC-0360 |
| `dequelabs/axe-core` | MPL-2.0 | weak-copyleft | SRC-0086 |
| `eclipse-theia/theia` | EPL-2.0 | weak-copyleft | SRC-0126 |
| `eclipse/openvsx` | EPL-2.0 | weak-copyleft | SRC-0168 |
| `hcengineering/platform` | EPL-2.0 | weak-copyleft | SRC-0270 |
| `helix-editor/helix` | MPL-2.0 | weak-copyleft | SRC-0128 |
| `libgit2/libgit2` | GPL-2.0 WITH linking-exception | weak-copyleft | SRC-0102 |
| `NixOS/nix` | LGPL-2.1 | weak-copyleft | SRC-0117 |
| `opengrep/opengrep` | LGPL-2.1 | weak-copyleft | SRC-0205 |
| `oracle/opengrok` | CDDL-1.0 | weak-copyleft | SRC-0303 |
| `pa11y/pa11y` | LGPL-3.0 | weak-copyleft | SRC-0366 |
| `penpot/penpot` | MPL-2.0 | weak-copyleft | SRC-0082 |
| `semgrep/semgrep` | LGPL-2.1 | weak-copyleft | SRC-0210 |
| `toeverything/blocksuite` | MPL-2.0 | weak-copyleft | SRC-0146 |
| `viperproject/prusti-dev` | MPL-2.0 (+ per-crate) | weak-copyleft | SRC-0333 |

Notes: `NOASSERTION` from the API is not a licence. MCP SDK repos (absent rows, section 5) are in an MIT -> Apache-2.0
relicensing transition (new contributions Apache-2.0, docs CC-BY-4.0). Zed's root is Apache but GPL/AGPL crates exist; the
pin ledger already marks it `BOUNDED_ENRICHED_RIGHTS_COMPLEX`. Pin-ledger rights statements for Kilo/Goose/Codex/Tauri/etc.
were not re-verified at path level.

### 2.3 Proposed v3 dispositions

| Disposition | Rows |
|---|---|
| MINE_DEEP | 33 |
| KEEP_REFERENCE | 206 |
| DEFER | 127 |
| REJECT | 36 |

### 2.4 Changes since the 2026-08-14 freeze that matter

- `continuedev/continue`: README states the repo is **no longer actively maintained and read-only** (GitHub `archived` flag is
  still false; pushes continue). Treat as failure-corpus/reference only (pin ledger already says this).
- Archived since freeze: Roo Code, Void, 21st-dev/1code, TensorZero, PyRIT, LLM Guard.
- Ownership moves: Goose `block/goose` -> `aaif-goose/goose` (registry already uses new path); OpenHands
  `All-Hands-AI/OpenHands` -> `OpenHands/OpenHands`; opencode `sst/opencode` -> `anomalyco/opencode`; PR-Agent -> `The-PR-Agent`;
  Pi `badlogic/pi-mono` -> `earendil-works/pi`; Strands `sdk-python` -> `harness-sdk`; Composio agent-orchestrator -> `OrchestratorInc`.
- `JetBrains/intellij-community` root LICENSE.txt now carries "JetBrains Open-Source Build Terms v1.3 (2026-06-15)"; source-file
  licence must be re-verified before any reuse.
- Windsurf docs now redirect into Devin docs (product consolidation); merge SRC-0141 into SRC-0398 as one behavior oracle.

### 2.5 Pin-ledger drift (40-hex pins vs current default-branch HEAD)

| Artifact | Ledger pin (12) | HEAD 2026-10-27 (12) | Moved? | Probed via |
|---|---|---|---|---|
| `Kilo-Org/kilocode` | `f7115470740c` | `d75c029a2985` | yes | registry probe |
| `kirodotdev/Kiro` | `e8daa058590d` | `bfe7ff30d9b2` | yes | pin-ledger probe |
| `aaif-goose/goose` | `5751715df0b4` | `398165c9376e` | yes | registry probe |
| `zed-industries/zed` | `c05e34637b4f` | `37faef81f74f` | yes | registry probe |
| `greptileai/greptile-vscode` | `72fc0c5a68ff` | `8f4abd8fc1c2` | yes (archived) | pin-ledger probe |
| `augmentcode/context-connectors` | `f7d6472ae626` | `f7d6472ae626` | NO (unchanged) | registry probe |
| `augmentcode/augment-swebench-agent` | `17d813385f50` | `17d813385f50` | NO (unchanged) | pin-ledger probe |
| `qodo-ai/open-aware` | `68976a9dd957` | `68976a9dd957` | NO (unchanged) | registry probe |
| `CognitionAI/devin-cli` | `bd4163ed29e9` | `37d6de3de0a3` | yes | pin-ledger probe |
| `CognitionAI/devin-extension` | `36437282f7f1` | `36437282f7f1` | NO (unchanged) | pin-ledger probe |
| `CognitionAI/devin-outpost-k8s` | `992f807dac0d` | `fedb657f3270` | yes | pin-ledger probe |
| `eigent-ai/eigent` | `88d837f75ad9` | `a46f680ea220` | yes | registry probe |
| `deepseek-ai/deepseek-harness` | `47f943859bef` | `22ddee379240` | yes | registry probe |
| `cordiverse/cordis` | `8cc9e33fab69` | `c81e299808de` | yes | registry probe |
| `CommandCodeAI/command-code` | `5c8f1b48c9d6` | `630bbf418f62` | yes | pin-ledger probe |
| `CommandCodeAI/cmd-old-public` | `48cacf798aa2` | `48cacf798aa2` | NO (unchanged) (archived) | pin-ledger probe |
| `openai/codex` | `91d6f48992ad` | `6b56106ed9a3` | yes | registry probe |
| `tauri-apps/tauri` | `d727d631659f` | `7e39750cf6a4` | yes | registry probe |
| `microsoft/windows-rs` | `5f8e1504dea5` | `d6443f28190f` | yes | registry probe |
| `wezterm/wezterm` | `fe3006aefcdc` | `e68a8ec27727` | yes | registry probe |
| `jj-vcs/jj` | `3a81f836030b` | `531b68204688` | yes | registry probe |
| `GitoxideLabs/gitoxide` | `dc370d9cacb4` | `15b71a3a0bfb` | yes | registry probe |
| `bytecodealliance/wasmtime` | `0b9b72dc2bc7` | `ec63b69f3da9` | yes | registry probe |
| `WebAssembly/component-model` | `6be2295c9c7c` | `8505ba73dda2` | yes | registry probe |
| `NVIDIA/OpenShell` | `d22859c22d1d` | `bd2ecaf1526c` | yes | registry probe |
| `microsoft/litebox` | `7af6242f0729` | `7fa997bf1ebc` | yes | registry probe |
| `microsoft/hcsshim` | `2bbdac6fec23` | `838c2196b8c5` | yes | registry probe |
| `e2b-dev/E2B` | `034c503f1fd5` | `ee355b765ac0` | yes | pin-ledger probe |
| `daytonaio/daytona` | `ec4c21b2d597` | `ec4c21b2d597` | NO (unchanged) (archived) | pin-ledger probe |
| `continuedev/continue` | `5522c6f44ca0` | `5522c6f44ca0` | NO (unchanged) | registry probe |

An unchanged HEAD with a recent `pushed_at` (Continue) means pushes are landing on non-default branches only; consistent with
the README's read-only notice.

## 3. Capability grouping for the v3 architecture

Each registry row is assigned to exactly one primary group. G01-G15 are the v3 capability groups; X1-X7 are adjacent
areas present in the registry but outside the requested v3 capability list (default disposition `DEFER`).

### G01 - Desktop shell / IDE (18 rows)

- **MINE_DEEP:** SRC-0124 Code - OSS - Workbench layout, extension host, terminal/editor integration patterns (MIT); SRC-0170 Tauri 2 - Rust desktop shell; IPC/capabilities/updater; pin-ledger PATH_MINED_PASS1
- **KEEP_REFERENCE:** SRC-0125 Cursor, SRC-0126 Eclipse Theia, SRC-0130 Junie, SRC-0132 Kiro, SRC-0133 Lapce, SRC-0137 Pulsar, SRC-0138 Replit, SRC-0140 VSCodium, SRC-0141 Windsurf, SRC-0142 ZCode, SRC-0143 Zed, SRC-0265 Flutter, SRC-0357 dist / cargo-dist
- **DEFER:** SRC-0129 JetBrains IDE Platform, SRC-0139 Void, SRC-0168 Open VSX
- *Note:* Gap: no desktop agent-workbench shell is in the registry. `pingdotgg/t3code` and `stablyai/orca` (both MIT, live, pushed 2026-10-27) are the most direct quarries and should be added.

### G02 - Agent control plane / orchestration (56 rows)

- **MINE_DEEP:** SRC-0058 Goose - Permission inspector, sessions, ACP/MCP, subagents; Apache-2.0 (moved to aaif-goose org); SRC-0062 OpenCode - Client/server agent split, TUI+desktop clients, provider abstraction; MIT; SRC-0069 OpenAI Codex - Agent loop, app-server protocol, approvals, Windows sandbox; Apache-2.0
- **KEEP_REFERENCE:** SRC-0004 Waza, SRC-0005 KiroCrew, SRC-0009 Microsoft Agent Framework, SRC-0011 LangGraph, SRC-0015 OpenAI Agents SDK, SRC-0053 Claude Code, SRC-0054 Cline, SRC-0055 Continue, SRC-0056 Crush, SRC-0057 GitHub Copilot CLI / Agent, SRC-0059 Hermes Agent, SRC-0060 Kilo Code, SRC-0063 OpenHands, SRC-0064 Pi, SRC-0066 SWE-agent, SRC-0121 Manus, SRC-0164 Eigent, SRC-0165 Kimi / Kimi K3 / Agent Swarm / Kimi Code / Kimi Work / Kimi Skills, SRC-0166 CAMEL, SRC-0288 Composio Agent Orchestrator, SRC-0384 awslabs/cli-agent-orchestrator, SRC-0398 Devin, SRC-0400 DeepSeek Harness, SRC-0401 Cordis, SRC-0402 CommandCode
- **DEFER:** SRC-0002 Relay, SRC-0007 delegate-skills, SRC-0008 Delegate, SRC-0010 AutoGen / Magentic-One, SRC-0012 CrewAI, SRC-0013 Agno, SRC-0014 Google ADK 2.0, SRC-0017 Strands Agents SDK, SRC-0018 MetaGPT, SRC-0019 PydanticAI, SRC-0020 JetBrains Koog, SRC-0065 Roo Code, SRC-0120 OpenManus, SRC-0289 21st-dev/1code, SRC-0291 fynnfluegge/agtx, SRC-0292 morapelker/hive, SRC-0361 Coze Studio, SRC-0362 Eino, SRC-0364 DeerFlow, SRC-0365 smolagents, SRC-0385 open-multi-agent/open-multi-agent, SRC-0386 agentscope-ai/AgentTeams, SRC-0387 RightNow-AI/openfang, SRC-0391 Kocoro-lab/Shannon, SRC-0397 opencrust-org/opencrust
- **REJECT:** SRC-0003 Sema - URL is bare https://github.com/ - unresolvable; re-identify or drop; SRC-0061 OpenAI Codex CLI - Duplicate row of SRC-0069 (same repo) - merge; SRC-0290 kdlbs/kandev - AGPL-3.0
- *Note:* Many overlapping frameworks; mine at most three. OpenHands should be paired with `OpenHands/software-agent-sdk` (absent, MIT). DeepSeek Harness/Cordis stay reference per the registry's negative-oracle flag.

### G03 - Durable workflow (10 rows)

- **MINE_DEEP:** SRC-0110 DBOS - Embedded (library-mode) durable execution on Postgres/SQLite; fits local-first desktop; SRC-0113 Temporal - Reference semantics: deterministic replay, signals, timers, versioning; MIT
- **KEEP_REFERENCE:** SRC-0076 Argo Workflows, SRC-0112 Restate, SRC-0356 statig, SRC-0388 rivet-dev/rivet
- **DEFER:** SRC-0016 petgraph
- **REJECT:** SRC-0111 Inngest - SSPL-1.0 (delayed Apache); DBOS/Temporal/vercel workflow cover need; SRC-0389 dagucloud/dagu - GPL-3.0; covered by permissive durable engines; SRC-0390 orch8-io/engine - BUSL-1.1, 75 stars; covered by DBOS/Temporal
- *Note:* `vercel/workflow` (Apache-2.0, absent) and `vercel-labs/durable-harness` (Apache-2.0, absent; 255 stars) are relevant TypeScript durable-agent quarries; add and compare against DBOS. Restate/Inngest/orch8/dagu are rights-blocked.

### G04 - Terminal / PTY (11 rows)

- **MINE_DEEP:** SRC-0237 node-pty - Node ConPTY/forkpty binding if shell is Electron/Node (used by VS Code); SRC-0238 portable-pty - Rust cross-platform PTY incl. ConPTY; pin-ledger PATH_MINED_PASS1; SRC-0243 xterm.js - De-facto web terminal renderer; addons (fit, webgl, search, serialize)
- **KEEP_REFERENCE:** SRC-0230 Ghostty, SRC-0231 Alacritty, SRC-0239 tmux, SRC-0241 Windows ConPTY, SRC-0242 Windows Job Objects, SRC-0244 Atuin
- **REJECT:** SRC-0232 asciinema - GPL-3.0; record format reference only; SRC-0240 WezTerm - Duplicate row of SRC-0238 (same repo) - merge
- *Note:* Choose between portable-pty (Rust core) and node-pty (Node/Electron shell) once the shell runtime is decided; the other becomes reference.

### G05 - Editor engine (7 rows)

- **MINE_DEEP:** SRC-0135 Monaco Editor - Editor engine of Code-OSS; diff editor; MIT
- **KEEP_REFERENCE:** SRC-0128 Helix, SRC-0131 Kakoune, SRC-0134 Lite XL, SRC-0136 Neovim, SRC-0146 BlockSuite
- **DEFER:** SRC-0127 Emacs
- *Note:* Gap: CodeMirror 6 is not in the registry; consider adding as the lighter alternative to Monaco.

### G06 - Browser / computer use (11 rows)

- **MINE_DEEP:** SRC-0087 Browser Use - LLM-driven browser agent loop; DOM distillation; MIT; SRC-0255 Playwright Test - Browser automation + test runner; CDP/BiDi; trace viewer
- **KEEP_REFERENCE:** SRC-0088 Chrome DevTools Protocol, SRC-0089 FlaUI, SRC-0090 Microsoft UFO, SRC-0092 pywinauto, SRC-0093 Stagehand, SRC-0095 Windows UI Automation, SRC-0096 windows-rs, SRC-0097 Microsoft winappCli
- **DEFER:** SRC-0091 OmniParser
- *Note:* `microsoft/playwright-mcp` (Apache-2.0, absent) is the natural MCP bridge for Playwright. Computer-use eval corpora sit in G13.

### G07 - Design canvas (12 rows)

- **MINE_DEEP:** SRC-0079 OpenPencil - AI-native design editor; MIT; registry S+ design source; SRC-0080 Excalidraw - Whiteboard canvas, scene model, collab-ready; MIT
- **KEEP_REFERENCE:** SRC-0021 Base44, SRC-0022 Lovable, SRC-0078 Figma, SRC-0081 Miro, SRC-0082 Penpot, SRC-0083 v0, SRC-0084 Magic Patterns, SRC-0085 Impeccable, SRC-0094 Storybook
- **DEFER:** SRC-0363 FlowGram
- *Note:* `tldraw/tldraw` is absent and uses the proprietary tldraw licence (commercial licence for production) - do not add as a code quarry.

### G08 - Git / worktree / diff (13 rows)

- **MINE_DEEP:** SRC-0043 gix - Pure-Rust Git (gix); pin-ledger PATH_MINED_PASS1; SRC-0099 Difftastic - Structural (tree-sitter) diff for review surfaces; MIT; SRC-0101 Jujutsu - Operation log / undo / working-copy-as-commit model for recovery
- **KEEP_REFERENCE:** SRC-0100 Git, SRC-0122 GitButler, SRC-0190 Gerrit, SRC-0283 Graphite, SRC-0284 github/gh-stack, SRC-0285 git-town/git-town, SRC-0286 ejoffe/spr, SRC-0287 ezyang/ghstack
- **DEFER:** SRC-0102 libgit2
- **REJECT:** SRC-0103 Mergiraf - GPL-3.0 and a mirror repo (64 stars); use upstream on Codeberg if ever needed
- *Note:* Git CLI remains the effect mechanism (binary invocation). GitButler is behavior-only (FSL).

### G09 - Code intelligence / memory / search (36 rows)

- **MINE_DEEP:** SRC-0046 ripgrep - Fast grep engine + ignore crate (MIT/Unlicense); SRC-0048 Tantivy - Embedded Rust full-text index for local search; SRC-0049 Tree-sitter - Incremental parsing substrate for all code intelligence
- **KEEP_REFERENCE:** SRC-0038 Meta Glean, SRC-0039 Codebase Memory MCP, SRC-0041 Aider Repo Map, SRC-0042 ast-grep, SRC-0045 Obsidian Export, SRC-0047 SQLite / rusqlite, SRC-0051 Zoekt, SRC-0052 Qodo Open Aware, SRC-0144 Salsa, SRC-0184 SCIP, SRC-0186 OpenRewrite, SRC-0193 Joern, SRC-0281 Augment Code, SRC-0293 elara-labs/code-context-engine, SRC-0294 Helweg/opencode-codebase-index, SRC-0295 flupkede/codesearch, SRC-0296 intuit/infigraph, SRC-0299 Microsoft GraphRAG, SRC-0300 Graphiti, SRC-0301 Mem0, SRC-0302 Context7, SRC-0349 Comby, SRC-0350 Codemod, SRC-0351 Soufflé
- **DEFER:** SRC-0040 tree-sitter-graph, SRC-0189 Cohere BinaryVectorDB, SRC-0282 augmentcode/context-connectors, SRC-0303 OpenGrok, SRC-0360 CozoDB
- **REJECT:** SRC-0044 Graphify - Repo 404 (deleted/private); SRC-0050 Universal Ctags - GPL-2.0; superseded by tree-sitter/ripgrep for v3; SRC-0297 giancarloerra/SocratiCode - AGPL-3.0; unverified claims; SRC-0298 PatrickSys/codebase-context - Elastic-2.0 source-available
- *Note:* Large overlap (Zoekt, SCIP, Glean, ast-grep, codebase-memory-mcp, Aider repo map). Keep as reference; mine only the three substrates.

### G10 - MCP / ACP / protocols (13 rows)

- **MINE_DEEP:** SRC-0174 Agent Client Protocol (ACP) - Agent<->client protocol used by Zed/Goose/others; Apache-2.0; has rust/ts SDK repos; SRC-0182 Model Context Protocol (MCP) - Org-level entry: must be re-pinned to spec + rust/typescript SDKs (MIT->Apache-2.0 transition)
- **KEEP_REFERENCE:** SRC-0001 cargo-semver-checks, SRC-0006 AG-UI, SRC-0173 A2A, SRC-0175 Agent Skills, SRC-0176 AGENTS.md, SRC-0178 Debug Adapter Protocol (DAP), SRC-0181 Language Server Protocol (LSP), SRC-0264 JetBrains RD, SRC-0307 Microsoft MCP Gateway, SRC-0392 agentgateway/agentgateway, SRC-0399 Fern
- *Note:* MCP row is org-level only; re-register `modelcontextprotocol/modelcontextprotocol` (spec), `rust-sdk`, `typescript-sdk` with pins. ACP SDK repos `agentclientprotocol/rust-sdk` and `typescript-sdk` exist (Apache-2.0).

### G11 - Sandbox / containment (9 rows)

- **MINE_DEEP:** SRC-0203 NVIDIA OpenShell - Agent sandbox runtime + policy; Apache-2.0; pin-ledger PATH_MINED_PASS1; SRC-0308 Microsoft LiteBox - Windows-capable library-OS isolation research; MIT; pin-ledger PATH_MINED_PASS1
- **KEEP_REFERENCE:** SRC-0145 Firecracker, SRC-0172 WIT, SRC-0198 Extism, SRC-0200 Gemini CLI Sandbox, SRC-0215 Wasmtime, SRC-0309 microsoft/hcsshim, SRC-0310 Alibaba OpenSandbox
- *Note:* Windows primitives (Job Objects, ConPTY, hcsshim) stay reference; Wasmtime stays deferred per pin ledger.

### G12 - Policy engine / authorization (10 rows)

- **MINE_DEEP:** SRC-0032 Cedar for Agents - Cedar schemas/patterns specific to agent tool authorization; SRC-0197 Cedar - Policy language + Rust evaluator; analyzable authorization
- **KEEP_REFERENCE:** SRC-0033 Cedar Local Agent, SRC-0204 Open Policy Agent, SRC-0279 SPIFFE / SPIRE, SRC-0304 OpenFGA, SRC-0305 SpiceDB, SRC-0306 OPAL, SRC-0395 mvar-security/mvar, SRC-0396 oktsec/oktsec
- *Note:* OPA/OpenFGA/SpiceDB/OPAL are enterprise-later references; Cedar is the single policy engine candidate.

### G13 - Review / assurance / eval (56 rows)

- **MINE_DEEP:** SRC-0027 Qodo PR-Agent - Open PR review agent; MIT; repo moved qodo-ai -> The-PR-Agent; SRC-0252 Inspect AI - Eval framework with sandboxed tool tasks; MIT; SRC-0261 Terminal-Bench - Terminal-agent benchmark harness; Apache-2.0
- **KEEP_REFERENCE:** SRC-0024 Qodana, SRC-0025 Qodo Agents, SRC-0026 Greptile, SRC-0028 ReSharper InspectCode / CleanupCode, SRC-0029 CodeRabbit, SRC-0030 Cubic, SRC-0031 Greptile Skills, SRC-0037 actionlint, SRC-0067 SWE-bench mini agents, SRC-0073 Loom, SRC-0074 Shuttle, SRC-0086 axe-core, SRC-0180 JUnit XML, SRC-0183 SARIF, SRC-0192 Miri, SRC-0194 AgentDojo, SRC-0199 garak, SRC-0201 Gitleaks, SRC-0205 Opengrep, SRC-0210 Semgrep CE, SRC-0212 Snyk Agent Scan, SRC-0216 zizmor, SRC-0247 cargo-nextest, SRC-0248 cargo-llvm-cov, SRC-0249 BrowserGym, SRC-0250 cargo-fuzz, SRC-0251 cargo-mutants, SRC-0253 Kani, SRC-0254 OSWorld, SRC-0256 Promptfoo, SRC-0257 proptest, SRC-0258 Schemathesis, SRC-0260 SWE-bench, SRC-0262 WebArena, SRC-0311 ServiceNow WorkArena, SRC-0312 ServiceNow AgentLab, SRC-0313 Windows Agent Arena, SRC-0339 NeMo Guardrails, SRC-0367 Lighthouse, SRC-0368 Web Platform Tests
- **DEFER:** SRC-0259 Stryker, SRC-0328 TLA+, SRC-0329 Apalache, SRC-0330 P language, SRC-0332 Verus, SRC-0333 Prusti, SRC-0337 PyRIT, SRC-0338 LLM Guard, SRC-0366 Pa11y
- **REJECT:** SRC-0211 SkillSpector - Repo 404 (deleted/private); SRC-0263 Qodo Cover - AGPL-3.0; test-gen behavior only; SRC-0314 AutoElicit - Repo 404 - corpus not public at URL; re-locate; SRC-0315 RedTeamCUA - Repo 404 - corpus not public at URL; re-locate
- *Note:* Several 404s (AutoElicit, RedTeamCUA, SkillSpector) need re-location or removal.

### G14 - Collaboration / sync (15 rows)

- **MINE_DEEP:** SRC-0158 Loro - Rust CRDT with history/time-travel; MIT; SRC-0160 Yjs - Most-integrated CRDT (Monaco/Excalidraw/CodeMirror bindings); MIT
- **KEEP_REFERENCE:** SRC-0071 Matrix, SRC-0114 Zulip, SRC-0115 Supabase, SRC-0159 Automerge, SRC-0334 LiveStore, SRC-0335 PGlite, SRC-0336 ElectricSQL
- **DEFER:** SRC-0156 Eclipse Open Collaboration Tools, SRC-0161 Anytype / AnySync
- **REJECT:** SRC-0070 Mattermost - AGPL-3.0 server; chat collab out of v3 core; SRC-0072 Discourse - GPL-2.0; forum software, out of scope; SRC-0116 GraphQL / PostgREST / Realtime patterns - Duplicate row of SRC-0115 (same repo) - merge; SRC-0162 AppFlowy - AGPL-3.0
- *Note:* Mattermost/AppFlowy (AGPL) and Discourse (GPL) rejected; chat/forum collaboration is out of v3 core.

### G15 - Mobile / remote (4 rows)

- **MINE_DEEP:** SRC-0246 Zellij - Session attach/detach, plugin system, web client for remote access; MIT
- **KEEP_REFERENCE:** SRC-0245 Eugeny Tabby, SRC-0266 Wispr Flow, SRC-0267 ElevenLabs UI
- *Note:* Gap: no mobile client or remote-control protocol source in the registry. Zellij is the only live remote-session quarry; consider adding a mobile/remote reference during replan.

### X1 - Adjacent: spec / planning methodology (9 rows)

- **KEEP_REFERENCE:** SRC-0218 Ponytail, SRC-0219 BMAD Method, SRC-0220 CUE, SRC-0221 Gherkin, SRC-0222 GitHub Spec Kit, SRC-0224 MADR, SRC-0225 OpenSpec
- **DEFER:** SRC-0223 Kiro Specs
- **REJECT:** SRC-0226 Task Master - MIT + Commons Clause - not OSI; methodology reference via OpenSpec/Spec Kit

### X2 - Adjacent: model gateway / local inference (9 rows)

- **KEEP_REFERENCE:** SRC-0323 LiteLLM
- **DEFER:** SRC-0068 Tabby, SRC-0163 Cohere / Command / Aya / Rerank concepts, SRC-0322 TensorZero, SRC-0324 Bifrost, SRC-0325 Portkey Gateway, SRC-0326 SGLang, SRC-0327 Candle
- **REJECT:** SRC-0157 TabbyML - Duplicate row of SRC-0068 (same repo) - merge

### X3 - Adjacent: supply chain / compliance scanning (21 rows)

- **KEEP_REFERENCE:** SRC-0098 Cosign, SRC-0104 SLSA, SRC-0105 TUF / rust-tuf, SRC-0106 Witness, SRC-0119 Magika, SRC-0167 ORT, SRC-0177 CycloneDX, SRC-0179 in-toto Attestation, SRC-0185 SPDX, SRC-0195 cargo-audit, SRC-0196 cargo-deny, SRC-0202 Grype, SRC-0206 OpenSSF Scorecard, SRC-0208 OSV-Scanner, SRC-0209 ScanCode Toolkit, SRC-0213 Syft, SRC-0214 Trivy, SRC-0228 GUAC, SRC-0229 Rekor
- **REJECT:** SRC-0077 Renovate - AGPL-3.0; use as hosted bot at most; SRC-0207 OSS Review Toolkit - Duplicate row of SRC-0167 (same repo) - merge

### X4 - Adjacent: observability / runtime evidence (12 rows)

- **DEFER:** SRC-0169 OpenTelemetry Rust, SRC-0171 tracing, SRC-0191 Hud, SRC-0316 Parca, SRC-0318 OpenTelemetry eBPF Profiler, SRC-0319 Microsoft ETW, SRC-0320 Samply, SRC-0321 flamegraph-rs, SRC-0358 Apache DataFusion, SRC-0359 Apache Arrow Rust
- **REJECT:** SRC-0317 Pyroscope - AGPL-3.0; SRC-0340 Arize Phoenix - Elastic-2.0 source-available

### X5 - Adjacent: knowledge / work / research / docs (32 rows)

- **DEFER:** SRC-0023 Gamma, SRC-0107 Docling, SRC-0108 JetBrains Grazie, SRC-0109 JetBrains Writerside, SRC-0147 claude-obsidian, SRC-0148 Obsidian, SRC-0149 Obsidian Skills, SRC-0150 Notion Custom Agents, SRC-0151 AFFiNE, SRC-0187 Perplexity, SRC-0188 Sakana AI Scientist, SRC-0217 Sakana Darwin Gödel Machine, SRC-0268 Tavily, SRC-0269 Tavily Skills / MCP, SRC-0270 Huly, SRC-0271 Microsoft Loop / Teams / Planner, SRC-0272 Coda, SRC-0273 Fibery, SRC-0274 Asana Work Graph / AI Teammates, SRC-0275 Atlassian Teamwork Graph, SRC-0276 Linear, SRC-0278 ChatGPT Work / Projects / Apps / Scheduled Work, SRC-0280 Backstage, SRC-0341 PaperQA2, SRC-0342 FutureHouse Robin, SRC-0343 Crawl4AI, SRC-0346 GROBID, SRC-0347 docling.rs, SRC-0348 Typst
- **REJECT:** SRC-0277 Plane - AGPL-3.0; SRC-0344 Firecrawl - AGPL-3.0 (repo moved to firecrawl org); SRC-0345 SearXNG - AGPL-3.0

### X6 - Adjacent: build / env / language / formal / binary (21 rows)

- **KEEP_REFERENCE:** SRC-0233 Dev Containers
- **DEFER:** SRC-0034 Buck2, SRC-0035 Pants, SRC-0036 Bazel, SRC-0075 Dagger, SRC-0117 Nix, SRC-0118 Pixi, SRC-0123 Harness Open Source, SRC-0152 Biome, SRC-0153 Kotlin Compiler, SRC-0154 Oxc, SRC-0155 Ruff, SRC-0227 JetBrains MPS, SRC-0234 Devbox, SRC-0235 direnv, SRC-0236 mise, SRC-0331 FoundationDB, SRC-0353 Ghidra, SRC-0354 angr, SRC-0355 LIEF
- **REJECT:** SRC-0352 DDisasm - AGPL-3.0

### X7 - Adjacent: Edara adaptive-organization research (17 rows)

- **DEFER:** SRC-0369 FoundationAgents/AFlow, SRC-0370 metauto-ai/GPTSwarm, SRC-0371 SALT-NLP/DyLAN, SRC-0376 lm-sys/RouteLLM, SRC-0377 ulab-uiuc/LLMRouter, SRC-0378 AgentOptimizer/agentopt, SRC-0379 fidelity/mabwiser, SRC-0380 VowpalWabbit/vowpal_wabbit, SRC-0381 google/or-tools, SRC-0382 rust-or/good_lp, SRC-0383 rust-or/highs, SRC-0394 MR9812/BlindGuard
- **REJECT:** SRC-0372 bingreeky/MaAS - No license file (all rights reserved); paper reference only; SRC-0373 wangzx1219/AgentDropout - No license file (all rights reserved); paper reference only; SRC-0374 yanweiyue/AgentPrune - No license file; stale; paper reference only; SRC-0375 ulab-uiuc/GraphPlanner - No license file; 22 stars; paper reference only; SRC-0393 wslong20/G-safeguard - No license file; stale; paper reference only

## 4. Presence check for named projects

| Project | In registry? | Registry row(s) | Live state 2026-10-27 | Licence | HEAD (12) | Proposed action |
|---|---|---|---|---|---|---|
| pingdotgg/t3code | NO | - | LIVE, pushed 2026-10-27, archived=False, 30721 stars | MIT | `36d4d711b79c` | ADD -> G01 MINE_DEEP candidate |
| stablyai/orca | NO | - | LIVE, pushed 2026-10-27, archived=False, 107797 stars | MIT | `dc735050b3c6` | ADD -> G01/G02 MINE_DEEP candidate |
| vercel/workflow | NO | - | LIVE, pushed 2026-10-27, archived=False, 2475 stars | Apache-2.0 | `af8c6d3295eb` | ADD -> G03 MINE_DEEP candidate |
| vercel-labs/durable-harness | NO | - | LIVE, pushed 2026-10-23, archived=False, 255 stars | Apache-2.0 | `ea8aa4060cf4` | ADD -> G03 reference (young, 255 stars) |
| sst/opencode | YES | SRC-0062 | RENAMED -> `anomalyco/opencode`, pushed 2026-10-27, archived=False, 222262 stars | MIT | `7b1e54a74f62` | Present as anomalyco/opencode (redirect) |
| All-Hands-AI/OpenHands | YES | SRC-0063 | RENAMED -> `OpenHands/OpenHands`, pushed 2026-10-27, archived=False, 91999 stars | MIT | `6c120073f5a1` | Present as OpenHands/openhands (redirect) |
| OpenHands/software-agent-sdk | NO | - | LIVE, pushed 2026-10-27, archived=False, 1310 stars | MIT | `f7cbea4ff621` | ADD -> G02 reference paired with SRC-0063 |
| block/goose | YES | SRC-0058 | RENAMED -> `aaif-goose/goose`, pushed 2026-10-27, archived=False, 55818 stars | Apache-2.0 | `398165c9376e` | Present as aaif-goose/goose |
| continuedev/continue | YES | SRC-0055 | LIVE, pushed 2026-10-27, archived=False, 36346 stars | Apache-2.0 | `5522c6f44ca0` | Present; upstream read-only - reference only |
| zed-industries/zed | YES | SRC-0143 | LIVE, pushed 2026-10-27, archived=False, 92286 stars | Mixed: Apache-2.0 / GPL-3.0 / AGPL-3.0 per crate | `37faef81f74f` | Present; rights complex |
| MCP spec repo | YES | SRC-0182 | LIVE, pushed 2026-10-26, archived=False, 9543 stars | MIT->Apache-2.0 transition | `54b91cdb8f21` | Org-level only; ADD exact repo |
| MCP typescript-sdk | YES | SRC-0182 | LIVE, pushed 2026-10-27, archived=False, 13662 stars | MIT->Apache-2.0 transition | `b415e60bdf0e` | Covered only by org row; ADD exact repo |
| MCP python-sdk | YES | SRC-0182 | LIVE, pushed 2026-10-27, archived=False, 24684 stars | MIT | `d7845c073a2b` | Covered only by org row; optional |
| MCP rust-sdk | YES | SRC-0182 | LIVE, pushed 2026-10-26, archived=False, 4058 stars | MIT->Apache-2.0 transition | `cd88056ffdc9` | Covered only by org row; ADD exact repo |
| agentclientprotocol (spec) | YES | SRC-0174 | LIVE, pushed 2026-10-27, archived=False, 4522 stars | Apache-2.0 | `e50f62b4a1ca` | Present |
| ACP typescript-sdk | NO | - | LIVE, pushed 2026-10-26, archived=False, 266 stars | Apache-2.0 | `bca8e4919992` | ADD as child artifact of SRC-0174 |
| ACP rust-sdk | NO | - | LIVE, pushed 2026-10-26, archived=False, 230 stars | Apache-2.0 | `644377ad2654` | ADD as child artifact of SRC-0174 |
| tldraw/tldraw | NO | - | LIVE, pushed 2026-10-27, archived=False, 51110 stars | tldraw licence (proprietary) | `b793bc636610` | Do NOT add as code quarry (proprietary tldraw licence) |
| excalidraw/excalidraw | YES | SRC-0080 | LIVE, pushed 2026-10-27, archived=False, 134652 stars | MIT | `808d068e1826` | Present |
| xtermjs/xterm.js | YES | SRC-0243 | LIVE, pushed 2026-10-27, archived=False, 21297 stars | MIT | `d8a8247dbc11` | Present |
| microsoft/monaco-editor | YES | SRC-0135 | LIVE, pushed 2026-10-26, archived=False, 46901 stars | MIT | `dbf1945df2ff` | Present |
| microsoft/node-pty | YES | SRC-0237 | LIVE, pushed 2026-10-23, archived=False, 2055 stars | MIT | `3d2987da0085` | Present |
| cedar-policy (cedar, cedar-for-agents, cedar-local-agent) | YES | SRC-0197, SRC-0032, SRC-0033 | LIVE, pushed 2026-10-27, archived=False, 1820 stars | Apache-2.0 | `2c2b84772a63` | Present (3 rows) |
| microsoft/playwright | YES | SRC-0255 | LIVE, pushed 2026-10-27, archived=False, 98648 stars | Apache-2.0 | `a169686c61af` | Present |
| microsoft/playwright-mcp | NO | - | LIVE, pushed 2026-10-22, archived=False, 38704 stars | Apache-2.0 | `0c4107acbecb` | ADD as child artifact of SRC-0255 |

Note: `_work/src/` already contains local checkouts named `t3code`, `orca`, `workflow`, `durable-harness`; they are not
registry entries and were not inspected here.

## 5. Full 402-row table

Legend: `live_status` LIVE / RENAMED (-> current path) / 404 / ORG_LEVEL / UNRESOLVABLE / NON_GITHUB. `archived` is the GitHub
flag (`-` when not applicable). `license` is the effective label (API SPDX, or root-LICENSE head where the API said
NOASSERTION/null). `pushed_at` is the last push date. Group codes refer to section 3.

| id | name | url | live_status | archived | license | head_sha | pushed_at | grp | proposed_v3_disposition | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| SRC-0001 | cargo-semver-checks | https://github.com/obi1kenobi/cargo-semver-checks | LIVE | no | Apache-2.0 | `08bef854ab12` | 2026-10-26 | G10 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0002 | Relay | https://relay.ai | NON_GITHUB | - | - | - | - | G02 | DEFER | Closed/defunct product; historical lesson only |
| SRC-0003 | Sema | https://github.com/ | UNRESOLVABLE | - | - | - | - | G02 | REJECT | URL is bare https://github.com/ - unresolvable; re-identify or drop |
| SRC-0004 | Waza | https://github.com/microsoft/waza | LIVE | no | MIT | `8fc8185e52dd` | 2026-10-27 | G02 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0005 | KiroCrew | https://github.com/kirodotdev/KiroCrew | LIVE | no | Apache-2.0 | `cd89e0519486` | 2026-10-27 | G02 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0006 | AG-UI | https://github.com/ag-ui-protocol/ag-ui | LIVE | no | MIT | `2e17b31ef019` | 2026-10-27 | G10 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0007 | delegate-skills | https://github.com/amElnagdy/delegate-skills | LIVE | no | MIT | `3aa72d681a79` | 2026-10-14 | G02 | DEFER | Live, MIT; overlapping orchestration framework - revisit at Edara gate |
| SRC-0008 | Delegate | https://github.com/nikhilgarg28/delegate | LIVE | no | MIT | `a0f3d04cdab0` | 2026-03-22 | G02 | DEFER | Live, MIT; overlapping orchestration framework - revisit at Edara gate |
| SRC-0009 | Microsoft Agent Framework | https://github.com/microsoft/agent-framework | LIVE | no | MIT | `981f70e3c7bb` | 2026-10-27 | G02 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0010 | AutoGen / Magentic-One | https://github.com/microsoft/autogen | LIVE | no | MIT (LICENSE-CODE) + CC-BY-4.0 docs | `004749e6b710` | 2026-10-16 | G02 | DEFER | MIT code; maintenance mode, superseded by Agent Framework |
| SRC-0011 | LangGraph | https://github.com/langchain-ai/langgraph | LIVE | no | MIT | `858891aaa164` | 2026-10-27 | G02 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0012 | CrewAI | https://github.com/crewAIInc/crewAI | LIVE | no | MIT | `c5f996ab6d91` | 2026-10-27 | G02 | DEFER | Live, MIT; overlapping orchestration framework - revisit at Edara gate |
| SRC-0013 | Agno | https://github.com/agno-agi/agno | LIVE | no | Apache-2.0 | `5233c41110cf` | 2026-10-27 | G02 | DEFER | Live, Apache-2.0; overlapping orchestration framework - revisit at Edara gate |
| SRC-0014 | Google ADK 2.0 | https://github.com/google/adk-python | LIVE | no | Apache-2.0 | `2084efbe1b9f` | 2026-10-27 | G02 | DEFER | Live, Apache-2.0; overlapping orchestration framework - revisit at Edara gate |
| SRC-0015 | OpenAI Agents SDK | https://github.com/openai/openai-agents-python | LIVE | no | MIT | `b040da59037b` | 2026-10-27 | G02 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0016 | petgraph | https://github.com/petgraph/petgraph | LIVE | no | Apache-2.0 | `e38de6fed059` | 2026-10-26 | G03 | DEFER | Live, Apache-2.0; overlapping orchestration framework - revisit at Edara gate |
| SRC-0017 | Strands Agents SDK | https://github.com/strands-agents/sdk-python | RENAMED -> strands-agents/harness-sdk | no | Apache-2.0 | `54577596108f` | 2026-10-27 | G02 | DEFER | Live, Apache-2.0; overlapping orchestration framework - revisit at Edara gate (renamed -> strands-agents/harness-sdk) |
| SRC-0018 | MetaGPT | https://github.com/FoundationAgents/MetaGPT | LIVE | no | MIT | `11cdf466d042` | 2026-01-21 | G02 | DEFER | Live, MIT; overlapping orchestration framework - revisit at Edara gate |
| SRC-0019 | PydanticAI | https://github.com/pydantic/pydantic-ai | LIVE | no | MIT | `a61e7a854e3a` | 2026-10-27 | G02 | DEFER | Live, MIT; overlapping orchestration framework - revisit at Edara gate |
| SRC-0020 | JetBrains Koog | https://github.com/JetBrains/koog | LIVE | no | Apache-2.0 | `22e342e033c7` | 2026-10-26 | G02 | DEFER | Live, Apache-2.0; overlapping orchestration framework - revisit at Edara gate |
| SRC-0021 | Base44 | https://base44.com | NON_GITHUB | - | - | - | - | G07 | KEEP_REFERENCE | vendor product page (closed); behavior/spec oracle only |
| SRC-0022 | Lovable | https://lovable.dev | NON_GITHUB | - | - | - | - | G07 | KEEP_REFERENCE | vendor product page (closed); behavior/spec oracle only |
| SRC-0023 | Gamma | https://gamma.app | NON_GITHUB | - | - | - | - | X5 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0024 | Qodana | https://www.jetbrains.com/qodana/ | NON_GITHUB | - | - | - | - | G13 | KEEP_REFERENCE | vendor product page (closed); behavior/spec oracle only |
| SRC-0025 | Qodo Agents | https://github.com/qodo-ai/agents | LIVE | no | MIT | `8fbedb21acd9` | 2026-04-05 | G13 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0026 | Greptile | https://www.greptile.com | NON_GITHUB | - | - | - | - | G13 | KEEP_REFERENCE | Closed product; review behavior oracle |
| SRC-0027 | Qodo PR-Agent | https://github.com/qodo-ai/pr-agent | RENAMED -> The-PR-Agent/pr-agent | no | MIT | `ae053ea8979a` | 2026-10-27 | G13 | MINE_DEEP | Open PR review agent; MIT; repo moved qodo-ai -> The-PR-Agent |
| SRC-0028 | ReSharper InspectCode / CleanupCode | https://www.jetbrains.com/help/resharper/InspectCode.html | NON_GITHUB | - | - | - | - | G13 | KEEP_REFERENCE | vendor product page (closed); behavior/spec oracle only |
| SRC-0029 | CodeRabbit | https://www.coderabbit.ai | NON_GITHUB | - | - | - | - | G13 | KEEP_REFERENCE | Closed product; review behavior oracle |
| SRC-0030 | Cubic | https://www.cubic.dev | NON_GITHUB | - | - | - | - | G13 | KEEP_REFERENCE | Closed product; review behavior oracle |
| SRC-0031 | Greptile Skills | https://github.com/greptileai/skills | LIVE | no | MIT | `4a13eb124ab1` | 2026-10-26 | G13 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0032 | Cedar for Agents | https://github.com/cedar-policy/cedar-for-agents | LIVE | no | Apache-2.0 | `41c07851b933` | 2026-10-22 | G12 | MINE_DEEP | Cedar schemas/patterns specific to agent tool authorization |
| SRC-0033 | Cedar Local Agent | https://github.com/cedar-policy/cedar-local-agent | LIVE | no | Apache-2.0 | `2c971b1c270f` | 2026-05-07 | G12 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0034 | Buck2 | https://github.com/facebook/buck2 | LIVE | no | Apache-2.0 | `b0e7032ba50b` | 2026-10-27 | X6 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0035 | Pants | https://github.com/pantsbuild/pants | LIVE | no | Apache-2.0 | `fc1e5f565b03` | 2026-10-26 | X6 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0036 | Bazel | https://github.com/bazelbuild/bazel | LIVE | no | Apache-2.0 | `bcb0ceca09ad` | 2026-10-27 | X6 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0037 | actionlint | https://github.com/rhysd/actionlint | LIVE | no | MIT | `011a6d15e749` | 2026-07-16 | G13 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0038 | Meta Glean | https://github.com/facebookincubator/Glean | LIVE | no | BSD-3-Clause | `42677f968959` | 2026-10-27 | G09 | KEEP_REFERENCE | Live, BSD-3-Clause; secondary to MINE_DEEP picks |
| SRC-0039 | Codebase Memory MCP | https://github.com/DeusData/codebase-memory-mcp | LIVE | no | MIT | `8530c8cd1c1a` | 2026-10-26 | G09 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0040 | tree-sitter-graph | https://github.com/tree-sitter/tree-sitter-graph | LIVE | no | Apache-2.0 | `b930fb59c217` | 2024-12-11 (stale) | G09 | DEFER | Stale (last push 2024-12) |
| SRC-0041 | Aider Repo Map | https://github.com/Aider-AI/aider | LIVE | no | Apache-2.0 | `5dc9490bb35f` | 2026-05-22 | G09 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0042 | ast-grep | https://github.com/ast-grep/ast-grep | LIVE | no | MIT | `461e7d35ae4d` | 2026-10-27 | G09 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0043 | gix | https://github.com/GitoxideLabs/gitoxide | LIVE | no | Apache-2.0 | `15b71a3a0bfb` | 2026-10-27 | G08 | MINE_DEEP | Pure-Rust Git (gix); pin-ledger PATH_MINED_PASS1 |
| SRC-0044 | Graphify | https://github.com/robert-mcdermott/graphify | 404 | - | - | - | - | G09 | REJECT | Repo 404 (deleted/private) |
| SRC-0045 | Obsidian Export | https://github.com/zoni/obsidian-export | LIVE | no | BSD-style | `87cb4ceb0ae4` | 2026-10-26 | G09 | KEEP_REFERENCE | Live, BSD-style; secondary to MINE_DEEP picks |
| SRC-0046 | ripgrep | https://github.com/BurntSushi/ripgrep | LIVE | no | Unlicense | `6892bc2b7efe` | 2026-10-23 | G09 | MINE_DEEP | Fast grep engine + ignore crate (MIT/Unlicense) |
| SRC-0047 | SQLite / rusqlite | https://github.com/rusqlite/rusqlite | LIVE | no | MIT | `20e5056d6031` | 2026-10-26 | G09 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0048 | Tantivy | https://github.com/quickwit-oss/tantivy | LIVE | no | MIT | `360a5ebbbb6f` | 2026-10-27 | G09 | MINE_DEEP | Embedded Rust full-text index for local search |
| SRC-0049 | Tree-sitter | https://github.com/tree-sitter/tree-sitter | LIVE | no | MIT | `dfe770858e3c` | 2026-10-27 | G09 | MINE_DEEP | Incremental parsing substrate for all code intelligence |
| SRC-0050 | Universal Ctags | https://github.com/universal-ctags/ctags | LIVE | no | GPL-2.0 | `82494361bb3e` | 2026-10-11 | G09 | REJECT | GPL-2.0; superseded by tree-sitter/ripgrep for v3 |
| SRC-0051 | Zoekt | https://github.com/sourcegraph/zoekt | LIVE | no | Apache-2.0 | `a0f878415e04` | 2026-10-27 | G09 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0052 | Qodo Open Aware | https://github.com/qodo-ai/open-aware | LIVE | no | MIT | `68976a9dd957` | 2025-10-29 | G09 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0053 | Claude Code | https://docs.anthropic.com/en/docs/claude-code | NON_GITHUB | - | - | - | - | G02 | KEEP_REFERENCE | Closed product; docs moved to code.claude.com/docs; behavior oracle |
| SRC-0054 | Cline | https://github.com/cline/cline | LIVE | no | Apache-2.0 | `775d03980399` | 2026-10-27 | G02 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0055 | Continue | https://github.com/continuedev/continue | LIVE | no | Apache-2.0 | `5522c6f44ca0` | 2026-10-27 | G02 | KEEP_REFERENCE | Apache-2.0 but README: no longer maintained / read-only; mine failure corpus only |
| SRC-0056 | Crush | https://github.com/charmbracelet/crush | LIVE | no | FSL-1.1-MIT | `3538c722ffce` | 2026-10-27 | G02 | KEEP_REFERENCE | FSL-1.1-MIT source-available: behavior only, no code reuse |
| SRC-0057 | GitHub Copilot CLI / Agent | https://docs.github.com/en/copilot | NON_GITHUB | - | - | - | - | G02 | KEEP_REFERENCE | Closed product docs; behavior oracle |
| SRC-0058 | Goose | https://github.com/aaif-goose/goose | LIVE | no | Apache-2.0 | `398165c9376e` | 2026-10-27 | G02 | MINE_DEEP | Permission inspector, sessions, ACP/MCP, subagents; Apache-2.0 (moved to aaif-goose org) |
| SRC-0059 | Hermes Agent | https://github.com/NousResearch/hermes-agent | LIVE | no | MIT | `e5ea5fd9ccdf` | 2026-10-27 | G02 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0060 | Kilo Code | https://github.com/Kilo-Org/kilocode | LIVE | no | MIT | `d75c029a2985` | 2026-10-27 | G02 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0061 | OpenAI Codex CLI | https://github.com/openai/codex | LIVE | no | Apache-2.0 | `6b56106ed9a3` | 2026-10-27 | G02 | REJECT | Duplicate row of SRC-0069 (same repo) - merge |
| SRC-0062 | OpenCode | https://github.com/anomalyco/opencode | LIVE | no | MIT | `7b1e54a74f62` | 2026-10-27 | G02 | MINE_DEEP | Client/server agent split, TUI+desktop clients, provider abstraction; MIT |
| SRC-0063 | OpenHands | https://github.com/OpenHands/openhands | LIVE | no | MIT | `6c120073f5a1` | 2026-10-27 | G02 | KEEP_REFERENCE | MIT; pair with OpenHands/software-agent-sdk (absent) for SDK mining |
| SRC-0064 | Pi | https://github.com/badlogic/pi-mono | RENAMED -> earendil-works/pi | no | MIT | `72363383ff79` | 2026-10-27 | G02 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks (renamed -> earendil-works/pi) |
| SRC-0065 | Roo Code | https://github.com/RooCodeInc/Roo-Code | LIVE | YES | Apache-2.0 | `b867ec914575` | 2026-05-15 | G02 | DEFER | Archived 2026; historical quarry only (Cline lineage) |
| SRC-0066 | SWE-agent | https://github.com/SWE-agent/SWE-agent | LIVE | no | MIT | `3ea751c087f3` | 2026-10-26 | G02 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0067 | SWE-bench mini agents | https://github.com/swe-bench | ORG_LEVEL | - | - | - | - | G13 | KEEP_REFERENCE | Org-level URL; re-pin to SWE-bench/mini-swe-agent repo |
| SRC-0068 | Tabby | https://github.com/TabbyML/tabby | LIVE | no | Apache-2.0 + proprietary ee/ | `21b29048d7bc` | 2026-06-30 | X2 | DEFER | Apache-2.0 + proprietary ee/; self-hosted completion out of v3 core |
| SRC-0069 | OpenAI Codex | https://github.com/openai/codex | LIVE | no | Apache-2.0 | `6b56106ed9a3` | 2026-10-27 | G02 | MINE_DEEP | Agent loop, app-server protocol, approvals, Windows sandbox; Apache-2.0 |
| SRC-0070 | Mattermost | https://github.com/mattermost/mattermost | LIVE | no | AGPL-3.0 / Apache-2.0 mixed | `e190c0f1e490` | 2026-10-27 | G14 | REJECT | AGPL-3.0 server; chat collab out of v3 core |
| SRC-0071 | Matrix | https://matrix.org | NON_GITHUB | - | - | - | - | G14 | KEEP_REFERENCE | spec/standard site; behavior/spec oracle only |
| SRC-0072 | Discourse | https://github.com/discourse/discourse | LIVE | no | GPL-2.0 | `6691d02e0d8b` | 2026-10-27 | G14 | REJECT | GPL-2.0; forum software, out of scope |
| SRC-0073 | Loom | https://github.com/tokio-rs/loom | LIVE | no | MIT | `948c8cc78b17` | 2026-02-20 | G13 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0074 | Shuttle | https://github.com/awslabs/shuttle | LIVE | no | Apache-2.0 | `fccb2f286522` | 2026-10-27 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0075 | Dagger | https://github.com/dagger/dagger | LIVE | no | Apache-2.0 | `1e085d3fe4aa` | 2026-10-27 | X6 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0076 | Argo Workflows | https://github.com/argoproj/argo-workflows | LIVE | no | Apache-2.0 | `d3b8e91b4f90` | 2026-10-27 | G03 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0077 | Renovate | https://github.com/renovatebot/renovate | LIVE | no | AGPL-3.0 | `78734cb84414` | 2026-10-27 | X3 | REJECT | AGPL-3.0; use as hosted bot at most |
| SRC-0078 | Figma | https://figma.com | NON_GITHUB | - | - | - | - | G07 | KEEP_REFERENCE | Closed product; design behavior oracle |
| SRC-0079 | OpenPencil | https://github.com/open-pencil/open-pencil | LIVE | no | MIT | `992048f91872` | 2026-10-27 | G07 | MINE_DEEP | AI-native design editor; MIT; registry S+ design source |
| SRC-0080 | Excalidraw | https://github.com/excalidraw/excalidraw | LIVE | no | MIT | `808d068e1826` | 2026-10-27 | G07 | MINE_DEEP | Whiteboard canvas, scene model, collab-ready; MIT |
| SRC-0081 | Miro | https://miro.com | NON_GITHUB | - | - | - | - | G07 | KEEP_REFERENCE | vendor product page (closed); behavior/spec oracle only |
| SRC-0082 | Penpot | https://github.com/penpot/penpot | LIVE | no | MPL-2.0 | `f6f9df9a1a94` | 2026-10-27 | G07 | KEEP_REFERENCE | MPL-2.0 file-level copyleft; design-system behavior reference |
| SRC-0083 | v0 | https://v0.dev | NON_GITHUB | - | - | - | - | G07 | KEEP_REFERENCE | Closed product; generation behavior oracle |
| SRC-0084 | Magic Patterns | https://www.magicpatterns.com | NON_GITHUB | - | - | - | - | G07 | KEEP_REFERENCE | vendor product page (closed); behavior/spec oracle only |
| SRC-0085 | Impeccable | https://github.com/pbakaus/impeccable | LIVE | no | Apache-2.0 | `d34c87e1a009` | 2026-10-27 | G07 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0086 | axe-core | https://github.com/dequelabs/axe-core | LIVE | no | MPL-2.0 | `6b52b841461b` | 2026-10-26 | G13 | KEEP_REFERENCE | MPL-2.0; use unmodified as a11y checker dependency |
| SRC-0087 | Browser Use | https://github.com/browser-use/browser-use | LIVE | no | MIT | `2cc71890e650` | 2026-10-27 | G06 | MINE_DEEP | LLM-driven browser agent loop; DOM distillation; MIT |
| SRC-0088 | Chrome DevTools Protocol | https://chromedevtools.github.io/devtools-protocol/ | NON_GITHUB | - | - | - | - | G06 | KEEP_REFERENCE | Protocol spec (Playwright/Browser Use build on it) |
| SRC-0089 | FlaUI | https://github.com/FlaUI/FlaUI | LIVE | no | MIT | `fd7cc64ab019` | 2026-08-13 | G06 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0090 | Microsoft UFO | https://github.com/microsoft/UFO | LIVE | no | MIT | `eae3c0a8d168` | 2026-10-23 | G06 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0091 | OmniParser | https://github.com/microsoft/OmniParser | LIVE | no | CC-BY-4.0 (models mixed) - VERIFY | `354021201345` | 2026-07-20 | G06 | DEFER | CC-BY-4.0 + model-weight licence questions; VERIFY before use |
| SRC-0092 | pywinauto | https://github.com/pywinauto/pywinauto | LIVE | no | BSD-3-Clause | `ecd3276df609` | 2026-10-23 | G06 | KEEP_REFERENCE | Live, BSD-3-Clause; secondary to MINE_DEEP picks |
| SRC-0093 | Stagehand | https://github.com/browserbase/stagehand | LIVE | no | MIT | `63078cf85ddf` | 2026-10-27 | G06 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0094 | Storybook | https://github.com/storybookjs/storybook | LIVE | no | MIT | `b18e7e47f984` | 2026-10-27 | G07 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0095 | Windows UI Automation | https://learn.microsoft.com/windows/win32/winauto/entry-uiauto-win32 | NON_GITHUB | - | - | - | - | G06 | KEEP_REFERENCE | Windows platform API docs |
| SRC-0096 | windows-rs | https://github.com/microsoft/windows-rs | LIVE | no | Apache-2.0 | `d6443f28190f` | 2026-10-27 | G06 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0097 | Microsoft winappCli | https://github.com/microsoft/winappCli | LIVE | no | MIT | `aa0113a6f4ff` | 2026-10-27 | G06 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0098 | Cosign | https://github.com/sigstore/cosign | LIVE | no | Apache-2.0 | `ef56e6999cda` | 2026-10-26 | X3 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0099 | Difftastic | https://github.com/Wilfred/difftastic | LIVE | no | MIT | `0b92338c6042` | 2026-10-26 | G08 | MINE_DEEP | Structural (tree-sitter) diff for review surfaces; MIT |
| SRC-0100 | Git | https://github.com/git/git | LIVE | no | GPL-2.0-only | `37b3475fb530` | 2026-10-26 | G08 | KEEP_REFERENCE | GPL-2.0; invoke as binary (canonical effect mechanism), no code reuse |
| SRC-0101 | Jujutsu | https://github.com/jj-vcs/jj | LIVE | no | Apache-2.0 | `531b68204688` | 2026-10-27 | G08 | MINE_DEEP | Operation log / undo / working-copy-as-commit model for recovery |
| SRC-0102 | libgit2 | https://github.com/libgit2/libgit2 | LIVE | no | GPL-2.0 WITH linking-exception | `42a89d7cc937` | 2026-10-16 | G08 | DEFER | GPL-2.0 w/ linking exception; gix preferred |
| SRC-0103 | Mergiraf | https://github.com/qundao/mirror-mergiraf | LIVE | no | GPL-3.0 | `2b9a722cbcd8` | 2026-10-20 | G08 | REJECT | GPL-3.0 and a mirror repo (64 stars); use upstream on Codeberg if ever needed |
| SRC-0104 | SLSA | https://slsa.dev/ | NON_GITHUB | - | - | - | - | X3 | KEEP_REFERENCE | Provenance framework spec |
| SRC-0105 | TUF / rust-tuf | https://github.com/theupdateframework/rust-tuf | LIVE | no | Apache-2.0 | `219ca7d05818` | 2026-08-24 | X3 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0106 | Witness | https://github.com/in-toto/witness | LIVE | no | Apache-2.0 | `1eaafd56616b` | 2026-10-26 | X3 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0107 | Docling | https://github.com/docling-project/docling | LIVE | no | MIT | `103edefc99a3` | 2026-10-27 | X5 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0108 | JetBrains Grazie | https://www.jetbrains.com/grazie/ | NON_GITHUB | - | - | - | - | X5 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0109 | JetBrains Writerside | https://www.jetbrains.com/writerside/ | NON_GITHUB | - | - | - | - | X5 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0110 | DBOS | https://github.com/dbos-inc/dbos-transact-py | LIVE | no | MIT | `2873b8c22ba2` | 2026-10-27 | G03 | MINE_DEEP | Embedded (library-mode) durable execution on Postgres/SQLite; fits local-first desktop |
| SRC-0111 | Inngest | https://github.com/inngest/inngest | LIVE | no | SSPL-1.0 (Apache-2.0 future) | `e7d0e0ab8360` | 2026-10-27 | G03 | REJECT | SSPL-1.0 (delayed Apache); DBOS/Temporal/vercel workflow cover need |
| SRC-0112 | Restate | https://github.com/restatedev/restate | LIVE | no | BUSL-1.1 | `d188f08a3baf` | 2026-10-27 | G03 | KEEP_REFERENCE | BUSL-1.1: durable-execution behavior only; no code reuse |
| SRC-0113 | Temporal | https://github.com/temporalio/temporal | LIVE | no | MIT | `f7ca7c3c4931` | 2026-10-27 | G03 | MINE_DEEP | Reference semantics: deterministic replay, signals, timers, versioning; MIT |
| SRC-0114 | Zulip | https://github.com/zulip/zulip | LIVE | no | Apache-2.0 | `3e9bc1e13f70` | 2026-10-27 | G14 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0115 | Supabase | https://github.com/supabase/supabase | LIVE | no | Apache-2.0 | `7f7ebf527b1e` | 2026-10-27 | G14 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0116 | GraphQL / PostgREST / Realtime patterns | https://github.com/supabase/supabase | LIVE | no | Apache-2.0 | `7f7ebf527b1e` | 2026-10-27 | G14 | REJECT | Duplicate row of SRC-0115 (same repo) - merge |
| SRC-0117 | Nix | https://github.com/NixOS/nix | LIVE | no | LGPL-2.1 | `0130f9ce8cdb` | 2026-10-27 | X6 | DEFER | LGPL-2.1; reproducibility reference, not v3 core |
| SRC-0118 | Pixi | https://github.com/prefix-dev/pixi | LIVE | no | BSD-3-Clause | `aa97f0a9e67e` | 2026-10-27 | X6 | DEFER | Live, BSD-3-Clause; outside v3 capability list |
| SRC-0119 | Magika | https://github.com/google/magika | LIVE | no | Apache-2.0 | `8d3d3b9b9452` | 2026-10-23 | X3 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0120 | OpenManus | https://github.com/FoundationAgents/OpenManus | LIVE | no | MIT | `3309bf4e416f` | 2026-09-30 | G02 | DEFER | Live, MIT; overlapping orchestration framework - revisit at Edara gate |
| SRC-0121 | Manus | https://manus.im | NON_GITHUB | - | - | - | - | G02 | KEEP_REFERENCE | vendor product page (closed); behavior/spec oracle only |
| SRC-0122 | GitButler | https://github.com/gitbutlerapp/gitbutler | LIVE | no | FSL-1.1-MIT | `9695908f3943` | 2026-10-27 | G08 | KEEP_REFERENCE | FSL-1.1-MIT: virtual-branch/workspace behavior only; no code reuse |
| SRC-0123 | Harness Open Source | https://github.com/harness/harness | LIVE | no | Apache-2.0 | `01a8d2f639a8` | 2026-10-27 | X6 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0124 | Code - OSS | https://github.com/microsoft/vscode | LIVE | no | MIT | `502cb7d77e4e` | 2026-10-27 | G01 | MINE_DEEP | Workbench layout, extension host, terminal/editor integration patterns (MIT) |
| SRC-0125 | Cursor | https://docs.cursor.com/ | NON_GITHUB | - | - | - | - | G01 | KEEP_REFERENCE | Closed product; docs now at cursor.com/docs; behavior oracle |
| SRC-0126 | Eclipse Theia | https://github.com/eclipse-theia/theia | LIVE | no | EPL-2.0 | `f47c3ea8a4ad` | 2026-10-27 | G01 | KEEP_REFERENCE | EPL-2.0 weak copyleft; Theia AI/IDE framework behavior reference |
| SRC-0127 | Emacs | https://git.savannah.gnu.org/cgit/emacs.git | NON_GITHUB | - | - | - | - | G05 | DEFER | GPL-3.0 (savannah cgit; 502 on spot-check); editor reference only |
| SRC-0128 | Helix | https://github.com/helix-editor/helix | LIVE | no | MPL-2.0 | `ba40e547426b` | 2026-09-29 | G05 | KEEP_REFERENCE | MPL-2.0; modal editing/LSP client reference |
| SRC-0129 | JetBrains IDE Platform | https://github.com/JetBrains/intellij-community | LIVE | no | JetBrains build terms at root (source headers Apache-2.0) - VERIFY | `c50523cd5d94` | 2026-10-27 | G01 | DEFER | Root LICENSE now JetBrains build terms; JVM platform out of v3 stack - VERIFY rights |
| SRC-0130 | Junie | https://junie.jetbrains.com/docs/ | NON_GITHUB | - | - | - | - | G01 | KEEP_REFERENCE | Closed agent; behavior oracle |
| SRC-0131 | Kakoune | https://github.com/mawww/kakoune | LIVE | no | Unlicense | `4d4ee86c2d03` | 2026-10-11 | G05 | KEEP_REFERENCE | Live, Unlicense; secondary to MINE_DEEP picks |
| SRC-0132 | Kiro | https://kiro.dev/docs/ | NON_GITHUB | - | - | - | - | G01 | KEEP_REFERENCE | Closed IDE; spec/hooks/powers behavior oracle |
| SRC-0133 | Lapce | https://github.com/lapce/lapce | LIVE | no | Apache-2.0 | `f66ffaa95387` | 2026-10-09 | G01 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0134 | Lite XL | https://github.com/lite-xl/lite-xl | LIVE | no | MIT | `234fa0998016` | 2026-03-11 | G05 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0135 | Monaco Editor | https://github.com/microsoft/monaco-editor | LIVE | no | MIT | `dbf1945df2ff` | 2026-10-26 | G05 | MINE_DEEP | Editor engine of Code-OSS; diff editor; MIT |
| SRC-0136 | Neovim | https://github.com/neovim/neovim | LIVE | no | Apache-2.0 + Vim | `54f94d6fc4ec` | 2026-10-27 | G05 | KEEP_REFERENCE | Live, Apache-2.0 + Vim; secondary to MINE_DEEP picks |
| SRC-0137 | Pulsar | https://github.com/pulsar-edit/pulsar | LIVE | no | MIT | `e88d8d9ab7b5` | 2026-10-27 | G01 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0138 | Replit | https://docs.replit.com/ | NON_GITHUB | - | - | - | - | G01 | KEEP_REFERENCE | Closed product; behavior oracle |
| SRC-0139 | Void | https://github.com/voideditor/void | LIVE | YES | Apache-2.0 | `b3166e7ef2ae` | 2026-06-02 | G01 | DEFER | Archived 2026; historical Code-OSS fork quarry |
| SRC-0140 | VSCodium | https://github.com/VSCodium/vscodium | LIVE | no | MIT | `081f269dd2cd` | 2026-10-26 | G01 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0141 | Windsurf | https://docs.windsurf.com/ | NON_GITHUB | - | - | - | - | G01 | KEEP_REFERENCE | Closed; docs.windsurf.com now redirects to docs.devin.ai/desktop - merge with Devin |
| SRC-0142 | ZCode | https://zcode.z.ai/ | NON_GITHUB | - | - | - | - | G01 | KEEP_REFERENCE | Closed product; behavior oracle |
| SRC-0143 | Zed | https://github.com/zed-industries/zed | LIVE | no | Mixed: Apache-2.0 / GPL-3.0 / AGPL-3.0 per crate | `37faef81f74f` | 2026-10-27 | G01 | KEEP_REFERENCE | ACP/agent panel behavior; mixed GPL/AGPL/Apache crates - path-level rights only |
| SRC-0144 | Salsa | https://github.com/salsa-rs/salsa | LIVE | no | Apache-2.0 | `8e61e5b47b99` | 2026-10-27 | G09 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0145 | Firecracker | https://github.com/firecracker-microvm/firecracker | LIVE | no | Apache-2.0 | `00860f10ae6e` | 2026-10-27 | G11 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0146 | BlockSuite | https://github.com/toeverything/blocksuite | LIVE | no | MPL-2.0 | `5cb5cb68471c` | 2026-10-22 | G05 | KEEP_REFERENCE | MPL-2.0; block editor reference |
| SRC-0147 | claude-obsidian | https://github.com/AgriciDaniel/claude-obsidian | LIVE | no | MIT | `2e545563172f` | 2026-10-25 | X5 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0148 | Obsidian | https://obsidian.md | NON_GITHUB | - | - | - | - | X5 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0149 | Obsidian Skills | https://github.com/kepano/obsidian-skills | LIVE | no | MIT | `3ccff5338ea7` | 2026-09-15 | X5 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0150 | Notion Custom Agents | https://notion.so | NON_GITHUB | - | - | - | - | X5 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0151 | AFFiNE | https://github.com/toeverything/AFFiNE | LIVE | no | MIT + proprietary backend dirs | `8cef09e1dd62` | 2026-10-27 | X5 | DEFER | MIT + proprietary backend dirs; knowledge workspace out of v3 core |
| SRC-0152 | Biome | https://github.com/biomejs/biome | LIVE | no | Apache-2.0 | `b30a85cf2eaf` | 2026-10-27 | X6 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0153 | Kotlin Compiler | https://github.com/JetBrains/kotlin | LIVE | no | Apache-2.0 (license/ dir, not API-detected) | `065bf70a72cc` | 2026-10-27 | X6 | DEFER | Live, Apache-2.0 (license/ dir, not API-detected); outside v3 capability list |
| SRC-0154 | Oxc | https://github.com/oxc-project/oxc | LIVE | no | MIT | `49fbffbfe4f0` | 2026-10-27 | X6 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0155 | Ruff | https://github.com/astral-sh/ruff | LIVE | no | MIT | `691b60a3f3bc` | 2026-10-27 | X6 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0156 | Eclipse Open Collaboration Tools | https://github.com/eclipse-oct | ORG_LEVEL | - | - | - | - | G14 | DEFER | Org-level URL; live-session collab later |
| SRC-0157 | TabbyML | https://github.com/TabbyML/tabby | LIVE | no | Apache-2.0 + proprietary ee/ | `21b29048d7bc` | 2026-06-30 | X2 | REJECT | Duplicate row of SRC-0068 (same repo) - merge |
| SRC-0158 | Loro | https://github.com/loro-dev/loro | LIVE | no | MIT | `75e4bf2bf01c` | 2026-10-23 | G14 | MINE_DEEP | Rust CRDT with history/time-travel; MIT |
| SRC-0159 | Automerge | https://github.com/automerge/automerge | LIVE | no | MIT | `5bae7757ef7b` | 2026-10-26 | G14 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0160 | Yjs | https://github.com/yjs/yjs | LIVE | no | MIT | `0e0dc3401b97` | 2026-10-23 | G14 | MINE_DEEP | Most-integrated CRDT (Monaco/Excalidraw/CodeMirror bindings); MIT |
| SRC-0161 | Anytype / AnySync | https://github.com/anyproto | ORG_LEVEL | - | - | - | - | G14 | DEFER | Org-level URL; local-first knowledge later |
| SRC-0162 | AppFlowy | https://github.com/AppFlowy-IO/AppFlowy | LIVE | no | AGPL-3.0 | `5cf3a365dec0` | 2026-10-27 | G14 | REJECT | AGPL-3.0 |
| SRC-0163 | Cohere / Command / Aya / Rerank concepts | https://cohere.com | NON_GITHUB | - | - | - | - | X2 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0164 | Eigent | https://github.com/eigent-ai/eigent | LIVE | no | Apache-2.0 | `a46f680ea220` | 2026-10-27 | G02 | KEEP_REFERENCE | Apache-2.0; registry highest-priority pair with CAMEL - mine at Edara gate, not v3 core |
| SRC-0165 | Kimi / Kimi K3 / Agent Swarm / Kimi Code / Kimi Work / Kimi Skills | https://www.kimi.com | NON_GITHUB | - | - | - | - | G02 | KEEP_REFERENCE | vendor product page (closed); behavior/spec oracle only |
| SRC-0166 | CAMEL | https://github.com/camel-ai/camel | LIVE | no | Apache-2.0 | `64b9a613d1c3` | 2026-10-27 | G02 | KEEP_REFERENCE | Apache-2.0; Eigent lineage (camel-ai 0.2.91a5) - commit pin still pending |
| SRC-0167 | ORT | https://github.com/oss-review-toolkit/ort | LIVE | no | Apache-2.0 | `ea8163b06da4` | 2026-10-27 | X3 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0168 | Open VSX | https://github.com/eclipse/openvsx | RENAMED -> eclipse-openvsx/openvsx | no | EPL-2.0 | `5aaf44455aa8` | 2026-10-27 | G01 | DEFER | EPL-2.0; extension marketplace only needed if v3 hosts VS Code extensions |
| SRC-0169 | OpenTelemetry Rust | https://github.com/open-telemetry/opentelemetry-rust | LIVE | no | Apache-2.0 | `740db318e515` | 2026-10-27 | X4 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0170 | Tauri 2 | https://github.com/tauri-apps/tauri | LIVE | no | Apache-2.0 | `7e39750cf6a4` | 2026-10-27 | G01 | MINE_DEEP | Rust desktop shell; IPC/capabilities/updater; pin-ledger PATH_MINED_PASS1 |
| SRC-0171 | tracing | https://github.com/tokio-rs/tracing | LIVE | no | MIT | `9d0e557728ec` | 2026-10-09 | X4 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0172 | WIT | https://github.com/WebAssembly/component-model | LIVE | no | Apache-2.0 | `8505ba73dda2` | 2026-10-27 | G11 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0173 | A2A | https://github.com/a2aproject/A2A | LIVE | no | Apache-2.0 | `98279d623163` | 2026-10-21 | G10 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0174 | Agent Client Protocol (ACP) | https://github.com/agentclientprotocol/agent-client-protocol | LIVE | no | Apache-2.0 | `e50f62b4a1ca` | 2026-10-27 | G10 | MINE_DEEP | Agent<->client protocol used by Zed/Goose/others; Apache-2.0; has rust/ts SDK repos |
| SRC-0175 | Agent Skills | https://agentskills.io/ | NON_GITHUB | - | - | - | - | G10 | KEEP_REFERENCE | Open format spec (skills) |
| SRC-0176 | AGENTS.md | https://agents.md/ | NON_GITHUB | - | - | - | - | G10 | KEEP_REFERENCE | Open convention spec |
| SRC-0177 | CycloneDX | https://cyclonedx.org/ | NON_GITHUB | - | - | - | - | X3 | KEEP_REFERENCE | SBOM standard |
| SRC-0178 | Debug Adapter Protocol (DAP) | https://microsoft.github.io/debug-adapter-protocol/ | NON_GITHUB | - | - | - | - | G10 | KEEP_REFERENCE | Protocol spec |
| SRC-0179 | in-toto Attestation | https://github.com/in-toto/attestation | LIVE | no | Apache-2.0 | `50bf01716982` | 2026-10-26 | X3 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0180 | JUnit XML | https://github.com/testmoapp/junitxml | LIVE | no | NONE | `1bcb6fb8b620` | 2023-01-17 (stale) | G13 | KEEP_REFERENCE | Format documentation only; no license, stale since 2023 |
| SRC-0181 | Language Server Protocol (LSP) | https://microsoft.github.io/language-server-protocol/ | NON_GITHUB | - | - | - | - | G10 | KEEP_REFERENCE | Protocol spec |
| SRC-0182 | Model Context Protocol (MCP) | https://github.com/modelcontextprotocol | ORG_LEVEL | - | - | - | - | G10 | MINE_DEEP | Org-level entry: must be re-pinned to spec + rust/typescript SDKs (MIT->Apache-2.0 transition) |
| SRC-0183 | SARIF | https://docs.oasis-open.org/sarif/sarif/v2.1.0/ | NON_GITHUB | - | - | - | - | G13 | KEEP_REFERENCE | OASIS standard - finding interchange |
| SRC-0184 | SCIP | https://github.com/scip-code/scip | LIVE | no | Apache-2.0 | `d556dd3c24b3` | 2026-10-27 | G09 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0185 | SPDX | https://spdx.dev/ | NON_GITHUB | - | - | - | - | X3 | KEEP_REFERENCE | SBOM/licence standard |
| SRC-0186 | OpenRewrite | https://github.com/openrewrite/rewrite | LIVE | no | Apache-2.0 | `a0a942e9124a` | 2026-10-27 | G09 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0187 | Perplexity | https://www.perplexity.ai | NON_GITHUB | - | - | - | - | X5 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0188 | Sakana AI Scientist | https://sakana.ai/ai-scientist/ | NON_GITHUB | - | - | - | - | X5 | DEFER | research/paper page; outside v3 capability list |
| SRC-0189 | Cohere BinaryVectorDB | https://github.com/cohere-ai/BinaryVectorDB | LIVE | no | Apache-2.0 | `c337615e5e0a` | 2024-05-17 (stale) | G09 | DEFER | Stale (last push 2024-05) |
| SRC-0190 | Gerrit | https://github.com/GerritCodeReview/gerrit | LIVE | no | Apache-2.0 | `51294e6b72a1` | 2026-10-27 | G08 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0191 | Hud | https://www.hud.io | NON_GITHUB | - | - | - | - | X4 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0192 | Miri | https://github.com/rust-lang/miri | LIVE | no | Apache-2.0 | `79c8b3a987ac` | 2026-10-27 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0193 | Joern | https://github.com/joernio/joern | LIVE | no | Apache-2.0 | `9fd178db7bca` | 2026-10-27 | G09 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0194 | AgentDojo | https://github.com/ethz-spylab/agentdojo | LIVE | no | MIT | `089ed468cf3e` | 2026-06-02 | G13 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0195 | cargo-audit | https://github.com/rustsec/rustsec/tree/main/cargo-audit | LIVE | no | Apache-2.0 OR MIT (crate manifests; unverified) | `af72bfab4ac8` | 2026-10-26 | X3 | KEEP_REFERENCE | Live, Apache-2.0 OR MIT (crate manifests; unverified); secondary to MINE_DEEP picks |
| SRC-0196 | cargo-deny | https://github.com/EmbarkStudios/cargo-deny | LIVE | no | Apache-2.0 | `2ab89dcdbedd` | 2026-10-26 | X3 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0197 | Cedar | https://github.com/cedar-policy/cedar | LIVE | no | Apache-2.0 | `2c2b84772a63` | 2026-10-27 | G12 | MINE_DEEP | Policy language + Rust evaluator; analyzable authorization |
| SRC-0198 | Extism | https://github.com/extism/extism | LIVE | no | BSD-3-Clause | `051b765bb6ab` | 2026-10-09 | G11 | KEEP_REFERENCE | Live, BSD-3-Clause; secondary to MINE_DEEP picks |
| SRC-0199 | garak | https://github.com/NVIDIA/garak | LIVE | no | Apache-2.0 | `d6a8be1d07de` | 2026-10-23 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0200 | Gemini CLI Sandbox | https://github.com/google-gemini/gemini-cli | LIVE | no | Apache-2.0 | `363a13119a57` | 2026-10-27 | G11 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0201 | Gitleaks | https://github.com/gitleaks/gitleaks | LIVE | no | MIT | `5f6ec56cfa6f` | 2026-10-23 | G13 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0202 | Grype | https://github.com/anchore/grype | LIVE | no | Apache-2.0 | `882c0aba4052` | 2026-10-27 | X3 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0203 | NVIDIA OpenShell | https://github.com/NVIDIA/OpenShell | LIVE | no | Apache-2.0 | `bd2ecaf1526c` | 2026-10-27 | G11 | MINE_DEEP | Agent sandbox runtime + policy; Apache-2.0; pin-ledger PATH_MINED_PASS1 |
| SRC-0204 | Open Policy Agent | https://github.com/open-policy-agent/opa | LIVE | no | Apache-2.0 | `21c9f6de5fb5` | 2026-10-27 | G12 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0205 | Opengrep | https://github.com/opengrep/opengrep | LIVE | no | LGPL-2.1 | `398a063da1f2` | 2026-10-27 | G13 | KEEP_REFERENCE | LGPL-2.1; invoke as external scanner |
| SRC-0206 | OpenSSF Scorecard | https://github.com/ossf/scorecard | LIVE | no | Apache-2.0 | `83b2069eee6e` | 2026-10-27 | X3 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0207 | OSS Review Toolkit | https://github.com/oss-review-toolkit/ort | LIVE | no | Apache-2.0 | `ea8163b06da4` | 2026-10-27 | X3 | REJECT | Duplicate row of SRC-0167 (same repo) - merge |
| SRC-0208 | OSV-Scanner | https://github.com/google/osv-scanner | LIVE | no | Apache-2.0 | `8748c7ca24ec` | 2026-10-27 | X3 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0209 | ScanCode Toolkit | https://github.com/aboutcode-org/scancode-toolkit | LIVE | no | Apache-2.0 + CC-BY-4.0 data | `f356c8fc039e` | 2026-10-26 | X3 | KEEP_REFERENCE | Live, Apache-2.0 + CC-BY-4.0 data; secondary to MINE_DEEP picks |
| SRC-0210 | Semgrep CE | https://github.com/semgrep/semgrep | LIVE | no | LGPL-2.1 | `087e93b3a1fd` | 2026-10-27 | G13 | KEEP_REFERENCE | LGPL-2.1; invoke as external scanner |
| SRC-0211 | SkillSpector | https://github.com/Agent-Hellboy/SkillSpector | 404 | - | - | - | - | G13 | REJECT | Repo 404 (deleted/private) |
| SRC-0212 | Snyk Agent Scan | https://github.com/snyk/agent-scan | LIVE | no | Apache-2.0 | `a8c8c5879a00` | 2026-10-27 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0213 | Syft | https://github.com/anchore/syft | LIVE | no | Apache-2.0 | `fb56f1eef190` | 2026-10-26 | X3 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0214 | Trivy | https://github.com/aquasecurity/trivy | LIVE | no | Apache-2.0 | `d18962e8f817` | 2026-10-27 | X3 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0215 | Wasmtime | https://github.com/bytecodealliance/wasmtime | LIVE | no | Apache-2.0 | `ec63b69f3da9` | 2026-10-27 | G11 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0216 | zizmor | https://github.com/woodruffw/zizmor | RENAMED -> zizmorcore/zizmor | no | MIT | `dc2209b6b6d7` | 2026-10-26 | G13 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks (renamed -> zizmorcore/zizmor) |
| SRC-0217 | Sakana Darwin Gödel Machine | https://sakana.ai/dgm/ | NON_GITHUB | - | - | - | - | X5 | DEFER | research/paper page; outside v3 capability list |
| SRC-0218 | Ponytail | https://github.com/DietrichGebert/ponytail | LIVE | no | MIT | `09c434ab73ca` | 2026-10-18 | X1 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0219 | BMAD Method | https://github.com/bmad-code-org/BMAD-METHOD | LIVE | no | MIT | `61e01f82644c` | 2026-10-20 | X1 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0220 | CUE | https://github.com/cue-lang/cue | LIVE | no | Apache-2.0 | `fd5988ba2177` | 2026-10-26 | X1 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0221 | Gherkin | https://github.com/cucumber/gherkin | LIVE | no | MIT | `b5c83591754d` | 2026-10-27 | X1 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0222 | GitHub Spec Kit | https://github.com/github/spec-kit | LIVE | no | MIT | `ee94598c3c87` | 2026-10-26 | X1 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0223 | Kiro Specs | https://kiro.dev/docs/specs/ | NON_GITHUB | - | - | - | - | X1 | DEFER | docs/spec; outside v3 capability list |
| SRC-0224 | MADR | https://github.com/adr/madr | LIVE | no | MIT OR CC0-1.0 | `ba75bb1b20d4` | 2026-08-28 | X1 | KEEP_REFERENCE | Live, MIT OR CC0-1.0; secondary to MINE_DEEP picks |
| SRC-0225 | OpenSpec | https://github.com/Fission-AI/OpenSpec | LIVE | no | MIT | `6d04a1b58ded` | 2026-10-27 | X1 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0226 | Task Master | https://github.com/eyaltoledano/claude-task-master | LIVE | no | MIT + Commons Clause | `c0c98d367c55` | 2026-04-28 | X1 | REJECT | MIT + Commons Clause - not OSI; methodology reference via OpenSpec/Spec Kit |
| SRC-0227 | JetBrains MPS | https://github.com/JetBrains/MPS | LIVE | no | Apache-2.0 | `2ae351c4fc10` | 2026-10-27 | X6 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0228 | GUAC | https://github.com/guacsec/guac | LIVE | no | Apache-2.0 | `a3f0a4df51ab` | 2026-10-26 | X3 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0229 | Rekor | https://github.com/sigstore/rekor | LIVE | no | Apache-2.0 | `b939d42f0a21` | 2026-10-26 | X3 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0230 | Ghostty | https://github.com/ghostty-org/ghostty | LIVE | no | MIT | `d87c497aff31` | 2026-10-27 | G04 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0231 | Alacritty | https://github.com/alacritty/alacritty | LIVE | no | Apache-2.0 | `bbb2cbf9470a` | 2026-10-26 | G04 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0232 | asciinema | https://github.com/asciinema/asciinema | LIVE | no | GPL-3.0 | `cf66ef4c9b01` | 2026-10-27 | G04 | REJECT | GPL-3.0; record format reference only |
| SRC-0233 | Dev Containers | https://github.com/devcontainers/spec | LIVE | no | CC-BY-4.0 | `c95ffeed1d05` | 2026-03-20 | X6 | KEEP_REFERENCE | Dev container spec (CC-BY-4.0 text); env reproducibility |
| SRC-0234 | Devbox | https://github.com/jetify-com/devbox | LIVE | no | Apache-2.0 | `28c07cf12823` | 2026-10-26 | X6 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0235 | direnv | https://github.com/direnv/direnv | LIVE | no | MIT | `3d0b4ae1ed83` | 2026-10-26 | X6 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0236 | mise | https://github.com/jdx/mise | LIVE | no | MIT | `3f0b767f12f7` | 2026-10-27 | X6 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0237 | node-pty | https://github.com/microsoft/node-pty | LIVE | no | MIT | `3d2987da0085` | 2026-10-23 | G04 | MINE_DEEP | Node ConPTY/forkpty binding if shell is Electron/Node (used by VS Code) |
| SRC-0238 | portable-pty | https://github.com/wezterm/wezterm/tree/main/pty | LIVE | no | MIT | `e68a8ec27727` | 2026-10-26 | G04 | MINE_DEEP | Rust cross-platform PTY incl. ConPTY; pin-ledger PATH_MINED_PASS1 |
| SRC-0239 | tmux | https://github.com/tmux/tmux | LIVE | no | ISC | `df302c561af5` | 2026-10-27 | G04 | KEEP_REFERENCE | Live, ISC; secondary to MINE_DEEP picks |
| SRC-0240 | WezTerm | https://github.com/wezterm/wezterm | LIVE | no | MIT | `e68a8ec27727` | 2026-10-26 | G04 | REJECT | Duplicate row of SRC-0238 (same repo) - merge |
| SRC-0241 | Windows ConPTY | https://learn.microsoft.com/windows/console/creating-a-pseudoconsole-session | NON_GITHUB | - | - | - | - | G04 | KEEP_REFERENCE | Windows platform API docs (ConPTY) |
| SRC-0242 | Windows Job Objects | https://learn.microsoft.com/windows/win32/procthread/job-objects | NON_GITHUB | - | - | - | - | G04 | KEEP_REFERENCE | Windows platform API docs (Job Objects) |
| SRC-0243 | xterm.js | https://github.com/xtermjs/xterm.js | LIVE | no | MIT | `d8a8247dbc11` | 2026-10-27 | G04 | MINE_DEEP | De-facto web terminal renderer; addons (fit, webgl, search, serialize) |
| SRC-0244 | Atuin | https://github.com/atuinsh/atuin | LIVE | no | MIT | `5e82ba214c1f` | 2026-10-27 | G04 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0245 | Eugeny Tabby | https://github.com/Eugeny/tabby | LIVE | no | MIT | `467ce8ebfa46` | 2026-10-27 | G15 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0246 | Zellij | https://github.com/zellij-org/zellij | LIVE | no | MIT | `237fe15970e7` | 2026-10-27 | G15 | MINE_DEEP | Session attach/detach, plugin system, web client for remote access; MIT |
| SRC-0247 | cargo-nextest | https://github.com/nextest-rs/nextest | LIVE | no | Apache-2.0 | `2dc813284e32` | 2026-10-27 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0248 | cargo-llvm-cov | https://github.com/taiki-e/cargo-llvm-cov | LIVE | no | Apache-2.0 | `b405aca51cc8` | 2026-10-15 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0249 | BrowserGym | https://github.com/ServiceNow/BrowserGym | LIVE | no | Apache-2.0 | `4ccc72332ab9` | 2026-10-21 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0250 | cargo-fuzz | https://github.com/rust-fuzz/cargo-fuzz | LIVE | no | Apache-2.0 | `bf2fc668dafd` | 2026-07-20 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0251 | cargo-mutants | https://github.com/sourcefrog/cargo-mutants | LIVE | no | MIT | `6c720ae82a17` | 2026-10-19 | G13 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0252 | Inspect AI | https://github.com/UKGovernmentBEIS/inspect_ai | LIVE | no | MIT | `1692fd8d7364` | 2026-10-27 | G13 | MINE_DEEP | Eval framework with sandboxed tool tasks; MIT |
| SRC-0253 | Kani | https://github.com/model-checking/kani | LIVE | no | Apache-2.0 | `744b3e84d6eb` | 2026-10-26 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0254 | OSWorld | https://github.com/xlang-ai/OSWorld | LIVE | no | Apache-2.0 | `044bc33901cb` | 2026-10-26 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0255 | Playwright Test | https://github.com/microsoft/playwright | LIVE | no | Apache-2.0 | `a169686c61af` | 2026-10-27 | G06 | MINE_DEEP | Browser automation + test runner; CDP/BiDi; trace viewer |
| SRC-0256 | Promptfoo | https://github.com/promptfoo/promptfoo | LIVE | no | MIT | `e48ed85e08ff` | 2026-10-26 | G13 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0257 | proptest | https://github.com/proptest-rs/proptest | LIVE | no | Apache-2.0 | `70cf37d46b7d` | 2026-10-10 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0258 | Schemathesis | https://github.com/schemathesis/schemathesis | LIVE | no | MIT | `40d1929dfb45` | 2026-10-27 | G13 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0259 | Stryker | https://github.com/stryker-mutator | ORG_LEVEL | - | - | - | - | G13 | DEFER | Org-level URL (JS/.NET mutation); cargo-mutants covers Rust |
| SRC-0260 | SWE-bench | https://github.com/SWE-bench/SWE-bench | LIVE | no | MIT | `02e7a74ffd0b` | 2026-09-18 | G13 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0261 | Terminal-Bench | https://github.com/harbor-framework/terminal-bench | LIVE | no | Apache-2.0 | `6964e9252c90` | 2026-10-27 | G13 | MINE_DEEP | Terminal-agent benchmark harness; Apache-2.0 |
| SRC-0262 | WebArena | https://github.com/web-arena-x/webarena | LIVE | no | Apache-2.0 | `dce04686a562` | 2025-11-26 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0263 | Qodo Cover | https://github.com/qodo-ai/qodo-cover | LIVE | no | AGPL-3.0 | `adcf55baba40` | 2026-04-05 | G13 | REJECT | AGPL-3.0; test-gen behavior only |
| SRC-0264 | JetBrains RD | https://github.com/JetBrains/rd | LIVE | no | Apache-2.0 | `6ae828fce6ce` | 2026-10-21 | G10 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0265 | Flutter | https://github.com/flutter/flutter | LIVE | no | BSD-3-Clause | `7ebd8154adff` | 2026-10-27 | G01 | KEEP_REFERENCE | Live, BSD-3-Clause; secondary to MINE_DEEP picks |
| SRC-0266 | Wispr Flow | https://wisprflow.ai | NON_GITHUB | - | - | - | - | G15 | KEEP_REFERENCE | vendor product page (closed); behavior/spec oracle only |
| SRC-0267 | ElevenLabs UI | https://github.com/elevenlabs/ui | LIVE | no | MIT | `3a28ebab197f` | 2026-10-16 | G15 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0268 | Tavily | https://www.tavily.com | NON_GITHUB | - | - | - | - | X5 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0269 | Tavily Skills / MCP | https://github.com/tavily-ai | ORG_LEVEL | - | - | - | - | X5 | DEFER | Org-level URL; web-research connector later |
| SRC-0270 | Huly | https://github.com/hcengineering/platform | LIVE | no | EPL-2.0 | `f292d165efa8` | 2026-10-26 | X5 | DEFER | EPL-2.0; work-platform out of v3 core |
| SRC-0271 | Microsoft Loop / Teams / Planner | https://microsoft.com | NON_GITHUB | - | - | - | - | X5 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0272 | Coda | https://coda.io | NON_GITHUB | - | - | - | - | X5 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0273 | Fibery | https://fibery.io | NON_GITHUB | - | - | - | - | X5 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0274 | Asana Work Graph / AI Teammates | https://asana.com | NON_GITHUB | - | - | - | - | X5 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0275 | Atlassian Teamwork Graph | https://www.atlassian.com | NON_GITHUB | - | - | - | - | X5 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0276 | Linear | https://linear.app | NON_GITHUB | - | - | - | - | X5 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0277 | Plane | https://github.com/makeplane/plane | LIVE | no | AGPL-3.0 | `a9e70360c5bc` | 2026-10-27 | X5 | REJECT | AGPL-3.0 |
| SRC-0278 | ChatGPT Work / Projects / Apps / Scheduled Work | https://openai.com | NON_GITHUB | - | - | - | - | X5 | DEFER | vendor product page (closed); outside v3 capability list |
| SRC-0279 | SPIFFE / SPIRE | https://github.com/spiffe/spire | LIVE | no | Apache-2.0 | `a33d43d3c1cd` | 2026-10-26 | G12 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0280 | Backstage | https://github.com/backstage/backstage | LIVE | no | Apache-2.0 | `2f9abb647aca` | 2026-10-27 | X5 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0281 | Augment Code | https://www.augmentcode.com | NON_GITHUB | - | - | - | - | G09 | KEEP_REFERENCE | Closed product; context-engine behavior oracle |
| SRC-0282 | augmentcode/context-connectors | https://github.com/augmentcode/context-connectors | LIVE | no | MIT | `f7d6472ae626` | 2026-02-11 | G09 | DEFER | 18 stars; registry REJECT_OR_NEGATIVE_ORACLE; last push 2026-02 |
| SRC-0283 | Graphite | https://graphite.com | NON_GITHUB | - | - | - | - | G08 | KEEP_REFERENCE | Closed product; stacked-PR behavior oracle |
| SRC-0284 | github/gh-stack | https://github.com/github/gh-stack | LIVE | no | MIT | `2a49e6751238` | 2026-10-26 | G08 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0285 | git-town/git-town | https://github.com/git-town/git-town | LIVE | no | MIT | `d0cc7951b01e` | 2026-10-23 | G08 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0286 | ejoffe/spr | https://github.com/ejoffe/spr | LIVE | no | MIT | `0767a458e50f` | 2026-04-22 | G08 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0287 | ezyang/ghstack | https://github.com/ezyang/ghstack | LIVE | no | MIT | `68d401f6f6e7` | 2026-09-24 | G08 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0288 | Composio Agent Orchestrator | https://github.com/ComposioHQ/agent-orchestrator | RENAMED -> OrchestratorInc/agent-orchestrator | no | Apache-2.0 | `70606c814f6f` | 2026-10-27 | G02 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks (renamed -> OrchestratorInc/agent-orchestrator) |
| SRC-0289 | 21st-dev/1code | https://github.com/21st-dev/1code | LIVE | YES | Apache-2.0 | `9f1bc76fa437` | 2026-03-06 | G02 | DEFER | Archived; benchmark/behavior quarry only |
| SRC-0290 | kdlbs/kandev | https://github.com/kdlbs/kandev | LIVE | no | AGPL-3.0 | `61a96d8c9a99` | 2026-10-27 | G02 | REJECT | AGPL-3.0 |
| SRC-0291 | fynnfluegge/agtx | https://github.com/fynnfluegge/agtx | LIVE | no | Apache-2.0 | `8ae68682f10b` | 2026-10-23 | G02 | DEFER | Live, Apache-2.0; overlapping orchestration framework - revisit at Edara gate |
| SRC-0292 | morapelker/hive | https://github.com/morapelker/hive | LIVE | no | MIT | `782d3ae2e664` | 2026-09-29 | G02 | DEFER | Live, MIT; overlapping orchestration framework - revisit at Edara gate |
| SRC-0293 | elara-labs/code-context-engine | https://github.com/elara-labs/code-context-engine | LIVE | no | MIT | `75071156e08a` | 2026-08-23 | G09 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0294 | Helweg/opencode-codebase-index | https://github.com/Helweg/opencode-codebase-index | RENAMED -> Helweg/open-codebase-index | no | MIT | `fd9ed753d14c` | 2026-10-27 | G09 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks (renamed -> Helweg/open-codebase-index) |
| SRC-0295 | flupkede/codesearch | https://github.com/flupkede/codesearch | LIVE | no | Apache-2.0 | `765e3daad6f4` | 2026-10-27 | G09 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0296 | intuit/infigraph | https://github.com/intuit/infigraph | LIVE | no | Apache-2.0 | `cf82f5d7440d` | 2026-10-02 | G09 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0297 | giancarloerra/SocratiCode | https://github.com/giancarloerra/SocratiCode | LIVE | no | AGPL-3.0 | `dae6d3a073f9` | 2026-10-23 | G09 | REJECT | AGPL-3.0; unverified claims |
| SRC-0298 | PatrickSys/codebase-context | https://github.com/PatrickSys/codebase-context | LIVE | no | Elastic-2.0 | `1928b267347a` | 2026-10-21 | G09 | REJECT | Elastic-2.0 source-available |
| SRC-0299 | Microsoft GraphRAG | https://github.com/microsoft/graphrag | LIVE | no | MIT | `c600ff80b77b` | 2026-10-27 | G09 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0300 | Graphiti | https://github.com/getzep/graphiti | LIVE | no | Apache-2.0 | `2b5db9e139b2` | 2026-10-26 | G09 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0301 | Mem0 | https://github.com/mem0ai/mem0 | LIVE | no | Apache-2.0 | `26cdefb46600` | 2026-10-26 | G09 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0302 | Context7 | https://github.com/upstash/context7 | LIVE | no | MIT | `5c368c93ef92` | 2026-10-27 | G09 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0303 | OpenGrok | https://github.com/oracle/opengrok | LIVE | no | CDDL-1.0 | `03b382868424` | 2026-10-26 | G09 | DEFER | CDDL-1.0; Zoekt/Tantivy preferred |
| SRC-0304 | OpenFGA | https://github.com/openfga/openfga | LIVE | no | Apache-2.0 | `57b39bc3dcc1` | 2026-10-27 | G12 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0305 | SpiceDB | https://github.com/authzed/spicedb | LIVE | no | Apache-2.0 | `7e7420c3f541` | 2026-10-27 | G12 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0306 | OPAL | https://github.com/permitio/opal | LIVE | no | Apache-2.0 | `7e63ab4694c2` | 2026-10-27 | G12 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0307 | Microsoft MCP Gateway | https://github.com/microsoft/mcp-gateway | LIVE | no | MIT | `f57c4f049dcc` | 2026-10-21 | G10 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0308 | Microsoft LiteBox | https://github.com/microsoft/litebox | LIVE | no | MIT | `7fa997bf1ebc` | 2026-10-27 | G11 | MINE_DEEP | Windows-capable library-OS isolation research; MIT; pin-ledger PATH_MINED_PASS1 |
| SRC-0309 | microsoft/hcsshim | https://github.com/microsoft/hcsshim | LIVE | no | MIT | `838c2196b8c5` | 2026-10-22 | G11 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0310 | Alibaba OpenSandbox | https://github.com/alibaba/OpenSandbox | RENAMED -> opensandbox-group/OpenSandbox | no | Apache-2.0 | `62a64f0b48cd` | 2026-10-27 | G11 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks (renamed -> opensandbox-group/OpenSandbox) |
| SRC-0311 | ServiceNow WorkArena | https://github.com/ServiceNow/WorkArena | LIVE | no | Apache-2.0 | `e885130962f6` | 2026-09-28 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0312 | ServiceNow AgentLab | https://github.com/ServiceNow/AgentLab | LIVE | no | Apache-2.0 | `8488c564eea0` | 2026-10-06 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0313 | Windows Agent Arena | https://github.com/microsoft/WindowsAgentArena | LIVE | no | MIT | `eb220c4dcf64` | 2026-10-26 | G13 | KEEP_REFERENCE | Live, MIT; secondary to MINE_DEEP picks |
| SRC-0314 | AutoElicit | https://github.com/microsoft/AutoElicit | 404 | - | - | - | - | G13 | REJECT | Repo 404 - corpus not public at URL; re-locate |
| SRC-0315 | RedTeamCUA | https://github.com/microsoft/RedTeamCUA | 404 | - | - | - | - | G13 | REJECT | Repo 404 - corpus not public at URL; re-locate |
| SRC-0316 | Parca | https://github.com/parca-dev/parca | LIVE | no | Apache-2.0 | `a64451cf6d17` | 2026-10-27 | X4 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0317 | Pyroscope | https://github.com/grafana/pyroscope | LIVE | no | AGPL-3.0 | `970ede2630f7` | 2026-10-27 | X4 | REJECT | AGPL-3.0 |
| SRC-0318 | OpenTelemetry eBPF Profiler | https://github.com/open-telemetry/opentelemetry-ebpf-profiler | LIVE | no | Apache-2.0 | `c159050f8964` | 2026-10-27 | X4 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0319 | Microsoft ETW | https://github.com/microsoft/Windows-classic-samples | LIVE | no | MIT | `434f6002bdf9` | 2026-09-03 | X4 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0320 | Samply | https://github.com/mstange/samply | LIVE | no | Apache-2.0 | `99fe90353bae` | 2026-10-24 | X4 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0321 | flamegraph-rs | https://github.com/flamegraph-rs/flamegraph | LIVE | no | Apache-2.0 | `6f88e785ce3d` | 2026-10-05 | X4 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0322 | TensorZero | https://github.com/tensorzero/tensorzero | LIVE | YES | Apache-2.0 | `62eb8f63e8ec` | 2026-06-11 | X2 | DEFER | Archived 2026-06; frozen gateway quarry |
| SRC-0323 | LiteLLM | https://github.com/BerriAI/litellm | LIVE | no | MIT + proprietary enterprise/ | `cfe0100e1fca` | 2026-10-27 | X2 | KEEP_REFERENCE | MIT core + proprietary enterprise/; provider-coverage reference |
| SRC-0324 | Bifrost | https://github.com/maximhq/bifrost | LIVE | no | Apache-2.0 | `d4a247904ac8` | 2026-10-27 | X2 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0325 | Portkey Gateway | https://github.com/Portkey-AI/gateway | LIVE | no | MIT | `669825cbe89e` | 2026-05-25 | X2 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0326 | SGLang | https://github.com/sgl-project/sglang | LIVE | no | Apache-2.0 | `de26bb16a972` | 2026-10-27 | X2 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0327 | Candle | https://github.com/huggingface/candle | LIVE | no | Apache-2.0 | `12bb5d1f6350` | 2026-10-14 | X2 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0328 | TLA+ | https://github.com/tlaplus/tlaplus | LIVE | no | MIT | `fad899c74ca8` | 2026-10-26 | G13 | DEFER | Live, MIT; formal-methods assurance later |
| SRC-0329 | Apalache | https://github.com/apalache-mc/apalache | LIVE | no | Apache-2.0 | `9a13950e0ebd` | 2026-10-12 | G13 | DEFER | Live, Apache-2.0; formal-methods assurance later |
| SRC-0330 | P language | https://github.com/p-org/P | LIVE | no | MIT | `260da928f675` | 2026-09-03 | G13 | DEFER | Live, MIT; formal-methods assurance later |
| SRC-0331 | FoundationDB | https://github.com/apple/foundationdb | LIVE | no | Apache-2.0 | `414a6ec83442` | 2026-10-27 | X6 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0332 | Verus | https://github.com/verus-lang/verus | LIVE | no | MIT | `39e84676a32a` | 2026-10-27 | G13 | DEFER | Live, MIT; formal-methods assurance later |
| SRC-0333 | Prusti | https://github.com/viperproject/prusti-dev | RENAMED -> prusti/prusti | no | MPL-2.0 (+ per-crate) | `38594c8f3af1` | 2026-10-27 | G13 | DEFER | MPL-2.0; formal methods later |
| SRC-0334 | LiveStore | https://github.com/livestorejs/livestore | LIVE | no | Apache-2.0 | `aafda2024137` | 2026-10-26 | G14 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0335 | PGlite | https://github.com/electric-sql/pglite | LIVE | no | Apache-2.0 | `02b1a415a42a` | 2026-10-27 | G14 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0336 | ElectricSQL | https://github.com/electric-sql/electric | LIVE | no | Apache-2.0 | `3f9809fb0bd8` | 2026-10-06 | G14 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0337 | PyRIT | https://github.com/Azure/PyRIT | LIVE | YES | MIT | `bec7cb5d6089` | 2026-03-25 | G13 | DEFER | Archived; red-team orchestration quarry |
| SRC-0338 | LLM Guard | https://github.com/protectai/llm-guard | LIVE | YES | MIT | `168c1034ffdb` | 2026-07-08 | G13 | DEFER | Archived; scanner corpus reference |
| SRC-0339 | NeMo Guardrails | https://github.com/NVIDIA-NeMo/Guardrails | LIVE | no | Apache-2.0 | `b6d160969f15` | 2026-10-27 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0340 | Arize Phoenix | https://github.com/Arize-ai/phoenix | LIVE | no | Elastic-2.0 | `1a275005b53e` | 2026-10-27 | X4 | REJECT | Elastic-2.0 source-available |
| SRC-0341 | PaperQA2 | https://github.com/Future-House/paper-qa | LIVE | no | Apache-2.0 | `c692d0dfeac4` | 2026-10-26 | X5 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0342 | FutureHouse Robin | https://github.com/Future-House/Robin | LIVE | no | Apache-2.0 | `4a5cce310f3b` | 2026-04-21 | X5 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0343 | Crawl4AI | https://github.com/unclecode/crawl4ai | LIVE | no | Apache-2.0 | `888299fb5f0b` | 2026-10-26 | X5 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0344 | Firecrawl | https://github.com/mendableai/firecrawl | RENAMED -> firecrawl/firecrawl | no | AGPL-3.0 | `2b68c4c56efc` | 2026-10-27 | X5 | REJECT | AGPL-3.0 (repo moved to firecrawl org) |
| SRC-0345 | SearXNG | https://github.com/searxng/searxng | LIVE | no | AGPL-3.0 | `ef7bae9ddbec` | 2026-10-27 | X5 | REJECT | AGPL-3.0 |
| SRC-0346 | GROBID | https://github.com/kermitt2/grobid | RENAMED -> grobidOrg/grobid | no | Apache-2.0 | `c568f9087f05` | 2026-10-27 | X5 | DEFER | Live, Apache-2.0; outside v3 capability list (renamed -> grobidOrg/grobid) |
| SRC-0347 | docling.rs | https://github.com/docling-project/docling.rs | LIVE | no | MIT | `b9357538ea2a` | 2026-10-27 | X5 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0348 | Typst | https://github.com/typst/typst | LIVE | no | Apache-2.0 | `05437aeac994` | 2026-10-27 | X5 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0349 | Comby | https://github.com/comby-tools/comby | LIVE | no | Apache-2.0 | `3b6bdff7bc3b` | 2026-06-08 | G09 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0350 | Codemod | https://github.com/codemod/codemod | LIVE | no | Apache-2.0 | `0affdcf205aa` | 2026-10-22 | G09 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0351 | Soufflé | https://github.com/souffle-lang/souffle | LIVE | no | UPL-1.0 | `f53dab8bf4bb` | 2026-10-02 | G09 | KEEP_REFERENCE | Live, UPL-1.0; secondary to MINE_DEEP picks |
| SRC-0352 | DDisasm | https://github.com/GrammaTech/ddisasm | LIVE | no | AGPL-3.0 | `1d17f292e367` | 2026-10-26 | X6 | REJECT | AGPL-3.0 |
| SRC-0353 | Ghidra | https://github.com/NationalSecurityAgency/ghidra | LIVE | no | Apache-2.0 | `1b9e58a915cf` | 2026-10-27 | X6 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0354 | angr | https://github.com/angr/angr | LIVE | no | BSD-2-Clause | `aaf96e6c28b1` | 2026-10-27 | X6 | DEFER | Live, BSD-2-Clause; outside v3 capability list |
| SRC-0355 | LIEF | https://github.com/lief-project/LIEF | LIVE | no | Apache-2.0 | `86a95f1d8cce` | 2026-10-26 | X6 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0356 | statig | https://github.com/mdeloof/statig | LIVE | no | MIT | `3780eecdbcf4` | 2025-11-29 | G03 | KEEP_REFERENCE | MIT Rust HSM; small, maintained |
| SRC-0357 | dist / cargo-dist | https://github.com/axodotdev/cargo-dist | LIVE | no | Apache-2.0 | `86d735eb02c0` | 2026-10-24 | G01 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0358 | Apache DataFusion | https://github.com/apache/datafusion | LIVE | no | Apache-2.0 | `6286f5e6053a` | 2026-10-27 | X4 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0359 | Apache Arrow Rust | https://github.com/apache/arrow-rs | LIVE | no | Apache-2.0 | `dc5949512288` | 2026-10-27 | X4 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0360 | CozoDB | https://github.com/cozodb/cozo | LIVE | no | MPL-2.0 | `481af058abac` | 2024-12-04 (stale) | G09 | DEFER | MPL-2.0 and no push since 2024-12 (stale) |
| SRC-0361 | Coze Studio | https://github.com/coze-dev/coze-studio | LIVE | no | Apache-2.0 | `fefb05ff27be` | 2026-07-29 | G02 | DEFER | Live, Apache-2.0; overlapping orchestration framework - revisit at Edara gate |
| SRC-0362 | Eino | https://github.com/cloudwego/eino | LIVE | no | Apache-2.0 | `0a5ca53b9d3b` | 2026-10-27 | G02 | DEFER | Live, Apache-2.0; overlapping orchestration framework - revisit at Edara gate |
| SRC-0363 | FlowGram | https://github.com/bytedance/flowgram.ai | LIVE | no | MIT | `02a01680b53f` | 2026-10-23 | G07 | DEFER | Live, MIT; overlapping orchestration framework - revisit at Edara gate |
| SRC-0364 | DeerFlow | https://github.com/bytedance/deer-flow | LIVE | no | MIT | `fb553747d1d6` | 2026-10-27 | G02 | DEFER | Live, MIT; overlapping orchestration framework - revisit at Edara gate |
| SRC-0365 | smolagents | https://github.com/huggingface/smolagents | LIVE | no | Apache-2.0 | `96f33faaf028` | 2026-10-22 | G02 | DEFER | Live, Apache-2.0; overlapping orchestration framework - revisit at Edara gate |
| SRC-0366 | Pa11y | https://github.com/pa11y/pa11y | LIVE | no | LGPL-3.0 | `aede96f5c68c` | 2026-10-26 | G13 | DEFER | LGPL-3.0; axe-core/Lighthouse cover need |
| SRC-0367 | Lighthouse | https://github.com/GoogleChrome/lighthouse | LIVE | no | Apache-2.0 | `1a4ffa418258` | 2026-10-25 | G13 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0368 | Web Platform Tests | https://github.com/web-platform-tests/wpt | LIVE | no | BSD-3-Clause | `4d0cdba6d462` | 2026-10-27 | G13 | KEEP_REFERENCE | Live, BSD-3-Clause; secondary to MINE_DEEP picks |
| SRC-0369 | FoundationAgents/AFlow | https://github.com/FoundationAgents/AFlow | LIVE | no | MIT | `3f457218fc71` | 2025-12-25 | X7 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0370 | metauto-ai/GPTSwarm | https://github.com/metauto-ai/GPTSwarm | LIVE | no | MIT | `c23a827f561c` | 2026-02-05 | X7 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0371 | SALT-NLP/DyLAN | https://github.com/SALT-NLP/DyLAN | LIVE | no | MIT | `006e440a519f` | 2024-05-16 (stale) | X7 | DEFER | Stale (last push 2024-05-16) |
| SRC-0372 | bingreeky/MaAS | https://github.com/bingreeky/MaAS | LIVE | no | NONE | `987f3c1bc9a9` | 2025-11-13 | X7 | REJECT | No license file (all rights reserved); paper reference only |
| SRC-0373 | wangzx1219/AgentDropout | https://github.com/wangzx1219/AgentDropout | LIVE | no | NONE | `855befab08df` | 2026-06-12 | X7 | REJECT | No license file (all rights reserved); paper reference only |
| SRC-0374 | yanweiyue/AgentPrune | https://github.com/yanweiyue/AgentPrune | LIVE | no | NONE | `c544dd6a1858` | 2025-03-23 (stale) | X7 | REJECT | No license file; stale; paper reference only |
| SRC-0375 | ulab-uiuc/GraphPlanner | https://github.com/ulab-uiuc/GraphPlanner | LIVE | no | NONE | `56010b1f43c6` | 2026-04-26 | X7 | REJECT | No license file; 22 stars; paper reference only |
| SRC-0376 | lm-sys/RouteLLM | https://github.com/lm-sys/RouteLLM | LIVE | no | Apache-2.0 | `0b64fdafe049` | 2024-08-10 (stale) | X7 | DEFER | Stale (last push 2024-08-10) |
| SRC-0377 | ulab-uiuc/LLMRouter | https://github.com/ulab-uiuc/LLMRouter | LIVE | no | MIT | `c65ee0122bc9` | 2026-10-19 | X7 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0378 | AgentOptimizer/agentopt | https://github.com/AgentOptimizer/agentopt | LIVE | no | Apache-2.0 | `2bcafeaaf439` | 2026-10-25 | X7 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0379 | fidelity/mabwiser | https://github.com/fidelity/mabwiser | LIVE | no | Apache-2.0 | `b104071351d5` | 2024-09-05 (stale) | X7 | DEFER | Stale (last push 2024-09-05) |
| SRC-0380 | VowpalWabbit/vowpal_wabbit | https://github.com/VowpalWabbit/vowpal_wabbit | LIVE | no | BSD-3-Clause | `00196b35f63b` | 2026-10-15 | X7 | DEFER | Live, BSD-3-Clause; outside v3 capability list |
| SRC-0381 | google/or-tools | https://github.com/google/or-tools | LIVE | no | Apache-2.0 | `100f66e6242a` | 2026-10-27 | X7 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0382 | rust-or/good_lp | https://github.com/rust-or/good_lp | LIVE | no | MIT | `83d030b103d5` | 2026-09-03 | X7 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0383 | rust-or/highs | https://github.com/rust-or/highs | LIVE | no | MIT | `16956d200e68` | 2026-09-19 | X7 | DEFER | Live, MIT; outside v3 capability list |
| SRC-0384 | awslabs/cli-agent-orchestrator | https://github.com/awslabs/cli-agent-orchestrator | LIVE | no | Apache-2.0 | `a7a1db9c81ea` | 2026-10-27 | G02 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0385 | open-multi-agent/open-multi-agent | https://github.com/open-multi-agent/open-multi-agent | LIVE | no | MIT | `009bdbe079a9` | 2026-10-26 | G02 | DEFER | Live, MIT; overlapping orchestration framework - revisit at Edara gate |
| SRC-0386 | agentscope-ai/AgentTeams | https://github.com/agentscope-ai/AgentTeams | LIVE | no | Apache-2.0 | `d8332e0a9da4` | 2026-10-26 | G02 | DEFER | Live, Apache-2.0; overlapping orchestration framework - revisit at Edara gate |
| SRC-0387 | RightNow-AI/openfang | https://github.com/RightNow-AI/openfang | LIVE | no | Apache-2.0 | `acf2587e46be` | 2026-07-02 | G02 | DEFER | Live, Apache-2.0; overlapping orchestration framework - revisit at Edara gate |
| SRC-0388 | rivet-dev/rivet | https://github.com/rivet-dev/rivet | LIVE | no | Apache-2.0 | `80ee8b8c22b8` | 2026-10-26 | G03 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0389 | dagucloud/dagu | https://github.com/dagucloud/dagu | LIVE | no | GPL-3.0 | `9d5e5f3b31a6` | 2026-10-27 | G03 | REJECT | GPL-3.0; covered by permissive durable engines |
| SRC-0390 | orch8-io/engine | https://github.com/orch8-io/engine | LIVE | no | BUSL-1.1 | `21cb1454cb86` | 2026-10-27 | G03 | REJECT | BUSL-1.1, 75 stars; covered by DBOS/Temporal |
| SRC-0391 | Kocoro-lab/Shannon | https://github.com/Kocoro-lab/Shannon | LIVE | no | MIT | `391b61913028` | 2026-09-05 | G02 | DEFER | Live, MIT; overlapping orchestration framework - revisit at Edara gate |
| SRC-0392 | agentgateway/agentgateway | https://github.com/agentgateway/agentgateway | LIVE | no | Apache-2.0 | `a550bd2365b5` | 2026-10-27 | G10 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0393 | wslong20/G-safeguard | https://github.com/wslong20/G-safeguard | LIVE | no | NONE | `890c99f1cbc8` | 2025-06-28 (stale) | X7 | REJECT | No license file; stale; paper reference only |
| SRC-0394 | MR9812/BlindGuard | https://github.com/MR9812/BlindGuard | LIVE | no | Apache-2.0 | `ecbd8e9b02c9` | 2026-08-24 | X7 | DEFER | Live, Apache-2.0; outside v3 capability list |
| SRC-0395 | mvar-security/mvar | https://github.com/mvar-security/mvar | LIVE | no | Apache-2.0 | `379d9fe80034` | 2026-07-09 | G12 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0396 | oktsec/oktsec | https://github.com/oktsec/oktsec | LIVE | no | Apache-2.0 | `50e2666a60e4` | 2026-09-18 | G12 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0397 | opencrust-org/opencrust | https://github.com/opencrust-org/opencrust | LIVE | no | MIT | `f564e0c05014` | 2026-10-19 | G02 | DEFER | Live, MIT; overlapping orchestration framework - revisit at Edara gate |
| SRC-0398 | Devin | https://devin.ai | NON_GITHUB | - | - | - | - | G02 | KEEP_REFERENCE | Closed product; managed-agent lifecycle oracle |
| SRC-0399 | Fern | https://github.com/fern-api/fern | LIVE | no | Apache-2.0 | `d8503915fd6d` | 2026-10-27 | G10 | KEEP_REFERENCE | Live, Apache-2.0; secondary to MINE_DEEP picks |
| SRC-0400 | DeepSeek Harness | https://github.com/deepseek-ai/deepseek-harness | LIVE | no | MIT | `22ddee379240` | 2026-10-23 | G02 | KEEP_REFERENCE | MIT; registry marks negative oracle + path mining; harness event model |
| SRC-0401 | Cordis | https://github.com/cordiverse/cordis | LIVE | no | MIT | `c81e299808de` | 2026-10-27 | G02 | KEEP_REFERENCE | MIT; DeepSeek Harness lineage (plugin/reversible effects) |
| SRC-0402 | CommandCode | https://commandcode.ai | NON_GITHUB | - | - | - | - | G02 | KEEP_REFERENCE | Closed product; Taste/skills behavior oracle |

## 6. Limits of this verification

- Inventory/rights/access only; no code, path-level licence, NOTICE, dependency or security audit was performed.
- Licence labels for 47 repos come from the first ~500 characters of the root licence file; sub-directory licences
  (e.g. `ee/`, `enterprise/`, GPL crates in Zed) were noted only where the root file says so.
- Non-GitHub URLs were classified, and 22 spot-checked; the other ~39 were not fetched.
- HEAD SHAs move daily; they are observation anchors for 2026-10-27, not acquisition pins. Re-pin at the acquisition gate.
- Dispositions are proposals for the v3 replan and require owner ratification; d1 or any automated classifier was not used to
  decide them.
