# Founder Decision Record — V3 Foundation

```text
STATUS = AWAITING FOUNDER DECISION (no decision is recorded until the founder states it in the PR)
PREPARED = 2026-10-27
```

## Recommended foundation (one line)

**T3-first hybrid:** hard-fork `pingdotgg/t3code@36d4d711b79c73eb33131944f73ea4a8c6156484` as shell + server +
orchestration; keep WePLD's tested Rust core as the authority sidecar; port six Orca modules from
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
| ESTIMATE | v1 incl. all trust/Brain/completion work ≈ 37–68 pw (08) | ≥30–60 pw **before** trust work (+ ≈25–45 pw of the same trust work) | 08; R02 §14; R03D §16 |

## Decisions requested from the founder

| # | Decision | Recommended | Alternatives |
|---|---|---|---|
| F1 | Accept ADR-001 foundation | Yes | Orca-first; own platform |
| F2 | Accept Electron and retire Tauri shell (ADR-002) | Yes | Keep Tauri (re-plan shell) |
| F3 | Accept "one authority per fact" (ADR-004) | Yes | — |
| F4 | Repo visibility/enforcement (ADR-010) | Private + GitHub Pro/Team, or private + read-permission fix | Public |
| F5 | Governance reset (ADR-011) replacing the successor chain | Yes | Keep chain (not recommended) |
| F6 | Fork-not-track policy for T3 | Yes | Rebase tracking (infeasible at ~1.3k PRs/week) |
| F7 | Claude auth posture: API key default; no subscription proxy; seek Anthropic confirmation | Yes | — |
| F9 | Accept the v1 scope line (P−1…P5) and the 12–26 month v1 calendar estimate, with P2/P3 as earlier stopping points | Yes | larger v1 |
| F10 | Authorize the P−1 break-glass record (signed) to repair the integrity workflow | Yes | make repo public first (ADR-010 a) |
| F11 | Create a founder-only SSH signing key and allowed_signers file for protected-path co-sign | Yes | — |
| F8 | Communication: Arabic discussion, English artifacts (AGENTS.md) — resolve the Astro "English-only" contradiction | AGENTS.md | — |

## What the founder is NOT being asked

To disclose permission agreements. Rights for T3/Orca are recorded as MIT (verified) + `FOUNDER-ATTESTED` (not verified,
not disclosed).
