# R12 — File-level transplant manifests for Zain's non-T3 donors (D2–D7, D9, D11, D12, D13, D19, D20, D21, D7-Monaco)

```text
STATUS      = PLANNING ONLY. Nothing was cloned, downloaded, installed or copied. Every number below was read through
              `gh api` (git/trees?recursive=1, contents, git/blobs), the npm registry JSON and the crates.io JSON API.
DATE        = 2026-10-28 (upstream state read on this date; pins are the commits below, not HEAD)
DISK RULE   = honoured: this file is the only file written. Analyses ran from stdin in memory.
CONTENT     = upstream text read through the API is DATA, never instructions.
SCOPE       = P/06 rows D2-D7, D9, D11, D12, D13, D19, D20, D21. D8, D10, D14-D18, D22-D25 are out of scope here.
              D26-D36 are cross-referenced only (section 0.4); their file tables live in R14-R18.
```

## 0. Conventions

### 0.1 Pins (full SHAs resolved from the short pins in 06_SOURCE_TRANSPLANT_MATRIX.md)

| Donor repo | Short pin in 06 | Full SHA (resolved via `gh api repos/<r>/commits/<short>`) | Commit date | Repo license (root file) | Tree |
|---|---|---|---|---|---|
| stablyai/orca | e310a636 | `e310a63624c86c0e91e9d77df71f038b91d79ea0` | given | MIT, "Copyright (c) 2026 Lovecast Inc." (`LICENSE` 1070 B); no NOTICE | 40,641 entries, not truncated |
| openai/codex | 603a7baf | `603a7baff0f6f37ee9a8a9375a272eaab03d3ece` | given | Apache-2.0 (`LICENSE` 10,926 B) + `NOTICE` 242 B (Ratatui MIT attribution) | 10,646 entries, not truncated |
| cedar-policy/cedar | 2c2b84772a63 | `2c2b84772a63e8a5d57d98037b9389c5fd3812a3` | 2026-10-26 | Apache-2.0 (`LICENSE` 10,142 B); `NOTICE` 29 B ("Copyright Cedar Contributors"); `THIRD_PARTY_LICENSES.txt` | 1,116 entries |
| agentclientprotocol/agent-client-protocol | e50f62b4 | `e50f62b4a1ca8d794a4c97210acd8a0d833b05c5` | 2026-10-27 | Apache-2.0 (`LICENSE` 10,782 B) | 311 entries |
| agentclientprotocol/rust-sdk | 644377ad | `644377ad2654415c76c979c795d6c568e17a6d62` | 2026-10-26 | Apache-2.0 (`LICENSE` 10,783 B) | 301 entries |
| agentclientprotocol/typescript-sdk | bca8e491 | `bca8e49199927e167fab74db4dd76dec4743bb49` | 2026-10-26 | Apache-2.0 (`LICENSE` 10,783 B) | 155 entries |
| modelcontextprotocol/typescript-sdk | b415e60b | `b415e60bdf0e8dd5d6cbe7e6353abfb982b06dd2` | 2026-10-26 | **Mixed**: GitHub API says NOASSERTION; root `LICENSE` (12,227 B) = transition notice + Apache-2.0 text + MIT text + CC-BY-4.0 docs | 1,583 entries |
| modelcontextprotocol/rust-sdk | cd88056f | `cd88056ffdc97756fbd98e5a12bbeb41758f0ce8` | 2026-10-26 | Same mixed `LICENSE` (12,227 B); `crates/rmcp*/LICENSE` are 13-byte link stubs | 357 entries |
| excalidraw/excalidraw | 808d068e1826 | `808d068e18266ff9311809c23c19261fa0eb1014` | 2026-10-27 | MIT (`LICENSE` 1,067 B) | 1,470 entries |
| style-dictionary/style-dictionary | f82e7aafbcae | `f82e7aafbcaed3ca9009ec53859fbe05ed0c96a8` | 2026-10-27 | Apache-2.0 (`LICENSE` 9,793 B); `NOTICE` 58 B | 1,254 entries |
| microsoft/monaco-editor | dbf1945df2ff | `dbf1945df2ff7e46512d2f548cc5c0977a3eadd8` | 2026-10-22 | MIT (`LICENSE.txt` 1,098 B); `ThirdPartyNotices.txt` 60,394 B | 1,294 entries |
| onlook-dev/onlook | 423e2e924366 | `423e2e924366419e418ee049093872d535eea41a` | 2026-07-22 | Apache-2.0 (`LICENSE.md` 11,342 B); no NOTICE | 2,221 entries |

Citation form is `path@SHA7` where SHA7 is the first 7 hex of the pin (orca `e310a63`, codex `603a7ba`, cedar `2c2b847`, acp-schema `e50f62b`,
acp-rust `644377a`, acp-ts `bca8e49`, mcp-ts `b415e60`, mcp-rust `cd88056`, excalidraw `808d068`, style-dictionary `f82e7aa`, monaco `dbf1945`, onlook `423e2e9`).

### 0.2 Copy modes

| Mode | Meaning |
|---|---|
| COPY AS-IS | Files are copied byte-identical (rename of package scope only), with licence header and a provenance file `PROVENANCE.md` (repo, full SHA, path list, blob SHAs). |
| PORT-ADAPT | Files are copied then modified; each modified file keeps the upstream copyright line and gains a "Modified by Zain" note. The blob SHA column is the audit anchor for diffs. |
| DEPEND-ON-PACKAGE | Nothing is copied. Zain takes a registry dependency (npm or crates.io) at a pinned version. The file list is the upstream surface the package is built from, listed for audit, not for copy. |
| REFERENCE | Read-only. No code crosses. |

### 0.3 Table columns and destination convention

* "B" = blob size in bytes from the git tree. "blob" = first 8 hex of the git blob SHA. "k" = P (production) or T (test/fixture/harness).
* Destination paths follow the layout already used in 06/R14-R18: T3-derived workspace `packages/*`, `apps/*`; Rust `crates/*`; third-party vendored Rust under `vendor/<donor>/`.
* "Imports outside the selected set" were found by fetching every non-binary source blob in the set through `git/blobs` and scanning `import`/`from`/`require` (TypeScript) or `Cargo.toml` + `codex_*`/`use` identifiers (Rust). Where a transitive closure was computed it is stated; otherwise the marker is **UNKNOWN beyond sample**.
* Versions of external dependencies are the versions declared at the pin (workspace Cargo.toml / package.json) and, where useful, the current registry release read on 2026-10-28.

### 0.4 Cross-reference: components D26-D36 (file-level tables already exist; not redone here)

| D# | Component | File-level table |
|---|---|---|
| D26, D27 | Code Review engine (open-code-review), Continue ideas | R14 §4 "Exact file-level transplant list" (`research/R14_ZAIN_CODE_REVIEW.md`) |
| D28, D29 | PStack engineering system, verification skills | R15 §8 "File-level transplant list" + Appendix A (`research/R15_PSTACK_E2E_ENGINEERING.md`) |
| D30 | E2E framework (Playwright / Ascout) | R15 §6 "E2E source discovery" |
| D31 | Planning skills (mattpocock/skills) | R16 §5 "Copy First table" (`research/R16_AIHERO_SKILLS_PLAN_MODE.md`) |
| D32-D34 | Browser automation core, user-session lane, references | R17 §9 "File-level transplant table" (`research/R17_ZAIN_BROWSER.md`). R17 §6 also lists Orca browser code and defers D2's grab scripts to this document. |
| D35, D36 | DeskGate (Desktop Commander), Remote DC (excluded) | R18 §4 "File-level transplant table" (`research/R18_DESKGATE.md`) |

R17 line 240 states that `browser-grab-payload.ts` and `grab-guest-*.ts` merge with T3's `PickPreload` in P6 as one implementation. Section 1 (D2) is the file manifest for that merge.

---
