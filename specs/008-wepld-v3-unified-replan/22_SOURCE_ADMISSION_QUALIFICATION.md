# 22 — Source Admission and License Qualification Matrix (Astro M-1)

```text
STATUS = PROPOSED decisions; admission happens per task (GOV-07) and is enforced by LIC-01 / GV-16.
LEVELS = L1 exists at pin · L2 root license checked · L3 dependency closure listed · L4 redistribution approved
         (license + notice + closure + build inclusion decided). Only L4 sources may ship in a release.
EVIDENCE = 06, research/R11 §5, research/R12, Astro round-1 spot checks (15 license files, 14 pins)
```

## 1. Donor roots

| Source @pin | License (L2) | Closure (L3) | v1 decision | Gate |
|---|---|---|---|---|
| pingdotgg/t3code @36d4d711 | MIT (Astro-checked) | R11: 406 dependency rows, 28 kept package.json | RETAIN (fork) with §2 removals | F-01 admission (SRC-01, LIC-01) |
| stablyai/orca @e310a636 | MIT | R12: D2 near-closed (6 modules); D3 44 shared modules; D4 closed; D7 489 modules | D4 reference only (C-25 replaces taskkill); D2 port at I-05; D3 port with listed closure at I-06 (installers excluded); D7 REWRITE at I-02 | per-task admission |
| openai/codex @603a7baf | Apache-2.0 | R12 D9: needs codex-protocol, codex-utils-pty, codex-otel, codex-http-client; `windows-sandbox-service` needs `codex-core` (Cargo.toml L23) | **post-v1 (R5)**: adapt sandbox crates only with their closure; windows-sandbox-service REFERENCE only; bubblewrap vendor tree (LGPL-2.0) NOT vendored — system bwrap; `rama =0.3.0-alpha.4` pinned or replaced | S-01 admission (estimate raised to 4–8 pw) |
| alibaba/open-code-review @375f64cd | Apache-2.0 | Go module closure: K-02 SBOM | R3 engine lane; §4(b) change notices for Z-P1..Z-P7 | K-02 |
| cursor/plugins @ab1f702c (pstack, cursor-team-kit) | MIT ×2 (separate LICENSE files) | skill text only | RETAIN (adapt) | E-01 (ES-AT-02/03) |
| mattpocock/skills @59db609e | MIT | skill text only | RETAIN (copy/adapt) | L-06 (D4, D5) |
| wonderwhy-er/DesktopCommanderMCP @db3430f2 | MIT | schemas + logic ported; no runtime dependency | RETAIN (port) | H-00 |
| microsoft/playwright @cfe490d9 | Apache-2.0 | npm package | DEPEND | Y-02 |
| cedar-policy/cedar @2c2b84772a63 | Apache-2.0 | crates | DEPEND if chosen at C-05 (Ponytail) | C-05 |
| agentclientprotocol (schema/SDKs) @e50f62b4 | Apache-2.0 | SDK packages | DEPEND | C-08 |
| modelcontextprotocol/typescript-sdk @b415e60b | mixed (MIT/Apache-2.0 code, CC-BY-4.0 docs) | npm | DEPEND; ship all license texts | V-05 |
| anthropic-experimental/sandbox-runtime @98a4016d | Apache-2.0 | — | REFERENCE (P8) | S-03 |
| vercel/workflow @af8c6d32, durable-harness @ea8aa406 | Apache-2.0 | — | PATTERN ONLY (no code) | — |
| desktop-commander/remote-desktop-commander @a6573e86 | all rights reserved | — | EXCLUDED | — |

## 2. T3 inherited dependencies needing a decision before v1 (R11 §5)

| Package | Issue | Decision | Rationale / effect | Task |
|---|---|---|---|---|
| `heic-to@1.5.2` | LGPL-3.0 | **REMOVE** | HEIC preview is non-essential; LGPL relinking/notice obligations for bundled JS are not worth v1 risk; feature returns later via OS codecs | F-02 (LIC-01) |
| `electron-webauthn` | no declared license in registry metadata | **REMOVE** (no redistribution without terms; actual terms to be inspected only if the founder wants it back) | WebAuthn handled by `zain-approve` (webauthn.dll) at A1 or Chromium WebAuthn at A2 (17 §4) | F-02, C-00 FG-02 |
| `jszip` | MIT OR GPL-3.0-or-later | RETAIN, elect MIT (recorded in notices) | — | F-11 |
| `dompurify` | MPL-2.0 OR Apache-2.0 | RETAIN, elect Apache-2.0 | — | F-11 |
| `@anthropic-ai/claude-agent-sdk` | commercial terms | NOT BUNDLED (user-provided, G4) | SEC-13 | F-06 (T8) |
| `@cursor/sdk` | custom terms | **STRIP** with the Cursor provider | not part of v1 provider set | F-02 |

## 3. Post-v1 unknowns (deferred with explicit gates)

| Unknown | Gate | Provisional estimate effect |
|---|---|---|
| Orca closures beyond depth 2 (D2, D3, D5, D6, D7) | admission at I-05, I-06, I-07, W-05, I-02 | I-02 raised to 2–3.5 pw (rewrite) |
| Orca native sidecars (Swift, PowerShell, Python) for computer use | admission at W-05; ExecutionPolicy Bypass replaced | W-05 6–10 pw kept, at risk |
| `codex_protocol` symbols used by sandbox crates; `process-hardening` on Windows; TLS termination in network-proxy | admission at S-01/S-04 | S-01 4–8 pw |
| Excalidraw fonts license files; npm 0.18.1 vs repo 0.18.0 | admission at D-07 | — |
| LSP client `@hediet/json-rpc` license UNKNOWN | admission at I-03 (alternative client if unresolved) | — |
| Test-file imports of donor code | admission per task | — |

## 4. Rules

- Founder attestation never substitutes for a public license (06 §3b).
- A source at L1–L3 may be studied but not shipped; LIC-01 fails the installer for any package without an approved
  license entry.
- "Copy as-is" is allowed only for closed sets (R12 D4 was closed, but is now reference-only because C-25 supersedes it).
