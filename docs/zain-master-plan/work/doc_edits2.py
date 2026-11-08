import pathlib, re, sys

def rep(fname, pairs):
    p = pathlib.Path(fname); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if a not in t:
            sys.exit(f'ANCHOR MISSING in {fname}: {a[:80]!r}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', fname)

def rep_block(fname, start, end, new):
    p = pathlib.Path(fname); t = p.read_text(encoding='utf-8')
    s = t.index(start); e = t.index(end, s) + len(end)
    p.write_text(t[:s] + new + t[e:], encoding='utf-8'); print('block', fname)

# ---------------- 05 architecture
rep('05-ARCHITECTURE-AND-DECISIONS.md', [
    ('    PA["Provider adapters: Codex app-server, ACP family, OpenCode, local OpenAI-compatible (Z-11)"]',
     '    PA["Provider adapters: Codex app-server, ACP family, OpenCode (also runs raw OpenAI-compatible routes, Z-11), user-provided Claude SDK (F-06)"]'),
    ('    IX["Index service (rg + tree-sitter + local embeddings, Z-28)"]', '    IX["Index service (rg + tree-sitter, Z-28; embeddings deferred)"]'),
    ('    AP["zain-approve: Core-owned approval surface (A1/A2/A3)"]', '    AP["zain-approve: Core-owned A1 approval surface (A2 is an isolated desktop window)"]'),
    ('  M <-- "WebSocket RPC (Zain-1)" --> O', '  R <-- "WebSocket RPC (Zain-1), per-launch client token" --> O'),
    ('  AP --> LG\n', '  AP --> PDP\n'),
    ('in the effect path, so R0 makes no mediation claim (ADR-Z01).', 'in the effect path, so R0 makes no mediation and no injection-control claim (ADR-Z01). The Core is the single ledger\nwriter; the approval surface reports to the policy decision point, never to the ledger directly.'),
    ('| Context engine | Repository index, retrieval, Brain notes, compaction capsules | Index API; `brain.query` MCP tool | Index (local), Brain (FTS5) | Ignored files never indexed; embeddings local only | Rebuild from source of truth | GATE-CTX-01 | rg + tree-sitter + FTS5 (REIMPLEMENT) | Z-28, M-03..M-05 |',
     '| Context engine | Repository index, retrieval, Brain notes, compaction capsules | Index API; `brain.query` MCP tool | Index (local), Brain (FTS5) | Ignored files never indexed; no embeddings until V3 ADR-006 is amended | Rebuild from source of truth | GATE-CTX-01 | rg + tree-sitter + FTS5 (REIMPLEMENT) | Z-28, M-03..M-05 |'),
    ('| Model gateway | Capability probes, routing, data classes, budgets | Provider adapter API; probe results; routing log | Endpoint registry, budgets | Remote endpoints untrusted; private data only to authorized routes | Explicit fallback chain; refuse with reason | GATE-MODEL-01, PROV-01 |',
     '| Model gateway | Capability probes, routing, server-side data classes, budgets, pre-session endpoint checks for hosted agents | Provider adapter API; probe results; routing log | Endpoint registry, budgets | Remote endpoints untrusted; private data only to authorized routes; agents\' own connections stay UNMEDIATED until R1/S-04 | Explicit fallback chain; refuse with reason | GATE-MODEL-01, GATE-MODEL-02, PROV-01 |'),
    ('| ADR-Z02 | Model access goes through a capability- and data-class-routed gateway; no hard-coded model names; no silent fallback to unauthorized routes | Provider neutrality; privacy; local-first | Z-11, Z-12 |',
     '| ADR-Z02 | Routes that Zain launches or configures go through a capability- and server-classified data-class gateway; hosted agents are checked before a session starts (effective endpoint and provider config); no hard-coded model names; no silent fallback. Agents\' own file reads and network calls are not covered and stay UNMEDIATED until C-17/S-04 | Provider neutrality; privacy; local-first; honest scope | Z-11, Z-12 |'),
    ('| ADR-Z05 | No verdict rests on one model; T2 sign-off needs an authorized route outside the builder\'s model family or the founder; otherwise REVIEW_BLOCKED | Independent review; resolves the hosted-provider review dependency | Z-06, V-01, K-08 |',
     '| ADR-Z05 | Consistent with V3 ADR-011: T2 work needs a qualified reviewer (the founder) plus security review; model reviews are advisory for T2 and may substitute only for T0/T1 when the model family differs from both the builder and the provider under test and the route is authorized for the data class; otherwise REVIEW_BLOCKED. V-01 checks model family, not just route | Independent review; resolves the hosted-provider review dependency | Z-06, V-01, K-08 |'),
    ('| ADR-Z03 | IDE parity in steps: external editor bridge, then Monaco plus local completion and index, then LSP/DAP; a Code-OSS fork only if Z-20\'s measurements justify reopening ADR-001 |',
     '| ADR-Z03 | IDE parity in steps: external editor bridge, then Monaco plus local completion and index, then LSP/DAP; Z-20 decides between Monaco + LSP client and monaco-vscode-api before F-17; a Code-OSS fork stays a desk estimate and reopens ADR-001 only by founder decision |'),
])
rep_block('05-ARCHITECTURE-AND-DECISIONS.md', '**R1 mediated file write by an ACP agent**', '```\n\n**Model routing', '''**R1 mediated file write by an ACP agent** (follows V3 07 §3 and 17 §1)

```mermaid
sequenceDiagram
  participant A as ACP agent
  participant S as Zain Server (PEP)
  participant C as Zain Core (PDP + ledger)
  participant U as Approval surface (A1 zain-approve / A2 window)
  participant F as fs-gate
  A->>S: fs/write(path, bytes)
  S->>S: stage bytes (staged object id, input digest)
  S->>C: propose{logical_operation_id, exact_target, input_digest, principal}
  C->>C: policy decision + coverage check
  alt needs approval
    C->>U: approval request (canonical binding, level)
    U-->>C: approve / deny / expire
  end
  C->>C: durable dispatch record (fsync; fencing epoch; staged object id)
  C-->>S: grant id (or deny)
  S->>F: write staged object via handle (no-follow, reparse rejected)
  F-->>S: APPLIED | NOT_APPLIED | UNKNOWN
  S->>C: report(outcome, evidence)
  C->>C: ledger append (hash chain)
  S-->>A: result
```

**Model routing''')
rep('05-ARCHITECTURE-AND-DECISIONS.md', [
    ('  T->>G: request(task_class=agent_edit, data_class=private-code, needs=[tool_calls])\n  G->>G: candidates = routes with probe(tool_calls)=pass AND data_class allowed AND budget left',
     '  T->>G: request(task_class=agent_edit, project, needs=[tool_calls])\n  G->>G: data_class = max(project class, content class); unknown fails closed\n  G->>G: candidates = routes with probe(tool_calls)=pass AND data_class allowed AND budget left AND endpoint identity verified'),
])

# ---------------- 06 models and review
rep('06-MODELS-CONTEXT-AND-REVIEW.md', [
    ('**Task classes and routing.** `agent_edit` needs tool_calls and json_schema. `completion` needs fim and the latency\nbound. `review` needs a route other than the builder\'s (V-01). `embed` needs embeddings and locality=local.\n`chat` needs streaming. A request names its task class and data class.',
     '**Task classes and routing.** `agent_edit` needs tool_calls and json_schema. `completion` needs fim and the latency\nbound. `review` needs a different model family from the builder (V-01). `chat` needs streaming. A request names its\ntask class; the **Server** assigns the data class. Workspace content is at least `private-code`, callers may only\nraise the class, and an unknown class fails closed.'),
    ('**Adapters.** One OpenAI-compatible adapter covers Ollama, llama.cpp server and LM Studio. Hosted agents keep their\nown T3 adapters (Codex app-server, ACP family, OpenCode).',
     '**Adapters and scope.** Raw OpenAI-compatible endpoints (Ollama, llama.cpp server, LM Studio, authorized remote\nendpoints) run through the existing OpenCode worker, which supplies the tool loop; Zain generates its provider\nconfiguration. Hosted agents keep their own T3 adapters (Codex app-server, ACP family). Before such a session starts,\nthe gateway checks the agent\'s effective endpoint and provider configuration and refuses routes not authorized for\nthe project\'s data class, including the configured third-party relay. Localhost runtimes are bound to their owning\nprocess image or started with a per-session token, so a spoofed listener cannot receive private prompts. The\ngateway does **not** cover files an agent reads by itself or connections it opens itself; those stay UNMEDIATED until\nR1 (C-17) and the OS network proxy (S-04).'),
    ('- Model-based review is advisory. It may use a route only if that route is authorized for the data class.\n- T2 sign-off needs either the founder or an authorized route from a different model family than the builder.',
     '- Model-based review is advisory. It may use a route only if that route is authorized for the data class.\n- Consistent with V3 ADR-011: T2 sign-off needs the founder (qualified reviewer) plus security review. A model route\n  may substitute only for T0/T1, and only when its model family differs from both the builder and the provider under\n  test. A ChatGPT-backed OCR review of Codex-built work is the same family and does not qualify.'),
    ('| Embeddings (optional) | Local embedding model through the gateway (`embed` class) | Local vector store next to the index | Never sent off the machine |',
     '| Embeddings | Deferred: V3 ADR-006 defers vector search for v1; an ADR amendment is required first | — | Would be local-only |'),
])
pathlib.Path('06-MODELS-CONTEXT-AND-REVIEW.md').write_text(pathlib.Path('06-MODELS-CONTEXT-AND-REVIEW.md').read_text(encoding='utf-8').replace(
    '- embeddings for the local index (Z-28);\n', '- embeddings for the local index, once V3 ADR-006 is amended;\n'), encoding='utf-8')
