# 24 — First Working Build (R0a), Tester Build (R0b), Qualified R0 — revision 4

```text
STATUS = R0a FOUNDER WORK ORDER APPROVED TO START Q-00, subject to all A3-A7 evidence gates; nothing built/run or package-qualified by this document. The concrete selected build route is in OPUS_R0A_BUILD_EXECUTION_2026-11-02.md.
STRATEGY = Copy First: T3 @36d4d711 is the application foundation; Zain compiles and packages T3's own code with a
           small set of overlays. Nothing that T3 already provides is rebuilt.
NUMBERS = generated (GENERATED_PLAN_REPORT.md §3). R0a has a 2.8–7.6 person-week KNOWN-WORK SUBTOTAL; Q-06 is MEASURE and excluded, so this is NOT a delivery bound,
          not a delivery envelope; the earlier 0.9–2.6 pw figure is withdrawn (it omitted the build DAG, inventories,
          admission and fix-to-pass work).
APPROVAL_PACKET = R0A_FEASIBILITY_READINESS.md (approvable without approving R1)
```

## 1. Upstream evidence (unchanged facts; corrected interpretation)

| Evidence | What it shows | What it does not show |
|---|---|---|
| T3 v0.1.3 (2026-10-27, target `d2c44031`) ships `T3-Code-0.1.3-x64.exe` (288,555,696 bytes); nightlies ship Windows x64 installers (Astro-verified) | T3's pipeline produces Windows installers from source at those commits | that our pin `36d4d711` builds; the `win32-x64.zip` is a CLI archive, not a portable desktop build |
| Five successful Release runs for `36d4d711` (e.g. 40539812023) **skipped** the JS build and Windows x64 jobs (Astro) | — | buildability of the pin (unestablished, not disproven) |
| `release.yml` @pin: `resolve_commit` guarded by `github.repository == 'pingdotgg/t3code'` (L51–55); `preflight` uses secret `T3_TASK_CACHE_READ_TOKEN` (L102–135); `relay_public_config` needs `CLOUDFLARE_API_TOKEN` (L388–459); `build_bundle` on 32 vCPU, 30-min timeout, needs relay config, uploads `js-bundle` (L502–590); Windows x64 caller uses reusable `release-desktop.yml` (L706–728) | the Windows job is one node of a DAG with donor-secret dependencies | that free runners finish within timeouts |
| `release-desktop.yml` @pin: build job (70-min timeout on Windows, L119–124) downloads relay tracing (L196–203) and `js-bundle` (L218–220); embeds the same-arch Linux CLI archive for WSL (L377–436, L505–506); signing secrets (L444–458); separate Windows `verify` job, 15 min (L660–690) | WSL packaging and verification are part of the upstream Windows output | an installer/desktop-UI/provider e2e — upstream verify checks native loads, CLI and resource monitor only |
| T3 `ClaudeAdapterV2.ts` L24 imports `query`, `getSessionMessages`, `forkSession` at runtime; `scripts/lib/cli-external-packages.ts` L3 removes optional Claude executables but keeps SDK JS; `apps/server/vite.config.ts` L106 bundling config; Cursor registered via provider imports | deleting package directories after bundling does not remove SDK code and can break module loading | — |
| Founder machine: Windows 11 Home | — | Windows Sandbox / Hyper-V are not available; isolation uses a separate local Windows user account |

## 2. What Copy First saves (reviewable) and what it does not

Reused without reimplementing: Electron shell, web UI, server, orchestration-v2, retained providers (Codex, ACP; Claude later via
F-06), terminals, worktrees, diff review, `build-desktop-artifact.ts` with unsigned NSIS (`signed` defaults false), native
probes, notices tooling (`licenses:sync`), upstream verify steps, 1,278 test files.

Not saved: compiling a new JS bundle from modified source, removing donor-secret steps from the DAG, provider-disabled
bundling, identity/egress inventories, admission records, and fixing whatever blocks the minimum smoke on this machine.

## 3. Minimal R0a build DAG (Q-04)

```text
source @36d4d711 + overlays (Q-02 identity, Q-03 egress, provider registry: Claude + Cursor disabled)
  └─▶ [1] install: pnpm 12.14.0 --frozen-lockfile, Node 26.12.1, pinned action SHAs; no task-cache secret
       └─▶ [2] JS + Windows CLI SEA bundles: build_bundle and separate CLI bundling WITHOUT relay_public_config / relay tracing; telemetry channel 'dev';
               repository guard and donor publish steps removed; Claude/Cursor removed from BOTH BUILT_IN_DRIVERS and BUILT_IN_USAGE_DRIVERS plus indirect imports; provenance for EVERY bundled root kept for PKG-01
            └─▶ [3] native + CLI archive + package staging: resource monitor/native modules, sanitized Windows CLI SEA/archive, build-desktop-artifact.ts --platform win
                    --target nsis (unsigned), NO --wsl-runtime AND clear T3CODE_DESKTOP_WSL_RUNTIME (WSL backend disabled for R0a)
                 └─▶ [4] Windows verify: native loads, actual Windows CLI SEA/archive, resource monitor + PKG-01 scan of all ASAR/SEA/nested/unpacked payload roots
                      └─▶ [5] LOCAL_ONLY artifact (PKG-02; no hosted build without new explicit verified zero-cost approval) → Q-05 installed + provider smoke
```

Where it runs (zero cost, A2-02): LOCAL_ONLY on the founder Windows machine (requires Node 26.12.1, pnpm 12.14.0, Python/node-gyp,
Rust MSVC target, Visual Studio C++ build tools/Windows SDK and verified available free disk/RAM — do not start a cold build if resource preflight fails). No hosted GitHub build or paid fallback is approved. A future private repository route needs a new verified spending/access/retention decision. The public Zain repository never uploads a binary or packaged-content log.

WSL: disabled in R0a (no Linux CLI archive built); restoration in qualified R0 requires an explicit new task with sanitized Linux CLI archive, identity/egress parity and real startup/provider smoke. F-02 alone does not presently schedule this work. Do not modify existing founder WSL disks.

## 4. Inventories (Q-02, Q-03)

### 4.1 Identity and runtime paths (Q-02; tests FWB-02..04)

| Path class | Known site @pin | Required behaviour |
|---|---|---|
| App home `.t3` | `apps/desktop/src/app/DesktopStatePaths.ts` L13/L19 | Zain dev home, never the T3 home |
| Electron userData/profile; legacy dev-profile reuse; Windows `Local State` migration | `DesktopUserData.ts` L34 | separate profile; migrations disabled |
| CLI shim environment (`T3CODE_HOME` passthrough) | `DesktopCliShim.ts` L53 | ambient `T3CODE_HOME` ignored/overridden for CLI and children |
| Protocol registration | `ElectronProtocol.ts` L16–17 | distinct scheme; T3 handler untouched |
| Single-instance lock; local server port / endpoint discovery | inventory item | cannot attach to a running T3 |
| WSL backend paths | release-desktop.yml L377–436 | disabled in R0a |
| Anything else found | — | added to the inventory; no estimate cap |

### 4.2 Donor egress (Q-03; tests EGR-02, EGR-03)

Update feed and the manual "check for updates" action; PostHog telemetry; relay/cloud public configuration
(`apps/server/src/cloud/publicConfig.ts` L85, build-time `scripts/lib/public-config.ts` L26); relay tracing; error
reporting; reconnect paths. Disabled at entry points; provider authentication and inference routes stay enabled. Every
forbidden-sink test is paired with a positive provider control (EGR-03), so over-blocking is detected.

## 5. First-build status semantics (Q-05, FWB-01; A2-15)

| Status | Meaning | R0a accepted? |
|---|---|---|
| `FIRST_WORKING_BUILD_PASSED` | installer installs; desktop launches; terminal runs a command; worktree created; diff review works; one real provider turn completes on the declared route (Codex login or a qualified ACP agent) | **yes** |
| `FEASIBILITY_COMPLETE_WITH_FAILURES` | the build/smoke procedure ran end to end and failures are recorded with reproductions | no — Q-06 continues |
| `PARTIAL_SMOKE_NO_CREDENTIALS` | everything except the provider turn passed because no credentials were available | no |

Q-06 fixes only blockers of that minimum smoke; its effort is MEASURE (unknown until Q-05).

## 6. Claims per milestone

| Milestone | Audience / channel | Claims (each backed by a registered test) | Not claimed |
|---|---|---|---|
| R0a | founder only; local or private repository | T3 functionality runs under a separate Zain dev identity without touching T3 state (FWB-02..04); no donor-endpoint egress in the tested scenarios while a provider works (EGR-02/03); no Claude/Cursor SDK code in the package (PKG-01); artifact not public (PKG-02) | license qualification for distribution, Core authority, containment, recovery, accessibility, branding completeness |
| R0b | invited testers; access-controlled channel | R0a + license removals and packaged-closure license gate (LIC-01); user-provided Claude route (F-06, T7, T8, CC-T04); browser cookie stores not imported (BRW-AT-04/14); Supervised default, no Full access (UI-01); credentials not in settings/logs (SEC12-01); material defects fixed (F-21) | Core authority, approvals, outcomes, containment, editor |
| R0 | public repository users (unsigned; PD for signed distribution) | R0b + governance-admitted source, donor identifiers removed, keyboard/screen-reader baseline for existing surfaces, budgets measured | authority, built-in editor |
| R1 | as R0 | generated templates (21 §3) | 21 §3 "Not claimed" |

## 7. Audit of the 45 former R0 tasks — revised with Astro's assessment

Changes from revision 3.1 (others unchanged; see 14 for current rows):

| Task | Revision 3.1 | Revision 4 | Reason (Astro round 2) |
|---|---|---|---|
| B-01 | QUAL, full benchmark VM | minimal isolation folded into Q-05 (separate local Windows account); full image stays QUAL | Windows 11 Home has no Sandbox/Hyper-V |
| F-01 | admission of FWB tree | upstream manifest + overlay diff + exclusions (no KEEP-tree equality) | equality conflicts with overlays |
| F-02 | QUAL | split: F-20 early license/SDK removals (R0b) + F-02 broad strip (R0) | removals cannot follow distribution |
| F-06 | TEST | depends on F-20 (SDK-free compiled output first) | A2-01 |
| F-11 | TEST | depends on F-20; access-controlled channel only | A2-02 |
| F-12 | QUAL | split: Q-06 boot blockers (R0a), F-21 material tester defects (R0b), F-12 remaining (R0) | early blockers cannot wait |
| F-13 | 0 (folded) | reinstated as named seam-walkthrough budget, 1–2 pw, R1, prerequisite of C-01 | learning is not free |
| F-14 | QUAL | existing surfaces only; Inbox/approvals A11Y-04 in R1 | A2-06 |
| F-17 | R1 | wording fixed (no "real IDE" claim for R0) | stale text |
| F-18 | R1 | split: F-22 tester credential handling (R0b) + F-18 Tauri retirement (R1) | credentials cannot be waived for testers |
| Q-tasks | T1 | T2; Q-00 admission record added; Q-06 fix-to-pass added | A2-03 |

## 8. Preservation check

T3 (R0a onward), Orca ports (R3), OCR engine lane + Continue rule import (R3; delegated review R1), PStack + E2E (R2), Plan
Mode with AI Hero skills (R0 label; R2 enforced + skills), Zain Browser (R0b hardening; R1 agents disabled; R2 lanes), DeskGate
(R2/R3/R7), Trusted Core (R1), Project Brain (R2), WSL backend (re-enabled in qualified R0), Claude feature coverage (03F labels
across R0–R7). Nothing was deleted.

## 9. Astro Round-3 build-start correction (2026-11-02)

This document's exact R0a execution authority, chosen Windows CLI SEA path, local-only policy, source-admission gates and all nine Round-3 findings are tracked in OPUS_R0A_BUILD_EXECUTION_2026-11-02.md. A3-05 and A3-06 are mandatory pre-Q-04/pre-Q-01 respectively. A3-01/02/03/04/07/08/09 remain gated in their stated later tiers; a passing R0a installer cannot be called R1 approved.
