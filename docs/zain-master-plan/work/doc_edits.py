"""Targeted prose corrections after the EGM reviews (run from docs/zain-master-plan). Fails if an anchor is missing."""
import pathlib, sys

def rep(fname, pairs):
    p = pathlib.Path(fname); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if a not in t:
            sys.exit(f'ANCHOR MISSING in {fname}: {a[:70]!r}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', fname)

# privacy: no personal paths or relay host names in documents (Review D-R17)
for f in ('01-REPOSITORY-AUDIT.md', '07-SECURITY-AND-CONTAINMENT.md'):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    t = t.replace('C:\\Users\\<user>\\OneDrive\\Desktop\\wepld', '%USERPROFILE%\\OneDrive\\Desktop\\wepld').replace('`C:\\Users\\<user>` and `D:\\`', 'the user profile and `D:\\`')
    t = t.replace('C:\\Users\\<user>', '%USERPROFILE%')
    p.write_text(t, encoding='utf-8')
rep('06-MODELS-CONTEXT-AND-REVIEW.md', [('OpenCode configured through a third-party relay (<relay-host>)', 'OpenCode configured through a third-party relay')])
rep('13-RISKS-AND-OPEN-DECISIONS.md', [('(c) OpenCode through the third-party relay <relay-host>', '(c) OpenCode through the configured third-party relay')])

# 01: citations (D-R15)
rep('01-REPOSITORY-AUDIT.md', [
    ('| 9 | Git binary on Windows is the first `git.exe` on PATH, no signature or version check; `--no-lazy-fetch` needs Git ≥ 2.44 (`crates/core/src/git_topology.rs:338-341`) | V / I | C-12 hardening |',
     '| 9 | Git binary is found by PATH lookup with no signature check (`crates/core/src/git_topology.rs:272`); the Git version is not observed (`:333`) although `--no-lazy-fetch` (`:43`) needs Git ≥ 2.44 | V / I | C-12 hardening |'),
    ('(14 §PF line 28, CI-02, PKG-02, 24 §6, 22 §63)', '(14_TASK_CATALOG.md:28, CI-02, PKG-02, 24_FIRST_WORKING_BUILD.md:86, 22_SOURCE_ADMISSION_QUALIFICATION.md:63)'),
])

# 04: pins, license states, LOCAL_ONLY, counts, DEC-04, Codex
rep('04-SOURCE-STRATEGY.md', [
    ('VERIFIED  = 2026-11-08, gh read-only API (repo metadata, HEAD commit, releases, LICENSE file contents, nested license scan)',
     'VERIFIED  = LICENSE file re-read on 2026-11-08 through the gh read-only API (20 sources); RECORDED_V3 = license verified by V3 research at its pin, not re-read (13)'),
    ('| COPY | Use the source as-is under its license | license VERIFIED, pinned commit, not strong copyleft |',
     '| COPY | Use the source as-is under its license | license VERIFIED or RECORDED_V3, pinned commit, not strong copyleft (any AND-term that is GPL/AGPL/SSPL without a permissive OR-alternative) |'),
    ('| ADAPT | Fork and modify into Zain-owned code | same as COPY |', '| ADAPT | Fork and modify into Zain-owned code | same as COPY; a COPY/ADAPT capability needs at least one COPY/ADAPT/KEEP source |'),
    ('| Zain Rust core (S1/S2) | **KEEP** | main 0a843a2 | founder-owned (no LICENSE file) | — |',
     '| Zain Rust core (S1/S2) | **KEEP** (identity, git topology, framing; the ledger and policy engine are new modules, REIMPLEMENT) | main 0a843a2 | founder-owned (no LICENSE file) | — |'),
    ('**re-pin decision DEC-04** |', '**re-pin decision DEC-04**; full notices obligation (MIT, Apache-2.0, OFL-1.1, CC0, BSD entries); jszip→MIT and dompurify→Apache-2.0 elections; heic-to, electron-webauthn, @cursor/sdk removed (V3 22 §2) |'),
    ('| Orca `stablyai/orca` | ADAPT (bounded ports only) | pin e310a636 / HEAD 26179069 | MIT | Latest commit deleted 763 tests; rebaseline before porting |',
     '| Orca `stablyai/orca` | ADAPT (bounded ports only: Design Mode, TUI-agent catalog, Linear, computer-use helpers; diff comments are a rewrite) | pin e310a636 / HEAD 26179069 | MIT | Latest commit deleted 763 tests; rebaseline before porting |'),
    ('| Alibaba Open Code Review | ADAPT (engine fork, R3) | pin 375f64cd / v1.13.6 |', '| Alibaba Open Code Review | ADAPT (engine fork, R3) | pin 375f64cd (= v1.13.3) / current v1.13.6 |'),
    ('| PStack and cursor-team-kit (`cursor/plugins`) | ADAPT | 6b0300214a09 |', '| PStack and cursor-team-kit (`cursor/plugins`) | ADAPT | pin ab1f702c / HEAD 6b0300214a09 |'),
    ('| AI Hero skills `mattpocock/skills` | ADAPT | pin 59db609e / v1.3.2 | MIT | Re-pin |', '| AI Hero skills `mattpocock/skills` | ADAPT | pin 59db609e / v1.3.2 | MIT | Re-pin; exclude the `pr` skill (third-party content, V3 R16) |'),
    ('| OpenAI Codex | ADAPT (Windows sandbox set, S-01) | 603a7baff0f6 | Apache-2.0 | Windows sandbox now default-on upstream |',
     '| OpenAI Codex | ADAPT (Windows sandbox set, S-01: restricted token, ACLs, firewall; not AppContainer) | 603a7baff0f6 | Apache-2.0 (RECORDED_V3) | Default-on upstream; elevated backend needs admin and windows-sandbox-service (reference only); bubblewrap not vendored |'),
    ('| Monaco, monaco-languageclient, monaco-vscode-api | INTEGRATE | see registry | MIT | — |',
     '| Monaco, monaco-languageclient, monaco-vscode-api, @vscode/debugprotocol | INTEGRATE | see registry | MIT | monaco-vscode-api replaces monaco-editor, so it is conditional on Z-20 |'),
    ('| Playwright, Cedar, windows-service-rs, Ollama, llama.cpp, LM Studio, Opengrep | INTEGRATE (external or bounded) | see registry | Apache/MIT/LGPL-2.1/proprietary app | Several **UNVERIFIED** this pass; verify at admission |',
     '| Playwright, Cedar, rusqlite, MCP TypeScript SDK, ACP SDKs, Excalidraw, Style Dictionary, windows-service-rs, Ollama, llama.cpp, LM Studio, Opengrep, Claude Agent SDK (user-provided) | INTEGRATE (external or bounded) | see registry | Apache/MIT/mixed MIT+Apache+CC-BY (MCP SDK)/LGPL-2.1/proprietary | Mostly RECORDED_V3 or UNVERIFIED; verify at admission; Claude SDK never bundled |'),
    ('| Vercel Workflow, durable-harness | REFERENCE (patterns) | 4beb5bcc / badd648d |', '| Vercel Workflow, durable-harness | REFERENCE (patterns) | pins af8c6d32 / ea8aa406 (HEADs 4beb5bcc / badd648d) |'),
    ('| E2E (candidate Ascout) | DEFER | 70458aed |', '| E2E (candidate Ascout) | DEFER | pin ecada2bc / HEAD 70458aed |'),
    ('| ADAPT | 29 | Desktop shell, terminal, worktrees, diff review, checkpoints (T3); review engine (OCR); engineering loop (PStack); DeskGate (Desktop Commander); OS sandbox (Codex) |',
     '| ADAPT | 29 | Desktop shell, terminal, worktrees, diff review, checkpoints (T3); review engine (OCR, R3); engineering loop (PStack); DeskGate (Desktop Commander); OS sandbox (Codex); Design Mode capture (Orca) |'),
    ('| REIMPLEMENT | 19 | Model gateway with data classes, local completion, local code index, approvals, ProcessHost, file gate, design language, report export |',
     '| REIMPLEMENT | 22 | Trusted Core ledger and policy (inside the kept crates), delegated review, model gateway, local completion, local code index, approvals, ProcessHost, file gate, design language, design studio canvas, report export |'),
    ('| KEEP | 1 | Trusted Core PDP and ledger on the existing Rust core |\n', ''),
    ('| DEFER / REJECT | 3 / 3 |', '| DEFER / REJECT | 3 / 3 |'),
    ('5. **No public donor content.** Until the repository is private (Z-01), donor source, built artifacts and package\n   scans stay local (V3 OPUS packet).',
     '5. **No public donor content, and LOCAL_ONLY builds.** Donor source, built artifacts and package scans stay on the founder\n   machine (V3 OPUS packet A4/A3-06). Privacy alone is not enough: a private build repository needs a separate verified\n   decision on billing, collaborators, retention and quotas before any transfer.'),
    ('The founder reports permission to use the selected donor sources. This plan treats that as intent, not proof. Every\nsource above that is reused carries a license verified from its LICENSE file. Where rights could not be verified\n(PStack root, Ascout relicensing, Onlook, several INTEGRATE dependencies), the registry says UNVERIFIED or UNRESOLVED\nand reuse waits for admission.',
     'The founder reports permission to use the selected donor sources. This plan treats that as intent, not proof. Every\nCOPY/ADAPT source carries a license that is either re-read from its LICENSE file this pass (VERIFIED) or recorded by\nV3 at its pin (RECORDED_V3). PStack and cursor-team-kit are verified per folder; their repository root has no license.\nWhere rights are unknown (Ascout relicensing, several INTEGRATE dependencies), the registry says UNVERIFIED or\nUNRESOLVED and reuse waits for admission (F-01, LIC-01).'),
])
