# 06 — Models, Context and Review

```text
SCOPE    = model gateway (provider neutrality, local-first, data classes, budgets), context engine, review routes
EVIDENCE = founder machine measured 2026-11-08; competitor docs (03); V3 18_PROVIDER_ENFORCEMENT_MATRIX.md, R03C §10.5
TASKS    = Z-10, Z-11, Z-12, Z-28, Z-06; V3 B-06, F-22, C-24, V-01, K-04..K-11
```

## 1. Hardware reality on the founder machine (measured 2026-11-08)

| Resource | Value | Consequence for models |
|---|---|---|
| CPU | Intel Core i5-13420H, 8 cores / 12 threads | CPU inference only |
| GPU | Intel UHD Graphics (integrated, about 1 GB reported) | No CUDA; no useful GPU offload for large models |
| RAM | 15.7 GB total, very little free at sample time | Electron + Node server + Rust core + a browser + a local model compete for memory |
| Disk | C: 3.4 GB free; D: 20 GB free | A 7B Q4 model is about 4–5 GB; space competes with builds (Z-07) |
| Local runtimes | Ollama directory present with no models; LM Studio and llama.cpp not found on PATH | Nothing local is ready today |
| Existing logins | Codex CLI config present; OpenCode configured through a third-party relay; Alibaba OCR CLI configured with provider "chatgpt" | Hosted routes exist but none is authorized for private Zain code in writing |

**Verdict on the "no paid provider" experience (I, to be measured in Z-11).** A fully local experience at the quality
of hosted frontier models is **not practical** on this machine. CPU-only 7B-class models generate only a few tokens
per second and handle multi-step tool use poorly. Even vendors that support local models warn against small ones for
agents (03 §1). Local models are practical for:

- fill-in-the-middle completion with a small code model (1–3B), if GATE-PERF-07 latency holds;
- embeddings for the local index, once V3 ADR-006 is amended;
- classification and triage (the d1-local 600M classifier is advisory only and must never approve);
- offline or air-gapped fallback for simple edits.

Agent turns at useful quality need a hosted route the founder already pays for or holds, used through the provider's
official login: the Codex CLI is V3's default (DEC-08). Zain must state this limitation in onboarding, not hide it.

**Provider policy constraint (V3 R03C §10.5).** Anthropic does not allow third-party products to route requests
through users' Claude Free/Pro/Max credentials. Zain therefore never extracts or relays subscription credentials. A
user can still run an official CLI in Zain's terminal; such effects are UNMEDIATED in V3 terms.

## 2. Gateway design (ADR-Z02, Z-11)

**Capability record per route** (filled by probes, never assumed from the model name):

| Field | Probe |
|---|---|
| `tool_calls` | Round-trip of a forced tool call with a JSON-schema argument |
| `json_schema` | Strict structured output against a schema |
| `context_tokens` | Largest prompt accepted, measured in steps |
| `fim` | Prefix/suffix completion request |
| `vision` | Small image description |
| `embeddings` | Embedding endpoint returns vectors of stable dimension |
| `streaming` | Token stream with cancellation |
| `latency_p50_ms`, `tokens_per_s` | Measured on this machine |
| `locality` | local / LAN / remote |
| `data_classes_allowed` | Set by the founder: `public`, `private-plan`, `private-code`; `secrets` is never allowed |
| `cost_class`, `budget` | FREE / subscription / PAID; per-task and per-day token and time caps |

**Task classes and routing.** `agent_edit` needs tool_calls and json_schema. `completion` needs fim and the latency
bound. `review` needs a different model family from the builder (V-01). `chat` needs streaming. A request names its
task class; the **Server** assigns the data class. Workspace content is at least `private-code`, callers may only
raise the class, and an unknown class fails closed. The gateway picks the cheapest qualified route
with budget left, local first. If none qualifies it **refuses with a reason**: there is no silent fallback.

**Adapters and scope.** Raw OpenAI-compatible endpoints (Ollama, llama.cpp server, LM Studio, authorized remote
endpoints) run through the existing OpenCode worker, which supplies the tool loop; Zain generates its provider
configuration. Hosted agents keep their own T3 adapters (Codex app-server, ACP family). Before such a session starts,
the gateway checks the agent's effective endpoint and provider configuration and refuses routes not authorized for
the project's data class, including the configured third-party relay. Localhost runtimes are bound to their owning
process image or started with a per-session token, so a spoofed listener cannot receive private prompts. The
gateway does **not** cover files an agent reads by itself or connections it opens itself; those stay UNMEDIATED until
R1 (C-17) and the OS network proxy (S-04). Anthropic-compatible adapters exist only for providers the
founder has authorized with an API key, never via subscription credentials.

**Defaults.** A newly added remote endpoint starts with `data_classes_allowed = {public}`. The founder must mark it
for private use. Secrets are stripped from prompts by a redaction pass, and ignored files never enter prompts.

## 3. Resolving the hosted-provider review dependency

The status context for this session described a review component that depended on an unauthorized hosted provider.
That component is Ascout's E6B; Zain has the same problem in two places (01 §7):

1. **Program review** (who reviews Zain's own changes and plans). Today's local options are a hosted provider behind
   the OCR CLI, a third-party relay behind OpenCode, or a 600M advisory classifier.
2. **Product review** (Zain Code Review, K-tasks). V3 already makes delegated review the default and keeps the engine
   lane local-only until its proxy exists (K-09, K-10).

**Resolution (ADR-Z05, Z-06, DEC-01).**

- Deterministic local checks always run: tests, the validator, linters, Opengrep rules, secret scanning.
- Model-based review is advisory. It may use a route only if that route is authorized for the data class.
- Consistent with V3 ADR-011: T2 sign-off needs the founder (qualified reviewer) plus security review. A model route
  may substitute only for T0/T1, and only when its model family differs from both the builder and the provider under
  test. A ChatGPT-backed OCR review of Codex-built work is the same family and does not qualify.
- When no such route exists, the gate is `REVIEW_BLOCKED`. Work can proceed to `DONE_UNREVIEWED`, never to `DONE`.
- The Code Review findings schema is the same for every route, so routes can change without changing gates.

## 4. Context engine (Z-28 and V3 M-03..M-05)

| Layer | What | Where it lives | Privacy rule |
|---|---|---|---|
| Text search | ripgrep over the workspace | Index service in Server | Honors .gitignore and .zainignore |
| Symbols | tree-sitter symbol tables for TS/JS, Python, Rust, Go, C# | Index service | Same |
| Embeddings | Deferred: V3 ADR-006 defers vector search for v1; an ADR amendment is required first | — | Would be local-only |
| Conversation context | T3 thread history plus compaction capsules (M-05) | Server state, Core Brain | Capsules are summaries with source links |
| Project memory | Brain notes, preferences, spec index (FTS5) | Core | Preferences start as CANDIDATE (ADR-006) |

Retrieval for a turn is budgeted by the route's measured `context_tokens`. The agent sees file paths and line
ranges, so every claim can be traced back.

## 5. Verification

| Gate | What it proves |
|---|---|
| GATE-MODEL-01 | No private-class request reaches an unauthorized endpoint; capability mismatches are refused |
| GATE-PERF-07 | Local completion latency on this CPU, or the lane disables itself |
| GATE-CTX-01 | Offline indexing within bounds and zero egress |
| GATE-REV-01 | An authorized independent review route exists, or REVIEW_BLOCKED is recorded |
| GATE-J03, GATE-J16 | Model setup and switching work end to end on the installed build |
