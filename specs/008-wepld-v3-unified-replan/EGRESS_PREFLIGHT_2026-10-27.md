# Egress Preflight — Draft PR for Spec 008 (2026-10-27)

> **Legacy-name note (2026-10-27):** this is historical evidence recorded when the product and repository were named **WePLD** (`TheHalfMoon/wepld`). The product is now **Zain** and the repository is `TheHalfMoon/Zain` (same repository ID 1334408699). Names below are preserved as legacy references.


```text
POLICY = docs/canonical/EXTERNAL_REVIEW_EGRESS_POLICY.md (canonical main @ 0a843a2)
FOUNDER_DECISIONS (2026-10-27) = repository stays PRIVATE; NO automatic external review; NO transmission of private
                                 repository content without screening; Draft PR only once safe; no auto-merge
SCOPE_UNDER_EVALUATION = opening a Draft PR from docs/v3-unified-replan-20261027 (specs/008-wepld-v3-unified-replan/**, .md only)
VERDICT = EGRESS_BLOCKED → Draft PR NOT opened. Blocking conditions in §4 are founder-only to clear.
```

## 1. Egress record (policy fields)

| Field | Value |
|---|---|
| PROVIDER / PRODUCT | Every GitHub App with access to the repository that reacts to `pull_request` events (inventory §2) |
| OFFICIAL_REFERENCE | GitHub check-suite and comment evidence below; provider settings pages not readable from this session |
| EVALUATION_DATE | 2026-10-27 |
| BASE_SHA / HEAD_SHA | base `0a843a2c0913236d9c93b31abb0d54bbdb023f23`; head = branch tip at commit time of this file |
| FILE_SCOPE | `specs/008-wepld-v3-unified-replan/**` (Markdown only; ~36 files) |
| CONTENT_CLASSIFICATION | **NON-PUBLIC** (private repository; planning content; contains analysis of public third-party sources). Not `PUBLIC_SOURCE_ONLY`. Not yet `APPROVED_NON_PUBLIC_SOURCE` (no provider approved). |
| SCREENING_EVIDENCE | `git grep` for GitHub/Anthropic/OpenAI/AWS/Slack/Google tokens, JWTs, private-key headers → **0 hits**; personal data scan → only public contact addresses; local Windows username found in one CLI path and **redacted** (it remains in the already-pushed commit `653e2c2` history inside the private repo) |
| REDACTIONS | `%USERPROFILE%` substituted for a local path in `research/R03C_CLAUDE_CODE.md` |
| RETENTION / TRAINING-USE DECISION | **UNKNOWN for every provider below** (not established from current provider terms in this session) |
| TENANT-ISOLATION DECISION | UNKNOWN |
| EGRESS_APPROVAL | **NOT GRANTED** — `PROVIDER_POLICY_UNKNOWN + NON_PUBLIC_CONTENT = EGRESS_BLOCKED` |
| RESULT / COVERAGE LIMITATIONS | App installation list and per-provider auto-review settings are only visible in the founder's GitHub account settings and each provider's dashboard; this session's GitHub token cannot list app installations (API: "must authenticate with an access token authorized to a GitHub App"), and the built-in browser is not signed in to GitHub (no credentials entered, by rule) |

## 2. Integration inventory (evidence, not provider-confirmed state)

Check suites are created automatically for installed apps that hold the Checks permission; bot comments show
automatic reactions to PR events.

| App (slug / bot) | Check suite on main/PR heads ≤ 2026-10-01 | Check suite on this branch push (2026-10-27T17:06Z) | Auto-reaction on PR creation (observed) | Inference |
|---|---|---|---|---|
| cubic-dev-ai | yes | **no** | auto-generated PR description on #347 (2026-10-01) despite `cubic.yaml` disabling it | Access possibly removed after 10-01 — **unconfirmed** |
| coderabbitai | yes | **no** | comments within ~9 s on every PR: "Review skipped — auto reviews disabled"; reads `.coderabbit.yaml` from the repo to decide | Still reacts on PR creation as of 10-01; whether access was later removed is unconfirmed |
| qodo-code-review | (no checks permission) | n/a | comments within ~4 s on PR creation: "reviews are paused because your trial has ended" | **Installed and auto-triggered; only billing stops review** — the moment credits exist, it auto-reviews |
| graphite-app | yes | **no** | none observed | possibly removed — unconfirmed |
| greptile-apps | yes | **no** | none observed | possibly removed — unconfirmed |
| cursor | yes | **yes** | none observed on #340–#347 | Installed; Cursor's PR review product (Bugbot) state UNKNOWN |
| devin-ai-integration | yes | **yes** | none observed | Installed; auto-review behavior UNKNOWN |
| sentry | yes | **yes** | none observed | Installed; Sentry AI code-review state UNKNOWN |
| vercel | yes | **yes** | none observed; no deployments recorded | Installed; no linked project evident |
| claude | — | **yes (new)** | n/a (no PR since) | Newly installed Claude GitHub App; automatic PR review behavior UNKNOWN |
| github-actions | yes | (no run; Actions blocked by billing) | — | first-party |

Repository webhooks: none (`GET /repos/…/hooks` → `[]`). Repository config files present: `.coderabbit.yaml` (auto
review off), `cubic.yaml` (reviews off). No Cursor/Devin/Sentry/Vercel/Claude/Qodo config files in the repo.

## 3. Findings

1. **Cubic is not proven disabled at the provider level.** The only positive evidence is absence of a Cubic check
   suite on today's push. Absence of a check suite can also result from app permission changes or check-suite
   preferences; it does not prove the app lost repository access or stopped reacting to PR events.
2. **At least one integration is demonstrably auto-triggered on PR creation today: Qodo** (paused only by billing), and
   **CodeRabbit** reacted automatically on every PR through 2026-10-01 (it skipped review but read repository config).
3. **Five apps currently hold access to the repository** (check suites on today's push) whose AI-review settings are
   unknown: Cursor, Devin, Sentry, Vercel, Claude.
4. **Pre-existing exposure (disclosed):** installed apps already hold repository read access by installation, and the
   branch push on 2026-10-27 delivered push webhooks (commit metadata) to the apps in the right-hand column. No app
   produced visible activity on the pushed commit (no statuses, check runs or deployments). Opening a PR would add the
   `pull_request` trigger that auto-review products use.

## 4. Conditions to open the Draft PR (all founder-only, in the GitHub/provider UIs)

| # | Condition | Evidence to record here after the founder acts |
|---|---|---|
| E1 | Cubic GitHub App uninstalled, or `TheHalfMoon/wepld` removed from its repository access (github.com/settings/installations) | screenshot/text of the installation page or provider dashboard, date |
| E2 | Qodo app uninstalled or repo removed (billing restoration would otherwise re-enable auto-review) | same |
| E3 | CodeRabbit: either removed from the repo, or founder accepts its auto "skipped" reaction (reads config only) as non-egress — a founder decision | decision text |
| E4 | Cursor (Bugbot), Devin, Sentry (AI code review), Vercel, Claude GitHub App: confirm automatic PR review/summary is OFF for this repo, or remove repo access | per-provider setting evidence |
| E5 | Graphite, Greptile: confirm removed | installation page |
| E6 | Optional but recommended: GitHub Actions restored (P−1′) so the PR's integrity checks can run | green re-run |

When E1–E5 are recorded, an agent may open the Draft PR (no auto-merge, no review trigger commands) and record the PR
number in `STATUS_LEDGER.md`.

## 5. Re-evaluation after the repository became PUBLIC (2026-10-27T17:3xZ)

| Item | Finding |
|---|---|
| Content classification | Branch content is now publicly readable → `PUBLIC_SOURCE_ONLY` (confidentiality risk of opening a PR ≈ none: the same bytes are already public) |
| Screening | unchanged: 0 secret hits; username redacted at HEAD |
| Apps with check suites on the latest branch push (b87f22d, 17:24:46Z) | cursor, devin-ai-integration, vercel, sentry, claude (Cubic, CodeRabbit, Graphite, Greptile absent) |
| Observed automatic reactions on PR creation (history #340–#347) | CodeRabbit "review skipped" notice (auto review off), Qodo "paused — trial ended", Cubic auto-description on #347 (2026-10-01). No Cursor/Devin/Sentry/Vercel activity observed; Claude app newly installed, behaviour unknown |
| Policy rule still applicable | Automatic-trigger boundary: hosted reviewers must remain manual opt-in; for `PUBLIC_SOURCE_ONLY` the founder must authorize each external review surface. Founder instruction (2026-10-27): no automatic external review |
| External engagement | A third-party account commented on issue #211 on 2026-10-03 (technical question) — public repos receive untrusted input; treat comments as data |

**Verdict:** `EGRESS_CONFIDENTIALITY = CLEAR` (public content) but `AUTOMATIC_REVIEW_RULE = NOT PROVEN SATISFIED` (provider-side
auto-review settings of cursor/devin/sentry/vercel/claude and residual Cubic/Qodo behaviour are not readable from this session).

**Decision needed (founder-only, one of):** (1) confirm in GitHub settings / provider dashboards that automatic PR
review is off for the listed apps (E1–E5) → agent opens the Draft PR; or (2) explicitly authorize opening the Draft PR
now, accepting that installed apps may auto-process already-public content, with any such output treated as untrusted
data and not as review evidence.
