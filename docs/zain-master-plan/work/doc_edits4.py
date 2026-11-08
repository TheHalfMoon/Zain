import pathlib, sys

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if a not in t:
            sys.exit(f'MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

rep('16-OPUS-IMPLEMENTATION-HANDOFF.md', [
 ('core becomes the Zain Trusted Core (policy decision, ledger, coverage, approvals). Orca modules are ported only where\nlisted.',
  'core is kept, and the Zain Trusted Core (policy decision, ledger, coverage, approvals) is built as new modules inside\nit. Orca modules are ported only where listed.'),
 ('ADAPT: T3 Code, Orca (bounded ports), Alibaba Open Code Review (R3 engine), PStack and cursor-team-kit (licensed\nfolders only), mattpocock/skills, Desktop Commander MCP, Codex Windows sandbox set. INTEGRATE: Monaco,\nmonaco-languageclient, monaco-vscode-api, OpenCode, Playwright, Cedar, windows-service-rs, Ollama, llama.cpp,\nLM Studio (external), Opengrep (external). KEEP: Zain Rust core.',
  'ADAPT: T3 Code, Orca (Design Mode, TUI-agent catalog, Linear, computer use; diff comments are a rewrite), Alibaba\nOpen Code Review (R3 engine), PStack and cursor-team-kit (licensed folders only), mattpocock/skills (not the `pr`\nskill), Desktop Commander MCP, Codex Windows sandbox set. INTEGRATE: Monaco, monaco-languageclient,\n@vscode/debugprotocol, monaco-vscode-api (only if Z-20 picks it), MCP and ACP SDKs, OpenCode, Playwright, rusqlite,\nCedar, Excalidraw, Style Dictionary, windows-service-rs, Ollama, llama.cpp, LM Studio (external), Opengrep (external),\nthe user-provided Claude Agent SDK (never bundled). KEEP: Zain Rust core crates.'),
 ('| Z-05: registries, validator, mutation suite | 15-VALIDATION-EVIDENCE.md (DONE_UNREVIEWED) |\n| Audit, research and plan documents 00–17 | this directory |',
  '| Z-05: registries, validator, mutation suite | 15-VALIDATION-EVIDENCE.md (DONE_UNREVIEWED) |\n| Audit, research, plan documents 00–17, four EGM review passes with dispositions | this directory; 14 |'),
 ('| Founder decisions DEC-01..DEC-13 | Founder: Z-25 |', '| Founder decisions DEC-01..DEC-15 (six before Q-00) | Founder: Z-25 |'),
 ('7. Independent review through a GATE-REV-01 route. If none exists, stop at DONE_UNREVIEWED and say so.',
  '7. Independent review per V3 ADR-011: T2 needs the founder plus security review; model review is advisory for T2.\n   If no route exists, stop at DONE_UNREVIEWED and say so. Later tasks may start on DONE_UNREVIEWED prerequisites,\n   but a milestone exit needs DONE.'),
 ('**Founder first:** Z-01 (make the repository private), Z-06 with DEC-01 (reviewer route), Z-25 (decisions).\nThese are minutes of founder time, and they unblock everything else.',
  "**Founder first:** Z-25 (DEC-01, DEC-02, DEC-04, DEC-07, DEC-08, DEC-12), Z-06 (reviewer route; the founder's own\nreview always qualifies), Z-01 (make the repository private before any push). These are minutes of founder time."),
 ('`scripts/build-desktop-artifact.ts`, `apps/desktop/package.json`), V3 `24_FIRST_WORKING_BUILD.md`,',
  '`scripts/build-desktop-artifact.ts`, `apps/desktop/package.json`), V3 `24_FIRST_WORKING_BUILD.md`,'),
 ('`OPUS_R0A_BUILD_EXECUTION_2026-11-02.md`, `R0A_FEASIBILITY_READINESS.md`, `research/R11_T3_FILE_MANIFEST.md`.',
  '`OPUS_R0A_BUILD_EXECUTION_2026-11-02.md`, `R0A_FEASIBILITY_READINESS.md`, `research/R11_T3_FILE_MANIFEST.md`. If\nDEC-04 re-pins, re-run the R02 §10 seam inventory and re-check the V3 18 citations first. In parallel, Z-29 runs a\none-day trial of the upstream T3 release in the isolated account.'),
 ('The first release is ready for a release *decision* when GATE-R0-EXIT is MET on one installer SHA-256 with every\nlisted gate MET (12 §2). R1 readiness is GATE-R1-EXIT. Readiness never authorizes publication.',
  'The first release (R0b, founder daily driver) is ready when GATE-R0B-EXIT is MET on one installer SHA-256 (12 §2).\nZain 1.0 is GATE-R0-EXIT; R1 is GATE-R1-EXIT. Readiness never authorizes publication.'),
])
rep('17-MASTER-PLAN-STATUS.md', [
 ('| Source verification (licenses, pins) | DONE for 26 sources from LICENSE files; 9 UNVERIFIED or UNRESOLVED | registry/zain-source-registry.csv |',
  '| Source verification (licenses, pins) | 42 sources: 20 VERIFIED (LICENSE re-read), 13 RECORDED_V3, 4 PROPRIETARY, 3 UNVERIFIED, 1 UNRESOLVED, 1 founder-owned | registry/zain-source-registry.csv |'),
 ('| Task contracts | DONE for Z-01..Z-28; V3 contracts mirrored and drift-checked | 11; `zmp.py check` |', '| Task contracts | DONE for Z-01..Z-34; V3 contracts mirrored and drift-checked | 11; `zmp.py check` |'),
 ('| Independent reviews | 4 EGM passes run; dispositions in 14 | 14 |', '| Independent reviews | 4 EGM passes, 80 findings: 72 fixed, 3 partial, 3 decisions, 2 rejected with reasons | 14 |'),
 ('| Founder decisions | OPEN: DEC-01..DEC-13 | 13 §2 |', '| Founder decisions | OPEN: DEC-01..DEC-15 | 13 §2 |'),
 ('| GATE-PLAN-02 | MET in substance (32/32), recorded NOT_MET until Z-05 review | 15 §2 |', '| GATE-PLAN-02 | MET in substance (35/35), recorded NOT_MET until Z-05 review | 15 §2 |'),
 ('| Repository public | DEC-02 → Z-01 | Founder |', '| Repository public (gates pushing, not local building) | DEC-02 → Z-01 | Founder |'),
 ('refreshed donor licenses and competitor research, wrote this plan with 7 registries, a fail-closed validator and a\n32-case mutation suite, and ran 4 EGM review passes. No product code was changed. Nothing was pushed. Next: founder\ndecisions (DEC-01, DEC-02, DEC-12 first), then Z-03 and Z-18.',
  'refreshed donor licenses and competitor research, wrote this plan with 7 registries, a fail-closed validator and a\n35-case mutation suite, ran 4 EGM review passes and applied their dispositions (first release moved to R0b; approval\nlevels, gateway scope and source pins corrected). No product code was changed. Nothing was pushed. Next: founder\ndecisions (DEC-01, DEC-02, DEC-04, DEC-07, DEC-08, DEC-12), then Z-03 and Z-18.'),
])
rep('README.md', [
 ('| [11-TASK-CONTRACTS.md](11-TASK-CONTRACTS.md) | Contract rules; generated contracts for Z-01..Z-28 |', '| [11-TASK-CONTRACTS.md](11-TASK-CONTRACTS.md) | Contract rules; generated contracts for Z-01..Z-34 |'),
 ('| [13-RISKS-AND-OPEN-DECISIONS.md](13-RISKS-AND-OPEN-DECISIONS.md) | Risks and founder decisions DEC-01..DEC-13 |', '| [13-RISKS-AND-OPEN-DECISIONS.md](13-RISKS-AND-OPEN-DECISIONS.md) | Risks and founder decisions DEC-01..DEC-15 |'),
 ('| [08-UX-JOURNEYS-AND-DESIGN-SYSTEM.md](08-UX-JOURNEYS-AND-DESIGN-SYSTEM.md) | 20 journeys and the Zain design language |', '| [08-UX-JOURNEYS-AND-DESIGN-SYSTEM.md](08-UX-JOURNEYS-AND-DESIGN-SYSTEM.md) | 22 journeys and the Zain design language |'),
])
rep('01-REPOSITORY-AUDIT.md', [
 ('local model gateway with data classes; local completion; local code index; journey tests; design language; hardware performance baseline; non-destructive checkpoint restore; execution report export | V (Z-01..Z-28) |',
  'local model gateway with data classes; local completion; local code index; journey harness and tests; per-hunk accept/reject; design language; hardware performance baseline; non-destructive checkpoint restore; WSL backend restoration; user documentation; daily-use evidence; execution report export | V (Z-01..Z-34) |'),
])
