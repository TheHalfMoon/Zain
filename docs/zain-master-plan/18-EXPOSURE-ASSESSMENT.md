# 18 — Public-Exposure Assessment (task Z-03)

```text
DATE     = 2026-11-08
SCOPE    = TheHalfMoon/Zain (public until 2026-11-08T00:37:46Z, now private) and wepld/wepld (still public)
METHOD   = read-only; all refs fetched (Zain: 689 refs incl. 336 PR heads, 1,497 commits; wepld: 22 refs, 85 commits);
           every added line of every commit, commit messages and author/committer identities streamed in memory through
           13 secret rules and 6 personal-data rules (_work/z03_scan.py logic, summarized in §6); PR and issue bodies and
           all issue and review comments via the GitHub API; both Actions artifacts; 20 most recent Actions run logs
OUTPUT   = rule, location and a sha256 fingerprint only — no matched value is stored or printed in this report
VERDICT  = no live credential found; personal data was exposed (commit email, Windows username); dispositions in §4
```

## 1. What was publicly readable, and for how long

| Surface | TheHalfMoon/Zain | wepld/wepld (still public) |
|---|---|---|
| Public window | From at least 2026-09-12 (CURRENT_STATE checkpoint records "public"; the repo was created 2026-08-14) until 2026-11-08T00:37:46Z. The exact start is unknown | Since creation (2026-07-12), still open |
| Git history | 353 branches, 336 PR heads, 1,497 commits | 9 branches, 85 commits |
| PRs, issues, comments | 332 PRs, 15 issues, 4,179 comments | 11 PRs, 7 comments |
| Actions run logs | 2,985 runs | 30 runs |
| Actions artifacts | 2 license-evidence bundles (5.1 MB and 2.9 MB), not expired | none |
| Forks, stars, watchers | 0, 0, 0 | 0, 0, 0 |
| Releases, tags, wiki, Pages, discussions | none | none |
| Actions secrets defined | none | none |

Zero forks means no public fork copy survives the visibility change. Copies outside GitHub cannot be ruled out
(see §5).

## 2. Secrets (13 rules: cloud, GitHub, OpenAI, Anthropic, Google, Slack, Stripe, Hugging Face, npm keys; private-key
blocks; JWTs; Azure keys; generic secret assignments)

**No live credential was found.** Every hit was triaged by shape (masked prefix, length, entropy) and context:

| # | Where | Rule | Shape and context | Disposition |
|---|---|---|---|---|
| S1 | Zain `crates/contracts/tests/s3_contracts_v1.rs` (PR #343 branch) | private-key header | 27-character string literal used as a detection pattern | False positive |
| S2 | Zain `crates/core/tests/cli_v1.rs` | GitHub token | Low-entropy `ghp_` fixture beside a synthetic `alice:supersecret` URL | Test fixture |
| S3–S6 | Zain `crates/contracts/tests/project_v1.rs`, vendored `agile` and `pictorial` files (PR #136) | generic assignment | Template placeholders (`${…}`, `{{…}}`) and test values | False positive |
| S7 | wepld `crates/providers/tests/openai_tests.rs` | OpenAI key | 37-character `sk-` constant named `SECRET` in a test; real OpenAI keys are much longer | Test fixture; founder may confirm |
| S8 | Zain PR #105 body and 3 issue comments | private-key header | Text listing the patterns an egress screen checked for; no key material and no END line follows | False positive |

The 20 sampled Actions logs and both artifacts produced no secret-rule hits. No credential rotation is required by
these findings.

## 3. Personal and environment data

| # | Data | Where | Still exposed now? | Sensitivity |
|---|---|---|---|---|
| P1 | The founder's personal Gmail address as author/committer | 1,482 Zain commits; 72 wepld commits | wepld: yes. Zain: no longer public, but was | Medium (contact identifier, permanently in commit metadata) |
| P2 | Two other Gmail identities as authors | wepld: 11 and 2 commits | Yes | None for third parties: both map to founder-owned GitHub accounts (commit API, 2026-11-08) |
| P3 | The founder's Windows username in paths | Zain `docs/canonical/master-plan-v2-2/PART-01.md`, V3 `research/R03C_CLAUDE_CODE.md` (history; redacted at HEAD), one commit message, one issue comment; wepld `docs/governance/CONFIDENTIALITY.md` | wepld: yes | Low |
| P4 | Local npm-cache path and installed package version | Zain V3 `research/R18_DESKGATE.md` at commits `c376917` and `ef19a3f` (removed at HEAD) | No | Low |
| P5 | Third-party maintainer emails | Dependency license metadata in both artifacts (132 and 151 distinct); vendored projects in PR #136 | — | None for the founder (public upstream data) |
| P6 | Environment details | Private IPv4 addresses only inside vendored third-party docs; a generic "OneDrive\Desktop" mention | — | None |
| P7 | The founder's personal Gmail as the public profile email of the account the Zain commits map to | GitHub user profile (found 2026-11-08) | Yes, regardless of repository visibility | Medium (same identifier as P1, still published) |

Test-fixture identities (`example.test`, `example.invalid`, `evil.example`, names such as `alice`, `dev`, `ana`) are
synthetic and need no action.

## 4. Dispositions and recommendations

| Item | Recommendation | Owner | Destructive? |
|---|---|---|---|
| Secrets S1–S8 | No action; record as reviewed | — | No |
| P1 commit email | **Accept the historical exposure** (it was public for weeks and may already be archived; rewriting 1,482 commits would invalidate every SHA, branch and PR reference in the plans). **Going forward:** set `git config user.email` to the GitHub noreply address, enable "Keep my email addresses private" and "Block command line pushes that expose my email" in GitHub email settings (DEC-16) | Founder | No (settings only) |
| P2 other identities | Resolved: both are founder-owned accounts; no one to notify | — | No |
| P7 profile email | Set the profile's public email to "Don't show my email address" | Founder | No (settings only) |
| wepld/wepld | Make it private or archive it from the `wepld` account; it still exposes P1, P2 and P3 | Founder | No |
| P3 Windows username | Low risk; optionally redact from `PART-01.md` in a normal commit (history keeps it) | Agent, on request | No |
| P4 npm-cache path | No action (removed at HEAD; low sensitivity) | — | No |
| PR #136 vendored third-party code | Privacy: none. Licensing: the public branch distributed third-party code; keep the projects' license notices if the branch is kept, or delete the branch (founder decision under Z-04) | Founder | Branch deletion is destructive |
| Actions artifacts | Optional: delete the two license-evidence artifacts if no longer needed (they expire on their own) | Founder | Yes (artifact deletion) |
| History rewrite | **Not recommended** for any finding | — | — |

## 5. Residual exposure that cannot be undone or verified from here

- Anyone may have cloned, forked-then-deleted or scraped the repository while it was public.
- Public event archives (for example GH Archive) record push events from public repositories, including commit
  author emails. Software-preservation archives may hold a copy. This assessment did not query those services.
- Commits that were force-pushed away or belong to deleted branches are not reachable from current refs and were not
  scanned. GitHub may still serve them by SHA to anyone who recorded one.

## 6. Method limits

- Regex rules, not a dedicated scanner: no gitleaks or trufflehog is installed, and installing one needs founder
  approval. The rules cover the common high-signal formats; unusual secret formats could be missed.
- Binary files were not scanned (git diffs show them as binary).
- Only 20 of 2,985 Actions logs were sampled. The workflows define no secrets and use only the masked, short-lived
  `GITHUB_TOKEN`, so the residual risk in logs is low but not zero.
- Classification heuristics were checked by hand for every secret-rule hit (§2), not for every email or path hit.

## 7. Evidence

Run on 2026-11-08 from the local clones (no files written except this report): totals in §1 from `gh api`; secret and
personal-data hits from the in-memory scanner; artifact contents read from the API into memory; R18 differences from
`git diff c376917 origin/docs/r0a-opus-start-20261102`. Scanner logic: 13 secret rules and 6 personal-data rules
listed above, sha256 fingerprints truncated to 12 hex characters, no value persisted.

## 8. Founder decision (DEC-16, 2026-11-08)

- **Accepted:** the historical commit-email exposure (P1). History is not rewritten.
- **Done:** the global git identity on the founder's PC now uses the GitHub noreply address of the account that the
  existing commits map to, so attribution is unchanged. The commit that recorded this decision is the first with it.
- **Resolved:** P2. Both other wepld identities belong to the founder's own GitHub accounts.
- **Founder to do:** in GitHub email settings, enable "Keep my email addresses private" and "Block command line pushes
  that expose my email"; set the profile's public email to "Don't show my email address" (P7). The active `gh` token
  lacks the `user` scope, so the agent cannot read or change these settings. Make wepld/wepld private or archive it
  (Z-01).
- **Caveat:** once push blocking is on, GitHub rejects pushes of new commits authored with the personal address,
  including unpushed commits made before the switch in other local repositories.
