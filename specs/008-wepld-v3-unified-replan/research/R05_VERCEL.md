# R05: Vercel durability research (Workflow SDK and durable-harness)

- **Mission:** 008-wepld-v3-unified-replan. This is planning research only. Nothing was installed, built, run or tested.
- **Date:** 2026-10-27. Every URL below was accessed on 2026-10-27.
- **Method:** Shallow clones were read at the source level. Vendor blog posts and docs were fetched. GitHub and npm metadata came from `gh api` and the npm registry. The text of both repositories was treated as data, not as instructions.
- **Notation:** `path@SHA7` refers to a file in the pinned clone. Line numbers are approximate. The text says **UNKNOWN** wherever a claim could not be verified from source or primary docs.

---

## 0. Pins

### 0.1 Source repositories (shallow clones under `_work/src/`)

| Repo | Local path | Commit SHA (HEAD, `main`) | Commit date | License | NOTICE file |
|---|---|---|---|---|---|
| vercel/workflow | `_work/src/workflow` | `af8c6d3295ebc9aa7c0168cd0ca5007f62e6b9ba` | 2026-10-26T15:13:23-07:00 | Apache-2.0 (`LICENSE.md`, "Copyright 2025 Vercel Inc.") | none in repo root |
| vercel-labs/durable-harness | `_work/src/durable-harness` | `ea8aa4060cf4fb8cd39737ce8ab21c4e0f40c741` | 2026-10-23T08:24:03-07:00 | Apache-2.0 (`LICENSE.md`, "Copyright 2026 Vercel Inc.") | none |
| pingdotgg/t3code (comparison only, clone already present) | `_work/src/t3code` | `36d4d711b79c73eb33131944f73ea4a8c6156484` | 2026-10-27T07:17:36-07:00 | MIT (GitHub API) | not checked |

Short SHAs used in citations: **W** = `af8c6d3` (workflow), **H** = `ea8aa40` (durable-harness), **T** = `36d4d71` (t3code).

`vercel/workflow` also ships `DCO.txt`, which is a contributor sign-off requirement. It places no obligation on consumers.

### 0.2 Repo health (GitHub API, 2026-10-27)

| Repo | Stars | Forks | Open issues+PRs | Created | Last push | Commits on default branch | Contributors |
|---|---|---|---|---|---|---|---|
| vercel/workflow | 2,475 | 390 | 459 | 2025-10-23 | 2026-10-27 | ~2,048 | ~139 |
| vercel-labs/durable-harness | 255 | 12 | 7 | 2026-10-16 | 2026-10-23 | 25 | 4 |
| mizzle-dev/workflow-worlds (Turso/Redis/Mongo community Worlds) | 32 | 10 | 10 | 2025-11-29 | 2026-06-02 | n/a | n/a (repo-level license field is `null`; the npm packages say MIT) |

Test footprint at the pins:
- **workflow:** 469 `*.test.ts(x)/mts` files. `packages/world-testing` is a World conformance suite covering idempotency, event-ids, in-band-fence, hooks, inline-execution and more.
- **durable-harness:** 237 test files. About 52k test lines against about 78k non-test TS lines across the monorepo.

### 0.3 npm versions (registry, 2026-10-27)

| Package | `latest` | Published | License | In-repo version at pin |
|---|---|---|---|---|
| `workflow` | 5.2.3 | 2026-10-20 | Apache-2.0 | 5.2.3 |
| `@workflow/core` | 5.2.3 | 2026-10-20 | Apache-2.0 | 5.2.3 |
| `@workflow/world` (interface) | 5.0.5 | 2026-10-20 | Apache-2.0 | 5.0.5 |
| `@workflow/world-local` | 5.1.2 | 2026-10-20 | Apache-2.0 | 5.1.2 |
| `@workflow/world-postgres` | 5.0.5 | 2026-10-20 | Apache-2.0 | 5.0.5 |
| `@workflow/world-vercel` | 5.2.3 | 2026-10-20 | Apache-2.0 | 5.2.3 |
| `@workflow/ai` | 5.0.3 | 2026-10-12 | Apache-2.0 | 5.0.3 |
| `durable-harness` | 0.0.1 (beta tag `0.0.1-beta.6`) | 2026-10-23 | Apache-2.0 | 0.0.1 |
| `@workflow-worlds/turso` | 0.2.2 | 2026-02-09 | MIT | n/a |
| `@workflow-worlds/redis` | 0.2.2 | 2026-02-09 | MIT | n/a |

Runtime dependency pins worth noting:
- **`@workflow/world-postgres`:** `graphile-worker 0.16.6`, `pg 8.20.0`, `drizzle-orm 0.45.2`, `cbor-x 1.6.0` (`packages/world-postgres/package.json@W`).
- **`durable-harness`:** `@workflow/world ^5.0.4`, `@workflow/world-local ^5.1.1`, `@workflow/world-vercel ^5.2.1`, `@vercel/oidc 3.2.0`, `ws 8.21.3`. It declares `engines.node >=22`. Tracing needs Node 24 according to its CHANGELOG (`packages/durable-harness/package.json@H`, `CHANGELOG.md@H`).

### 0.4 Primary web sources

| ID | URL | What it is |
|---|---|---|
| B1 | https://vercel.com/blog/introducing-workflow | WDK launch post, 2025-10-23 |
| B2 | https://vercel.com/blog/making-every-harness-durable | durable-harness post, 2026-10-19 |
| D1 | https://vercel.com/docs/agent-harnesses/self-hosting | durable-harness self-hosting |
| D2 | https://vercel.com/docs/agent-harnesses/tools | replay rules, files, documents |
| D3 | https://vercel.com/docs/workflows/pricing | Vercel Workflow pricing and limits (page `last_updated` 2026-09-16) |
| D4 | useworkflow.dev / workflow-sdk.dev docs | Mirrored in-repo at `docs/content/docs/v5/**` and `docs/content/worlds/v5/**` @W. The in-repo copy was used as the citable source. |

---

## 1. Executive summary

1. **The Workflow SDK** (`workflow` 5.2.3) is a deterministic-replay, event-sourced durable-execution engine for TypeScript. `"use workflow"` functions are replayed from an append-only per-run event log in a sandboxed `node:vm` (or QuickJS) context with seeded `Math.random`, a fixed `Date` and seeded `crypto`. `"use step"` functions run with full Node access, and their results are memoized in the log. Its guarantees are at-least-once per step attempt, with memoization of committed outcomes. The vendor documents this plainly: the Postgres World README says handlers "still need to tolerate at-least-once execution". The SDK never claims exactly-once for side effects. It offers `stepId` as an idempotency key and leaves deduplication to the external API.

2. **durable-harness** (`0.0.1`, 9 days old at the pin, 25 commits, 4 contributors) does **not** use the `"use workflow"`/`"use step"` compiler or the `@workflow/core` replay runtime. Its kernel (`packages/harness-world`, private, bundled into the published package) writes directly to the **World interface** (`@workflow/world`). Each agent session is a run, and every model or tool call is an "effect sandwich": an intent (`step_started` with an envelope), then the body, then an outcome (`step_completed`/`step_failed`). Two replay classes exist, `'safe' | 'never'` (`packages/harness-world/src/types.ts@H` L10-19). An interrupted `never` effect is resolved to `step_failed` with the message "...not safe to rerun. It may or may not have taken effect." plus any partial progress (`driver.ts@H` ~L1527-1570). The model then decides what to do. This is an honest unknown-outcome surface, not exactly-once.

3. **The World interface** is the reusable asset. It is `interface World extends Queue, Streamer, Storage` (`packages/world/src/interfaces.ts@W` L740). It specifies dense, 1-based slot event IDs with bump-and-report semantics, an optional in-band writer fence for fencing tokens, hook-resume deduplication, and capabilities that fail closed.

4. **Running locally without Vercel is technically possible but not production-grade on the bundled Local World.**
   - **Local World:** it stores JSON files with temp-file-plus-rename and no `fsync` (`packages/world-local/src/fs.ts@W` ~L475-530). Its queue is **in memory**, and recovery happens by re-enqueueing pending and running runs on `start()`. The vendor states it "is designed for development, not production" (`docs/content/worlds/v5/local.mdx@W`, Limitations).
   - **Data loss on upgrade:** the Local World silently **deletes** a pre-5.1.0 flat-layout data directory on start.
   - **Postgres World:** a "reference implementation". It does not authenticate its flow route and does not encrypt data (D1, `packages/world-postgres/README.md@W`).
   - **Community Worlds (Turso, Redis, Mongo):** published in Feb 2026 at 0.2.2. **Compatibility with the v5 spec is UNKNOWN or unlikely.** v5 requires slot-numbered event IDs, and the vendor says compatibility tests are being "brought back" (`docs/content/worlds/v5/upgrading-to-v5.mdx@W`).

5. **Against the four "never forget" properties** (§5):
   - **(1) Execution durability:** the SDK provides it, given a durable World.
   - **(2) Semantic/project memory:** not provided. durable-harness adds only per-session typed "documents" of at most 64 KB.
   - **(3) Scheduling/continuation:** provided (durable `sleep`, hooks, webhooks, continue-as-new via `start()`). Cron is not provided on non-Vercel Worlds.
   - **(4) Safe effect authority:** only partial.
     - Provided: idempotency-key plumbing (`stepId`), the replay classes in durable-harness, and fencing (in-band fence and epochs).
     - Not provided: reconciliation of unknown-outcome effects beyond telling the model, and permission revalidation on resume.

6. **Recommendation, in short:** use both as **pattern sources, not dependencies**, for a local-first desktop or CLI product.
   - **Adopt** the World contract ideas, the intent/outcome sandwich, the `safe`/`never` classes, fencing tokens and the chaos-drill test style.
   - **Reject** a runtime dependency on durable-harness. It is 0.0.x, Vercel Sandbox and AI Gateway are central to it, and Claude Code and Codex adapters run *only* in Vercel Sandbox.
   - **Consider** `workflow` plus a custom SQLite World only if we accept its compiler and bundler integration and its HTTP queue-callback architecture. Its Electron compatibility is UNKNOWN.

---

## 2. Workflow SDK path-level analysis (@W)

### 2.1 Directives and the compiler transform

| Item | Finding | Citation |
|---|---|---|
| Compiler | The SWC plugin `@workflow/swc-plugin` 5.0.1 has three modes. **Step mode** keeps step bodies, registers them, and replaces workflow bodies with a throw carrying `workflowId`. **Workflow mode** replaces step bodies with `globalThis[Symbol.for("WORKFLOW_USE_STEP")]` and keeps workflow bodies. **Detect mode** is used for discovery. Client mode merged into step mode in 5.0. | `docs/content/docs/v5/how-it-works/code-transform.mdx@W`; `packages/swc-plugin-workflow` |
| IDs | `step//{filepath}//{functionName}` and `workflow//{filepath}//{functionName}`. Identity is therefore **file path plus function name**, so renaming or moving a file changes it. | same |
| Integration | Bundler or framework plugins exist for next, vite, rollup, nitro, nuxt, sveltekit, astro, nest and vitest (`packages/*`). A documented Bun integration example uses a Bun plugin plus `workflow build`. | `docs/content/docs/v5/how-it-works/framework-integrations.mdx@W` |
| Execution route | Workflow orchestration and queued steps are served by one combined HTTP flow route, `/.well-known/workflow/v1/flow`, and webhooks by `/.well-known/workflow/v1/webhook/:token`. | code-transform.mdx; `docs/content/docs/v5/foundations/hooks.mdx@W` |
| Outside a workflow | Calling a step outside a workflow is a plain function call, with no retries and no durability. | `foundations/workflows-and-steps.mdx@W` |

### 2.2 Event log schema

The event type enum is defined in `packages/world/src/events.ts@W` L19-46:

| Entity | Events | Notes |
|---|---|---|
| Run | `run_created`, `run_started`, `run_completed`, `run_failed`, `run_cancelled` | `run_created` carries the deploymentId, workflowName, input and executionContext |
| Attribute | `attr_set` | experimental |
| Step | `step_created`, `step_started`, `step_completed`, `step_failed`, `step_retrying` | `step_started.eventData.ownerMessageId` is the inline-ownership lease (§2.6). `step_retrying.retryAfter` sets the backoff |
| Hook | `hook_created`, `hook_received`, `hook_disposed`, `hook_conflict` | the world writes `hook_conflict` |
| Wait | `wait_created`, `wait_completed` | a wait completes at most once |
| System | `noop` | sealed-log filler (spec ≥7), written by the backend only |

Storage contract (`interfaces.ts@W` L170-185, L366-394):
- The log is append-only. Run, step and hook entities are materialized views and are never mutated directly.
- **Event IDs are slots:** `evnt_` followed by a dense 1-based position, zero-padded to 26 characters.
- **Bump and report:** a create never fails because its slot is taken. The World commits at the next free slot and returns the events it skipped.
- Readers must always see a prefix of the log, never a log with a hole.

Correlation: a step's `correlationId` is its `stepId`, a hook's is its `hookId` and a wait's is its `waitId`.

Duplicate handling: concurrent replays can commit duplicate `step_created`, `step_started` or `wait_created` events. These are "committed but inert", because replay groups events into classes and skips a duplicate class for an entity (`how-it-works/event-sourcing.mdx@W` "Duplicate events").

Spec versions (`packages/world/src/spec-version.ts@W`):
- Current spec is **8** (`HOOK_FORCE_CLAIM`). Version 6 introduced slot identity, version 7 the sealed log.
- The runtime refuses a World outside `[floor=6, ceiling=8]`.
- Each run keeps the spec version it was stamped with for its whole life.

### 2.3 Step memoization and deterministic replay

- **Each delivery re-executes from the top.** Every workflow-handler delivery re-runs the workflow function from the beginning. The `WORKFLOW_USE_STEP` hook returns the cached result when the log has a terminal event for that call position, and otherwise suspends and runs the step. Steps usually run **inline** in the same invocation until an inline budget or the invocation deadline is reached (code-transform.mdx, workflows-and-steps.mdx).
- **Two engines** (`packages/core/src/runtime/vm-mode.ts@W`):
  - `node:vm` is the default.
  - `quickjs` (WASM) is opt-in through `WORKFLOW_VM=quickjs`. It enables VM-memory snapshots (`experimental_snapshots` on the World), so a run resumes from a snapshot plus the events after it instead of replaying the whole log.
  - QuickJS runs are exempt from the 25k-event ceiling (D3; `configuration/worlds.mdx@W` `WORKFLOW_MAX_EVENTS`).
- **Replay cost grows with the log.** Vercel caps a run at **25,000 events** and **10,000 steps** on node:vm, with **240 s maximum replay duration**. It warns of slowdown past about 2,000 events (D3). The local default for `WORKFLOW_MAX_EVENTS` is 25,000.
- **Divergence handling:** `REPLAY_DIVERGENCE` is a runtime signal. The runtime re-queues another replay up to a budget. If the budget is exhausted, the run fails with `CORRUPTED_EVENT_LOG` (`docs/content/docs/v5/errors/replay-divergence.mdx@W`).

### 2.4 How non-deterministic code is handled

From `packages/core/src/vm/index.ts@W` L48-140:
- `Math.random` is replaced by `seedrandom(seed)`. The seed is derived from run identifiers, and `crypto.getRandomValues` and `crypto.randomUUID` use the same RNG.
- `Date()`, `new Date()` and `Date.now()` return a fixed timestamp that advances deterministically with the log.
- These are deleted from the workflow realm: `Atomics.waitAsync`, async `WebAssembly.compile/instantiate*`, `WeakRef` and `FinalizationRegistry`.
- `crypto.subtle` methods other than a synchronous-digest `digest` throw.
- `fetch` and Node modules are disallowed inside workflow functions (errors `fetch-in-workflow`, `node-js-module-in-workflow`, `timeout-in-workflow`).
- The comment notes this is "best-effort, for non-adversarial code". Determinism is a *convention enforced by sandbox restrictions*, not a proof.

The docs warn that seeded randomness is predictable. Hook tokens generated in a workflow are "hard to guess, not secret", so secrets must be generated in a step (`foundations/hooks.mdx@W` Security).

### 2.5 Sleep, hooks, webhooks and human-in-the-loop

| Primitive | Semantics | Citation |
|---|---|---|
| `sleep(duration)` | Writes `wait_created`, then `wait_completed` exactly once (an atomic entity transition). No limit on Vercel (D3). Local World: delayed redelivery uses `setTimeout`, clamped to 2^31-1 ms, and recomputes from persisted state. Restart recovery re-enqueues runs. | event-sourcing.mdx; `packages/world-local/src/queue.ts@W` L60-67 |
| `createHook({token})` / `defineHook` | Registration commits only when the workflow suspends. Active tokens are globally unique, and a duplicate gives `hook_conflict`, after which `getConflict()` returns the owner `Run`. `experimental_minRetention` keeps the token reserved after the run ends. `experimental_force` takes a token over (spec ≥8, `hookForceClaim` capability). | `foundations/idempotency.mdx@W`, `foundations/hooks.mdx@W`, `interfaces.ts@W` L682-705 |
| `resumeHook(token, payload)` | Delivers a `hook_received` event. **Transport retries of one call** are deduplicated through a per-call `resumeId` plus payload digest when the World declares `hookResumeDedup` (local and postgres: yes, statically). `resumeId` is a fresh ULID per call (`packages/core/src/runtime/resume-hook.ts@W` L44, L499). **Two separate deliveries of the same external webhook are NOT deduplicated by the SDK**, so the application must dedupe on the provider's event ID. | `interfaces.ts@W` L646-680 |
| `createWebhook()` | Public route `/.well-known/workflow/v1/webhook/:token`. "the token in that URL is the only authorization performed". | `foundations/hooks.mdx@W` |
| Human in the loop | A hook or webhook raced with `sleep` (`Promise.race`) gives approval with a timeout. Cookbook pages: `cookbook/agent-patterns/human-in-the-loop.mdx`, `ai/human-in-the-loop.mdx`. | in-repo docs @W |

### 2.6 Queue and scheduler semantics

Queue interface (`packages/world/src/queue.ts@W` L607-750):
- Methods: `queue(name, payload, {idempotencyKey, delaySeconds, deploymentId, region})`, optional `queueBatch`, `createQueueHandler(prefix, handler)` returning an HTTP `(Request)=>Response`, optional `registerHandler(prefix, fn)` for in-process delivery (local and postgres), optional `registerRoute`, and optional `invoke` (request/response, capability-gated).
- **Delivery is at-least-once.** "A rejected handler must retry the same message with an incremented attempt." `meta.messageId` SHOULD be stable across redeliveries. `deliveryCount` and `createdAt` are reported where known.
- **`invoke` transport errors are unknown outcomes:** "the request may have been successfully processed by the executor... and the success result may be lost."

Inline step ownership and liveness (`docs/content/docs/v5/changelog/step-message-ownership.mdx@W`; `packages/core/src/runtime/constants.ts@W` L478-500):
- An inline step stamps the owning queue `messageId` on `step_started`.
- Other wakes defer re-execution until an ownership **lease of 860 s** (clamped to 1..900 s) expires.
- The vendor rejected heartbeats and lock stores and reused the queue's un-acked-message state as the liveness signal.
- **Implication:** a self-hosted, multi-instance inline step that runs longer than about 15 min can be re-executed concurrently, because the lease cannot be raised past 900 s.

Delivery budget (`constants.ts@W` L4-40):
- `MAX_QUEUE_DELIVERIES = 48`. On Vercel, with backoff capped at 900 s per hop, that is about 9-10 h of wall clock.
- After that the run fails with `MAX_DELIVERIES_EXCEEDED`, which bounds survival through a backend or network outage.
- world-postgres sizes its Graphile attempt cap from this value.

Concurrency limits:
- Local World: `WORKFLOW_LOCAL_QUEUE_CONCURRENCY` default 1000 concurrent handlers, in-process.
- Postgres World: `queueConcurrency` default 50, poll interval 500 ms (`configuration/worlds.mdx@W`).

Scheduling and cron:
- No built-in cron primitive in the SDK was found. Recurring work is modelled as `sleep` loops or self-restarting runs (`cookbook/common-patterns/scheduling.mdx@W`).
- On Vercel, the platform cron exists separately (D3 lists "Schedules/cron: No limit"). **Cron on self-hosted Worlds: UNKNOWN / not provided.**

### 2.7 Retries and backoff

- Default `maxRetries = 3`, so 4 attempts in total (`packages/core/src/runtime/step-executor.ts@W` L74; `foundations/errors-and-retries.mdx@W`). It is set per step with `fn.maxRetries = n`.
- "Steps get enqueued immediately after a failure", so the default retry has **no backoff**. Backoff comes from `RetryableError({ retryAfter })` (a duration string, ms or a Date) and is stored on `step_retrying.retryAfter`.
- `FatalError` skips retries. Serialization failures and aborts are treated as fatal.
- Backend connection failures retry on existing policies. The docs add: "A connection failure does not prove that the backend rejected a write: it may have accepted it before the response was lost" (`errors-and-retries.mdx@W`).
- Compensation is a user-level **saga** pattern (rollbacks as steps, which must be idempotent). The SDK has no automatic compensation.

### 2.8 Idempotency keys

- **Step level:** `getStepMetadata().stepId` is "stable across retries" and is meant to be passed as the external API's idempotency key (`foundations/idempotency.mdx@W`). This works only for APIs that support keys.
- **Run level:** no atomic "start-if-absent". The pattern is a deterministic hook token plus `hook.getConflict()` inside the workflow. The vendor admits the race: "two concurrent requests can both observe 'no hook yet' and each call `start()`" and a native API "is in the works" (`idempotency.mdx@W` warn callout).
- **Queue level:** `QueueOptions.idempotencyKey`. On the Local World this is an **in-memory** `Map` of in-flight messages that is lost on restart (`world-local/src/queue.ts@W` L184-232). On Postgres it is a Graphile job key; the DB-durability of that key is UNKNOWN, not verified.

### 2.9 World interface (exact)

The file is `packages/world/src/interfaces.ts@W`, `export interface World extends Queue, Streamer, Storage` (L740). Its members:

| Group | Methods (required unless marked "?") |
|---|---|
| `Storage.runs` | `get`, `waitForTerminalStatus?`, `getMany?`, `list`, `experimentalSetAttributes?`, `cancelMany?` |
| `Storage.steps` | `get`, `list` |
| `Storage.events` | `create(runId\|null, data, params)` for `run_created`, `create(runId, data, params)`, `createBatch?`, `get`, `list`, `listByCorrelationId` |
| `Storage.hooks` | `get`, `getByToken`, `list` |
| `Storage.experimental_snapshots?` | `save`, `load`, `delete` (QuickJS VM snapshots) |
| `Streamer.streams` | `createWriteSession?`, `write`, `writeMulti?`, `close`, `get`, `list`, `getChunks`, `getInfo`; `streamFlushIntervalMs?` |
| `Queue` (`queue.ts`) | `getDeploymentId`, `queue`, `queueBatch?`, `createQueueHandler`, `registerHandler?`, `registerRoute?`, `invoke?`, `isDeploymentUnavailableError?` |
| World extras | `specVersion` (required), `capabilities?`, `analytics?`, `start?`, `close?`, `getRuntimeDeadline?`, `getEncryptionKeyForRun?`, `createRunId?`, `regionForRunId?`, `resolveLatestDeploymentId?`, `uploadDynamicWorkflowCode?`, `getEnvironment?`, `describeRun?`, `validateRunExecutionContext?`, `telemetry?` |
| `WorldCapabilities` | `invoke`, `hookRetention`, `maxConcurrency`, `inBandFence`, `hookResumeDedup`, `hookForceClaim`, `deploymentAffinity`, `dynamicWorkflowCode`. All fail closed. |

**In-band writer fence** (`inBandFence`, L609-644):
- The World keeps a per-run `seqInBand` counter.
- An `inBand: true` create must carry `expectedSeqInBand`. On a mismatch the World throws `InBandSupersededError` (HTTP 412) and writes nothing.
- This is a **fencing token** primitive at the storage layer, with a conformance test in `packages/world/src/test-support/in-band-fence-conformance.ts@W`.
- Note from the source: "the runtime does not send the fence yet". Only durable-harness uses it today.
- Local and postgres implement it. world-local does so with a lock file (`world-local/src/index.ts@W` ~L160-165).

### 2.10 Local World (`@workflow/world-local` 5.1.2)

| Aspect | Finding | Citation |
|---|---|---|
| Storage | JSON files under `WORKFLOW_LOCAL_DATA_DIR` (default `.workflow-data`), per-run `events/<runId>/` and `steps/<runId>/`, `.locks/` for claims and terminal markers | `docs/content/worlds/v5/local.mdx@W`; `world-local/src/storage/*` |
| Atomicity | Writes go to a temp file and are renamed into place (`withWindowsRetry` around rename). Create-if-absent uses `wx` or link-based promotion. **No `fsync` or `fdatasync` anywhere** (grep found none). | `world-local/src/fs.ts@W` L475-530, L585-600 |
| Multi-writer | "does not protect against concurrent writes from multiple processes... last writer wins". Hook-token and in-band fence paths use lock and claim files. | `fs.ts@W` L475-482 |
| Queue | **In memory.** It delivers by HTTP POST to the app (undici, or `node:http` with `WORKFLOW_NODE_HTTP=1`), or in-process via `registerHandler`. Delayed messages use `setTimeout`. | `world-local/src/queue.ts@W`; local.mdx |
| Recovery | `start()` re-enqueues pending and running runs (`WORKFLOW_LOCAL_RECOVER_ACTIVE_RUNS`, default true) and calls `releaseOrphanedSteps` so inline steps from a dead process rerun immediately rather than after the 860 s lease. An interrupted attempt **counts toward retries**, so a `maxRetries: 0` step fails on restart. | local.mdx; `world-local/src/index.ts@W` L160-240 |
| Single-instance assumption | "Recovery assumes that nothing else is running workflows on the same data directory and tag" (including an older worker thread after a dev-server reload), "the step can run twice" | local.mdx |
| Upgrade hazard | "Data written by `@workflow/world-local` releases before 5.1.0 uses a flat layout and is not migrated: when the World starts on a data directory that holds only flat-layout files, it logs a warning, **deletes the directory**, and starts with an empty one." | local.mdx "Data directory layout" |
| Vendor position | "The Local World is designed for development, not production: In-memory queue... Filesystem storage... Single instance... No authentication" | local.mdx "Limitations" |
| Encryption | Not implemented (only the Vercel manifest entry lists `encryption`) | `worlds-manifest.json@W` |

**Verdict:** a persistent local disk plus `recoverActiveRuns` gives **crash recovery for a single process**. The lack of `fsync` means power loss can lose acknowledged writes. The queue's idempotency map is volatile. Data directories are deleted across one documented upgrade boundary. It is **not production-capable offline** by the vendor's own statement. For durable-harness, Vercel says the Local World "suits development, and a single server whose disk persists" (D1).

### 2.11 Postgres World (`@workflow/world-postgres` 5.0.5)

- **Architecture:** Drizzle schema, one `pg.Pool`, and **graphile-worker 0.16.6** as the queue. A separate `pg.Client` handles `LISTEN/NOTIFY`, which drives stream chunks and the terminal-status long-poll (`packages/world-postgres/HOW_IT_WORKS.md@W`).
- **Tables** (`src/drizzle/schema.ts@W`): runs, events, `workflow_event_slots`, steps, hooks, waits, invocations, `workflow_snapshots` and streams. There are unique indexes `workflow_events_hook_resume_unique` and `workflow_events_entity_creation_unique`. Schema history spans 28 SQL migrations (`src/drizzle/migrations/`). Bootstrap is `npx --package=@workflow/world-postgres bootstrap`, which is idempotent and must be re-run after upgrades (D1).
- **Delayed jobs:** `{timeoutSeconds}` becomes a new Graphile job with a future `runAt`, which is durable rescheduling.
- **Security:** "does **not** automatically authenticate the requests that drive workflow execution". The flow route is "publicly reachable by default" (`README.md@W` §Security). It does not encrypt data either (D1 Limitations).
- **Shutdown:** "Because aborting a client request does not prove that its server handler stopped, workflow and step handlers still need to tolerate **at-least-once execution**" (HOW_IT_WORKS.md).
- **Vendor stance:** "for production use-cases, we highly recommend cloning this reference implementation and adapting it" (README).
- **Multi-instance:** several servers on one DB is supported. "the World lets one server at a time drive a session", which the in-band fence provides (D1).

### 2.12 Other Worlds

`worlds-manifest.json@W` lists:
- **Official:** local, postgres, vercel.
- **Community:** Turso, MongoDB, Redis (mizzle-dev); SurrealDB; Jazz; the vinnymac "fantasticfour" set (redis, redis-bullmq, cloudflare, mysql, azure, nats-jetstream, upstash); platformatic; eveland; and a browser World by pranaygp.

durable-harness also vendors a Cloudflare World at `apps/cloudflare/vendor/world-cloudflare`, version `0.0.0-pr4682`, which is private.

**v5 compatibility of community Worlds is UNKNOWN.** The v5 spec *requires* dense slot-numbered event IDs. The runtime refuses Worlds below spec 6. `@workflow-worlds/*` were last published 2026-02-09, and the docs say "We're working on bringing back World compatibility tests" (`docs/content/worlds/v5/upgrading-to-v5.mdx@W`). A SQLite-class World for v5 would therefore probably have to be written or ported by us, with `@workflow/world-testing` as the conformance suite.

### 2.13 Observability, tracing and streaming

- **OpenTelemetry:** the SDK depends only on `@opentelemetry/api` (an optional peer). Spans include `workflow.start`, `workflow.execute` (the consumer root), steps and backend HTTP calls, and trace context propagates across queue deliveries (`docs/content/docs/v5/observability/tracing.mdx@W`). Without an SDK registered, tracing is a no-op.
- **CLI and web UI:** `npx workflow inspect runs`, `--web`, and Cancel and "Rerun on latest" (`observability/index.mdx@W`). They work against any World.
- **Lifecycle hooks and attributes:** `observability/lifecycle-hooks.mdx` and `attributes.mdx`. Attributes are limited to 64 per run, with experimental storage.
- **Streams:** `getWritable()` gives named per-run streams (`world.streams.*`) that resume from an index (`get(runId, name, startIndex)` with negative tail indices). Streams can be passed across runs. The resumable AI chat transport is `@workflow/ai` `WorkflowChatTransport` (`foundations/streaming.mdx`, `ai/resumable-streams.mdx`). On Vercel: chunks up to 10 MB, 1,000 chunks/s per stream (D3).

### 2.14 Crash mid-step: what actually happens

| Crash point | Outcome | Citation |
|---|---|---|
| Before `step_started` is durable | Replay re-schedules the step, which runs once later. | runtime design (code-transform.mdx) |
| After `step_started`, during the body (eager/queued step) | The queue redelivers and the body **runs again**, with `attempt` incremented. You may see several `step_started` events; "no error will be visible". | `docs/content/docs/v5/errors/step-executed-multiple-times.mdx@W` |
| After `step_started`, during the body (inline step) | Only the owning message's redelivery re-executes the body before the 860 s lease ends. Other wakes defer. On Local, restart releases orphans immediately. | `changelog/step-message-ownership.mdx@W`; local.mdx |
| Body finished, `step_completed` write lost | The step **re-executes** (no outcome recorded). On Vercel, a rate-limited result write is retried for the life of the invocation, so the step does not rerun because of throttling alone (D3). | D3 "Rate limits"; errors-and-retries.mdx |
| Two concurrent replays | Duplicate inert events. The first committed event of a class wins. | event-sourcing.mdx |

The net result is **at-least-once execution of step bodies, plus exactly-once *recording* of a step's first terminal outcome.** The SDK never claims exactly-once side effects.

### 2.15 Explicit safe vs unsafe replay in the SDK

The Workflow SDK has **no per-step replay class**. Every step is presumed retryable (default 3 retries). The only levers are:
- `maxRetries = 0`, which still re-executes after a crash mid-body via redelivery or orphan release. On Local, an interrupted attempt counts toward retries, so a `maxRetries: 0` step fails instead.
- `FatalError`.
- Idempotency keys.

The `safe`/`never` classification exists **only in durable-harness** (§3).

### 2.16 Versioning and migration of in-flight workflows

- **Pinning:** runs are pinned to the deployment that started them (`foundations/versioning.mdx@W`). On Vercel this is a real deployment ID. On Local the deployment ID is synthetic (`dpl_local@<sdk-version>`), and the `deploymentAffinity` capability is deliberately unset (`interfaces.ts@W` L707-720).
- **Self-hosted implication:** there is **no code pinning**. Upgrading the app binary replays in-flight runs against *new* code. Any change to workflow-function control flow, or to step name, path or arguments, risks `REPLAY_DIVERGENCE` and then `CORRUPTED_EVENT_LOG`. This is an inference from the pinning model plus the replay rules; the vendor docs only describe Vercel pinning.
- **Migration options:**
  - Cancel and rerun on latest, or `start(..., {deploymentId: "latest"})`. This is Vercel-specific.
  - "Self upgrading workflows" via explicit continue-as-new recursion through `start()`, where serialized state is the migration boundary.
- **Spec and storage versioning:** each run carries `specVersion`. Postgres has 28 forward migrations. Local had a destructive layout change at 5.1.0 (§2.10).

### 2.17 Cancellation

- **Run cancellation:** a `run_cancelled` event, from pending or running (event-sourcing.mdx).
- **Step cancellation:** `AbortController`/`AbortSignal` are serializable across workflow and step boundaries. Cancellation is **cooperative**: a step that ignores the signal runs to completion. Abort errors become `FatalError` and skip retries (`foundations/cancellation.mdx@W`).

---

## 3. durable-harness analysis (@H)

### 3.1 Architecture

- **Published shape:** the `durable-harness` package (`packages/durable-harness`) bundles private workspace packages: `harness-world` (the kernel), `harness-pi`, `harness-claude-code`, `harness-codex`, `harness-opencode`, `harness-fx`, `harness-process`, `harness-sandbox`, `harness-hands` and `pi-world`.
- **Entry points:** `/pi`, `/pi-durable`, `/opencode`, `/claude-code`, `/codex`, `/fx`, `/sandbox`, `/next`, `/vercel`, `/tools` and `/instrumentation/otel` (`packages/durable-harness/package.json@H`).
- **No `@workflow/core`:** `harness-world` depends only on `@workflow/world`, plus `@vercel/agent-runs`, `devalue` and `ulid` (`packages/harness-world/package.json@H`). It is described as "Run agent harnesses directly on a Workflow SDK World: the session is a run, its transcript is the event log". **It does not use `"use workflow"`, `"use step"` or deterministic replay of JS.** It folds the event log into a `SessionState` (`fold.ts`), and harness adapters re-derive in-memory state from that fold.
- **Session model:** one session is one World run. Inbox submissions (`prompt | steer | followUp | withdraw | chaos`) are `hook_received` events on the session's inbox hook. Each model or tool call is a step, keyed by a harness-chosen **memo key**, and the first committed step per key wins (`types.ts@H` L20-35, L132-160).
- **Queue:** durable-harness uses its own queue prefix (`__{namespace}_wkf_workflow_`) and its own flow route `/.well-known/durable-harness/v1/flow`. A process that makes no agents must call `forwardQueue(world)` (D1).

### 3.2 The effect sandwich (how a harness turn is wrapped)

The implementation is `DriveContext.effect(key, opts, fn)` in `packages/harness-world/src/driver.ts@H` L2298 onward.

1. **Memo check.** If `key` already has a completed record, its output is returned. A failed record throws `EffectFailure`. This step is the replay.
2. **Ownership check** against the latest fold: `check()`. Preempted or handed-off drives stop writing.
3. **Running record handling.** A parked record yields. A settled record re-enters. An own orphaned intent is released and retried. Otherwise the drive yields with `contended`.
4. **Pipelining.** In *run-ahead* mode, a `safe` effect starts before its intent is durable. A **`never` effect is a barrier**: everything issued so far is durable before it starts.
5. **Lane routing.** If the effect `needs` a capability the current lane lacks (`browser < function < sandbox`), the drive commits a `handoff` fact instead and yields.
6. **Intent commit.** A new born-running `step_started` is written with `correlationId = step_<ulid>`. Its `eventData.input` is an envelope `{key, replay, input, epoch, drv, anchor, placed?, requires?, needs?, retryOf?, chain/seq?}`.
7. **First-writer check.** If another step won the key, this drive writes `step_failed{message:'superseded'}` and yields. If the step came back fenced (epoch moved), the drive stops. If foreign progress is seen, it releases its intent and yields.
8. **Body.** `fn(io)` runs with `io.progress()` streamed to `step:<id>`, `io.stepId`, `io.park()`, `io.docs` and `io.signal`.
9. **Outcome commit.** `step_completed` or `step_failed` is written. Document edits ride on the same `step_completed`.

### 3.3 Replay classes

From `types.ts@H` L10-19:
```ts
export type ReplayPolicy = 'safe' | 'never';
```
- `safe`: "run it again. Reads, idempotent writes, model calls."
- `never`: "do not rerun. The harness gets an *interrupted* result carrying whatever partial output reached the log, and decides what to do."

`resolveAbandoned()` (`driver.ts@H` ~L1520-1575) acts once an intent's driver is proven gone:
- `safe` → `step_retrying` `{interrupted:true}`, which releases the record for a new step with `retryOf`.
- `never` → `step_failed` `{message: "interrupted: ... it is not safe to rerun. It may or may not have taken effect.", interrupted: true, partial}`.

Model calls are `safe`, so a re-run model call may be billed again. B2 says a *finished* model call is never billed twice. Only interrupted ones re-run.

How each harness presents interrupted calls (D2):
- Pi re-runs `safe` tools.
- Claude Code, Codex and OpenCode tell the model a `safe` call is safe to repeat.
- For `never`, all of them tell the model it "may or may not have happened, so it can check before it tries again".

Defaults (D2):
- `durability: 'on'` (run-ahead) for `/pi`.
- `durability: 'strict'` for Claude Code, Codex and OpenCode.
- A `never` call always waits for its intent to be durable.

There is **no third class**. "unsafe" appears only in a doc comment (`types.ts@H` ~L293); no `'unsafe'` literal exists in the code. There is also no "compensate" or "reconcile" class.

### 3.4 How tool outcomes are recorded

- **Result:** the outcome is the `step_completed` payload, encoded with devalue. Large file content goes to hash-checked blobs (`blobs.ts`).
- **Partial progress:** `io.progress()` writes JSON lines to a per-step stream. On interruption, they are attached as `partial` to the failure.
- **Virtual workspace (`virtual()`):** a just-bash shell in a worker thread with an empty environment and no network. File changes commit with the tool's result, so an interrupted call "leaves nothing behind, and the call runs again". The workspace is limited to about 500 files (D2).
- **Sandbox:** files live on a Vercel Drive. An interrupted command "may have partly run, and the model is told" (D2).
- **Parked work:** detached sandbox commands use `park`, `settle` and `detach` fact steps. A `Settlement` is `{by: 'inline'|'push'|'check'|'backstop'|'tether', exitCode, files, ok, value|error}`, and first writer wins (`types.ts@H` L106-140).
- **Documents (`defineDoc`):** typed JSON per session, at most 64 KB, versioned with `migrate(value, fromVersion)`, with optimistic `updateDoc` on a revision. App code can read them through `agent.sessions.doc` (D2; `harness-world/src/docs.ts@H`, 930 lines).

### 3.5 Leases, fencing and ownership

- **Epoch:** "the session's fencing token: how many `handoff` steps were accepted". Steps written with a stale epoch are ignored by every reader (`types.ts@H` SessionState.epoch, `fenced`).
- **In-band World fence:** `SessionLog.arm` uses `inBandFence` (§2.9). A refused write throws `LogSuperseded`, and the drive stops. `DriveContext.fence()` exposes `{count, fenced}` for arming external machines such as the sandbox relay. If the fence is not `fenced`, mutating sandbox commands are not armed (`types.ts@H` L296-330; `in-band-fence.test.ts`, 965 lines).
- **Anchors:** a delivery is anchored to a queue message lease (Vercel), to the process (Node), to a tab, or to a sandbox daemon. "Liveness is the queue's alone" (`driver.ts@H` DriverOptions.anchors). `directDriveMs` defaults to 60 s and `maxInvocationMs` to 10 min.
- **Known gap:** live stream writes are **not** fenced. A stalled old drive can still interleave UI deltas after a takeover (`docs/followups.md@H` "Live writes after a takeover").

### 3.6 Built-in chaos and recovery drills

`chaos.ts@H` (`ChaosKind = 'process' | 'sandbox-vm' | 'sandbox-command' | 'drop-callback' | 'sandbox-new-vm' | 'sandbox-zombie' | 'relay-drop'`) injects crashes through a `chaos` inbox submission. Tests named `chaos.test.ts`, `drills.test.ts`, `runahead-blips.test.ts`, `drive-fence.test.ts`, `tab-lost` and `invariants.test.ts` exist. This is a directly reusable *test design pattern* for our suite (§7).

### 3.7 Maturity and coupling

| Signal | Value |
|---|---|
| Version | 0.0.1. The AGENTS.md policy stays on `0.0.x` (patch-only), and the README says "experimental". D1 says "`durable-harness` is in beta". |
| Age / commits | Repo created 2026-10-16. 25 commits, 4 contributors, 255 stars, 7 open issues. |
| Tests | 237 test files in the monorepo. 4 libfx-related tests are skipped (`docs/followups.md@H`). |
| Vercel coupling | **Claude Code and Codex "run only in the session's own Vercel Sandbox... on your own server too"** (D1, README). Model calls default to Vercel AI Gateway (`AI_GATEWAY_API_KEY` or OIDC). Pi accepts a custom pi-ai `Model`. Agent Runs tracing uses `@vercel/agent-runs`. A Next.js-centric discovery plugin is included. |
| Runtime | Node ≥22 (tracing needs Node 24). Bun, Deno and Electron are not mentioned, so **UNKNOWN**. |
| Known limitation | For `/pi` and OpenCode, a turn starts in the chat request and hands over to the queue after 60 s. A command running at handover "is stopped, not run again" (D2). |

---

## 4. Comparison note: T3 Code orchestration-v2 (@T, skim only)

`apps/server/src/orchestration-v2/EffectOutbox.ts@T` (724 lines) is a SQLite outbox on the Effect `SqlClient`. Its rows carry `status`, `attempt_count`, `lease_owner` and `lease_expires_at`. `reconcileAfterProcessLoss` (~L492-525) does two things:
- It **cancels** pending or running effects whose types are `PROCESS_BOUND`.
- It **re-queues** running effects whose types are in `REPLAY_SAFE_EFFECT_TYPES_AFTER_PROCESS_LOSS`.

`EventSink.ts` (1,019 lines) is the event-write side.

| Dimension | Workflow SDK | durable-harness | T3 orchestration-v2 |
|---|---|---|---|
| Unit of durability | step (compiler-delimited) | effect (adapter-delimited memo key) | outbox effect row (typed request union) |
| Replay classification | none (all retryable) | `safe` / `never` per tool | per effect *type*: replay-safe vs process-bound (cancel) |
| Liveness | queue message lease (860 s) | queue anchor + epoch + in-band fence | DB lease owner/expiry |
| Unknown outcome | re-executes (at-least-once) | `never` → interrupted, model told | process-bound → cancelled with error text |
| Storage | pluggable World | World | local SQLite |
| Local-first fit | weak (Local World is dev-only) | weak (Vercel Sandbox/Gateway-centric) | strong (desktop app server) |

The three designs converge on the same idea: **classify effects by replay safety at the type level and never silently re-execute unknown-outcome effects.** T3 does this without a remote dependency. Deeper analysis belongs to the T3 research agent.

---

## 5. "Never forget": four testable properties

Each property is defined so that it can be **falsified by a test**. "Provided" means the mechanism exists in the code at the pinned SHA. It does not mean the property holds end to end in our product.

### P1: Execution durability

**Definition:**
- For any process kill at any instruction boundary, after restart every effect with a committed outcome is returned from the log and **not re-executed**.
- Every run that was `pending` or `running` resumes without human action within T_resume.
- No committed event is lost after the store acknowledged it, on a crash-consistent store.

**Tests:** kill at each boundary (§7 R1). Count body executions per memo key. Diff log prefixes before and after.

### P2: Semantic and project memory

**Definition:**
- Facts, decisions and artifacts produced in session S are retrievable by a *later, different* session S' of the same project, by meaning or key.
- They survive process restart, schema upgrade and context-window compaction.
- They have provenance (which run or step produced them) and explicit retention.

**Tests:** cross-session recall after restart, compaction and upgrade. Provenance must resolve to an existing log event.

### P3: Scheduling and continuation

**Definition:**
- A run can durably wait (on time, an external signal or human approval) for an unbounded period.
- It resumes exactly once per wake condition after restarts.
- Recurring work fires with bounded skew. Missed fires during downtime are handled by a declared policy (catch-up, skip or coalesce).
- Long-lived work can roll onto new code at explicit boundaries (continue-as-new).

**Tests:** sleep across a kill. Resume on a hook after restart. Downtime spanning a scheduled fire. Duplicate wake.

### P4: Safe effect authority

**Definition.** Every side-effecting call:
- (a) carries a **stable idempotency key** derived from durable identity;
- (b) is classified by a **replay class** (at least `safe`, `never`/unknown-outcome, and ideally `reconcilable`);
- (c) runs only under a **lease and fencing token**, so a stale executor cannot commit or act;
- (d) on crash with intent-without-outcome, enters an explicit **unknown-outcome state** that is resolved by **reconciliation** (query the provider by key or receipt), never by blind retry;
- (e) **re-validates permissions and credentials** at resume time against current policy rather than trusting the authorization captured at intent time.

**No exactly-once claims are permitted.** The target is *at-least-once attempt + idempotent effect + exactly-once recorded outcome*.

**Tests:** §7 R2, R3, R4 and R5.

### 5.1 Provided / not provided matrix

| Property and sub-requirement | Workflow SDK 5.2.3 | durable-harness 0.0.1 | Evidence |
|---|---|---|---|
| **P1** committed outcomes not re-executed | **Provided** (memoized `step_completed`) | **Provided** (memo key, first committed wins) | §2.3, §3.2 |
| P1 auto-resume after crash | **Provided** on Vercel and Postgres. On Local, **only with `recoverActiveRuns` on `start()`**, single process | **Provided** (`recoverSessions`, `getWorld()` on start) | §2.10, D1 |
| P1 durable store crash-consistency | Depends on the World. **Local: no fsync, so not provided under power loss.** Postgres: DB-grade | Inherits the World | §2.10 |
| P1 in-flight body re-execution | **At-least-once** (re-executes) | `safe`: re-executes; `never`: not re-executed, surfaced as interrupted | §2.14, §3.3 |
| **P2** cross-session semantic memory | **Not provided** | **Not provided.** Only per-session `defineDoc` documents (≤64 KB, versioned) | D2 |
| P2 survives context compaction | n/a | UNKNOWN (harness-specific, e.g. Pi's own compaction) | not found in source |
| **P3** durable sleep / timers | **Provided** (`sleep`, no max) | Inherits World queue delays. Session idle waits on the inbox hook | §2.5 |
| P3 external signal / HITL | **Provided** (hooks, webhooks, token uniqueness, force-claim) | **Provided** (inbox hook: prompt/steer/followUp/withdraw). Approvals via libfx hooks (fx) | §2.5, §3.1 |
| P3 duplicate wake suppression | Partial: `hookResumeDedup` covers transport retries of one call; **not** duplicate external webhook deliveries; `wait_completed` at most once | Submission `nonce`; withdraw semantics. Full dedup of resends UNKNOWN | §2.5; `types.ts@H` Submission |
| P3 cron / recurring with catch-up policy | **Not provided** in the SDK (Vercel platform cron is separate). Sleep loops only | Not provided | §2.6 |
| P3 roll onto new code | Vercel: pinning plus `deploymentId:'latest'`. Self-host: **no pinning**; continue-as-new by user pattern | Run name embeds `durable-harness@<version>`; migration story UNKNOWN | §2.16 |
| **P4a** stable idempotency key | **Provided** (`stepId`, stable across retries) | **Provided** (`io.stepId` per intent; a retry of a released `safe` effect gets a **new** stepId with `retryOf`) | §2.8, §3.2 |
| P4b replay classes | **Not provided** | **Provided:** `safe` / `never` only (no `reconcilable`) | §3.3 |
| P4c lease / fencing | Inline-ownership lease (queue message, 860 s, max 900). In-band fence in the World spec but "runtime does not send the fence yet" | **Provided:** epoch + World in-band fence + `DriveFence` for external machines. Live stream not fenced | §2.6, §2.9, §3.5 |
| P4d reconciliation of possibly-executed effects | **Not provided** (user saga/compensation; idempotency key only) | **Partial:** surfaces "may or may not have taken effect" + partial output **to the model**. No programmatic reconcile hook | §2.7, §3.3 |
| P4e permission / credential revalidation on resume | **Not provided** | **Not provided** generically. Claude Code/Codex sandboxes hold no credentials (the function makes model calls); chat-route `authorize` is per request. Resume-time policy recheck UNKNOWN | B2, README |
| Exactly-once claims | None. Docs repeatedly require idempotency | None. Blog avoids "exactly-once" (B2) | §2.14, B2 |

---

## 6. Local, offline, runtime, lock-in and cost

### 6.1 Can it run fully local without Vercel?

| Component | Fully local? | Caveats |
|---|---|---|
| `workflow` core + Local World | **Yes for dev.** No network is needed for storage or queue. | Dev-only per vendor. In-memory queue. No fsync. Single instance. Destructive layout upgrade at 5.1.0. Queue delivers by **HTTP to the app's own base URL** unless `registerHandler` is used. |
| `workflow` + Postgres World | **Yes**, with a local Postgres | A reference implementation: no auth on the flow route, no encryption. Needs a long-lived process (graphile-worker). |
| `workflow` + community SQLite/Turso World | **UNKNOWN** for v5 | Probably needs porting to slot IDs. Conformance via `@workflow/world-testing`. |
| `workflow` + Vercel World | No | Needs `VERCEL_DEPLOYMENT_ID` and OIDC |
| durable-harness `/pi` (custom pi-ai Model, `virtual()`) | **Plausibly yes** on Local or Postgres | Default models go through AI Gateway. A custom `Model` is documented for Pi (`pi.ts@H` L17-25). Fully offline end-to-end operation is UNKNOWN and was not run. |
| durable-harness Claude Code / Codex | **No** | "run only in a Vercel Sandbox... on your own server too" (D1). Needs a Vercel token, team and project. |
| durable-harness OpenCode | Partial | `virtual()` is local. `sandbox()` needs Vercel. |
| Observability | Local CLI and web UI work on any World. Agent Runs (`@vercel/agent-runs`) is Vercel. OTel is generic. | |

### 6.2 Runtime support

| Runtime | Workflow SDK | durable-harness |
|---|---|---|
| Node.js | Yes. Repo dev engine `node ^24`. Published packages declare no `engines` (`packages/*/package.json@W`). | `>=22`; tracing needs 24 |
| Bun | **Documented integration example** (`how-it-works/framework-integrations.mdx@W` uses `Bun.serve`, a Bun plugin and `workflow build`). Code-transform docs say steps have "Node.js/Deno/Bun access". CI coverage UNKNOWN. | UNKNOWN |
| Deno | Mentioned only in passing. UNKNOWN. | UNKNOWN |
| Cloudflare Workers | QuickJS engine exists "usable on platforms that do not implement `node:vm` (e.g. Cloudflare Workers)" (`vm-mode.ts@W`). Community CF World. | `apps/cloudflare` example with a vendored CF World (private) |
| **Electron main process** | **UNKNOWN.** No mention anywhere (grep). Requirements: `node:vm`, `node:crypto`, undici; a bundler step with the SWC plugin; a queue callback over HTTP to a local base URL or in-process `registerHandler`; a long-lived process for Postgres; a writable data directory. Electron main *is* Node, so this is plausible but untested by the vendor. | UNKNOWN. Next/Vercel-function oriented; `flowHandler()` takes a Fetch `Request`, so it could be mounted in any server. |
| Windows | world-local wraps rename and unlink in `withWindowsRetry`, which suggests Windows was considered. Test coverage UNKNOWN. | UNKNOWN |

### 6.3 Vendor lock-in

- **Low at the license level.** Everything is Apache-2.0: Workflow SDK, durable-harness, `@workflow/world`, world-local and world-postgres.
- **Moderate at the architecture level:**
  1. Code identity and IDs come from **file path plus function name**, produced by a **proprietary-shaped compiler transform**. Leaving means rewriting workflows and steps.
  2. Several features are Vercel-only:
     - deployment pinning (`deploymentAffinity`, `deploymentId:'latest'`);
     - encryption (`getEncryptionKeyForRun`);
     - regions;
     - the `invoke` capability;
     - managed queue backoff semantics (VQS).
  3. **The production self-host story is "clone and adapt the reference Postgres World".**
- **High for durable-harness.** Its Claude Code and Codex adapters require Vercel Sandbox and Drive. The model path defaults to AI Gateway. Observability uses Vercel Agent Runs. The Next.js discovery plugin assumes Vercel deployment shapes.

### 6.4 Cost

| Option | Cost model |
|---|---|
| Self-hosted (Local or Postgres) | $0 license. You pay compute, Postgres and ops yourself. Event-log growth is your storage cost: each step is about 3 events, and a virtual workspace writes an event per file change. |
| Vercel Workflow (D3, page `last_updated` 2026-09-16) | **Events $0.02 per 1K** (Hobby: 50K/month included). **Data Written $0.50/GB** (Hobby: 1 GB). **Data Retained $0.50/GB-month** (not on Hobby). Plus Functions compute and Vercel Queues at standard rates. Limits: 25k events/run and 10k steps/run on node:vm (QuickJS with snapshots exempt), 50 MB payload, 2 GB entity storage per run, 240 s replay, 200 event creations/run/s. API rate limits: Hobby 50k, Pro 500k, Enterprise 2.5M requests/min. |
| durable-harness on Vercel | Workflow costs plus Vercel Sandbox and Drive usage plus AI Gateway token pricing. Sandbox and Drive pricing were not fetched (**UNKNOWN**). |

A worked example, illustrative only: an agent turn with 30 tool and model effects makes roughly 90-100 events, about $0.002 per turn in event fees on Vercel. The real cost is dominated by model tokens and compute.

---

## 7. Recovery test suite outline

**Scope:** this suite is product-agnostic. It applies to whichever durability layer we build or adopt. It borrows the durable-harness chaos-submission idea: the crash point is injected *through the log*, so it is replayable and deterministic.

**Harness requirements:**
- A fault-injection hook at every effect boundary.
- A fake provider that records every request with its idempotency key and can delay, drop, duplicate or fail responses.
- An external "ledger" of real side effects, used as ground truth.
- A log inspector that can assert prefix and fold invariants.

**Global invariants, checked after every test:**
- **I1:** the log is a dense prefix (no holes, monotonic slots).
- **I2:** each memo key has at most one committed terminal outcome.
- **I3:** ground-truth side effects for a `never` effect are ≤1 per idempotency key, unless reconciliation proved absence and the effect was retried.
- **I4:** no write is accepted from a fenced (stale) executor.
- **I5:** every run is either terminal or resumable (no wedged run) within T_resume.
- **I6:** no secret appears in the log, streams or traces.

### R1: Process kill at each step boundary

| ID | Kill point | Expected | Metric |
|---|---|---|---|
| R1.1 | Before intent write | Effect runs once after restart | body executions = 1 |
| R1.2 | After intent durable, before body | `safe`: runs once. `never`: surfaced as interrupted (no execution), or reconciled | `never` executions = 0 or 1 per ground truth; model or user informed |
| R1.3 | Mid-body (after a partial external write) | `safe`: re-run converges (idempotent). `never`: unknown-outcome state, then reconciliation | duplicate external effects = 0 for keyed APIs |
| R1.4 | After body, before outcome write | Same as R1.3. Partial progress is preserved | partial chunks recovered = 100% |
| R1.5 | After outcome write, before ack/next | No re-execution. Next effect proceeds | re-executions = 0 |
| R1.6 | During a multi-event batch write | Atomic per attempt. Either all events land or none | torn batches = 0 |
| R1.7 | During a handoff or lease transfer | Exactly one owner. The old owner's later writes are refused | stale accepted writes = 0 |

**Sweep:** for every effect in a scripted 50-effect turn, kill at each of the 5 points, giving 250 runs. **Pass:** I1-I6 hold in 100% of runs. **SLO:** p95 resume latency below 10 s on local single-process. Workflow's default 860 s inline lease would fail this unless orphans are released on restart, so measure it.

### R2: Duplicate webhooks and wakes

- Deliver the same external webhook (the same provider event ID) 2-10 times, concurrently and spaced. **Expected:** one logical resume. Workflow dedups only per-call transport retries, so app-level dedup on the provider ID is required.
- Resume a hook during a run's sleep and then again after. Fire a wait-completion twice.
- **Metric:** logical resumes per provider event = 1. Duplicate `hook_received` events are either rejected or inert.

### R3: Missing receipts

- The provider performs the action, but the response is lost (connection reset after commit).
- **Expected:** the effect enters `unknown_outcome`. Reconciliation queries by idempotency key or receipt and finds `applied`, then the outcome is committed without a retry.
- **Metric:** reconciliation success rate ≥99% for providers with a lookup API. For providers without one, 100% of cases escalate to the user. Blind retries = 0.

### R4: Unknown-outcome side effects

| Case | Expected |
|---|---|
| `never` tool interrupted, provider has idempotency keys | Retry with the **same** key is allowed (the provider dedups). Record this as `reconciled-by-key`. |
| `never` tool interrupted, provider has no keys or lookup | Do not retry. Surface "may or may not have happened" to the model and user, matching durable-harness. Require explicit confirmation. |
| `safe` tool whose classification was wrong (actually mutating) | Detected by the ledger diff. The test fails, and the classification is flagged. |

**Metrics:** unknown-outcome effects resolved = 100% (reconciled or escalated). Silent duplicates = 0.

### R5: Lost credentials and permission changes

- Revoke or rotate a provider token between intent and resume. Downgrade the user's permission between intent and resume.
- **Expected:** resume re-validates. Effects needing the revoked scope go to `blocked_on_auth`, not failed-and-forgotten and not executed with stale authority. No credential is persisted in the log.
- **Metrics:** stale-authority executions = 0. Secret-scan hits in log, streams and traces = 0.

### R6: Corrupted local state

- Truncate the last event file or WAL page. Zero-fill a middle event. Delete a lock or claim file. Leave a stray `*.tmp.*`. Use a mixed-layout data directory (world-local raises `DataDirLayoutError`). Simulate power loss (no fsync) with a filesystem fault injector.
- **Expected:**
  - Detection at startup through checksums and density checks.
  - Quarantine of the affected run with a diagnostic.
  - No silent truncation that looks like a valid shorter log. This is the sealed-log lesson in `spec-version.ts@W`.
  - Unaffected runs proceed.
- **Metrics:** corruption detected = 100%. Silent divergence = 0. Blast radius limited to the affected runs.

### R7: Schema and code upgrades

- Upgrade the storage schema (N→N+1 migrations) with runs in flight. Downgrade attempt. A world-local style layout change, where the vendor's behavior is to **delete** the data directory and our requirement is to refuse or migrate, never delete.
- Change workflow code under an in-flight run: rename a step file, add a step in the middle, reorder `Promise.all`.
- **Expected:** a migration is forward-only with a backup, or it refuses to start. Code changes either replay correctly, divergence is detected and the run is parked for continue-as-new, or a version pin is honored.
- **Metrics:** data loss on upgrade = 0. Divergence detected before any side effect = 100%.

### R8: Provider exhaustion

- 429s with `retry-after`, 5xx storms, quota exhaustion, and model provider down for 1 min, 1 h and 12 h.
- **Expected:**
  - Backoff honors `retry-after`.
  - The delivery budget is explicit. Workflow's 48 deliveries, about 10 h on Vercel, then fail the run. We need a declared policy: park, not fail.
  - Model calls are `safe` but cost-bearing. Re-billing is bounded and measured.
- **Metrics:** runs failed by transient exhaustion = 0 (parked instead). Duplicate paid model calls per crash ≤1. Time-to-resume after provider recovery below 2× backoff.

### R9: Context overflow

- Conversation or log grows past the model context. The event log reaches max events (25k default). Snapshot or compaction is needed.
- **Expected:** compaction is a recorded, deterministic effect, either memoized or reproducible. A resumed turn after compaction sees the same compacted context. P2 memory survives compaction.
- **Metrics:** post-compaction recall of pinned facts = 100%. `MAX_EVENTS_EXCEEDED` failures = 0 (rollover via continue-as-new).

### R10: Network loss

- Loss between executor and store, at mid-write and with a write acked but the response lost. This is the documented "connection failure does not prove that the backend rejected a write".
- Loss between executor and provider. Partition of two executors sharing a store.
- **Expected:** writes are idempotent or bump-and-report. Executor writes under a partition are fenced, and only one makes progress.
- **Metrics:** duplicate events with semantic effect = 0. Dual-owner progress = 0. Recovery within T_resume after heal.

### R11: Cancellation

- Cancel a run during: sleep; a `safe` effect; a `never` effect; a parked or sandbox command; a pending hook. Cancel twice. Cancel concurrently with completion.
- **Expected:**
  - Cancellation is durable (`run_cancelled`).
  - Cooperative steps stop. Non-cooperative ones run to completion, but their outcome is not acted upon. Workflow's abort is cooperative.
  - In-flight `never` effects are reconciled, not abandoned.
  - Hooks are released.
  - There is no zombie live-stream output after cancel. durable-harness has an open gap here: live writes are not fenced.
- **Metrics:** post-cancel external side effects started = 0. Post-cancel stream writes accepted = 0. Hook tokens released = 100%.

### Suite-level success metrics

| Metric | Target |
|---|---|
| Invariant violations (I1-I6) across all scenarios | 0 |
| Crash-point coverage (effect boundaries × kill points) | 100% of enumerated points |
| p95 time-to-resume, single local process | < 10 s |
| `never`-class duplicate external effects | 0 |
| Unknown-outcome effects left unresolved after 24 h | 0 |
| Data loss on schema upgrade | 0 |
| Determinism: the same fault seed gives the same log | 100% reproducible |

---

## 8. Recommendations (per need)

| Need | Workflow SDK | durable-harness | Rationale |
|---|---|---|---|
| P1 execution durability engine for a local-first app | **Pattern-only** (conditional adopt) | **Reject** as a dependency | WDK is solid and well-tested (469 test files, a conformance suite), but its only first-party local backend is dev-only. Adopting it means writing and maintaining a v5 SQLite World plus compiler integration, and Electron is UNKNOWN. Revisit adoption if we accept Node-server shape plus Postgres, or if a maintained v5 SQLite World appears. |
| World/storage contract design (dense slots, bump-and-report, fail-closed capabilities, in-band fence) | **Adopt (pattern)** | n/a | `interfaces.ts@W` is the best-specified artifact in either repo. Mirror its invariants in our own event store. |
| Effect sandwich (intent → body → outcome) with memo keys | n/a | **Adopt (pattern)** | `driver.ts@H` `effect()` is the closest match to agent tool calls. It needs no JS replay sandbox. |
| Replay classes | Gap | **Adopt and extend** | Take `safe`/`never`. Add `reconcilable` with a provider lookup hook and an explicit `unknown_outcome` state (P4d), which neither repo has. |
| Fencing / leases | Pattern (queue-message lease) | **Adopt (pattern)** | Use an epoch plus a store-enforced in-band counter. Also fence live streams, which durable-harness leaves open. |
| P2 semantic/project memory | Reject (absent) | Pattern-only (`defineDoc` typed, versioned, ≤64 KB) | Neither provides cross-session memory. Use the typed, versioned doc with migrate as a sub-pattern only. |
| P3 scheduling/continuation | **Pattern-only** | Reject | Durable sleep plus hook race plus continue-as-new are good patterns. Cron with a catch-up policy must be ours. |
| P4 safe effect authority | Pattern (stepId keys, saga) | Pattern (interrupted surfacing, credential-less sandbox) | Permission revalidation and reconciliation are unaddressed by both. We must build them. Never claim exactly-once. |
| Chaos/recovery testing | Pattern (`world-testing` conformance) | **Adopt (pattern)** | Chaos-as-log-submission and drills are directly reusable test designs. |
| Claude Code / Codex durable wrappers | n/a | **Reject** | Hard dependency on Vercel Sandbox. 0.0.x. 25 commits. |
| Observability | Pattern (OTel span model, propagation across queue) | Reject (Agent Runs is Vercel) | Use OTel API only. |

**Overall verdict:** **pattern-only** for both, with one conditional. Adopt `workflow` itself only if the target architecture becomes a Node server on Postgres. In that case still harden or own the World, because the reference Postgres World has no auth and no encryption. **Reject** durable-harness as a runtime dependency. Reassess when it leaves 0.0.x and if a non-Vercel sandbox path appears.

---

## 9. UNKNOWNs and open questions

1. Electron main-process compatibility of `@workflow/core`, the SWC transform and world-local. Nothing has been tested or documented.
2. Bun and Deno CI coverage for Workflow. The only evidence is a docs example.
3. v5 compatibility of the community Worlds (Turso, SQLite, Redis, Mongo).
4. Durability of Graphile `idempotencyKey` (job key) semantics across a DB failover in world-postgres.
5. Whether durable-harness `/pi` runs fully offline with a local pi-ai Model, on Local World, with no Vercel calls (OIDC or Agent Runs side effects).
6. Context-compaction behavior in durable-harness adapters, and whether compaction is a memoized effect.
7. Vercel Sandbox and Drive pricing, which was not fetched.
8. Permission or credential revalidation on resume in any harness adapter. No code was found.
9. Whether Workflow's runtime will start sending the in-band fence. The source comment says "not yet".

---

## 10. Source index (all accessed 2026-10-27)

**workflow @ `af8c6d3295ebc9aa7c0168cd0ca5007f62e6b9ba`:**
- `packages/world/src/interfaces.ts`, `queue.ts`, `events.ts`, `steps.ts`, `spec-version.ts`
- `packages/world-local/src/{fs.ts,queue.ts,index.ts}`
- `packages/world-postgres/{README.md,HOW_IT_WORKS.md,package.json,src/drizzle/schema.ts}`
- `packages/core/src/vm/index.ts`, `runtime/vm-mode.ts`, `runtime/constants.ts`, `runtime/step-executor.ts`, `runtime/resume-hook.ts`
- `worlds-manifest.json`
- `docs/content/docs/v5/{foundations/*,how-it-works/*,errors/*,configuration/worlds.mdx,deploying.mdx,changelog/step-message-ownership.mdx,observability/*,cookbook/common-patterns/scheduling.mdx}`
- `docs/content/worlds/v5/{local.mdx,upgrading-to-v5.mdx}`

**durable-harness @ `ea8aa4060cf4fb8cd39737ce8ab21c4e0f40c741`:**
- `packages/harness-world/src/{types.ts,driver.ts,session-log.ts,chaos.ts}`, `packages/harness-world/package.json`
- `packages/durable-harness/{README.md,package.json,CHANGELOG.md,src/world.ts,src/pi.ts}`
- `docs/followups.md`, `AGENTS.md`

**t3code @ `36d4d711b79c73eb33131944f73ea4a8c6156484`:** `apps/server/src/orchestration-v2/EffectOutbox.ts`

**Web:** B1, B2, D1, D2 and D3 as listed in §0.4. GitHub REST API (`repos/*`, commits and contributors pagination). npm registry (`registry.npmjs.org/<pkg>`).
