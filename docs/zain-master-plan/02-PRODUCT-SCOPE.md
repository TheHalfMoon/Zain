# 02 — Product Vision and Scope

```text
PRODUCT  = Zain — a private, local-first, Windows-first AI-native desktop development environment
VISION   = V3 product statement (ZAIN_V3_MASTER_PLAN.md §1), unchanged
NEW HERE = a defined first release (R0b, DEC-07), the six pillars mapped to owners, and the gaps Zain can own (03 §3)
SOURCE   = registry/zain-capability-matrix.csv (59 rows; every row maps to tasks and, for early releases, a gate)
```

## 1. What Zain is

Zain is a desktop workbench where the developer and any model or agent work on real code. Zain decides which
**mediated** effects are allowed, records what happened (including outcomes it could not observe), remembers the
project across models, and decides what counts as done, while stating exactly what it could not observe.

Zain should feel like a premium developer tool and be usable without AI. It must never claim more security than its
enforcement provides.

## 2. The six pillars and who owns them

| Pillar | What "done" means for Zain | Owner subsystems (05 §3) | First milestone with real value |
|---|---|---|---|
| A — IDE | Editor, LSP, debugging, search, git, terminal, multi-project, restore — good without AI | Application shell, Editor kernel, Workspace manager, Git engine | R0b (terminal, git, diff, external editor); R0 (search, restore verified); R1 (Monaco, local index); R3 (LSP, DAP) |
| B — AI assistance | Multi-file edits with diff review, checkpoints, plan mode, completion, inline edit, review, model choice | Agent runtime, Model gateway, Context engine, Review service | R0a (provider turn); R0 (routing, plan mode); R1 (completion, review) |
| C — Autonomous agents | Missions, parallel agents, approvals, budgets, cancellation, evidence-based completion | Agent runtime, Workflow engine, Security system | R0 (parallel worktree sessions); R1 (approvals, kill); R2 (missions, completion) |
| D — Engineering automation | Plan → implement → test → review → repair loop, E2E, PR shepherding, reports | Workflow engine, Testing engine, Observability | R2 (loop, E2E, report export); R3 (PR shepherding) |
| E — Secure desktop | Effect-time policy, ledger, ProcessHost, file gate, egress control, sandbox, secrets, kill switch | Security system, Tool execution broker, Browser | R0b (no telemetry, keyring); R1 (Trusted Core); R2 (egress proxy); R5 or R2 per DEC-06 (OS sandbox) |
| F — Product design | Own design language, accessibility, onboarding, approvals and diff UX, empty/error states | UI architecture | R0 (design language v1, a11y baseline) |

## 3. Release definitions

V3 defines R0a through R7. This plan keeps that ladder and adds **M0** (privacy and repository control) in front of
it. It also names the **first release**: R0b (DEC-07, founder decision required).

| Milestone | Name | What the founder can do at exit | Claims allowed |
|---|---|---|---|
| M0 | Privacy and repository control | Nothing new in the product; repository private, reviewer route chosen, decisions signed | None |
| R0a | First Working Build | Install a locally built, unsigned Zain installer in an isolated account; run one real provider turn; terminal, worktree and diff work | "Feasibility build; not for use" |
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

## 5. Gaps Zain can own

These come from the 2026-11-08 competitor update (03 §3). Each is backed by evidence there.

| Gap | Why competitors leave it open | Zain plan |
|---|---|---|
| A native Windows sandbox that is on by default and works with real toolchains | Only Codex ships one on by default; VS Code's is experimental and off; Cursor routes through WSL2; Claude Code, Devin and Factory are unsandboxed on native Windows | ProcessHost (C-25) in R1; OS sandbox S-01 (DEC-06) |
| Local models on every surface, including completion | Copilot, Cursor and JetBrains do not allow local models for inline completion; JetBrains says agents cannot use local models | Z-11 routing, Z-12 local completion |
| One policy layer over every hosted agent | Hosts of ACP agents keep each agent's own permissions | Trusted Core PDP (C-02..C-09) |
| Honest rollback | Checkpoints elsewhere restore files only; shell side effects are not tracked | Z-27 quarantine; coverage model says UNKNOWN for shells (C-23) |
| An auditable log of outbound traffic | No product offers a per-agent default-deny proxy with a viewable log | F-05, Y-10, S-04 |
| Cost control independent of vendor quotas | Users report quota lockouts and cost jumps across vendors | Z-11 per-route budgets |
| Portable, open project state | Roo Code shut down, Continue went read-only, Windsurf was renamed | Brain (M-03), skills/MCP import (V-05, V-06) |
| A local-only code index | Copilot's semantic search needs GitHub; JetBrains Air Context is cloud embeddings | Z-28 |

## 6. Non-goals

- A public release, website, package publishing or telemetry before explicit founder authorization.
- Hosted Zain services. The optional runner (R7) is self-hosted.
- Reusing GPL code (Zed crates), the proprietary Remote Desktop Commander relay, or Amp code.
- A Code-OSS fork, unless Z-20's measured spike justifies reopening ADR-001.
- Claims of security, sandboxing or trust beyond what a passing enforcement test proves.
