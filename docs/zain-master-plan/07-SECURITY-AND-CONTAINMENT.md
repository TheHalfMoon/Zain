# 07 — Security, Containment and Privacy

```text
BASELINE = V3 17_TRUST_BOUNDARY_SPEC.md, 18_PROVIDER_ENFORCEMENT_MATRIX.md, 19_COMPONENT_SECURITY_REVISIONS.md,
           09_RECOVERY_SECURITY_AND_EVALUATION.md, ADR-007, ADR-020..024 (authoritative for R1+ trust design)
ADDED    = privacy of the program itself, Windows 11 Home specifics, incident lessons, release-blocking rules
RULE     = prompting is never a security control; a feature is not "secure" because its tests pass
```

## 1. Trust boundaries

| Zone | Trusted for | Not trusted for |
|---|---|---|
| Founder | Approvals, authorizations, publication decisions | — |
| Zain Core (Rust) | Policy decisions, grants, ledger (single writer), coverage, the A1 approval surface | Observing effects it is not told about |
| Zain Server (Node, PEP) | Executing effects it mediates; reporting outcomes | Anything outside its mediation (terminals, CLI agents' own tools, agents' own file reads and connections) |
| Desktop main | Window management, updater, the A2 isolated approval window | Authorization beyond A2 |
| Renderer | Displaying state | Authorization of any kind (it can be compromised by rendered content) |
| Providers and agents (Codex, ACP, OpenCode, local models) | Producing proposals | Any decision; their output is untrusted input |
| Protocol handler, deep links, single-instance arguments | Data (open a project or a view) | Triggering any effect by themselves; actions are allowlisted |
| Other same-user processes | Nothing | They can reach localhost ports, the Server RPC unless authenticated, Credential Manager/DPAPI secrets and provider CLI files |
| Repository content, tool output, web pages, MCP servers, extensions | Data | Instructions |
| Third-party services (GitHub apps, model relays) | Only what the founder authorized | Private content by default |

## 2. Threat model (release-blocking items in bold)

**Honest R0a–R0 statement.** Until R1 there is no injection control beyond T3's supervised prompts, which the
renderer draws. Providers that cannot prompt in supervised mode (OpenCode and Pi until C-24) are disabled or labelled
"unsupervised" (GATE-SEC-01). Agents can read files and settings with the user's rights.

| Threat | Example | Enforcement boundary | Tasks / tests | Release |
|---|---|---|---|---|
| **Prompt / tool-output injection** | README tells the agent to delete files or exfiltrate keys | R0b: supervised prompts only (no claim); R1: policy decision on every mediated effect, Core-owned approvals, untrusted-content labelling | F-07, C-05, C-09, C-12, Y-07 | R0b (prompts), R1 (mediated) |
| **Destructive shell or filesystem operations** | `rm -rf`, `git clean -fd`, bulk delete on OneDrive paths | Quarantine-first revert (R0b); ProcessHost, fs-gate, bulk-delete and disk-reserve guards (R1) | Z-27, C-25, H-08, Z-19 | R0b, R1 |
| **Credential theft** | Agent reads `.env`, provider tokens | Keyring or provider-CLI storage; ignored and secret paths excluded from prompts and index; fs-gate deny list for writes. **Residual:** Credential Manager/DPAPI and provider CLI files are readable by any same-user process, and shell reads are UNKNOWN coverage until S-01 | F-22, Z-11, Z-28, H-08, S-01 | R0b, R1, R5 |
| **Unauthorized network egress** | Donor telemetry, update feeds, agent fetches attacker URL | Egress removal (Q-03, F-05); browser egress proxy (Y-10); OS-level network proxy (S-04) | EGR-01..03, GATE-PRIV-04 | R0a/R0b, R2, R5 |
| **Private code to unauthorized models** | Relay endpoint, AI review apps on GitHub | Server-side data classes; pre-session check of each hosted agent's effective endpoint; endpoint identity for localhost runtimes; app egress closure; repository privacy | Z-11, Z-02, Z-01 | M0, R0 |
| Workspace escape | Symlink or junction out of the worktree; `..` tricks | Handle-relative, no-follow, reparse-rejecting operations (policy for OneDrive placeholders in Z-19) | H-08, FSG-*, Z-19 | R1 |
| Approval bypass / spoofing | Renderer draws a fake approval | Core-owned A1 surface or A2 isolated window with canonical binding; no R1 approval is drawn by the renderer | C-13, APR-* | R1 |
| Agent privilege escalation | Agent edits Zain's own settings, policy or provider config | Protected paths; Core data root denied to providers (R1). Before R1 this is not prevented | C-16, G-03 | R1 |
| Local RPC abuse | Another same-user process connects to the Server WebSocket | Authenticated client token per launch (verify T3's mechanism in Q-02; add if absent) | Q-02, C-06 | R0a, R1 |
| Deep-link abuse | A web page opens `zain://` with crafted arguments | Allowlisted protocol actions; no effect from a link without user action | Q-02, F-03 | R0b |
| Cross-workspace leakage | Index or Brain returns another project's data | Per-project stores; project-bound threads | Z-28, M-03 | R1, R2 |
| Persistent-state corruption | Crash during write; tampered ledger | FULL sync, envelope hash, anchors, unanchored interval disclosed | C-03, C-19, LED-* | R1 |
| Dependency compromise | Malicious npm update | Frozen lockfile, pinned donors, license and provenance admission | Q-00, F-01, LIC-* | R0a, R0 |
| Malicious extension or MCP server | MCP server instructs agent; extension reads files | Per-tool grants; hash-pinned skills; MCPB manifest review | V-05..V-07 | R2 |
| Unsafe automatic merges | Agent merges its own PR | Gated merges; builder ≠ reviewer | E-06, V-01 | R3 |
| Command injection through launchers | File name from model output reaches `code.cmd` through cmd.exe | Resolve editors to `.exe`; cmd-specific escaping; argument arrays; negative tests with `&`, `%`, `^`, quotes | Z-13, C-25 | R0b, R1 |
| Localhost endpoint spoofing | Agent-spawned process listens on the port an Ollama route expects | Bind routes to the owning process image or start runtimes with a per-session token | Z-11 | R0 |
| Untrusted generated code executed | Agent runs generated tests with network | Supervised prompts (R0b); ProcessHost + network policy (R1+); sandbox (S-01) | F-07, C-25, S-01 | R0b → R5 |

## 3. Windows-specific containment (real capabilities, not Unix assumptions)

| Mechanism | Available on the founder's Windows 11 Home 10.0.26300? | Use in Zain | Proof task |
|---|---|---|---|
| Job Objects (kill-on-close, limits, nested jobs) | Yes (all editions) | ProcessHost: every launch created suspended inside a per-launch job; the tree of processes it launched is killed on cancel or emergency stop | C-00 FG-01, C-25 |
| ConPTY inside a job | Yes, but needs proof that the conhost/OpenConsole child stays in the job | Terminals under ProcessHost | C-00 |
| No-follow file operations (`CreateFileW` with `FILE_FLAG_OPEN_REPARSE_POINT`, or `NtCreateFile` with `FILE_OPEN_REPARSE_POINT` relative to a root handle) | Yes | fs-gate (no-follow, reparse rejection, ADS and hardlink checks). OneDrive Files On-Demand placeholders are reparse points: Z-19 sets the policy | H-08, A3-04, Z-19 |
| Codex Windows sandbox set (restricted token, ACLs, firewall rules) | Unelevated tier: likely; elevated tier needs admin setup (sandbox users, firewall service) | OS sandbox candidate (S-01). Restricted tokens alone do not block reads or network | C-00, S-01 |
| AppContainer | Present on Windows 11 | **Not the selected backend** (V3 ADR-014 uses the Codex set); listed only because competitors use it | — |
| MXC / BaseContainer | Vendor docs name 25H2 26200.x and 26H1 28000.x builds; **26300 is outside both** | Candidate backend (Codex, sandbox-runtime) | C-00 on 26300 and again on each tester build before DEC-06 |
| WSL2 | Available | **Outside** Job Objects, fs-gate and the kill switch (a VM). WSL contexts are labelled UNKNOWN coverage (Z-33) | Z-33 |
| Windows Sandbox, Hyper-V VMs | **No** (Home edition) | Not available; B-01 amended by Z-24 | Z-24 |
| Separate local user account | Yes | R0a test isolation (A5) | Z-09 |

Claims follow evidence. Until C-00 passes, Zain claims no process containment. Until S-01 passes its escape suite,
it claims no OS sandbox. A C-00 pass on the founder's Insider-range build says nothing about testers' builds; each
build line is qualified separately.

## 4. Permission lifecycle and kill switch

1. **Request**: an agent proposes an effect. The Server classifies it (effect class, exact target, network, data
   class). Workspace content is at least `private-code`; callers may raise the class, never lower it.
2. **Decide**: R0a–R0 use T3's supervised mode. From R1 the Core decides with policy, grants and coverage.
3. **Approve** (from R1, copied from V3 17 §4.5):
   - **A1**: Core-owned native surface (`zain-approve`) plus the platform authenticator (webauthn.dll).
   - **A2**: isolated Electron approval window (desktop main) plus Chromium WebAuthn.
   - **A3**: TOTP code in the A2 window. No device-bound user presence.
   The level is part of the binding, recorded, and shown in the trust indicator. A downgrade (A1→A2→A3) needs an
   assertion at the current level. No R1 approval is a confirm drawn by the renderer.
4. **Dispatch and execute**: the Core durably records the dispatch (logical operation id, exact target, input digest,
   fencing epoch). The effect then runs through ProcessHost or fs-gate under the grant.
5. **Report**: APPLIED, NOT_APPLIED or UNKNOWN with evidence. UNKNOWN never counts as success.
6. **Expire**: run-scoped grants expire on cancel, restart or scope change. Persistent grants (V3 18) are explicit,
   scoped, listed in settings and revocable.
7. **Emergency stop**: one action (UI, global shortcut, CLI `zain stop`) kills every process launched under
   ProcessHost and pauses all continuations. In-flight effects become UNKNOWN until reconciled. It does **not** reach
   processes started through WMI, Task Scheduler, services, COM or DDE, nor anything inside the WSL VM (V3 17 §3).
   Delivered by C-25 in R1. Before R1 the stop acts on T3's own process management only, and onboarding says so.

## 5. Program privacy (this repository and its tooling)

| Control | State 2026-11-08 | Task |
|---|---|---|
| Repository private | **Not met**: public | Z-01 |
| No automatic third-party AI review | Unverified; apps installed | Z-02 |
| Past exposure assessed | Not done | Z-03 |
| Research tools do not send private content to unauthorized services | This session ran web research with generic product queries only; no private content was sent; no OpenCode/DeepSeek review was run because the configured route is a third-party relay | Z-06, DEC-01 |
| No donor source or binaries in a public location | Withdrawn with ADR-Z04 (2026-11-08): donor source is pushed with its license notices; secrets never | ADR-Z04 |

## 6. Lessons from incidents

| Evidence | Lesson | Requirement |
|---|---|---|
| V3 ledger 2026-10-28: donor clones filled the disk and were deleted afterwards | Builds and clones need a capacity preflight and a reserve | GATE-RES-01; disk reserve in Z-19 |
| `%USERPROFILE%\OneDrive\Desktop\wepld` checkout shows every tracked file deleted in the working tree (cause unknown; OneDrive sync may propagate deletions) | Deleting inside synced folders can spread; deletions need a recoverable path | Protected synced paths, quarantine-first (Z-19); forensics (Z-18) |
| A public report (2025-12) of an agent in an auto-approve mode wiping a user's D: drive on Windows (03 §1) | Auto-approve plus unrestricted filesystem access is unsafe | Supervised default (F-07); no Full access lane until S-05 inside a sandbox |
| T3 revert runs `git clean -fd` | "Undo" can delete user work | Z-27 quarantine |
| `usn-journal.csv` cited as recovery evidence but not found | Recovery evidence must be stored with the incident note | Z-18 records evidence locations |

## 7. Security gates that block releases

A release cannot pass while any HIGH or CRITICAL security finding is open for that release, regardless of test
status. R0 security gates: GATE-SEC-01, GATE-SEC-02, GATE-PRIV-04, GATE-MODEL-01. R1 adds GATE-SEC-03 and the V3
R1 claim tests (CLM-01, CLM-02) under GATE-R1-EXIT. Independent review of T2 work goes through GATE-REV-01 routes
only.
