# 04 — Source Registry and Copy-First Decisions

```text
REGISTRY  = registry/zain-source-registry.csv (35 sources) · registry/zain-capability-matrix.csv (decisions per capability)
VERIFIED  = LICENSE file re-read on 2026-11-08 through the gh read-only API (20 sources); RECORDED_V3 = license verified by V3 research at its pin, not re-read (13)
BASELINE  = V3 06_SOURCE_TRANSPLANT_MATRIX.md, 22_SOURCE_ADMISSION_QUALIFICATION.md, research/R06, R11, R12, R13
RULE      = owner permission statements do not replace license verification; unverifiable rights → independent implementation
```

## 1. Decision vocabulary and the rules `zmp.py` enforces

| Decision | Meaning | Enforced rule |
|---|---|---|
| COPY | Use the source as-is under its license | license VERIFIED or RECORDED_V3, pinned commit, not strong copyleft (any AND-term that is GPL/AGPL/SSPL without a permissive OR-alternative) |
| ADAPT | Fork and modify into Zain-owned code | same as COPY; a COPY/ADAPT capability needs at least one COPY/ADAPT/KEEP source |
| INTEGRATE | Bounded dependency or external process | not strong copyleft; admission at task time (F-01, LIC-01) |
| REIMPLEMENT | No suitable source; build in Zain | — |
| KEEP | Existing Zain code stays | — |
| REFERENCE | Read for design only; no code copied | capabilities may not COPY/ADAPT from it |
| DEFER | Out of scope for now | — |
| REJECT | Unsuitable (license, abandonment, proprietary) | capabilities may not COPY/ADAPT from it |

## 2. Source decisions (summary of the registry)

| Source | Decision | Pinned / current | License (from LICENSE file) | Change since 2026-10-27 that matters |
|---|---|---|---|---|
| T3 Code `pingdotgg/t3code` | **ADAPT** (hard fork; ADR-001) | pin 36d4d711 / HEAD a9e709f1, v0.1.7 (2026-11-04) | MIT | Upstream moved fast; v0.1.7 ships Windows installers from CI; Electron 44.10.1; **re-pin decision DEC-04**; full notices obligation (MIT, Apache-2.0, OFL-1.1, CC0, BSD entries); jszip→MIT and dompurify→Apache-2.0 elections; heic-to, electron-webauthn, @cursor/sdk removed (V3 22 §2) |
| Zain Rust core (S1/S2) | **KEEP** (identity, git topology, framing; the ledger and policy engine are new modules, REIMPLEMENT) | main 0a843a2 | founder-owned (no LICENSE file) | — |
| Orca `stablyai/orca` | ADAPT (bounded ports only: Design Mode, TUI-agent catalog, Linear, computer-use helpers; diff comments are a rewrite) | pin e310a636 / HEAD 26179069 | MIT | Latest commit deleted 763 tests; rebaseline before porting |
| Alibaba Open Code Review | ADAPT (engine fork, R3) | pin 375f64cd (= v1.13.3) / current v1.13.6 | Apache-2.0 | Patches Z-P1..Z-P7 need rebasing; logo is a brand mark (exclude) |
| PStack and cursor-team-kit (`cursor/plugins`) | ADAPT | pin ab1f702c / HEAD 6b0300214a09 | MIT per folder; **no root license** | Take files only from folders with a LICENSE |
| AI Hero skills `mattpocock/skills` | ADAPT | pin 59db609e / v1.3.2 | MIT | Re-pin; exclude the `pr` skill (third-party content, V3 R16) |
| Desktop Commander MCP | ADAPT (adapters behind Core) | pin db3430f2 / v0.3.1 | MIT | Re-pin |
| OpenAI Codex | ADAPT (Windows sandbox set, S-01: restricted token, ACLs, firewall; not AppContainer) | 603a7baff0f6 | Apache-2.0 (RECORDED_V3) | Default-on upstream; elevated backend needs admin and windows-sandbox-service (reference only); bubblewrap not vendored |
| OpenCode `anomalyco/opencode` | INTEGRATE (worker) | 3bf90a2406b0 | MIT | Repository moved from `sst/`; v2.2.x |
| Monaco, monaco-languageclient, monaco-vscode-api, @vscode/debugprotocol | INTEGRATE | see registry | MIT | monaco-vscode-api replaces monaco-editor, so it is conditional on Z-20 |
| Playwright, Cedar, rusqlite, MCP TypeScript SDK, ACP SDKs, Excalidraw, Style Dictionary, windows-service-rs, Ollama, llama.cpp, LM Studio, Opengrep, Claude Agent SDK (user-provided) | INTEGRATE (external or bounded) | see registry | Apache/MIT/mixed MIT+Apache+CC-BY (MCP SDK)/LGPL-2.1/proprietary | Mostly RECORDED_V3 or UNVERIFIED; verify at admission; Claude SDK never bundled |
| Vercel Workflow, durable-harness | REFERENCE (patterns) | pins af8c6d32 / ea8aa406 (HEADs 4beb5bcc / badd648d) | Apache-2.0 | `world-local` is dev/test quality; `world-postgres` has no auth |
| sandbox-runtime `anthropics/sandbox-runtime` | REFERENCE | 27fce0db | Apache-2.0 | Moved org; **opt-in Windows MXC backend** at HEAD |
| Continue | REFERENCE (rule importer only) | 5522c6f4 (unchanged) | Apache-2.0 + CLA | Read-only, unmaintained |
| Graft / Trail-code | REFERENCE (not adopted) | 8c974dc5 | MIT | `trail init` writes to `~/.claude.json` and `~/.codex/config.toml`; telemetry on by default |
| VS Code / Code-OSS | REFERENCE (Z-20 spike only) | b4bd9bd3 | MIT + notices; trademarks | Marketplace excludes forks |
| Zed | REFERENCE | b5cd310b | GPL-3.0 (215 crates) + Apache-2.0 (38) | No AGPL crates now; GPL still blocks reuse |
| Theia | REFERENCE | 8179891f | EPL-2.0 or GPL-2.0 w/ CPE | — |
| Cline, Aider | REFERENCE | see registry | Apache-2.0 | Aider dormant |
| Amp | REFERENCE (patterns only) | — | proprietary | — |
| E2E (candidate Ascout) | DEFER | pin ecada2bc / HEAD 70458aed | Apache-2.0 per API only | FO-9 relicensing confirmation open (DEC-13) |
| Onlook | DEFER (V3 says ADAPT for R4) | 423e2e92 | Apache-2.0 (not re-checked) | Re-verify before R4 |
| Roo Code | REJECT | archived | Apache-2.0 | Shut down |
| Remote Desktop Commander | REJECT | 7aaa331e | all rights reserved | Proprietary |

## 3. Capability-to-source mapping highlights

The full mapping is in `registry/zain-capability-matrix.csv`. The validator checks that every COPY/ADAPT capability
names a source, that no reuse comes from a REJECT or REFERENCE source, and that early-release capabilities have a
verification gate.

| Decision | Count | Examples |
|---|---|---|
| ADAPT | 29 | Desktop shell, terminal, worktrees, diff review, checkpoints (T3); review engine (OCR, R3); engineering loop (PStack); DeskGate (Desktop Commander); OS sandbox (Codex); Design Mode capture (Orca) |
| REIMPLEMENT | 22 | Trusted Core ledger and policy (inside the kept crates), delegated review, model gateway, local completion, local code index, approvals, ProcessHost, file gate, design language, design studio canvas, report export |
| INTEGRATE | 4 | Monaco, LSP and debug clients, MCP/skills extensions |
| DEFER / REJECT | 3 / 3 | VS Code extension compatibility, CI investigation, code signing / Orca as foundation, Zed reuse, Remote DC relay |

## 4. Provenance and rebranding rules

1. **Keep every license and notice.** Preserve donor LICENSE and NOTICE files, Monaco/VS Code `ThirdPartyNotices`, and
   nested notices in T3 (opencode, Ghostty, Expo, Bluesky, VoidZero). For Apache-2.0 files, add a change notice to
   each modified file (§4(b)).
2. **Rebrand the product, not the provenance.** Product-facing names, icons, identifiers, installers and the CLI become
   Zain (F-03, N-02, N-03, Z-17). Copyright lines and attribution stay intact. No donor trademarks in shipped branding:
   T3, Orca, OpenCode, Desktop Commander, Trail, PStack, "AI Hero", the OCR logo, VS Code and Eclipse marks.
3. **Record provenance per file.** Each imported or adapted file keeps a provenance entry: source repository, commit,
   path, license, modification note. F-01 admission and LIC-01/LIC-02 tests check this.
4. **No silent re-pins.** A donor commit change is a Q-00-style admission event with its own license and closure check.
5. **No public donor content, and LOCAL_ONLY builds.** Donor source, built artifacts and package scans stay on the founder
   machine (V3 OPUS packet A4/A3-06). Privacy alone is not enough: a private build repository needs a separate verified
   decision on billing, collaborators, retention and quotas before any transfer.

## 5. Owner-permission statement

The founder reports permission to use the selected donor sources. This plan treats that as intent, not proof. Every
COPY/ADAPT source carries a license that is either re-read from its LICENSE file this pass (VERIFIED) or recorded by
V3 at its pin (RECORDED_V3). PStack and cursor-team-kit are verified per folder; their repository root has no license.
Where rights are unknown (Ascout relicensing, several INTEGRATE dependencies), the registry says UNVERIFIED or
UNRESOLVED and reuse waits for admission (F-01, LIC-01). No proprietary source (Amp, Remote Desktop Commander, the Claude Agent SDK's
commercial terms) is copied.
