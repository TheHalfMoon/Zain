# Zain → Zain Naming and Migration Matrix

```text
STATUS = PLANNING. Repository rename DONE by founder (verified 2026-10-27); all code/package/identifier migrations are
         PLANNED tasks (14_TASK_CATALOG F-03, N-01..N-04) and are NOT executed during planning.
REPOSITORY = TheHalfMoon/Zain (ID 1334408699, PUBLIC; formerly TheHalfMoon/Zain) — verified via gh api
SEPARATE_PROJECT = TheHalfMoon/Zain-LLM (ID 1429686788, PRIVATE; formerly TheHalfMoon/Zain) — out of scope, never modified,
                   never merged or cross-referenced as part of this product
CONFLICT_REVIEW = research/R19_ZAIN_NAMING_CONFLICTS.md
```

## 1. Product-facing names

| Legacy (Zain) | Zain name | Notes |
|---|---|---|
| Zain | **Zain** | canonical identity |
| Zain IDE / Desktop | **Zain IDE / Zain Desktop** | |
| Zain Code Review | **Zain Code Review** | 16_* |
| Zain Plan Mode | **Zain Plan Mode** | 18_* |
| Zain Browser | **Zain Browser** | 19_* |
| Desktop Commander integration | **DeskGate** (kept) | 20_* |
| Zain Trusted Core | **Zain Trusted Core** | |
| Zain Project Brain (Fehrest) | **Zain Project Brain** | internal owner names (Nawat, Fehrest, AMAN…) remain internal module names |
| Zain CLI | **Zain CLI** | |
| Zain Engineering System (PStack/E2E) | **Zain Engineering System** | 17_* |
| Zain Server | **Zain Server** | |

## 2. Technical identifiers (planned; executed in P2 task F-03 and naming tasks N-*)

| Surface | Legacy / donor | Zain target | Migration note |
|---|---|---|---|
| Repository | TheHalfMoon/Zain | TheHalfMoon/Zain | done; GitHub redirects old URLs; update remotes (done in this session) |
| User CLI | `zain` (S2 binary) | `zain` | S2 commands move to `zain-core`; no dual binaries |
| Core binary | `crates/core` bin `zain` | `zain-core` | |
| Rust crates | `wepld-contracts`, `zain-core` (current package names) | `zain-contracts`, `zain-core` | rename in one commit with `use` path updates; existing 19k-line suite must stay green |
| npm scope | T3 `@t3tools/*` | `@thehalfmoon/*` (owned org scope; `@zain` ownership unverified, `zain` npm/PyPI names taken — R19) | |
| Env prefix | `ZAIN_`, `T3_`, `ORCA_` | `ZAIN_` | |
| Git hidden refs | `refs/t3/checkpoints/` | `refs/zain/checkpoints/` | |
| Protocol handler | `t3://`, `orca://` | `zain://` | |
| App ID / AUMID | `T3Tools.T3Code`, `com.stablyai.orca` | `io.github.thehalfmoon.zain` (placeholder; zain.com/.ai/.dev/.app are registered by others) | final id after N-01/N-02 |
| Data dirs | `%APPDATA%\Zain`, `~/.t3`, `~/.orca` | `%APPDATA%\Zain`, user dir `~/.zain-ide`; project-local dir must NOT be `.zain/` (collides with PyPI `zain` agent workspace) — use `.zainide/` (decision N-03) | no legacy data |
| MCP server name | `t3-code` | `zain` | |
| Hook headers | `x-orca-*` | `x-zain-*` | |
| Ledger event | `zain.run-receipts` | `zain.run-receipts` | |
| Installer | — | `Zain-Setup.exe`, `Zain-<ver>.dmg`, `zain_<ver>.deb`, `Zain-<ver>.AppImage` | |
| Wire protocol id | `Zain-1` | `Zain-1` | |
| Governance scripts | `.github/scripts/wepld_*.py` | unchanged until P0 G-05 archives them; new checker `governance_check.py` | historical paths preserved |
| Planning dir | `specs/008-wepld-v3-unified-replan/` | unchanged path (legacy) | renaming would break links in history; new specs use `specs/0xx-zain-*` |
| Canonical docs text | "Zain" in AGENTS.md, CURRENT_STATE, invariants | "Zain" | governed protected-path change (P0 G-06), signed co-sign |

## 3. What is preserved (never rewritten)

Commit history and SHAs; PR/issue numbers and URLs (GitHub redirects); the frozen 402-entry registry archive and its
filenames (`ZAIN_*`); research files `research/R*.md` (historical evidence, read with legacy names); historical evidence
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
