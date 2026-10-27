# CI 403 Re-diagnosis (2026-10-27)

```text
SUBJECT = foundation-integrity run 36589753362 (push to main @ 0a843a2c…, 2026-09-29T15:22Z) failed with HTTP 403
TRIGGER = founder challenge: both workflows on main already declare `permissions: contents: read`
RESULT = draft-1/revision-2 diagnosis ("permissions: {} on a private repo") was WRONG and is withdrawn.
         The P−1 one-line permissions fix is NOT necessary and is removed from the roadmap.
CURRENT_BLOCKER = GitHub Actions jobs do not start at all on this repository: billing / spending limit (founder-only).
```

## 1. Facts (verified 2026-10-27)

| # | Fact | Evidence |
|---|---|---|
| F1 | `foundation-integrity.yml` on main: top-level `permissions: contents: read`; checkout `persist-credentials: false`; the push-verification step passes `GITHUB_TOKEN: ${{ github.token }}` | `git show origin/main:.github/workflows/foundation-integrity.yml` lines 9–10, 61–74 |
| F2 | The run's token really had `Contents: read`, `Metadata: read` | run log, "GITHUB_TOKEN Permissions" group (log lines 21–23) |
| F3 | The script authenticates every REST call with `Authorization: Bearer <token>` (no unauthenticated path when the env var is set) | `.github/scripts/wepld_integrity.py` `GitHubClient.json` L330–352; token from `--github-token-env` L2070 |
| F4 | In `verify_remote_baseline`, the `contents/` request is issued first and must succeed before the `compare/` request is attempted; the run failed on `compare/` → the preceding `contents/` call with the same token on the same private repo **succeeded** | `wepld_integrity.py` L1091–1124; failing message names the `compare/` URL |
| F5 | The 403s cluster in one window: s1-admission runs 36588716489 (15:14, `git/blobs/…`), 36589030582 (15:17, `git/commits/…`), 36589691943 (15:22, `git/commits/…`) and the main push 36589753362 (15:22, `compare/…`) | `gh run view --log-failed` |
| F6 | The same workflows with the same permissions passed shortly before (14:43, 14:52, 14:54, 14:55 on 2026-09-29) and again on 2026-09-30 (six runs on PR #346) | `gh run list` |
| F7 | PR #347 failures (2026-10-01) are the expected base-controlled-path negative oracle (`AGENTS.md` changed), not 403s | run logs 36840908817 / 36840909079 |
| F8 | The s1-admission design reads candidate commit/tree/blob objects through the REST API (data-only, no checkout), i.e. many requests per run; several successor verifications call `verify_remote_baseline` repeatedly | `wepld_integrity.py` L498–576, L1680–1705 |
| F9 | Re-run of the failed job (attempt 2, 2026-10-27) **did not start**: annotation "The job was not started because recent account payments have failed or your spending limit needs to be increased." | check-run 122348322500 annotations |

## 2. Conclusion

- **Not a permission or visibility problem.** F1–F4 show the token had and used `contents: read` successfully against
  the private repository in the same run, immediately before the failing call.
- **Most probable cause: transient REST API throttling** of the repository's `GITHUB_TOKEN` (primary or secondary rate
  limit) during a burst of ≥8 integrity runs in ~40 minutes, each issuing many object reads (F5, F6, F8). A
  permission-class 403 would fail on the first request and would not self-heal the next day.
- **Classification: PROBABLE, not PROVEN.** The script discards the response body and `x-ratelimit-*` headers, so the
  exact GitHub message ("API rate limit exceeded" / "secondary rate limit") is not in the log, and the decisive re-test
  (F9) could not run because Actions jobs are currently blocked by billing.
- Earlier statements in this package that the repository's private status caused the failure are withdrawn. The private
  status is still real (branch-protection API returns 403 on the current plan), but it did not cause run 36589753362.

## 3. Consequences for the plan

| Item | Old | New |
|---|---|---|
| P−1 | change `permissions: {}` → `contents: read` | **Removed.** Replaced by P−1′ (below) |
| G1 | "main repaired via break-glass" | "Actions can run again (billing) and main's integrity run is green on re-run" |
| Governance hardening (later, governed T2 change, not now) | — | make `GitHubClient` log HTTP status, `x-ratelimit-remaining/reset` and the response `message`; bounded retry with backoff on rate-limit 403/429 only; reduce per-run object reads (cache blobs by SHA within a run) |

**P−1′ (founder-only):** restore GitHub Actions for this private repository (payment method / spending limit / plan),
then re-run 36589753362 unchanged. If it passes → throttling diagnosis confirmed and main is green with no code change.
If it fails again with 403 → capture the full response by running the same policy command locally with a founder token
and open a governed fix.

## 4. Addendum — confirmation (2026-10-27T17:39Z)

After the repository was made public (Actions available again), run 36589753362 was re-run **unchanged** (attempt 3,
same SHA `0a843a2c…`, same workflow and policy files). Result: **SUCCESS**, including the `verify-local
--remote-baseline` step and all v1–v72 activation markers (`gh run view 36589753362 --attempt 3`).

```text
DIAGNOSIS = CONFIRMED TRANSIENT (no permission, workflow or policy change was needed)
MOST_PROBABLE_MECHANISM = REST API throttling during the 2026-09-29 burst (exact GitHub message still unlogged)
MAIN_STATUS = GREEN at 0a843a2c (attempt 3)
A-01 = DONE · A-02 = NOT NEEDED · P−1′ = CLOSED
FOLLOW-UP = G-04 (log status/rate-limit headers + bounded backoff) remains in P0 so the next transient is diagnosable
```
