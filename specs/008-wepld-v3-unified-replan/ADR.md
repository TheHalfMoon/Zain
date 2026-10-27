# Architecture Decision Records (V3)

All ADRs: `STATUS = PROPOSED` until this package is merged and the founder signs `FOUNDER_DECISION_RECORD.md`.

---

## ADR-001 — Foundation ownership: T3-first, Orca modules, Rust Core authority

- **Context:** Need one shell + agent control plane. Candidates verified at source: T3 @36d4d711 (~1.0M LOC, single
  event-sourced store, server-first) and Orca @e310a636 (~2.37M LOC, three stores, Electron-first, stronger IDE breadth).
- **Decision:** Option A. Hard-fork T3 (shell, server, orchestration, providers). Port Orca modules D2–D7 into
  WePLD-owned packages. Rust Core is the authority sidecar.
- **Alternatives rejected:** B Orca-first (≥30–60 pw before trust work, fourth store, 421 Windows issues); C dual app via
  `orcad` (two runtimes/stores, non-public RPC, doubled RAM) except as a time-boxed bridge; D own platform (60–120 pw)
  kept as fallback; E unmodified T3 + outside-agent Core (no per-effect authority); F merge both apps.
- **Consequences:** inherit Effect 4 + T3 bugs; no upstream tracking; fastest path to a working product.
- **Revisit if:** G2 or G3 fails (`00_*` §7).

## ADR-002 — Electron (inherited) over Tauri for the shell

- **Context:** WePLD's Tauri shell is a ~1k-line status demo; T3 and Orca are Electron; T3's browser automation,
  preview webviews, `printToPDF`, Orca's Design Mode capture rely on Electron `webContents`/CDP; T3 runs its server
  as Node (`ELECTRON_RUN_AS_NODE`).
- **Decision:** Electron 44 (T3's). Retire the Tauri host after P3 proves the Core sidecar under the new shell.
- **Alternatives:** Tauri + Node sidecar + port of T3 web UI (needs a bundled Node runtime anyway, loses webContents/CDP
  parity on WebView2/WebKitGTK; months of porting for a RAM gain that is unmeasured).
- **Consequences:** higher baseline RAM (measured in B2, budgeted); `glib` vendor patch can be retired.
- **Revisit if:** B2 budget fails twice after stripping and lazy-loading.

## ADR-003 — Editor, canvas and Design Studio

- **Decision:** Monaco (MIT) as the editor surface (with Orca diff-comments port), no LSP in v1 (DEFER; candidate
  monaco-languageclient later). Design Studio = WePLD-built iframe-artboard canvas + Orca Design Mode capture + Onlook-style
  element→source mapping + Excalidraw freeform layer + DTCG tokens (Style Dictionary). Reject tldraw (license),
  Webstudio (AGPL), Craft.js (dormant).
- **Consequences:** Design Studio is the largest net-new UI (P7, 6–10 pw).

## ADR-004 — Event and state ownership: one authority per fact

- **Context:** T3's log compacts, snapshots, rewrites payloads, prunes outbox outcomes (R02 §11). Spec 006 §19 needs
  durable, unknown-aware effect receipts.
- **Decision:** T3 `statev2.sqlite` is authoritative for conversation/run/UI state; Core Ledger (append-only,
  hash-chained, `synchronous=FULL`) is authoritative for grants, decisions, effect outcomes, missions, continuations,
  completion and Brain. No fact has two writers. Cross-links: `wepld.receipt-linked` (compaction-exempt) in T3; T3 ids in
  ledger payloads.
- **Rejected:** making T3's log the single evidence log (requires disabling compaction → 17 GiB class growth, #21154);
  adding a second orchestrator (Vercel Workflow, Orca orchestration).

## ADR-005 — Workflow engine: T3 executor + Core continuations; Vercel as patterns only

- **Decision:** T3 EffectWorker remains the sole executor. Core owns mission-level continuations and fires idempotent
  commands into T3. Adopt Vercel/durable-harness patterns (World invariants, effect sandwich, replay classes extended with
  RECONCILABLE, epoch fencing, crash drills).
- **Rejected:** Workflow SDK runtime (Local World dev-only/no fsync; compiler coupling; Electron untested; second
  orchestrator); durable-harness runtime (0.0.1, Vercel Sandbox dependency).

## ADR-006 — Memory (Project Brain)

- **Decision:** Core Brain in the ledger SQLite family: typed entries (decision, constraint, preference, spec, fact,
  mission summary, compaction capsule) with provenance refs, supersede-not-edit, FTS5 search, per-project isolation,
  incognito = no writes. Injection via capsule at turn start + `brain.query` MCP tool. Vector search, code graph
  (Maemar) deferred.
- **Rejected for v1:** vector DB service; provider-native memory as authority.

## ADR-007 — Permissions and the Claude/provider authority relay

- **Decision:** Core Nawat is the only PDP. Seams S1–S8 (P3), S9 sandbox (P8). UX modes Manual / Auto-with-review /
  Skip × per-tool Always / Needs approval / Blocked compile into Core policy; Skip never overrides Blocked; Full access only
  inside sandbox. Claude via SDK with PreToolUse hook → Core, compiled deny floor, `canUseTool` → Inbox. Cedar is the
  first policy-engine candidate (Ponytail may choose hand-written Rust rules if smaller).
- **Claude SDK distribution:** do not bundle `@anthropic-ai/claude-agent-sdk` in the installer until G4; resolve from the
  user's environment or install-on-consent showing Anthropic terms.

## ADR-008 — Providers and workers

- **Decision:** v1 workers: Claude (API key/Bedrock/Vertex/Foundry), Codex (app-server), ACP family (registry), OpenCode,
  Pi, local models via OpenAI-compatible/ACP agents, and CLI agents in PTYs (Orca catalog) as "unmanaged-but-observed"
  workers with weaker authority (PTY input/outputs only). No silent fallback; route changes recorded in ledger. Per-role
  pins (reviewer ≠ builder).
- **Rejected:** embedding proprietary agents as libraries (Amp core, Cursor internals); subscription-credential proxying.

## ADR-009 — Self-hosting and remote

- **Decision:** Same Server+Core stack runs headless as an opt-in runner on user hardware; clients connect over
  LAN/Tailscale with T3's scoped/DPoP auth. No WePLD-hosted relay or cloud in v1. Project bundle export/import for
  machine moves; live multi-device sync deferred (CRDT candidates Loro/Yjs).

## ADR-010 — Repository visibility and enforcement

- **Context:** repo is private; branch protection unavailable on the current plan (403); integrity workflow fails on
  compare API (403) since 2026-09-29.
- **Decision options for founder:** (a) make public again (free protection, unlimited public Actions; IP exposure),
  (b) stay private + GitHub Pro/Team for protection, (c) stay private, free: workflow `permissions: contents: read`,
  process-level guard (`--match-head-commit`) only. **Recommendation: (b) if budget allows, else (c)**; (a) only if the
  founder is comfortable with public code (it was public until September).

## ADR-011 — Governance and build method reset

- **Decision:** Keep the *semantics* of BUILD_METHOD (spec → Ponytail → source check → implement → deterministic gates →
  independent review → security review for T2 → reconcile → accept → learn). Replace the mechanism: one stable
  `governance_check.py` running from the base SHA, `PROTECTED_PATHS` manifest, risk tiers T0/T1/T2, exact-head merge
  guard. Independent review: at least one qualified reviewer distinct from the builder route; when hosted reviewers are
  unavailable, an independent-model local review with recorded limitation is an allowed T0/T1 substitute (founder
  authorization recorded once in the ADR, not per PR); T2 still requires a qualified independent reviewer or `REVIEW_BLOCKED`.
- **Consequences:** ends successor-per-edit (≥3 PRs per test fix); preserves trusted-base, exact-head and no
  self-authorization properties. Requires its own bootstrap PR (P0), which the current trusted base will judge.
