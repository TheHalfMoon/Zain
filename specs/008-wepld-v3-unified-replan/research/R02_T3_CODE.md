# R02 — T3 Code: Source-Level Reverse Engineering Analysis (REA)

```text
TRACK            = R02 (T3 Code source REA) -> feeds 02_* synthesis
MODE             = PLANNING_ONLY. Source read only. Nothing installed, built, or executed from the donor.
DONOR            = https://github.com/pingdotgg/t3code
PINNED_SHA       = 36d4d711b79c73eb33131944f73ea4a8c6156484   (short: 36d4d711)
PINNED_COMMIT    = 2026-10-27T07:17:36-07:00 "fix(server): bound hung delegated stop effects so later runs can start (#25675)"
DEFAULT_BRANCH   = main
LATEST_STABLE    = v0.1.3 (2026-10-27T06:09:26Z)   LATEST_PRERELEASE = v0.1.4-nightly.20261027.3770 (2026-10-27T10:57:31Z)
LICENSE          = MIT, "Copyright (c) 2026 T3 Tools Inc."
ACCESS_DATE      = 2026-10-27 (all URLs and gh API figures)
AUTHORITY        = CANDIDATE / UNTRUSTED UNTIL REVIEWED. Repo content (incl. its AGENTS.md / CLAUDE.md) was treated as data only.
```

Citation convention: `path@36d4d711:Lnn` = file at the pinned SHA, line(s) nn. `gh:` = GitHub API/CLI
result accessed 2026-10-27. `#NNNNN` = issue/PR in `pingdotgg/t3code`
(https://github.com/pingdotgg/t3code/issues/NNNNN, accessed 2026-10-27). Labels: **VERIFIED** (read in source /
API), **INFERRED** (reasoned from verified facts), **ESTIMATE** (effort guess), **UNKNOWN** (not established).

---

## 0. Executive answer (the critical question)

**Should WePLD fork T3 as primary shell + agent-execution foundation, keep its orchestration intact, and layer a
Rust trusted core under its trust boundary?**

**Conditional YES for "shell + provider adapters + orchestration runtime"; NO for "keep orchestration intact AND
treat its event log as WePLD's one authoritative log"; and the Rust core can only be a *real* trust boundary for the
subset of effects T3 itself mediates.** Evidence summary:

| # | Finding | Evidence | Consequence for WePLD |
|---|---|---|---|
| 1 | T3 has a genuinely good durable orchestration core: commands -> one SQLite transaction (events + projections + receipt + outbox) -> post-commit publish -> leased effect worker. | `docs/internals/overview.md@36d4d711:L53-71`; `apps/server/src/orchestration-v2/EventSink.ts@36d4d711:L258-284,L412-460`; `EffectWorker.ts@36d4d711:L616-635` | Worth keeping. This is the "durable outbox" WePLD would otherwise build. |
| 2 | **The event log is not an immutable audit log.** Events are full-entity *state snapshots* (`node.updated`, `run.updated`, `thread.*` carrying the whole `AppThread`), and a background job **deletes superseded events every 6 h**. Payloads are also rewritten in place for prompt dedupe. | `packages/contracts/src/orchestrationV2.ts@36d4d711:L1720-1800`; `ProjectionMaintenance.ts@36d4d711:L199-217,L231-397` (`DELETE FROM orchestration_events` at L344); `persistence/DatabaseStorage.ts@36d4d711:L22,L88-127`; `persistence/OrchestrationEventStore.ts@36d4d711:L438-530` | **Direct conflict with "one authoritative event log"** in WePLD's evidence/receipt sense. See §11. |
| 3 | **T3 has no policy decision point of its own.** "Permission modes" are mapped onto each provider's native approval/sandbox settings; default for new threads is **Full access** (Codex `approvalPolicy: "never"`, `sandboxPolicy: dangerFullAccess`; Claude `bypassPermissions`). T3 relays provider-initiated approval requests to the user. | `docs/user/permission-modes.md@36d4d711:L6-17`; `Adapters/CodexAdapterV2.ts@36d4d711:L687-727`; `Adapters/ClaudeAdapterV2.ts@36d4d711:L1481-1485`; `RuntimePolicy.ts@36d4d711` (resolve returns mode+cwd only) | Nawat-as-PDP has clean *hook points* (§10) but in full-access/native-tool providers the agent acts **without asking anyone**. A Rust core is only authoritative if WePLD forces approval modes and/or owns the sandbox. |
| 4 | **Extreme upstream churn.** 1,429 commits in week of 2026-10-18; 1,274 PRs merged in the last 7 days; 2,264 commits between v0.1.0 (Oct 15) and v0.1.3 (Oct 27). | gh: `stats/commit_activity`; gh search `is:merged merged:>=2026-10-20` = 1274; gh compare `v0.1.0...v0.1.3` ahead_by=2264 | A solo founder **cannot track upstream**. Treat as a hard fork pinned at one SHA; cherry-pick only. |
| 5 | **Size and stack weight.** ~1.0 M non-test TS/TSX lines across `apps/*` + `packages/*` (server 238k, web 281k, mobile 157k); `Orchestrator.ts` alone 12,839 lines; `ClaudeAdapterV2.ts` 11,063. Built on Effect 4 (`effect@4.0.5`), Node `node:sqlite`, Electron 44.9.3, pnpm 12, Vite+ 1.4.0, `@tsc-rs/typescript@0.8.0`. | §2 tables | High comprehension cost; every orchestration change is high regression risk without the replay test kit. |
| 6 | **Real reliability debt is storage/DB-writer related**, plus memory growth and Windows rough edges. | #21154, #19780, #25788, #21840, #23482, #21539, #18485, #15579, #2767, #11084, #13544, #25262, #18165 (§13) | Fork inherits these. Event-log compaction (finding 2) exists *because* of #21154. |
| 7 | Gaps vs. WePLD target: no IDE-grade editor/LSP (only a light file editor on `@pierre/diffs`), no design canvas, no Windows background service, cloud features tied to T3 Connect/Clerk/PostHog. Terminal (libghostty-vt + node-pty), in-app browser/preview automation, diff review, worktrees, hidden-ref checkpoints and revert **are present**. | §12 | Shell is "years ahead" for chat/agent control; editor/design are WePLD-owned gaps. |

**Recommendation (detail in §15):** Fork at `36d4d711` (or the `v0.1.3` tag) as a **hard fork**; strip mobile, T3
Connect/relay, Clerk, PostHog, marketing, and low-value providers; keep `apps/server` orchestration-v2, `apps/web`,
`apps/desktop`, `packages/{contracts,client-runtime,shared,provider-core,provider-acp,effect-acp,effect-codex-app-server}`.
Put the Rust core in as a **sidecar policy + receipts service** at five seams (§10). **Redefine "one authoritative
event log" as "one authority per fact"**: the Rust core's append-only, never-compacted receipts log is authoritative for
effect decisions/outcomes; T3's compactable orchestration log is authoritative for conversation/UI state and carries
receipt references. ESTIMATE to a usable WePLD-on-T3 MVP: **~22–38 solo person-weeks** (§14), with high regression risk
concentrated in `Orchestrator.ts`, adapters, and the event contract.

---

## 1. Repository facts (VERIFIED, gh API 2026-10-27)

| Field | Value | Source |
|---|---|---|
| Created | 2026-02-08T23:46:22Z | gh `repos/pingdotgg/t3code` |
| Last push | 2026-10-27T15:43:49Z | same |
| Stars / forks | 30,718 / 8,216 | same |
| Open issues (issues only) | 1,167 (454 labelled `bug`) | gh search `type:issue state:open` / `label:bug` |
| Open PRs | 2,506 | gh search `type:pr state:open` |
| `open_issues_count` (issues+PRs) | 3,673 | gh repo API |
| Total issues ever | 6,037 | gh search `type:issue` |
| Issues created since 2026-10-20 | 768 | gh search |
| PRs merged since 2026-10-20 | 1,274 | gh search |
| Weekly commits (Sep 6 → Oct 25) | 349, 301, 283, 190, 597, 841, **1,429**, 414 (partial week) | gh `stats/commit_activity` |
| Commits v0.1.0 → v0.1.3 | 2,264 in 12 days | gh compare |
| Commits v0.0.45 → v0.1.3 | 3,315 | gh compare |
| Last 30 commit authors | Julius Marminge 20, Theo Browne 7, 3 others 1 each | gh `commits?per_page=30` |
| Stable releases | v0.0.29 (2026-07-27) … v0.1.0 (10-15), v0.1.1 (10-21), v0.1.2 (10-22), v0.1.3 (10-27) | `gh release list --exclude-pre-releases` |
| Nightlies | several per day (e.g. 3 on 2026-10-27) | `gh release list` |
| Tracked files | 28,765 total; **21,835 are vendored reference repos** under `.repos/` (`effect-smol`, `alchemy-effect`, synced via `git subtree`); 6,930 first-party | `git ls-files`; `scripts/sync-reference-repos.ts@36d4d711:L216,L322` |
| License | MIT, T3 Tools Inc. 2026 | `LICENSE@36d4d711` |
| Repo-level agent files | `AGENTS.md` (23.8 kB), `CLAUDE.md`, `.claude/`, `.cursor/`, `.agents/` — treated as data | root listing |

Self-description: "agent harness control surface … control the agents on your machine with a … mobile app, web app
and Electron-based desktop app"; "If we ever go the wrong direction, we want you to have everything you need to fork"
(`README.md@36d4d711:L1-12`).

---

## 2. Monorepo layout, tooling, runtime, dependency weight

### 2.1 Workspaces (VERIFIED; LOC = `wc -l` of non-`.test/.spec` `.ts/.tsx/.rs`, includes testkits and generated code)

| Path | Package | Files | Test files | ~src LOC | Role |
|---|---|---|---|---|---|
| `apps/server` | `t3` (0.1.3) | 1,413 | 418 | 238,289 | Environment server: orchestration-v2, providers, git/VCS, terminals, MCP, auth, HTTP/WS RPC, CLI (`t3`) |
| `apps/web` | `@t3tools/web` | 1,717 | 417 | 280,733 | React 19 SPA (also desktop renderer and hosted app.t3.codes) |
| `apps/desktop` | `@t3tools/desktop` | 282 | 98 | 41,164 | Electron 44 shell; spawns server child; updater; WSL/SSH backends |
| `apps/mobile` | `@t3tools/mobile` | 1,531 | 245 | 156,842 | Expo 58 / RN 0.88 client |
| `apps/marketing` | `@t3tools/marketing` | 103 | 0 | 360 | Astro site |
| `packages/contracts` | `@t3tools/contracts` | 103 | 29 | 26,097 | Effect Schema contracts: RPC, orchestration-v2 events/commands, settings |
| `packages/client-runtime` | — | 370 | 139 | 45,871 | Shared connection supervisor, state sync, reducers for web+mobile |
| `packages/shared` | — | 219 | 90 | 25,262 | Utilities incl. `nodeSqliteClient`, `DrainableWorker`, `KeyedLock`, `PtyAdapter` |
| `packages/provider-core` | — | 67 | 19 | 7,311 | `ProviderAdapterV2` contract, driver/instance model, MCP session helpers |
| `packages/effect-codex-app-server` | `effect-codex-app-server` | 21 | 5 | 61,268 (mostly `_generated`) | Typed JSON-RPC client for `codex app-server` |
| `packages/effect-acp` | `effect-acp` | 23 | 6 | 24,734 (mostly `_generated`) | Typed Agent Client Protocol client/agent |
| `packages/provider-acp` | — | 18 | 7 | 14,268 | Generic ACP adapter incl. client fs/terminal policy |
| `packages/provider-acp-registry` | — | 24 | 5 | 5,352 | ACP registry agents (claudeAcp, copilotAcp, devinAcp, droidAcp …) |
| `packages/provider-{cursor,fx,grok,muse,opencode,pi}` | — | 14–39 each | 3–15 | 1.3k–12.8k each | Per-provider drivers/adapters |
| `packages/provider-testing` | — | 7 | 0 | 531 | Test helpers |
| `packages/source-control-{core,definitions,github,gitlab,bitbucket,azure-devops,forgejo,gitcafe,testing}` | — | 3–60 | 0–18 | 36–13.7k | Forge integrations (PRs, review) |
| `packages/ssh`, `packages/tailscale` | — | 11 / 5 | 4 / 1 | 2.8k / 0.5k | Remote environment transport helpers |
| `infra/relay` | — | 119 | 32 | 16,329 | T3 Connect relay (Cloudflare Workers/Durable Objects via Alchemy) |
| `infra/task-cache` | — | 63 | 11 | 3,710 | CI test cache |
| `native/resource-monitor` | `t3-resource-monitor` (Rust, MIT) | 3 | 0 | 1,366 | **Existing Rust stdio sidecar** (process telemetry) |
| `native/{hyprland,kde}-snap-shot` | Rust | 10 / 14 | 0 / 2 | 1.8k / 1.0k | Linux screenshot helpers |
| `native/libghostty-vt` | C ABI headers + VERSION pin | 32 | 0 | — | Ghostty VT (MIT) for terminals |
| `native/browser-secret` | C (libsecret) | 2 | 0 | — | Reads Chromium cookie key on Linux for browser import |

Totals (INFERRED from the table): ~1.00 M non-test lines in `apps/*`+`packages/*`; 1,693 first-party test files.

### 2.2 Build tooling and runtime (VERIFIED)

| Concern | Value | Source |
|---|---|---|
| Package manager | `pnpm@12.14.0` (workspace + catalog) | `package.json@36d4d711` `packageManager`; `pnpm-workspace.yaml@36d4d711` |
| Task runner / bundler | **Vite+** (`vp`, `vite-plus@1.4.0`; `vite` aliased to `@voidzero-dev/vite-plus-core@1.4.0`). **Not turbo, not bun** (bun only for two replay-recording scripts). | `package.json@36d4d711` scripts; `pnpm-workspace.yaml@36d4d711:L77-78`; `apps/server/package.json@36d4d711:L25-26` |
| TypeScript | `typescript: npm:@tsc-rs/typescript@0.8.0` (a native TS compiler distribution) | `pnpm-workspace.yaml@36d4d711:L75` |
| Effect | `effect@4.0.5` + `@effect/*@4.0.5` (Effect 4 / "effect-smol"); `.repos/effect-smol` vendored as reference | `pnpm-workspace.yaml@36d4d711:L43-65` |
| Node | Dev engine `26.12.1`; server package `^22.16 \|\| ^23.11 \|\| >=24.10`; persistence uses built-in **`node:sqlite`** | `package.json@36d4d711` `engines`; `apps/server/package.json`; `packages/shared/src/nodeSqliteClient.ts@36d4d711:L1,L122,L205` |
| Electron | `electron@44.9.3`, `electron-updater@^6.8.9`, `electron-builder` (patched `app-builder-lib@26.16.1`) | `apps/desktop/package.json@36d4d711`; `patches/` |
| React | `react@19.3.0`, TanStack Router, Tiptap 3, Tailwind 4 | `pnpm-workspace.yaml`; `apps/web/package.json` |
| Lint/format | oxlint + custom `oxlint-plugin-t3code`, `vp fmt`, knip | root `package.json` |
| Patches | 33 `pnpm` patches (Expo/RN, `node-pty@1.2.0-beta.15`, `@effect/vitest@4.0.5`, `app-builder-lib`, `@pierre/diffs`, …) | `patches/` |
| CI | GitHub Actions: `ci.yml`, `windows-tests.yml`, `release.yml`, `release-desktop.yml`, mobile EAS, relay deploy, AUR | `.github/workflows/` |

### 2.3 Dependency weight (VERIFIED from package.json; direct deps only)

| Package | deps | devDeps | Notable heavy deps |
|---|---|---|---|
| `apps/server` | 38 | 17 | `@anthropic-ai/claude-agent-sdk@^0.3.276`, `@cursor/sdk@1.0.38`, `@opencode-ai/sdk@^1.3.15`, `@muse-code/sdk@1.4.6`, `playwright-core@1.60.0`, `node-pty@^1.2.0-beta.15`, `@napi-rs/keyring`, `@ff-labs/fff-node`, `zod@^4.6.5`, `undici` |
| `apps/web` | 71 | 20 | Tiptap (14 pkgs), `pdfjs-dist@6.4.299`, `sql.js@1.15.0`, `katex`, `@betteroffice/{docx,pptx,xlsx}`, `@pierre/diffs`, `@pierre/trees`, Clerk (`@clerk/clerk-js`, `@clerk/react`, `@clerk/electron`) |
| `apps/desktop` | 20 | 7 | `electron@44.9.3`, `playwright-core`, `ffi-rs`, `dbus-next`, `@crowecawcaw/xa11y`, Clerk electron/passkeys, `electron-webauthn` |
| `apps/mobile` | 86 | 11 | Expo 58 (~40 `expo-*`), RN 0.88, Reanimated, Nitro modules, local tarballs of forked RN libs |
| `packages/*` (24 pkgs) | 1–18 each | 0–6 | mostly workspace + `effect` |
| `pnpm-lock.yaml` | ~3.6k package entries (rough grep count; INFERRED) | | 912 kB lockfile |

---

## 3. Orchestration V2 — architecture and source of truth

### 3.1 Design intent (VERIFIED, `docs/orchestration-v2/README.md@36d4d711`)

- "V2 is an orchestrator rewrite, not a rewrite of the whole app domain platform" (L5). Codex app-server is the
  reference protocol; weaker providers adapt into the same model "with app-owned ids and explicit capability flags" (L7).
- Key invariants (L31-42): app ids primary, provider ids are refs; child completion never closes parent run;
  checkpoints attach to checkpointable scopes; rollback in app run count reconciled with provider; capability-driven
  policy; provider switches create explicit context-handoff artifacts; replay-backed integration tests.
- Layering (L44-54): native protocol -> rotating raw diagnostics -> adapter/normalizer -> **V2 event store** -> runtime
  graph -> conversation projection -> UI/API views.
- "Raw provider diagnostics … for debugging and replay capture. The durable app state is the normalized orchestration
  state: events/entities, correlation refs, projections, and command receipts." (L56)
- The doc still describes the durable outbox as a "Tracked Follow-Up" (L110-166), but **it is implemented** at the pinned
  SHA (`EffectOutbox.ts`, `EffectWorker.ts`) — the doc is stale on this point (VERIFIED by source).

`docs/internals/overview.md@36d4d711:L53-71` is the current statement: "The event log is the source of truth for
orchestration state. The v2 orchestrator serializes commands and decides events without performing provider or
filesystem work. EventSink commits events, persisted projections, the accepted command receipt, and outbox effects in
one database transaction. Subscribers receive events after that commit." and "A command acknowledgement therefore means
the intent committed, not that the provider … finished."

### 3.2 Module map (VERIFIED; `apps/server/src/orchestration-v2/`, 163 entries, 110 `*.test.ts`)

| Module | Lines | Responsibility | Key symbols |
|---|---|---|---|
| `Orchestrator.ts` | 12,839 | Command decider. Per-thread keyed lock, receipt check, `dispatchOnce` → planned events+effects, `commitCommand`. | `OrchestratorV2Shape` (L320-422), `dispatch` (L331), `dispatchWithReceiptEffect` (L12146-12320), `threadDispatch.withLock` (L12365-12411) |
| `EventSink.ts` | 1,019 | **Single write path.** Transaction: append events → apply projections → upsert projection metadata → enqueue outbox; then serialized post-commit publish. Conditional writes (`writeIfRunCurrent`, `writeIfProviderThreadOwner`, `writeIfProviderThreadUnchanged`). | `commitThenPublish` (L258-284), `applyStoredEvents` (L356-384), `writeEffect` (L412-460) |
| `EventStore.ts` | 156 | Thin V2 facade over `persistence/OrchestrationEventStore.ts` | `EventStoreV2Shape` (L50-73) |
| `CommandReceiptStore.ts` | 202 | Idempotency receipts (`accepted`/`rejected`, `resultSequence`) | `CommandReceiptV2` (L43-52), `insertIfAbsent` |
| `EffectOutbox.ts` | 724 | Durable effect queue table `orchestration_v2_effect_outbox` with leases, per-thread FIFO, cancellation, process-loss reconciliation, 7-day pruning | `OrchestrationEffectRequestV2` (L32-120), `REPLAY_SAFE_EFFECT_TYPES_AFTER_PROCESS_LOSS` (L122-134), `PROCESS_BOUND_EFFECT_TYPES` (L136-142), `SETTLED_EFFECT_RETENTION = 7 days` (L156), `reconcileAfterProcessLoss` (L492) |
| `EffectWorker.ts` | 941 | Claims effects, executes via services, succeed/retry/fail. Defaults: lease 30 s, maxAttempts 5, concurrency 4. | `OrchestrationEffectExecutorV2.execute` switch (L99-560), worker options (L616-635), `DEFAULT_EFFECT_WORKER_CONCURRENCY = 4` (L871) |
| `ProjectionStore.ts` | 7,726 | Projection tables (`orchestration_v2_projection_*`), reads, snapshot windows | `ORCHESTRATION_V2_PROJECTION_SCHEMA_VERSION` |
| `ProjectionMaintenance.ts` | 405 | `verify`, `rebuild` (wipe + replay), **`compactEventStore`** | L120-137 wipe, L199-217 supersedable types, L231-397 compaction |
| `ProviderEventIngestor.ts` | 890 | Adapter event → domain events; retries BEGIN IMMEDIATE busy failures | L73-79 retry rationale, `ingestNormalized` (L293) |
| `ProviderSessionManager.ts` | 2,462 | Opens adapter sessions, issues per-session MCP credentials, fans out adapter events to ingestor | MCP creds L437-487, `openSession` L2113, `ingestNormalized` L1951 |
| `ProviderTurnStartService.ts` | 1,443 | Executes `provider-turn.start` effect | — |
| `RuntimeRequestService.ts` | 142 | Executes `runtime-request.respond` (approval/user-input answer) against live provider session | `respond` (L~85-140) |
| `RuntimePolicy.ts` | 154 | Resolves runtime policy = `{runtimeMode, interactionMode, cwd}` from thread | `RuntimePolicyV2Override` (approval/sandbox `Unknown`) |
| `RunFinalizationService.ts` | 126 | After a run: capture checkpoint, refresh workspace/VCS/PR status | `finalize` (L57-87) |
| `ThreadSettlementService.ts` | 692 | Server-owned "settle" (auto-archive) by PR state/inactivity | — |
| `ProviderRuntimeRecoveryService.ts` | 791 | Startup/shutdown reconciliation: terminalize runs, stop sessions, close requests, retire/requeue effects, restart continuations | `reconcile`, `recover`, `prepareForShutdown` (L68-76, L700-788) |
| `CheckpointCaptureService.ts`, `CheckpointRollbackService.ts` (382), `CheckpointRestoreSafety.ts` (91), `CheckpointService.ts` (593) | — | Checkpoint capture/rollback coordinated with provider thread rollback | — |
| `ThreadForkService.ts`, `ProviderSwitchService.ts`, `ContextHandoffService.ts` | — | Forks, provider switches, portable handoffs | — |
| `Adapters/*AdapterV2.ts` | Claude 11,063; Codex 7,495; Antigravity; testkits for Acp/Cursor/Fx/Grok/Muse/OpenCode/OpenCode2/Pi | Provider adapters living in server (others live in `packages/provider-*`) | — |
| `legacy/LegacyV1ThreadImporter.ts` | — | V1 → V2 lazy transcript importer | — |
| `testkit/` | 94 fixture dirs | Replay harness + scenario integration tests | `ProviderReplayHarness.ts`, `DeterministicRuntime.ts` |

### 3.3 Storage engine (VERIFIED)

- **SQLite via Node's built-in `node:sqlite` (`DatabaseSync`)**, wrapped as an Effect `SqlClient` with a reader worker
  and a checkpoint worker thread: `packages/shared/src/nodeSqliteClient.ts@36d4d711:L1,L205-209,L505-520`;
  `apps/server/src/persistence/Sqlite.ts@36d4d711:L44-62` (`readerWorker: true`, `checkpointWorker: true`).
- File: `<stateDir>/statev2.sqlite` (`apps/server/src/config.ts@36d4d711:L148`). First V2 launch snapshots V1
  `state.sqlite` via `NodeSqlite.backup` and migrates only the copy (`persistence/initializeV2Database.ts@36d4d711:L24,L36`;
  `docs/internals/legacy-orchestration-migration.md@36d4d711:L3-8`).
- Pragmas (`persistence/Sqlite.ts@36d4d711:L12-33`): `busy_timeout=5000`, `foreign_keys=ON`,
  `auto_vacuum=INCREMENTAL` (new DBs only), `journal_mode=WAL`, **`synchronous=NORMAL`** (comment: "OS crashes or power
  loss can roll back post-checkpoint commits without corruption"), `checkpoint_fullfsync=ON`, `journal_size_limit=32 MiB`.
- Migrations: 69 numbered + `Migrations/OrchestrationV2/*` (Foundation, ApplicationEventSource, EffectCancellation,
  RecoveryIndexes, Subagents, ThreadLaunchWorkflows, …) under `apps/server/src/persistence/Migrations/` run by
  `Migrations.ts` at layer setup (`Sqlite.ts@36d4d711:L33`). 88 files in the folder.
- Other durable state **outside** the DB (VERIFIED `config.ts@36d4d711:L148-167`): `attachments/`, `logs/` (server
  trace NDJSON), `logs/provider/events.log` (raw provider frames; rotating, 10 MiB × 10 files, 512 MiB total, 14 days —
  `provider/EventNdjsonLogger.ts@36d4d711:L26-30`), `logs/terminals/`, `<baseDir>/worktrees/`, git hidden refs in each
  repo, provider-native stores (Codex home, Claude transcripts, Pi session files), desktop `connection-catalog.json`
  (#4750, #23470), OS keyring (`@napi-rs/keyring`).

### 3.4 Event schema (VERIFIED)

Table `orchestration_events` (`Migrations/001_OrchestrationEvents.ts@36d4d711`): `sequence INTEGER PRIMARY KEY
AUTOINCREMENT`, `event_id UNIQUE`, `aggregate_kind`, `stream_id`, `stream_version` (UNIQUE per aggregate+stream),
`event_type`, `occurred_at`, `command_id`, `causation_event_id`, `correlation_id`, `actor_kind`, `payload_json`,
`metadata_json`; plus `application_event_version` (V1=1, V2=2) added by
`Migrations/OrchestrationV2/ApplicationEventSource.ts@36d4d711:L36-39`. **No hash chain / prev-hash / signature
column** (grep over migrations, VERIFIED).

V2 domain event union: `packages/contracts/src/orchestrationV2.ts@36d4d711:L1709-1800+`. Base fields: `id, threadId,
runId?, nodeId?, driver?, providerInstanceId?, rawEventId?, occurredAt`. Types include `thread.created`, 21
`thread.*` state events **whose payload is the whole `OrchestrationV2AppThread`**, `thread.pull-request-link-updated`,
`run.created/updated`, `run-attempt.created/updated`, `run.background-work-cancelled`, `node.updated`,
`subagent.updated`, `provider-session.*`, `provider-thread.updated`, `provider-turn.updated`, `turn-item.updated`,
`message.updated`, `plan.updated`, `runtime-request.updated`, `checkpoint*`, `context-handoff.updated`,
`context-transfer.*`. Command union: `OrchestrationV2Command` (L2753-3217).

**Semantics: state-transfer events ("latest entity snapshot") rather than fine-grained domain deltas** (INFERRED from
payload types; consistent with compaction keyed by `(event_type, stream_id, entity_id)` in
`ProjectionMaintenance.ts@36d4d711:L262-328`).

`actor_kind` is `"provider"` if `rawEventId` set else `"server"` (`OrchestrationEventStore.ts@36d4d711:L500`).
`causation_event_id` is always `NULL` for V2 agent events and `correlation_id` = `command_id`
(`OrchestrationEventStore.ts@36d4d711:L495-498`).

### 3.5 Idempotency and command receipts (VERIFIED)

- `dispatchWithReceiptEffect` (`Orchestrator.ts@36d4d711:L12146-12320`): look up receipt by `commandId`; if
  `rejected` → `OrchestratorCommandPreviouslyRejectedError`; if accepted for same thread → return stored events by
  command id with `replayed: true`, **no side effects re-run**; thread mismatch → `OrchestratorCommandIdConflictError`.
- Rejections are persisted via `eventSink.commitRejectedCommand` so a retry sees the same rejection.
- Commands that plan no events still record a receipt (`L12271-12300`).
- Outbox insert is `ON CONFLICT(effect_id) DO NOTHING` (`EffectOutbox.ts@36d4d711:L404`).
- Dispatch is serialized per thread with keyed semaphores; parent/child locks taken sequentially "never nested … neither
  reentrant nor deadlock-aware" (`Orchestrator.ts@36d4d711:L12365-12411`).
- Known gap: #16184 (open) "Retrying an MCP mutation with the same clientRequestId creates duplicate work after a server
  restart"; #11168 (open) duplicate child dispatch after a 5-min client ceiling.

### 3.6 Replay semantics (VERIFIED)

- Projections are rebuildable: `ProjectionMaintenance.rebuild` deletes all `orchestration_v2_projection_*` tables and
  re-applies events (`ProjectionMaintenance.ts@36d4d711:L118-190`); `verify` compares `thread.created` streams with
  projection rows (L68-110). Offline `t3 doctor`-style maintenance verifies before and after compaction
  (`persistence/DatabaseMaintenance.ts@36d4d711:L175-190`).
- Because compaction keeps the latest snapshot per entity plus anchors, **replay reconstructs current state but not
  history** (INFERRED from L231-397).
- Client reconnect: thread streams resume by replaying ≤128 events / ≤1 MiB, otherwise a bounded snapshot
  (`ThreadStream.ts@36d4d711:L15-20`); command results return the committed sequence used as a recovery cursor
  (`docs/orchestration-v2/README.md@36d4d711:L108`).

### 3.7 Crash recovery (VERIFIED)

- Commit+publish under `Effect.uninterruptibleMask`; once committed, every subscriber hears before the writer exits
  (`EventSink.ts@36d4d711:L258-284`).
- On restart, `EffectOutbox.reconcileAfterProcessLoss` **cancels** pending/running process-bound effects
  (`provider-turn.start/interrupt/steer/restart`, `runtime-request.respond`) and **requeues** replay-safe ones
  (`EffectOutbox.ts@36d4d711:L122-142,L492-530`).
- `ProviderRuntimeRecoveryService.recover/reconcile` terminalizes non-terminal runs, stops sessions, closes requests, and
  can enqueue `provider-runtime.continue` "restart continuation" effects (`ProviderRuntimeRecoveryService.ts@36d4d711:L478,L624,L700-788`).
- Per-thread FIFO for effects: a pending effect is not claimable while an older pending or a running effect exists on
  the same thread (title generation excepted) — "Retry backoff must block later effects so turns cannot race a pending
  rollback" (`EffectOutbox.ts@36d4d711:L317-345`).
- Durability caveat: `synchronous=NORMAL` (§3.3) — power loss may roll back recent commits. Past corruption bugs:
  #11084 (overlapping server lifecycles corrupted `state.sqlite`, closed 2026-10-14), #13544 (macOS F_FULLFSYNC, closed).
- Unknown-outcome handling for provider effects: process-bound effects are cancelled rather than reconciled against the
  provider — i.e. **no "effect may have happened" state** comparable to WePLD Spec 006 §19 (INFERRED from L136-142 and
  L492-506; e.g. a `provider-turn.start` sent just before a crash is marked cancelled even if the provider started work).

### 3.8 RunFinalization and ThreadSettlement (VERIFIED)

- `RunFinalizationService.finalize` = capture checkpoint then best-effort workspace/VCS/PR refresh; refresh failures are
  logged, not retried, "Retrying a display refresh after the checkpoint is durable blocks the next turn"
  (`RunFinalizationService.ts@36d4d711:L57-87`). Provider-turn completion and finalization are separate milestones
  (`docs/internals/overview.md@36d4d711:L73-80`).
- `ThreadSettlementService` is server-owned auto-settle (archive-like) driven by PR merge/close and inactivity; guarded
  `thread.auto-settle` command; PR sync reactor re-reads links when a run ran a merge/close CLI command
  (`docs/internals/overview.md@36d4d711:L87-97`).

---

## 4. Provider process execution and adapter lifecycle

### 4.1 Supported drivers (VERIFIED `apps/server/src/provider/builtInDrivers.ts@36d4d711:L31-42`)

| Driver | Spawn / protocol | Where | Notes |
|---|---|---|---|
| **Codex** | Spawns `codex app-server` child process; typed **JSON-RPC** via `effect-codex-app-server` | `Adapters/CodexAdapterV2.ts@36d4d711:L78-98,L1374-1402`; `provider/codexLaunchArgs.ts@36d4d711:L13` | Richest protocol; managed ChatGPT auth/handoff (`provider/CodexChatGpt*.ts`) |
| **Claude** | **`@anthropic-ai/claude-agent-sdk`** `query()` in-process (SDK spawns Claude Code) | `Adapters/ClaudeAdapterV2.ts@36d4d711:L48-52,L1419-1496` | `canUseTool` callback (L9265, L9499) |
| **Cursor** | `@cursor/sdk` | `packages/provider-cursor/src/server/CursorSdk.ts` | — |
| **OpenCode** | `@opencode-ai/sdk` against an OpenCode HTTP server (1.x: one server per thread; 2.x: one per instance) | `docs/internals/providers.md@36d4d711:L14-25` | — |
| **Pi** | user's `pi` in **RPC mode** (stdio) | `packages/provider-pi/src/server/rpc.ts`; providers.md L32-37 | — |
| **Grok**, **fx** | **ACP** via `provider-acp` | `packages/provider-grok/src/server/acpSupport.ts`, `provider-fx/.../acpSupport.ts` | — |
| **Antigravity** | ACP runtime with T3-managed installer/profiles | `Adapters/AntigravityAdapterV2.ts@36d4d711:L15-19`; `provider/AntigravityInstallation.ts` | — |
| **Muse** | `@muse-code/sdk` | `packages/provider-muse` | — |
| **ACP Registry** | Any ACP agent from the registry (Claude ACP, Copilot, Devin, Droid …) | `packages/provider-acp-registry/src/server/{claudeAcp,copilotAcp,devinAcp,droidAcp}.ts` | Managed binaries |

Driver kind vs instance: instances are per-account configurations; routing is by instance (`docs/internals/providers.md@36d4d711:L7-10`).
Provider maintenance runs only through the proven owning installer (L77-99).

### 4.2 Adapter contract (VERIFIED `packages/provider-core/src/server/ProviderAdapter.ts@36d4d711`)

`ProviderAdapterV2` service (L632-648): `instanceId`, `driver`, `getCapabilities`, `planSelectionTransition`,
`openSession(input) -> ProviderAdapterV2SessionRuntime` (scoped). Session runtime (L543-631): `events` stream,
`ensureThread`, `resumeThread`, `injectHistory?`, `startTurn`, `compactThread?`, `steerTurn`, `stopTask?`,
`awaitBackgroundTasks?`, `interruptTurn`, `stopSubagent?`, `unloadThread?`, **`respondToRuntimeRequest`**,
`readThreadSnapshot`, `uploadFeedback?`, `mcpApps?`, `rollbackThread`, `forkThread`. Event union
`ProviderAdapterV2Event` (L79-168): `app_thread.created`, `provider_session.updated`, `provider_thread.updated`,
`provider_turn.updated`, `node.updated`, `subagent.updated`, …

Lifecycle (VERIFIED wiring): `EffectWorker` claims `provider-turn.start` → `ProviderTurnStartService.start` →
`ProviderSessionManager` opens/reuses session (`ProviderSessionManager.ts@36d4d711:L2113`) after issuing an MCP
credential (L437-487) → adapter `events` → `ProviderEventIngestorV2.ingestNormalized` (L1951) → `EventSink.write*`.

### 4.3 Permission / approval relay (VERIFIED)

| Provider | Native mechanism T3 uses | Code |
|---|---|---|
| Codex | `turn/start` params `approvalPolicy` + `sandboxPolicy` per runtime mode: Supervised=`untrusted`+`readOnly`; Auto-accept edits=`on-request`+`workspaceWrite`; Auto=`on-request`+`auto_review`; **Full access=`never`+`dangerFullAccess`**. Handles server requests `item/commandExecution/requestApproval`, `item/fileChange/requestApproval`, `item/permissions/requestApproval`, `execCommandApproval`, `applyPatchApproval`. | `CodexAdapterV2.ts@36d4d711:L687-727,L742-750,L5039,L5111,L5184,L5326,L5396` |
| Claude | SDK `permissionMode` (`bypassPermissions` for full access) + `canUseTool` callback bridged into Effect | `ClaudeAdapterV2.ts@36d4d711:L1481-1496,L2360-2390,L9265,L9499-9500,L9758` |
| ACP family | `session/request_permission`; **T3 is the ACP client and implements `fs/*` and `terminal/*`** with a client policy (`allow/ask/deny`, symlink-aware path checks "fail closed") | `packages/provider-acp/src/server/clientPolicy.ts@36d4d711:L7-14,L40,L192-236`; `adapter.ts@36d4d711:L5860,L5876,L5959,L5983` |
| OpenCode | session permission rules; "always" grants avoided (`once`) | providers.md L27-31 |

Flow: provider request → `runtime-request.updated` (pending) + `approval_request` turn item → client answers →
`runtime-request.respond` command commits resolution → effect `runtime-request.respond` → `RuntimeRequestService.respond`
→ `session.respondToRuntimeRequest` (`RuntimeRequestService.ts@36d4d711:~L85-140`). Codex async questions are answered
by a new user message (`responseCapability: { type: "message" }`, providers.md L104-117).

User-facing modes: Supervised / Auto-accept edits / Auto / **Full access (initial default)**
(`docs/user/permission-modes.md@36d4d711:L6-17`). "Providers enforce permissions differently" (L21).

**Assessment (INFERRED):** T3's approval model is *relay*, not *authority*. There is no T3-owned policy engine; the
decision is the provider's (mode) or the human's (prompt). Open bugs in this area: #24882 (pending Claude approval
re-notified ~40×), #21935 (approvals stay pending after delegated task cancel), #22957, #14878 (MCP elicitations
declined without prompt), #23918.

### 4.4 MCP (VERIFIED)

- T3 exposes an authenticated HTTP MCP endpoint at `/mcp` (`docs/orchestration-v2/orchestrator-mcp-server.md@36d4d711:L31-38`).
  It is injected into **its own** provider sessions with a per-session bearer token scoped to environment+thread+instance+
  session, expiring and revoked on release (L40-56). Codex gets `-c mcp_servers.t3-code.url=…` + bearer env var
  (L60-70); Claude gets an HTTP MCP server in SDK options + `allowedTools: ["mcp__t3-code__*"]` (L74-90).
- Tools: create app-owned sub-agents on any provider instance, wait/poll/cancel, create/list/read/rename threads, link
  PRs, send/steer/interrupt runs (L8-18). Implementation: `apps/server/src/mcp/OrchestratorMcpService.ts` (2,964 lines),
  `McpHttpServer.ts`, `McpToolAccess.ts`, `McpSessionRegistry.ts`, `threadAccess.ts`, `WorktreeMcpService.ts`,
  `PreviewAutomationBroker.ts`, `AcpMcpStdioBridge.ts`.
- **Outside agents controlling T3** (`docs/user/outside-agents.md@36d4d711`): Claude Code / Codex / ChatGPT add
  `https://<env>/mcp`, OAuth (PKCE, stateless public clients) via `apps/server/src/auth/McpOAuth.ts`; owner approves with a
  pairing code; grant is **read-only** or a **runtime-mode ceiling** (Supervised…Full access), not a scope list; MCP
  sessions (subject `mcp-client`) are rejected on every non-`/mcp` route (`docs/internals/environment-auth.md@36d4d711:L44-63`).
  Every tool declares its access class in `McpToolAccess` (compile-time).

---

## 5. Auth, remote environments, transport, compatibility

| Concern | Finding | Source |
|---|---|---|
| Ownership model | Execution stays in the environment that owns the workspace; web/desktop/mobile are RPC clients; desktop renderer follows the same boundary | `docs/internals/overview.md@36d4d711:L3-19` |
| Transport | **WebSocket** at `GET /ws`, Effect RPC (`RpcServer.makeProtocolWithHttpEffectWebsocket`) with **JSON** serialization (`RpcSerialization.layerJson`) | `apps/server/src/ws.ts@36d4d711:L108,L3309-3379` |
| RPC surface | 203 `Rpc.make` definitions, 31 streaming | `packages/contracts/src/rpc.ts@36d4d711` (grep counts) |
| Auth | Environment-issued scoped sessions; cookies, bearer, **DPoP**; short-lived WS tickets (DPoP-bound for RPC); per-RPC scope middleware `RpcScopeAuthorization`; pairing links delegate scopes; `terminal:operate` and `orchestration:operate` are effectively root-equivalent ("either can mint a session with every scope") | `docs/internals/environment-auth.md@36d4d711:L6-20,L64-79`; `apps/server/src/auth/RpcAuthorization.ts` |
| Guest links | HMAC tokens for one thread, never in `SessionStore` | same doc L28-40 |
| Remote | LAN/Tailscale direct (`packages/tailscale`), SSH (`packages/ssh`), WSL backend (`apps/desktop/src/wsl/`), and **T3 Connect** cloud relay (Clerk identity, Cloudflare Worker + Durable Objects, managed tunnels) | `docs/internals/t3-connect.md@36d4d711:L1-25`; `infra/relay/` |
| Reconnect | One supervisor per environment, jittered exponential backoff capped at 5 min, liveness probes (500 ms → descriptor probe; 3 s/15 s deadlines) | `docs/internals/connection-runtime.md@36d4d711:L9-37`; `packages/client-runtime/src/connection/supervisor.ts` |
| Version compatibility | Hard gate: `ORCHESTRATION_PROTOCOL_VERSION = 2`; `/ws` rejects missing/mismatched `orchestrationProtocol` query with **HTTP 426**; finer features negotiated by capability flags in the environment descriptor, never by client version | `packages/contracts/src/environment.ts@36d4d711:L13-16`; `ws.ts@36d4d711:L3313-3324`; `overview.md@36d4d711:L21-38` |
| Analytics | Server-owned PostHog delivery; `distinct_id` from hashed Codex workspace / Claude machine id / install id | `docs/internals/product-analytics.md@36d4d711:L1-30` |

---

## 6. Git worktrees, checkpoints, diff review, revert

| Concern | Finding | Source |
|---|---|---|
| Worktrees | `git worktree add [-b new] -- <path> <ref>` in `GitVcsDriverCore`; per-thread env mode `local \| worktree`; worktrees under `<baseDir>/worktrees`; project `t3.json` scripts with `runOnWorktreeCreate`; `worktree prune`; submodule modes | `apps/server/src/vcs/GitVcsDriverCore.ts@36d4d711:L1178,L3704-3705,L4227`; `config.ts@36d4d711:L160`; `contracts/src/environment.ts@36d4d711:L48-52`; `t3.json@36d4d711` |
| Checkpoints | **Hidden refs** `refs/t3/checkpoints/<base64url(threadId)>/turn/<n>`; capture = temp `GIT_INDEX_FILE` + `read-tree --reset HEAD` + add + `write-tree` + `commit-tree` + `update-ref` (no commits on user branch) | `apps/server/src/checkpointing/Utils.ts@36d4d711:L4-9`; `vcs/GitVcsDriver.ts@36d4d711:L819-~1155` (`write-tree` L1108, `commit-tree` L1129, `update-ref` L1151) |
| Restore | `git restore --source <oid> --worktree --staged -- .` then **`git clean -fd -- .`** then `git reset` (destructive for untracked, non-ignored files) | `vcs/GitVcsDriver.ts@36d4d711:L1174-1245` |
| Revert safety | Revert must coordinate provider conversation rollback; providers that cannot roll back reject **before** touching files; restore isolation checked at admission and rollback because checkpoints restore whole checkouts | `docs/internals/overview.md@36d4d711:L82-85`; `orchestration-v2/CheckpointRestoreSafety.ts@36d4d711:L12-60`; `CheckpointRollbackService.ts` |
| Diff | `CheckpointStore.diffCheckpoints` (patch/numstat, byte caps, path filter), `listAuthoredPaths`; UI `DiffPanel`, `components/diffs/*` (`@pierre/diffs`), diff comments/annotations; PR review guides and per-file "viewed" state persisted | `checkpointing/CheckpointStore.ts@36d4d711`; `apps/web/src/components/diffs/`; `persistence/PullRequest{FilesViewed,ReviewGuides}.ts` |
| VCS abstraction | `VcsDriver` with optional `checkpoints` ops — only Git implements them | `checkpointing/CheckpointStore.ts@36d4d711` `resolveCheckpoints` |
| Known issues | #12341 (open) workspace ownership changes racing checkpoint restore; #22315 (open) diff counters collide across chats on same repo; #25146 (open) worktree handoff during streaming turn fails | gh |

---

## 7. Electron packaging, updater, service modes, OS specifics

| Concern | Finding | Source |
|---|---|---|
| Shell | Electron 44.9.3; `main: dist-electron/boot.cjs`; desktop spawns the **server as a child process using `process.execPath` with `ELECTRON_RUN_AS_NODE=1`**; WSL backend uses `wsl.exe` | `apps/desktop/package.json@36d4d711`; `apps/desktop/src/backend/DesktopBackendConfiguration.ts@36d4d711:L522-534,L649`; `DesktopBackendManager.ts@36d4d711:L435-450` |
| Packaging | `scripts/build-desktop-artifact.ts`: Windows **NSIS** (x64/arm64) with server packed as `resources/server.asar` sidecar; macOS DMG (sign + notarize `scripts/sign-macos.ts`, passkey entitlements); Linux AppImage + `.deb`; AUR packaging; Azure Trusted Signing on Windows | `scripts/build-desktop-artifact.ts@36d4d711:L173,L715-779,L1018,L1620,L2700-2802`; `packaging/aur/` |
| Updater | `electron-updater` with GitHub provider; channels `latest`/`nightly` (+ maintainer `preview`); merged update manifests; remote-environment update flow; `.deb` updates via dpkg prompt | `apps/desktop/src/updates/updateChannels.ts@36d4d711:L12`; `DesktopUpdates.ts@36d4d711:L399`; `scripts/merge-update-manifests.ts` |
| Service modes | `t3` CLI: `t3 serve`, `t3 service install/status/restart/uninstall` (systemd user service on Linux, launchd on macOS), `t3 update` with channels, `npx t3@latest`, desktop-bundled server, WSL server tree, SSH remote | `docs/user/background-service.md@36d4d711:L1-60`; `apps/server/src/cli/{service,serviceLauncher,update}.ts`; `apps/server/src/cloud/bootService.ts` |
| **Windows** | Desktop + CLI (`install.ps1`, winget, scoop) supported; **"Windows background services are not supported."**; WSL recommended for agents; dedicated `windows-tests.yml` | `docs/user/background-service.md@36d4d711:L88`; `docs/user/install.md@36d4d711:L60-95`; `.github/workflows/windows-tests.yml` |
| Linux specifics | Pre-ready desktop-entry identity for portals, AppImage Exec refresh, Wayland shortcut caveats, `native/browser-secret` libsecret | `docs/internals/overview.md@36d4d711:L108-120` |

---

## 8. Tests (VERIFIED counts at pinned SHA, excluding `.repos/`)

| Metric | Value |
|---|---|
| Test files (`*.test/.spec.ts(x)`) | **1,693** |
| Integration tests (`*.integration.test.ts`) | 24 |
| Browser tests (`*.browser.test.tsx?`, Vitest browser + Playwright) | 102 |
| `apps/server/src/orchestration-v2` test files | 110 |
| Replay fixture directories (`orchestration-v2/testkit/fixtures`) | 94 (claude 18, opencode2 16, thread 10, grok 7, subagent 6, tool 5, muse 4 …) |
| Frameworks | Vitest via Vite+ (`vp test`), `@effect/vitest` (patched), `effect/testing` `TestClock`, `@vitest/browser-playwright`, Rust `cargo test` for `native/*`, scripted mobile E2E (`scripts/mobile-e2e/*`) |

Meaningful coverage (VERIFIED by file names/headers):
- **Orchestration recovery**: `testkit/OrchestratorReplayRecovery.integration.test.ts` (e.g. "keeps a Claude subagent
  resumed after a server restart in its own thread", L383), `OrchestratorReplayRestartBackgroundNote.integration.test.ts`,
  `ProviderRuntimeRecoveryService{,.regression}.test.ts`, `ProjectionRecovery.test.ts`, `RestartContinuation.test.ts`,
  `BackgroundWorkStop.integration.test.ts`, `EffectWorker.test.ts`, `RunFinalizationQueue.test.ts`.
- **Persistence**: `persistence/OrchestrationEventStore{,.sequence}.test.ts`, `Migrations.test.ts`, per-migration tests,
  `FoundationPersistence.test.ts`, `DatabaseMaintenance.test.ts`.
- **Adapters**: very large per-adapter suites (Claude 14,759 lines, ACP 7,403, Codex 6,742, OpenCode2 4,480) + replay fixtures per provider.
- **Wire/perf budgets**: `test:perf:v2-wire` script lists 16 suites (`package.json@36d4d711`), `apps/server/integration/transferBudgetV2.integration.test.ts`.
- Strategy: "test doubles exist only at true process, network, clock, id, and filesystem boundaries"; mocked
  orchestrator/adapters/sink/projection are disallowed in integration tests
  (`docs/orchestration-v2/testing-strategy.md@36d4d711:L1-50`).

UNKNOWN: line/branch coverage percentages (no coverage report read); CI pass rate; flake rate.

---

## 9. Third-party notices, embedded assets, license obligations

| Item | Finding | Source |
|---|---|---|
| Project license | MIT (T3 Tools Inc.). Obligation: keep copyright + permission notice in copies/substantial portions. | `LICENSE@36d4d711` |
| Notice generation | Web build emits `third-party-licenses.json`; mobile generates a virtual module; build **fails** if a collected package lacks a distributable license or notice text; SPDX templates pinned | `docs/internals/open-source-licenses.md@36d4d711:L1-35` |
| Manual notices | `third-party-licenses.config.json`: 51 custom entries — MIT 35, Apache-2.0 7, CC0-1.0 4, OFL-1.1 1, Apache-2.0 AND OFL-1.1 1, BSD-2-Clause 1, ISC 1, MIT AND Apache-2.0 AND BSD-3-Clause 1 (e.g. opencode Office viewers MIT, Ionic keyboard assist MIT, freesound CC0 sounds) | `third-party-licenses.config.json@36d4d711` |
| Vendored code with own LICENSE | `apps/web/src/components/files/office/LICENSE.opencode`, `apps/web/src/terminal/ghostty/fonts/LICENSE`, `native/libghostty-vt/LICENSE` (MIT, Mitchell Hashimoto & Ghostty contributors; pin `9f62873b…`), mobile `t3-highlights/Vendor/{simde,wasm2c}/LICENSE`, `t3-terminal/THIRD_PARTY_NOTICES.md` | `git ls-files` |
| `.repos/` reference repos | `alchemy-effect` (Apache-2.0), `effect-smol` (UNKNOWN exact license field; Effect is MIT upstream) — **not shipped**, but 21,835 files in tree; strip in a fork | `.repos/alchemy-effect/package.json:L5` |
| Brand assets | `assets/{dev,nightly,prod}` Icon Composer projects + exports; "T3" name/logo | `assets/README.md@36d4d711` |
| Trademark | MIT grants no trademark rights; a fork must rebrand (name, icons, `T3Tools.T3Code` app id, `t3.codes` URLs, `t3` CLI name) — INFERRED legal reading, not legal advice | — |
| Service coupling to strip | Clerk (`@clerk/*`), T3 Connect relay (`infra/relay`, `apps/server/src/relay`, `cloud/`), PostHog analytics (`apps/server/src/telemetry`), Discord release notifier, app store/EAS configs | §2.3, §5 |
| Commercial SDKs | `@anthropic-ai/claude-agent-sdk`, `@cursor/sdk`, `@muse-code/sdk`, `@opencode-ai/sdk` — each has its own license/terms; UNKNOWN which are non-OSS; must be checked before redistribution | `apps/server/package.json@36d4d711` |

---

## 10. Exact seams for a Rust trusted-core sidecar

Precedent: T3 already ships a Rust stdio NDJSON sidecar (`native/resource-monitor`, `PROTOCOL_VERSION = 3`, bounded
queues) located/spawned by `apps/server/src/resourceTelemetry/ResourceMonitorBinary.ts@36d4d711:L62,L158-159`. WePLD's S1
framed-stdio protocol (`01_LIVE_WEPLD_AUDIT.md` §4, "KEEP as the Core sidecar protocol") fits the same pattern: an
Effect `Context.Service` wrapping a scoped child process owned by the **server** (not Electron), so it also works for
headless/WSL/SSH environments.

| # | Seam | Exact location | What the core would do | Enforcement strength |
|---|---|---|---|---|
| S1 | **Runtime policy resolution** (pre-turn) | `apps/server/src/orchestration-v2/RuntimePolicy.ts@36d4d711` `RuntimePolicyV2.resolve` (returns `{runtimeMode, interactionMode, cwd}`; `RuntimePolicyV2Override` has `approvalPolicy`/`sandboxPolicy` as `Unknown`) | Clamp mode (never `full-access`), choose sandbox/approval policy and cwd per grant | Strong for Codex (native sandbox), medium for Claude (permissionMode), weak for others |
| S2 | **Provider approval callbacks** | Claude `canUseToolEffect` `Adapters/ClaudeAdapterV2.ts@36d4d711:L9265-9536`; Codex server-request handlers `CodexAdapterV2.ts@36d4d711:L5039-5396`; ACP `session/request_permission` `packages/provider-acp/src/server/adapter.ts@36d4d711:L5983` | Nawat PDP decides allow/deny/ask before the human prompt; record decision receipt | Only sees what the provider asks about; nothing in full-access/bypass |
| S3 | **ACP client fs/terminal** (T3 executes the effect) | `packages/provider-acp/src/server/clientPolicy.ts@36d4d711:L192-236`; `adapter.ts@36d4d711:L5876` (`terminal/create`), `L5959` (`writeTextFile`); `clientTerminals.ts` | Core is a true PEP: grant-check + execute (or delegate execution to Rust) + receipt | **Strongest** — effect physically passes through T3 |
| S4 | **Effect worker** (T3's own side effects) | `EffectWorker.ts@36d4d711` `OrchestrationEffectExecutorV2.execute` switch L99-560 (turn start, interrupt, steer, restart, runtime-request.respond, provider-thread.rollback, checkpoint.capture, cleanups) | Pre-execution grant revalidation ("effect-time authority"), post-execution outcome receipt incl. unknown-outcome on crash | Strong for listed effect types; it is the natural place for Spec 006 §19 semantics |
| S5 | **EventSink commit hook** | `EventSink.ts@36d4d711:L412-460` (`writeEffect` transaction) and `applyStoredEvents` L356-384 | Mirror committed events (or a digest) to the core's append-only log with `sequence`↔receipt id cross-refs; or require core receipt id on effect-bearing events | Integrity/evidence only (not prevention) |
| S6 | **MCP tool access** | `apps/server/src/mcp/McpToolAccess.ts`, `threadAccess.ts`, `OrchestratorMcpService.ts`; MCP credential issue `ProviderSessionManager.ts@36d4d711:L437-487` | Grants for outside/inside agents calling T3 orchestration tools | Strong for T3 tools |
| S7 | **Git writes / worktrees / checkpoint restore** | `vcs/GitVcsDriver.ts@36d4d711:L819-1245` (capture/restore), `GitVcsDriverCore.ts@36d4d711:L3704` (worktree add), `git/GitManager.ts`, `GitWorkflowService.ts` | Grant-gate destructive ops (`clean -fd`, restore, push, PR merge) | Strong for T3-initiated git; none for agent-run `git` inside a provider shell |
| S8 | **T3 terminals** | `apps/server/src/terminal/Manager.ts`, `NodePtyAdapter.ts`; RPC scope `terminal:operate` | Gate PTY creation/commands initiated via T3 | Strong for T3 terminals |
| S9 | **Process spawn of providers** | `CodexAdapterV2.ts@36d4d711:L1374-1402` (`ChildProcess.make`), `provider-core/src/server/processGroup.ts`, `apps/server/src/processRunner.ts` | Launch providers inside a core-owned sandbox (job object / seccomp / sandbox-exec) | Only way to bound full-capability agents; **not present in T3** — net-new WePLD work |

Where a Rust core **cannot** be authoritative without S9: Claude/Codex/Cursor/OpenCode/Pi running their own tools in
"Full access" or with native auto-approval — those tool calls never reach T3 (INFERRED from §4.3).

---

## 11. Conflicts with "one authoritative event log"

| # | Conflict | Evidence | Severity | Mitigation option |
|---|---|---|---|---|
| C1 | **Events are deleted.** `compactEventStore` deletes superseded `thread.*` state events, read-state events, and all but newest `message.updated`/`node.updated`/`turn-item.updated` (non-command) per entity, plus imported-legacy rows and receipts; scheduled every 6 h at 10% duty. | `ProjectionMaintenance.ts@36d4d711:L199-217,L231-397`; `persistence/DatabaseStorage.ts@36d4d711:L22,L88-127` | **High** | Keep T3 log as operational state; put authority in core log (C-option A), or exempt WePLD receipt event types from compaction (needs contract + compaction change) |
| C2 | **Events are snapshots, not facts.** Payload = full current entity; history of *what changed* is lost after compaction. | `orchestrationV2.ts@36d4d711:L1720-1800` | High | Same as C1 |
| C3 | **Stored payloads are rewritten** for prompt dedupe (`promptSequence` pointer instead of text; restored via SQL `CASE` on read) — rows are not self-contained or byte-stable. | `OrchestrationEventStore.ts@36d4d711:L289-300,L453-466` | Medium | Hash over decoded/restored payload, not stored bytes |
| C4 | **No integrity chain** (no prev-hash/signature column). | migrations grep; `001_OrchestrationEvents.ts@36d4d711` | Medium | Core computes chain over mirrored events |
| C5 | **Second durable queue with mutable state**: `orchestration_v2_effect_outbox` rows mutate `pending→running→succeeded/failed/cancelled`, **pruned after 7 days**. Effect outcomes are not events. | `EffectOutbox.ts@36d4d711:L145-160,L682-690` | High (for WePLD effect receipts) | Core receipts become the outcome record; T3 outbox stays a work queue |
| C6 | **Raw provider truth lives in rotating logs** (10×10 MiB, 14 days), deliberately not in DB. | `README.md (orch-v2)@36d4d711:L56,L103`; `EventNdjsonLogger.ts@36d4d711:L26-30` | Medium (for forensic evidence) | Core stores hashes of raw frames it cares about |
| C7 | **Provider-native state is co-authoritative** for conversation (Codex home DBs, Claude transcripts, Pi session files); rollback "reconciled with provider conversation state". | `README.md (orch-v2)@36d4d711:L37-38,L89-90`; providers.md L32-37; #24486 (Codex shadow-home WAL split) | Medium | Accept as external system of record; core records refs |
| C8 | **Workspace state in git hidden refs**, outside DB; `restoreCheckpoint` is destructive. | §6 | Medium | Core receipts reference checkpoint commit OIDs |
| C9 | **Process-bound effects cancelled on crash**, no unknown-outcome state. | `EffectOutbox.ts@36d4d711:L136-142,L492-506` | High vs WePLD Spec 006 §19 | Implement unknown-outcome in core receipts at S4 |
| C10 | **Durability `synchronous=NORMAL`**. | `Sqlite.ts@36d4d711:L26-28` | Low–Medium | Core log uses fsync-per-commit |
| C11 | Legacy V1 database copied once (`state.sqlite` → `statev2.sqlite`), not refreshed — two historical stores. | legacy-orchestration-migration.md L3-8; #15017 | Low (fork can drop V1) | Drop V1 importer in fork |
| C12 | Other client-side persistent stores: desktop `connection-catalog.json`, mobile `expo-sqlite`, web `sql.js` | #4750, #23470; `apps/mobile/package.json`, `apps/web/package.json` | Low | Out of authority scope |

Conclusion (INFERRED): WePLD cannot honestly say "T3's orchestration log **is** our one authoritative event log" without
(a) disabling compaction (re-opening #21154-class growth: 17 GiB DB, 2.55 M rows on one install) and (b) adding
integrity and unknown-outcome semantics. The coherent rule is **"one authority per fact"**: core log = authority for
grants, decisions, effect outcomes, completion; T3 log = authority for conversation/UI state; each references the other's ids.

---

## 12. Product gaps vs. a WePLD target

| Capability | Present in T3? | Evidence | Gap size (INFERRED) |
|---|---|---|---|
| Multi-provider agent chat, subagents, queue/steer, forks, provider switch | **Yes (strong)** | §3–4 | none |
| Terminal | **Yes** — server-owned PTYs (`node-pty`), libghostty-vt renderer (WASM in web), retention caps 5k lines/8 MiB | `docs/internals/terminal-runtime.md@36d4d711:L1-40`; `apps/server/src/terminal/` | none |
| In-app browser / preview / agent browser automation | **Yes** — Electron webviews, server headless browser (`playwright-core`), preview MCP toolkit, recordings | `apps/web/src/browser/`, `components/preview/`; `mcp/PreviewAutomationBroker.ts`; issues #15579, #18165 | small (stability) |
| File browser & previews | **Yes** — PDF, Office (docx/pptx/xlsx), notebooks, images, fonts, mermaid, large text | `apps/web/src/components/files/` | none |
| File editing | **Light** — `@pierre/diffs` `EditProvider`/`Editor` in `FilePreviewPanel`, `fileSaveSessions`, RPC `projects.writeFile`; "open in external editor" | `FilePreviewPanel.tsx@36d4d711:L33-39,L582`; `contracts/src/rpc.ts@36d4d711:L393` | **Large if WePLD wants IDE**: no LSP, no Monaco/CodeMirror, no refactoring, no debugger |
| Diff review / PR review | **Yes (strong)** — diff panel, annotations, PR review guides, 7 forges | §6; `packages/source-control-*` | none |
| Worktrees / checkpoints / revert | **Yes** | §6 | none |
| Design / visual canvas | **No** (HTML renders + previews only) | `docs/user/html-renders.md`; no canvas package found | **Large** — WePLD-owned |
| Spec/plan artifacts | Plan mode / proposed plans exist; no spec-kit style artifacts | contracts `proposed_plan`, `plan.updated` | Medium |
| Policy engine / sandbox | **No** (relay only) | §4.3 | **Core differentiator gap** (Nawat) |
| Evidence / trusted completion / independent review | **No** | — | WePLD-owned |
| Windows background service | **No** | background-service.md L88 | Medium for Windows-first founder |
| Mobile | Yes (Expo) | `apps/mobile` | Out of scope initially |
| Headless/remote server | Yes | §5, §7 | none |

---

## 13. Real-world reliability problems (gh issues, states as of 2026-10-27)

| Area | Issues | Notes |
|---|---|---|
| **Storage growth** | #21154 (closed) "orchestration_events grows without bound …" — 17 GiB `statev2.sqlite`, 2.55 M rows, `node.updated` 1.21 M rows / 1.94 GB in two days, driven by OpenCode streaming; #19780 (open) intermediate turn-item snapshots outside compaction (78.5 MB); #25788 (closed today) deleted/archived thread history kept; #13166 (closed) bounded retention; #8345 (closed) immutable runtimes consuming disk | Root cause of compaction design (C1) |
| **DB writer stalls** | #21840 (open) opening a long thread blocks writer 7–10 s; #23482 (open) open read txn freezes all writes once WAL > 32 MB; #21539 (closed) Windows desktop disconnects during 36–44 s stalls with 12.5 GB DB; #23372 (open) desktop windowless 8+ min while startup recovery holds a write txn; #17765 (open) snapshot HTTP handlers lack timeout | Single SQLite writer on main event loop is the bottleneck |
| **DB corruption / locking** | #11084 (closed) overlapping lifecycles malformed DB; #13544 (closed) macOS hard shutdown corruption; #15542 (closed) "database is locked" left Claude process unsupervised; #5099, #6097 (closed) | Fixed but indicates fragility |
| **Memory / CPU** | #18485 (open) nightly ~11.5 GB; #15579 (open) hidden preview webviews ~2.7 GB; #2767 (closed) 63 GB after macOS sleep; #18165 (open) Windows headless-shell GPU spin ~5 cores; #16614 (open) device hub ~200% CPU; #6332 (closed) 455 proc/s poller | Preview/browser features are the main leak surface |
| **Stuck runs / recovery** | #15197 (open) Claude run "running" forever; #22510 (open) wake run stuck; #16449 (closed); #16502 (open) Codex subagents fail after shared app-server SIGKILL; #25599 (open) Antigravity tasks stuck; #16184 (open) duplicate work after restart | Run lifecycle edge cases still churning |
| **Windows** | #25262 (open) desktop starts processes but no UI; #21281 (open) crash on OpenCode model setup; #22961 (open) WSL port reuse; #21889 (open) wrong Tailscale address for WSL; #24332, #24367 (open); #18551 (closed) EBUSY temp cleanup; #19681 (open) symlink tests need Developer Mode | Windows is second-class vs macOS/Linux |
| **Crashes (desktop/native)** | #23349 (open) Cursor SDK AbortError crashes backend; #14259, #24315, #16629 (open) Linux AppImage SIGBUS/SIGTRAP; #17476 (open) macOS a11y SIGTRAP | — |
| **Data/config loss** | #4750 (open) non-atomic `connection-catalog.json` can brick app; #23470 (open) undecryptable catalog overwritten → saved environments deleted; #23858 (open) service install rebinds base dir orphaning data | Client-side state hygiene |
| **Approvals** | #24882, #21935, #22957, #14878, #23918 (open) | §4.3 |

---

## 14. Integration cost and regression risk (solo founder) — ALL FIGURES ARE ESTIMATES

Assumptions: one experienced founder, part-time AI-assisted coding, Windows-first dev box, WePLD Rust core S1/S2 already
exist (`01_LIVE_WEPLD_AUDIT.md` §4), fork frozen at `36d4d711`, MVP providers limited to **Claude + Codex + ACP family**.

| Work package | Scope | ESTIMATE (person-weeks) | Regression risk | Notes |
|---|---|---|---|---|
| WP0 Fork hygiene | Rebrand (name/icons/app id/URLs/CLI), delete `.repos/`, mobile, marketing, relay/T3 Connect, Clerk, PostHog, unused providers & forges; make Windows build green | 3–5 | Medium | Clerk/Connect touch auth UI and settings; knip helps find dead code |
| WP1 Ramp-up | Effect 4 idioms, Layer graph (`runtimeLayer.ts` 391 lines, 65 provide/merge), orchestration-v2 invariants, replay testkit | 2–4 | — | Effect 4 is a hard prerequisite; `Orchestrator.ts` is 12.8k lines |
| WP2 Core sidecar plumbing | Effect service spawning Rust core (pattern of `ResourceMonitorBinary.ts`), S1 framed stdio, health/restart, packaging into `server.asar`/desktop resources on Win/mac/Linux | 2–3 | Low–Medium | Server-owned so headless/WSL also work |
| WP3 Policy hooks (Nawat PDP) | S1 runtime-mode ceiling (remove full-access), S2 Claude `canUseTool` + Codex approval handlers + ACP permission, S3 ACP fs/terminal PEP, S6 MCP, S8 terminals | 4–8 | **High** | Each provider's approval semantics differ; the Claude adapter alone is 11k lines with a 14.7k-line test |
| WP4 Effect-time authority at EffectWorker (S4) | Pre-execute revalidation; outcome receipts; unknown-outcome on process loss (replace cancel-only) | 2–4 | High | Touches recovery paths with known open bugs (§13) |
| WP5 Event-log reconciliation (S5) | "One authority per fact": core append-only receipts log + cross-refs in T3 events (new event type(s) in `contracts/orchestrationV2.ts`, projection, migration, compaction exemption) | 3–6 | **High** | Contract change ripples to web client-runtime reducers and wire projection |
| WP6 Process sandbox (S9) — optional for MVP | Launch providers under OS sandbox controlled by core (Windows job objects/AppContainer, macOS sandbox-exec, Linux namespaces/landlock) | 4–10 | High | Net-new; required for real authority over full-capability agents |
| WP7 Editor gap | Embed Monaco/CodeMirror + optional LSP bridge in `components/files` | 3–6 | Low–Medium | Or defer: "open in external editor" exists |
| WP8 Hardening of inherited bugs | DB growth/stalls (#21840, #23482, #19780), Windows startup (#25262), stuck runs | 2–4 initially | Medium | Ongoing |
| WP9 Upstream tracking | Cherry-pick security/critical fixes only | 0.5–1 / month ongoing | Medium | Full rebase infeasible at ~1.3k merged PRs/week |
| **Total to MVP (WP0–WP5 + WP8, excl. WP6/WP7)** | | **~18–34** | | **~22–38 incl. a minimal WP7 editor** |
| **With real sandbox (WP6)** | | **~26–48** | | |

Alternative lower-cost path (ESTIMATE 6–10 pw): run T3 **unmodified** as a donor runtime and have WePLD core act as an
**outside agent** over T3's `/mcp` with a runtime-mode ceiling (§4.4). This keeps upstream updatability but gives the
core **no** per-tool authority (only thread-level mode ceiling), so it does not satisfy Nawat's effect-time authority.

---

## 15. Recommendation

1. **Fork, do not track.** Pin `36d4d711b79c73eb33131944f73ea4a8c6156484` (or `v0.1.3`) as `UPSTREAM_BASE`; record
   it in WePLD's source registry; treat later upstream changes as optional cherry-picks. Churn evidence: §1.
2. **Keep** (high value, hard to rebuild): orchestration-v2 command/receipt/EventSink/outbox/worker pattern; provider
   adapters for Claude, Codex, ACP (+ ACP registry); `client-runtime` connection/state sync; web shell (chat, diff
   review, terminal, files, preview); desktop Electron shell + updater + Windows NSIS packaging; hidden-ref checkpoints;
   replay test kit.
3. **Strip** for v1: `apps/mobile`, `apps/marketing`, `infra/relay`, T3 Connect/Clerk, PostHog analytics, Antigravity,
   Muse, fx, Grok, Cursor (re-add later), V1 legacy importer, `.repos/`.
4. **Do not adopt T3's log as the single authoritative evidence log.** Adopt "one authority per fact" (§11) and make the
   Rust core's never-compacted, hash-chained receipts log authoritative for grants, decisions, effect outcomes and
   completion. Add a `wepld.receipt-linked` reference on effect-bearing T3 events; exempt it from compaction.
5. **Rust core seams in priority order:** S1 (mode ceiling, remove Full access) → S3 (ACP fs/terminal PEP) → S2
   (Claude/Codex approvals) → S4 (EffectWorker effect-time authority + unknown-outcome) → S5 (commit mirror) →
   S6/S7/S8 → S9 (sandbox) when WePLD needs authority over non-ACP agents.
6. **Be explicit about the trust claim:** until S9 exists, WePLD can claim authority only over effects T3 mediates
   (ACP client fs/terminal, T3 terminals, T3 git ops, MCP tools, outbox effects) and over provider approval prompts —
   **not** over tools a provider executes natively.
7. **Gaps WePLD must own:** IDE-grade editor (or defer to external editor), design surface, policy/evidence/completion
   UX, Windows background service.

---

## 16. Unknowns

| # | Unknown | Why it matters |
|---|---|---|
| U1 | Exact license terms of `@cursor/sdk`, `@muse-code/sdk`, `@anthropic-ai/claude-agent-sdk`, `@opencode-ai/sdk` for redistribution in a fork | Packaging legality |
| U2 | `.repos/effect-smol` license field (not read) | Only matters if not stripped |
| U3 | Test coverage %, CI pass/flake rates | Regression-risk calibration |
| U4 | Whether compaction can be safely disabled per event type without projection drift beyond what `verify` checks | WP5 design |
| U5 | Real behavior of Windows desktop at scale (most stall reports are macOS/Linux nightlies) | Windows-first founder |
| U6 | How much of the 1,274 PRs/week is agent-generated and its defect rate | Cherry-pick trust |
| U7 | Whether Claude Agent SDK `canUseTool` is invoked for every tool in all permission modes used by T3 (only `bypassPermissions` path verified) | S2 coverage |
| U8 | Exact `ProjectionStore` table set rebuilt vs. retained across compaction for subagent prompt anchors | Replay correctness |

---

## 17. Reproduction notes

```text
git clone --depth 1 https://github.com/pingdotgg/t3code   (2026-10-27)
HEAD = 36d4d711b79c73eb33131944f73ea4a8c6156484 (main)
gh api repos/pingdotgg/t3code ; gh release list -R pingdotgg/t3code ; gh api repos/pingdotgg/t3code/stats/commit_activity
gh api "search/issues?q=repo:pingdotgg/t3code+type:issue+state:open" (and variants in §1)
gh api repos/pingdotgg/t3code/compare/v0.1.0...v0.1.3
gh search issues --repo pingdotgg/t3code "<term>" (terms: memory leak, database size, disk space, crash, Windows,
  SQLITE_BUSY, data loss, corrupt, stuck running, duplicate, statev2, approval)
Counts: git ls-files filtered by path and by *.test|*.spec|*.integration.test|*.browser.test; LOC via wc -l.
Dependency counts: package.json parsed with a local read-only script (no donor code executed).
```
