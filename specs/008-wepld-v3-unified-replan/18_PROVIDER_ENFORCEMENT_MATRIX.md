# 18 — Provider × Operation Enforcement Matrix (Astro H-2)

```text
STATUS = PROPOSED. Evidence = source reading at t3code@36d4d711 (R11 §3.2, Astro citations) and vendor documentation;
         nothing has been run. Every cell is re-verified at C-09 / C-24 admission; an unverified cell defaults to EXCLUDED.
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

## 4. Trusted tier at R1

Claude and Codex rows (after C-09 tests) and ACP agents individually qualified. OpenCode and Pi are available in R0/R1 as
untrusted workers: their effects are UNMEDIATED, their contexts have UNKNOWN coverage, and missions using them cannot
reach `COMPLETED_TRUSTED` until C-24 qualifies them.
