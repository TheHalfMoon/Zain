# 00 — Executive Summary

```text
DATE      = 2026-11-08
PRODUCT   = Zain (formerly WePLD) — private, local-first, Windows-first AI-native desktop development environment
BRANCH    = docs/zain-master-plan-20261108 (pushed after the repository was made private on 2026-11-08; no PR)
VERDICT   = CONDITIONALLY READY (see §8)
```

## A. Current Zain status (verified)

- **Repository:** `TheHalfMoon/Zain` was **public** at audit time and was made **private** on 2026-11-08 at the founder's
  direction. Its history was public before that (Z-03), and the legacy `wepld/wepld` was public until 2026-11-08T01:22:38Z (01 §2).
- **Product code:** a 10k-line Rust Core (identity, read-only git topology, evidence store, CLI) plus a Tauri status
  window that V3 retires. There is no editor, terminal, chat or agent. Governance code is 85k lines, 8.4 times the
  product code (01 §3).
- **Plan:** V3 (176 tasks, R0a–R7) selects a T3 Code fork with the Rust Core as the authority. Its validator passes
  but fails open (A3-01). Critical C-1 is open, and R1 is "do not approve". R0a has not started.
- **History mix-up:** E4–E7, FD-4 and `70458ae` belong to Ascout, not Zain. `usn-journal.csv` was not found (01 §7).
- **Machine:** C: has 3.4 GB free and D: 20 GB; 16 GB RAM; integrated GPU. Node and pnpm are below the pins. R0a is
  resource-blocked today.

## B. Target architecture

V3 ADR-001 is confirmed: a hard fork of T3 Code (Electron, Node server, React), with the Rust Trusted Core as the
single policy decision point and ledger writer, plus bounded Orca ports. It was re-evaluated against a Code-OSS fork
and kept, because of the agent-first donor, the defined authority seams and what this hardware can build. IDE parity
comes in steps: external editor (R0b), Monaco with local completion and index (R1), then LSP/DAP. Z-20 decides the
Monaco path before F-17 (05).

## C. Source strategy

ADAPT: T3 Code, Orca (Design Mode, TUI-agent catalog, Linear, computer use), Alibaba OCR (R3 engine), PStack and
cursor-team-kit, mattpocock/skills (without the `pr` skill), Desktop Commander and the Codex Windows sandbox set.
INTEGRATE: Monaco, LSP and debug clients, MCP/ACP SDKs, OpenCode, Playwright, rusqlite, Cedar, local model servers,
Excalidraw and Style Dictionary. KEEP: the Rust core crates, with the ledger and policy as new modules. REFERENCE:
Vercel Workflow, Continue, Graft, VS Code, Zed (GPL), Theia and Amp. REJECT: Roo Code and the Remote Desktop
Commander relay. 20 licenses were re-read on 2026-11-08 and 13 are recorded from V3. Pins stay at V3's values until
re-pinned through admission (DEC-04) (04).

## D. Product scope

Six pillars, with every capability mapped to tasks and gates (61 capabilities). **First release = R0b, the founder
daily driver** (DEC-07, changed after independent review). It covers official-login agents in worktrees, diff review
with per-hunk accept/reject, quarantine-first revert, terminal, external editor, no telemetry, keyring credentials,
the supervised default, and clean install/uninstall. It makes no mediation or injection-control claim. R0 qualifies
it as Zain 1.0 (identity, design, model gateway, recovery, WSL, docs, daily-use evidence). R1 adds the Trusted Core,
approvals, ProcessHost, Monaco, local completion and the local index (02).

## E. Roadmap and critical path

M0 privacy and control (parallel) → R0a first working build → **R0b first release** → R0 Zain 1.0 → R1 Trusted
Starter → R2–R7. Cumulative known effort: R0a 5.1–10.3 pw, R0b 10.6–20.1 pw, R0 26.3–47.9 pw, R1 76.4–123.6 pw,
all tiers 196–324 pw. Founder review time is extra (RK-25). Critical path to R0b:
Z-25 → Q-00 → Q-01 → Q-02 → Q-04 → F-20 → F-06 → F-11 → Z-22 (10).

## F. Major risks

7 CRITICAL, all mitigated by tasks:

- **RK-03:** scope beyond solo capacity
- **RK-01:** public repository
- **RK-04:** governance overhead
- **RK-05:** disk too small to build
- **RK-06:** CPU-only local models cannot reach agentic quality
- **RK-09:** unproven Windows containment on a Home build in the Insider range
- **RK-10:** injection leading to destructive actions

13 HIGH, including:

- **RK-14:** no authorized independent reviewer
- **RK-25:** founder review bandwidth
- **RK-13:** the V3 validator fails open
- **RK-16:** revert loses data
- **RK-17:** private code reaches unauthorized endpoints

Full list in 13.

## G. Plan validation

- `zmp.py check`: 0 errors across 7 registries (210 tasks, 440 edges, 58 gates, 61 capabilities, 42 sources, 25
  risks, 22 journeys) and the generated documents.
- Mutation suite: 35/35 seeded defects rejected with their exact error codes. During development it found 3
  validator defects, and review found 2 more; all are fixed.
- V3 `plan_graph.py --check`: exit 0.
- Four EGM independent review passes produced 80 findings: 72 fixed, 3 partial, 3 turned into founder decisions and
  2 rejected with reasons (14). EGM is Claude-family, so GATE-REV-01 (non-Claude review) is **not** met.

## H. Readiness verdict: CONDITIONALLY READY

**Ready now:** M0, plus the read-only agent task Z-18 (Z-03 is done, unreviewed).

**Not ready for R0a build work until:**

1. Founder decisions: **done**. The founder decided DEC-01..DEC-16 on 2026-11-08 (13 §2).
2. The reviewer route authorized by DEC-01 is qualified with one dry-run review (Z-06).
3. Disk capacity on D: reaches GATE-RES-01 (Z-07, DEC-12).
4. The toolchain matches the pins (Z-08).
5. The isolated account and provider route exist (Z-09, Z-10). These are needed before Q-05.

Repository privacy (Z-01) gates any push, not local building. R1 stays not approved until Z-26 fixes A3-01, A3-02
and C-1, and C-00 proves the Windows mechanisms.

## I. Exact next implementation task

- **Founder:** Z-25 (the six decisions above), Z-06 and Z-01. Each takes minutes.
- **Agent, now:** **Z-03**, the public-exposure assessment (read-only), together with Z-18.
- **First engineering unit:** **V3 Q-00**, the R0a admission record, with Z-07 and Z-08. Z-29 (a one-day trial of
  the upstream T3 release) runs alongside (16 §6).

## J. Repository evidence

- **Base:** `23bea38` (`docs/r0a-opus-start-20261102`).
- **Branch:** `docs/zain-master-plan-20261108`, local commit only (17 §5).
- **Contents:** `docs/zain-master-plan/` with 18 documents, 7 registries and 2 tools.
- **Not done:** no pull request was created, and nothing was pushed or published.
