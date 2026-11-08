# 22 — Third-Party App and Egress Inventory (task Z-02)

```text
DATE     = 2026-11-08
TASK     = Z-02 (AGENT+FOUNDER): inventory of GitHub Apps with access to TheHalfMoon/Zain (agent); remove each app or
           document its automatic review OFF (founder); disposition of cubic.yaml; scratch-push check afterwards
STATUS   = inventory done; app changes wait for the founder (§4); the scratch-push check follows them (§5)
RULE     = main's EXTERNAL_REVIEW_EGRESS_POLICY.md: hosted reviewers stay manual opt-in until a machine-enforced
           pre-egress gate exists. This holds while the repository is public: public content limits confidentiality
           impact, not the automatic-trigger rule
METHOD   = read-only API. `GET /user/installations` is refused for the gh CLI login (it needs a GitHub App user token),
           so installed apps are inferred from check suites and bot activity
```

## 1. Other egress paths

| Path | Finding |
|---|---|
| Repository webhooks | none |
| Deploy keys | none |
| Actions secrets / variables | 0 / 0 |
| Rulesets | none |
| Deployments | none recorded |

## 2. Apps with repository access (inferred)

Evidence: check suites on main's head and on the 40 most recent PR heads (2026-09-09 to 2026-10-01, through #347);
bot comments and reviews on those PRs; check suites on seven plan-branch commits pushed 2026-11-08, five of them while
the repository was private (00:37–01:31Z).

| App | Seen as | Latest activity | Automatic review state |
|---|---|---|---|
| CodeRabbit | check suite on PRs and main; 306 comments/reviews | #347, 2026-10-01 | **OFF in `.coderabbit.yaml`** (`auto_review.enabled: false`); still posts an automatic "review skipped" summary comment |
| cubic | check suite on PRs and main (conclusion neutral) | #347 | **OFF in `cubic.yaml`** (`reviews.enabled: false`, auto-approve and ultrareview disabled) |
| Qodo | 37 comments | #347: "reviews are paused because your trial has ended" | Paused by billing, not by setting; V3 FO-3 already recommends removal |
| Cursor (Bugbot) | check suite on PRs, main and plan pushes | 2026-11-08 (queued, never run) | Not documented |
| Devin | check suite on PRs, main and plan pushes | 2026-11-08 (queued) | Not documented |
| Graphite | check suite on PRs and main | #347 | Not documented |
| Greptile | check suite on PRs and main | #347 | Not documented |
| Sentry | check suite on PRs, main and plan pushes | 2026-11-08 (queued) | Not documented |
| Vercel | check suite on PRs, main and plan pushes | 2026-11-08 (queued); no deployments | Not documented |
| Claude (Anthropic GitHub App) | check suite on plan pushes | 2026-11-08 (queued) | Not documented |

**During today's private window,** five plan-branch pushes created queued check suites for Cursor, Devin, Vercel,
Sentry and Claude. None ran a check and Vercel made no deployment. Each app was notified of the commit, and its
installation token could read the repository; whether any did is not visible. That content is public again now.

## 3. Assessment

- Two apps (CodeRabbit, cubic) have automatic review documented OFF in the repository. CodeRabbit still comments
  automatically, and both still create check suites.
- Eight apps have no documented OFF setting.
- GATE-PRIV-02 needs 0 apps with automatic review on and 0 third-party AI check suites. Check suites exist for every
  installed app with the Checks permission, whatever its review setting. So only removing repository access, or
  uninstalling, meets the gate.
- DEC-01 named the founder and OCR on the founder's ChatGPT login as reviewers; none of these hosted apps is an
  authorized review route.

## 4. Proposed founder actions

In GitHub, signed in as TheHalfMoon: **Settings → Applications → Installed GitHub Apps**
(https://github.com/settings/installations). For each app below, open **Configure**. Under **Repository access**,
remove `Zain`, or uninstall the app if nothing else needs it. Also check whether the app is set to **All
repositories**.

1. Qodo
2. Cursor (Bugbot)
3. Devin
4. Graphite
5. Greptile
6. Sentry
7. Vercel
8. Claude
9. cubic
10. CodeRabbit (or keep it for manual reviews only; see below)

**Option:** the governance `AGENTS.md` lists CodeRabbit among wanted correctness reviewers when policy permits.
Keeping CodeRabbit with its automatic review OFF allows manual, egress-checked reviews later. The cost is that its
check suite and "review skipped" comments remain, so GATE-PRIV-02 would need a recorded exception for it.

**`cubic.yaml` and `.coderabbit.yaml`:** keep them on `main`. They document the OFF state, and changing `main` goes
through governance. Once cubic is removed, `cubic.yaml` is inert and can go with the planning merge at G-03.

## 5. Check after the founder's changes

Push an empty commit to a scratch branch and wait about two minutes. List that commit's check suites and the
branch's comments, expecting no third-party app. Then delete the scratch branch, and record the outputs here. The
push is public, so it runs only with the founder's go-ahead.
