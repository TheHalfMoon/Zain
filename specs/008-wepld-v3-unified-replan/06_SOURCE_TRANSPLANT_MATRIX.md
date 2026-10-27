# 06 — Source Transplant Matrix

```text
STATUS = PROPOSED acquisition decisions. Nothing is admitted, copied or installed by this document.
RIGHTS_CLASSES = PUBLIC-OSS (license verified at root file) | FOUNDER-ATTESTED (private authorization, not independently
                 verified, not disclosed) | PUBLIC-SDK (vendor terms) | PUBLIC-BEHAVIOR (docs only) | PROPRIETARY-UNAVAILABLE
PIN_DATE = 2026-10-27 (HEAD of default branch unless stated); pins become admission pins only at the phase entry gate
REGISTRY_BASE = frozen 402-entry V1 (archive 35dee10e…) — not rewritten; additions below are V3 candidates (R06 §4)
```

## 1. Foundation and module donors

| # | Capability → target | Source @ pin | License / rights | Paths | Decision | Why (rewrite avoided) | Exit / update strategy | Key risks | Replacement / acceptance tests | ESTIMATE pw | Conf. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | Shell, server, orchestration, providers, worktrees, diff, terminal, browser, packaging | pingdotgg/t3code @36d4d711 | MIT, PUBLIC-OSS + FOUNDER-ATTESTED | `apps/{desktop,web,server}`, `packages/{contracts,client-runtime,provider-*,source-control-*,shared}` | **FORK FOUNDATION** | ~1M LOC of working, tested product | Hard fork; cherry-pick security fixes monthly; no rebase | Effect 4 learning curve; Windows/storage debt; churn | T3's own 1,693 test files must pass on fork (baseline ratio recorded in P1) + WePLD seam tests | 18–34 (MVP) | M |
| D2 | Design Mode element capture | stablyai/orca @e310a636 `src/main/browser/grab-*.ts`, `browser-grab-payload.ts`, `src/shared/browser-grab-types` | MIT | as listed | **PORT (ADAPT)** | ~1.1k LOC hard-won UX | Owned copy; no sync | Electron capture glue differs from T3 | AT-01..05 (03B) | 3–6 | M |
| D3 | CLI agent catalog + hook/OSC 7501 status | Orca `src/shared/tui-agent-config*.ts`, `src/shared/{agent-hook-listener,program-status}` | MIT | as listed | **PORT** | 45 CLI agents' launch/ready rules | Catalog curated in WePLD | CLI drift. **Never write hooks into the user's global `~/.claude`/`~/.codex`**: use per-launch overlays (`CLAUDE_CONFIG_DIR`, `CODEX_HOME`) and an authenticated loopback hook endpoint (per-PTY secret) so other local processes cannot spoof status. CLI agents are `UNMEDIATED` workers (07 §6) | PTY agent launches; status detection fixture tests | 3–5 | M |
| D4 | Windows-safe process host | Orca `src/packages/process-host/src` | MIT | package | **COPY AS-IS** (rename) | Windows tree-kill/quoting | Owned | low | process kill/tree tests on Windows | 1–2 | H |
| D5 | Linear integration | Orca `src/main/linear` | MIT | dir | **PORT** | 6.8k LOC low coupling | Owned | API drift | contract tests with recorded fixtures | 2–4 | M |
| D6 | Computer use sidecar | Orca `src/main/computer`, `native/computer-use-*` | MIT | dirs | **PORT (Phase 9)** | cross-OS native helpers | Owned | high-risk effect class | Core-gated input injection tests | 3–6 | L |
| D7 | Editor + diff comments | `microsoft/monaco-editor` @dbf1945df2ff (MIT) + Orca `components/{editor,diff-comments}` | MIT | — | **INTEGRATE Monaco + PORT diff comments** | editor engine solved | npm pin | bundle weight | editor a11y + large-file tests | 4–8 | M |
| D8 | Durability patterns | vercel/workflow @af8c6d32, vercel-labs/durable-harness @ea8aa406 | Apache-2.0 | `packages/world/src/interfaces.ts`, durable-harness `driver.ts` | **PATTERN ONLY** | — | n/a | — | R1–R11 (09) | 0 (design) | H |
| D9 | Process sandbox (Win/Linux), exec policy, network proxy | openai/codex @603a7baf `codex-rs/{sandboxing,linux-sandbox,bwrap,windows-sandbox-rs,windows-sandbox-service,mxc-sandbox,process-hardening,execpolicy,network-proxy}` (full set per R10 §3; service/bwrap crates may be required for the Windows/Linux sandboxes to function) | Apache-2.0 (NOTICE handling required) | crates | **ADAPT (Job Object floor in P3; full sandbox Phase 8)** into Core | production OS sandboxes in Rust | vendored crates, re-pinned per phase | crate coupling to codex-core; Windows service model | escape test suite; network egress tests | 4–10 | M |
| D10 | Sandbox wrapper (fs/network) | anthropics/sandbox-runtime @98a4016d | Apache-2.0 | repo | **REFERENCE / optional WRAP** | macOS/Linux coverage | npm pin | not native Windows | same escape suite | 1–2 | M |
| D11 | Policy engine | cedar-policy/cedar @2c2b84772a63 (Rust) + cedar-for-agents @41c07851 | Apache-2.0 | crates/schemas | **INTEGRATE (Phase 3)** | analyzable authorization | crate pin | policy authoring UX | policy unit tests; deny-overrides tests | 2–4 | M |
| D12 | ACP schema/SDKs | agentclientprotocol/agent-client-protocol @e50f62b4, rust-sdk @644377ad, typescript-sdk @bca8e491 | Apache-2.0 | schema, sdks | **INTEGRATE** | T3 already has provider-acp | pin | spec v2 draft | ACP conformance fixtures | 1–2 | H |
| D13 | MCP SDKs | modelcontextprotocol/typescript-sdk @b415e60b, rust-sdk @cd88056f | MIT→Apache-2.0 transition (verify per file) | — | **INTEGRATE** | standard | pin | license transition | MCP conformance | 1 | M |
| D14 | Claude worker | `@anthropic-ai/claude-agent-sdk` 0.3.311 (via T3 adapter) or `claude-agent-acp` 0.97.0 (**also depends on the same SDK**, so it does not avoid the question) | PUBLIC-SDK (Commercial Terms) / Apache-2.0 adapter | — | **INTEGRATE; excluded from installer until G4** (P2 task: remove from `server.asar`, load from user-consented location, CI gate fails if `claude-agent-sdk*` is in installer contents) | official route | user-env resolution | redistribution UNKNOWN; the SDK pulls platform binaries that ship Claude Code itself (R03C §0) | CC-T01..05 | 1–2 | M |
| D15 | Codex worker | `codex app-server` (T3 adapter) | Apache-2.0 | — | **INTEGRATE** | official route | pin | protocol churn | contract tests | 0 (inherited) | H |
| D16 | Thread store / rollout / memories (Rust) | openai/codex `codex-rs/{thread-store,rollout,history,memories,file-search}` | Apache-2.0 | crates | **REFERENCE** for Brain + local search | — | — | — | — | 0 | M |
| D17 | Ledger storage | rusqlite (bundled SQLite) | MIT | crate | **INTEGRATE (Phase 3)** | standard | crate pin | dependency admission | ledger crash tests | 1 | H |
| D18 | Local full-text search | SQLite FTS5 (in D17) — Tantivy deferred | public domain / MIT | — | **INTEGRATE** | no extra service | — | ranking quality | Brain recall tests | 0.5 | M |
| D19 | Canvas freeform layer | excalidraw/excalidraw @808d068e1826 | MIT | packages/excalidraw | **INTEGRATE (Phase 7)** | — | npm pin | bundle | AT tests | 1–2 | M |
| D20 | Element→source mapping | onlook-dev/onlook @423e2e924366 (`data-oid` approach; OSS line slowing — hosted successor in early access, R03B §9), click-to-component, react-dev-inspector | Apache-2.0 / MIT | — | **ADAPT (Phase 7)** | — | owned | framework coverage | AT source-mapping tests | 3–5 | L |
| D21 | Design tokens | W3C DTCG 2025.10 spec + style-dictionary/style-dictionary @f82e7aafbcae | W3C / Apache-2.0 | — | **COPY spec / INTEGRATE** | — | pin | DTCG support in progress | token round-trip tests | 1 | M |
| D22 | Review producer (local) | The-PR-Agent/pr-agent @ae053ea8979a | MIT | — | **WRAP as optional reviewer worker** | — | pin | model cost | review fixture tests | 1–2 | M |
| D23 | Eval harness | UKGovernmentBEIS/inspect_ai @1692fd8d7364; harbor-framework/terminal-bench @6964e9252c90 | MIT / Apache-2.0 | — | **INTEGRATE (Phase 6 benchmarks)** | — | pin | — | B-suite in 09 | 1–2 | M |
| D24 | Sync/CRDT (multi-device, later) | loro-dev/loro, yjs | MIT | — | **DEFER** | — | — | — | — | — | — |
| D25 | Existing WePLD Core | TheHalfMoon/wepld `crates/{contracts,core}` @0a843a2 | owned | as listed | **KEEP** | tested S1/S2 | owned | — | existing 19k-line test suite | 0 | H |

Rejected / reference-only (not exhaustive; full 402-row dispositions in `research/R06_REGISTRY_VERIFICATION.md`):

| Source | Decision | Reason |
|---|---|---|
| Orca as foundation | REJECT | `03D` §5 |
| T3 mobile app, T3 Connect relay, Clerk, PostHog | REJECT (strip) | cloud coupling/telemetry |
| tldraw | REJECT | license forbids production use without key |
| Webstudio, claude-squad | REJECT (AGPL) / reference only | copyleft |
| Zed editor crates | REFERENCE ONLY | GPL/AGPL per crate |
| Vercel Workflow as engine; durable-harness runtime | REJECT | second orchestrator; Vercel Sandbox dependency |
| DBOS/Temporal | REFERENCE | patterns only; T3 already has the executor |
| Tauri 2 (SRC-0170) | RETIRE as shell | `ADR-002` |
| Continue (SRC continue) | DEFER/REJECT as reviewer | README says repo is read-only/unmaintained (R06) |
| Amp code (`@ampcode/*`, official-plugins) | REJECT | commercial license / no license |
| Daytona, coder/agentapi | REJECT | archived |

## 2. Registry reconciliation (V3 candidate additions, not a rewrite of V1)

New candidate rows: `pingdotgg/t3code`, `stablyai/orca` (re-pin e310a636), `vercel/workflow`, `vercel-labs/durable-harness`,
`openai/codex` crates (Codex already present as a row; add crate-level paths), `OpenHands/software-agent-sdk`,
`agentclientprotocol/{rust-sdk,typescript-sdk,claude-agent-acp}`, `modelcontextprotocol/{typescript-sdk,rust-sdk}`,
`anthropics/sandbox-runtime`, `onlook-dev/onlook`, `style-dictionary/style-dictionary`, DTCG spec, `microsoft/playwright-mcp`.
Moved repos to re-point: Goose → aaif-goose, OpenHands → OpenHands org, opencode → anomalyco, PR-Agent → The-PR-Agent,
Pi → earendil-works. Registry hygiene: 5 duplicate rows, 4 dead (404), 6 archived, 22/30 ledger pins moved (R06).

## 3. Provenance and notice obligations

- Keep `LICENSE` texts of T3 (MIT, T3 Tools Inc.) and Orca (MIT, Lovecast Inc.) in `THIRD_PARTY_NOTICES/` and the
  generated `third-party-licenses.json` (T3 build already fails on missing notices — keep that gate).
- Apache-2.0 donors (codex crates, Cedar, ACP, sandbox-runtime, Style Dictionary, onlook ideas if code copied): retain
  NOTICE files where present, state changes in modified files.
- Record `FOUNDER-ATTESTED` next to T3/Orca rows: the founder affirms broader permissions privately; the package does
  not rely on them beyond MIT terms and does not disclose them.
- Shipped UI and product-owned symbols are WePLD-branded; credits live only in notices/about.

## 4. Rename and collision register (fork identity)

| Surface | Donor value | WePLD value | Collision risk if missed |
|---|---|---|---|
| App ID / AUMID | `T3Tools.T3Code`, `com.stablyai.orca` | `ai.wepld.desktop` | notifications/keychain attributed to donor |
| CLI | `t3`, `orca` | `wepld` (Server CLI); Core binary → `wepld-core` | PATH collision with existing S2 `wepld` binary (rename Core) |
| Protocol | `t3://`?, `orca://` | `wepld://` | deep-link hijack |
| Update feed | T3/Orca GitHub releases | WePLD GitHub releases | **silent cross-update to donor binaries** |
| Data dirs | `~/.t3`, `%APPDATA%\Orca`, `~/.orca` | `%APPDATA%\WePLD`, `~/.wepld` | reading/corrupting donor profiles |
| Hidden refs | `refs/t3/checkpoints/…` | `refs/wepld/checkpoints/…` | two products restoring each other's checkpoints |
| MCP server name | `t3-code` | `wepld` | tool-name clashes in agent configs |
| Env vars | `T3_*`, `ORCA_*` | `WEPLD_*` | leakage into agent env |
| Telemetry | PostHog, Clerk | none (local OTel only) | data egress |

CI gate (Phase 2 exit): grep for donor identifiers and endpoints fails the build.
