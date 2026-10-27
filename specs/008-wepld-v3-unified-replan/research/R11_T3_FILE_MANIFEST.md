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

## 0. Completeness statement (read first)

**VERIFIED (read from the pinned tree, blobs, registry):** pin and tree SHAs; all 28,763 blobs classified exactly once with exact counts and sizes (section 2); existence of every MODIFY path; seam line ranges in section 3 (re-read against raw blobs); notice/licence blob SHAs; direct dependencies and registry licences of KEPT `package.json` files (section 5); test and fixture counts from paths (section 6).

**UNKNOWN or UNVERIFIED (not established):** import-graph correctness of STRIP carve-outs (cloud/, device/, relay consumers); line numbers of caller-removal edits (PostHog, Clerk, SDK imports, BrowserImport callers); OpenCode/Pi permission seams; the `~/.t3` definition site; transitive npm/crate licences; code-search counts in section 4 are HEAD-based, file-level and indicative only. Rows marked UNVERIFIED were found by filename or search hit.

**Constraints honoured:** nothing cloned or downloaded; no file written except this manifest; GitHub API use stayed far below the 1,500-request budget (one recursive tree call per generator run, about 35 contents calls, a few commit calls, code search); licences came from read-only registry GETs.

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
| Tree listing | `git/trees/<sha>?recursive=1`: `truncated=false`; 32844 entries = 28763 blobs + 4079 trees + 2 gitlinks | gh |
| Commit | 2026-10-27T14:17:36Z, "fix(server): bound hung delegated stop effects so later runs can start (#25675)" | gh |
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

### 2.1 Every top-level directory and workspace

| Path | Disposition | Files | Approx size | K / M / S | Reason | Zain destination |
|---|---|---:|---:|---|---|---|
| `.agents` | **STRIP** | 7 | 25,651 B | 0 / 0 / 7 | Upstream agent skills | - |
| `.claude` | **STRIP** | 1 | 17 B | 0 / 0 / 1 | Upstream | - |
| `.cursor` | **STRIP** | 2 | 4,904 B | 0 / 0 / 2 | Upstream | - |
| `.devcontainer` | **STRIP** | 3 | 5,397 B | 0 / 0 / 3 | Upstream devcontainer | - |
| `.github/workflows` | **MODIFY** | 22 | 236,280 B | 0 / 4 / 18 | 22 workflows: 4 kept (ci, windows-tests, release, release-desktop), 18 stripped | `.github/workflows/` (4 kept) |
| `.github (non-workflow)` | **MODIFY** | 22 | 85,647 B | 7 / 0 / 15 | actions/ kept; issue templates, triage, scripts mostly stripped | `.github/{actions,scripts}` |
| `.macroscope` | **STRIP** | 4 | 19,571 B | 0 / 0 / 4 | Upstream review-bot config | - |
| `.repos` | **STRIP** | 21,833 | 156,828,976 B | 0 / 0 / 21,833 | Vendored reference repos | - |
| `.vite-hooks` | **KEEP** | 1 | 10 B | 1 / 0 / 0 | pre-commit hook (10 B) | `.vite-hooks/` |
| `.vscode` | **KEEP** | 2 | 539 B | 2 / 0 / 0 | Editor settings | `.vscode/` |
| `apps/desktop` | **MODIFY** | 282 | 3,164,214 B | 246 / 14 / 22 | Electron 44.9.3 shell, updater, WSL/SSH, preview/browser host; carve-outs: Clerk bridge, BrowserImport | `apps/desktop` |
| `apps/marketing` | **STRIP** | 103 | 3,137,573 B | 0 / 0 / 103 | Astro marketing site | - |
| `apps/mobile` | **STRIP** | 1,531 | 75,286,594 B | 0 / 0 / 1,531 | Expo 58 / RN 0.88 client | - |
| `apps/server` | **MODIFY** | 1,413 | 25,551,146 B | 1,137 / 57 / 219 | Orchestration-v2, providers, git/VCS, terminals, MCP, auth, WS RPC, CLI; seam host (S1-S8). Carve-outs: telemetry, cloud/relay, device, V1 importer, Antigravity, 4 stripped provider adapters | `apps/server` (package `t3` -> Zain Server, bin `zain`) |
| `apps/web` | **MODIFY** | 1,717 | 27,536,735 B | 1,664 / 10 / 43 | React 19 SPA = desktop renderer; carve-outs: Clerk/Connect UI, browser-import wizard, V1 toast | `apps/web` |
| `assets/dev` | **STRIP** | 12 | 8,781,218 B | 0 / 0 / 12 | T3 dev brand assets | - |
| `assets/nightly` | **STRIP** | 13 | 5,679,494 B | 0 / 0 / 13 | T3 nightly brand assets | - |
| `assets/prod` | **STRIP** | 11 | 1,746,204 B | 0 / 0 / 11 | T3 prod brand assets | - |
| `assets (root)` | **STRIP** | 1 | 3,915 B | 0 / 0 / 1 | assets README | - |
| `docs/internals` | **MODIFY** | 31 | 182,822 B | 30 / 0 / 1 | Architecture notes; kept as vendor reference (donor identity left inside vendor docs) | `docs/vendor/t3code/internals/` (reference) |
| `docs/operations` | **STRIP** | 9 | 132,100 B | 0 / 0 / 9 | T3 release/relay/mobile ops docs | - |
| `docs/orchestration-v2` | **KEEP** | 9 | 122,648 B | 9 / 0 / 0 | Design docs for the kept orchestrator | `docs/vendor/t3code/orchestration-v2/` (reference) |
| `docs/user` | **STRIP** | 41 | 251,582 B | 0 / 0 / 41 | T3 end-user docs | - |
| `docs (root)` | **KEEP** | 1 | 3,125 B | 1 / 0 / 0 | docs/ top-level file | `docs (root)` |
| `evals` | **STRIP** | 16 | 447,896 B | 0 / 0 / 16 | Evals | - |
| `infra/relay` | **STRIP** | 119 | 1,451,686 B | 0 / 0 / 119 | T3 Connect relay | - |
| `infra/task-cache` | **STRIP** | 63 | 244,374 B | 0 / 0 / 63 | CI test cache | - |
| `native/browser-secret` | **STRIP** | 2 | 4,657 B | 0 / 0 / 2 | C libsecret cookie-key reader; Y-00 | - |
| `native/hyprland-snap-shot` | **KEEP** | 10 | 92,149 B | 10 / 0 / 0 | Linux (Hyprland) screenshot helper; not in F-02 STRIP list, deferred | `native/hyprland-snap-shot` (deferred, STRIP candidate) |
| `native/kde-snap-shot` | **KEEP** | 14 | 77,549 B | 14 / 0 / 0 | Linux (KDE) screenshot helper; not in F-02 STRIP list, deferred | `native/kde-snap-shot` (deferred, STRIP candidate) |
| `native/libghostty-vt` | **KEEP** | 32 | 298,479 B | 32 / 0 / 0 | Ghostty VT C-ABI headers + pin for terminal renderer (MIT, LICENSE kept) | `native/libghostty-vt` |
| `native/resource-monitor` | **KEEP** | 3 | 54,826 B | 3 / 0 / 0 | Existing Rust stdio NDJSON sidecar (process telemetry, PROTOCOL_VERSION 3); pattern for CoreBridge (C-06) | `native/resource-monitor` (binary renamed; precedent for Core sidecar) |
| `oxlint-plugin-t3code` | **KEEP** | 65 | 230,629 B | 65 / 0 / 0 | Custom oxlint rules (60 rule files) enforcing Effect conventions; renamed | `oxlint-plugin-zain` |
| `packages/client-runtime` | **MODIFY** | 370 | 3,168,308 B | 359 / 0 / 11 | Shared connection supervisor/state for web; carve-out: relay/ | `packages/client-runtime` |
| `packages/contracts` | **MODIFY** | 103 | 1,073,145 B | 93 / 6 / 4 | Effect Schema contracts (RPC, orchestration-v2, settings); carve-outs: relay, browserImport | `packages/contracts` (scope `@thehalfmoon/*`) |
| `packages/effect-acp` | **KEEP** | 23 | 1,227,557 B | 23 / 0 / 0 | Typed ACP client/agent (mostly generated) | `packages/effect-acp` |
| `packages/effect-codex-app-server` | **KEEP** | 21 | 2,568,809 B | 21 / 0 / 0 | Typed JSON-RPC client for `codex app-server` (mostly generated) | `packages/effect-codex-app-server` |
| `packages/provider-acp` | **MODIFY** | 18 | 675,398 B | 15 / 3 / 0 | Generic ACP adapter incl. client fs/terminal policy (S2/S3 host) | `packages/provider-acp` |
| `packages/provider-acp-registry` | **KEEP** | 24 | 308,746 B | 24 / 0 / 0 | ACP registry agents (claudeAcp, copilotAcp, ...) | `packages/provider-acp-registry` |
| `packages/provider-core` | **KEEP** | 67 | 415,482 B | 67 / 0 / 0 | `ProviderAdapterV2` contract, driver/instance model | `packages/provider-core` |
| `packages/provider-cursor` | **STRIP** | 39 | 391,910 B | 0 / 0 / 39 | Unused provider; `@cursor/sdk` dependency | - |
| `packages/provider-fx` | **STRIP** | 14 | 66,573 B | 0 / 0 / 14 | Unused provider | - |
| `packages/provider-grok` | **STRIP** | 21 | 219,195 B | 0 / 0 / 21 | Unused provider | - |
| `packages/provider-muse` | **STRIP** | 28 | 298,789 B | 0 / 0 / 28 | Unused provider; `@muse-code/sdk` | - |
| `packages/provider-opencode` | **KEEP** | 38 | 731,856 B | 38 / 0 / 0 | OpenCode driver/adapter (kept family, 02 sec.2) | `packages/provider-opencode` |
| `packages/provider-pi` | **KEEP** | 23 | 439,902 B | 23 / 0 / 0 | Pi driver/adapter (kept family, 02 sec.2) | `packages/provider-pi` |
| `packages/provider-testing` | **KEEP** | 7 | 19,289 B | 7 / 0 / 0 | Provider test helpers | `packages/provider-testing` |
| `packages/shared` | **MODIFY** | 219 | 1,502,010 B | 204 / 1 / 14 | Utilities (nodeSqliteClient, PtyAdapter, DrainableWorker); carve-out: relay*/connectAuth | `packages/shared` |
| `packages/source-control-azure-devops` | **KEEP** | 19 | 201,736 B | 19 / 0 / 0 | Azure DevOps forge (candidate to trim later) | `packages/source-control-azure-devops` |
| `packages/source-control-bitbucket` | **KEEP** | 17 | 194,033 B | 17 / 0 / 0 | Bitbucket forge (candidate to trim later) | `packages/source-control-bitbucket` |
| `packages/source-control-core` | **KEEP** | 18 | 131,192 B | 18 / 0 / 0 | Forge abstraction (kept; forge packages not in F-02 STRIP list) | `packages/source-control-core` |
| `packages/source-control-definitions` | **KEEP** | 3 | 2,277 B | 3 / 0 / 0 | Forge definitions | `packages/source-control-definitions` |
| `packages/source-control-forgejo` | **KEEP** | 17 | 178,039 B | 17 / 0 / 0 | Forgejo forge (candidate to trim later) | `packages/source-control-forgejo` |
| `packages/source-control-gitcafe` | **KEEP** | 17 | 210,450 B | 17 / 0 / 0 | GitCafe forge (candidate to trim later) | `packages/source-control-gitcafe` |
| `packages/source-control-github` | **KEEP** | 60 | 2,486,058 B | 60 / 0 / 0 | GitHub forge (PRs, review) | `packages/source-control-github` |
| `packages/source-control-gitlab` | **KEEP** | 23 | 252,037 B | 23 / 0 / 0 | GitLab forge (candidate to trim later) | `packages/source-control-gitlab` |
| `packages/source-control-testing` | **KEEP** | 4 | 13,528 B | 4 / 0 / 0 | Forge test helpers | `packages/source-control-testing` |
| `packages/ssh` | **KEEP** | 11 | 126,499 B | 11 / 0 / 0 | SSH remote environment transport | `packages/ssh` |
| `packages/tailscale` | **KEEP** | 5 | 26,301 B | 5 / 0 / 0 | Tailscale remote transport | `packages/tailscale` |
| `packaging` | **STRIP** | 5 | 9,370 B | 0 / 0 / 5 | AUR PKGBUILDs | - |
| `patches` | **MODIFY** | 33 | 406,365 B | 10 / 0 / 23 | 33 pnpm patches; kept = effect/vitest, fff-node, @pierre/diffs, @legendapp/list, app-builder-lib, dbus-next, markdown, node-pty | `patches/` |
| `scripts` | **MODIFY** | 101 | 1,862,956 B | 57 / 8 / 36 | Build/release/dev scripts: kept = desktop artifact build, release smoke, install, notices, dev-runner; carve-outs: mobile/Discord/seeds/.repos sync | `scripts/` |
| `(root files)` | **MODIFY** | 20 | 1,041,566 B | 5 / 8 / 7 | 20 root files: 7 kept/modified config, rest stripped | repo root (see 2.3 and section 7) |
| **TOTAL** | | **28,763** | **331,937,983 B** | **4,361 / 111 / 24,291** | KEEP 64,479,194 B, MODIFY 4,730,453 B, STRIP 262,728,336 B | |

Excluding `.repos/` the tree has **6,930** first-party files (175,109,007 B); after STRIP the imported set is **4,472** files (69,209,647 B) = KEEP 4,361 + MODIFY 111.

### 2.2 STRIP rules (carve-outs) with counts

Rules are applied in order after the MODIFY set (2.3); a file whose path is a MODIFY path is never stripped. Counts are exact over the pinned tree.

| STRIP rule | Files | Approx size | Test files | Reason |
|---|---:|---:|---:|---|
| `.repos/` | 21,833 | 156,828,976 B | 3,778 | Vendored reference repos (effect-smol, alchemy-effect via subtree); not shipped (R02 sec.9); 2 gitlinks |
| `apps/mobile` | 1,531 | 75,286,594 B | 245 | Expo/React-Native client; STRIP list in 08 P2 |
| `apps/marketing` | 103 | 3,137,573 B | 0 | Astro marketing site; STRIP list in 08 P2 |
| `infra/relay` | 119 | 1,451,686 B | 32 | T3 Connect relay (Cloudflare Workers/Durable Objects); STRIP |
| `infra/task-cache` | 63 | 244,374 B | 11 | CI test cache on Cloudflare incl. vendored vite-plus remote cache; Zain CI differs |
| `native/browser-secret` | 2 | 4,657 B | 0 | Reads Chromium cookie key (libsecret) for browser import; Y-00 |
| `packages/provider-cursor` | 39 | 391,910 B | 14 | Unused provider (08 P2 STRIP) |
| `packages/provider-fx` | 14 | 66,573 B | 3 | Unused provider (08 P2 STRIP) |
| `packages/provider-grok` | 21 | 219,195 B | 5 | Unused provider (08 P2 STRIP) |
| `packages/provider-muse` | 28 | 298,789 B | 10 | Unused provider (08 P2 STRIP; muse SDK proprietary-risk) |
| `browser-import` | 24 | 216,436 B | 11 | Real-browser cookie import (DPAPI/Keychain/libsecret); Y-00, R17 sec.5.1 |
| `v1-importer` | 6 | 101,039 B | 2 | V1 thread importer; no legacy data in Zain (08 P2 STRIP) |
| `antigravity` | 30 | 481,658 B | 13 | Antigravity provider (02 sec.2 STRIP) |
| `stripped-provider-adapters/testkits` | 56 | 1,842,124 B | 6 | Adapters/testkits/recorders of stripped providers |
| `telemetry-posthog` | 9 | 69,901 B | 4 | PostHog analytics (AnalyticsService); F-05 |
| `connect-clerk-relay` | 110 | 941,336 B | 44 | T3 Connect / Clerk / relay client side (six service/update files under cloud/ are carved back to MODIFY) |
| `mobile-device-tooling` | 37 | 728,886 B | 15 | Expo/EAS and device-hub tooling for the mobile client (UNVERIFIED importers) |
| `scripts-mobile-and-misc` | 36 | 1,197,650 B | 8 | Mobile helpers, Discord notifier, issue seeds, reference-repo sync (.repos), task-cache runner |
| `github-non-core` | 33 | 176,797 B | 4 | Upstream project governance, mobile, relay, AUR, Vercel, macOS preview workflows |
| `assets` | 37 | 16,210,831 B | 0 | T3 brand art (name/logo, Icon Composer projects); replaced by Zain assets |
| `docs-user-ops` | 50 | 383,682 B | 0 | Upstream user/ops docs (T3 Connect, mobile, analytics, T3 install); Zain writes its own |
| `evals` | 16 | 447,896 B | 1 | MCP-tool-use and thread-title evals tied to T3 names/providers; recreate for Zain |
| `upstream-agent-and-ci-config` | 29 | 105,786 B | 0 | Upstream agent instructions (data, not instructions), review-bot/CI config, README/CONTRIBUTING, AUR |
| `patches-mobile-clerk-muse` | 23 | 196,056 B | 0 | pnpm patches for stripped deps (Expo/RN, Clerk, Muse, alchemy) |
| `fixture-dirs-of-stripped-providers` | 42 | 1,697,931 B | 0 | Replay fixture dirs whose only provider transcripts are Cursor/Fx/Grok/Muse |

Regexes (VERIFIED, applied to repo-relative paths):

- `.repos/`: `^\.repos/`
- `apps/mobile`: `^apps/mobile/`
- `apps/marketing`: `^apps/marketing/`
- `infra/relay`: `^infra/relay/`
- `infra/task-cache`: `^infra/task-cache/`
- `native/browser-secret`: `^native/browser-secret/`
- `packages/provider-cursor`: `^packages/provider-cursor/`
- `packages/provider-fx`: `^packages/provider-fx/`
- `packages/provider-grok`: `^packages/provider-grok/`
- `packages/provider-muse`: `^packages/provider-muse/`
- `browser-import`: `^(apps/desktop/src/preview/BrowserImport/|apps/desktop/scripts/(build-browser-secret|browser-secret-native)|apps/web/src/components/settings/[bB]rowserImportWizard|packages/contracts/src/browserImport)`
- `v1-importer`: `^(apps/server/src/orchestration-v2/legacy/|apps/server/src/persistence/Migrations/OrchestrationV2/LegacyV1ImportState|apps/web/src/components/LegacyThreadMigrationToast|docs/internals/legacy-orchestration-migration)`
- `antigravity`: `^apps/server/src/.*[aA]ntigravity`
- `stripped-provider-adapters/testkits`: `^(apps/server/src/orchestration-v2/Adapters/(Cursor|Fx|Grok|Muse)AdapterV2|apps/server/src/orchestration-v2/testkit/(Cursor|Fx|Grok|Muse)ReplayFixtures|apps/server/scripts/record-(cursor|muse)|apps/server/scripts/.*(grok|antigravity))`
- `telemetry-posthog`: `^apps/server/src/telemetry/`
- `connect-clerk-relay`: `^(apps/server/src/relay/|apps/server/src/cloud/|apps/web/src/cloud/|apps/web/src/components/(clerk|cloud)/|apps/desktop/src/app/DesktopClerk|packages/client-runtime/src/relay/|packages/shared/src/(relay[A-Za-z]*|connectAuth)\.|packages/contracts/src/relay(Client)?\.|apps/server/src/cli/connect\.|apps/server/src/scheduledTasks/RelayDeliveryProof)`
- `mobile-device-tooling`: `^(apps/server/src/device/|apps/server/schema/)`
- `scripts-mobile-and-misc`: `^scripts/(mobile-|seed-issue|notify-discord|export-android|convert-device|legend-list|sync-reference-repos|fixtures/|test-cached)`
- `github-non-core`: `^\.github/(ISSUE_TEMPLATE|triage|SECURITY|TRIAGE_EXEMPTIONS|VOUCHED|pull_request_template|scripts/(mirror-play-apk|relay-state-output|stage-preview-bundle|thread-transfer-report|vercel-deployment-output))|^\.github/workflows/(agent-context-budget|deploy-relay|desktop-macos-preview|desktop-macos-preview-publish|issue-labels|mobile-|pr-size|pr-vouch|publish-aur|relay-|stale-needs|thread-transfer|web-preview)`
- `assets`: `^assets/`
- `docs-user-ops`: `^docs/(user|operations)/`
- `evals`: `^evals/`
- `upstream-agent-and-ci-config`: `^(\.agents/|\.cursor/|\.claude/|\.macroscope/|\.devcontainer/|packaging/aur/|\.coderabbit\.config\.ts$|\.vercelignore$|\.task-cache\.json$|AGENTS\.md$|CLAUDE\.md$|CONTRIBUTING\.md$|README\.md$)`
- `patches-mobile-clerk-muse`: `^patches/(@clerk|@expo|@muse|@react-native|@react-navigation|alchemy|expo-|react-native)`
- `fixture-dirs-of-stripped-providers`: fixture dirs under `apps/server/src/orchestration-v2/testkit/fixtures/` whose provider transcripts belong only to cursor/fx/grok/muse: `fx_early_stop`, `fx_subagent`, `grok_auto_blocked_command`, `grok_background_bash`, `grok_background_bash_fast_wake`, `grok_background_subagent`, `grok_monitor`, `grok_prompt_error`, `grok_subagent_lineage`, `muse_permission`, `muse_subagent_approval`, `muse_subagent_interrupt`, `muse_workflow`, `skill_invocation`
- stripped-provider fixture files inside kept dirs: `<dir>/(cursor|fx|grok|muse)_(transcript|output).*`

Kept patches (`patches/`): everything not matched by the STRIP regex. `@legendapp/list` is a dependency of `apps/web` (`apps/web/package.json@36d4d711:L31`), so its 128,731 B patch is KEPT.

### 2.3 MODIFY files per tag (111 files; exact paths in section 3 and section 7)

| Tag | Files | Approx size |
|---|---:|---:|
| S1 | 9 | 1,033,044 B |
| S2 | 2 | 373,721 B |
| S3 | 2 | 24,656 B |
| S4/S4b | 3 | 97,253 B |
| S5 | 4 | 92,798 B |
| S6 | 8 | 325,836 B |
| S7 | 6 | 356,567 B |
| S8 | 2 | 122,350 B |
| SETTLE | 1 | 28,069 B |
| UPDATER | 9 | 254,730 B |
| POSTHOG | 7 | 343,810 B |
| CLERK | 10 | 123,538 B |
| CLERK(service kept) | 4 | 57,781 B |
| CLAUDE-SDK | 9 | 79,905 B |
| BROWSER-IMPORT | 8 | 158,603 B |
| CDP/Y-00 | 4 | 39,508 B |
| PROTOCOL | 1 | 9,009 B |
| IDENTITY | 22 | 1,209,275 B |

(A file can carry several tags - e.g. `ClaudeAdapterV2.ts` is S1+S2+SDK - and is counted once in the K/M/S totals above. IDENTITY lists the identity-critical files of section 4; the many other files touched only by the mechanical sweep stay KEEP.)

### 2.4 Rows needing a decision before F-02 (PROPOSED defaults shown)

- `native/hyprland-snap-shot`, `native/kde-snap-shot`, `apps/desktop/src/snapShot/**` (41 files), `apps/desktop/gnome-extension/**`: Linux-only screenshot helpers. NOT in the F-02 STRIP list, so kept; recommend STRIP at F-02 if the P2 target stays Windows-first.
- `packages/source-control-{gitlab,bitbucket,azure-devops,forgejo,gitcafe}`: not in the F-02 STRIP list, so kept; candidates to trim later (library code only).
- `docs/internals/**`, `docs/orchestration-v2/**`: kept as vendor reference under `docs/vendor/t3code/`; they still contain donor identifiers, so the Q-03 grep gate must allow-list `docs/vendor/t3code/`.

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

Generator check on 2026-10-28 against the pinned tree: **111** distinct MODIFY paths registered, **0 missing** (all exist).

Existing sibling test files of MODIFY paths (tests that must be updated with the edit):

| MODIFY file | Sibling tests@36d4d711 |
|---|---|
| `apps/desktop/src/app/DesktopEnvironment.ts` | `DesktopEnvironment.test.ts` |
| `apps/desktop/src/electron/ElectronProtocol.ts` | `ElectronProtocol.test.ts` |
| `apps/desktop/src/ipc/methods/preview.ts` | `preview.test.ts` |
| `apps/desktop/src/ipc/methods/window.ts` | `window.test.ts` |
| `apps/desktop/src/preview/BrowserSession.ts` | `BrowserSession.test.ts` |
| `apps/desktop/src/preview/CdpRelay.ts` | `CdpRelay.test.ts` |
| `apps/desktop/src/updates/DesktopUpdates.ts` | `DesktopUpdates.test.ts` |
| `apps/server/src/auth/McpOAuth.ts` | `McpOAuth.test.ts` |
| `apps/server/src/checkpointing/CheckpointStore.ts` | `CheckpointStore.test.ts` |
| `apps/server/src/cli/app.ts` | `app.test.ts` |
| `apps/server/src/cli/service.ts` | `service.test.ts` |
| `apps/server/src/cli/update.ts` | `update.test.ts` |
| `apps/server/src/cloud/bootService.ts` | `bootService.test.ts` |
| `apps/server/src/cloud/selfUpdate.ts` | `selfUpdate.test.ts` |
| `apps/server/src/cloud/serviceLauncherClient.ts` | `serviceLauncherClient.test.ts` |
| `apps/server/src/cloud/servicePreflight.ts` | `servicePreflight.test.ts` |
| `apps/server/src/desktopUpdate/DesktopAppUpdate.ts` | `DesktopAppUpdate.test.ts` |
| `apps/server/src/git/GitManager.ts` | `GitManager.test.ts` |
| `apps/server/src/git/GitWorkflowService.ts` | `GitWorkflowService.test.ts` |
| `apps/server/src/guest/GuestShareService.ts` | `GuestShareService.test.ts` |
| `apps/server/src/mcp/McpHttpServer.ts` | `McpHttpServer.test.ts` |
| `apps/server/src/mcp/McpSessionRegistry.ts` | `McpSessionRegistry.test.ts` |
| `apps/server/src/mcp/McpToolAccess.ts` | `McpToolAccess.test.ts` |
| `apps/server/src/mcp/OrchestratorMcpService.ts` | `OrchestratorMcpService.test.ts` |
| `apps/server/src/mcp/WorktreeMcpService.ts` | `WorktreeMcpService.test.ts` |
| `apps/server/src/mcp/threadAccess.ts` | `threadAccess.test.ts` |
| `apps/server/src/mcp/toolkits/preview/handlers.ts` | `handlers.test.ts` |
| `apps/server/src/mcp/toolkits/preview/tools.ts` | `tools.test.ts` |
| `apps/server/src/orchestration-v2/Adapters/ClaudeAdapterV2.ts` | `ClaudeAdapterV2.test.ts` |
| `apps/server/src/orchestration-v2/Adapters/CodexAdapterV2.ts` | `CodexAdapterV2.test.ts` |
| `apps/server/src/orchestration-v2/DispatchModeLimit.ts` | `DispatchModeLimit.test.ts` |
| `apps/server/src/orchestration-v2/EffectWorker.ts` | `EffectWorker.test.ts` |
| `apps/server/src/orchestration-v2/ProviderEventIngestor.ts` | `ProviderEventIngestor.test.ts` |
| `apps/server/src/orchestration-v2/ProviderRuntimeRecoveryService.ts` | `ProviderRuntimeRecoveryService.regression.test.ts`, `ProviderRuntimeRecoveryService.test.ts` |
| `apps/server/src/orchestration-v2/ProviderSessionManager.ts` | `ProviderSessionManager.test.ts` |
| `apps/server/src/orchestration-v2/RuntimePolicy.ts` | `RuntimePolicy.test.ts` |
| `apps/server/src/orchestration-v2/RuntimeRequestService.ts` | `RuntimeRequestService.test.ts` |
| `apps/server/src/orchestration-v2/ThreadSettlementService.ts` | `ThreadSettlementService.test.ts` |
| `apps/server/src/persistence/DatabaseStorage.ts` | `DatabaseStorage.test.ts` |
| `apps/server/src/persistence/OrchestrationEventStore.ts` | `OrchestrationEventStore.test.ts` |
| `apps/server/src/provider/CodexChatGptAuth.ts` | `CodexChatGptAuth.test.ts` |
| `apps/server/src/provider/Drivers/ClaudeExecutable.ts` | `ClaudeExecutable.test.ts` |
| `apps/server/src/provider/claudeUsageLimits.ts` | `claudeUsageLimits.test.ts` |
| `apps/server/src/serverRuntimeStartup.ts` | `serverRuntimeStartup.test.ts` |
| `apps/server/src/terminal/Manager.ts` | `Manager.test.ts` |
| `apps/server/src/terminal/NodePtyAdapter.ts` | `NodePtyAdapter.test.ts` |
| `apps/server/src/vcs/GitVcsDriver.ts` | `GitVcsDriver.test.ts` |
| `apps/server/src/vcs/GitVcsDriverCore.ts` | `GitVcsDriverCore.test.ts` |
| `apps/server/src/ws.ts` | `ws.test.ts` |
| `apps/web/src/composerDraftStore.ts` | `composerDraftStore.test.ts` |
| `packages/contracts/src/environment.ts` | `environment.test.ts` |
| `packages/contracts/src/settings.ts` | `settings.test.ts` |
| `packages/provider-acp/src/server/clientPolicy.ts` | `clientPolicy.test.ts` |
| `packages/provider-acp/src/server/clientTerminals.ts` | `clientTerminals.test.ts` |
| `packages/shared/src/t3ProjectFile.ts` | `t3ProjectFile.test.ts` |
| `scripts/build-desktop-artifact.ts` | `build-desktop-artifact.test.ts` |
| `scripts/dev-runner.ts` | `dev-runner.test.ts` |
| `scripts/lib/cli-external-packages.ts` | `cli-external-packages.test.ts` |
| `scripts/merge-update-manifests.ts` | `merge-update-manifests.test.ts` |

59 of 111 MODIFY paths have a sibling test file.

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

72 files:

```text
.env.example
.github/SECURITY.md
.github/triage/PLAYBOOK.md
.github/workflows/release.yml
AGENTS.md
README.md
apps/desktop/gnome-extension/bundle.json
apps/desktop/gnome-extension/metadata.json
apps/desktop/resources/linux/com.t3tools.t3code.metainfo.xml
apps/desktop/src/app/CodexAuthCallback.test.ts
apps/desktop/src/app/DesktopClerk.test.ts
apps/desktop/src/electron/ElectronProtocol.test.ts
apps/marketing/astro.config.mjs
apps/marketing/src/pages/95.astro
apps/marketing/src/pages/download.astro
apps/marketing/src/pages/privacy-policy.astro
apps/marketing/src/pages/security-policy.astro
apps/marketing/src/pages/terms-of-service.astro
apps/marketing/vercel.ts
apps/mobile/app.config.ts
apps/mobile/src/features/connection/pairing.test.ts
apps/mobile/src/features/settings/lib/legal-document-url.ts
apps/server/scripts/acp-mock-agent.ts
apps/server/src/cli/triagePrompt.ts
apps/server/src/cloud/publicConfig.test.ts
apps/server/src/cloud/servicePreflight.test.ts
apps/server/src/cloud/servicePreflight.ts
apps/server/src/http.test.ts
apps/server/src/orchestration-v2/Adapters/AcpAdapterV2.test.ts
apps/server/src/project/ManagedProjectFolders.ts
apps/server/src/provider/CodexAuthCallback.test.ts
apps/server/src/telemetry/AnalyticsService.ts
apps/web/src/branding.ts
apps/web/src/cloud/connectCliAuth.test.ts
apps/web/src/components/clerk/electronPasskeys.test.ts
apps/web/src/components/settings/pairingUrls.test.ts
apps/web/src/hostedPairing.test.ts
apps/web/src/legalLinks.ts
apps/web/src/lib/bootError.ts
apps/web/src/terminal/ghostty/core.test.ts
apps/web/src/terminal/ghostty/surface.test.ts
apps/web/vercel.ts
docs/internals/linux-snap-shot.md
docs/internals/product-analytics.md
docs/operations/relay-observability.md
docs/operations/release.md
docs/user/appearance.md
docs/user/background-service.md
docs/user/default-browser.md
docs/user/faq.md
docs/user/install.md
docs/user/prompt-links.md
docs/user/providers-acp.md
docs/user/telemetry.md
docs/user/welcome-wizard.md
infra/relay/src/http/Api.test.ts
infra/relay/src/monitoring.ts
packages/contracts/src/t3ProjectFile.ts
packages/shared/src/codexAuthHandoff.test.ts
packages/shared/src/connectAuth.test.ts
packages/shared/src/connectAuth.ts
packages/shared/src/promptLinks.test.ts
packages/shared/src/providerAuthReturnUrl.ts
packages/shared/src/relayAuth.test.ts
packages/shared/src/remote.test.ts
packages/shared/src/t3ProjectFile.test.ts
packages/shared/src/threadLinks.test.ts
packages/source-control-github/src/server/githubStackRebase.ts
scripts/build-desktop-artifact.ts
scripts/install.ps1
scripts/install.sh
t3.json
```

### 4.2 `T3CODE_` by area (198 files)

99 files; grouped by first three path segments (count):

```text
.cursor/rules/cursor-cloud.mdc  (1)
.env.example  (1)
AGENTS.md  (1)
apps/desktop/scripts  (2)
apps/desktop/src  (12)
apps/desktop/vite.config.ts  (1)
apps/marketing/src  (1)
apps/mobile/README.md  (1)
apps/mobile/app.config.ts  (1)
apps/mobile/eas.json  (1)
apps/mobile/fingerprint.config.js  (1)
apps/mobile/metro.config.js  (1)
apps/mobile/src  (1)
apps/server/scripts  (1)
apps/server/src  (24)
apps/server/vite.config.ts  (1)
apps/web/src  (4)
apps/web/vercel.ts  (1)
apps/web/vite.config.ts  (1)
docs/internals/devcontainer.md  (1)
docs/internals/environment-auth.md  (1)
docs/internals/product-analytics.md  (1)
docs/internals/t3-connect.md  (1)
docs/operations/android-notifications.md  (1)
docs/operations/connect-setup.md  (1)
docs/operations/development.md  (1)
docs/operations/observability.md  (1)
docs/operations/relay-observability.md  (1)
docs/operations/release.md  (1)
docs/user/background-service.md  (1)
docs/user/faq.md  (1)
docs/user/install.md  (1)
docs/user/portable-handoffs.md  (1)
docs/user/source-control.md  (1)
docs/user/t3-connect-troubleshooting.md  (1)
docs/user/telemetry.md  (1)
infra/relay/README.md  (1)
infra/relay/src  (1)
packages/provider-core/src  (1)
packages/shared/src  (7)
packages/ssh/src  (1)
scripts/build-cli-archive.ts  (1)
scripts/build-desktop-artifact.ts  (1)
scripts/dev-runner.ts  (1)
scripts/install.ps1  (1)
scripts/install.sh  (1)
scripts/lib/public-config.ts  (1)
scripts/lib/windows-jsign.ts  (1)
scripts/mobile-native-client.ts  (1)
scripts/mock-update-server.ts  (1)
scripts/npm-launcher/t3.mjs  (1)
scripts/render-metrics.ts  (1)
scripts/setup-worktree.ts  (1)
scripts/smoke-cli-archive.ts  (1)
scripts/smoke-desktop-app.ts  (1)
```

### 4.3 Files containing `T3Tools.T3Code` (50)

50 files:

```text
.agents/skills/test-t3-mobile/SKILL.md
.agents/skills/test-t3-mobile/scripts/pair-client.sh
.github/workflows/mobile-android-apk.yml
.github/workflows/release.yml
README.md
apps/desktop/gnome-extension/captureService.js
apps/desktop/resources/linux/com.t3tools.t3code.metainfo.xml
apps/desktop/scripts/electron-launcher.mjs
apps/desktop/src/app/DesktopEarlyElectronStartup.ts
apps/desktop/src/app/DesktopEnvironment.ts
apps/desktop/src/app/DesktopLinuxUrlHandler.test.ts
apps/desktop/src/app/DesktopPreReadyPlatform.test.ts
apps/desktop/src/preview/Passkeys.test.ts
apps/desktop/src/snapShot/CaptureShortcutConfig.test.ts
apps/desktop/src/snapShot/DesktopSnapShot.test.ts
apps/desktop/src/snapShot/HyprlandSnapShot.test.ts
apps/desktop/src/snapShot/KdeSnapShot.ts
apps/desktop/src/snapShot/LinuxSnapShot.test.ts
apps/desktop/src/snapShot/NiriSnapShot.test.ts
apps/desktop/src/snapShot/PortalCaptureShortcut.test.ts
apps/desktop/src/snapShot/captureConfigEdit.test.ts
apps/marketing/src/lib/site.ts
apps/mobile/app.config.ts
apps/mobile/scripts/measure-renders.mts
apps/server/src/cloud/bootService.test.ts
apps/server/src/cloud/bootService.ts
apps/server/src/serverRuntimeState.test.ts
apps/web/src/components/settings/MobileAppSettingsRow.tsx
docs/internals/linux-snap-shot.md
docs/operations/android-notifications.md
docs/operations/connect-setup.md
docs/operations/release.md
docs/user/background-service.md
docs/user/faq.md
docs/user/install.md
infra/relay/src/agentActivity/ApnsDeliveries.test.ts
infra/relay/src/agentActivity/FcmClient.test.ts
infra/relay/src/agentActivity/FcmDeliveries.test.ts
infra/relay/src/auth/RelayTokens.test.ts
infra/relay/src/environments/EnvironmentConnector.test.ts
infra/relay/src/environments/EnvironmentLinker.test.ts
infra/relay/src/environments/EnvironmentPublishSignatures.test.ts
infra/relay/src/environments/ManagedEndpointProvider.test.ts
infra/relay/src/environments/ManagedEndpointReaper.test.ts
scripts/build-desktop-artifact.test.ts
scripts/build-desktop-artifact.ts
scripts/mobile-e2e/checks.test.ts
scripts/mobile-e2e/device.ts
scripts/mobile-native-client.ts
scripts/mobile-showcase.ts
```

### 4.4 Files containing `pingdotgg` (scripts 8, apps/desktop 6, apps/server 24)

38 files:

```text
apps/desktop/gnome-extension/metadata.json
apps/desktop/resources/linux/com.t3tools.t3code.metainfo.xml
apps/desktop/src/app/DesktopStartupRecovery.ts
apps/desktop/src/snapShot/DesktopSnapShot.test.ts
apps/desktop/src/snapShot/snapShot.test.ts
apps/desktop/src/updates/releaseNotes.test.ts
apps/server/package.json
apps/server/scripts/acp-mock-agent.ts
apps/server/src/cli/triagePrompt.ts
apps/server/src/cli/update.test.ts
apps/server/src/device/EasDeviceHost.test.ts
apps/server/src/git/GitManager.test.ts
apps/server/src/mcp/linkOrigin.test.ts
apps/server/src/mcp/toolkits/pullRequests/handlers.test.ts
apps/server/src/orchestration-v2/Adapters/AcpAdapterV2.test.ts
apps/server/src/orchestration-v2/Orchestrator.control-reads.test.ts
apps/server/src/orchestration-v2/ProjectionStore.test.ts
apps/server/src/orchestration-v2/ThreadStop.test.ts
apps/server/src/orchestration-v2/legacy/LegacyV1Cutover.integration.test.ts
apps/server/src/orchestration-v2/legacy/LegacyV1ThreadImporter.test.ts
apps/server/src/orchestration-v2/runtimeLayer.test.ts
apps/server/src/orchestration-v2/testkit/fixtures/thread_fork_native_prior_turn/codex_transcript.ndjson
apps/server/src/peer/PeerForwarding.test.ts
apps/server/src/persistence/Migrations/050_ProjectionThreadPullRequests.test.ts
apps/server/src/project/AgentSessionScanner.test.ts
apps/server/src/provider/ModelManifest.ts
apps/server/src/pullRequest/PullRequestService.test.ts
apps/server/src/vcs/GitVcsDriver.test.ts
apps/server/src/vcs/GitVcsDriverCore.test.ts
apps/server/src/vcs/VcsStatusBroadcaster.test.ts
scripts/build-desktop-artifact.test.ts
scripts/install.ps1
scripts/install.sh
scripts/install.test.ts
scripts/lib/linux-arm64-sea.ts
scripts/mobile-showcase-environment.ts
scripts/notify-discord-release.test.ts
scripts/npm-launcher/t3.mjs
```

### 4.5 Files containing `x-t3` (22)

22 files:

```text
apps/desktop/src/snapShot/KdeSnapShot.ts
apps/server/src/scheduledTasks/RelayDeliveryProof.ts
apps/server/src/scheduledTasks/webhookRoute.test.ts
apps/server/src/scheduledTasks/webhookRoute.ts
apps/server/src/scheduledTasks/webhookTemplate.test.ts
apps/server/src/scheduledTasks/webhookTemplate.ts
apps/web/src/components/chat/composerMentionDrag.ts
docs/internals/composer-context-references.md
docs/internals/t3-connect.md
docs/operations/relay-observability.md
infra/relay/src/hooks/HookForwarder.test.ts
infra/relay/src/hooks/HookForwarder.ts
infra/relay/src/hooks/upstream.ts
infra/task-cache/src/NativeClients.test.ts
infra/task-cache/src/NativeClients.ts
packages/contracts/src/composerContextClipboard.ts
packages/contracts/src/environment.ts
packages/contracts/src/relay.ts
packages/contracts/src/settings.ts
packages/shared/src/relayJwt.ts
scripts/fixtures/issue-18188/seed-stale-thread-command.js
scripts/mobile-native-client.ts
```

---

## 5. Direct dependencies of KEPT packages (VERIFIED from `package.json` at the pin; licenses from the public npm registry)

**Summary.** 28 KEPT package manifests; 406 dependency rows; 156 unique registry packages checked (rows for `workspace:`/`file:` specs excluded from licence counts).

Licence histogram (rows): MIT 251, Apache-2.0 12, ISC 8, BSD-3-Clause 4, apache-2.0 3, MIT AND Apache-2.0 2, BSD-2-Clause 2, SEE LICENSE IN README.md 1, SEE LICENSE IN LICENSE.md 1, (Apache-2.0 AND OFL-1.1) 1, OFL-1.1 1, (MPL-2.0 OR Apache-2.0) 1, LGPL-3.0 1, (MIT OR GPL-3.0-or-later) 1, NONE-DECLARED 1.

- **COMMERCIAL-SDK terms (check)** (4): @anthropic-ai/claude-agent-sdk (SEE LICENSE IN README.md), @cursor/sdk (SEE LICENSE IN LICENSE.md), @muse-code/sdk (MIT), @opencode-ai/sdk (MIT)
- **PROPRIETARY/UNDECLARED** (3): @anthropic-ai/claude-agent-sdk (SEE LICENSE IN README.md), @cursor/sdk (SEE LICENSE IN LICENSE.md), electron-webauthn (NONE-DECLARED)
- **STRONG-COPYLEFT** (1): jszip ((MIT OR GPL-3.0-or-later))
- **WEAK-COPYLEFT** (2): dompurify ((MPL-2.0 OR Apache-2.0)), heic-to (LGPL-3.0)

Dependencies removed by STRIP (appear in KEPT manifests): `@clerk/clerk-js`, `@clerk/electron`, `@clerk/electron-passkeys`, `@clerk/react`, `@cursor/sdk`, `@muse-code/sdk`, `@t3tools/provider-cursor`, `@t3tools/provider-fx`, `@t3tools/provider-grok`, `@t3tools/provider-muse`.

### `native/resource-monitor/Cargo.toml` (Rust, crate `t3-resource-monitor`, MIT)

| Crate | Section | Version | Licence (crates.io) |
|---|---|---|---|
| `serde` | dependencies | `1.0.228` | MIT OR Apache-2.0 |
| `serde_json` | dependencies | `1.0.150` | MIT OR Apache-2.0 |
| `sysinfo` | dependencies | `0.39.3` | MIT |

No `Cargo.lock` was read; transitive crates are not enumerated (UNKNOWN). Transitive npm dependencies (about 3.6k lockfile entries per R02) are NOT covered here: the `scripts/lib/third-party-licenses.ts` gate (Q-02) is the authority for them.

Method: `package.json` of each KEPT workspace fetched at the pin via the contents API; `catalog:` specs resolved from `pnpm-workspace.yaml@36d4d711` (57 catalog entries parsed); `npm:` aliases resolved to their target. Licences come from the public npm registry version document (`GET registry.npmjs.org/<pkg>/<version>`), the same field `npm view <pkg>@<ver> license` prints, queried over HTTP so that no npm cache file is written (disk rule). Where the exact base version of a range is not published the row says `(latest)`. `UNKNOWN` = lookup failed. Dev dependencies do not ship in the installer but are listed because they enter the build.

### `package.json` (`@t3tools/monorepo` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@coderabbitai/config` | dev | `1.1.0` | 1.1.0 | Apache-2.0 |  |
| `@shadcn/lint` | dev | `0.1.5` | 0.1.5 | MIT |  |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `knip` | dev | `6.34.0` | 6.34.0 | ISC |  |
| `typescript` | dev | `catalog:` | 0.8.0 | MIT AND Apache-2.0 |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `scripts/package.json` (`@t3tools/scripts` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@effect/platform-node` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@electron/asar` | dep | `^4.3.0` | 4.3.0 | MIT |  |
| `@electron/osx-sign` | dep | `2.7.0` | 2.7.0 | BSD-2-Clause |  |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/tailscale` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `agent-device` | dep | `0.21.32` | 0.21.32 | MIT |  |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `playwright-core` | dep | `1.60.0` | 1.60.0 | Apache-2.0 |  |
| `plist` | dep | `catalog:` | 3.1.1 | MIT |  |
| `pngjs` | dep | `7.0.0` | 7.0.0 | MIT |  |
| `sharp` | dep | `0.35.4` | 0.35.4 | Apache-2.0 |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@types/plist` | dev | `catalog:` | 3.0.5 | MIT |  |
| `@types/pngjs` | dev | `6.0.5` | 6.0.5 | MIT |  |
| `esbuild` | dev | `0.28.2` | 0.28.2 | MIT |  |
| `postject` | dev | `1.0.0-alpha.6` | 1.0.0-alpha.6 | MIT |  |
| `typescript` | dev | `catalog:` | 0.8.0 | MIT AND Apache-2.0 |  |
| `typescript-legacy` | dev | `npm:typescript@~6.0.3` | 6.0.3 | Apache-2.0 |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `oxlint-plugin-t3code/package.json` (`@t3tools/oxlint-plugin-t3code` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@effect/platform-node` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@oxlint/plugins` | dep | `^1.63.0` | 1.63.0 | MIT |  |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `apps/server/package.json` (`t3` 0.1.3)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@anthropic-ai/claude-agent-sdk` | dep | `^0.3.276` | 0.3.276 | SEE LICENSE IN README.md | COMMERCIAL-SDK terms (check), PROPRIETARY/UNDECLARED, MOVE out of server.asar (F-06) |
| `@cursor/sdk` | dep | `1.0.38` | 1.0.38 | SEE LICENSE IN LICENSE.md | COMMERCIAL-SDK terms (check), PROPRIETARY/UNDECLARED, REMOVE (F-02/Y-00) |
| `@effect/platform-node` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/platform-node-shared` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@ff-labs/fff-node` | dep | `0.11.0` | 0.11.0 | MIT |  |
| `@muse-code/sdk` | dep | `1.4.6` | 1.4.6 | MIT | COMMERCIAL-SDK terms (check), REMOVE (F-02/Y-00) |
| `@napi-rs/keyring` | dep | `^1.3.0` | 1.3.0 | MIT |  |
| `@opencode-ai/sdk` | dep | `^1.3.15` | 1.3.15 | MIT | COMMERCIAL-SDK terms (check) |
| `@t3tools/provider-acp` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-acp-registry` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-cursor` | dep | `workspace:*` | workspace | - | REMOVE (F-02/Y-00), rename scope (F-03) |
| `@t3tools/provider-fx` | dep | `workspace:*` | workspace | - | REMOVE (F-02/Y-00), rename scope (F-03) |
| `@t3tools/provider-grok` | dep | `workspace:*` | workspace | - | REMOVE (F-02/Y-00), rename scope (F-03) |
| `@t3tools/provider-muse` | dep | `workspace:*` | workspace | - | REMOVE (F-02/Y-00), rename scope (F-03) |
| `@t3tools/provider-opencode` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-pi` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-azure-devops` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-bitbucket` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-definitions` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-forgejo` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-gitcafe` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-github` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-gitlab` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `character-entities` | dep | `2.0.2` | 2.0.2 | MIT |  |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `jose` | dep | `catalog:` | 6.2.2 | MIT |  |
| `node-pty` | dep | `^1.2.0-beta.15` | 1.2.0-beta.15 | MIT |  |
| `playwright-core` | dep | `1.60.0` | 1.60.0 | Apache-2.0 |  |
| `proper-lockfile` | dep | `4.1.2` | 4.1.2 | MIT |  |
| `saxes` | dep | `6.0.0` | 6.0.0 | ISC |  |
| `stream-chain` | dep | `^4.2.5` | 4.2.5 | BSD-3-Clause |  |
| `stream-json` | dep | `3.6.0` | 3.6.0 | BSD-3-Clause |  |
| `undici` | dep | `catalog:` | 8.11.2 | MIT |  |
| `yaml` | dep | `catalog:` | 2.9.0 | ISC |  |
| `yauzl` | dep | `^3.4.0` | 3.4.0 | MIT |  |
| `zod` | dep | `^4.6.5` | 4.6.5 | MIT |  |
| `@effect/graphql-generator` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@modelcontextprotocol/sdk` | dev | `1.29.0` | 1.29.0 | MIT |  |
| `@t3tools/contracts` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-testing` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-testing` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/ssh` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/tailscale` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/web` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `@types/proper-lockfile` | dev | `^4.1.4` | 4.1.4 | MIT |  |
| `@types/yauzl` | dev | `^3.4.0` | 3.4.0 | MIT |  |
| `effect-acp` | dev | `workspace:*` | workspace | - |  |
| `effect-codex-app-server` | dev | `workspace:*` | workspace | - |  |
| `graphql` | dev | `16.14.1` | 16.14.1 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `apps/web/package.json` (`@t3tools/web` 0.1.3)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@base-ui/react` | dep | `^1.4.1` | 1.4.1 | MIT |  |
| `@betteroffice/docx` | dep | `0.4.3` | 0.4.3 | Apache-2.0 |  |
| `@betteroffice/fonts` | dep | `0.4.0` | 0.4.0 | (Apache-2.0 AND OFL-1.1) |  |
| `@betteroffice/pptx` | dep | `0.2.0` | 0.2.0 | Apache-2.0 |  |
| `@betteroffice/xlsx` | dep | `0.3.0` | 0.3.0 | Apache-2.0 |  |
| `@clerk/clerk-js` | dep | `catalog:` | 6.40.0 | MIT | REMOVE (F-02/Y-00) |
| `@clerk/electron` | dep | `catalog:` | 0.1.3 | MIT | REMOVE (F-02/Y-00) |
| `@clerk/react` | dep | `catalog:` | 6.18.0 | MIT | REMOVE (F-02/Y-00) |
| `@daypicker/react` | dep | `^10.0.1` | 10.0.1 | MIT |  |
| `@dnd-kit/core` | dep | `^6.3.1` | 6.3.1 | MIT |  |
| `@dnd-kit/modifiers` | dep | `^9.0.0` | 9.0.0 | MIT |  |
| `@dnd-kit/sortable` | dep | `^10.0.0` | 10.0.0 | MIT |  |
| `@dnd-kit/utilities` | dep | `^3.2.2` | 3.2.2 | MIT |  |
| `@effect/atom-react` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@fontsource-variable/inter` | dep | `^5.3.0` | 5.3.0 | OFL-1.1 |  |
| `@formkit/auto-animate` | dep | `^0.9.0` | 0.9.0 | MIT |  |
| `@legendapp/list` | dep | `catalog:` | 3.3.5 | MIT |  |
| `@noble/hashes` | dep | `catalog:` | 1.8.0 | MIT |  |
| `@pierre/diffs` | dep | `catalog:` | 1.6.1 | apache-2.0 |  |
| `@pierre/trees` | dep | `1.0.0-beta.6` | 1.0.0-beta.6 | apache-2.0 |  |
| `@t3tools/client-runtime` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@tanstack/react-pacer` | dep | `^0.19.4` | 0.19.4 | MIT |  |
| `@tanstack/react-router` | dep | `^1.160.2` | 1.160.2 | MIT |  |
| `@tiptap/core` | dep | `^3.31.3` | 3.31.3 | MIT |  |
| `@tiptap/extension-blockquote` | dep | `^3.31.3` | 3.31.3 | MIT |  |
| `@tiptap/extension-code` | dep | `^3.31.3` | 3.31.3 | MIT |  |
| `@tiptap/extension-code-block` | dep | `^3.31.3` | 3.31.3 | MIT |  |
| `@tiptap/extension-heading` | dep | `^3.31.3` | 3.31.3 | MIT |  |
| `@tiptap/extension-horizontal-rule` | dep | `^3.31.3` | 3.31.3 | MIT |  |
| `@tiptap/extension-italic` | dep | `^3.31.3` | 3.31.3 | MIT |  |
| `@tiptap/extension-list` | dep | `^3.31.3` | 3.31.3 | MIT |  |
| `@tiptap/extension-task-item` | dep | `^3.31.3` | 3.31.3 | MIT |  |
| `@tiptap/extension-task-list` | dep | `^3.31.3` | 3.31.3 | MIT |  |
| `@tiptap/pm` | dep | `^3.31.3` | 3.31.3 | MIT |  |
| `@tiptap/react` | dep | `^3.31.3` | 3.31.3 | MIT |  |
| `@tiptap/starter-kit` | dep | `^3.31.3` | 3.31.3 | MIT |  |
| `class-variance-authority` | dep | `^0.7.1` | 0.7.1 | Apache-2.0 |  |
| `culori` | dep | `^4.0.2` | 4.0.2 | MIT |  |
| `dompurify` | dep | `^3.4.16` | 3.4.16 | (MPL-2.0 OR Apache-2.0) | WEAK-COPYLEFT |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `entities` | dep | `8.1.0` | 8.1.0 | BSD-2-Clause |  |
| `fast-xml-parser` | dep | `5.7.3` | 5.7.3 | MIT |  |
| `hast-util-to-html` | dep | `^9.0.5` | 9.0.5 | MIT |  |
| `hast-util-to-jsx-runtime` | dep | `^2.3.6` | 2.3.6 | MIT |  |
| `heic-to` | dep | `^1.5.2` | 1.5.2 | LGPL-3.0 | WEAK-COPYLEFT |
| `jose` | dep | `catalog:` | 6.2.2 | MIT |  |
| `jsonc-parser` | dep | `3.3.1` | 3.3.1 | MIT |  |
| `jszip` | dep | `3.10.1` | 3.10.1 | (MIT OR GPL-3.0-or-later) | STRONG-COPYLEFT |
| `katex` | dep | `^0.16.47` | 0.16.47 | MIT |  |
| `lucide` | dep | `^0.564.0` | 0.564.0 | ISC |  |
| `lucide-react` | dep | `^0.564.0` | 0.564.0 | ISC |  |
| `morphicons` | dep | `^1.7.1` | 1.7.1 | MIT |  |
| `pdfjs-dist` | dep | `6.4.299` | 6.4.299 | Apache-2.0 |  |
| `pele` | dep | `^1.8.0` | 1.8.0 | MIT |  |
| `react` | dep | `catalog:` | 19.3.0 | MIT |  |
| `react-dom` | dep | `catalog:` | 19.3.0 | MIT |  |
| `react-markdown` | dep | `^10.1.0` | 10.1.0 | MIT |  |
| `remark-gfm` | dep | `catalog:` | 4.0.1 | MIT |  |
| `remark-math` | dep | `6.0.0` | 6.0.0 | MIT |  |
| `remark-parse` | dep | `catalog:` | 11.0.0 | MIT |  |
| `saxes` | dep | `6.0.0` | 6.0.0 | ISC |  |
| `sql.js` | dep | `1.15.0` | 1.15.0 | MIT |  |
| `tailwind-merge` | dep | `^3.4.0` | 3.4.0 | MIT |  |
| `tiff` | dep | `7.1.3` | 7.1.3 | MIT |  |
| `unbash` | dep | `^5.0.0` | 5.0.0 | ISC |  |
| `unified` | dep | `catalog:` | 11.0.5 | MIT |  |
| `use-sync-external-store` | dep | `^1.6.0` | 1.6.0 | MIT |  |
| `zustand` | dep | `^5.0.11` | 5.0.11 | MIT |  |
| `@effect/platform-node` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@tailwindcss/vite` | dev | `^4.0.0` | 4.0.0 | MIT |  |
| `@tanstack/router-plugin` | dev | `^1.161.0` | 1.161.0 | MIT |  |
| `@types/compression` | dev | `^1.8.1` | 1.8.1 | MIT |  |
| `@types/culori` | dev | `^4.0.1` | 4.0.1 | MIT |  |
| `@types/mdast` | dev | `^4.0.4` | 4.0.4 | MIT |  |
| `@types/react` | dev | `catalog:` | 19.3.0 | MIT |  |
| `@types/react-dom` | dev | `catalog:` | 19.3.0 | MIT |  |
| `@types/sql.js` | dev | `1.4.11` | 1.4.11 | MIT |  |
| `@types/use-sync-external-store` | dev | `^0.0.6` | 0.0.6 | MIT |  |
| `@vercel/config` | dev | `^0.3.0` | 0.3.0 | MIT |  |
| `@vitejs/plugin-react` | dev | `^6.1.2` | 6.1.2 | MIT |  |
| `@vitest/browser-playwright` | dev | `5.0.5` | 5.0.5 | MIT |  |
| `compression` | dev | `^1.8.2` | 1.8.2 | MIT |  |
| `oxc-transform-react` | dev | `~0.152.0` | 0.152.0 | MIT |  |
| `playwright` | dev | `1.60.0` | 1.60.0 | Apache-2.0 |  |
| `tailwindcss` | dev | `^4.0.0` | 4.0.0 | MIT |  |
| `vite` | dev | `catalog:` | 1.4.0 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `apps/desktop/package.json` (`@t3tools/desktop` 0.1.3)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@clerk/electron` | dep | `catalog:` | 0.1.3 | MIT | REMOVE (F-02/Y-00) |
| `@clerk/electron-passkeys` | dep | `catalog:` | 0.0.3 | MIT | REMOVE (F-02/Y-00) |
| `@crowecawcaw/xa11y` | dep | `0.13.0` | 0.13.0 | MIT |  |
| `@effect/platform-node` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@napi-rs/keyring` | dep | `^1.3.0` | 1.3.0 | MIT |  |
| `@t3tools/client-runtime` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/ssh` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/tailscale` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `dbus-next` | dep | `0.10.2` | 0.10.2 | MIT |  |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `electron` | dep | `44.9.3` | 44.9.3 | MIT |  |
| `electron-store` | dep | `^8.2.0` | 8.2.0 | MIT |  |
| `electron-updater` | dep | `^6.8.9` | 6.8.9 | MIT |  |
| `electron-webauthn` | dep | `catalog:` | 1.3.1 | NONE-DECLARED | PROPRIETARY/UNDECLARED |
| `ffi-rs` | dep | `1.3.2` | 1.3.2 | MIT |  |
| `playwright-core` | dep | `1.60.0` | 1.60.0 | Apache-2.0 |  |
| `react-grab` | dep | `^0.1.32` | 0.1.32 | MIT |  |
| `tldts` | dep | `catalog:` | 7.4.2 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `acorn` | dev | `8.16.0` | 8.16.0 | MIT |  |
| `cross-env` | dev | `^10.1.0` | 10.1.0 | MIT |  |
| `electron-builder` | dev | `26.16.1` | 26.16.1 | MIT |  |
| `tailwindcss` | dev | `^4.0.0` | 4.0.0 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/contracts/package.json` (`@t3tools/contracts` 0.1.3)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/client-runtime/package.json` (`@t3tools/client-runtime` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@pierre/diffs` | dep | `catalog:` | 1.6.1 | apache-2.0 |  |
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-acp-registry` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-cursor` | dep | `workspace:*` | workspace | - | REMOVE (F-02/Y-00), rename scope (F-03) |
| `@t3tools/provider-fx` | dep | `workspace:*` | workspace | - | REMOVE (F-02/Y-00), rename scope (F-03) |
| `@t3tools/provider-grok` | dep | `workspace:*` | workspace | - | REMOVE (F-02/Y-00), rename scope (F-03) |
| `@t3tools/provider-muse` | dep | `workspace:*` | workspace | - | REMOVE (F-02/Y-00), rename scope (F-03) |
| `@t3tools/provider-opencode` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-pi` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-definitions` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `three` | dep | `0.180.0` | 0.180.0 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@types/three` | dev | `0.180.0` | 0.180.0 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/shared/package.json` (`@t3tools/shared` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@noble/curves` | dep | `catalog:` | 1.9.1 | MIT |  |
| `@noble/hashes` | dep | `catalog:` | 1.8.0 | MIT |  |
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `jose` | dep | `catalog:` | 6.2.2 | MIT |  |
| `mdast-util-directive` | dep | `catalog:` | 3.1.0 | MIT |  |
| `mdast-util-to-hast` | dep | `^13.2.1` | 13.2.1 | MIT |  |
| `micromark-extension-directive` | dep | `catalog:` | 4.0.0 | MIT |  |
| `micromark-util-character` | dep | `catalog:` | 2.1.1 | MIT |  |
| `rehype-raw` | dep | `catalog:` | 7.0.0 | MIT |  |
| `rehype-sanitize` | dep | `catalog:` | 6.0.0 | MIT |  |
| `remark-breaks` | dep | `catalog:` | 4.0.0 | MIT |  |
| `remark-gfm` | dep | `catalog:` | 4.0.1 | MIT |  |
| `remark-math` | dep | `6.0.0` | 6.0.0 | MIT |  |
| `remark-parse` | dep | `catalog:` | 11.0.0 | MIT |  |
| `remark-rehype` | dep | `catalog:` | 11.1.2 | MIT |  |
| `unified` | dep | `catalog:` | 11.0.5 | MIT |  |
| `yaml` | dep | `catalog:` | 2.9.0 | ISC |  |
| `@effect/platform-node` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@types/mdast` | dev | `^4.0.4` | 4.0.4 | MIT |  |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `micromark-util-types` | dev | `catalog:` | 2.0.2 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/provider-core/package.json` (`@t3tools/provider-core` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/platform-node` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/effect-codex-app-server/package.json` (`effect-codex-app-server` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/openapi-generator` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/platform-node` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/effect-acp/package.json` (`effect-acp` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/openapi-generator` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/platform-node` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/provider-acp/package.json` (`@t3tools/provider-acp` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `diff` | dep | `8.0.3` | 8.0.3 | BSD-3-Clause |  |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/platform-node` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `effect-acp` | dev | `workspace:*` | workspace | - |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/provider-acp-registry/package.json` (`@t3tools/provider-acp-registry` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@noble/hashes` | dep | `catalog:` | 1.8.0 | MIT |  |
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-acp` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/platform-node` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@t3tools/provider-testing` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `effect-acp` | dev | `workspace:*` | workspace | - |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/provider-opencode/package.json` (`@t3tools/provider-opencode` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@opencode-ai/sdk` | dep | `^1.3.15` | 1.3.15 | MIT | COMMERCIAL-SDK terms (check) |
| `@opencode/client` | dep | `2.0.28` | 2.0.28 | MIT |  |
| `@opencode/protocol` | dep | `2.0.28` | 2.0.28 | MIT |  |
| `@opencode/schema` | dep | `2.0.28` | 2.0.28 | MIT |  |
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/platform-node` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@t3tools/provider-testing` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/provider-pi/package.json` (`@t3tools/provider-pi` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/platform-node` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@t3tools/provider-testing` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/provider-testing/package.json` (`@t3tools/provider-testing` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@effect/platform-node` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |

### `packages/source-control-core/package.json` (`@t3tools/source-control-core` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/source-control-definitions/package.json` (`@t3tools/source-control-definitions` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@t3tools/source-control-azure-devops` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-bitbucket` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-forgejo` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-gitcafe` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-github` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-gitlab` | dep | `workspace:*` | workspace | - | rename scope (F-03) |

### `packages/source-control-github/package.json` (`@t3tools/source-control-github` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/graphql-generator` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/platform-node` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@t3tools/source-control-testing` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/source-control-gitlab/package.json` (`@t3tools/source-control-gitlab` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@t3tools/source-control-testing` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/source-control-bitbucket/package.json` (`@t3tools/source-control-bitbucket` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/platform-node` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@t3tools/source-control-testing` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/source-control-azure-devops/package.json` (`@t3tools/source-control-azure-devops` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `diff` | dep | `8.0.3` | 8.0.3 | BSD-3-Clause |  |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/platform-node` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@t3tools/source-control-testing` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/source-control-forgejo/package.json` (`@t3tools/source-control-forgejo` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/platform-node` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@t3tools/source-control-testing` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/source-control-gitcafe/package.json` (`@t3tools/source-control-gitcafe` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/provider-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@t3tools/source-control-testing` | dev | `workspace:*` | workspace | - | rename scope (F-03) |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/source-control-testing/package.json` (`@t3tools/source-control-testing` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@effect/platform-node` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/source-control-core` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |

### `packages/ssh/package.json` (`@t3tools/ssh` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@t3tools/contracts` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/platform-node` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |

### `packages/tailscale/package.json` (`@t3tools/tailscale` -)

| Dependency | Section | Spec | Resolved | Licence | Flag / action |
|---|---|---|---|---|---|
| `@t3tools/shared` | dep | `workspace:*` | workspace | - | rename scope (F-03) |
| `effect` | dep | `catalog:` | 4.0.5 | MIT |  |
| `@effect/vitest` | dev | `catalog:` | 4.0.5 | MIT |  |
| `@types/node` | dev | `catalog:` | 24.12.4 | MIT |  |
| `vite-plus` | dev | `catalog:` | 1.4.0 | MIT |  |


---

## 6. Tests per KEPT area, replay fixtures, and tests removed with STRIP (VERIFIED from tree paths)

Test file = path containing `.test.` or `.spec.` (covers `.test.ts(x)`, `.integration.test.ts`, `.browser.test.tsx`, `.test.cjs/.mjs/.py`).

### 6.1 Test files by workspace (KEEP / MODIFY / STRIP)

| Workspace | Tests kept | Tests that are MODIFY paths* | Tests removed (STRIP) | Of which integration | Of which browser |
|---|---:|---:|---:|---:|---:|
| `.github (non-workflow)` | 1 | 0 | 4 | 0 | 0 |
| `apps/desktop` | 91 | 0 | 11 | 0 | 0 |
| `apps/mobile` | 0 | 0 | 245 | 0 | 0 |
| `apps/server` | 357 | 1 | 60 | 24 | 0 |
| `apps/web` | 405 | 1 | 11 | 0 | 102 |
| `evals` | 0 | 0 | 1 | 0 | 0 |
| `infra/relay` | 0 | 0 | 32 | 0 | 0 |
| `infra/task-cache` | 0 | 0 | 11 | 0 | 0 |
| `native/kde-snap-shot` | 2 | 0 | 0 | 0 | 0 |
| `oxlint-plugin-t3code` | 28 | 0 | 0 | 0 | 0 |
| `packages/client-runtime` | 134 | 0 | 5 | 0 | 0 |
| `packages/contracts` | 28 | 0 | 1 | 0 | 0 |
| `packages/effect-acp` | 6 | 0 | 0 | 0 | 0 |
| `packages/effect-codex-app-server` | 5 | 0 | 0 | 0 | 0 |
| `packages/provider-acp` | 7 | 0 | 0 | 0 | 0 |
| `packages/provider-acp-registry` | 5 | 0 | 0 | 0 | 0 |
| `packages/provider-core` | 19 | 0 | 0 | 0 | 0 |
| `packages/provider-cursor` | 0 | 0 | 14 | 0 | 0 |
| `packages/provider-fx` | 0 | 0 | 3 | 0 | 0 |
| `packages/provider-grok` | 0 | 0 | 5 | 0 | 0 |
| `packages/provider-muse` | 0 | 0 | 10 | 0 | 0 |
| `packages/provider-opencode` | 15 | 0 | 0 | 0 | 0 |
| `packages/provider-pi` | 7 | 0 | 0 | 0 | 0 |
| `packages/shared` | 83 | 0 | 7 | 0 | 0 |
| `packages/source-control-azure-devops` | 7 | 0 | 0 | 0 | 0 |
| `packages/source-control-bitbucket` | 6 | 0 | 0 | 0 | 0 |
| `packages/source-control-core` | 5 | 0 | 0 | 0 | 0 |
| `packages/source-control-forgejo` | 6 | 0 | 0 | 0 | 0 |
| `packages/source-control-gitcafe` | 6 | 0 | 0 | 0 | 0 |
| `packages/source-control-github` | 18 | 0 | 0 | 0 | 0 |
| `packages/source-control-gitlab` | 10 | 0 | 0 | 0 | 0 |
| `packages/ssh` | 4 | 0 | 0 | 0 | 0 |
| `packages/tailscale` | 1 | 0 | 0 | 0 | 0 |
| `scripts` | 20 | 0 | 8 | 0 | 0 |
| **Total first-party (excl. `.repos/`)** | **1276** | **2** | **428** | 24 | 102 |

*A test file that is itself a MODIFY path (e.g. `IntegrationsSettings.logic.test.ts`). Test files that merely sit next to a MODIFY source file are KEPT but must be updated (list in 3.9). `.repos/` holds 3778 further test files (all stripped).

R02 sec.8 reports 1,693 first-party test files; this tree-path count is 1706 (this table counts any path containing `.test.` or `.spec.`, including `.test.py/.cjs/.mjs`; R02 counted `.ts(x)` only).

**Tests surviving STRIP: 1278** (KEEP 1276 + MODIFY-path 2). This is the denominator for Q-05.

### 6.2 Kept test areas called out by R02 (VERIFIED counts of surviving test files)

| Area | Path pattern | Surviving test files |
|---|---|---:|
| orchestration-v2 (all) | `^apps/server/src/orchestration-v2/` | 101 |
| orchestration-v2 testkit (replay, recovery) | `^apps/server/src/orchestration-v2/testkit/` | 10 |
| persistence (store, migrations) | `^apps/server/src/persistence/` | 27 |
| provider adapters (Adapters/) | `^apps/server/src/orchestration-v2/Adapters/` | 8 |
| server provider/ | `^apps/server/src/provider/` | 46 |
| mcp | `^apps/server/src/mcp/` | 23 |
| vcs + git + checkpointing | `^apps/server/src/(vcs\|git\|checkpointing)/` | 12 |
| terminal | `^apps/server/src/terminal/` | 4 |
| auth | `^apps/server/src/auth/` | 12 |
| server preview/browser | `^apps/server/src/preview/` | 10 |
| desktop preview/browser host | `^apps/desktop/src/preview/` | 13 |
| desktop updates | `^apps/desktop/src/updates/` | 5 |
| web browser + preview UI | `^apps/web/src/(browser\|components/preview)/` | 20 |
| provider-acp | `^packages/provider-acp/` | 7 |
| effect-acp / codex-app-server | `^packages/(effect-acp\|effect-codex-app-server)/` | 11 |
| contracts | `^packages/contracts/` | 28 |
| scripts (build/release) | `^scripts/` | 20 |
| oxlint plugin | `^oxlint-plugin-t3code/` | 28 |

### 6.3 Replay fixtures (`apps/server/src/orchestration-v2/testkit/fixtures/`)

- Fixture dirs at pin: **92** (348 files incl. shared `index.ts`/`shared.ts`/READMEs, 7,547,006 B). R02 sec.8 counted 94; this count is VERIFIED from paths (dirs directly under `fixtures/`).
- STRIP whole dirs (only Cursor/Fx/Grok/Muse transcripts): **14**: `fx_early_stop`, `fx_subagent`, `grok_auto_blocked_command`, `grok_background_bash`, `grok_background_bash_fast_wake`, `grok_background_subagent`, `grok_monitor`, `grok_prompt_error`, `grok_subagent_lineage`, `muse_permission`, `muse_subagent_approval`, `muse_subagent_interrupt`, `muse_workflow`, `skill_invocation`.
- Files kept: **263**; files stripped: **85** (stripped-provider files in kept dirs + whole dirs).

Kept fixture files by kind: claude 54, codex 51, opencode 23, pi 15, registry 11, shared README.md 4, shared index.ts 1, shared input.ts 64, shared output.ts 39, shared shared.ts 1.

Stripped fixture files by kind: cursor 18, fx 13, grok 18, muse 11, shared input.ts 14, shared output.ts 11.

Other fixture dirs outside orchestration-v2: `apps/server/integration/fixtures/` (1), `apps/web/test/fixtures/` (3), `packages/effect-acp/test/fixtures/` (2), `packages/effect-codex-app-server/test/fixtures/` (1) - KEPT; `scripts/fixtures/` (9 files, 907,420 B, issue-18188 seeds) and `apps/mobile/scripts/fixtures/` (3) - STRIP.

Rust: `native/resource-monitor` has no separate test files (inline `cargo test`, R02 sec.8).

### 6.4 Tests removed with STRIP (by rule, excluding `.repos/`)

| STRIP rule | Test files removed |
|---|---:|
| `apps/mobile` | 245 |
| `apps/marketing` | 0 |
| `infra/relay` | 32 |
| `infra/task-cache` | 11 |
| `native/browser-secret` | 0 |
| `packages/provider-cursor` | 14 |
| `packages/provider-fx` | 3 |
| `packages/provider-grok` | 5 |
| `packages/provider-muse` | 10 |
| `browser-import` | 11 |
| `v1-importer` | 2 |
| `antigravity` | 13 |
| `stripped-provider-adapters/testkits` | 6 |
| `telemetry-posthog` | 4 |
| `connect-clerk-relay` | 44 |
| `mobile-device-tooling` | 15 |
| `scripts-mobile-and-misc` | 8 |
| `github-non-core` | 4 |
| `assets` | 0 |
| `docs-user-ops` | 0 |
| `evals` | 1 |
| `upstream-agent-and-ci-config` | 0 |
| `patches-mobile-clerk-muse` | 0 |
| `fixture-dirs-of-stripped-providers` | 0 |

Kept perf-budget and wire suites from R02 sec.8: `test:perf:v2-wire` (16 suites) and `apps/server/integration/transferBudgetV2.integration.test.ts`.

---

## 7. Build and packaging files to modify

Existence and size are VERIFIED from the tree (`*` = not present at the pin). Disposition column agrees with the classifier of section 2 except where the "KEEP (sweep)" note says the file only changes through the section 4 mechanical sweep.

| Path@36d4d711 | Bytes | Disposition | Why it changes |
|---|---:|---|---|
| `scripts/build-desktop-artifact.ts` | 151,914 | MODIFY | Installer builder: electron-builder config, NSIS, server.asar sidecar, SDK exclusions, Clerk key, publish config, Azure Trusted Signing (R02 sec.7) |
| `scripts/build-desktop-artifact.test.ts` | 70,386 | KEEP | Asserts packaging config; update expectations (T3Tools.T3Code hits) with the identity sweep |
| `scripts/lib/windows-jsign.ts` | 2,203 | KEEP | jsign signing helper - relevant to F-11 OV cert + cloud-HSM |
| `scripts/verify-windows-desktop-artifact.ts` | 1,877 | KEEP | Windows payload check |
| `scripts/merge-update-manifests.ts` | 3,652 | MODIFY | Merged update manifests |
| `scripts/merge-update-manifests.test.ts` | 5,313 | KEEP | Test |
| `scripts/mock-update-server.ts` | 5,176 | KEEP | Local feed for updater tests (reused by Q-14) |
| `scripts/build-cli-archive.ts` | 21,731 | KEEP | CLI archive (`t3` -> `zain` via sweep) |
| `scripts/smoke-cli-archive.ts` | 7,095 | KEEP | Smoke |
| `scripts/smoke-desktop-app.ts` | 4,490 | KEEP | Smoke |
| `scripts/release-smoke.ts` | 13,841 | KEEP | Release smoke (identity via sweep) |
| `scripts/build-npm-launcher.ts` | 4,660 | KEEP | npx launcher builder (decide strip vs rename with t3.mjs) |
| `scripts/install.sh` | 10,068 | MODIFY | Installer (pingdotgg hits) |
| `scripts/install.ps1` | 11,259 | MODIFY | Windows installer (T3Tools.T3Code, t3.codes, pingdotgg) |
| `scripts/sign-macos.ts` | 224 | KEEP | macOS signing (224 B shim) |
| `scripts/resolve-nightly-release.ts` | 7,581 | KEEP | Nightly resolution |
| `scripts/resolve-previous-release-tag.ts` | 11,403 | KEEP | Release tag resolution |
| `scripts/update-release-package-versions.ts` | 5,668 | KEEP | Version bump across packages (workspace list via sweep) |
| `scripts/lib/third-party-licenses.ts` | 41,210 | KEEP | Notice generation gate |
| `scripts/lib/desktop-external-packages.ts` | 816 | MODIFY | Externals list (drop Clerk) |
| `scripts/lib/cli-external-packages.ts` | 2,978 | MODIFY | Externals list (drop Clerk) |
| `scripts/lib/public-config.ts` | 5,770 | KEEP | Build-time public config (`T3CODE_*` via sweep; Clerk/relay URLs must be reviewed - UNVERIFIED) |
| `scripts/lib/linux-arm64-sea.ts` | 4,743 | KEEP | pingdotgg hit - review |
| `scripts/apply-web-brand-assets.ts` | 2,445 | KEEP | Brand asset application -> Zain assets |
| `scripts/export-brand-icons.ts` | 25,662 | KEEP | Icon export -> Zain icons |
| `scripts/dev-runner.ts` | 35,221 | MODIFY | Dev runner (`T3CODE_` env) |
| `scripts/setup-worktree.ts` | 4,848 | KEEP | Dev worktree setup |
| `scripts/check-changed.ts` | 13,410 | KEEP | Changed-file CI helper |
| `apps/desktop/package.json` | 1,287 | MODIFY | electron-builder `build` block, `productName`, deps |
| `apps/desktop/scripts/electron-launcher.mjs` | 15,807 | KEEP | Launcher (T3Tools.T3Code hit - sweep) |
| `apps/desktop/vite.config.ts` | 5,035 | MODIFY | Bundle config (Clerk externals) |
| `apps/server/vite.config.ts` | 6,173 | KEEP | Server bundle (Clerk hit in code search - review) |
| `apps/web/vite.config.ts` | 14,750 | MODIFY | Web bundle (Clerk hit) |
| `apps/desktop/resources/linux/com.t3tools.t3code.metainfo.xml` | 1,082 | MODIFY | AppStream metadata (rename) |
| `patches/app-builder-lib@26.16.1.patch` | 980 | KEEP | Patched electron-builder core |
| `patches/node-pty@1.2.0-beta.15.patch` | 2,870 | KEEP | node-pty patch |
| `pnpm-workspace.yaml` | 16,555 | MODIFY | Workspace globs, catalog, overrides, release-age excludes |
| `package.json` | 6,042 | MODIFY | Root scripts / engines / packageManager `pnpm@12.14.0` |
| `pnpm-lock.yaml` | 911,965 | MODIFY | Regenerated, never edited |
| `third-party-licenses.config.json` | 26,373 | MODIFY | Notice config |
| `.github/workflows/ci.yml` | 23,769 | MODIFY | CI |
| `.github/workflows/windows-tests.yml` | 2,874 | MODIFY | Windows CI |
| `.github/workflows/release.yml` | 61,987 | MODIFY | Release pipeline |
| `.github/workflows/release-desktop.yml` | 32,938 | MODIFY | Desktop release |
| `.github/actions/ci-changes/action.yml` | 2,253 | KEEP | CI change detection |
| `.github/actions/setup-ci-deps/action.yml` | 3,671 | KEEP | CI deps |
| `.github/actions/setup-apt-mirrors/action.yml` | 1,086 | KEEP | CI apt mirrors |
| `native/resource-monitor/Cargo.toml` | 298 | KEEP | Rust sidecar crate |

Other packaging facts (VERIFIED, R02 sec.7): Windows NSIS x64/arm64 with `resources/server.asar` sidecar (`build-desktop-artifact.ts@36d4d711:L1018` `WINDOWS_SERVER_ASAR_RESOURCE`, L715-779 payload checks); macOS DMG sign + notarize; Linux AppImage + `.deb`; desktop spawns the server with `ELECTRON_RUN_AS_NODE=1` (`DesktopBackendConfiguration.ts@36d4d711:L522-534`); `packaging/aur/*` (5 files) STRIPPED. The Zain Core binary `zain-core` is packaged next to `server.asar` (07 sec.9, F-10) - a net-new step in `build-desktop-artifact.ts`.

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
- Licence flags needing a decision: jszip is dual (MIT OR GPL-3.0-or-later; elect MIT), heic-to LGPL-3.0 (dynamic-link/attribution review), dompurify (MPL-2.0 OR Apache-2.0; elect Apache-2.0), electron-webauthn has no declared licence, and @anthropic-ai/claude-agent-sdk and @cursor/sdk carry custom terms (SEE LICENSE).
