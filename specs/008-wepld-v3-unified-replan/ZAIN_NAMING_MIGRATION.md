# WePLD → Zain Naming and Migration Matrix

```text
STATUS = PLANNING. Repository rename DONE by founder (verified 2026-10-27); all code/package/identifier migrations are
         PLANNED tasks (14_TASK_CATALOG F-03, N-01..N-04) and are NOT executed during planning.
REPOSITORY = TheHalfMoon/Zain (ID 1334408699, PUBLIC; formerly TheHalfMoon/wepld) — verified via gh api
SEPARATE_PROJECT = TheHalfMoon/Zain-LLM (ID 1429686788, PRIVATE; formerly TheHalfMoon/Zain) — out of scope, never modified,
                   never merged or cross-referenced as part of this product
CONFLICT_REVIEW = research/R19_ZAIN_NAMING_CONFLICTS.md
```

## 1. Product-facing names

| Legacy name | Zain name | Notes |
|---|---|---|
| WePLD | **Zain** | canonical identity |
| WePLD IDE / WePLD Desktop | **Zain IDE / Zain Desktop** | |
| WePLD Code Review | **Zain Code Review** | 16 §2 |
| WePLD Plan Mode | **Zain Plan Mode** | 16 §4 |
| WePLD Browser | **Zain Browser** | 16 §5 |
| Desktop Commander integration | **DeskGate** (kept) | 16 §6 |
| WePLD Trusted Core | **Zain Trusted Core** | |
| WePLD Project Brain (Fehrest) | **Zain Project Brain** | internal module names (Nawat, Fehrest, AMAN) stay internal |
| WePLD CLI | **Zain CLI** | |
| WePLD Engineering System | **Zain Engineering System** | 16 §3 |
| WePLD Server | **Zain Server** | |

## 2. Technical identifiers (planned; executed by F-03, F-10, F-18, N-01..N-04 — NOT during planning)

| Surface | Current / legacy value (verified 2026-10-28) | Zain target | Migration note |
|---|---|---|---|
| Repository | TheHalfMoon/wepld | TheHalfMoon/Zain | **done** by founder; GitHub redirects old URLs; local remote updated |
| User CLI | `wepld` (S2 binary, `crates/core/src/bin/wepld.rs`) | `zain` | S2 commands move under `zain-core`; no dual binaries (F-10) |
| Core binary | `wepld` (same source) | `zain-core` | F-10 |
| Rust crates | `wepld-contracts`, `wepld-core`, `wepld-desktop` (`crates/*/Cargo.toml`, `apps/desktop/src-tauri/Cargo.toml`) | `zain-contracts`, `zain-core`; `wepld-desktop` deleted with Tauri (F-18) | N-04, one commit, Rust suite must stay green |
| Governance scripts | `.github/scripts/wepld_*.py` (169 files) | unchanged until G-05 archives them; new `governance_check.py` | historical paths preserved |
| Registry archive | `docs/canonical/artifacts/WEPLD_CANONICAL_ARTIFACTS_2026-08-14.tar.gz` | unchanged (frozen evidence) | never renamed |
| npm scope | T3 `@t3tools/*` | `@thehalfmoon/*` (owned org scope; npm `zain` and PyPI `zain` taken; `@zain` ownership unverified) | N-03 |
| Env prefix | `T3CODE_*`, `ORCA_*` (donors); no product `WEPLD_*` variables exist yet | `ZAIN_*` (Zain-LLM must use a distinct prefix, e.g. `ZAINLLM_`) | F-03 |
| Git hidden refs | `refs/t3/checkpoints/` | `refs/zain/checkpoints/` | F-03 |
| Protocol handler | `t3code://`, `orca://` | `zain://` (configurable) | F-03 |
| App ID / AUMID | `T3Tools.T3Code`, `com.stablyai.orca` | `io.github.thehalfmoon.zain` placeholder (zain.com/.ai/.dev/.app registered by others) | final id after N-01/N-02 |
| Data dirs | T3 `~/.t3`, Orca `%APPDATA%\Orca`, `~/.orca` | `%APPDATA%\Zain`, user dir `~/.zain-ide`, project-local `.zainide/` (not `.zain/`, which PyPI `zain` uses) | no shipped product → no user data to migrate |
| MCP server name | `t3-code` | `zain` | F-03 |
| Hook headers | `x-t3-*`, `x-orca-*` | `x-zain-*` | I-06 |
| Ledger cross-link event | (new) | `zain.run-receipts` | C-11 |
| Installer artifacts | — | `Zain-Setup.exe`, `Zain-<ver>.dmg`, `zain_<ver>.deb`, `Zain-<ver>.AppImage` | F-11, I-09 |
| Wire protocol id | T3 protocol v2 | `Zain-1` | F-09 |
| Planning dir | `specs/008-wepld-v3-unified-replan/` | unchanged (legacy path) | new specs use `specs/0xx-zain-*` |
| Canonical docs text | "WePLD" in AGENTS.md, CURRENT_STATE, invariants, master index | "Zain" | governed protected-path change (G-06/N-04), signed co-sign |

## 3. What is preserved (never rewritten)

Commit history and SHAs; PR/issue numbers and URLs (GitHub redirects); the frozen 402-entry registry archive and its
filenames (`WEPLD_*`); research files `research/R*.md` (historical evidence, read with legacy names); historical evidence
files `01_LIVE_WEPLD_AUDIT.md`, `CI_403_REDIAGNOSIS_2026-10-27.md`, `EGRESS_PREFLIGHT_2026-10-27.md` (legacy-name
note added); all third-party copyright notices and licenses.

## 4. Do-not-merge rule

"Zain" (this product, repo ID 1334408699) and "Zain-LLM" (separate private language-model project, repo ID 1429686788)
must not share packages, identifiers, release channels or documentation. Package scope and app ID must be chosen so that
neither project's artifacts can be mistaken for the other's; any future integration is a separate, explicitly
designed connector.

## 5. Conflict review summary (R19, 2026-10-27; not legal advice)

| Area | Finding | Risk |
|---|---|---|
| Trademark | Zain Group (Kuwait telecom, since 2007; ZainTECH sells cloud/AI in KSA). Register entries (WIPO/USPTO/SAIP) not retrievable here | **HIGH** for a standalone "Zain" software mark in KSA/GCC |
| PyPI `zain` | taken by a terminal coding agent using `.zain/` | High confusion (same category) |
| npm `zain` | taken (personal CLI) | Medium |
| crates.io `zain`, `zain-core` | free | Low |
| GitHub handles `zain`, `zain-ai` | taken (personal) | Low (repo is TheHalfMoon/Zain) |
| Domains zain.com/.ai/.dev/.app | registered by others; zainide.* show no registration (unverified) | reverse-DNS on zain.* impossible |
| Zain-LLM | separate project; use distinct prefix (e.g., `ZAINLLM_`) | must stay separate |

**Founder-only decision (FO-8):** obtain counsel clearance for "Zain" (or a qualified variant such as "Zain IDE" /
another mark) **before** any public distribution, package publishing or domain purchase. Planning continues under the
working name Zain.

## 6. Pre-implementation clearance (before P2 F-03)

Results and risk levels: `research/R19_ZAIN_NAMING_CONFLICTS.md`. Clearance tasks N-01…N-04 in 14_TASK_CATALOG.
