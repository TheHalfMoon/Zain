# Assumptions and Unknowns Ledger

Every unknown has an owner phase, the evidence that closes it, and whether it blocks.

| ID | Unknown / assumption | Source | Blocks | Closure evidence | Phase |
|---|---|---|---|---|---|
| U-01-1 | Date/actor of public→private switch | 01 H2 | no | GitHub audit log | P0 |
| U-01-2 | Founder's intended visibility | 01 | P0 design | ADR-010 decision | P0 |
| U-02-1 | T3 test pass ratio on Windows; flake rate | R02 §8 | G2 | P1 run | P1 |
| U-02-2 | Whether Claude `canUseTool` fires for every tool in each permission mode | R02 §16 | P3 design detail | P3 spike with SDK | P3 |
| U-02-3 | Redistribution terms of `@cursor/sdk`, `@muse-code/sdk`, `@opencode-ai/sdk` | R02 §9 | no (stripped/optional) | read terms | P2 |
| U-02-4 | Effort estimates (all) | R02 §14, R03D §16 | no | P1/P3 actuals | P1–P3 |
| U-03-1 | Subscription-backed SDK orchestration = "ordinary use"? | R03C §10.5 | G4 for that mode | written Anthropic answer | P2 |
| U-03-2 | Claude Agent SDK redistribution inside installer | R03C | bundling | Anthropic terms/answer | P2 |
| U-03-3 | 257 Help Center articles at digest depth; API platform docs; changelogs line-level | R03 §7c | no | further reading when a feature's phase opens | per phase |
| U-03-4 | 8 open Claude doc discrepancies | R03 §3 | no | Anthropic/testing | per phase |
| U-03-5 | No hands-on observation of Claude UI features | R03 | no | founder-run observation scripts per 03F | per phase |
| U-03B-1 | Claude Design: Figma export, web capture, breakpoints, admin lock, two-way sync | R03B | no | official docs/testing | P7 |
| U-03D-1 | Orca runtime performance; exact IPC count; tamper evidence | R03D §18 | no | P1 comparison run | P1 |
| U-04-1 | Amp provider failover semantics; Gigawatt pricing | R04 §11 | no | docs | — |
| U-05-1 | Workflow SDK under Electron; community Worlds v5 compatibility | R05 §6 | no (not adopted) | — | — |
| U-06-1 | MCP SDK license transition per file (`@modelcontextprotocol/sdk` already in the fork at P2) | R10 | low | per-file check at admission | **P2** |
| U-06-2 | `codex-acp` license (NOASSERTION) | R10 | if used | license file | P2 |
| U-07-1 | Electron RAM vs goal | ADR-002 | revisit trigger | B2 | P1/P2 |
| U-07-2 | Ledger fsync latency on founder hardware | 07 §4 | budget | P3 microbench | P3 |
| A-1 | Assumption: founder's AI-assisted capacity ≈ 1 pw per calendar week | 08 | schedule | track actuals | all |
| A-2 | Assumption: T3 at pin remains MIT and pin stays fetchable | 06 | low | mirror pinned tarball into a private archive at P1 | P1 |
| A-3 | Assumption: Windows-first remains the priority | AGENTS.md | ordering | founder | — |
| U-07-3 | Windows Hello / platform WebAuthn availability inside Electron on the founder's hardware; passkey pairing UX for phones | 07 §6 | P3 approval design | P3 spike | P3 |
| U-07-4 | Azure Trusted Signing eligibility for an individual in Saudi Arabia | 07 §9 | public Windows release | provider check | P2 |
| U-07-5 | Write-latency cost of `synchronous=FULL` on the T3 receipt table | 07 §5 | budget | P1 measurement | P1 |
| U-08-1 | Whether the break-glass repair alone restores the v72 gate (no other 403 paths) | 08 P−1 | P−1 | run after change | P−1 |
