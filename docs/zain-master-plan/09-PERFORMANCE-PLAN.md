# 09 — Performance Plan

```text
PRINCIPLE = targets come from measurements on the founder's machine against the upstream T3 release build, not from
            competitor marketing; every threshold below marked PROVISIONAL is replaced by Z-14's measured numbers
BASELINE  = V3 09 §3 benchmarks B1–B14 and budgets NF-01..NF-08 (F-15, C-21) remain; this plan adds hardware binding
```

## 1. Reference machine (measured 2026-11-08)

| Item | Value |
|---|---|
| CPU | Intel Core i5-13420H, 8 cores / 12 threads |
| Memory | 15.7 GB |
| GPU | Intel UHD Graphics (integrated) |
| Storage | C: 200 GB (3.4 GB free), D: 257 GB (20 GB free); NVMe model not recorded |
| OS | Windows 11 Home 10.0.26300 |
| Toolchain present | Node 24.19.0, pnpm 9.12.0, Rust 1.97.1 MSVC, VS Build Tools 2022, Windows SDK 10.0.26100, Python 3.14.7 |

Measurement conditions for every benchmark: AC power, no other build running, 5 runs, report median and p95, record
free RAM before each run. Background `cargo build --release` jobs from other projects were running on this machine
during the audit; Z-14 must check for and record such contention.

## 2. Metrics and thresholds

| Gate | Metric | Method | Threshold | Status |
|---|---|---|---|---|
| GATE-PERF-01 | Cold start to interactive window | Reboot-free cold start: kill all Zain processes, clear OS file cache where possible, launch, wait for first interactive frame | ≤ 1.10 × donor baseline and ≤ 6 s | PROVISIONAL |
| GATE-PERF-02 | Warm start | Relaunch within 60 s | ≤ 1.10 × donor baseline and ≤ 3 s | PROVISIONAL |
| GATE-PERF-03 | Idle memory, one project open | Sum of working sets of all Zain processes after 5 min idle | ≤ 1.15 × donor baseline and ≤ 1.2 GB | PROVISIONAL |
| GATE-PERF-04 | Terminal open | Median of 10 opens to prompt | ≤ 700 ms | PROVISIONAL |
| GATE-PERF-05 | Large repository | 50k-file fixture: open to interactive; git status refresh | open ≤ 5 s; status ≤ 2 s | PROVISIONAL |
| GATE-PERF-07 | Local completion | 20 prompts × 5 runs with a local FIM model | p50 ≤ 600 ms to first suggestion, else lane off by default | PROVISIONAL |
| GATE-CTX-01 | Local index | 50k-file fixture: initial build, incremental update, query | initial ≤ 10 min CPU-only; update ≤ 2 s; query ≤ 300 ms | PROVISIONAL |
| V3 C-21 / B13 | Effect overhead through the Core | p95 per mediated effect | ≤ 25 ms (V3 NF-04) | V3 budget |
| V3 F-15 / B1–B3 | Offline and startup budgets | V3 09 §3 | V3 NF-01..03 | V3 budget |

**Why these provisional numbers.** The ratios against the upstream release build (1.10× and 1.15×) bound Zain's
added cost, since a fork should not be much slower than its donor. The absolute ceilings are deliberately loose for a
16 GB laptop with an integrated GPU. **Final thresholds** are min(absolute ceiling, upstream median × ratio), set from
Z-14's measurements and approved by the founder, so no gate can pass itself. The 50k-file fixture is a pinned commit
of a large public repository recorded in Z-14. The local completion model and quantization are named in Z-12.

## 3. Additional measurements without gates (tracked for regressions)

| Measurement | Why |
|---|---|
| Agent-turn overhead excluding model time | Shows the cost of orchestration, checkpoints and (from R1) Core mediation |
| Diff render for 5k changed lines | Diff review is a core journey |
| Checkpoint capture and restore time on the 50k-file fixture | Revert must stay usable on large repositories |
| Memory after 8 h of agent activity | Long-running stability |
| Shutdown time and orphaned processes after quit | Child-process cleanup (ProcessHost from R1) |
| Installer size, install time and uninstall residue | J01, GATE-PKG-02 |
| Cold build wall time, peak RAM and disk for Q-04 | Feeds GATE-RES-01's measured threshold |

## 4. Real desktop tests, not mocks

Every performance and journey test runs against the installed NSIS build in the isolated account (Z-09), driven by
Playwright for Electron or OS-level scripts. Component-level microbenchmarks may supplement these tests but cannot
replace them. Results are stored as CSV with the installer SHA-256 and the machine description.
