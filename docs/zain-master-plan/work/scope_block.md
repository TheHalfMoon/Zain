| **R0b** | **First release — founder daily driver and private tester build** | Use Zain every day for real work: multi-provider agents (official logins) in worktrees, diff review with per-hunk accept/reject, revert that quarantines instead of deleting, terminal (PowerShell, Git Bash, `wsl.exe` as a shell), external editor at file:line, no telemetry, keyring-only credentials, supervised default, clean install and uninstall; give the build to named private testers | "Private build; agent actions are **not** policy-enforced; no injection control beyond supervised prompts" |
| R0 | Zain 1.0 — qualified | Full Zain identity and design language, capability- and data-class-routed models with local endpoints, crash-recovery verification, WSL backend, governance reset, journeys J02–J22 verified, user documentation, 10 days of daily-use evidence | Same as R0b |
| R1 | Zain Trusted Starter | Trusted Core decides enumerated provider operations; Core-owned approvals; ProcessHost; file gate; Monaco editor; local completion; local code index | Generated, bounded claim templates only (V3 21 §3) |
| R2 | v1 workflows | Missions, Brain, enforced plan mode, engineering loop, E2E, browser lanes with egress proxy, DeskGate, execution report export | Per generated templates |
| R3–R7 | Breadth | IDE breadth (LSP, DAP), review engine, design studio, OS sandbox, general agent work, remote runner | Per generated templates |

**Why R0b is the first release (DEC-07, changed after review).** Cumulative known effort is about 10.6–20.1 pw to
R0b, 26.3–47.9 pw to R0 and 76.4–123.6 pw to R1 (10 §2). R0 adds governance reset, full rebrand, design language,
the model gateway and 13 scripted journeys. Those are worth doing, but none is needed for the founder to start
using the workbench. The independent scope review showed that putting them in front of daily use repeats the
project's main failure mode (RK-03, RK-04). R0b gets a usable, honest tool into daily use first. R0 then qualifies it
using evidence from that use (Z-32).

## 4. First-release scope (R0b) in detail

**In scope** (mapped in the capability matrix with gates):

- Locally built, unsigned NSIS installer with clean uninstall; Zain namespace isolated from any T3 install (CAP-01,
  CAP-54; Q-02, F-11, Z-22)
- Multi-provider agent sessions through official logins (Codex by default) and ACP; parallel sessions in worktrees
  (CAP-16, CAP-29). OpenCode and Pi are disabled or labelled "unsupervised" until C-24 (GATE-SEC-01)
- Terminal with PowerShell and Git Bash, plus `wsl.exe` as a shell (the T3 WSL backend returns in R0) (CAP-10)
- Diff review with per-file and per-hunk accept/reject (Z-31); per-turn checkpoints with quarantine-first revert
  (Z-27) (CAP-20, CAP-21)
- Open in external editor at file:line, with safe launching (Z-13, CAP-03)
- No telemetry and no donor egress; credentials only in the OS keyring or the provider's own CLI login (CAP-48,
  CAP-46)
- Supervised default with Full access removed (F-07)
- Browser preview hardening (Y-00)
- Measured performance baseline (Z-14) and the minimal journey harness (Z-30)

**Added in R0 (Zain 1.0 qualified):** full rebrand and identity (F-03, N-02, N-03), design language (Z-17),
accessibility pass (F-14), model gateway with local endpoints and data classes (Z-11), crash-recovery verification
(Z-21), WSL backend (Z-33), update feed (F-04, DEC-15), governance reset (G-03, G-05, G-08), journeys J02–J22 (Z-15),
user documentation (Z-34), daily-use evidence (Z-32), V3 validator repair (Z-26).

**Later:** Monaco editor, local completion and inline edit, local code index (R1); Trusted Core authority and
approvals (R1); LSP and DAP (R3, or R1 per DEC-05); missions, Brain, engineering loop, browser lanes, DeskGate (R2);
design studio (R4); OS sandbox (R5, or R2 per DEC-06); computer use (R6); remote runner (R7); code signing (optional
paid track).

