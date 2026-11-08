# 13 — Risks and Open Decisions

```text
RISKS     = registry/zain-risk-register.csv (25 risks; severity = likelihood × impact, checked by zmp.py)
DECISIONS = DEC-01..DEC-16 below; all decided by the founder on 2026-11-08 (Z-25). None is decided by this document; the Decided column records founder answers.
```

## 1. Risk summary

Severity uses likelihood × impact on 1–5 scales: CRITICAL ≥ 20, HIGH ≥ 12, MEDIUM ≥ 6. `zmp.py check` recomputes
the severity and rejects a HIGH or CRITICAL risk that has no mitigation task.

| Risk | Severity | One line | Mitigation | Gate |
|---|---|---|---|---|
| RK-03 | CRITICAL | Full V3 scope (196–324 pw including this plan's tasks) exceeds solo capacity | Z-25 scope decision; first release = R0b; Z-32 daily-use evidence | GATE-R0-EXIT, GATE-USE-01 |
| RK-01 | CRITICAL | Repository and history are public | Z-01, Z-03 | GATE-PRIV-01, GATE-PRIV-03 |
| RK-04 | CRITICAL | Governance (85k LOC) and planning (48k lines) dwarf product code (10k LOC) | G-03, G-05, Z-25 | GATE-R0-EXIT |
| RK-05 | CRITICAL | The machine cannot build (C: 3.4 GB free) | Z-07 | GATE-RES-01 |
| RK-06 | CRITICAL | No-paid, CPU-only path cannot deliver agentic quality | Z-10, Z-11 | GATE-MODEL-01 |
| RK-09 | CRITICAL | Windows containment unproven on a Home Insider-range build | C-00, C-25, H-08 | GATE-R1-EXIT |
| RK-10 | CRITICAL | Injection drives destructive actions | F-07, C-05, C-12, Z-19 | GATE-SEC-01, GATE-SEC-03 |
| RK-02 | HIGH | Third-party AI review apps read code | Z-02 | GATE-PRIV-02 |
| RK-11 | HIGH | Fork drift from a fast upstream | F-13, B-03, B-07 | GATE-R0-EXIT |
| RK-12 | HIGH | IDE pillar unmet early | Z-13, Z-20, F-17 | GATE-IDE-01 |
| RK-13 | HIGH | V3 validator fails open; exit ordering wrong | Z-26 | GATE-PLAN-03 |
| RK-14 | HIGH | No authorized independent reviewer | Z-06 | GATE-REV-01 |
| RK-07 | HIGH | Donor/SDK license contamination | Q-00, Q-04, F-06, F-20 | GATE-R0A-EXIT |
| RK-16 | HIGH | Checkpoint restore deletes untracked files | Z-27 | GATE-J18 |
| RK-17 | HIGH | Private code to an unauthorized model endpoint | Z-11, Z-06 | GATE-MODEL-01 |
| RK-19 | HIGH | Privacy removes free branch protection and CI minutes | Z-01, G-03 | GATE-PRIV-01 |
| RK-20 | HIGH | Founder OS build differs from vendor-tested lines | C-00, Z-24 | GATE-R1-EXIT |
| RK-21 | HIGH | Disk-full and mass-deletion evidence unresolved | Z-18, Z-19 | GATE-M0-EXIT |
| RK-22 | HIGH | Other projects' claims mislead execution | Z-25 | GATE-M0-EXIT |
| RK-15 | MEDIUM | npm supply chain | Q-00, F-01 | GATE-R0A-EXIT |
| RK-08 | MEDIUM | Trademark conflict on the name | N-01 | — |
| RK-18 | MEDIUM | Unsigned builds erode trust | Z-22 | GATE-PKG-01 |
| RK-25 | HIGH | Founder review bandwidth (about 35 T2 tasks in R0a–R0) | Z-06 | GATE-REV-01 |
| RK-23 | MEDIUM | Status docs contradict code | G-06, Z-04 | GATE-M0-EXIT |
| RK-24 | MEDIUM | No local code index | Z-28 | GATE-CTX-01 |

## 2. Open decisions for the founder

Each decision lists the options, the recommendation and what it unblocks. Decisions are recorded by Z-25. All sixteen were decided on 2026-11-08; the Decided column holds each answer.

| ID | Decision | Options | Recommendation | Unblocks | Decided |
|---|---|---|---|---|---|
| DEC-01 | Which reviewer routes may see private Zain content (A7); T2 sign-off follows V3 ADR-011 (founder plus security review) | (a) founder human review; (b) Alibaba OCR with the founder's ChatGPT login, authorized in writing; (c) OpenCode through the configured third-party relay; (d) local model only (advisory) | (a) for T2 sign-off; (b) as advisory review only (ChatGPT-backed OCR is the same model family as the Codex builder, so it cannot substitute for T0/T1 review of Codex-built work); local deterministic checks always; not (c) | Z-06, every T2 gate | 2026-11-08, founder in chat: founder signs off T2; OCR on the founder's ChatGPT login is authorized for private content as advisory review; local checks always; the relay (c) is not authorized |
| DEC-02 | Repository visibility | Make TheHalfMoon/Zain private now; keep public; and for wepld/wepld: private, archive or keep | Make both private before any further push | Z-01, Q-01 | 2026-11-08, founder in chat: both private. Zain private since 00:37:46Z; wepld/wepld private since 01:22:38Z (anonymous API 404) **Reversed 2026-11-08 by the founder in chat: both repositories public again since 01:31Z; everything is kept in the repository.** |
| DEC-03 | Branch protection once private on GitHub Free | Pay for GitHub Pro (breaks zero-cost rule); rely on the local base-run checker (G-03) plus founder-signed merges (G-02); keep public | G-03 + G-02, no paid plan; record that server-side protection is absent | G-07 rewording | 2026-11-08, founder in chat: no paid plan; local checker G-03 plus founder-signed merges G-02; server-side protection recorded as absent Moot while the repository is public (branch protection is free on public repositories); applies again if it goes private. |
| DEC-04 | T3 source pin | Keep 36d4d711 (all R11 manifests); re-pin to v0.1.7 tag (a9e709f1 line) | Re-pin to the v0.1.7 release tag, which has Windows CI and installers; Q-00 records the R11 deltas | Q-00, Q-01 | 2026-11-08, founder in chat: re-pin to the v0.1.7 tag at Q-00, recording the R11 deltas |
| DEC-05 | Editor parity timing | Keep LSP/DAP in R3 (V3); pull the LSP spike I-03 into R1 after Z-20 | Pull I-03 into R1 if Z-20 confirms Monaco; external editor (Z-13) covers R0–R0b | I-03, Z-20 | 2026-11-08, founder in chat: pull I-03 into R1 if Z-20 confirms Monaco; otherwise it stays in R3 |
| DEC-06 | Windows OS sandbox timing | Keep S-01 in R5; pull to R2 as the differentiator competitors lack | Pull S-01 to R2 after C-00 proves the mechanisms on the founder build | S-01 | 2026-11-08, founder in chat: S-01 moves to R2 once C-00 proves the mechanisms; otherwise it stays in R5 |
| DEC-07 | Definition of the first release | R0b founder daily driver; R0 Zain 1.0 qualified; V3 R1 "Trusted Starter" | **R0b** (changed after the scope review): use the workbench daily from about 11–20 pw instead of 26–48 pw; R0 qualifies it on daily-use evidence; R1 adds trust claims | GATE-R0B-EXIT | 2026-11-08, founder in chat: R0b is the first release |
| DEC-08 | Model policy for the no-paid path | Subscription CLIs through official login; local small models; third-party relays | Official CLI logins (Codex) for agent turns, with the per-session CODEX_HOME arrangement from V3 18; local models for completion and triage; no relays for private code | Z-10, Z-11 | 2026-11-08, founder in chat: official CLI logins (Codex) for agent turns, local models for completion and triage, no relays for private code |
| DEC-14 | Claude sessions in the V3 P2 exit (F-16) | Founder supplies an Anthropic API key (paid); make the Claude-key session optional in F-16 | Optional: F-16 passes with Codex and ACP sessions; a Claude session is tested only if the founder supplies a key | F-16 | 2026-11-08, founder in chat: optional; a Claude session is tested only if the founder supplies a key |
| DEC-16 | Response to the historical exposure found by Z-03 (18) | Accept the commit-email exposure and switch to the GitHub noreply address with email privacy settings; rewrite history (invalidates every SHA, branch and PR reference); do nothing | Accept and switch to noreply now; make or archive wepld/wepld private; identify the two other wepld identities | GATE-PRIV-03 | 2026-11-08, founder in chat: accept the exposure, no history rewrite; commits now use the GitHub noreply address. The other wepld identities are founder-owned accounts. Still open: GitHub email-privacy settings and profile email (18 P7). Both repositories public again since 01:31Z by founder choice (DEC-02 reversed) |
| DEC-15 | Update feed (F-04) hosting and signing-key custody | Private release assets with a client token (V3 forbids tokens in the client); a static host the founder controls; no auto-update before R1 | No auto-update in R0b; for R0, a founder-controlled static host with an ed25519 key held offline by the founder, or defer F-04 to R1 | F-04 | 2026-11-08, founder in chat: no auto-update in R0b; for R0 a founder-controlled static host with an ed25519 key held offline |
| DEC-09 | Governance freeze | Continue the v1–v72 successor chain; freeze it and replace with G-03 at R0 | Freeze: no v73+ during R0a/R0b; the build branch stays local; G-03 replaces the chain at R0 | G-03, G-05 | 2026-11-08, founder in chat: freeze; no v73+ during R0a/R0b; G-03 replaces the chain at R0 Amended 2026-11-08: the build branch is pushed, not kept local (founder: everything in the repository). |
| DEC-10 | Attribution of historical claims | Confirm that E4–E7, FD-4 and 70458ae belong to Ascout; say where usn-journal.csv is | Confirm, and point the agent at usn-journal.csv if it exists | Z-18, Z-25 | 2026-11-08, founder in chat: confirmed as Ascout's; the founder does not know where usn-journal.csv is, so it is treated as not found |
| DEC-11 | Admission of registry CSVs and tools | Add a governed policy successor admitting `docs/zain-master-plan/registry/*.csv` and `tools/*.py`; keep them on the planning branch until G-03 | Keep on the planning branch until G-03 replaces the chain (avoids a v73) | Z-05 merge | 2026-11-08, founder in chat: keep them on the planning branch until G-03 |
| DEC-12 | Build volume | D: after freeing space; external drive; C: after cleanup | D:, after the founder frees space to GATE-RES-01 | Z-07 | 2026-11-08, founder in chat: D:, after the founder frees it to GATE-RES-01 (15 GB free on 2026-11-08) |
| DEC-13 | E2E donor | Ascout (founder-owned, needs FO-9 relicensing confirmation); Playwright-only reimplementation | Playwright-only for Z-15 now; Ascout decision before E-03 | E-03, SRC-E2E | 2026-11-08, founder in chat: Playwright-only for Z-15; Ascout decided before E-03 |

## 3. Questions this plan could not resolve

1. **Where is `usn-journal.csv`?** No copy exists in any TheHalfMoon repository default branch, any of the 353 Zain
   remote refs, or the Orcel checkout. A disk-wide search for it was cut off when the earlier session ended. **Founder, 2026-11-08 (DEC-10):** location not known; treated as not found. **Z-18:** not found. A filename search of all of C: and D: (`dir /s /b /a-d *usn*.csv`, 2026-11-08 01:35Z, completed) returned no match; folders that need administrator rights were skipped (19 §6)
2. **Is ChatGPT (via the OCR CLI) or the Nara relay authorized for private code?** The configuration exists. No
   written authorization was found (DEC-01). **Answered 2026-11-08 (DEC-01):** OCR through the founder's ChatGPT
   login is authorized as advisory review; the third-party relay is not.
3. **GitHub Free private-repository limits.** Checked on docs.github.com on 2026-11-08: protected branches and
   rulesets are available only in public repositories on GitHub Free. Actions usage on private repositories draws on
   a small included compute allowance (the current plans page describes 12 USD per month; older pages still say
   2,000 minutes). Confirm the allowance on the billing page and set a 0 USD spending limit when making the change
   (Z-01).
