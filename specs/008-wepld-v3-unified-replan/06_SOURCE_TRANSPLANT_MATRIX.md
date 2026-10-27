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
| D1 | Shell, server, orchestration, providers, worktrees, diff, terminal, browser, packaging | pingdotgg/t3code @36d4d711 | MIT, PUBLIC-OSS + FOUNDER-ATTESTED | `apps/{desktop,web,server}`, `packages/{contracts,client-runtime,provider-*,source-control-*,shared}` | **FORK FOUNDATION** | ~1M LOC of working, tested product | Hard fork; cherry-pick security fixes monthly; no rebase | Effect 4 learning curve; Windows/storage debt; churn | T3's own 1,693 test files must pass on fork (baseline ratio recorded in P1) + Zain seam tests | 18–34 (MVP) | M |
| D2 | Design Mode element capture | stablyai/orca @e310a636 `src/main/browser/grab-*.ts`, `browser-grab-payload.ts`, `src/shared/browser-grab-types` | MIT | as listed | **PORT (ADAPT)** | ~1.1k LOC hard-won UX | Owned copy; no sync | Electron capture glue differs from T3 | AT-01..05 (03B) | 3–6 | M |
| D3 | CLI agent catalog + hook/OSC 7501 status | Orca `src/shared/tui-agent-config*.ts`, `src/shared/{agent-hook-listener,program-status}` | MIT | as listed | **PORT** | 45 CLI agents' launch/ready rules | Catalog curated in Zain | CLI drift. **Never write hooks into the user's global `~/.claude`/`~/.codex`**: use per-launch overlays (`CLAUDE_CONFIG_DIR`, `CODEX_HOME`) and an authenticated loopback hook endpoint (per-PTY secret) so other local processes cannot spoof status. CLI agents are `UNMEDIATED` workers (07 §6) | PTY agent launches; status detection fixture tests | 3–5 | M |
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
| D22 | Review producer (local) | The-PR-Agent/pr-agent @ae053ea8979a | MIT | — | **REFERENCE only** (superseded by D26) | — | pin | model cost | review fixture tests | 1–2 | M |
| D23 | Eval harness | UKGovernmentBEIS/inspect_ai @1692fd8d7364; harbor-framework/terminal-bench @6964e9252c90 | MIT / Apache-2.0 | — | **INTEGRATE (Phase 6 benchmarks)** | — | pin | — | B-suite in 09 | 1–2 | M |
| D24 | Sync/CRDT (multi-device, later) | loro-dev/loro, yjs | MIT | — | **DEFER** | — | — | — | — | — | — |
| D25 | Existing Zain Core | TheHalfMoon/Zain `crates/{contracts,core}` @0a843a2 | owned | as listed | **KEEP** | tested S1/S2 | owned | — | existing 19k-line test suite | 0 | H |

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
- Shipped UI and product-owned symbols are Zain-branded; credits live only in notices/about.

## 4. Rename and collision register (fork identity)

| Surface | Donor value | Zain value | Collision risk if missed |
|---|---|---|---|
| App ID / AUMID | `T3Tools.T3Code`, `com.stablyai.orca` | `<reverse-domain>.zain.desktop` | notifications/keychain attributed to donor |
| CLI | `t3`, `orca` | `zain` (Server CLI); Core binary → `zain-core` | PATH collision with the existing S2 `wepld` binary (rename Core) |
| Protocol | `t3://`?, `orca://` | `zain://` | deep-link hijack |
| Update feed | T3/Orca GitHub releases | Zain GitHub releases | **silent cross-update to donor binaries** |
| Data dirs | `~/.t3`, `%APPDATA%\Orca`, `~/.orca` | `%APPDATA%\Zain`, `~/.zain` | reading/corrupting donor profiles |
| Hidden refs | `refs/t3/checkpoints/…` | `refs/zain/checkpoints/…` | two products restoring each other's checkpoints |
| MCP server name | `t3-code` | `zain` | tool-name clashes in agent configs |
| Env vars | `T3_*`, `ORCA_*` | `ZAIN_*` | leakage into agent env |
| Telemetry | PostHog, Clerk | none (local OTel only) | data egress |

CI gate (Phase 2 exit): grep for donor identifiers and endpoints fails the build.

## 1b. Founder-amendment components (2026-10-28) — file-level detail in research/R14–R18

| # | Capability → target | Source @ pin | License / rights | Paths (summary) | Decision | Destination | Key risks | Qualification tests | ESTIMATE pw |
|---|---|---|---|---|---|---|---|---|---|
| D26 | Review engine → Zain Code Review | alibaba/open-code-review @375f64cd (v1.13.3) | Apache-2.0 (no NOTICE) + FOUNDER-ATTESTED | Go engine: selection, rules, grouping, reviewers, relocation, filter, manifest, SARIF (~33k LOC) — R14 §5 | **FORK (vendor + patches Z-P1..Z-P6)** | `native/zain-review-engine`, `packages/review-engine` | route override via ambient config (patched), second toolchain (Go), upstream velocity | ZCR-T01..T25 | 11–16 |
| D27 | Review ideas | continuedev/continue @5522c6f4 | Apache-2.0; README: read-only/unmaintained | rules/checks formats | **REFERENCE + small importer** | `packages/review-engine/import-continue` | dead hub/action | importer fixtures | in K-04 |
| D22 | (was) PR-Agent reviewer wrap | The-PR-Agent/pr-agent @ae053ea8 | MIT | — | **REFERENCE only** (replaced by D26) | — | duplicate review system | — | 0 |
| D28 | Engineering loop | cursor/plugins @ab1f702c `pstack/` (v0.15.35) | MIT © 2026 Lauren Tan; names/logos not licensed | 58 skills, 23 playbooks, 2 agents, scripts+tests — R15 App. A | **PORT/ADAPT (renamed)** | `packages/skills/zain-engineering` | upstream churn; persona leakage | ES-AT-01..16 | 11–17 (with E2E) |
| D29 | Verification skills | cursor/plugins @ab1f702c `cursor-team-kit` | MIT © Cursor | control-ui, control-cli, verify-this, run-smoke-tests, deslop | **ADAPT** | same | — | ES-AT | in E-01 |
| D30 | E2E framework | Playwright (SRC-0255) + **UNRESOLVED source**: candidate TheHalfMoon/Ascout @ecada2bc Spec 016 | Playwright Apache-2.0; Ascout founder-owned (relicense confirmation FO-9) | Playwright executor, evidence model, 8 fixtures | **PENDING FO-9** | `packages/browser-verify` | spec/code status mismatch in Ascout | ES-AT e2e | 3–5 (E-03) |
| D31 | Planning skills | mattpocock/skills @59db609e | MIT © 2026 Matt Pocock | 12 adapt + 4 copy + 4 pattern (R16 §5) | **COPY/ADAPT** | `packages/skills/zain-plan` | `pr` contains humanlayer text → excluded | R16 D1–D6, N1–N14 | 7–11 |
| D32 | Browser automation core | T3 `PreviewAutomationBroker`, `CdpRelay.ts` @36d4d711; Playwright @cfe490d9 (v1.64.1) | MIT / Apache-2.0 | R17 §5, §9 | **EVOLVE in fork** | Zain Server `browser/*` | no pre-request redirect gate (new work) | R17 §11 | 11–17 core |
| D33 | User-session lane | Playwright `packages/extension` (MV3) @cfe490d9 | Apache-2.0 | extension + relay | **PORT (P9)** | `packages/browser-extension` | store listing, user profile risk | R17 §11 | 4–6 |
| D34 | Browser agent references | browser-use/browser-harness @4ced8e00; Browser Use @2cc71890; Orca `src/main/browser` @e310a636 | MIT | HAR-from-CDP watchdog idea | **REFERENCE only** | — | whole-Chrome attach, `exec()`, telemetry | — | 0 |
| D35 | Desktop/terminal tools → DeskGate | wonderwhy-er/DesktopCommanderMCP @db3430f2 (v0.3.1) | MIT + FOUNDER-ATTESTED | tool schemas, pure logic (~10 modules) — R18 §4 | **PORT (adapters only)** | `packages/deskgate` | DC is not a boundary; must not bring own spawn/config | DG-N01..N14, DG-B1..B9 | 5–8.5 |
| D36 | Remote Desktop Commander | desktop-commander/remote-desktop-commander @a6573e86 | **All rights reserved; docs only; relay proprietary/unavailable** | — | **EXCLUDED** | — | — | — | 0 |

## 3b. Notice obligations for components D26–D36 and additional dependencies

| Source | Obligation |
|---|---|
| alibaba/open-code-review (Apache-2.0) | keep LICENSE; Apache-2.0 §4(b) prominent change notices in every file modified by Z-P1..Z-P6; no upstream NOTICE file |
| Playwright + MV3 extension (Apache-2.0) | keep LICENSE, upstream NOTICE and ThirdPartyNotices files |
| cursor/plugins pstack + cursor-team-kit (MIT) | per-directory LICENSE texts (© 2026 Lauren Tan; © Cursor); names/logos excluded |
| mattpocock/skills (MIT) | LICENSE (© 2026 Matt Pocock) + per-file manifest hashes; `pr` skill excluded |
| wonderwhy-er/DesktopCommanderMCP (MIT) | LICENSE + copyright line in ported files |
| Orca browser/CDP code if ported (MIT) | Lovecast Inc. copyright line |
| LSP client, DAP (`@vscode/debugprotocol`), jsign, electron-updater, WebAuthn library, ripgrep, PPTX/XLSX libraries | pinned and license-checked at task admission (I-03, I-04, F-11, F-04, C-13, H-04, W-02); `@hediet/json-rpc` license UNKNOWN blocks that client until resolved |

**Founder attestation rule:** FOUNDER-ATTESTED records the founder statement only; it has **no effect** on admission,
license or notice obligations, or trademark rights. Third-party code is governed by its public license.
