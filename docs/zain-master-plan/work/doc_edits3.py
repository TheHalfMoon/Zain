import pathlib, sys

def rep(fname, pairs):
    p = pathlib.Path(fname); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if a not in t:
            sys.exit(f'ANCHOR MISSING in {fname}: {a[:80]!r}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', fname)

# ---------------- 10 roadmap
rep('10-ROADMAP-AND-CRITICAL-PATH.md', [
    ('| **M0** Privacy and repository control | Repository private; app egress closed; exposure assessed; PRs reconciled; reviewer route chosen; incident note; founder decisions | Founder accepts starting M0 | GATE-M0-EXIT |',
     '| **M0** Privacy and repository control | Repository private; app egress closed; exposure assessed; PRs reconciled; reviewer route chosen; incident note; founder decisions | Founder accepts starting M0 | GATE-M0-EXIT (runs in parallel with R0a; it gates pushing, not local building) |'),
    ('| **R0a** First Working Build | Locally built unsigned installer; isolated smoke with a real provider turn | M0 exit; Z-07..Z-10; V3 A3–A7 evidence | GATE-R0A-EXIT |',
     '| **R0a** First Working Build | Locally built unsigned installer; isolated smoke with a real provider turn; one-day trial of upstream T3 (Z-29) | Z-25 decisions DEC-01/02/04/07/08/12; Z-06 reviewer route; Z-07 capacity; Z-08 toolchain (V3 A3–A7). Local work only | GATE-R0A-EXIT |'),
    ('| **R0b** Tester build | No telemetry; keyring credentials; supervised default; clean uninstall; open-in-editor; non-destructive revert; baseline measured | R0a PASS | GATE-R0B-EXIT |',
     '| **R0b** First release: founder daily driver | No telemetry; keyring credentials; supervised default; clean uninstall; open-in-editor; per-hunk accept/reject; non-destructive revert; journey harness; baseline measured | R0a PASS | GATE-R0B-EXIT |'),
    ('| **R0** Zain 1.0 private daily driver | Strip/rebrand/admission; governance reset (G-03); model gateway; design language; journeys J02–J18; recovery; validator repaired | R0b exit | GATE-R0-EXIT |',
     '| **R0** Zain 1.0 qualified | Strip/rebrand/admission; governance reset (G-03); model gateway; design language; WSL backend; journeys J02–J22; recovery; docs; validator repaired; 10 days of daily-use evidence | R0b exit | GATE-R0-EXIT |'),
    ('- **What R1 costs.** R1 adds 50–76 pw on top of R0\'s cumulative 23–42 pw. That gap is why the first release is R0\n  (DEC-07).',
     '- **What R1 costs.** R1 adds 50–76 pw on top of R0\'s cumulative 26–48 pw, and R0 itself adds 16–28 pw on top of\n  R0b\'s 11–20 pw. That is why the first release is R0b (DEC-07).\n- **Founder review time is not in these numbers.** About 35 T2 tasks in R0a–R0 need the founder\'s review (RK-25).\n  At roughly half a day each, that is several founder-weeks spread across the critical path.\n- **Open-ended tasks are timeboxed.** Q-06 and F-21 are MEASURE tasks. Each gets a 2 pw timebox; when it runs out,\n  the founder decides whether to continue, cut scope, or record FEASIBILITY_COMPLETE_WITH_FAILURES.'),
    ('- **Scope honesty.** The full ladder (192–318 pw known work) is not feasible', '- **Scope honesty.** The full ladder (196–324 pw known work) is not feasible'),
    ('| M0-founder | Z-01, Z-02, Z-06, Z-25 | M0-agent |', '| M0-founder | Z-01, Z-02, Z-06, Z-25 | M0-agent and the R0a prerequisites |'),
    ('| R0a-prereq | Z-07, Z-08, Z-09, Z-10 | Z-26 validator repair; Q-00 read-only inventory |', '| R0a-prereq | Z-07, Z-08, Z-09, Z-10, Z-29 | M0 tasks; Z-26 validator repair; Q-00 read-only inventory |'),
    ('| R0b-product | Z-13, Z-14, Z-27 after Q-05 | V3 R0b tasks F-05, F-07, F-22, N-01, Y-00 |', '| R0b-product | Z-13, Z-14, Z-27, Z-30, Z-31 after Q-05 | V3 R0b tasks F-05, F-07, F-22, N-01, Y-00 |'),
    ('| R0-product | Z-11, Z-17, Z-21 | V3 governance reset G-03/G-05/G-08 |', '| R0-product | Z-11, Z-17, Z-21, Z-33 | V3 governance reset G-03/G-05/G-08; Z-32 daily-use log; Z-34 docs |'),
    ('| R1 | Z-12, Z-20, Z-28 after F-17; C-00 spikes | Core C-02..C-06 chain |', '| R1 | Z-20 first, then F-17, then Z-12 and Z-28; C-00 spikes | Core C-02..C-06 chain |'),
    ('    Z01[Z-01 private repo] --> Q01\n    Z02[Z-02 app egress] --> Q01\n    Z06[Z-06 reviewer route] --> Q01\n    Z03[Z-03 exposure] ; Z04[Z-04 PRs] ; Z18[Z-18 incident] ; Z25[Z-25 decisions] ; Z05[Z-05 registries]',
     '    Z06[Z-06 reviewer route] --> Q01\n    Z25[Z-25 decisions] --> Q00\n    Z01[Z-01 private repo] ; Z02[Z-02 app egress] ; Z03[Z-03 exposure] ; Z04[Z-04 PRs] ; Z18[Z-18 incident] ; Z05[Z-05 registries]'),
    ('    Z09[Z-09 test account] --> Q05 ; Z10[Z-10 provider route] --> Q05\n', '    Z09[Z-09 test account] --> Q05 ; Z10[Z-10 provider route] --> Q05\n    Z09 --> Z29[Z-29 upstream trial]\n'),
    ('    Q05 --> Z13[Z-13 external editor] & Z14[Z-14 perf baseline] & Z27[Z-27 safe revert]\n',
     '    Q05 --> Z13[Z-13 external editor] & Z14[Z-14 perf baseline] & Z27[Z-27 safe revert] & Z30[Z-30 harness] & Z31[Z-31 hunk accept/reject]\n'),
    ('    F16 --> Z15 ; Z11[Z-11 model gateway] --> Z15 ; Z13 --> Z15\n', '    F16 --> Z15 ; Z11[Z-11 model gateway] --> Z15 ; Z13 --> Z15 ; Z30 --> Z15 ; Z17 --> Z15\n    Z17 --> F14\n'),
    ('The complete graph (429 edges)', 'The complete graph (440 edges)'),
])

# ---------------- 11 contracts
rep('11-TASK-CONTRACTS.md', [
    ('SOURCES  = registry/zain-task-backlog.csv (204 rows) · registry/zain-dependency-edges.csv', 'SOURCES  = registry/zain-task-backlog.csv (210 rows) · registry/zain-dependency-edges.csv (440 edges)'),
    ('SCOPE    = 28 new master-plan tasks (Z-01..Z-28) in full below; 176 V3 tasks by reference', 'SCOPE    = 34 master-plan tasks (Z-01..Z-34) in full below; 176 V3 tasks by reference'),
    ('1. **Entry.** All prerequisites and gate edges are DONE (or NOT_NEEDED). The task\'s spec note exists. Its tests are\n   written first and fail for the right reason.',
     '1. **Entry.** All prerequisites and gate edges are DONE, DONE_UNREVIEWED or NOT_NEEDED. The task\'s spec note exists.\n   Its tests are written first and fail for the right reason. A milestone exit gate needs its T2 tasks fully DONE.'),
    ('| Q-01 import | Z-01, Z-02, Z-06, Z-07, Z-08 | Repository public; AI review apps; no authorized reviewer (A7); C: 3.4 GB free; Node 24.19.0 / pnpm 9.12.0 vs pins |',
     '| Q-00 admission | Z-25 | Pin (DEC-04), provider route (DEC-08) and build volume (DEC-12) must be decided first |\n| Q-01 import | Z-06, Z-07, Z-08 | No authorized reviewer (A7); C: 3.4 GB free; Node 24.19.0 / pnpm 9.12.0 vs pins. Repository privacy (Z-01) gates pushing, not a local import of public MIT source (ADR-Z04) |'),
    ('**Re-pin question (DEC-04).**', '**Timeboxes.** Q-06 and F-21 (MEASURE) get 2 pw each; when exhausted the founder decides (10 §3).\n\n**Re-pin question (DEC-04).**'),
    ('re-pin to the release tag, with the R11 manifest deltas for changed files.', 're-pin to the release tag, with the R11 manifest deltas for changed files, a re-run of the R02 §10 seam inventory and a\nre-check of the V3 18 file:line citations at the new pin.\n\n**Amending V3 contracts.** Z-24 and Z-26 change V3 text. Amendments go in a separate commit that edits only the\nnamed V3 rows, carries the founder\'s approval, and passes `plan_graph.py --check` and `zmp.py check`. The DEC-09\nfreeze applies to governance policy successors (v73+), not to planning documents.'),
])

# ---------------- 13 risks and decisions
rep('13-RISKS-AND-OPEN-DECISIONS.md', [
    ('RISKS     = registry/zain-risk-register.csv (24 risks;', 'RISKS     = registry/zain-risk-register.csv (25 risks;'),
    ('DECISIONS = DEC-01..DEC-13 below;', 'DECISIONS = DEC-01..DEC-15 below;'),
    ('| RK-03 | CRITICAL | Full V3 scope (192–318 pw including this plan\'s tasks) exceeds solo capacity | Z-25 scope decision; initial release = R0 | GATE-R0-EXIT |',
     '| RK-03 | CRITICAL | Full V3 scope (196–324 pw including this plan\'s tasks) exceeds solo capacity | Z-25 scope decision; first release = R0b; Z-32 daily-use evidence | GATE-R0-EXIT, GATE-USE-01 |'),
    ('| RK-23 | MEDIUM |', '| RK-25 | HIGH | Founder review bandwidth (about 35 T2 tasks in R0a–R0) | Z-06 | GATE-REV-01 |\n| RK-23 | MEDIUM |'),
    ('| DEC-01 | Which reviewer routes may see private Zain content (A7) |', '| DEC-01 | Which reviewer routes may see private Zain content (A7); T2 sign-off follows V3 ADR-011 (founder plus security review) |'),
    ('| (a) for T2 sign-off, plus (b) if the founder authorizes ChatGPT for private code; local deterministic checks always; not (c) |',
     '| (a) for T2 sign-off; (b) as advisory review only (ChatGPT-backed OCR is the same model family as the Codex builder, so it cannot substitute for T0/T1 review of Codex-built work); local deterministic checks always; not (c) |'),
    ('| DEC-07 | Definition of the first release | V3 R1 "Trusted Starter"; R0 "private daily driver" with no trust claims | R0 + Z R0 tasks as Zain 1.0 private daily driver; R1 adds trust claims | GATE-R0-EXIT | — |',
     '| DEC-07 | Definition of the first release | R0b founder daily driver; R0 Zain 1.0 qualified; V3 R1 "Trusted Starter" | **R0b** (changed after the scope review): use the workbench daily from about 11–20 pw instead of 26–48 pw; R0 qualifies it on daily-use evidence; R1 adds trust claims | GATE-R0B-EXIT | — |'),
    ('| DEC-08 | Model policy for the no-paid path | Subscription CLIs through official login; local small models; third-party relays | Official CLI logins (Codex) for agent turns; local models for completion, embeddings and triage; no relays for private code | Z-10, Z-11 | — |',
     '| DEC-08 | Model policy for the no-paid path | Subscription CLIs through official login; local small models; third-party relays | Official CLI logins (Codex) for agent turns, with the per-session CODEX_HOME arrangement from V3 18; local models for completion and triage; no relays for private code | Z-10, Z-11 | — |\n| DEC-14 | Claude sessions in the V3 P2 exit (F-16) | Founder supplies an Anthropic API key (paid); make the Claude-key session optional in F-16 | Optional: F-16 passes with Codex and ACP sessions; a Claude session is tested only if the founder supplies a key | F-16 | — |\n| DEC-15 | Update feed (F-04) hosting and signing-key custody | Private release assets with a client token (V3 forbids tokens in the client); a static host the founder controls; no auto-update before R1 | No auto-update in R0b; for R0, a founder-controlled static host with an ed25519 key held offline by the founder, or defer F-04 to R1 | F-04 | — |'),
])

# ---------------- 09 performance
rep('09-PERFORMANCE-PLAN.md', [
    ('PRINCIPLE = targets come from measurements on the founder\'s machine against the unchanged donor build, not from',
     'PRINCIPLE = targets come from measurements on the founder\'s machine against the upstream T3 release build, not from'),
    ('**Why these provisional numbers.** The ratios against the donor build (1.10× and 1.15×) bound Zain\'s added cost,\nsince a fork should not be much slower than its donor. The absolute ceilings are deliberately loose for a 16 GB\nlaptop with an integrated GPU. Z-14 replaces both with measured values before R0 exit.',
     '**Why these provisional numbers.** The ratios against the upstream release build (1.10× and 1.15×) bound Zain\'s\nadded cost, since a fork should not be much slower than its donor. The absolute ceilings are deliberately loose for a\n16 GB laptop with an integrated GPU. **Final thresholds** are min(absolute ceiling, upstream median × ratio), set from\nZ-14\'s measurements and approved by the founder, so no gate can pass itself. The 50k-file fixture is a pinned commit\nof a large public repository recorded in Z-14. The local completion model and quantization are named in Z-12.'),
])
