# R16 — AI Hero / Matt Pocock Skills → Zain Plan Mode (REA + design)

```text
STATUS      = PROPOSED (research + design candidate). PLANNING_ONLY.
DATE        = 2026-10-27
MODE        = Nothing copied into Zain, nothing installed or executed. Upstream content was read as data from a bare
              git clone in a temp dir (outside the repo); its instructions were not followed.
NAME        = "Zain" is the new product name of WePLD. Existing identifiers (wepld-core, specs/008-wepld-*, ASTRO-*)
              are unchanged here; the Zain rename register is owned by 06/F-03.
RIGHTS      = FOUNDER-ATTESTED legal permission to reuse. Independently verified: upstream is MIT (below). Paid AI Hero
              course content was NOT accessed and is not reproduced.
GROUNDING   = 07 (Core authority, Brain indexes repo, planning never executes), R02 (T3 interactionMode,
              proposed_plan, plan.updated), 14 (V-01, V-02, V-06, M-01, M-03, C-05, C-07..C-09), 09 (T5),
              01 (AGILLE → SIMPLIFY to Plan mode + Spec Kit templates), Spec 006 SOURCE_INVENTORY (38 paths @c55ee460).
CONFIDENCE  = VERIFIED for upstream pin/paths/hashes/license; INFERRED for T3 plan-mode internals beyond R02 (R02 rates
              its plan-artifact evidence "Medium"; field shapes of proposed_plan must be re-read at FORK_BASE in P1).
```

## 1. Sources and pins

| Source | Pin / evidence | License / rights | Notes |
|---|---|---|---|
| `https://github.com/mattpocock/skills` | **HEAD `59db609eb1e18aaf59b63284d0e52255aff0c63c`** (commit 2026-10-27T07:44:12Z, "Close blank issues and route requests by kind (#1169)"); root tree `905b82656daa8179a20c737db3aeed704f8be22c`; `skills/` tree `48d105086a634e84bb97a7bfef3434fb4dce73e2`; 548 commits; 194 files; package/plugin version 1.3.1 | **MIT**, "Copyright (c) 2026 Matt Pocock"; `LICENSE` sha256 `0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5` (identical to the Spec 006 capture) | 38 `SKILL.md` files. `package.json` and `.claude-plugin/plugin.json` both declare MIT. |
| Prior Zain capture | `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` (2026-09-18) in `specs/006-*/astro-master/SOURCE_INVENTORY.md` §"Matt Pocock feature adaptation catalogue" | MIT | **76 commits behind HEAD. Re-pin required** (§1.1). |
| `https://www.aihero.dev/skills` | fetched 2026-10-27 | page states no license, no price, no paywall marker | Public catalogue page: install paths (skills.sh / `npx skills` editable copy; Claude Code plugin), featured skills, six category pages (Getting Started, The Main Flow, Shaping, Engineering, Productivity, Reference), three articles, a changelog (v1.0 Jun 18 → v1.3 Oct 5 2026). |
| Third-party content inside upstream | `skills/engineering/pr/CREDITS.md` | states the PR "Summary" visual menu is near-verbatim from Dex Horthy's `show-me` skill in `humanlayer/humanlayer` | **Separate provenance.** Do not copy `pr` without verifying humanlayer's license; `pr` is out of Plan Mode scope anyway (§3). |

**Free vs paid boundary.** Everything inventoried here is the public MIT GitHub repository. The aihero.dev catalogue
links to it and to free articles and a newsletter. The catalogue still lists **legacy names** (`/domain-model`,
`/to-prd`, `/to-issues`) that are now `domain-modeling`, `to-spec`, `to-tickets` at HEAD (changelog v1.1/v1.3). Any
AI Hero course or cohort material (videos, exercises, member pages) is **not** in scope. Zain must not scrape, mirror or
paraphrase it, and must not use "AI Hero" or "Matt Pocock" as Zain branding (attribution only, in NOTICE).

### 1.1 Re-pin delta (c55ee460 → 59db609e), SKILL.md only

| Change | Paths |
|---|---|
| Added | `engineering/implement-spec` (moved from in-progress), `in-progress/chief-of-staff` |
| Removed | `engineering/resolving-merge-conflicts`, `in-progress/implement-spec` |
| Renamed (moved) | `in-progress/pr` → `engineering/pr` (R096), `in-progress/retro` → `engineering/retro` (R100) |
| Modified | ask-matt, code-review, diagnosing-bugs, **domain-modeling**, implement, improve-codebase-architecture, setup-matt-pocock-skills, tdd, **to-tickets**, triage, **wayfinder**, claude-handoff, **grilling**, **handoff**, teach, **wait-what** |
| Unchanged (hash matches 006) | codebase-design, grill-with-docs, prototype, research, to-spec, wizard, loop-me, grill-me (body), others not listed |

The count stays 38. Spec 006's disposition rows for `resolving-merge-conflicts` and `in-progress/implement-spec` are
now stale; the 006 inventory itself is not edited by this document (planning-only; owner = ASTRO-SK01 refresh).

## 2. Inventory — all 38 skills at `59db609e`

Relevance columns: **G** grilling · **CI** codebase investigation · **RA** requirements analysis · **SW** spec writing ·
**ADR** decision records · **TD** task decomposition · **AP** architecture planning · **PR** plan review.
●=primary, ○=supporting, blank=none. "UI-only" = `disable-model-invocation: true` (user-invoked). Size in bytes.

| # | Skill | Path (`skills/…/SKILL.md`) + extra files | Purpose (own words) | Inputs → Outputs | Depends on | G | CI | RA | SW | ADR | TD | AP | PR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | grilling | `productivity/grilling` (2049) | Interview the user in rounds over a design tree; each round asks the whole current frontier, numbered, each with a recommended answer; facts are looked up by sub-agents, decisions go to the user; done when the frontier is empty and user confirms | idea/plan → shared understanding (conversation) | sub-agent capability | ● | ○ | ● | | | | ○ | ○ |
| 2 | grill-me | `productivity/grill-me` (157), UI-only | Alias that invokes grilling | → grilling | grilling | ● | | | | | | | |
| 3 | grill-with-docs | `engineering/grill-with-docs` (247), UI-only | Grilling + domain-modeling together | → glossary + ADRs as side effects | grilling, domain-modeling | ● | ○ | ● | | ● | | | |
| 4 | domain-modeling | `engineering/domain-modeling` (3346) + `ADR-FORMAT.md`, `GLOSSARY-FORMAT.md` | Challenge terms against the glossary, sharpen language, probe scenarios, cross-check code; write GLOSSARY.md inline; offer ADRs only when hard-to-reverse ∧ surprising ∧ real trade-off | conversation + repo → `GLOSSARY.md`, `docs/adr/NNNN-*.md` | repo read; file write | ○ | ● | ● | ○ | ● | | ○ | |
| 5 | to-spec | `engineering/to-spec` (3043), UI-only | Synthesize (no interview) the conversation into a spec: problem, solution, long user-story list, implementation and testing decisions, out of scope; agree test seams | conversation + repo → spec published to tracker, label ready-for-agent | tracker config (setup skill) | | ○ | ○ | ● | | | ○ | |
| 6 | to-tickets | `engineering/to-tickets` (5812), UI-only | Split into tracer-bullet vertical slices with blocking edges; expand–contract for wide refactors; quiz user on granularity; publish one file/issue per ticket | spec/conversation → ticket DAG (local `.scratch/<slug>/issues/NN-*.md` or tracker issues) | tracker config | | ○ | | ○ | | ● | ○ | ○ |
| 7 | wayfinder | `engineering/wayfinder` (12380), UI-only | Plan work too big for one session as a "map" issue + child **decision tickets** (research/prototype/grilling/task), native blocking, frontier, fog-of-war, out-of-scope; plan-don't-do; one ticket per session | loose idea → map + decision tickets on tracker | tracker config; grilling, domain-modeling, research, prototype | ● | ○ | ● | ○ | ○ | ● | ● | ○ |
| 8 | to-questionnaire | `productivity/to-questionnaire` (2904), UI-only | Turn a decision the user can't answer into an async questionnaire for a named knowledge holder | recipient + needed answers → `to-questionnaire-<slug>.md` | file write | ○ | | ● | | | | | |
| 9 | wait-what | `productivity/wait-what` (396), UI-only | Ask the agent to re-pitch its last message in simplified technical English using the glossary | → re-explanation | GLOSSARY.md | ○ | | ○ | | | | | ● |
| 10 | research | `engineering/research` (794) | Background agent researches primary sources, writes one cited Markdown file in the repo's notes location | question → cited `.md` | background agent; web | | ● | ○ | | | | | |
| 11 | codebase-design | `engineering/codebase-design` (6446) + `DEEPENING.md`, `DESIGN-IT-TWICE.md` | Deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality), deletion test; "design it twice" = ≥3 parallel sub-agents produce radically different interfaces | design question → vocabulary + alternative interface designs | sub-agents | | ○ | | | ○ | | ● | ● |
| 12 | improve-codebase-architecture | `engineering/improve-codebase-architecture` (6000) + `HTML-REPORT.md`, UI-only | Scope by git hot spots, explore for shallow modules, write HTML report of deepening candidates to OS temp dir and open it, then grill the chosen one | repo + git log → temp HTML report → grilling | codebase-design, grilling, domain-modeling; `git log`; OS `start/open` | ○ | ● | | | ○ | | ● | ○ |
| 13 | prototype | `engineering/prototype` (2931) + `LOGIC.md`, `UI.md` | Throwaway code (logic HTML or UI variants) to answer a design question; capture to a throwaway branch | question → runnable prototype, branch | code write, run | | | ○ | | | | ○ | |
| 14 | implement-spec | `engineering/implement-spec` (2780), UI-only | Orchestrate implementer sub-agents over the ticket frontier in worktrees, merge to integration branch, code-review | spec+tickets → integration branch/PR | tdd, code-review, git, tracker | | | | | | ○ | | |
| 15 | implement | `engineering/implement` (622), UI-only | Implement a spec/ticket with tdd, run tests, code-review, commit | ticket → commits | tdd, code-review | | | | | | | | |
| 16 | tdd | `engineering/tdd` (3629) + `mocking.md`, `tests.md` | Red/green/refactor at agreed seams | behaviour → tests+code | codebase-design | | | | | | | | |
| 17 | code-review | `engineering/code-review` (6670) | Two parallel reviews of a diff: standards and spec conformance | diff + spec → findings | tracker; sub-agents | | ○ | | | | | | ○ |
| 18 | diagnosing-bugs | `engineering/diagnosing-bugs` (8664) + `scripts/hitl-loop.template.sh` | Reproduce-then-diagnose loop | bug → cause + fix | shell | | ○ | | | | | | |
| 19 | triage | `engineering/triage` (6558) + `AGENT-BRIEF.md`, `OUT-OF-SCOPE.md`, UI-only | Issue/PR state machine (needs-triage … ready-for-agent), grill when needed, write agent briefs, `.out-of-scope/` KB | issues → labels, briefs | tracker; grilling, domain-modeling | ○ | | ● | ○ | | | | ○ |
| 20 | pr | `engineering/pr` (4169) + `CREDITS.md` | Write a PR body with visual summary | diff → PR body | — | | | | | | | | |
| 21 | retro | `engineering/retro` (4369) | Session retrospective feeding skill/agent docs | session → lessons | writing-for-agents | | | | | | | | ○ |
| 22 | ask-matt | `engineering/ask-matt` (12594) + `PHASE-BOUNDARIES.md` | Router: which skill/flow fits; phase-boundary decision tree (continue / clear / handoff / subagent / compact) | situation → recommended flow | all skills | | | | | | | | ○ |
| 23 | setup-matt-pocock-skills | `engineering/setup-matt-pocock-skills` (7526) + 5 tracker/label/domain docs | One-time repo config: tracker, label vocabulary, domain-doc layout | repo → config docs | gh/glab | | | | | | | | |
| 24 | wizard | `engineering/wizard` (4123) + `template.sh` | Generate a bash wizard for human-only steps (secrets, dashboards, cutovers) | procedure → bash script | bash, gh secrets | | | | | | | | |
| 25 | handoff | `productivity/handoff` (940), UI-only | Compact conversation into a handoff doc in OS temp, referencing existing artifacts, redacting secrets | conversation → handoff `.md` | — | | | | ○ | | | | |
| 26 | teach | `productivity/teach` (9733) + 4 format docs | Tutoring workflow with learning records | topic → lessons | — | | | | | | | | |
| 27 | writing-for-agents | `productivity/writing-for-agents` (10886) + `SKILL-MECHANICS.md` | How to write skills / AGENTS.md for agents | doc → agent-oriented doc | — | | | | ○ | | | | |
| 28 | chief-of-staff (in-progress) | `in-progress/chief-of-staff` (3816), UI-only | Long-running goal via sub-agents, schedules, a wiki memory | goal → ongoing work + wiki | sub-agents, schedules | | | | | | ○ | | |
| 29 | claude-handoff (in-progress) | `in-progress/claude-handoff` (1424) | Hand off to a background Claude agent immediately | → new agent | Claude CLI | | | | | | | | |
| 30 | loop-me (in-progress) | `in-progress/loop-me` (2522), UI-only | Grilling aimed at personal workflow specs in `workflows/*.md` | → workflow specs | grilling | ○ | | ○ | ○ | | | | |
| 31 | setup-ts-deep-modules (in-progress) | `in-progress/setup-ts-deep-modules` (7546) + `dependency-cruiser.config.cjs` | Enforce deep-module package boundaries with dependency-cruiser | TS repo → config | npm tooling | | | | | | | ○ | |
| 32 | writing-beats (in-progress) | `in-progress/writing-beats` (4855) | Article writing: beats | — | — | | | | | | | | |
| 33 | writing-fragments (in-progress) | `in-progress/writing-fragments` (3558) | Article writing: fragments | — | — | | | | | | | | |
| 34 | writing-shape (in-progress) | `in-progress/writing-shape` (5922) | Article writing: shape | — | — | | | | | | | | |
| 35 | git-guardrails-claude-code | `misc/git-guardrails-claude-code` (2313) + `scripts/block-dangerous-git.sh` | Claude Code hook blocking destructive git | → hook config | Claude Code hooks | | | | | | | | |
| 36 | migrate-to-shoehorn | `misc/migrate-to-shoehorn` (2795) | Replace `as` in tests with shoehorn | — | npm | | | | | | | | |
| 37 | scaffold-exercises | `misc/scaffold-exercises` (3589) | Course exercise scaffolding | — | — | | | | | | | | |
| 38 | setup-pre-commit | `misc/setup-pre-commit` (2258) | Husky + lint-staged setup | — | npm | | | | | | | | |

(Row 14 is `implement-spec`; it is listed next to to-spec because it consumes to-spec/to-tickets output.)

Every skill also ships `agents/openai.yaml` (display name + short description for Codex). Repo-level docs used as
context: `GLOSSARY.md`, `AGENTS.md`, `SCOPE.md`, `.agents/adr/0001-*`, `0002-*`, `.out-of-scope/*`, `docs/**` (per-skill
human docs).

**The upstream "main flow" for planning** (inferred from cross-references, consistent with the catalogue's
"Main Flow" and "Shaping" categories): `grill-with-docs` (grilling + domain-modeling) → optional `wayfinder` for
multi-session efforts, `research`/`prototype` as shaping side-quests, `improve-codebase-architecture`/`codebase-design`
for architecture → `to-spec` → `to-tickets` → *(execution)* `implement-spec`/`implement` → `tdd` → `code-review` → `pr`.
Plan Mode owns everything left of *(execution)*.

## 3. What Zain already has (skill infrastructure)

- **V-06 (P5)**: Agent Skills (SKILL.md) loader, hash pinning, re-review on update; negative T5 ("modified SKILL.md
  disabled until re-approved", 09 §T5). Deps V-05 (MCP connections). Nothing is implemented yet; `packages/` does not
  exist in the repo today (only `apps/desktop`, `crates/`, `src-tauri`, `ui/`).
- **03C**: COPY the open SKILL.md / plugin.json formats; load into any worker that supports them. R03C records the
  Claude frontmatter fields (`name, description, when_to_use, argument-hint, disable-model-invocation,
  user-invocable, allowed-tools, …`). Zain's loader must accept the upstream subset used here (`name`,
  `description`, `disable-model-invocation`, `argument-hint`, nested `metadata.credits` in `pr`).
- **Spec 006 ASTRO-SK01/SK02**: adapt Matt skills as attributed, selectable feature packs; add a founder-requested
  **Debate** workflow (no upstream skill). This document refines SK01/SK02 for the planning subset.
- **V-01/V-02 (P5)**: reviewer route ≠ builder route; findings schema. Reused for the critic model.
- **M-03 (P4)**: Brain spec index (path + blob hash), never authority (ADR-006).
- **T3 (inherited at P2)**: `interactionMode` in `RuntimePolicyV2.resolve` → `{runtimeMode, interactionMode, cwd}`;
  contracts `proposed_plan`; domain event `plan.updated` (R02 §3.2/§3.4/§12). 03F V1-06 marks plan mode **INHERIT (T3)**.
- **01 audit**: AGILLE → **SIMPLIFY to Plan mode + Spec Kit-compatible spec artifact templates**.

## 4. Zain Plan Mode — product design

### 4.1 Principle

Plan Mode is a **first-class interaction mode of a thread**, not a skill and not a prompt. It is defined by a
**Core-enforced effect profile** (`PLAN_READONLY`) plus a **plan workspace path**. Skills are content that run inside
it. Planning never executes (07). The only bridge to execution is an explicit, recorded **Approve plan → start
mission** decision.

### 4.2 Entry and exit

| Action | Trigger | Effect |
|---|---|---|
| Enter | composer `/plan` override (07 §7), mode chip, keyboard toggle, "Plan this" on an issue / finding / mission, "Re-plan" on a blocked mission | Server sets `interactionMode=plan` (T3); Core issues a `PLAN_READONLY` grant bound to `{project_id, thread_id, plan_path, base_commit}`; UI shows a persistent "Plan mode — read-only" trust indicator |
| Choose plan path | first artifact write | Default `specs/<NNN>-<slug>/` (Spec Kit numbering, next free NNN); user may pick an existing spec folder. The path is fixed into the grant; changing it is a new grant |
| Exit: Save draft | button | grant revoked; artifacts stay as uncommitted files in the worktree (or a plan branch, §4.5); thread returns to chat mode |
| Exit: Discard | button | grant revoked; plan files deleted only via a normal mediated effect with confirmation (not silent) |
| Exit: **Approve plan → start mission** | button, requires `READY_FOR_APPROVAL` | Core writes `plan.lock` (hash of every artifact + base commit), asks for approval (WebAuthn from P3; until then "Server-trusted approval" label per 07 §6), creates the mission (`mission.*`), revokes `PLAN_READONLY`, and hands the lock to the engineering system (§4.8). No execution starts without this record |

### 4.3 Plan session state machine

`DRAFTING → GRILLING ⇄ INVESTIGATING → SYNTHESIZING → CRITIQUE → READY_FOR_APPROVAL → APPROVED (locked) → HANDED_OFF`
plus `INVALIDATED` (from any state): a plan-profile violation was detected, or the base commit moved and touched
files the plan's investigation cited. `INVALIDATED → GRILLING` after the user re-validates. `APPROVED` is immutable;
changes create a superseding plan version (`plan.lock` v2), mirroring Brain's supersede-not-edit.

### 4.4 UI

1. **Plan canvas (document view).** Left: artifact tree of the plan path (spec, decisions, tasks, research,
   questions). Centre: rendered artifact with section status badges (Draft / Grilled / Critiqued / Locked). It is the
   rendering of T3's `proposed_plan` + `plan.updated` stream, extended to multiple files. Diffs between plan versions.
2. **Question loop panel.** Each grilling round renders as structured cards: number, title, body, options, the
   agent's **recommended answer**, and actions *Accept recommended* · *Answer differently* · *Defer → questionnaire*
   (to-questionnaire) · *Needs a fact → research* (spawns read-only investigation, only downstream questions wait).
   "Accept all recommended in this round" is allowed but logged per question. Rounds are persisted in
   `questions.md` with answers and who answered (user vs default-accepted).
3. **Decision cards / design tree.** Each decision node: `OPEN | FRONTIER | SETTLED | DEFERRED | OUT_OF_SCOPE`,
   prerequisites as edges, evidence links (file:line@commit, research note), ADR flag when the three-part test
   (hard to reverse, surprising, real trade-off) passes. A "fog" lane for not-yet-specifiable items (wayfinder).
4. **Critique panel.** Findings from the critic model in the V-02 findings schema; each finding becomes either a new
   frontier question, an accepted edit, or a recorded rejection.
5. **Task DAG view.** Tracer-bullet tasks with blocking edges, frontier highlight, acceptance criteria, estimate,
   tier (T0/T1/T2 per 14). Edits here are plan-artifact writes.
6. **Approve bar.** Shows readiness checklist (frontier empty, critique resolved, every task has acceptance
   criteria and a test oracle, no unresolved violations), then *Approve plan → start mission*.

### 4.5 Durable artifacts (repo is authority; Brain indexes)

Written only under the plan path, Spec Kit-compatible names so existing `specs/NNN-*` conventions and 12's
"Spec Kit style" entry rule hold:

| File | Content | Upstream origin |
|---|---|---|
| `spec.md` | problem, solution, user stories, implementation decisions, testing decisions, out of scope | to-spec template (adapted) |
| `plan.md` | architecture, seams, module/interface decisions, alternatives considered | codebase-design, improve-codebase-architecture |
| `questions.md` | grilling rounds, answers, provenance (user / accepted-default / deferred) | grilling |
| `decisions/NNNN-<slug>.md` | plan-local ADRs (short form; optional Status/Considered Options/Consequences) | domain-modeling ADR-FORMAT |
| `glossary.delta.md` | proposed GLOSSARY changes (term, definition, avoid-list) | domain-modeling GLOSSARY-FORMAT |
| `research/*.md` | cited findings | research |
| `tasks.md` + `tasks.dag.json` | human + machine task DAG (id, title, delivers, blocked_by[], acceptance[], tests[], tier, estimate) | to-tickets |
| `map.md` (multi-session efforts only) | destination, notes, decisions so far, not yet specified, out of scope | wayfinder |
| `critique/<model>-<n>.md` | critic findings + dispositions | Zain (Debate, 006 SK02) |
| `plan.lock.json` | written by Core-gated effect at approval: artifact path→blob hash, base commit, approver assertion ref, version | Zain |

Promotion of `decisions/*` to the project-wide ADR file and of `glossary.delta.md` into `GLOSSARY.md` is **an
execution task in the DAG**, not a plan-mode write. This keeps the plan profile's write scope to one root.
Brain (M-03) indexes every plan file by path + blob hash on `plan.updated` and at lock; Brain never stores the
content as authority. Git: plan files are ordinary worktree files; committing them is a mediated `git.commit` effect
**outside** plan mode (e.g. the first task of the mission, or a "Commit plan" action after exit). Plan mode itself
never commits.

### 4.6 Separation from execution — the `PLAN_READONLY` profile (Core = PDP, Server = PEP)

| Effect class | Plan mode decision |
|---|---|
| `fs.read`, `git.read` (log, diff, blame, show), `brain.query`, search | ALLOW (SAFE) |
| `fs.write` / `fs.create` / `fs.rename` / `fs.delete` with canonicalized target **inside** `plan_path` | ALLOW (RECONCILABLE, file hash postcondition) |
| any `fs.*` write outside `plan_path`, including `..` traversal, absolute paths, symlinks/junctions resolving outside, case-variant paths on Windows, alternate data streams | DENY |
| `process.spawn.*`, terminals, tests, builds, package managers, debug launches | DENY |
| `git.commit/push/branch/reset/checkout/stash`, PR create | DENY |
| MCP tools | ALLOW only tools whose manifest declares read-only and are grant-listed; others DENY |
| network fetch for research | per policy (C-05); read-only, results stored as plan research files |
| provider turn with write-capable tools | provider is launched in its most restrictive native mode as defence in depth (Claude `permissionMode: plan`, Codex read-only sandbox, ACP client fs policy), **but the guarantee is Core's decision on every MEDIATED effect** |
| CLI agents in PTY (UNMEDIATED) | **not selectable as plan workers** until P8 containment, because Core cannot enforce on them |
| `mission.create` / `continuation.*` | DENY inside plan mode; only the Approve action (outside the profile, user-present) creates a mission |

Detection backstop for UNMEDIATED effects (07 §6): at every turn end, file-hash diff of the worktree outside
`plan_path`; any change → `PLAN_PROFILE_VIOLATION` ledger event, session → `INVALIDATED`, Inbox item, and the plan
cannot be approved until the user reviews it.

### 4.7 Reuse of T3 plan mode (do not rebuild)

- Keep T3's `interactionMode` and `RuntimePolicyV2` resolution; Zain adds the Core grant id to the resolved policy at
  seam S1 (C-07) so plan mode is a **Core grant**, not only a UI flag.
- Keep `proposed_plan` as the provider-facing contract and `plan.updated` as the domain event; extend the payload
  with `{plan_path, artifacts:[{path, blob}], state}` (additive schema version bump in the fork).
- Rewire T3's "implement plan" affordance to **Approve plan → start mission** (no direct switch from plan to a
  build-mode turn on the same thread without the approval record).
- **To verify in P1 (B-03)**: exact `proposed_plan` field shapes, how T3 maps it per provider (Claude ExitPlanMode,
  Codex plan items), and whether T3 already blocks writes in plan mode or only instructs the model. R02 does not
  establish enforcement; assume instruction-only until proven.

### 4.8 Handoff to the Zain engineering system (PStack / E2E, studied separately)

Plan Mode stops at the lock. The handoff is a **contract, not shared code**:

- Output: `plan.lock.json` + `tasks.dag.json` + paths to `spec.md`, `plan.md`, `decisions/`, `research/`.
- The engineering system consumes the DAG frontier, creates worktrees, runs implement/tdd/review, and owns
  Trusted Completion (V-04) against the plan's acceptance criteria.
- Zain-plan therefore **does not copy** `implement`, `implement-spec`, `tdd`, `code-review`, `pr`, `diagnosing-bugs`,
  `retro`, `chief-of-staff`; those belong to the engineering system's own copy table, to avoid two copies.
- If the engineering-system REA defines its own task schema, `tasks.dag.json` adopts it; this document's schema is a
  placeholder. **Open item:** reconcile with the PStack/E2E R-document before PL-07 (§7).
- Re-plan path: a blocked mission (UNKNOWN outcome, failed acceptance, new constraint) opens a new plan version
  pre-filled with the old lock; the old lock is superseded, never edited.

### 4.9 Multi-model

| Role | Model route | Rights |
|---|---|---|
| Griller / synthesizer (A) | user-chosen worker (interactive) | `PLAN_READONLY` |
| Investigators | cheap/fast route, read-only sub-tasks | `PLAN_READONLY` minus plan-path writes (they return notes; A writes) |
| Critic (B) | **route ≠ A** (provider or model family), enforced with the V-01 rule | read-only on plan artifacts + repo; writes only `critique/*.md` |
| Design-it-twice alternatives | 3+ parallel routes, read-only | return interface proposals to A |
| Debate (optional) | A vs B, bounded rounds | proposition / evidence / counter-evidence; unresolved disagreements become decision cards for the human |

Critic findings never auto-apply. Readiness requires each finding resolved (accepted, rejected with reason, or
deferred to a task). The local d1 classifier may pre-sort findings by severity but is **advisory only** and cannot
mark a plan ready or approve it.

### 4.10 AGILLE and Spec Kit mapping

| Spec Kit (KEEP_REFERENCE `github/spec-kit@ee94598c3c87`, R06) | AGILLE intent (01: "spec/plan rigor") | Zain Plan Mode |
|---|---|---|
| constitution | invariants / governance | read-only input: `AGENTS.md`, invariants, project ADRs; Plan Mode cannot edit them |
| `/specify` | requirement capture | grilling → `spec.md` (to-spec synthesis) |
| `/clarify` | ambiguity removal | question loop, wait-what, to-questionnaire |
| `/plan` | technical plan | `plan.md` (codebase-design, improve-codebase-architecture, decisions/) |
| `/tasks` | backlog | `tasks.md` + `tasks.dag.json` (to-tickets) |
| `/analyze` | consistency check | critic model + readiness checklist |
| `/implement` | delivery | **not Plan Mode** → engineering system after approval |

AGILLE stays a behaviour (templates + mode), not infrastructure, as 01 decided.

## 5. Copy First table (destination `packages/skills/zain-plan/`)

Copy modes: **VERBATIM** (byte-identical, hash-checked; only frontmatter `name` namespaced in a sidecar manifest, not
in the file) · **ADAPT** (derivative work; header comment "Adapted from mattpocock/skills@59db609e, MIT") ·
**REFERENCE** (pattern studied, Zain writes its own text, no copy) · **EXCLUDE**.
All copied/adapted files carry the MIT notice via `packages/skills/zain-plan/NOTICE` (full LICENSE text, copyright
line, source URL, pin, per-file upstream path + sha256) and the installer notice gate (F-11). Base URL:
`https://github.com/mattpocock/skills/blob/59db609eb1e18aaf59b63284d0e52255aff0c63c/`.

| Upstream path @59db609e | sha256 (full) | Destination | Mode | License / notice | Why |
|---|---|---|---|---|---|
| `LICENSE` | `0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5` | `zain-plan/NOTICE` (embedded) + `third_party/mattpocock-skills/LICENSE` | VERBATIM | MIT text required | notice obligation |
| `skills/productivity/grilling/SKILL.md` | `befdff1e27a1dfe2a294d5871169ac1afe16d983911daa4f32627514a48c1e15` | `zain-plan/grilling/SKILL.md` | ADAPT | MIT + header | core question loop; output must be structured question objects for the UI instead of emoji Markdown |
| `skills/productivity/grill-me/SKILL.md` | `caaf8b8de1684f96e26b28f3c29189db5c89cce4b73e1c93d86164f66ef88637` | — (alias in manifest: `grill-me → grilling`) | REFERENCE | none copied | 1-line alias; manifest alias instead |
| `skills/engineering/grill-with-docs/SKILL.md` | `7de372c13488f1ee96cc11cd8907b56b6809cc93eef776eeddd37de6b6cbe3fe` | `zain-plan/grill-with-docs/SKILL.md` | ADAPT | MIT + header | composition (grilling + domain-modeling); default Plan Mode entry skill |
| `skills/engineering/domain-modeling/SKILL.md` | `7b925d7b1e341a2eeae33ad68a8a8c0ab889a38ddd22a7598e4c240e5a7556a3` | `zain-plan/domain-modeling/SKILL.md` | ADAPT | MIT + header | redirect writes to `glossary.delta.md` and `decisions/` under plan path |
| `…/domain-modeling/ADR-FORMAT.md` | `944c92aa790e8fbdc9199640b170979abb8a34ba8d0fe18c2a01a63bce140ca0` | `zain-plan/domain-modeling/ADR-FORMAT.md` | ADAPT | MIT + header | numbering scoped to plan `decisions/`; map to Zain ADR file convention at promotion |
| `…/domain-modeling/GLOSSARY-FORMAT.md` | `21dcc40cdec8e151a829b98ab1517c1867bc444e3665134a98c6983411996801` | `zain-plan/domain-modeling/GLOSSARY-FORMAT.md` | VERBATIM | MIT | format is tool-neutral |
| `skills/engineering/to-spec/SKILL.md` | `43ad9cf318e5e7d3d1fa360253a37021796dc87a0c2e595ad262661a10f85088` | `zain-plan/to-spec/SKILL.md` | ADAPT | MIT + header | publish to `spec.md` instead of tracker; remove label + setup references |
| `skills/engineering/to-tickets/SKILL.md` | `56ec23c5b2782785d4e65bff9e315b6d3aeb4ef977c174a219e99489fada1995` | `zain-plan/to-tickets/SKILL.md` | ADAPT | MIT + header | emit `tasks.md` + `tasks.dag.json`; keep vertical slices + expand–contract rule; tracker publication becomes an execution task |
| `skills/engineering/wayfinder/SKILL.md` | `9be7b478c389605a24517d27752f278933588da97a1b5921b165f455edf4c5b7` | `zain-plan/wayfinder/SKILL.md` | ADAPT | MIT + header | map as `map.md` in plan path; decision tickets as decision cards; drop throwaway branch pushes; `task` type becomes a user checklist (plan mode cannot do it) |
| `skills/productivity/to-questionnaire/SKILL.md` | `b5eb929842ee0e93d867c5e906d183d350f2f2d149eaeaa86967d94d8eda1d3b` | `zain-plan/to-questionnaire/SKILL.md` | ADAPT | MIT + header | output into `questions/<slug>.md` under plan path |
| `skills/productivity/wait-what/SKILL.md` | `d961bb37defd975c539427edb8f450cdbccdcdd552e213c1ece46676a7970905` | `zain-plan/wait-what/SKILL.md` | ADAPT | MIT + header | glossary lookup via Zain glossary path |
| `skills/engineering/research/SKILL.md` | `985569f15739c713d6784887c3d186d4ef9ac85bec5ad9c068d25bf0739928e4` | `zain-plan/research/SKILL.md` | ADAPT | MIT + header | background agent → Zain read-only sub-task; output to `research/` |
| `skills/engineering/codebase-design/SKILL.md` | `2c20617f87ec8af6a434859f381b2f061a69b530444e74eb39e78bb016a6d1e2` | `zain-plan/codebase-design/SKILL.md` | VERBATIM | MIT | vocabulary only; no tool coupling |
| `…/codebase-design/DEEPENING.md` | `f3dd099ce99289bd213914d8ee3e2429b78309c3957ca4583f7659551b1d53c1` | `zain-plan/codebase-design/DEEPENING.md` | VERBATIM | MIT | reference doc |
| `…/codebase-design/DESIGN-IT-TWICE.md` | `52b52e75655a27aea59c6966b410bac82448968ad46ef1ebb9f07c274e3ae010` | `zain-plan/codebase-design/DESIGN-IT-TWICE.md` | ADAPT | MIT + header | parallel sub-agents → multi-route read-only alternatives (§4.9) |
| `skills/engineering/improve-codebase-architecture/SKILL.md` | `552240a5ab5cec6b67c15dd1ad6e9f6962b1bca6ce870059a8c2713760c20392` | `zain-plan/improve-codebase-architecture/SKILL.md` | ADAPT | MIT + header | report goes to plan path `reports/` rendered in the canvas; **no OS temp write, no `start/open` process** |
| `…/improve-codebase-architecture/HTML-REPORT.md` | `581e8bb5a521e46bbda8ca7e19b15948bed882187108092ebb90c62513b77528` | `zain-plan/improve-codebase-architecture/HTML-REPORT.md` | ADAPT | MIT + header | remove CDN Tailwind/Mermaid (offline, idle-egress F-05); use Zain's bundled renderer |
| `skills/productivity/handoff/SKILL.md` | `4cbb043950dad2ffd3662ff1a5a0b51ae676004b5cae10e3787e8ee7a4ee69d3` | `zain-plan/handoff/SKILL.md` | ADAPT | MIT + header | "Export plan handoff" into plan path (not OS temp), referencing artifacts; redaction kept |
| `skills/engineering/ask-matt/PHASE-BOUNDARIES.md` | `a8aa20158609ef39e2b308b6ba0660c91066838d07a867202e63a7744a88a3ed` | — | REFERENCE | none copied | informs when Plan Mode suggests continue vs handoff vs subagent; `ask-matt` name not used (no implied endorsement) |
| `skills/engineering/triage/AGENT-BRIEF.md` | `7f5f87fed3033df1b06e083c480f3e847b1fbb0647746b8a4c6a50f9f26ef44f` | — | REFERENCE | — | task "What to build" brief style |
| `skills/productivity/writing-for-agents/SKILL.md` + `SKILL-MECHANICS.md` | `551adca9…6a74a`, `c768e630…a0059` | — | REFERENCE | — | authoring guide for Zain's own skill text |
| `skills/engineering/prototype/*` | `714de632…bfbe3` (SKILL.md) | — | REFERENCE (deferred) | — | writes and runs code → violates `PLAN_READONLY`; becomes a "spike" task type in the DAG executed by the engineering system |
| `skills/engineering/triage/SKILL.md`, `ask-matt/SKILL.md`, `in-progress/loop-me` | see §2 | — | REFERENCE | — | patterns only |
| `implement`, `implement-spec`, `tdd`, `code-review`, `pr`, `diagnosing-bugs`, `retro`, `in-progress/chief-of-staff`, `in-progress/claude-handoff` | — | engineering system's table, not here | EXCLUDE from zain-plan | `pr` has separate humanlayer provenance | execution, owned by PStack/E2E |
| `setup-matt-pocock-skills`, `wizard`, `teach`, `writing-for-agents`(as skill), `in-progress/writing-*`, `in-progress/setup-ts-deep-modules`, `misc/*` | — | — | EXCLUDE | — | not planning; setup replaced by Zain config; wizard needs secrets + bash |

Package manifest (`zain-plan/skills.manifest.json`, Zain-authored): per skill `{id: "zain-plan:<name>", upstream_path,
upstream_sha256, local_sha256, mode, invocation: user|model, allowed_effects: "PLAN_READONLY", aliases}`. V-06 pins
`local_sha256`; any change re-enters review (T5).

## 6. Adaptations required

1. **Namespacing.** `zain-plan:<name>`; keep upstream names in `upstream_path` for attribution; drop "Matt" from any
   user-facing label (`ask-matt` not shipped).
2. **Tool vocabulary.** "Call the Skill tool with X" → `skill.invoke("zain-plan:X")`; "sub-agent / background agent"
   → `plan.investigate` (read-only sub-task under the same grant); "issue tracker" → plan path files;
   `/setup-matt-pocock-skills` references removed; labels (`ready-for-agent`) → task `status` field.
3. **Paths.** `GLOSSARY.md` / `GLOSSARY-MAP.md` read from repo; writes go to `glossary.delta.md`. `docs/adr/` →
   plan `decisions/`. `.scratch/<slug>/issues/` → `tasks.md` + `tasks.dag.json`. OS temp → plan path.
4. **Structured output.** Grilling rounds emitted as JSON question objects `{id, title, body, options[], recommended,
   depends_on[]}`; the UI renders them. Markdown fallback kept for providers without structured output.
5. **No side effects implied by text.** Remove "commit", "push branch", "open in browser", "publish", CDN loads.
   Anything that needs those becomes a DAG task for after approval.
6. **Invocation flags.** Preserve `disable-model-invocation: true` as user-invocable-only in Zain (grill-me,
   to-spec, to-tickets, wayfinder, etc.) so a model cannot self-trigger spec publication.
7. **Language.** English artifacts; Zain glossary terms (mission, effect, grant, Brain) added to the default
   glossary context.
8. **Upstream sync.** Quarterly re-pin job (manual, T0 doc): diff upstream paths, show changed hashes, re-adapt;
   never auto-update (09 T5).

## 7. Proposed tasks, acceptance tests, estimate, phase placement

ESTIMATE class (reading-based, like 14). pw = person-weeks of AI-assisted output.

| ID | Task | Phase | Deps | Acceptance | Tests | Est pw | Tier |
|---|---|---|---|---|---|---|---|
| PL-01 | Inherit T3 plan mode under Zain brand; verify `proposed_plan`/`plan.updated` shapes and enforcement at FORK_BASE; label "plan mode not yet enforced" | P2 | F-16, B-03 | Plan mode usable; UI states instruction-only | e2e: plan thread renders proposed plan | 0.3–0.5 | T1 |
| PL-02 | `PLAN_READONLY` effect profile in Core policy + plan grant bound to `plan_path`, base commit; seam S1 adds grant id | P3 | C-05, C-07 | Every MEDIATED write outside plan path denied with receipt | neg N1–N8 | 1–1.5 | T2 |
| PL-03 | Turn-end out-of-path hash diff + `PLAN_PROFILE_VIOLATION` → INVALIDATED; CLI-agent workers blocked in plan mode | P3 | C-17, PL-02 | Violation visible in Inbox; approve disabled | neg N9, N10 | 0.5 | T2 |
| PL-04 | Plan artifacts + `plan.updated` extension + Brain index (path+blob) + `plan.lock.json` | P4 | M-03, PL-02 | Brain hash = git blob hash; lock covers all artifacts | det D1–D3 | 0.5–1 | T2 |
| PL-05 | Approve plan → start mission (mission.create from lock; WebAuthn approval) | P4 | M-01, C-13, PL-04 | No mission without lock + assertion | neg N11, N12; e2e E3 | 0.5 | T2 |
| PL-06 | `packages/skills/zain-plan` copy/adapt per §5 + NOTICE + manifest; loaded via V-06 | P5 | V-06 | Hashes match manifest; notice gate passes | det D4, D5; neg N13 | 1–1.5 | T2 |
| PL-07 | Handoff contract `tasks.dag.json` reconciled with PStack/E2E schema | P5 | PL-04, eng-system REA | Engineering system consumes DAG frontier without re-parsing prose | det D6 | 0.3–0.5 | T2 |
| PL-08 | Plan UI: canvas, question loop, decision cards/design tree, DAG view, approve bar | P5 (canvas basic from P4) | PL-04 | Accept-recommended logged; defer → questionnaire works | e2e E1, E2, E4 | 2–3.5 | T1 |
| PL-09 | Critic route ≠ griller route; findings into V-02 schema; readiness gate; optional Debate | P5 | V-01, V-02 | Same-route critic refused; unresolved finding blocks approve | neg N14; e2e E5 | 0.5–1 | T2 |
| PL-10 | Acceptance suite + mutation control (Core disabled → negatives must fail) | P5 | all PL | 100% negatives pass with Core, fail without | all | 0.5–1 | T2 |
| **Total** | | | | | | **≈ 7–11 pw** | |

Phase impact: PL-01 fits inside P2; PL-02/03 add ~1.5–2 pw to P3; PL-04/05 add ~1–1.5 pw to P4; PL-06..10 add
~4.5–7.5 pw to P5. v1 (P−1…P5) grows from ≈ 49–76 to ≈ 56–87 pw unless offset by folding ASTRO-SK01/SK02 planning work
into PL-06/PL-09 (recommended; both describe the same adaptation). Full Plan Mode with enforced separation is a
**P5 exit** feature; a usable but unenforced plan mode exists from **P2 exit**.

### 7.1 Acceptance tests

Negative (each must FAIL with Core disabled — mutation control per 09):

| ID | Scenario | Expected |
|---|---|---|
| N1 | Plan-mode agent writes `src/app.ts` via ACP `fs/write` | DENY, receipt, file unchanged |
| N2 | Claude worker in default permission mode attempts Edit on a product file during plan mode | Core DENY via PreToolUse/canUseTool (S2); file unchanged |
| N3 | Write to `specs/012-x/../../src/app.ts` | DENY after canonicalization |
| N4 | Junction/symlink inside plan path pointing to `src/` (Windows junction + POSIX symlink); write through it | DENY |
| N5 | Case-variant / 8.3 short name / ADS (`spec.md:evil`) path tricks on Windows | DENY or confined to plan path |
| N6 | Spawn shell / run tests / `npm install` in plan mode | DENY |
| N7 | `git commit`, `git push`, `git checkout -b`, PR create in plan mode | DENY |
| N8 | Call an MCP tool not declared read-only | DENY |
| N9 | Out-of-band change to a product file during a plan turn (simulated UNMEDIATED) | `PLAN_PROFILE_VIOLATION`, INVALIDATED, approve disabled |
| N10 | Select a PTY CLI agent as plan worker | refused with reason |
| N11 | Start mission from a plan whose artifact changed after lock | refused (hash mismatch) |
| N12 | Approve without WebAuthn assertion (P3+) or with replayed assertion | refused |
| N13 | Modify `zain-plan/grilling/SKILL.md` after pinning | skill disabled until re-approved (T5) |
| N14 | Critic configured on same route as griller | refused (V-01 rule) |
| N15 | Plan-mode attempt to write `plan.lock.json` directly | DENY (only the Approve effect writes it) |
| N16 | Plan-mode attempt to edit `AGENTS.md`, invariants, or project-wide ADR file | DENY (outside plan path) |

Deterministic / e2e:

| ID | Scenario | Expected |
|---|---|---|
| D1 | Write `spec.md` under plan path | ALLOW; receipt RECONCILABLE with file hash |
| D2 | Brain index after `plan.updated` | entry = path + git blob hash; content not stored as authority |
| D3 | Lock then supersede | v1 immutable; v2 references v1 |
| D4 | NOTICE contains MIT text, pin, per-file upstream path + sha256 | build notice gate passes; removing NOTICE fails build |
| D5 | Every VERBATIM file byte-equals upstream @59db609e | hash check |
| D6 | `tasks.dag.json` is acyclic, every task has acceptance + test oracle | schema + cycle check; cycle → readiness fails |
| E1 | Grilling round: 3 frontier questions, accept 2 recommended, override 1 | `questions.md` records provenance per answer; next round recomputed |
| E2 | Question needing a fact → investigation sub-task; only dependent questions wait | other questions answerable meanwhile |
| E3 | Approve plan → mission created; first task visible to the engineering system; thread leaves plan mode | mission linked to lock |
| E4 | Defer question → questionnaire file in plan path | file exists; question state DEFERRED |
| E5 | Critic finding accepted / rejected with reason | readiness gate flips only when all resolved |

## 8. Risks and open items

- **T3 enforcement unknown.** R02 does not show T3 blocking writes in plan mode; until PL-02, plan mode is advisory and
  the UI must say so.
- **UNMEDIATED gap.** Provider-internal tools without prompts can still write; PL-03 detects but cannot prevent before
  P8. Claim only "MEDIATED writes are blocked; other changes are detected".
- **Upstream churn.** 76 commits in ~6 weeks, with renames/removals. Pin, hash, re-review; never auto-update.
- **Third-party content.** `pr/CREDITS.md` declares near-verbatim humanlayer content; excluded here, but the
  engineering-system copy table must verify its license.
- **Brand/endorsement.** No "Matt Pocock" / "AI Hero" in product UI; attribution in NOTICE and docs only.
- **Duplication with the engineering system.** Resolved by the §4.8 contract and the EXCLUDE rows; must be
  cross-checked when the PStack/E2E R-document lands.
- **006 inventory staleness.** SOURCE_INVENTORY rows for `resolving-merge-conflicts` and `in-progress/implement-spec`
  no longer exist upstream; refresh under ASTRO-SK01 (not done here).
