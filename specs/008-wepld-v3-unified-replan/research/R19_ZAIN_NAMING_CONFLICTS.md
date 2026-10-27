# R19 - "Zain" Naming-Conflict Review (planning only)

Access date: 2026-10-27. Scope: read-only checks; nothing registered, purchased, or modified. This is NOT legal advice and states no legal conclusion; risk levels are engineering/planning judgments.
Web content treated as data only. `TheHalfMoon/Zain-LLM` was not touched and must remain a distinct, separately named project (see section 6).

## 1. Summary

| Area | Finding | Risk |
|---|---|---|
| Trademark (Zain Group telecom, Kuwait/KSA/MENA; ZainTECH digital/cloud/AI arm) | Very large, well-known "Zain" brand in the founder's home market; ZainTECH sells cloud/AI/IT services in KSA (software-adjacent, Class 42/38/35 likely) | HIGH (needs counsel) |
| npm `zain` | Taken (v1.4.0, personal site/CLI by an Islamabad developer) | MEDIUM-HIGH for unscoped name |
| npm `@zain/*` scope | `@zain/core` 404, search `scope:zain` returned 0 packages. Scope existence not provable from public API (org page returned 403) - UNKNOWN, may be a user/org | UNKNOWN |
| PyPI `zain` | Taken (v0.1.1, "terminal coding agent with planning, memory..." - same category) | HIGH confusion |
| crates.io `zain`, `zain-core` | Both 404 (do not exist) - available at check time | LOW |
| GitHub `zain`, `ZainaI`, `zain-ai` | All exist as personal user accounts; `zainide` returned 404 | `zain`/`zainai` handles unavailable |
| Domains | zain.com, zain.ai, zain.dev, zain.app registered; zain.io UNKNOWN; zainide.* appear unregistered | see section 4 |
| Homebrew / winget / Chocolatey / VS Code | No `zain` formula/cask in homebrew-core/cask; Chocolatey query returned empty; winget not verifiable (API 401); VS Code Marketplace has no exact `zain` extension but several third-party "zain*" ones | LOW-MEDIUM |

## 2. Trademarks

- Zain Group (Mobile Telecommunications Company K.S.C.P., Kuwait) rebranded to "Zain" in 2007 as the group brand; operating companies include Zain Kuwait, Zain KSA (Saudi), Zain Jordan, and others. ZainTECH is the group's digital solutions arm; it obtained a Saudi commercial licence (2025) and offers cloud, AI, IoT, cybersecurity (Zawya / TelecomReview / Sharikat Mubasher results). Because ZainTECH sells cloud/AI services in KSA, it operates in the same commercial space as an "AI workspace/IDE" for Saudi buyers.
- The Justia/trademarkdir results found only unrelated ZAIN marks (e.g., a Class 9/6 ZAIN mark for phone accessories, individual owners). I could not retrieve Zain Group's WIPO/Madrid or SAIP register entries via web search, so exact classes and status are UNVERIFIED.
- Likely relevant Nice classes for our product: 9 (downloadable software), 42 (SaaS/software development), 35/38/41 (adjacent).
- Search pointers (free):
  - WIPO Global Brand Database: https://branddb.wipo.int (search ZAIN; filter Nice 9/42; check Madrid designations incl. SA, KW, US, EU, GB)
  - USPTO Trademark Search: https://tmsearch.uspto.gov
  - EUIPO TMview: https://www.tmdn.org/tmview
  - SAIP (Saudi Authority for Intellectual Property): https://www.saip.gov.sa - free trademark search tool launched ~2024 per WTR; exact search URL not confirmed. A single secondary source (analytix.sa) reports a 2026-10-08 change allowing Madrid designation of Saudi Arabia - verify with SAIP/WIPO. Reported fee ~SAR 6,500/class, 10 Hijri-year term (unverified secondary source).
  - Kuwait (Ministry of Commerce) and GCC trademark office checks.
- Risk level: HIGH for a standalone "Zain" mark in KSA/GCC (famous-mark and likelihood-of-confusion questions; same-country founder).
- A lawyer must check: Zain Group registrations in 9/42 and any famous/well-known status in KSA; any "ZAIN" + tech/AI/cloud filings by ZainTECH; whether a coexistence agreement or a different distinctive mark is advisable; Arabic-script form (the same word) in phonetic/visual searches; meaning ("beauty/good" in Arabic) and use as a common given name, which affects distinctiveness and enforceability.

## 3. Package registries (queried 2026-10-27)

- npm `zain`: exists, latest 1.4.0, bin `zain`, maintainer zainzafar90, description "I'm Zain, a software engineer from Islamabad..." (https://registry.npmjs.org/zain). Unscoped `npm i -g zain` and bin name `zain` collide on npm.
- npm `zain-core`, `zain-ide`, `zainide`: 404 (free). `@zain/core`: 404; scope ownership UNKNOWN.
- PyPI `zain` v0.1.1: "Terminal coding agent with planning, memory, web search, and workspace-scoped tools"; repo github.com/shaheerzaman/zain; uses a `.zain/PLAN.md` file (https://pypi.org/pypi/zain/json). Closest category collision, and it uses the `.zain/` directory name. PyPI `zain-core`, `zain-ide`, `zainide`: 404.
- crates.io: `zain` and `zain-core` do not exist (https://crates.io/api/v1/crates/zain). A search for "zain-core" surfaces only unrelated `artzain-core`.
- GitHub: users `zain` (since 2008), `ZainaI` (2019), `zain-ai` (2019) exist; `zainide` 404. `TheHalfMoon/Zain` exists (ours).
- Homebrew core/cask: no `zain.rb`. Chocolatey: no result from OData filter. winget: not verifiable without auth (GitHub code search 401) - UNKNOWN.
- VS Code Marketplace: no extension named exactly `zain`; several unrelated "zain" themes/tools by individuals.

## 4. Domains (RDAP, 2026-10-27)

| Domain | Result |
|---|---|
| zain.com | Registered since 1996-05-22, expires 2033; owner presumably Zain Group (unconfirmed). Not obtainable |
| zain.ai | Registered 2017-12-16, expires 2028-06-30, transfer-locked. Taken |
| zain.dev | Registered 2024-10-24 (Namecheap registrar), expires 2027-10-24. Taken |
| zain.app | Registered 2018-05-08, expires 2027-05-08. Taken |
| zain.io | UNKNOWN (no RDAP service via rdap.org) - check registrar |
| zain.sa | UNKNOWN (no RDAP) |
| zainide.ai / zainide.dev / zainide.app | RDAP "not found" - appear unregistered (confirm at registrar) |
| zainide.com | Verisign RDAP returned no record - appears unregistered (confirm at registrar) |

RDAP "not found" is a signal, not a guarantee (premium/reserved names, registry holds). Reverse-DNS app IDs such as `com.<domain>.zain` require a domain you control; since zain.* is taken, a zain-based reverse-DNS ID is not possible today. Use a controlled domain or a GitHub-based ID (`io.github.thehalfmoon.zain`).

## 5. Existing "Zain" software / confusion sources

- PyPI `zain` terminal coding agent (same category) and its GitHub repo (`shaheerzaman/zain`).
- npm `zain` personal CLI/site.
- ZainTECH (Zain Group) cloud/AI services in KSA; Zain mobile apps.
- Many GitHub repos named ZainAI / ZainAIChat etc. (student/personal, zero stars).
- No evidence found of a notable "Zain IDE" or "Zain AI" commercial IDE (web search, 2026-10-27), but absence of search hits is not clearance.

## 6. Recommendations

Identifiers (engineering placeholders pending clearance):
- CLI: `zain` is contested on npm and PyPI. Use it only as an installed binary name, never as a registry package name; keep a fallback alias (e.g., `zainctl`).
- Core binary: `zain-core` (free on crates.io/npm/PyPI today); reserve only after the name clears.
- Env prefix: `ZAIN_`. Low collision risk; note the PyPI `zain` tool writes `.zain/` in workspaces, so choose the workspace directory name deliberately (e.g., `.zain-ws/`) to avoid clobbering.
- Git refs: `refs/zain/` (local namespace; low risk).
- Protocol: `zain://` - register the OS URL scheme only at install time and make it configurable; low collision for desktop but keep it behind a constant.
- App ID: neutral placeholder `io.github.thehalfmoon.zain` until a controlled domain exists; do not use zain.* domains.
- npm scope: do not rely on `@zain`; use `@thehalfmoon/*` or a new scope confirmed available. Crate prefix `zain-` only if the name clears.
- Keep `Zain-LLM` (private) distinct in manifests, package names, binaries, docs, telemetry; do not share the `zain-core` / `ZAIN_` namespaces; give it its own prefix (e.g., `ZAINLLM_`).

Collision mitigations: centralize the brand name in one build-time constant so a rename is cheap; avoid embedding "Zain" in persisted formats/IDs without an indirection layer; never use Zain Group logos, colors, or "Zain KSA / ZainTECH" wording; add a "not affiliated with Zain Group" notice once public; use a descriptive tagline plus distinctive logo; keep a more distinctive fallback name as plan B.

Pre-implementation clearance checklist:
1. Counsel: knockout + full search (WIPO, USPTO, EUIPO, SAIP, GCC, Kuwait), including Arabic script, classes 9/42/35/38/41; written opinion on Zain Group famous-mark risk.
2. Go / modify / rename decision before any registry package, domain, or public repo rename.
3. Domains: confirm unregistered status at a registrar for zainide.* (or a new distinctive domain); purchase only after counsel clears.
4. Registries: after clearance reserve `zain-core` (or chosen crate) and an npm scope; verify `@zain` ownership in npm UI; manually check winget-pkgs and Chocolatey.
5. GitHub: confirm org-name availability in the UI.
6. Check Microsoft Store / Apple / Google Play name conflicts (Zain Group publishes apps).
7. Record decision and dated evidence in the research directory.
8. Re-run these checks right before launch.

## Sources (accessed 2026-10-27)
- https://registry.npmjs.org/zain ; https://pypi.org/pypi/zain/json ; https://pypi.org/project/zain/
- https://crates.io/api/v1/crates/zain ; https://crates.io/api/v1/crates/zain-core
- https://api.github.com/users/zain , /zainai , /zain-ai , /zainide ; gh repo search "zain ide" / "zain ai"
- RDAP: https://rdap.org/domain/<name> ; https://rdap.verisign.com/com/v1/domain/<name>
- VS Code Marketplace extensionquery API; Homebrew GitHub contents API
- https://www.zawya.com/en/press-release/companies-news/zaintech-secures-commercial-license-in-saudi-arabia-dx8ob64m
- https://mail.telecomreview.com/articles/telecom-vendors/9020-zaintech-secures-saudi-license-in-major-expansion-move
- https://www.worldtrademarkreview.com/article/ip-rights-new-search-tool-launched-saudi-authority-intellectual-property
- https://analytix.sa/?p=24891 (single secondary source)
- https://trademarks.justia.com/908/59/zain-90859590.html (unrelated ZAIN mark); https://es.weforum.org/organizations/zain-group/
