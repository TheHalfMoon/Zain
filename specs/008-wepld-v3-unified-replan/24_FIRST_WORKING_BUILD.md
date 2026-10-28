# 24 — First Working Build vs Qualified R0 vs Trusted R1 (Copy First time-to-build analysis)

```text
STATUS = PROPOSED (planning only; nothing built or run by Zain). Founder challenge 2026-10-28: the R0 estimate of
         21.8–34.35 pw was too long for a first working desktop application built from legally copyable donor source.
RESULT = three distinct milestones, each with its own claims:
         R0a First Working Build (FWB)  — T3 as-is + two overlays; local; no claims
         R0b Tester Build               — + the minimum needed before anyone else runs it; narrow stated claims
         R0  Qualified R0 Workbench     — governance, admission, rebrand, baseline, a11y; no authority claims
         R1  Trusted Starter            — unchanged security requirements (17–19, 21 §3)
NUMBERS = generated (GENERATED_PLAN_REPORT.md §3); FWB effort is CONDITIONAL (§4) until Q-05 measures it
```

## 1. Evidence about building T3 (upstream, not measured by Zain)

| Evidence (read-only, 2026-10-28) | What it shows | What it does not show |
|---|---|---|
| `pingdotgg/t3code` releases: v0.1.3 (2026-10-27T06:09Z) and nightlies 3748…3796 (four on 2026-10-27) each ship `T3-Code-<ver>-x64.exe`, `-arm64.exe`, `win32-x64.zip` | T3's own pipeline produces Windows x64 installers from source several times a day | that the same pipeline runs unchanged on GitHub-hosted runners; that our pin builds clean |
| `.github/workflows/release.yml` @36d4d711: Windows desktop jobs build on Ubuntu runners (Blacksmith, up to 32 vCPU) with `rust_target: x86_64-pc-windows-msvc` and a `verify_runner: windows-2025` job | cross-build + Windows verification is the upstream path; a Rust component is cross-compiled | runner time on 4-vCPU free runners; secret requirements beyond signing (to be read in Q-04) |
| `.github/workflows/windows-tests.yml` @36d4d711: `blacksmith-8vcpu-windows-2025`, manual inputs (package/test files) | Windows test runs exist but are manual-dispatch, not per-PR | Windows test pass ratio at our pin |
| `package.json` @36d4d711: Node 26.12.1, pnpm 12.14.0, `vp` task runner, `dev:desktop`, `dist:desktop:artifact` → `scripts/build-desktop-artifact.ts` | local dev and packaging entry points exist | local Windows build time and disk use on the founder machine |
| R11: 28,763 blobs at pin; KEEP 4,361 / MODIFY 111 / STRIP 24,291 (21,833 `.repos/`); 1,278 kept test files | most of the tree is not needed, but nothing has to be stripped to run | — |

Zain has **no measurement of its own**. The previous R0 estimate counted building, testing, learning, stripping and
rebranding as one up-front block; it did not separate "run the donor" from "qualify the product".

## 2. Copy First time savings (explicit, reviewable)

| Reused as-is in the First Working Build | Instead of | Source |
|---|---|---|
| Entire Electron desktop app, web UI, Node server, orchestration-v2, provider adapters (Codex, ACP, OpenCode, Pi, …), terminals, git/worktrees, diff review, browser preview | building any of it | T3 @36d4d711 |
| T3's Windows packaging (`build-desktop-artifact.ts`, electron-builder NSIS config) and its release workflow job | writing packaging and CI from scratch (part of old F-11) | release.yml, scripts/ |
| T3 notices generation (`licenses:sync`) | writing a notices generator for the first build | package.json scripts |
| 1,278 kept test files as regression baseline | writing a baseline test suite | R11 §6 |
| Upstream Windows release cadence as buildability evidence | proving Windows buildability before starting | releases |

What Copy First cannot remove: the Trusted Core, governance reset, security seams, and qualification — those are Zain's
own value and keep their R1 requirements unchanged.

## 3. Shortest realistic path to a working Zain app (R0a)

| Task | Work | Why it is the minimum |
|---|---|---|
| Q-01 | import T3 @36d4d711 unmodified into isolated branch `build/first-working` | no strip/rename needed to run; branch is never merged without F-01 admission |
| Q-02 | coexistence identity overlay (display name "Zain (dev)", app id, t3Home/data dir, protocol scheme, single-instance lock) | prevents sharing state with an installed T3 — the only rename required to run safely |
| Q-03 | egress-off overlay (update feed, PostHog, Connect/Clerk/relay disabled) | stops the build updating itself to T3 or sending telemetry |
| Q-04 | copy T3's Windows x64 release job, drop signing, keep Windows verify; exclude Claude/Cursor SDK packages from the package; artifacts ≤ 1 day | reuses the upstream pipeline; avoids filling the founder's disk (a full local `pnpm install` + build needs several GB); keeps public-repo artifacts from becoming redistribution |
| Q-05 | install + smoke on the founder machine; record timings/failures | converts this plan's conditional estimate into a measurement |

Generated effort: R0a 0.9–2.6 pw (GENERATED_PLAN_REPORT §3).

## 4. Conditional estimate — conditions (all UNVERIFIED until Q-04/Q-05)

The FWB estimate holds only if:

| # | Condition | If false |
|---|---|---|
| C1 | T3's Windows job runs on GitHub-hosted Ubuntu runners after replacing Blacksmith runner labels/cache actions | fall back to local `dev:desktop` on Windows (needs VS Build Tools, Rust MSVC, Node 26, pnpm 12, several GB free disk); add 0.5–2 pw |
| C2 | the job needs no secrets other than signing ones | stub or remove the dependent step; add 0.25–1 pw |
| C3 | free-runner time fits the 6-hour job limit (upstream uses up to 32 vCPU) | split jobs or local fallback |
| C4 | identity sites are those listed in R11 §4 (t3Home definition site is UNKNOWN in R11) | locate and override; add ≤ 0.25 pw |
| C5 | founder has credentials for at least one provider (Codex login, ACP agent, or API key) | smoke limited to UI/terminal/worktrees |
| C6 | the pin builds clean (upstream nightlies imply yes for HEAD on 2026-10-27, not for 36d4d711 exactly) | move to the nearest green upstream tag; record the new pin |

**No calendar date is promised.** At A-1 (1 pw per week, unvalidated) and with C1–C6 true, R0a is a matter of weeks, not
months; if C1 fails, the local fallback adds the stated amounts. Q-05 replaces this section with measured numbers.

## 5. Claims per milestone (narrowed honestly; R1 security unchanged)

| Milestone | Who may run it | Claims | Explicitly not claimed |
|---|---|---|---|
| R0a FWB | founder only, local | none beyond "T3 behaviour under a Zain dev name; no update/telemetry egress (EGR-02)" | branding completeness, licensing review, any security/authority/recovery property; Claude provider absent |
| R0b Tester | invited testers, unsigned, working name not public (N-01) | no telemetry/update egress (EGR-01/02); Claude SDK not bundled, user-provided (T7, T8); browser preview cannot read user browser cookies (BRW-AT-04/14); default Supervised, Full access removed (UI-01); third-party notices and license gate (LIC-01) | authority, approvals, outcomes, containment, editor, accessibility, Zain branding completeness |
| R0 Qualified | public repo users (unsigned; PD for signed distribution) | R0b + governance-admitted source, donor identifiers removed, keyboard/screen-reader baseline, budgets measured | any authority claim; built-in code editor (Monaco arrives in R1) |
| R1 Trusted Starter | as R0 | exactly 21 §3 | 21 §3 "Not claimed" list |

## 6. Audit of the 45 tasks previously in R0

Classes: **FWB** = required before the first build can run · **TEST** = required before user testing ·
**QUAL** = required before qualified R0 acceptance · **DEFER** = safely deferrable without weakening any claim made.

| Task | Old est | New est | Class | New release | Reason |
|---|---|---|---|---|---|
| A-01 | 0.05 | 0.05 | QUAL | R0 | CI evidence (already done) |
| A-02 | 0.1 | 0.1 | QUAL | R0 | only if 403 recurs |
| G-01 | 0.1 | 0.1 | QUAL | R0 | merge of planning package; not needed to build |
| G-02 | 0.1 | 0.1 | QUAL | R0 | signing key for co-sign |
| G-03 | 0.5–1 | 0.5–1 | QUAL | R0 | trusted checker before donor code reaches main |
| G-04 | 0.2 | 0.2 | DEFER | R2 | rate-limit logging; 403 shown transient |
| G-05 | 0.5–1 | 0.5–1 | QUAL | R0 | v72 checker would reject the donor tree on main; equivalence needed before F-01 |
| G-06 | 0.2 | 0.2 | QUAL | R0 | governed doc amendments |
| G-07 | 0.1 | 0.1 | QUAL | R0 | branch protection |
| G-08 | 0.75–1.25 | 0.75–1.25 | QUAL | R0 | inventory feeding G-03/G-05 |
| B-01 | 0.2 | 0.2 | QUAL | R0 | isolated baseline for donor benchmarks (no longer gated on G-03) |
| B-02 | 0.1 | 0.05 | QUAL | R0 | overlaps Q-01 import (hash already recorded) |
| B-03 | 0.5–1 | 0.25–0.5 | QUAL | R0 | build/run evidence now from Q-04/Q-05; remaining work = test pass ratio |
| B-04 | 0.3 | 0.3 | QUAL | R0 | B1–B5 baselines for F-15 budgets |
| B-05 | 0.1 | 0.1 | DEFER | R1 | fsync costs matter only for Core (NF-04) |
| B-06 | 0.1 | 0.1 | TEST | R0b | Claude SDK user-provided path before anyone else runs the app |
| B-07 | 0.05 | 0.05 | QUAL | R0 | G2 decision (no longer waits for C-00) |
| C-00 | 1.5–2.5 | 1.5–2.5 | DEFER | R1 | Windows feasibility for R1 mechanisms; R0 claims nothing they would support; now gates C-01 |
| E-00 | 0.2 | 0.2 | DEFER | R2 | PStack/E2E pins needed only for E-tasks |
| H-00 | 0.1–0.2 | 0.1–0.2 | DEFER | R2 | DeskGate admission needed only for H-tasks |
| N-01 | 0.2 | 0.2 | TEST | R0b | working-name rule before testers; free screening (no dependency on G-01) |
| N-02 | 0.1 | 0.1 | QUAL | R0 | final ids before qualified build |
| N-03 | 0.1 | 0.1 | QUAL | R0 | package/crate names; Zain-LLM separation |
| N-04 | 0.3 | 0.3 | DEFER | R1 | crate rename only needed when Core is packaged (F-10) |
| F-01 | 0.5 | 0.25 | QUAL | R0 | re-import double-counted with Q-01; now admission of the existing tree |
| F-02 | 1–2 | 1–1.75 | QUAL | R0 | strip; disabling part done in Q-03 |
| F-03 | 1–1.5 | 0.75–1.25 | QUAL | R0 | coexistence part done in Q-02 |
| F-04 | 0.5–1 | 0.5–1 | QUAL | R0 | Zain update feed (FWB/testers update by reinstall) |
| F-05 | 0.3 | 0.3 | TEST | R0b | idle-egress verification before testers |
| F-06 | 0.5 | 0.5 | TEST | R0b | SDK exclusion is a redistribution requirement |
| F-07 | 0.2 | 0.2 | TEST | R0b | Supervised default / no Full access before testers |
| F-08 | 0.2 | 0.2 | QUAL | R0 | settlement label cosmetic |
| F-09 | 0.1 | 0.1 | QUAL | R0 | protocol id bump |
| F-10 | 0.5 | 0.5 | DEFER | R1 | Core binary packaging needed only for Core work |
| F-11 | 0.75–1.25 | 0.75–1.25 | TEST | R0b | unsigned installer + notices/license gate before testers (packaging itself reused from Q-04) |
| F-12 | 2–4 | 0.5–3 | QUAL | R0 | only issues reproduced in Q-05/B-03; old range assumed all four upstream issues hit |
| F-13 | 2–4 | 0 | QUAL (folded) | R0 | learning is part of F-02/F-03/F-12/C-01; separate block was double counting |
| F-14 | 1.5–2.5 | 1.5–2.5 | QUAL | R0 | PR-24 (M) keyboard/screen-reader baseline |
| F-15 | 0.3 | 0.3 | QUAL | R0 | budgets vs baseline |
| F-16 | 0.2 | 0.2 | QUAL | R0 | R0 exit (no longer needs F-10, F-17, F-18) |
| F-17 | 2–3 | 2–3 | DEFER | R1 | Monaco (§7) |
| F-18 | 0.5 | 0.5 | DEFER | R1 | Tauri retirement follows F-10; keyring audit before R1 (R0 claims no credential-storage property) |
| Y-00 | 0.5–1 | 0.5–1 | TEST | R0b | remove donor cookie import before testers |
| L-01 | 0.3–0.5 | 0.3–0.5 | QUAL | R0 | Plan Mode label "not enforced" |
| K-01 | 0.5–0.75 | 0.5–0.75 | DEFER | R3 | OCR spike belongs to the engine lane |

Counts: FWB 0 (no existing task is needed — the five new Q-tasks replace the "make it run" portion of F-01/F-02/F-03/
F-04/F-11/B-03); TEST 7; QUAL 28; DEFER 10 (R1: 6, R2: 3, R3: 1). Nothing was deleted.

## 7. Monaco (F-17) decision

T3 already delivers chat/agent sessions, terminals, worktrees and diff review; Zain's R0 claims do not include a built-in
code editor. Monaco is first needed by K-05 (findings markers, R1). F-17 therefore moves to R1. Until then R0 states
"no built-in editor". PR-01 (IDE + AI workspace) is fully met at R1, not R0.

## 8. Double counting removed

| Overlap | Before | After |
|---|---|---|
| Learning Effect 4/orchestration (F-13) counted separately from the tasks that require it | +2–4 pw | 0 (folded) |
| Import/fetch counted twice (B-02, F-01) and again for the first build | 0.6 pw | Q-01 0.05–0.1 + B-02 0.05 + F-01 0.25 (admission only) |
| Build-and-run counted in B-03 and again in F-11/F-16 | B-03 0.5–1 | Q-04/Q-05 produce the evidence; B-03 0.25–0.5 (tests only) |
| Inherited bug fixes assumed for all four upstream issues | F-12 2–4 | 0.5–3, only reproduced issues |
| Rebranding counted fully in F-03 while Q-02 already renames identity sites | F-03 1–1.5 | 0.75–1.25 |
| Stripping counted fully in F-02 while Q-03 already disables egress | F-02 1–2 | 1–1.75 |

Resulting R0 (qualified) effort is generated; old 21.8–34.35 pw → see GENERATED_PLAN_REPORT §3 (R0 row). The deferred
tasks are not lost: their effort reappears in R1–R3 totals.

## 9. Preservation check

All capabilities stay scheduled with tasks and tests: T3 (R0a onward), Orca ports (R3), OCR engine lane + Continue rule
import (R3; delegated review R1), PStack + E2E (R2), Plan Mode with AI Hero skills (R0 "not enforced" label, R2 enforced read-only + skills),
Zain Browser (R0b hardening, R1 gating, R2 lanes), DeskGate (R2/R3/R7), Trusted Core (R1), Project Brain (R2), Claude
feature coverage (03F labels across R0–R7).
