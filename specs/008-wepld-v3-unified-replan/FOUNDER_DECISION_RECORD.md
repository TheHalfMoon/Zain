# Founder Decision Record — V3 Foundation

```text
STATUS = AWAITING FOUNDER DECISION (no decision is recorded until the founder states it in the PR)
PREPARED = 2026-10-27
```

## Recommended foundation (one line)

**T3-first hybrid:** hard-fork `pingdotgg/t3code@36d4d711b79c73eb33131944f73ea4a8c6156484` as shell + server +
orchestration; keep Zain's tested Rust core as the authority sidecar; port six Orca modules from
`stablyai/orca@e310a63624c86c0e91e9d77df71f038b91d79ea0`; Vercel durability as patterns only.

## Evidence for T3-first vs Orca-first vs hybrid

| Criterion | T3-first (A) | Orca-first (B) | Evidence |
|---|---|---|---|
| Single state store for sessions | ✓ one SQLite, one EventSink txn | ✗ three stores | R02 §3; R03D §6.4 |
| Authority seams exist where effects pass | ✓ S1–S8 named with line refs | ◐ effects scattered across main/daemon/runtime | R02 §10; R03D §4–6 |
| Size to own | ~1.0M LOC | ~2.37M LOC | R02 §2; R03D §3 |
| Windows issue load | moderate (startup, WSL) | 421 open Windows issues | R02 §13; R03D §2 |
| Cloud/telemetry to strip | Clerk, T3 Connect, PostHog | onorca.dev auth/relay/share, PostHog, update feed | R02 §9; R03D §15 |
| IDE breadth | ◐ (no Monaco) | ✓ Monaco, Design Mode, computer use, Linear | R03D §9–11 |
| Breadth gap closable by ports | ✓ the separable Orca modules are exactly T3's gaps | n/a | R03D §14, §16.2 |
| ESTIMATE | v1 incl. all trust/Brain/completion work ≈ 88–137 pw (08) | ≥30–60 pw **before** trust work (+ ≈25–45 pw of the same trust work) | 08; R02 §14; R03D §16 |

## Decisions requested from the founder

| # | Decision | Recommended | Alternatives |
|---|---|---|---|
| F1 | Accept ADR-001 foundation | Yes | Orca-first; own platform |
| F2 | Accept Electron and retire Tauri shell (ADR-002) | Yes | Keep Tauri (re-plan shell) |
| F3 | Accept "one authority per fact" (ADR-004) | Yes | — |
| F4 | Repo visibility/enforcement (ADR-010) | **DECIDED 2026-10-27 by founder: stays PRIVATE**; enforcement plan (b) Pro/Team or (c) free advisory still open | ~~Public~~ excluded |
| F5 | Governance reset (ADR-011) replacing the successor chain | Yes | Keep chain (not recommended) |
| F6 | Fork-not-track policy for T3 | Yes | Rebase tracking (infeasible at ~1.3k PRs/week) |
| F7 | Claude auth posture: API key default; no subscription proxy; seek Anthropic confirmation | Yes | — |
| F9 | Accept the v1 scope line (P−1′…P5) and the 2.2–4.2 year v1 calendar estimate, with P2/P3 as earlier stopping points | Yes | larger v1 |
| F10 | ~~Authorize the P−1 break-glass~~ **Withdrawn**: restore GitHub Actions billing/spending limit for the private repo (P−1′) | Yes | keep CI off (no merges possible under current policy) |
| F11 | Create a founder-only SSH signing key and allowed_signers file for protected-path co-sign | Yes | — |
| F8 | Communication: Arabic discussion, English artifacts (AGENTS.md) — resolve the Astro "English-only" contradiction | AGENTS.md | — |

## What the founder is NOT being asked

To disclose permission agreements. Rights for T3/Orca are recorded as MIT (verified) + `FOUNDER-ATTESTED` (not verified,
not disclosed).

## Founder-only items from the 2026-10-27 continuation (exact evidence and implications)

| # | Item | Evidence | Implication if not done |
|---|---|---|---|
| FO-1 | **Restore GitHub Actions** for the private repo (payment method / spending limit / plan) | Re-run of run 36589753362 (attempt 2) annotation: "The job was not started because recent account payments have failed or your spending limit needs to be increased." | No integrity check can run → no PR can be qualified or merged under current policy; the 403 diagnosis stays PROBABLE |
| FO-2 | **Cubic**: uninstall the GitHub App or remove `TheHalfMoon/Zain` from its repository access, and record evidence | Cubic auto-wrote PR #347's description on 2026-10-01 despite `cubic.yaml`; its check suite is absent on today's push, but that does not prove removal | Opening a PR may transmit private content to Cubic (`PROHIBITED_EGRESS`) |
| FO-3 | **Qodo**: uninstall or remove repo access | Auto-comment within ~4 s of PR creation: reviews "paused because your trial has ended" | Any future billing restoration silently re-enables automatic review of private PRs |
| FO-4 | **CodeRabbit**: decide remove vs accept its automatic "review skipped" reaction (it reads `.coderabbit.yaml`) | Auto-comments on every PR #340–#347 within ~9 s | If accepted, record it as non-review metadata access in the egress record |
| FO-5 | **Cursor, Devin, Sentry, Vercel, Claude GitHub Apps**: confirm automatic PR review/summary features are off for this repo or remove access | Check suites from all five on today's branch push | Unknown automatic processing of private PR content on creation |
| FO-6 | **Graphite, Greptile**: confirm removed | Check suites until 10-01, absent today | — |
| FO-7 | Enforcement plan for a private repo: (b) GitHub Pro/Team for branch protection/required checks, or (c) free/advisory | Branch-protection API 403 "Upgrade to GitHub Pro or make this repository public" | Under (c) every gate is advisory |

None of these can be performed by an agent under current rules (account settings, billing, app installations).
| FO-8 | **Trademark clearance for "Zain"** before distribution/publishing (R19: HIGH risk in KSA/GCC vs Zain Group; PyPI `zain` is a coding agent) | research/R19_ZAIN_NAMING_CONFLICTS.md | Distribution under a contested mark; forced rename later |
| FO-9 | **Confirm the E2E source**: which repository/framework was meant (provisional: `TheHalfMoon/Ascout@ecada2bc` Spec 016 + Playwright); which Ascout parts are canonical; relicensing into Zain; whether any cloud E2E service is ever acceptable | research/R15 §6 | E-03 cannot start; Engineering loop ships without browser E2E |
| FO-10 | **Accept the scope reality**: with the five components v1 = ≈88–137 pw (2.2–4.2 years solo at A-1); choose release tiers (ZAIN_V3_MASTER_PLAN §5a) or cut v1 scope | 14 §13 (computed) | Plan remains unrealistic for one person |
| FO-11 | Review the locally installed Desktop Commander configuration (unrestricted `allowedDirectories`, telemetry on) — independent of Zain | research/R18 §8 | Local exposure on the founder's machine |
