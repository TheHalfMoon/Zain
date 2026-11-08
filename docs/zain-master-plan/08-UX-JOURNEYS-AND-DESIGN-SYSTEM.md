# 08 — User Journeys and Design System

```text
JOURNEYS = registry/zain-ux-journeys.csv (22: the 20 required plus terminal and search, added after review); each has a JOURNEY gate in registry/zain-acceptance-gates.csv
UX BASE  = V3 07 §7 information architecture (5 destinations + trust indicator); donor UI from T3 (React 19, Tailwind 4)
TESTS    = Z-15 (R0 journeys), Z-16 (R1 journeys); later journeys verified by their component suites
```

## 1. Journeys

"First" is the milestone where the journey must work end to end. "Full" is where its complete form lands. Every
journey is tested on the **installed** build in the isolated account, with a happy path and the listed failure path.

| ID | Journey | First → full | Entry point | Key states | Backend | Permissions | Failure → recovery | Verifying tasks |
|---|---|---|---|---|---|---|---|---|
| J01 | Install and launch | R0b → R0 | Unsigned NSIS; SmartScreen "More info → Run anyway" documented | Installing, first launch, onboarding | Installer, protocol and AUMID registration | User-level install | Partial install leaves no registration; rerun idempotent | Q-04, Q-05, F-11, Z-22 |
| J02 | Create or open a project | R0 | Home: Open folder / Clone / New | Empty, loading, ready, not-a-repo | Project registry, git topology | Folder read | Non-git folder: offer `git init`, never automatic | F-16, Z-15 |
| J03 | Configure a local or authorized model | R0 → R1 | Onboarding or Settings → Models | Probing, capability table, data-class choice | Gateway probes | Founder marks data classes | Failed probe shows which capability; route disabled | Z-11, F-22, B-06 |
| J04 | Start an AI coding conversation | R0a | Project → New thread | Streaming, tool activity, done | Provider adapter, orchestration | Supervised | Expired auth: re-login via provider CLI; turn marked failed | Q-05, F-16 |
| J05 | Multi-file modification | R0 | Prompt naming several files | Plan, edits, diff ready | Turn + checkpoint capture | Supervised writes | Provider error mid-turn: revert from pre-turn checkpoint | F-16, Z-15 |
| J06 | Review and accept/reject changes | R0b → R1 | Diff panel; open in external editor | Per-file and per-hunk states | CheckpointStore diff | — | Rejected hunks restored; external edits refresh diff | Z-13, Z-31, Z-30, K-05 |
| J07 | Create an implementation plan | R0 → R2 | Plan mode or `/plan` | Questions, plan draft, approval | Plan mode (unenforced R0) | Read-only intent (enforced R2) | R0 banner "not yet enforced"; R2 invalidates on out-of-plan writes | L-01, L-02, L-06, L-08 |
| J08 | Run an autonomous engineering task | R2 | Plan → Approve → Mission | Running, waiting (CI/human), done | Missions, continuations | Mission-scoped grants | Survives reboot; retries within budget then waits | M-01, M-02, M-07, E-01, E-07 |
| J09 | Inspect agent progress and tool actions | R0 → R1 | Thread timeline; Inbox; trust indicator | Live, completed, unknown outcome | Receipts, coverage tags | — | Unknown outcomes listed, never hidden | F-16, C-14, C-17 |
| J10 | Approve sensitive operations | R1 | A1 Core surface or A2 isolated window | Pending, approved, denied, expired | Core decision + approval | Level A1/A2/A3 (V3 17 §4.5) shown | Deny or expiry stops the effect; agent informed; no silent retry | C-13, C-14, C-15, Z-16 |
| J11 | Run and diagnose tests | R0 → R3 | Terminal; agent runs tests; later E2E lane, debugger | Running, failed, rerun | ProcessHost (R1), E2E (R2), DAP (R3) | Supervised | Runner crash keeps output; budget stops loops | F-16, E-03, I-04 |
| J12 | Create and inspect Git changes | R0 → R1 | Source control view | Staged, committed, branch, PR | VcsDriver | Destructive ops gated from R1 | Failed push leaves local state intact | F-16, C-12 |
| J13 | Resume an interrupted agent task | R0 → R2 | Relaunch after crash | Interrupted, resumed | Event replay, process-loss reconciliation | — | R0: in-flight turn marked interrupted and can be re-sent; R2: resume with a context capsule | Z-21, M-05 |
| J14 | Recover from a failed operation | R1 | Inbox → unknown outcome | APPLIED / NOT_APPLIED / UNKNOWN | Reconciliation contracts | Retry needs replay-safety | Evidence shown; retry only if replay-safe | C-26, C-20, Z-16 |
| J15 | Manage multiple projects | R0 | Sidebar switcher | Available, unavailable | Project registry | — | Missing folder marked unavailable, not deleted | Z-15 |
| J16 | Change agent or model configuration | R0 → R1 | Thread settings; role pins | Switching | Gateway, provider sessions | Data classes respected | New provider session; history kept | Z-11, F-22, V-01 |
| J17 | Control background execution | R2 | Background tasks list | Scheduled, running, paused, missed | Continuations | Mission grants | Missed-run policy; cancel any task | M-02, M-06 |
| J18 | Restore a previous checkpoint | R0b → R2 | Thread → turn → Revert | Preview, restored, quarantined files | Checkpoint restore with quarantine | Supervised | Untracked files quarantined, listed, restorable | Z-27, K-06 |
| J19 | Investigate a security event | R1 → R2 | Inbox / ledger view → event | Event detail, evidence, export | Ledger, anchors, browser evidence | — | Unanchored interval shown explicitly | C-19, C-17, Y-06, Z-16 |
| J20 | Export an engineering execution report | R2 | Thread or mission → Export | Exporting, done, redaction failure | Ledger, receipts, diffs, tests | — | Redaction failure blocks export | Z-23 |
| J21 | Use the integrated terminal | R0b → R1 | Terminal panel (PowerShell, Git Bash, `wsl.exe` as a shell) | Running, exited, killed | node-pty / ConPTY; ProcessHost from R1 | Supervised | Hung process killed from the panel; from R1 the whole job tree (WSL excluded) | Q-05, Z-30, C-25 |
| J22 | Search and navigate project files | R0 → R1 | File explorer; project search | Searching, results, no results | rg search; local index from R1 | — | Search is cancellable; ignored files excluded | F-16, Z-15, Z-28 |

**Architecture requirements the journeys exposed** (now tasks): open-in-editor for J06 before Monaco (Z-13);
non-destructive revert for J18 (Z-27); a model setup flow with probes and data classes for J03 (Z-11); crash restore
on the real installed build for J13 (Z-21); report export for J20 (Z-23); clean uninstall for J01 (Z-22).

## 2. Information architecture

V3 07 §7 defines five destinations (Projects, Work, Inbox, Brain, Settings) plus a persistent trust indicator. This
plan keeps that structure and adds three rules:

1. **Every agent action is visible where it happened.** The thread timeline shows tool calls with their outcome
   (applied, not applied, unknown) and, from R1, their approval level and coverage tag.
2. **Approvals never live in the renderer alone.** From R1 the approval content shown to the user is the Core's
   canonical binding. The renderer only mirrors it.
3. **Honest status everywhere.** Plan mode in R0 carries a "not yet enforced" banner. The trust indicator in R0
   reads "Not mediated". No green "secure" state exists before its gate passes.

## 3. Zain design language v1 (Z-17)

The goal is a calm, precise, high-density developer tool with its own identity, not a copy of the donor, Linear,
Cursor or Claude. The values below are the **starting proposal** for Z-17; Z-17 finalizes them with contrast proofs.

| Token group | Proposal | Rule |
|---|---|---|
| Brand color | Deep teal-green family as the primary hue (working name "Zain Jade"), with a warm amber accent for attention states | Brand color is never used for status; status has its own scale |
| Neutrals | 12-step cool-gray scale for light and dark themes | Text on surfaces ≥ 4.5:1; UI component borders and focus ≥ 3:1 (WCAG 2.2 AA) |
| Status | success, warning, danger, info, **unknown** (a distinct violet-gray so "unknown outcome" never looks like success or failure) | Unknown is a first-class state |
| Typography | Inter (UI) and JetBrains Mono (code), both under the SIL Open Font License; scale 12 / 13 / 14 / 16 / 20 / 24 px; code 13 px | License check at Z-17; fallback to system UI fonts |
| Spacing | 4 px base: 4, 8, 12, 16, 24, 32, 48 | Dense default; a comfortable density setting |
| Radius and elevation | Radius 4 / 6 / 10; three elevation levels as borders plus subtle shadow | No glassmorphism on content surfaces |
| Motion | 120 ms (micro), 200 ms (panels), standard ease-out; no motion on keyboard-driven actions; honors reduced-motion | Motion explains state change, never decorates |
| Iconography | One outline icon set at 16 / 20 px, 1.5 px stroke; Zain mark redrawn for the app icon, installer and tray | No donor marks in shipped UI |
| Focus | 2 px focus ring in the brand color with a 2 px offset, always visible on keyboard focus | Never removed |

**Component priorities for R0:** shell chrome and sidebar; thread and timeline; diff panel; terminal frame;
approval prompt (R0 supervised and R1 Core surface); model setup; empty, loading and error states for every journey.

**Accessibility baseline (F-14 + Z-17):** full keyboard operation, visible focus, no keyboard traps, screen-reader
labels on controls. The accessible terminal mode (I-11) arrives in R3. Contrast is verified from the token file, not
by eye.
