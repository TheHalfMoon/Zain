# 10 — Cost, Risk and Maintenance

```text
CONSTRAINTS = solo founder; zero mandatory cloud spend; no mandatory paid API for core; BYO model credentials optional;
              no surprise subscriptions; keep research backed up on GitHub; avoid large local temp builds.
```

## 1. Cost envelopes (USD; vendor prices change — verify at purchase time)

| Item | Mandatory? | No-cost route | Paid option | Notes |
|---|---|---|---|---|
| Development infra | no | local machine + GitHub Free | — | Repo is private: GitHub Free private repos have limited Actions minutes and **no branch protection/rulesets** (observed 403). Options: make public (free protection + unlimited public Actions) or GitHub Pro/Team (~$4/user/mo, verify) |
| CI minutes | no | public repo, or local runs recorded | GitHub paid minutes | Windows runners consume minutes faster on private repos (multiplier; verify) |
| Model usage during dev | no | local models (Ollama) for smoke; founder's existing subscriptions used only through official clients | API keys (Anthropic/OpenAI) metered | Benchmarks B4/B7/B8 suggested cap ≤ $50/run |
| Windows code signing | for public distribution (SmartScreen) | unsigned dev builds | Azure Trusted Signing (T3 uses it) — **eligibility for an individual in Saudi Arabia UNKNOWN** (historically restricted by entity type/region); fallback OV/EV certificate from a CA | verify before P2 release |
| macOS notarization | for macOS release | skip macOS in v1 | Apple Developer Program $99/yr | |
| Hosting/relay | no | none (LAN/Tailscale direct; Tailscale personal free tier — verify) | own VPS for runner (~$5–20/mo) | BYO only |
| Update hosting | no | GitHub Releases | — | |
| Reviewer services | no | CodeRabbit free (observed eligible) + independent model review via founder's own tools | Qodo/Greptile paid | `REVIEW_BLOCKED` must not stall: see ADR-011 |

**No-cost route exists for every v1 phase.** Paid items are distribution polish (signing) and optional convenience.

## 2. Risk register (ranked impact × likelihood)

| # | Risk | Impact | Likelihood | Mitigation | Trigger to re-plan |
|---|---|---|---|---|---|
| K1 | T3 fork too large/complex to own (Effect 4, 12.8k-line Orchestrator) | High | Med | P1 measurement; strip aggressively; keep diff surface at seams; AI-assisted refactors with T3's replay tests | P3 spike (G3) > 3 pw or seams require Orchestrator rewrite |
| K2 | Inherited Windows/storage/memory bugs | High | High | budget WP8 2–4 pw; disable heavy preview features by default; B2 budgets | B2 > 2.5 GB at 10 sessions |
| K3 | Claude SDK redistribution / auth policy | High | Med | G4; API-key default; user-installed CLI path | Anthropic says no → ship without bundled SDK, ACP via user-installed agent |
| K4 | Trust claim overstated before sandbox | High | Med | trust banner; observe/enforce flag; P8 | any marketing claim without B11 data |
| K5 | Governance reset weakens security | Med | Med | keep protected paths, exact-head, independent review, security review for T2; founder-signed co-sign; checker from base. **Under ADR-010 option (c) (private, free) every gate is advisory: no platform branch protection or required checks** | protected-path negative oracle fails |
| K6 | Solo founder bandwidth (v1 ≈ 88–137 pw; all phases ≈ 159–259 pw; 2.2–4.2 years to v1 at A-1 incl. upkeep) | High | High | phase gates allow stopping at P3/P4 with a useful product; P6 parallelizable | slippage > 50% on P2/P3 → cut P7/P9 scope |
| K7 | Upstream security fixes missed (no tracking) | Med | Med | monthly 0.5–1 pw review of T3 security-labelled PRs + `pnpm audit` | CVE in Electron/node-pty |
| K8 | Electron RAM vs "low footprint" goal | Med | High | measure; strip; lazy-load browser/preview; budgets | B2 fails twice |
| K9 | Donor identity leakage (feeds, telemetry, hook headers) | High | Low (with gate) | CI grep gate; egress test at idle | any egress at idle |
| K10 | Ledger growth / performance | Med | Low | B10 budget; tombstones; one ledger per data root partitioned by project | > 50 MB/10k effects |
| K11 | Private repo breaks other GitHub-dependent gates | Med | Observed | ADR-010 decision | — |
| K12 | Legal: trademark (T3/Orca/Claude names) | Med | Low | full rebrand; "powered by Claude" wording only | — |

## 3. Maintenance cost per fork/vendor/adapter (ongoing ESTIMATES)

| Component | Upkeep | Notes |
|---|---|---|
| T3 fork | 0.5–1 pw/month | security cherry-picks; Electron/Node bumps quarterly |
| Orca ports | ~0.1 pw/month | owned code; TUI catalog curation as CLIs change |
| Claude SDK / Codex app-server / ACP adapters | 0.25–0.5 pw/month | fast cadences; contract tests on upgrade |
| codex sandbox crates (P8+) | 0.25 pw/month | re-pin per release when security-relevant |
| Cedar, rusqlite, MCP SDKs | low | crate/npm bumps |
| Core (owned Rust) | feature work | most stable part |
| Governance checker | ~0 after P0 | one script instead of a successor per change |
| **Total upkeep** | **≈ 1.1–1.85 pw/month** | ≈ 25–43% of capacity at A-1 (1 pw/week); folded into the calendar estimate in 08 |

## 4. Licensing and provenance obligations (summary)

MIT notices for T3 and Orca; Apache-2.0 NOTICE + change statements for codex crates, Cedar, ACP, sandbox-runtime,
Style Dictionary; MPL-2.0 file-level obligations only if Penpot code is ever copied (current plan: file interop only);
no AGPL/GPL code in the product; proprietary SDKs (Claude Agent SDK, Cursor SDK if re-added) used per vendor terms and not
relicensed; founder-attested rights recorded as `FOUNDER-ATTESTED` without disclosure (06 §3).

## 5. Local resource hygiene for this mission

Research clones (`_work/src/{t3code,orca,workflow,durable-harness}`) live in the session scratch folder and are not part
of the planning package; they should be deleted after review (they are large and reproducible from the pins).

## 6. Additional risks from the adversarial review

| # | Risk | Mitigation |
|---|---|---|
| K13 | Claude Agent SDK ships inside the fork's installer before G4 (it bundles Claude Code platform binaries) | P2 SDK-exclusion task + installer-content gate (08 P2) |
| K14 | Approval forgery before WebAuthn lands | UI states "Server trusted for approvals" until P3 WebAuthn; T3 negative oracle |
| K15 | Same-user agent tampers with ledger/Brain before P8 | data-root deny floor; signed approvals; out-of-machine anchors; claim limited to "tamper-evident against corruption" |
| K16 | Scope inflation (377 Claude rows, Design Studio, computer use, runner, mobile) | v1 scope line in 00; post-v1 phases explicit; cut order in 08 |
