# 20 — R0a Pre-Admission Record (V3 Q-00), draft for review

```text
DATE     = 2026-11-08
TASK     = V3 Q-00 (tier T2): source pin and digests, overlay scope, LOCAL_ONLY Windows route, capacity and cost=0
           controls, toolchain pins, frozen-lockfile policy, CLI archive route, shipped-closure license listing,
           decisions for heic-to / electron-webauthn / Claude SDK / Cursor SDK
STATUS   = REVIEW_BLOCKED: drafted by the builder; T2 needs the founder's sign-off (DEC-01). Q-01 is also
           RESOURCE_BLOCKED (§4)
METHOD   = read-only GitHub API, npm registry and local version checks; scripts and outputs in work/q00_*
```

## 1. Source pin and digests (DEC-04)

| Item | Value | Evidence |
|---|---|---|
| Repository | `pingdotgg/t3code`, MIT | 04 §1 |
| Pin | tag `v0.1.7` (lightweight) = commit `322f6544dfad0a3c8a0c8cbecf2c7f7874b14268`, 2026-11-04T00:41:08Z | `gh api …/git/refs/tags/v0.1.7` |
| Tree | `c18fd951fa853b3b317dea886dddf3fd48a915a5` | `gh api …/commits/322f6544` |
| Replaces | `36d4d711b79c73eb33131944f73ea4a8c6156484`; v0.1.7 is 1,393 commits ahead, 0 behind | `gh api …/compare` |
| Lockfile | `pnpm-lock.yaml`, 927,338 bytes, git blob `efc7f6e902d4cccde91885fcd9b1b308e7355490`, sha256 `f3258534e27d946c417a7220c9ea9d6a4ede9d2dde6fbd796a0ae6c299cf0e84`, lockfileVersion 9.0, two documents (pnpm bootstrap, then the project: 41 importers, 2,062 packages) | `work/q00_licenses.py`, `work/q00_closure.py` |
| Upstream Windows release (for the Z-29 trial, not for the build) | `t3-0.1.7-win32-x64.zip`, 113,322,741 bytes, sha256 `ebbe1f42b774c1492039f7d3f0b0e9572926b16f887c94574eff4644549cd15a` | release `SHA256SUMS` |

**R11 deltas.** Between the two pins the tree changed widely (old 28,763 files, new 31,539; 5,395 changed). Of the
156 paths named in the V3 R11 manifest, 55 are unchanged, 93 changed, 1 was removed or moved
(`apps/server/src/checkpointing/Utils.ts`), and 7 match no file at either pin (probably extraction noise).
Per-path results: `work/q00_r11_delta.csv`.

## 2. Toolchain pins

| Tool | Pin (source) | Installed now | Gap |
|---|---|---|---|
| Node | 26.12.1 (`engines.node`) | 24.19.0 | Z-08 |
| pnpm | 12.14.0 (`packageManager`) | 9.12.0 (global npm install) | Z-08 |
| Rust | Upstream uses unpinned `stable` (`dtolnay/rust-toolchain`). Proposed local pin: 1.97.1, the current `stable` here; 1.98.0 and 1.98.1 are also installed | rustup: stable 1.97.1 (active), 1.98.0, 1.98.1 | Founder confirms the pin |
| MSVC | Visual Studio Build Tools 2022 | 17.14.37710.0 | none known |
| Windows SDK | — | 10.0.26100.0 | none known |
| Python (node-gyp) | — | 3.14.7 | Confirm at Q-04 |
| WSL | needed only for the embedded Linux CLI archive | no distribution registered | §3 |

## 3. Build route, overlay scope and cost controls

- **LOCAL_ONLY** on the founder's Windows 11 x64 machine. No GitHub-hosted or paid runners: upstream's release uses
  Blacksmith runners and Azure Trusted Signing, and both are excluded. The build is unsigned (Z-22). Cost = 0.
- **Frozen install:** `pnpm install --frozen-lockfile` with pnpm 12.14.0 against the lockfile digest in §1.
  `.pnpmfile.cjs` (27 lines) runs during install with `readPackage` and `updateConfig` hooks; it has no network or
  process calls. Upstream carries 33 patches in `patches/`. Both are reviewed at Q-01.
- **Native code on Windows:** `native/resource-monitor` (Rust) builds with MSVC. `kde-snap-shot`,
  `hyprland-snap-shot` and `browser-secret` (libsecret) are Linux-only and are not built. `libghostty-vt` ships
  headers with its own LICENSE.
- **CLI archive route.** Upstream's Windows build embeds the Linux CLI archive, built on Linux, for the WSL backend.
  No WSL distribution exists here. **Proposed:** R0a builds the Windows CLI single-executable or archive path as V3
  requires, and omits the embedded Linux archive. The WSL backend stays disabled until Z-33 restores it at R0. The
  alternative, installing a WSL distribution, is a system change for the founder to approve.
- **Overlay scope (V3):** Q-01 imports as-is with no strip or rename. Before compiling, the Claude and Cursor drivers
  are disabled in `BUILT_IN_DRIVERS` and `BUILT_IN_USAGE_DRIVERS` and their imports removed (§5). No rewrite of the
  Electron, UI, terminal, diff, worktree or orchestration components.

## 4. Capacity (GATE-RES-01)

| Resource | Need | Now | State |
|---|---|---|---|
| Disk on the build volume D: (DEC-12) | at least 30 GB (provisional) | 16.5 GB | **RESOURCE_BLOCKED** (Z-07, founder frees D:) |
| Free RAM | at least 6 GB | 1.6 GB of 15.7 GB, while other builds run | **RESOURCE_BLOCKED** until those builds stop |
| CPU | — | 12 logical processors | — |

## 5. Shipped-closure license listing (LIC-02, pre-build)

The production closure (dependencies and optional dependencies, transitively) of `apps/desktop`, `apps/server` and
`apps/web`, following 29 workspace packages, has **860 packages** (`work/q00_license_listing.csv`). Licenses are from
the npm registry at each exact version; where npm has none, from the source repository's LICENSE. Upstream's
`third-party-licenses/spdx/v3.28.0` carries texts for 8 licenses (Apache-2.0, BSD-2-Clause, BSD-3-Clause, CC0-1.0,
ISC, MIT, OFL-1.1, Unlicense); 830 packages fall inside that set.

| Packages outside the set | License | Proposed decision |
|---|---|---|
| `@anthropic-ai/claude-agent-sdk@0.3.284` | proprietary ("SEE LICENSE IN README.md") | **Exclude** before compile (V3 sanitize step; DEC-14 makes Claude optional) |
| `@cursor/sdk@1.2.0` and 5 platform packages | proprietary ("SEE LICENSE IN LICENSE.md") | **Exclude** before compile (V3 sanitize step) |
| `heic-to@1.5.2` | LGPL-3.0 (bundled libheif build) | **Exclude for R0a**: HEIC image paste is a convenience, and LGPL compliance needs a relink or source offer |
| `electron-webauthn@1.3.1`, `@electron-webauthn/macos@1.3.1` | MIT (repository LICENSE; npm metadata empty) | **Keep**: the native part is macOS-only and absent on Windows |
| `@electron-webauthn/types@1.3.1`, `jsbi@2.0.5` | none in npm metadata and no repository link | **Check the package tarball LICENSE at Q-01**; exclude if none |
| `objc-js@1.5.0`, `map-stream@0.1.0`, `@react-grab/cli@0.1.44` | MIT (repository LICENSE) | Keep; objc-js is macOS-only |
| `tslib@2.8.1`, `jsc-safe-url@0.2.4` (0BSD); `sax@1.6.1` (BlueOak-1.0.0); `pako@1.0.11` (MIT AND Zlib); `argparse@2.0.1` (Python-2.0); `caniuse-lite` (CC-BY-4.0, data); `@nornagon/put@0.0.8` (MIT/X11); 6 `@pierre/*` (apache-2.0, lower case) | permissive | Keep; add the missing license texts to the notices |
| aliases `micromark-extension-math` → `micromark-extension-llm-math@3.1.0`, `typescript` → `@tsc-rs/typescript@0.8.0` | MIT; MIT AND Apache-2.0 | Keep |

This listing is pre-build. LIC-02 passes only when Q-04 checks the packaged output against it.

## 6. A3–A7 conditions

| Condition | State |
|---|---|
| A3 Q-00 independently reviewed | **Not yet**: this record awaits the founder's T2 sign-off (DEC-01); OCR may give an advisory pass after Z-06 |
| A4 LOCAL_ONLY route and capacity recorded | Recorded (§3, §4); capacity is below threshold |
| A5 isolated Windows account | Not created (Z-09) |
| A6 consented provider route | DEC-08 chose the official Codex login; not yet verified (Z-10) |
| A7 reviewer named | The founder, for T2 |

## 7. Still open inside Q-00

1. Re-run the R02 §10 seam inventory at the new pin, and re-check the V3 18 file:line citations against the 93
   changed and 1 moved R11 paths.
2. The founder's decisions on §5 (four special packages) and on the CLI archive route (§3).
3. The Rust pin (§2).
