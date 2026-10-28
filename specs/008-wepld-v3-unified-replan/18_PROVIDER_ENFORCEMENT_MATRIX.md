# 18 — Provider × Operation Enforcement Matrix (Astro H-2)

```text
STATUS = PROPOSED. Evidence = source reading at t3code@36d4d711 (R11 §3.2, Astro citations) and vendor documentation;
         nothing has been run. Every cell is re-verified at C-09 / C-24 admission; an unverified cell defaults to EXCLUDED.
STATUS_RULE = every ENFORCED cell is a TARGET until its PEM test passes; claim text is generated only from passing cells (CLM-01)
CELL_VALUES = ENFORCED (every instance reaches a Core decision before execution) · UNKNOWN-COV (decision may be
              mediated but execution/descendants are not covered — 17 §2) · EXCLUDED (not available in the trusted tier;
              the provider may still run as a labelled untrusted worker) · N/A
TRUSTED_TIER = the set of ENFORCED and UNKNOWN-COV cells of providers whose row is qualified by C-09/C-24 tests
```

## 1. Matrix

| Operation | Claude (Agent SDK, API key) | Codex (app-server) | ACP agents | OpenCode | Pi |
|---|---|---|---|---|---|
| File read | ENFORCED (PreToolUse on Read/Grep/Glob) | UNKNOWN-COV (known-safe reads auto-run inside Codex sandbox) | ENFORCED if via `fs/read_text_file`; else UNKNOWN-COV | EXCLUDED until C-24 | EXCLUDED until C-24 |
| File write / edit | ENFORCED decision; execution by provider (COVERED only if no shell in context) | ENFORCED via `fileChange/requestApproval` / `applyPatchApproval` | ENFORCED via `fs/write_text_file` (C-08 PEP + fs-gate) | EXCLUDED until patched (always-allow + auto-allow edits, adapter L632–655) | EXCLUDED until patched |
| Shell / command | decision ENFORCED (PreToolUse Bash); descendants UNKNOWN-COV | decision ENFORCED (`commandExecution/requestApproval`, `execCommandApproval`); descendants UNKNOWN-COV (Codex sandbox narrows writes) | ENFORCED decision via `terminal/create`; descendants UNKNOWN-COV | EXCLUDED | EXCLUDED |
| Network / web fetch | ENFORCED (PreToolUse WebFetch/WebSearch); model-side server tools are provider egress, not local effects | UNKNOWN-COV (server-side web search; sandbox network setting) | UNKNOWN-COV (agent-internal) | EXCLUDED (network tools auto-allowed upstream) | EXCLUDED |
| MCP tool calls | ENFORCED (PreToolUse on `mcp__*`; Zain `/mcp` S6) | ENFORCED for Zain `/mcp` tools (S6); third-party MCP servers configured in Codex → EXCLUDED | ENFORCED for Zain `/mcp`; agent-configured MCP → EXCLUDED | EXCLUDED | EXCLUDED |
| Subagent spawn | UNKNOWN-COV (subagent tools still pass PreToolUse; contexts inherit UNKNOWN) | N/A | agent-specific → EXCLUDED unless declared | EXCLUDED | EXCLUDED |
| Permission-mode change | ENFORCED: Core sets mode; SDK `permissionMode` fixed to `default`; mode changes are Core policy edits with assertion | ENFORCED: S1 clamp (`runtimeModeDefaults` L687–727, `approvalPolicy:"never"` L719 and `dangerFullAccess` L722 replaced) | ENFORCED: Zain client policy | EXCLUDED | EXCLUDED |
| Approval caching | Provider cache disabled: no allow rules, `settingSources` empty, no `acceptEdits`/`bypassPermissions`; grants cached only in Core | Zain never answers `ApprovedForSession`; session grants are Core grants | `allow_always` mapped to a scoped Core grant; client never auto-answers | upstream "once" grants and always-allow → must be removed | session approval cache returns `confirmed: true` (adapter L1251–1259; populated L2701–2702) → must be removed |
| Plan mode (read-only) | ENFORCED if no Bash in turn (PreToolUse denies writes/exec) | ENFORCED decisions; read auto-runs remain UNKNOWN-COV | per agent | EXCLUDED | EXCLUDED |

Notes:
- Claude ordering: the Agent SDK permission documentation describes hooks evaluated before permission rules and modes,
  with `canUseTool` consulted only when no earlier step decided. Zain therefore relies on **PreToolUse hooks** (first in
  order) and removes every allow rule and permissive mode so no earlier step can allow; `canUseTool` remains a second
  PEP. Order and option names are re-verified against the SDK version pinned at C-09 (source:
  https://code.claude.com/docs/en/agent-sdk/permissions).
- "Decision ENFORCED, descendants UNKNOWN-COV" means the launch is authorized by Core, but per 17 §2 the context's
  coverage is UNKNOWN; this is what the R1 claim text says.

## 2. Required changes per provider (C-09, C-24)

| Provider | Change | Test |
|---|---|---|
| Claude | PreToolUse hook on all tools → `effect.propose`/`dispatch`; `canUseTool` → same; `settingSources: []`; no `allowedTools`; `permissionMode: "default"`; managed deny rules for data root (C-16) | PEM-CLA-01..04, CC-T01..T03 |
| Codex | `approvalPolicy: "untrusted"`, `sandboxPolicy: workspaceWrite` from Core; handlers for every request type answer per Core; never `ApprovedForSession`; `danger-full-access` unreachable | PEM-CDX-01..04 |
| ACP | client policy: all `fs/*`, `terminal/*` through Core; `session/request_permission` options mapped to Core grants; agents whose internal tools bypass client methods are listed as UNKNOWN-COV per agent | PEM-ACP-01..03 |
| OpenCode | replace upstream permission rules (adapter L632–655) with `ask` for edit, bash, webfetch and MCP; route every ask to Core; disable "once" reuse | PEM-OPC-01..03; until green → EXCLUDED, worker labelled untrusted |
| Pi | remove the session approval cache (L1251–1259, L2701–2702); every request to Core | PEM-PI-01..03; until green → EXCLUDED |
| All | Core-held grants with `scope`, `expiry`, `fencing_epoch`, revocation; on revocation or epoch bump, sessions whose provider-side state could reuse a decision are restarted | PEM-GEN-01..04 |

## 3. Grant cache semantics (all providers)

- A grant is a Core fact `{grant_id, principal, mission, effect_class, target pattern, scope, expiry, epoch, revoked}`.
- `once` grants are consumed by one dispatch; `session` grants end with the provider session and with any epoch bump;
  `persistent` grants require an A1/A2 assertion and are listed in Settings with revoke.
- Revocation is effective at the next dispatch (T13 revalidation). Provider-side memory of a decision is never trusted:
  if a provider cannot be told to forget, its session is restarted (PEM-GEN-01).

## 4. R1 enumerated mediated surface (replaces the earlier "every effect" claim — A2-07)

R1 claims Core decisions **only** for these operations, and only for cells whose PEM tests pass:

| Provider (pinned runtime) | Operations decided by Core before execution | Not decided by Core in R1 (shown as UNMEDIATED/UNKNOWN) |
|---|---|---|
| Claude Agent SDK (version pinned at C-09; `settingSources: []`, `CLAUDE_CONFIG_DIR` per session, no allow rules, `permissionMode: default`) | tool calls reaching PreToolUse: Read/Grep/Glob, Write/Edit, Bash **launch**, WebFetch/WebSearch, `mcp__*`, subagent tool calls (PEM-CLA-01..05) | descendants of Bash; model-side server tools (provider egress) |
| Codex app-server (version pinned; `CODEX_HOME` per session with Zain-only MCP config; approvalPolicy `untrusted`; sandbox `workspaceWrite`) | requests that reach approval handlers: command execution, file change/patch, permission escalation; all response forms normalized, session-scoped allowances never sent (PEM-CDX-01..06) | Codex known-safe read/auto-run commands; server-side web search; descendants of approved commands |
| ACP agents (per agent, per method; qualified individually) | `fs/*` and `terminal/create` client methods; `session/request_permission` (PEM-ACP-01..03) | agent-internal tools; terminal descendants |
| OpenCode, Pi | none (EXCLUDED; untrusted workers) | everything |

Generic grant lifecycle (scope, expiry, epoch, revocation, session restart) for these providers is qualified in R1 by
C-28 (PEM-GEN-01..04). OpenCode/Pi qualification (C-24) is R2.
