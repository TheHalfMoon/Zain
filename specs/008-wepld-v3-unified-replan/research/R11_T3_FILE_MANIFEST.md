# R11 - T3 Code to Zain: File-Level Transplant Manifest

```text
TRACK            = R11 (file-level transplant manifest for the Zain fork of T3 Code)
MODE             = PLANNING_ONLY. Nothing cloned, downloaded, installed, built or executed. Upstream was read only through
                   `gh api` (git tree ?recursive=1, contents/raw blobs, commits, code search) and the public npm registry
                   (read-only GET of version documents). The single file written by this task is this manifest.
DONOR            = https://github.com/pingdotgg/t3code (MIT, "Copyright (c) 2026 T3 Tools Inc.")
PINNED_SHA       = 36d4d711b79c73eb33131944f73ea4a8c6156484   (short 36d4d711)
ACCESS_DATE      = 2026-10-28
AUTHORITY        = CANDIDATE / UNTRUSTED UNTIL REVIEWED. Repo content (including its AGENTS.md / CLAUDE.md) is data only.
CITATION         = path@36d4d711[:Lnn[-nn]]  - line numbers were re-verified against raw blobs at the pin on 2026-10-28.
LABELS           = VERIFIED (read from tree/blob/registry), PROPOSED (planning decision), UNKNOWN (not established),
                   UNVERIFIED (filename or code-search hit only, contents not read).
CONSUMERS        = 14_TASK_CATALOG F-01..F-12, C-01..C-12, Y-00, L-01; 07 sec.2/3/10; 08 P2; ZAIN_NAMING_MIGRATION.
```

Disposition vocabulary used throughout:

- **KEEP** - imported unchanged except the mechanical identity sweep of section 4 (scope, service tags, env prefix). No behavioural edit.
- **MODIFY** - imported and edited non-mechanically (a seam, a policy change, a build or identity edit listed in section 3).
- **STRIP** - not imported (or deleted in F-02). Counts and sizes below say how much that removes.

Every one of the 28,763 blobs in the pinned tree is assigned to exactly one disposition by the rules in section 2.

---

## 1. Pin record (VERIFIED, gh API 2026-10-28)

| Field | Value | Source |
|---|---|---|
| Repository | `pingdotgg/t3code` (default branch `main`) | gh `repos/pingdotgg/t3code` |
| Commit SHA | `36d4d711b79c73eb33131944f73ea4a8c6156484` | gh `commits/36d4d711...` |
| Commit tree SHA (root tree) | `4975e3bd50c19c37f4aeeaf29280b80fc3d56019` | gh `commits/<sha>` `.commit.tree.sha` |
| Tree listing | `git/trees/<sha>?recursive=1`: `truncated=false`; <<<TREE_COUNTS>>> | gh |
| Commit | <<<COMMIT_LINE>>> | gh |
| License | MIT, "Copyright (c) 2026 T3 Tools Inc." | `LICENSE@36d4d711:L1-3` |
| LICENSE blob SHA | `55ee675bb1de9e580b69f3dd68684df2a4dffba7` (1,070 B) | tree |
| Submodule gitlinks | 2 (`.repos/alchemy-effect/submodules/distilled` -> `e02e9d405b88`, `.../floci` -> `493909133db0`); both under STRIPPED `.repos/` | tree (`mode 160000`) |

### 1.1 License and notice files at the pin (excluding `.repos/`)

| Path@36d4d711 | Blob SHA | Bytes | Disposition |
|---|---|---|---|
| `LICENSE` | `55ee675bb1de9e580b69f3dd68684df2a4dffba7` | 1,070 | KEEP -> `THIRD_PARTY/t3code/LICENSE` (verbatim; also referenced from root NOTICE) |
| `third-party-licenses.config.json` | `e6d38a17e2d876bf3a91fb368cf4397428c73b3b` | 26,373 | MODIFY (prune entries of stripped deps; 51 manual entries at pin per R02 sec.9) |
| `scripts/lib/third-party-licenses.ts` | `ed373f99c217b6190664297d2940c77e1e0db6f4` | 41,210 | KEEP (notice-generation gate: build fails on missing notice) |
| `scripts/lib/third-party-licenses.test.ts` | `6db2d4a5b857aba499a55a971beb1d22f3ebe1d4` | 17,746 | KEEP |
| `packages/shared/src/thirdPartyLicenses.ts` | `ab570cb2e1e7013eb1e470cf5944501deced882a` | 3,985 | KEEP |
| `packages/shared/src/thirdPartyLicenses.test.ts` | `0e78ba2b8e0f2367b755a8fb9d462d7f3065d759` | 1,252 | KEEP |
| `apps/web/src/components/files/office/LICENSE.opencode` | `6439474beed8e0271df9862eff97ffd70ec2464c` | 1,065 | KEEP (vendored opencode Office viewers, MIT) |
| `apps/web/src/terminal/ghostty/fonts/LICENSE` | `06eb073d6b545f7f505919a52e6af903f913d4b8` | 1,082 | KEEP (Ghostty fonts) |
| `native/libghostty-vt/LICENSE` | `0a07a66cd1ad6ea35cc3b8150e2c37702fe5989d` | 1,097 | KEEP (MIT, Mitchell Hashimoto and Ghostty contributors) |
| `infra/task-cache/vendor/vite-plus-remote-cache-cloudflare/LICENSE` | `cf067b10e0dcfd4ccc442b46943cf5e6968f6622` | 1,079 | STRIP with `infra/task-cache` (vendored code leaves with it) |
| `apps/mobile/modules/t3-composer-editor/LICENSE` | `30b20e3b5f0f470947ba9480d90587ba07c137b4` | 1,106 | STRIP with `apps/mobile` |
| `apps/mobile/modules/t3-source-text/LICENSE` | `9aa27cb649d9a4c09a3a3fac60af7cd947297b2f` | 1,070 | STRIP with `apps/mobile` |
| `apps/mobile/modules/t3-highlights/Vendor/simde/LICENSE` | `c7f6b6d752a96f0a337351de7841cc5fe1ff780d` | 1,077 | STRIP with `apps/mobile` |
| `apps/mobile/modules/t3-highlights/Vendor/wasm2c/LICENSE` | `d645695673349e3947e8e5ae42332d0ac3164cd7` | 11,358 | STRIP with `apps/mobile` |
| `apps/mobile/modules/t3-terminal/THIRD_PARTY_NOTICES.md` | `0f8a18d50cbd0c3a47a0a9330b07253a8b55955a` | 1,555 | STRIP with `apps/mobile` |

There is **no top-level `NOTICE` file** at the pin (VERIFIED: no path matching `NOTICE` outside the rows above). MIT obligation for a
fork: keep the copyright line and permission text in copies or substantial portions (`LICENSE@36d4d711`); MIT grants no trademark
rights, so name, logo and `T3Tools.T3Code` / `t3.codes` identity are replaced (section 4). Brand art under `assets/` (T3 name/logo) is STRIPPED.

---

## 2. Disposition table (VERIFIED counts and sizes from the pinned tree)

Size = sum of blob sizes from the tree API (bytes; "approx" because git blob size is the stored size, not on-disk size).
"K/M/S" = files that are KEEP / MODIFY / STRIP inside that row. Workspace disposition: **STRIP** when every file is stripped;
**MODIFY** when at least one file is modified or a carve-out is stripped; otherwise **KEEP**.

<<<S2>>>

---

## 3. MODIFY items (exact paths, symbols and line ranges)

All paths exist in the pinned tree (existence is re-checked by the generator; see 3.9). Line ranges are from R02 sec.10 and were
re-verified against the raw blobs; where R02's path was wrong the corrected path is used and noted. "Task" = 14_TASK_CATALOG id.
Rows marked UNVERIFIED were found by filename or code-search hit and still need a content read at F-02/F-03.

**Corrections to R02 (VERIFIED against the tree):**

1. R02 sec.10 S2 cites `CodexAdapterV2.ts@36d4d711:L5039-5396` without a directory; the file is `apps/server/src/orchestration-v2/Adapters/CodexAdapterV2.ts` (7,496 lines). Likewise `ClaudeAdapterV2.ts` is under `Adapters/` (11,064 lines).
2. R02 sec.10 S6 cites `ProviderSessionManager.ts@36d4d711:L437-487` under `provider/`; the file is `apps/server/src/orchestration-v2/ProviderSessionManager.ts` (2,463 lines; L437-487 is the MCP credential issue/revoke block).
3. R02 / ZAIN_NAMING_MIGRATION list the env prefix as `T3_`; the real prefix is `T3CODE_` (e.g. `T3CODE_POSTHOG_KEY` at `apps/server/src/telemetry/AnalyticsService.ts@36d4d711:L64`, `T3CODE_CLERK_PUBLISHABLE_KEY` at `scripts/build-desktop-artifact.ts@36d4d711:L1264`).
4. ZAIN_NAMING_MIGRATION lists the protocol handler as `t3://`; the registered Electron scheme is `t3code` (`t3code-dev` in development): `apps/desktop/src/electron/ElectronProtocol.ts@36d4d711:L16-17`.
5. ZAIN_NAMING_MIGRATION lists hook headers `x-orca-*` (Orca donor); T3's own headers are `x-t3-*` (`ORCHESTRATION_PROTOCOL_HEADER = "x-t3-orchestration-protocol"` at `packages/contracts/src/environment.ts@36d4d711:L16`).
6. `scripts/build-desktop-artifact.ts@36d4d711:L983,L1033-1034` already excludes the `@anthropic-ai/claude-agent-sdk-*` platform packages from the desktop bundle and `pnpm-workspace.yaml@36d4d711:L268-275` overrides all eight of them to `"-"`; the **main** `@anthropic-ai/claude-agent-sdk` package is still a hard dependency of `apps/server` (`apps/server/package.json@36d4d711:L36`) and is therefore bundled into `server.asar`. F-06 only has to move the main package.

### 3.1 Seam S1 - RuntimePolicy and the permission default (F-07, C-07)

| Seam | Path@36d4d711 | Symbols / line ranges | Change | Task |
|---|---|---|---|---|
| S1 | `apps/server/src/orchestration-v2/RuntimePolicy.ts` | L34-40 `RuntimePolicyV2Override` (`approvalPolicy`, `sandboxPolicy` typed `Schema.Unknown`); L42-46 `RuntimePolicyV2Shape.resolve`; L49 service tag; L53-54 `layer` / `resolve` (155 lines) | Ask Core (CoreBridge) for a grant before returning `{runtimeMode, interactionMode, cwd}`; clamp mode (never `full-access`); fill approval/sandbox policy | C-07 |
| S1 | `packages/contracts/src/providerPolicy.ts` | L21 `"danger-full-access"`; L25-31 `RuntimeMode` literals incl. `"full-access"` L29; **L32 `DEFAULT_RUNTIME_MODE = "full-access"`** | Default -> Supervised; remove `full-access` from the selectable literals | F-07 |
| S1 | `packages/contracts/src/settings.ts` | L33 import; L1143 `Schema.withDecodingDefault(Effect.succeed(DEFAULT_RUNTIME_MODE))` | Follows new default; persisted `full-access` decodes to Supervised | F-07 |
| S1 | `apps/server/src/orchestration-v2/DispatchModeLimit.ts` | whole file (1,430 B) | UNVERIFIED relevance (filename + hit for `"full-access"`); treat `full-access` as unreachable | F-07 |
| S1 | `apps/web/src/components/chat/runtimeModeConfig.ts` | whole file (923 B) | UNVERIFIED (filename match); remove Full-access option from picker | F-07 |
| S1 | `apps/web/src/types.ts` | uses `DEFAULT_RUNTIME_MODE` (code-search hit) | Follows new default | F-07 |
| S1 | `apps/web/src/composerDraftStore.ts` | uses `DEFAULT_RUNTIME_MODE` (code-search hit) | Follows new default | F-07 |
| S1 | `apps/server/src/orchestration-v2/Adapters/ClaudeAdapterV2.ts` | L1481-1496 query options (`permissionMode`, `canUseTool`); L2378-2397 `permissionModeForClaudeRuntimePolicy` (`"bypassPermissions"` L2390, L2397; `case "full-access"` L2422) | Never emit `bypassPermissions` unless a Core grant says so | C-07 |
| S1 | `apps/server/src/orchestration-v2/Adapters/CodexAdapterV2.ts` | L687-727 `runtimeModeDefaults` (`approvalPolicy:"never"` L719 + `dangerFullAccess` L722); L742-750 override decode; L790 turn/start params | Core-chosen `approvalPolicy` / `sandboxPolicy` replace per-mode defaults | C-07 |

### 3.2 Seam S2 - provider approval callbacks (C-09)

| Seam | Path@36d4d711 | Symbols / line ranges | Change | Task |
|---|---|---|---|---|
| S2 | `apps/server/src/orchestration-v2/Adapters/ClaudeAdapterV2.ts` | **L9265-9536** `canUseToolEffect` (def L9265; `canUseTool` wrapper L9499-9500; call L9536); options plumbing L1419-1420, L1496 | Every `canUseTool` decision goes through Core `effect.propose` + `dispatch` before the human prompt; receipt | C-09 |
| S2 | `apps/server/src/orchestration-v2/Adapters/CodexAdapterV2.ts` | L5039 `item/commandExecution/requestApproval`; L5111 `item/fileChange/requestApproval`; L5184 `item/permissions/requestApproval`; L5326 `execCommandApproval`; L5396 `applyPatchApproval` | Core decides allow/deny/ask per server request; decision receipt | C-09 |
| S2 | `packages/provider-acp/src/server/adapter.ts` | L5860 approval-required text; L5876 `terminal/create` deny path; L5959 `writeTextFile`; **L5983 `nativeMethod: "session/request_permission"`** (8,524 lines) | ACP permission requests decided by Core | C-09 |
| S2 | `apps/server/src/orchestration-v2/RuntimeRequestService.ts` | whole file (5,692 B; respond flow ~L85-140 per R02) | Receipt on `runtime-request.respond` | C-09 |

OpenCode (`packages/provider-opencode`) and Pi (`packages/provider-pi`) apply their own permission rules (R02 sec.4.3: OpenCode "once" grants); no per-file seam is identified for them - **UNKNOWN**, read at C-09.

### 3.3 Seam S3 - ACP client policy: fs/terminal PEP (C-08)

| Seam | Path@36d4d711 | Symbols / line ranges | Change | Task |
|---|---|---|---|---|
| S3 | `packages/provider-acp/src/server/clientPolicy.ts` | L7 `AcpRuntimePolicy`; L14 `AcpPermissionDisposition = allow\|ask\|deny`; L40-42 symlink-aware canonicalisation, fail closed; **L192-236** `acpPermissionDisposition`, `acpMcpToolApprovalElicitationDisposition`, `acpClientExecuteDisposition`, `AcpApprovalGrantInput`, `AcpClientPolicyGrants`, `makeAcpClientPolicyGrants` (251 lines) | Disposition derives from Core grant; execution routed through Core with receipt | C-08 |
| S3 | `packages/provider-acp/src/server/adapter.ts` | L5876 `terminal/create`; L5959 `clientFileSystem.writeTextFile(request, policy.cwd)` | fs/terminal effect passes through Core | C-08 |
| S3 | `packages/provider-acp/src/server/clientTerminals.ts` | whole file (16,479 B) | Terminal PEP | C-08 |

### 3.4 Seam S4 / S4b - EffectWorker and recovery (C-10)

| Seam | Path@36d4d711 | Symbols / line ranges | Change | Task |
|---|---|---|---|---|
| S4 | `apps/server/src/orchestration-v2/EffectWorker.ts` | L59-69 `OrchestrationEffectExecutorV2` shape/tag; **L97-560** `execute`, `switch (effect.request.type)` L100 (`provider-runtime.continue` L101, `provider-session.detach` L121, `provider-turn.start` L141, `provider-turn.interrupt` L154, steer/restart, `runtime-request.respond`, `provider-thread.rollback`, `checkpoint.capture`, cleanups); 942 lines | Pre-execution grant revalidation; post-execution outcome receipt; EFFECT_OUTCOME_UNKNOWN on crash | C-10 |
| S4b | `apps/server/src/orchestration-v2/EffectOutbox.ts` | L125 `REPLAY_SAFE_EFFECT_TYPES_AFTER_PROCESS_LOSS`; L138 `PROCESS_BOUND_EFFECT_TYPES`; L211 `cancelUnsettled`; **L221 `reconcileAfterProcessLoss`** (interface), impl **L492-530** (process-bound -> `cancelled`, replay-safe -> requeued); L317-345 per-thread FIFO | No cancel/requeue before `core.open_dispatches`; mark unknown-outcome instead of `cancelled` | C-10 |
| S4b | `apps/server/src/orchestration-v2/ProviderRuntimeRecoveryService.ts` | L71-75 `reconcile` / `recover` interface; L194 `reconcileProjection`; L478; L624-627 and L768 `provider-runtime.continue`; L689 `reconcile`; **L700-788** restart continuation | No auto-continue before Core reconciliation | C-10 |

### 3.5 Seam S5 - EventSink and ProjectionMaintenance (C-11)

| Seam | Path@36d4d711 | Symbols / line ranges | Change | Task |
|---|---|---|---|---|
| S5 | `apps/server/src/orchestration-v2/EventSink.ts` | **L258-284** commit + publish under `Effect.uninterruptibleMask` (L263); L355-384 `applyStoredEvents`; **L410-460** `writeEffect` transaction (1,020 lines) | Per-run `zain.run-receipts` link event (sequence <-> receipt id) | C-11 |
| S5 | `apps/server/src/orchestration-v2/ProjectionMaintenance.ts` | L35 `compactEventStore` interface; **L231-397** implementation; **L344** `DELETE FROM orchestration_events WHERE sequence IN ...` (406 lines) | Exempt `zain.run-receipts` events from compaction | C-11 |
| S5 | `apps/server/src/persistence/OrchestrationEventStore.ts` | L438-530 (R02 sec.0: payload rewrite for prompt dedupe) | Verify receipt events are never rewritten | C-11 |
| S5 | `apps/server/src/persistence/DatabaseStorage.ts` | L22, L88-127 (R02 sec.0: `synchronous=NORMAL`) | Review durability for the link event only (Core ledger is FULL sync) | C-11 |

### 3.6 Seam S6 - MCP access (C-12)

| Seam | Path@36d4d711 | Symbols / line ranges | Change | Task |
|---|---|---|---|---|
| S6 | `apps/server/src/mcp/McpToolAccess.ts` | L70-75 read-only gate; L96-218 access-class wrappers `reads / readsAsCaller / actsAsCaller / writes / writesWithCapability / writesThreads / startsThreads / either / writesEnvironment`; L195 full-access message | Core-scoped grants replace read-only / runtime-ceiling grants | C-12 |
| S6 | `apps/server/src/mcp/threadAccess.ts` | whole file (6,543 B) | Thread-level grants via Core | C-12 |
| S6 | `apps/server/src/mcp/OrchestratorMcpService.ts` | whole file (2,965 lines, 116,155 B) | Gate each orchestrator tool; MCP server name `t3-code` -> `zain` | C-12, F-03 |
| S6 | `apps/server/src/mcp/McpHttpServer.ts` | L103 credential error text; L752-767 tool sets (`t3_thread_launch`, `t3_thread_send`, `t3_queue`, `t3_pending_request`, `t3_thread_transfer`); L1082 `name: "T3 Code"`; L1089 advertised-tool set; AnalyticsService import | Tool prefix `t3_*` -> `zain_*`; remove analytics | C-12, F-03, F-05 |
| S6 | `apps/server/src/mcp/McpSessionRegistry.ts` | whole file (8,332 B) | Per-session bearer scope = Core grant id | C-12 |
| S6 | `apps/server/src/auth/McpOAuth.ts` | whole file (20,672 B) | Outside-agent grants (read-only / runtime ceiling) map to Core grants | C-12 |
| S6 | `apps/server/src/orchestration-v2/ProviderSessionManager.ts` | L193-194 `mcpCredentialIdByThread`; L311-312 services; L390-401 reservation maps; **L437-487** credential issue/revoke (`issue` L466, `revokeProviderSession` L483) | MCP credential issue bound to Core grant (path corrected, see Correction 2) | C-12 |
| S6 | `apps/server/src/mcp/WorktreeMcpService.ts` | whole file (17,561 B) | Worktree tools through S7 | C-12 |

### 3.7 Seams S7 / S8 - git destructive operations and terminals (C-12)

| Seam | Path@36d4d711 | Symbols / line ranges | Change | Task |
|---|---|---|---|---|
| S7 | `apps/server/src/vcs/GitVcsDriver.ts` | L308 `pushCurrentBranch`; **L819** `captureCheckpoint` (`write-tree` L1108, `commit-tree` L1129, `update-ref` L1151); **L1161** `restoreCheckpoint` (`restore` L1186, **`clean -fd` L1213**); L1375 `update-ref -d` (1,409 lines) | Gate `clean -fd`, restore, ref delete, push through Core | C-12 |
| S7 | `apps/server/src/vcs/GitVcsDriverCore.ts` | L2335 `reset`; L2489-2646 `push` variants; **L3696-3715 `git worktree add`**; worktree prune/remove sites (4,533 lines) | Gate push / worktree add / remove | C-12 |
| S7 | `apps/server/src/git/GitManager.ts` | whole file (117,748 B) | Gate PR merge / push workflows | C-12 |
| S7 | `apps/server/src/git/GitWorkflowService.ts` | whole file (18,488 B) | Gate workflow-level git writes | C-12 |
| S7 | `apps/server/src/checkpointing/Utils.ts` | **L4 `CHECKPOINT_REFS_PREFIX = "refs/t3/checkpoints"`** | `refs/zain/checkpoints` | F-03 |
| S7 | `apps/server/src/checkpointing/CheckpointStore.ts` | whole file (5,456 B) | Route through gated driver | C-12 |
| S8 | `apps/server/src/terminal/Manager.ts` | L161-214 `TerminalManager` interface; **L2239 `ptyAdapter.spawn`**; L2838 `open`; L3126 `write` (3,361 lines) | Gate PTY creation and commands | C-12 |
| S8 | `apps/server/src/terminal/NodePtyAdapter.ts` | whole file (9,336 B) | PTY spawn hook | C-12 |

S9 (provider spawn under a sandbox) is net-new Zain work and has no upstream file to modify; the precedent for a Rust stdio sidecar is
`apps/server/src/resourceTelemetry/ResourceMonitorBinary.ts@36d4d711:L62,L158-159` (KEEP; C-06 CoreBridge copies its pattern).

### 3.8 Other required modifications

| Item | Path@36d4d711 | Symbols / line ranges | Change | Task |
|---|---|---|---|---|
| ThreadSettlement | `apps/server/src/orchestration-v2/ThreadSettlementService.ts` | L79-82 settled-at from PR state; **L131-134 `autoSettleOnMerge` gate**; L246 `ThreadSettlementServiceV2`; L292 `make`; L343 `type: "thread.auto-settle"` (693 lines) | Cosmetic "archived" only; never a completion signal | F-08 |
| Permission default | see 3.1 (`providerPolicy.ts:L32`) | | Supervised | F-07 |
| Updater feed | `apps/desktop/src/updates/updateChannels.ts` | L1-13 nightly/preview regexes, `resolveDefaultDesktopUpdateChannel` | Zain channel scheme | F-04 |
| Updater feed | `apps/desktop/src/updates/DesktopUpdates.ts` | L267 provider config; L318 "no update feed configured"; L453-463 `setChannel` / `allowPrerelease`; **L1043 `electronUpdater.setFeedURL`** (1,169 lines) | Generic provider, Zain-hosted feed, ed25519-signed manifest verified by Core; reject donor manifests | F-04 |
| Updater feed | `scripts/build-desktop-artifact.ts` | L65 `DESKTOP_APP_ID`; **L2687-2807** `resolveGitHubPublishConfig` (`provider: "github"` L2700; `buildConfig.publish` L2807); L1264-1270 Clerk key; L1620 Azure Trusted Signing; L983, L1033-1034 SDK platform exclusions (4,168 lines) | Generic publish provider; OV cert + jsign (F-11); drop Clerk; identity | F-04, F-11, F-03 |
| Updater feed | `scripts/merge-update-manifests.ts` | whole file (113 lines) | Manifest merge for Zain channels | F-04 |
| Updater feed | `apps/server/src/cli/update.ts` | L63-71 GitHub API with `GH_TOKEN` (548 lines) | Zain release feed; no tokens in client | F-04 |
| Updater feed | `apps/server/src/desktopUpdate/*` (2 files), `apps/server/src/cloud/selfUpdate.ts`, `apps/server/src/cloud/updateHandoff.ts` | filename-based (UNVERIFIED) | Re-point to Zain feed | F-04 |
| PostHog | `apps/server/src/telemetry/*` (9 files) | `AnalyticsService.ts` L64-67 `T3CODE_POSTHOG_KEY/HOST`; L191-216 batch POST; header comment L1 | **STRIP** the directory | F-05 |
| PostHog callers | `apps/server/src/server.ts`, `serverRuntimeStartup.ts`, `ws.ts`, `orchestration-v2/ProviderEventIngestor.ts`, `guest/GuestShareService.ts`, `provider/CodexChatGptAuth.ts`, `mcp/McpHttpServer.ts` | `AnalyticsService` imports (code search; line numbers UNKNOWN) | Remove layer + call sites | F-05 |
| PostHog docs | `docs/internals/product-analytics.md`, `docs/user/telemetry.md` | | STRIPPED with docs | F-05 |
| Clerk / T3 Connect | STRIP set: `apps/server/src/cloud/*` (except 6 service/update files), `apps/server/src/relay/*`, `apps/web/src/cloud/*`, `apps/web/src/components/{clerk,cloud}/*`, `apps/desktop/src/app/DesktopClerk*`, `packages/client-runtime/src/relay/*`, `packages/shared/src/{relay*,connectAuth}.ts`, `packages/contracts/src/{relay,relayClient}.ts`, `apps/server/src/cli/connect.ts`, `infra/relay` | see table 2.2 | Delete; fix importers (rows below) | F-02 |
| Clerk callers | `apps/desktop/src/preload.ts`, `apps/desktop/vite.config.ts`, `apps/desktop/package.json`, `apps/web/package.json`, `apps/web/vite.config.ts`, `apps/web/src/components/{HostedEmptyState.tsx, onboarding/WelcomeWizard.tsx, settings/LabsSettingsPanel.tsx}`, `scripts/lib/{desktop,cli}-external-packages.ts`, `scripts/build-desktop-artifact.ts` | `@clerk` import hits (code search) | Remove Clerk bridge, deps, externals | F-02 |
| Clerk service files kept | `apps/server/src/cloud/{bootService,serviceLauncherClient,servicePreflight,serviceProtocol}.ts` | `bootService.ts` 37,967 B; others name-based (UNVERIFIED) | Keep service-install logic, drop Connect/relay | F-02, F-03 |
| Claude SDK | `apps/server/package.json` | L36 `"@anthropic-ai/claude-agent-sdk": "^0.3.276"`; L37 `@cursor/sdk`; L41 `@muse-code/sdk`; L43 `@opencode-ai/sdk`; L47, L50 workspace cursor/muse | Move the SDK to a user-consented, lazily loaded location (not in `server.asar`); drop cursor/muse | F-06 |
| Claude SDK | `pnpm-workspace.yaml` | L159 `@anthropic-ai/claude-agent-sdk@0.3.276` in `minimumReleaseAgeExclude`; L268-275 eight platform-package overrides | Remove entries | F-06 |
| Claude SDK | `apps/server/src/provider/{ClaudeProvider,ClaudeTurnTokenUsage,claudeUsageLimits}.ts`, `apps/server/src/provider/Drivers/{ClaudeDriver,ClaudeExecutable}.ts`, `apps/server/src/claudeHistoryWorker.ts`, `Adapters/ClaudeAdapterV2.ts` | SDK imports (code-search hits; line numbers UNKNOWN) | Type-only static import; runtime import through a loader | F-06 |
| Claude SDK | `scripts/build-desktop-artifact.ts` | L983, L1033-1034 (existing platform-package exclusions) | Extend to the main package; installer-content gate | F-06 |
| Provider list | `apps/server/src/provider/builtInDrivers.ts` | L1-12 imports; L25-36 `BuiltInDriversEnv`; **L38-49 `BUILT_IN_DRIVERS`** (10 entries); L52-61 usage-reader env; L63-72 `BUILT_IN_USAGE_DRIVERS` (8) | Remove Antigravity, Cursor, Fx, Grok, Muse; keep Codex, Claude, OpenCode, Pi, AcpRegistry | F-02 |
| Browser import | STRIP set (table 2.2): `apps/desktop/src/preview/BrowserImport/**` (18 files, ~95 KB prod), `apps/desktop/scripts/{build-browser-secret,browser-secret-native.test}.mjs`, `apps/web/src/components/settings/{BrowserImportWizard.tsx, browserImportWizard.logic*}`, `packages/contracts/src/browserImport.ts`, `native/browser-secret/*` | R17 sec.5.1, sec.9 row 6 | Delete | Y-00 |
| Browser import callers | `apps/desktop/src/{main.ts, preload.ts, ipc/DesktopIpcHandlers.ts, ipc/methods/preview.ts, ipc/methods/window.ts}`, `apps/web/src/components/settings/IntegrationsSettings.tsx` (+ `.logic.test.ts`), `packages/contracts/src/{index.ts, ipc.ts}` | `BrowserImport` hits (code search) | Remove registrations, IPC channels, exports | Y-00 |
| CdpRelay | `apps/desktop/src/preview/CdpRelay.ts` | 204 lines: L44-47 `ACKNOWLEDGED` set (`Browser.grantPermissions` L45, `Browser.resetPermissions` L46); L75 ack short-circuit; L76-135 method switch | Per-lane method allowlist: deny `Browser.grantPermissions`, `Storage.getCookies`, `Network.getAllCookies` in the agent lane; deny `Fetch.*` from external clients | Y-00 |
| Agent partition | `apps/desktop/src/preview/BrowserSession.ts` | 11,581 B | Isolated, ephemeral agent partition | Y-00 |
| Evaluate off | `apps/server/src/mcp/toolkits/preview/{tools,handlers}.ts` | `preview_evaluate` among 12 tools (R17 sec.5.2) | Default-off outside Preview/Test lanes | Y-00 |
| Protocol bump | `packages/contracts/src/environment.ts` | L13-14 `ORCHESTRATION_PROTOCOL_VERSION = 2`; L16 `ORCHESTRATION_PROTOCOL_HEADER` | Zain-1 + header rename | F-09 |
| Protocol bump | `apps/server/src/ws.ts` | L108; L3309-3379 RPC over WebSocket; **L3313-3324** HTTP 426 gate (153,977 B) | Reject T3 clients | F-09 |
| Plan mode | none required | `L-01` inherits T3 plan mode as-is | Verify enforcement, label "not yet enforced" | L-01 |

### 3.9 Generated cross-check

<<<MODCHECK>>>

---

## 4. Identity occurrence targets (mapping to ZAIN_NAMING_MIGRATION)

`gh api search/code` **works** for this repo. Caveats (VERIFIED): the index covers the default branch HEAD (not the pin), counts are
**files** containing the token (not occurrences), the tokenizer splits on punctuation (so `t3-code`, `@t3tools` and `T3Tools` collapse
to overlapping tokens), and results exclude files over the index size limit. Counts below are therefore indicative; the F-03 grep gate
(Q-03) is the authority, not this table. Counts that include `.repos/` or STRIPPED trees are noted.

| Identifier class | Upstream form(s) at pin | Evidence | Files (search, HEAD 2026-10-28) | Zain target (ZAIN_NAMING_MIGRATION) | Notes |
|---|---|---|---|---|---|
| npm scope | `@t3tools/*` (`web`, `desktop`, `mobile`, `contracts`, plus 20+ `packages/*`) | `apps/desktop/package.json@36d4d711:L2` | 3,352 (token `T3Tools`/`@t3tools` is identical in the tokenizer) | `@thehalfmoon/*` | mechanical; includes ~1,100+ files in STRIPPED trees (`apps/mobile`, `infra/relay`) |
| Service tags | `"t3/orchestration-v2/RuntimePolicy/RuntimePolicyV2"` (`RuntimePolicy.ts@36d4d711:L50`), `"@t3tools/desktop/electron/ElectronProtocol"` (`ElectronProtocol.ts@36d4d711:L67`), `"t3/config/ServerConfig"` (`config.ts@36d4d711:L110`), `"t3/terminal/Manager/TerminalManager"` (`Manager.ts@36d4d711:L214`) | | UNKNOWN (tokenizer cannot match `t3/`) | `zain/...` | mechanical; replay fixtures must not embed tags (verify) |
| Server package / CLI | package `t3` (`apps/server/package.json@36d4d711:L2`), `bin.t3 -> ./dist/bin.mjs` (L10-11); `npx t3@latest`; `scripts/npm-launcher/t3.mjs` | | | CLI `zain` (Server); core binary `zain-core` | F-03, F-10 |
| Lower-case product id | `t3code`, `t3code-dev`, `t3code-server`, `t3code.server.managed_by`, `oxlint-plugin-t3code` | `config.ts@36d4d711:L123-128`; `ElectronProtocol.ts@36d4d711:L16-17`; `DesktopEnvironment.ts@36d4d711:L235` | 674 | `zain` | |
| Domain | `t3.codes` (e.g. `app.t3.codes`) | 73 files, listed in 4.1 | 73 | none yet - **no `zain.*` domain is available** (R19); use build-time config, never hard-code | blocked on N-01/N-02 |
| Display name | `T3 Code`, `T3 Code (Beta)` | `DesktopEnvironment.ts@36d4d711:L89`; `apps/desktop/package.json@36d4d711:L43`; `McpHttpServer.ts@36d4d711:L103,L1082` | 469 | `Zain` | working name; FO-8 clearance pending |
| Hidden git refs | `refs/t3/checkpoints/<base64url(threadId)>/turn/<n>` | `checkpointing/Utils.ts@36d4d711:L4` | `refs/t3`: 14 (5 for `refs/t3/checkpoints`: `checkpointing/Utils.ts`, `orchestration-v2/ProviderEventIngestor.test.ts`, `vcs/GitVcsDriver.test.ts`, `vcs/VcsProcess.test.ts`, `apps/web/src/components/chat/MessagesTimeline.logic.test.ts`) | `refs/zain/checkpoints/` | Q-18 |
| Env prefix | **`T3CODE_*`** (not `T3_`): `T3CODE_POSTHOG_KEY`, `T3CODE_CLERK_PUBLISHABLE_KEY`, ...; build defines `__T3CODE_BUILD_CHANNEL__`, `__T3CODE_TELEMETRY_CHANNEL__` (`config.ts@36d4d711:L24-27`) | | 198 (listed by area in 4.2) | `ZAIN_*` | includes CI workflows and docs |
| App id (Electron) | `com.t3tools.t3code`, `com.t3tools.t3code.dev` | `build-desktop-artifact.ts@36d4d711:L65`; `DesktopEnvironment.ts@36d4d711:L232`; file `apps/desktop/resources/linux/com.t3tools.t3code.metainfo.xml` | | `io.github.thehalfmoon.zain` (placeholder) | |
| AUMID / Windows app id | `T3Tools.T3Code` | 50 files (4.3) | 50 | same placeholder (final after N-01/N-02) | NSIS shortcut AUMID must equal the app id |
| Protocol scheme | **`t3code`** / `t3code-dev` (not `t3://`) | `ElectronProtocol.ts@36d4d711:L16-17` | `t3://` literal appears in 1 file (`oxlint-plugin-t3code/rules/no-raw-mcp-registration.test.ts`) | `zain://` (`zain-dev://`) | NAMING doc row to be corrected |
| Update feed | electron-updater GitHub provider built from `GITHUB_REPOSITORY` (`build-desktop-artifact.ts@36d4d711:L2687-2701`); release lookups via GitHub API (`apps/server/src/cli/update.ts@36d4d711:L63-71`); hard-coded `pingdotgg` in `scripts/install.sh`, `scripts/install.ps1`, `scripts/npm-launcher/t3.mjs`, `scripts/lib/linux-arm64-sea.ts` | | `pingdotgg`: 8 under `scripts/`, 6 under `apps/desktop`, 24 under `apps/server` (mostly tests; lists in 4.4) | Zain-hosted Generic provider, ed25519-signed manifest | F-04 |
| MCP server name / tool prefix | server `t3-code` (docs: Codex `-c mcp_servers.t3-code.url=...`, Claude `allowedTools: ["mcp__t3-code__*"]`, `docs/orchestration-v2/orchestrator-mcp-server.md@36d4d711:L60-90`); tools `t3_thread_launch`, `t3_queue`, `t3_pending_request`, `t3_thread_transfer` (`McpHttpServer.ts@36d4d711:L752-767`); displayed name `T3 Code` (L1082) | | `t3-code`: 140 (over-broad; true count UNKNOWN) | MCP server `zain`; tools `zain_*` | evals also reference it (STRIPPED) |
| Header names | `x-t3-orchestration-protocol` (`environment.ts@36d4d711:L16`); `x-t3-*` webhook / relay headers (22 files, 4.5) | | 22 | `x-zain-*` | NAMING doc says `x-orca-*` for hooks; Orca is a different donor |
| Data dirs | `t3Home` -> default `~/.t3` (`DesktopEnvironment.ts@36d4d711:L163,L180`; definition site UNKNOWN - not in `config.ts`); project file `t3.json` (289 B, repo root) | | UNKNOWN | user dir `~/.zain-ide`; project dir `.zainide/` (decision N-03; must not be `.zain/`); `%APPDATA%\Zain` | `packages/contracts/src/t3ProjectFile.ts`, `packages/shared/src/t3ProjectFile.ts` rename |
| OTLP / service names | `serviceName: "t3code-server"`, `service.namespace: "t3code"`, `service.runtime: "t3-server"` | `config.ts@36d4d711:L123-128` | | `zain-server` / `zain` | |
| Wire protocol id | `ORCHESTRATION_PROTOCOL_VERSION = 2` | `environment.ts@36d4d711:L13` | | `Zain-1` | F-09; T3 clients get 426 |
| AUR / packaging ids | `t3code-bin`, `t3code-nightly-bin` | `packaging/aur/*` | | none | STRIPPED |
| Telemetry hosts | `T3CODE_POSTHOG_KEY/HOST`; `distinct_id` from hashed machine ids | `AnalyticsService.ts@36d4d711:L64-67` | `posthog`: 13 files (6 in STRIPPED `.repos/`) | removed | F-05 |
| Preserved (never rewritten) | MIT copyright line `Copyright (c) 2026 T3 Tools Inc.`; vendored-code LICENSE files (1.1); commit SHA citations | | | | Q-03 allows these only under `THIRD_PARTY/` and root `NOTICE` |

### 4.1 Files containing `t3.codes` (73; search 2026-10-28)

<<<LIST_T3CODES>>>

### 4.2 `T3CODE_` by area (198 files)

<<<LIST_T3CODE_ENV>>>

### 4.3 Files containing `T3Tools.T3Code` (50)

<<<LIST_AUMID>>>

### 4.4 Files containing `pingdotgg` (scripts 8, apps/desktop 6, apps/server 24)

<<<LIST_PINGDOTGG>>>

### 4.5 Files containing `x-t3` (22)

<<<LIST_XT3>>>

---

## 5. Direct dependencies of KEPT packages (VERIFIED from `package.json` at the pin; licenses from the public npm registry)

<<<S5>>>

---

## 6. Tests per KEPT area, replay fixtures, and tests removed with STRIP (VERIFIED from tree paths)

Test file = path containing `.test.` or `.spec.` (covers `.test.ts(x)`, `.integration.test.ts`, `.browser.test.tsx`, `.test.cjs/.mjs/.py`).

<<<S6>>>

---

## 7. Build and packaging files to modify

<<<S7>>>

---

## 8. Qualification tests for the transplant

IDs `Q-nn` are proposed here and should be attached to F-01..F-16 / Y-00 as their verification column. "det" = deterministic CI check;
"neg" = negative test; "e2e" = needs an installed build. All fixtures are local.

| ID | Check | Type | Pass criterion | Backs |
|---|---|---|---|---|
| Q-01 | **Manifest hash**: sorted list of `path<TAB>blob-sha` for KEEP+MODIFY paths in the Zain tree (before the identity sweep and any seam edit) hashes to the value recorded in `THIRD_PARTY/t3code/IMPORT_MANIFEST.sha256`; the same list for STRIP paths is empty | det | equal; any extra or missing path fails | F-01 |
| Q-02 | **Notice retention**: `THIRD_PARTY/t3code/LICENSE` has blob SHA `55ee675bb1de9e580b69f3dd68684df2a4dffba7`; `apps/web/src/components/files/office/LICENSE.opencode`, `apps/web/src/terminal/ghostty/fonts/LICENSE`, `native/libghostty-vt/LICENSE` present; `scripts/lib/third-party-licenses.test.ts` green; build fails when a collected package lacks notice text | det | pass; deleting a notice fails the build | F-11, GOV-06 |
| Q-03 | **Donor-identifier grep gate**: zero matches of `T3Tools`, `@t3tools`, `t3code`, `T3CODE_`, `t3\.codes`, `T3 Code`, `refs/t3/`, `T3 Tools Inc` (allowed only under `THIRD_PARTY/t3code/` and root `NOTICE`), `pingdotgg`, `com\.t3tools`, `x-t3-`, `t3-code`, `\bt3_` in tracked files | det | 0 outside allow-list | F-03 |
| Q-04 | **STRIP completeness**: no path under any STRIP prefix in 2.2; `grep -r "@clerk\|posthog\|@cursor/sdk\|@muse-code\|BrowserImport\|infra/relay\|apps/mobile"` over sources and `package.json` files returns nothing; `pnpm why` finds none of the stripped packages | det | 0 hits | F-02 |
| Q-05 | **Install, typecheck, lint, kept suites**: `pnpm install --frozen-lockfile`, typecheck, oxlint with the renamed plugin, and the kept unit suites; kept-test count equals section 6 totals (no silently dropped tests) | det | green at the B-03 ratio | F-02, F-16 |
| Q-06 | **Replay fixtures**: all kept provider replay suites (`ClaudeReplayFixtures`, `CodexReplayFixtures`, `OpenCodeReplayFixtures`, `PiReplayFixtures`, `AcpRegistryReplayFixtures`) pass against the kept fixture dirs; no fixture file for Cursor/Fx/Grok/Muse remains | det | green | F-02 |
| Q-07 | **Recovery suites unchanged**: `testkit/OrchestratorReplayRecovery.integration.test.ts`, `OrchestratorReplayRestartBackgroundNote.integration.test.ts`, `ProviderRuntimeRecoveryService{,.regression}.test.ts`, `ProjectionRecovery.test.ts`, `RestartContinuation.test.ts`, `EffectWorker.test.ts`, `BackgroundWorkStop.integration.test.ts` pass before any seam edit | det | green (baseline for C-10/C-20) | F-16, C-10 |
| Q-08 | **No Full access**: `DEFAULT_RUNTIME_MODE` decodes to Supervised; schema decode of `"full-access"` is rejected or coerced; UI has no Full-access option; Claude adapter never emits `bypassPermissions`, Codex never emits `dangerFullAccess` | det + neg | pass | F-07 |
| Q-09 | **Settlement is cosmetic**: merging or closing a linked PR sets "archived", never "done" or "settled"; no completion signal is derived from `thread.auto-settle` | det | pass | F-08 |
| Q-10 | **Protocol mismatch**: a T3 client (header `x-t3-orchestration-protocol: 2` or none) to `/ws` gets HTTP 426; a Zain client passes | det + neg | 426 / 101 | F-09 |
| Q-11 | **Idle egress**: installed build idle for 10 minutes with no user action opens zero outbound connections (no PostHog, Clerk, relay, update beacon) | e2e | empty capture | F-05 |
| Q-12 | **Installer-content gate**: unpacked installer contains no `claude-agent-sdk*`, no `posthog`/`clerk` strings, no donor identifiers (Q-03 regexes), no `.repos`, `apps/mobile`, `native/browser-secret` artefacts | det | 0 hits | F-06, F-11 |
| Q-13 | **Claude optional**: without the SDK the Claude driver reports "not installed" with a consent flow and nothing else breaks; with a user-provided SDK and API key a Claude session completes a turn | e2e | pass | F-06 |
| Q-14 | **Updater refuses donor**: a manifest signed by or served from the upstream feed is rejected; a Zain-signed manifest is accepted | neg | reject / accept | F-04 |
| Q-15 | **Y-00**: no code path reads browser credential stores (no `ChromiumKeys`, `Cookies`, DPAPI/Keychain/libsecret readers); IPC channels for import absent; `CdpRelay` agent lane denies `Storage.getCookies`, `Network.getAllCookies`, `Browser.grantPermissions`; `preview_evaluate` off outside Preview/Test lanes; agent partition is ephemeral | det + neg | pass | Y-00 |
| Q-16 | **Hidden refs**: checkpoint capture creates `refs/zain/checkpoints/...`; no `refs/t3/` ref is ever written; restore works; `GitVcsDriver.test.ts`, `VcsProcess.test.ts` updated and green | det | pass | F-03 |
| Q-17 | **Windows shell**: NSIS (dev-signed) installs, launches, spawns the server child via `ELECTRON_RUN_AS_NODE=1` (`DesktopBackendConfiguration.ts@36d4d711:L522-534`), loads `fff` from `server.asar` (`build-desktop-artifact.ts@36d4d711:L733`); `windows-tests.yml` suite green | e2e | pass | F-11, F-16 |
| Q-18 | **MCP identity**: server name `zain`, tools `zain_*`, Codex/Claude injection (`-c mcp_servers.zain.url`, `allowedTools: ["mcp__zain__*"]`) works; outside-agent OAuth pairing still works | det + e2e | pass | F-03, C-12 |
| Q-19 | **Dependency licence audit**: every direct dependency of every KEPT `package.json` has an SPDX licence (section 5); proprietary and copyleft rows resolved before first public build | det | 0 UNKNOWN, 0 unresolved flags | F-11, GOV-07 |
| Q-20 | **Budget**: B1-B3 (startup, memory, size) <= P1 T3 baseline + 10%; bundle shrinks by at least the stripped mobile/relay share | bench | within budget | F-15 |
| Q-21 | **Rust**: `cargo test` for `native/resource-monitor`; renamed Core binary `zain-core` passes the existing 19k-line Rust suite; one `zain` binary on PATH | det | green | F-10 |
| Q-22 | **Seam smoke (G3 spike)**: ACP `fs/write` (S3) and a Codex approval (S2) through Core produce ledger receipts; `kill -9` between dispatch and report yields `EFFECT_OUTCOME_UNKNOWN`; recovery does not auto-continue (S4b) | det | go/no-go | C-01, C-10 |
| Q-23 | **Project-file rename**: `t3.json` reader accepts only the Zain project file under `.zainide/`; `.zain/` is never created | det + neg | pass | F-03, N-03 |
| Q-24 | **Pin integrity**: the importer script refuses to run unless the tree SHA is `4975e3bd50c19c37f4aeeaf29280b80fc3d56019` and commit is `36d4d711b79c73eb33131944f73ea4a8c6156484` | det | pass | F-01 |

---

## 9. Unknowns and follow-ups

- Which `apps/server/src/cloud/*` files beyond the six listed in 3.8 are required by service mode: **UNKNOWN** until the F-02 import-graph check (the six were chosen by name; `pinnedRuntime.ts`, `ManagedEndpointRuntime.ts`, `config.ts`, `http.ts` are STRIPPED here but must be confirmed unimported).
- STRIPPED-by-assumption trees whose importers were not traced: `apps/server/src/device/*` + `apps/server/schema/*` (mobile device tooling), `apps/server/src/scheduledTasks/RelayDeliveryProof.ts`, `packages/client-runtime` consumers of `relay/` (non-test consumers: UNKNOWN count).
- Line numbers for caller-removal rows (PostHog, Clerk, SDK imports, BrowserImport) were not extracted (UNKNOWN); only paths from code search.
- OpenCode and Pi permission-rule files (S2) not identified.
- Default `~/.t3` definition site and `t3Home` origin: UNKNOWN.
- Code-search counts are HEAD-based and file-level (section 4 caveats).
- Registry licence queries that failed are marked UNKNOWN in section 5.
