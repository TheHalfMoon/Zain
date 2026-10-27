# 16 — Zain First-Class Product Components

```text
STATUS = PROPOSED (planning only). Founder amendment 2026-10-27/28: Code Review, Engineering System (PStack + E2E),
         Plan Mode (AI Hero / mattpocock skills), Zain Browser, DeskGate are first-class, user-facing parts of Zain.
RESEARCH = research/R14 (Code Review), R15 (PStack/E2E), R16 (Plan Mode), R17 (Browser), R18 (DeskGate)
TASKS = 14_TASK_CATALOG.md K-*, E-*, L-*, Y-*, H-* · REQS = PR-26..PR-30, SEC-18..SEC-21
RIGHTS = public licenses verified per row (06 §1b) + FOUNDER-ATTESTED recorded but with no effect on third-party licenses, notices or trademarks;
         proprietary / unavailable components are marked EXCLUDED — attested permission cannot apply to code that is not available
NO_DUPLICATES_RULE = one review engine, one engineering loop, one planning mode, one browser controller, one PTY/process
                     host, one policy decision point (Core). Every component below is a client of those, never a second one.
```

## 1. Ownership map (no overlapping authorities)

| Concern | Single owner | Components that use it (never re-implement it) |
|---|---|---|
| Policy decisions, grants, receipts | Zain Trusted Core (Nawat + Ledger) | all five |
| Process / PTY execution | one Zain Server ProcessHost service (T3 node-pty for PTYs; ported Orca process-host logic inside it; static import guard forbids child_process elsewhere) | DeskGate, Code Review engine runner, E2E runner, LSP/DAP |
| Browser control | Zain Browser `BrowserController` (Server) | Engineering E2E (`zain-browser-verify`), Design Mode capture, DeskGate (none), agents via MCP |
| Review findings store and schema | Zain Code Review (`packages/review-engine`) | Engineering review lanes (E-05), Plan Mode critic (L-09), Trusted Completion |
| Planning artifacts (spec, ADR, task DAG) | Zain Plan Mode (repo files under `specs/<NNN>-<slug>/`, Brain index) | Engineering System reads only (L-07 contract) |
| Execution and verification loop | Zain Engineering System | Missions (P4) carry it; Code Review evaluates it |
| Orchestration (threads, runs, effects) | T3 orchestration-v2 in Zain Server | all; no component ships its own orchestrator |

## 2. Zain Code Review (R14)

- **Engine:** fork of `alibaba/open-code-review@375f64cd` (v1.13.3, Apache-2.0, actively maintained, Go) built as
  `native/zain-review-engine` — read-only review tools only; keeps OCR's changed-file selection, rules, grouping,
  parallel reviewers, full-file scan, line relocation, false-positive filter, manifest and SARIF.
- **Zain owns:** route choice (reviewer ≠ builder), Core proposals, findings store, dispositions (accept / dismiss /
  false positive with memory), fix proposals (preimage check → checkpoint → Core-granted write → verification → undo),
  IDE panel, CI.
- **Modes:** engine mode (OCR calls Zain's chosen model) and delegated mode (any provider session on another route
  reports findings through a Zain MCP tool) — one finding schema.
- **Continue (`continuedev/continue@5522c6f4`, Apache-2.0, README states read-only/unmaintained; hub retired):
  REFERENCE ONLY** — ideas reused (markdown checks, fixes in throwaway worktree); `.continue/rules|checks` importer.
- **Rejected:** PR-Agent as a second reviewer (06 D22 → reference), OCR viewer/IDE extensions (trusted-markdown
  injection; line-range fixes without preimage check), auto-fix by the reviewing agent, unpinned global installs.
- **Egress disclosure:** in P5 the engine calls the model endpoint directly (UNMEDIATED egress until the K-09 proxy in P6);
  local routes are the default and each cloud review route needs explicit approval.
- **Local/free:** Ollama / LM Studio via OpenAI-compatible endpoints or user keys; tool-calling probe before first run
  (a run with zero tool calls is FAILED, never "clean").
- **Earliest:** optional advisory spike late P2 (K-01); product in P5 (K-02..K-08); CI/scan in P6 (K-09).

## 3. Zain Engineering System (R15)

- **Source:** `cursor/plugins@ab1f702c` `pstack/` (MIT, © 2026 Lauren Tan) + `cursor-team-kit` verification skills (MIT,
  © Cursor). Names/logos not licensed → full rename; persona text excluded.
- **Loop:** investigate → plan (hand-off from Plan Mode) → implement → test → review → verify → ship, commands
  `/engineer`, `/test`, `/verify`, `/ship`; skills in `packages/skills/zain-engineering/`.
- **Completion rules ES-1..ES-7** extend Trusted Completion: VERIFIED verdict from an independent route bound to the exact
  tree; INCONCLUSIVE never passes; verdicts go stale on patch change.
- **E2E:** engine = **Playwright** (registry SRC-0255). **Source repository UNRESOLVED:** provisional candidate
  `TheHalfMoon/Ascout@ecada2bc` Spec 016 (Playwright executor + evidence model); founder must confirm (FO-9). Runs only in
  Zain Browser Test lane / isolated partition against allow-listed local dev origins; evidence hashed into Core.
- **Earliest:** P5 (E-01..E-05, E-07); shipping automation P6 (E-06).

## 4. Zain Plan Mode (R16)

- **Source:** `mattpocock/skills@59db609e` (MIT, 38 skills; Zain inventory re-pinned from `c55ee460`); aihero.dev/skills
  is a free catalog pointing to the same repo (no course content used). Adapt: grilling, grill-with-docs,
  domain-modeling (+ADR format), to-spec, to-tickets, wayfinder, to-questionnaire, wait-what, research,
  improve-codebase-architecture, handoff, design-it-twice; execution skills excluded (owned by Engineering System);
  `pr` excluded (contains third-party humanlayer text).
- **Mode:** T3 `interactionMode`/`proposed_plan` + Core `PLAN_READONLY` grant: writes allowed only under the plan path;
  shell, git, write-capable MCP and CLI agents blocked; turn-end diff invalidates on violation; "Approve plan → start
  mission" with WebAuthn creates a hash-locked `plan.lock.json`; critic route ≠ griller route.
- **Earliest:** usable (unenforced, labelled) at P2 (L-01); enforced P3 (L-02/03); durable artifacts P4; full UI and
  skills P5.

## 5. Zain Browser (R17)

- **One controller:** `BrowserController` in Zain Server evolved from T3 `PreviewAutomationBroker`; MCP, CLI, UI, and a
  future Claude `browser_toolset` adapter are thin front-ends. Orca browser code, browser-harness
  (`browser-use/browser-harness@4ced8e00`, MIT — attaches to the user's whole Chrome and `exec()`s agent Python) and Browser
  Use are REFERENCE only.
- **Lanes:** Preview (user-visible), Agent (isolated, ephemeral profile), Test (headless Playwright, loopback endpoint),
  User-session (opt-in, later, MV3 extension scoped to a Chrome tab group; ported from Playwright's extension).
- **Gaps found in donors:** T3 has **no pre-request navigation/redirect gate** (largest new piece, Y-03); T3 and Orca
  **import cookies from the user's real browsers** → removed in P2 (Y-00).
- **Effects:** every action is a Core effect with replay class and receipt (screenshot / accessibility snapshot / HAR
  hashes); hard blocks (payments, agent credential entry, account creation, executable downloads, permanent deletion,
  trades, following page instructions) cannot be overridden by Skip; sign-in by human takeover.
- **Earliest:** hardening P2; effect classes P3; localhost + allow-listed agent + Test lane P5; general web +
  user-session P9.

## 6. DeskGate (R18)

- **Source:** `wonderwhy-er/DesktopCommanderMCP@db3430f2` (v0.3.1, MIT). `desktop-commander/remote-desktop-commander`
  (`a6573e86`) is **all rights reserved and contains only docs/manifests**; the hosted relay/OAuth/dashboard are not
  public → **EXCLUDED** (no code exists to apply attested permission to). DC's own remote device agent (MIT) is a client
  of that relay → excluded. `vendor/telemetry-contract` (no license) excluded.
- **Design:** DeskGate = thin adapters on Zain Server `/mcp`, keeping familiar DC tool names; every call becomes a Core
  effect (`fs.*`, `process.spawn`, `terminal.input`, `process.signal`, `remote.session`); execution only by the single Server
  process/PTY host; no own config, blocklist or spawn code (static-import guard); `set_config_value` refused; signals limited
  to Zain-owned process trees; no network; remote only via Zain runner + project-home + passkey.
- **Known DC weaknesses not inherited:** blocklist first-word bypass, self-rewriting config, unrestricted default
  directories, plaintext argument logs, default telemetry.
- **Earliest:** core P3 (with seams S6/S8); search + cross-OS P6; remote P10.

## 7. Earliest practical version vs later (component view)

| Component | P2 (Workbench) | P3 (Trusted) | P4 | P5 (v1) | P6+ |
|---|---|---|---|---|---|
| Code Review | advisory spike | — | — | engine, panel, fixes, delegated | CI, scan |
| Engineering System | — | — | — | loop, E2E (if FO-9), completion rules | shipping |
| Plan Mode | unenforced | enforced read-only | artifacts + approval | skills + UI | — |
| Browser | cookie import removed, isolation | effect classes, hard blocks | — | agent/test lanes (localhost/allow-list) | general web, user-session (P9) |
| DeskGate | — | local tools | — | — | search, parity (P6); remote (P10) |
