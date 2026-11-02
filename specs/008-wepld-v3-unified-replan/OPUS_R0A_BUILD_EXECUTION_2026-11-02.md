# Zain V3 — Opus build-ready execution plan (2026-11-02)

## Executive decision and scope

FOUNDER DIRECTION: Stop open-ended replanning and begin the bounded founder-only R0a feasibility build, subject to the concrete admission and environment checks below. No R1 trust or release claims follow from this authorization.

PLAN STATUS: R0a build work order ready to execute starting with Q-00. The application itself is NOT built or tested by this document. R0b and Qualified R0 retain conditional gates; R1 remains NOT APPROVED until its listed design and runtime blockers pass. Copy First remains the approach.

SOURCE PIN: pingdotgg/t3code commit 36d4d711b79c73eb33131944f73ea4a8c6156484. Do not rewrite Electron, UI, terminal, diff, worktree or orchestration components already provided.

REPOSITORY POLICY: TheHalfMoon/Zain is PUBLIC. This documentation branch may contain only nonsensitive planning text. Use a separate LOCAL Windows working copy and local build/first-working branch for Q-01 onward. Do not push donor transplant, compiled source trees, installers, ASAR/SEA, package-content scans or sensitive logs to public Zain, create a PR, merge to main, or distribute. A future private build repository requires verified access and zero-cost billing controls before any transfer.

## A. Immediate Opus entry gates

A2 founder approval: this instruction is authorization to begin the limited R0a work order, not permission to bypass third-party licenses or use cloud credentials.

A3 independently reviewed Q-00: exact source pin/tree/lockfile, legal-use decisions covering all packaged/native dependencies and assets, SDK exclusion list, toolchain manifest and choice of review provider. Missing legal authorization means stop that import.

A4 execution route: LOCAL_ONLY on founder Windows x64 as default; no GitHub-hosted compute, no paid runners or third-party uploads without a separate verified private account access/spend/retention decision. Record available disk and RAM before importing. Insufficient local capacity = RESOURCE_BLOCKED, not a reason to silently enable hosted billing.

A5 test isolation: use a separate local Windows user account, distinct home/profile with no real T3 state or tokens. Use only synthetic T3 coexistence fixtures. Windows 11 Home is not Windows Sandbox or an arbitrary-provider OS confinement guarantee.

A6 model route: choose one consented real retained provider (founder's Codex login or named approved ACP). No token harvesting or subscription-credential reuse outside the provider's approved login path. Missing credentials = PROVIDER_BLOCKED or PARTIAL_SMOKE_NO_CREDENTIALS, not PASS.

A7 reviewer: name a reviewer independent of the builder for the T2 Q-00..Q-06 evidence. Own validator/test execution is not independent review. If unavailable record REVIEW_BLOCKED while proceeding with safe read-only inventory only.

No condition A3–A7 is asserted complete by this document. Opus may begin Q-00 evidence-gathering immediately; begin Q-01 source import only after all are evidenced.

## B. Concrete Windows build route — choose this path, do not leave the DAG ambiguous

1. Pin Node 26.12.1, pnpm 12.14.0 and the exact frozen donor lockfile; inventory/pin Rust MSVC, Visual Studio C++ Build Tools, Windows SDK, Python/node-gyp, CLI and native resource inputs. Record tool availability and hashes before installation. Native Windows x64 is the selected route; do not substitute a Linux cargo-xwin build without a separately reviewed change.
2. Import exact T3 source under local build/first-working and verify the unchanged donor baseline before overlays.
3. Apply Q-02 identity isolation: Zain app home, Electron dev/prod userData, old profile migrations, CLI/child environment, protocol/singleton, local server/port discovery. No T3 profile reads/writes or connection to an installed T3. Test with synthetic T3 profiles.
4. Apply Q-03 egress controls: disable donor update feed and manual updater, PostHog, relay/cloud public config, relay tracing, error telemetry and reconnect donor endpoints. Preserve intentional provider auth/inference and reconnect. EGR-02 donor-sink silence must be paired with EGR-03 real provider success.
5. Sanitize source BEFORE compiling: disable Claude and Cursor in both BUILT_IN_DRIVERS and BUILT_IN_USAGE_DRIVERS, all indirect imports, adapter/runtime imports and independently bundled entrypoints. Removing packages after bundling is not sufficient. Remove donor-owned repo guards, task-cache token dependency, relay-public-config/tracing, signing and publish steps.
6. Retain, sanitize and BUILD the independent Windows CLI SEA/archive path, including its own server bundle and resource monitor. The donor Windows verify job consumes that output. If this route proves impossible, record BUILD_ROUTE_BLOCKED and submit a narrowly specified Q-04 alternative that excludes the SEA/archive and positively verifies the desktop's actual shipped CLI path; no silent omission.
7. Disable WSL backend for R0a in code/config/subprocess environment and package options. Clear environment fallback T3CODE_DESKTOP_WSL_RUNTIME as well as omitting the --wsl-runtime argument. Never modify the founder's WSL VHDX in this experiment.
8. Build sanitized JS, same-architecture native modules/monitor and an UNSIGNED Windows x64 NSIS installer. Never copy architecture-mismatched cached outputs. Keep all binaries and intermediate content LOCAL.
9. Inspect the FINAL artifact bound to its SHA-256: ASAR, nested archives, Windows SEA executable payload, loose/unpacked native assets, notices and transitive license closure. PKG-01 must show excluded SDK code absent from EVERY shipped root. PKG-02 verifies no public artifact or packaged-content log.
10. Install and smoke in isolated account: desktop launches, terminal command executes, worktree creates, diff review works, one real declared-provider turn completes. Record FWB-01..04, EGR-02/03, CI-02, SRC-02, LIC-02 and PKG-01/02 against the SAME final installer and overlay revision.

Cold-cache recording: command, source pin/tree, overlay revision, toolchain lock versions, dependency/license admission, per-node exit code, wall time, peak RAM/disk, installer SHA, network trace conclusions and provider success. Before moving to another step, identify the exact independent reviewer and evidence. Any changed overlay/repackaged artifact invalidates earlier affected checks.

Hard STOP: donor secret required, paid compute, unauthorized source/license, public packaged content, embedded excluded SDK, T3-state access, forbidden donor egress, or failure to achieve provider-positive control. A reproducible failure is a valid feasibility measurement but not a passing build.

## C. Tasks, deliverables and pass criteria

| ID | Opus deliverable | Release gate |
|---|---|---|
| Q-00 | Source/toolchain/license admission and independently reviewed local capacity/route report | A3–A7 evidenced |
| Q-01 | Exact pinned donor tree imported locally with verified hashes | SRC-02 |
| Q-02 | Zain identity/namespace/coexistence inventory and overlay | FWB-02..04 |
| Q-03 | Donor-egress removal with legitimate-provider-positive control | EGR-02/03 |
| Q-04 | Complete Windows x64 JS + CLI SEA + native + unsigned NSIS graph; SDK-free package provenance | CI-02, PKG-01/02 |
| Q-05 | Installed local app + terminal + worktree + diff + real provider turn and measurements | FWB-01 + all packet exit tests |
| Q-06 | Fix measured minimum-smoke blockers, repack and rerun affected tests | FIRST_WORKING_BUILD_PASSED only on real pass |

Allowed statuses: FIRST_WORKING_BUILD_PASSED; FEASIBILITY_COMPLETE_WITH_FAILURES; PARTIAL_SMOKE_NO_CREDENTIALS; ADMISSION_BLOCKED; ISOLATION_BLOCKED; PROVIDER_BLOCKED; REVIEW_BLOCKED; RESOURCE_BLOCKED; BUILD_ROUTE_BLOCKED. Do not label missing tests as success or treat a packaging job as a working build.

No R0a artifact may be distributed. Before R0b tester distribution: R0a PASS plus F-20 legal/removal closure, F-21 material tester defects, F-22 credential gate, LIC-01 and shipped notices, F-05/F-07/Y-00 and all required tests; only named access-controlled recipients.

Qualified R0 adds F-01/G-03/G-05/G-08 governance/admission, old governance-negative oracles preserved, accessibility/kept-suite tests, true budget measurements, corrected structural plan validation and WSL restoration qualification. Still no Trusted Core or trusted recovery claim.

## D. Astro Round-3 closure without halting R0a

| Finding | Action and owner lane | Gate |
|---|---|---|
| A3-01 validator fail-open | Planning/validator lane: strict section-specific schema; reject malformed/duplicate task, requirement, suite, release rows; unknown IDs, invalid phases, empty suites, incomplete BEGIN/END pair, nonfinite/reversed estimates, structured expression bypasses. Permanently add Round-3 adversarial cases, assert the precise failure after ordinary regeneration. | Required before Qualified R0 |
| A3-02 / original C-1 | Trusted-plan lane: split COV-08/COV-09 R1 scope-policy units from V-04 R2 mission completion integrations; adjust oracle and dependencies with no C-23/V-04 cycle; make C-28 effective ancestor of R1 exit X-01; enforce exit prerequisite closure. | Before R1 planning approval |
| A3-03 outcome reconciliation | R1 trust lane: ambiguous move/delete/remote merge stays UNKNOWN; current object identity and changeable branch SHA are not operation receipts; add move-back ABA, merge-head ABA, same-credential other actor and missing receipt tests. | Before trusted operations |
| A3-04 Windows replacement | R1 filesystem lane: precise API access/share flags and handle lifetime; normal successful replace PLUS swap/hardlink/ADS/ancestor/name-alias adversarial tests. Refuse confined replacement if atomic protocol unproven. | Before confined filesystem claim |
| A3-05 incomplete DAG/SDK roots | Q-00/Q-04 owner: native Windows path, Windows CLI SEA and ALL usage-reader/runtime import roots, provenance scan and explicit WSL env disablement. | BEFORE Q-04 / R0a PASS |
| A3-06 no-cost control | Q-00 owner: LOCAL_ONLY; no hosted fallback; optional future private repo must verify billing/collaborators/retention/quotas before use. | BEFORE Q-01 |
| A3-07 confidential reviewer | R1 review lane: exact SDK tools/settings/history/MCP/plugin/environment/options allowlist; authenticated broker-only; initial/pretool and reconnect request payload decoy oracle without storing raw secrets. | Before confidential-review claim |
| A3-08 browser overclaim | R1 browser lane: agent-principal deny for all Zain MCP, RPC, alias, HTML preview and token issuance paths, including explicit overrides. Manual preview preserved; approved shell descendants excluded from guarantee. | Before R1 browser claim |
| A3-09 WSL and Continue | Qualified R0: add named WSL restored sanitized Linux CLI + overlay parity + positive provider startup smoke/test and revised estimate. R3: map Continue importer to K-10/ZCR-T03, not stale K-04. | Before respective tier |

Do not start another unbounded global plan review. A failed gate triggers a targeted correction, controlled retest and independent signoff. R1 remains DO NOT APPROVE until the required design and runtime evidence exist; this is NOT a hold on Q-00..Q-06.

## E. Instructions to Opus — execute autonomously within gates

1. Read the exact reviewed V3 catalog, R0A_FEASIBILITY_READINESS.md, 24_FIRST_WORKING_BUILD.md and this packet; use the latter to resolve the Round-3 build route and stop semantics.
2. Begin Q-00 immediately (read-only admission and resource check); document founder direction as A2. Record A3–A7 independently with real evidence; if absent, stop source import and work on other safe inventories.
3. Use LOCAL_ONLY and a local build/first-working branch. No PR, main merge, hosted run, releases, billing, binary uploads or public code import under this authorization.
4. Then implement Q-01..Q-06, preserving T3's working features through Copy First. Test every gate on the final artifact, not a proxy mock. Fix and rerun within the same bounded R0a scope.
5. Maintain a checkpoint record after each stage: commit/tree/installer SHA, tests/status, review evidence, time/RAM/disk cost, remaining blocker. Proceed without asking for routine "continue" approvals, but do NOT bypass a stop gate.
6. Start parallel A3-01/02 and A3-09 planning repairs only as independent bounded tasks; they must not delay admitted R0a experimentation.

End of executable R0a plan. It is a work order, not an assertion that any installer exists or that R1 architecture is approved.
