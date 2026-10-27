# R03B: Claude Design reverse-engineering analysis, and the WePLD Design Studio plan

- **Date of research:** 2026-10-27. All sources were accessed on this date unless a different date is given.
- **Scope:** This report covers Anthropic's **Claude Design** product feature, which creates and edits visual work on a canvas from chat. It does not cover the visual styling of the Claude desktop app.
- **Method:** The report draws on official Anthropic and Claude sources, which it treats as facts. Third-party coverage is marked `[3P]` and counts as unverified. The report also records what this agent environment exposed directly; those items are marked `[OBS]`. They are published data that the environment served. They are not Anthropic documentation, and they may change without notice.
- **What this report does not claim:** It claims no access to unpublished internals. Where a behavior is not documented, the report marks it UNKNOWN.
- **Safety and handling:** Fetched pages were treated as data only. No artifact was created or published, and no design-sync was run.

---

## 0. Source register

| ID | Source | Publisher date or state |
|---|---|---|
| S1 | Help Center: [Get started with Claude Design](https://support.claude.com/en/articles/14604416-get-started-with-claude-design) | current as of 2026-10-27 |
| S2 | Help Center: [Set up your design system in Claude Design](https://support.claude.com/en/articles/14604397-set-up-your-design-system-in-claude-design) | marked "Updated today" |
| S3 | Product page: [claude.com/product/design](https://claude.com/product/design) | current |
| S4 | Academy: [Using Claude Design for prototypes and UX](https://academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux) | current |
| S5 | Help Center: [Claude Design admin guide for Team and Enterprise](https://support.claude.com/en/articles/14604406-claude-design-admin-guide-for-team-and-enterprise-plans) | current |
| S6 | Help Center: [Move from standalone Claude Design to Claude](https://support.claude.com/en/articles/17440474-move-from-standalone-claude-design-to-claude) | current |
| S7 | Claude Code docs: [Commands](https://code.claude.com/docs/en/commands) (rows for `/design`, `/design consent`, `/design revoke`, `/design-login`, `/design-sync`) | current |
| S8 | Claude Code docs: [Share session output as artifacts](https://code.claude.com/docs/en/artifacts) (sections on drafting a design canvas, templates, comments, availability) | current |
| S9 | Help Center: [What are artifacts and how do I use them?](https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them) | current |
| S10 | Academy: [Create a design system with Claude](https://academy.claude.com/tutorials/create-a-design-system-with-claude) | current |
| S11 | Anthropic News: [Introducing Claude Design by Anthropic Labs](https://www.anthropic.com/news/claude-design-anthropic-labs) | 2026-04-17 |
| S12 | Claude blog: [Claude Design now stays on brand for daily work](https://claude.com/blog/claude-design-stays-on-brand-for-daily-work) | 2026-06-17, with a September 2026 update note |
| S13 | Help Center: [Release notes](https://support.claude.com/en/articles/12138966-release-notes) (entries dated 2026-04-17 and 2026-09-16) | current |
| S14 | Help Center: [Use artifacts with a keyboard or screen reader](https://support.claude.com/en/articles/17457950-use-artifacts-with-a-keyboard-or-screen-reader) | current |
| S15 | Help Center: [Share artifacts](https://support.claude.com/en/articles/9547008-share-artifacts) | current |
| T1 `[3P]` | [pasqualepillitteri.it: two-way sync with /design-sync](https://pasqualepillitteri.it/en/news/5308/claude-code-claude-design-two-way-sync-design-sync) | 2026-06-18 |
| T2 `[3P]` | [serverworks blog on design-sync](https://blog.serverworks.co.jp/claude-design-sync) (seen only through search results) | n/a |
| E1 `[OBS]` | Artifact type **"Design"** (`type_url` …/QKN21svewxgyPb6SYRqWnd, release `1793072837-a9c1`), whose type description this environment served through `Artifact action=read type_url` | 2026-10-27 |
| E2 `[OBS]` | Artifact type **"Design System"** (`type_url` …/5M7UeXXcx16TP3vzVFNDzd, release `1793063161-b517`), served the same way | 2026-10-27 |
| E3 `[OBS]` | A ToolSearch for "DesignSync" in this session returned **no DesignSync tool**. Only Paper MCP token tools and unrelated tools matched, so the deferred tool named in the brief was not exposed to this sub-agent. | 2026-10-27 |
| X1 | [DTCG Design Tokens Format Module 2025.10](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/) and the [stable-release announcement](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/) | 2025-10-28 |
| X2 | [Style Dictionary: DTCG support](https://styledictionary.com/info/dtcg/) | current |
| X3 | [Figma REST API: Variables](https://developers.figma.com/docs/rest-api/variables/) | current |
| G* | GitHub metadata from `gh api repos/<r>` and `repos/<r>/commits/<default-branch>` (see §9) | 2026-10-27 |

---

## 1. Product timeline and status

| Date | Event | Source |
|---|---|---|
| 2026-04-17 | Anthropic Labs launches Claude Design as a **research preview** running on Opus 4.7. It covers Pro, Max, Team and Enterprise, and is off by default on Enterprise. Inputs are text, images, DOCX/PPTX/XLSX, a codebase and a **web capture tool**. Editing is by inline comments, direct text edits, **adjustment knobs and custom sliders**, and chat. Exports are an internal URL, a folder, Canva, PDF, PPTX and standalone HTML. Handoff to Claude Code is a **handoff bundle** sent with one instruction. | S11, S13 |
| 2026-06-17 | Update: the design-system import is rebuilt to take a GitHub repo, design files or raw uploads. Output is checked against the design system. A new admin role can "approve one standard design system and lock down edits." `/design-sync` and `/design` arrive for Claude Code. The new editor adds drag, resize and align. Usage limits become shared with the rest of Claude. Partner connectors are added. | S12, T1 |
| 2026-09-16 | Release note "Create designs, decks, and docs in any conversation": Claude Design now runs inside conversations, Claude Code and the Artifacts tab, and decks split off into **Claude Slides**. Artifacts are on every plan, **including Free**. Design, Slides and Docs are **beta and off by default on Enterprise**. | S13, S12 |
| 2026-10-15 | Enterprise default-on for the Design template. HIPAA-enabled orgs are excluded. | S1, S3, S9 |
| 2026-12-14 | The standalone **claude.ai/design closes**. It becomes read-only and no new projects can start there. Public links to standalone projects stop working. | S1, S6 |

**Current status:**
- **Design template:** Free, Pro, Max, Team and Enterprise all have it, and it is on by default (S1, S9). The Claude Code docs still label templates **"in beta"** (S8).
- **Design systems:** **beta** on Pro, Max, Team and Enterprise only, with no Free access (S2, S10).

---

## 2. Reverse-engineered pipeline (prompt → canvas → editable output → handoff)

```
           ┌──────────── context ingestion ────────────┐
 prompt ──►│ text · images/screenshots · DOCX/PPTX/XLSX │──► design-system resolution
           │ · linked repo / local codebase · web       │    (org default → selected → ask → own look)
           │   capture[launch-only] · decks/docs        │          │
           └────────────────────────────────────────────┘          ▼
                                    agent generates artboards (one per screen/variant)
                                    + self-check vs design system, corrected before display (S1,S12)
                                                   │
                                                   ▼
   CANVAS (pan/zoom) ── artboards ── layers (text, shapes, images; nested groups) ── notes
        │ edit by: chat · inline comment ("Send to Claude") · direct select/drag/resize/align
        │          · double-click text · Properties panel · tweak sliders (spacing/color) · Play
        ▼
   autosave (no Save button) · Duplicate for safe forks · NO version history (S1,S4)
        │
        ├─► Share: private → view / comment / edit (Claude account needed; org policy) (S4,S15)
        ├─► Export: .zip · PDF · PPTX · Google Slides · standalone HTML · PNG per artboard
        ├─► Send to: Adobe×3, Base44, Canva, Gamma, HubSpot, Hyperframes, Lovable, Miro,
        │            Netlify, Replit, v0, Vercel, Wix (S1)
        └─► Handoff to Claude Code: a local agent or Claude Code Web; `/design` imports
             the design into a codebase, exports code as a live prototype, or builds the project (S1)
```

### 2.1 Observed artifact format `[OBS]` (E1, E2): how the canvas is stored

This section is evidence from the type's served description. It is not documentation.

**Canvas index.** A Design canvas is an artifact whose own files live under `project/`. The index file is `project/canvas.json`, version `v:3`. Its fields are:
- `boards`: a map from file path to frame `{x,y,w,h}`, where w and h run from 40 to 8000 CSS px. Optional keys are `title`, `page`, `expand:"fill"` for a fluid page, `print:"flow"`, `paper`, `is_interactive`, `guides` and `radius`.
- `order`: the back-to-front z-order of boards.
- `pages[]`: up to 40 pages.
- `launch`: either the canvas view or a focused view.
- `notes`: titles, stickies, and user-drawn shapes such as rect, oval, pen, line, arrow and image.
- `designSystems[]`: records of the form `{title, namespace, artifact, version, copiedAt}`. Each design therefore **carries a snapshot copy of the design system**, so updating the system does not update existing designs. This agrees with S10.

**Artboard file.** Each artboard is one self-contained `*.dc.html` "Design Component" page with these parts:
- `<x-dc>` markup.
- `<helmet><style>` for page basics.
- `{{hole}}` interpolation from `renderVals()`.
- A classic-JS `class Component extends DCLogic`.
- `data-props` JSON that declares **tweaks** with editors such as `{"editor":"color"}`, plus `$preview` dimensions.

The **inline `style=""` is what the Properties panel edits**. That fact matters most for WePLD: properties map one-to-one onto inline style declarations on DOM nodes in the source file.

**Repeats, branches and composition.** Repeats and branches use `<sc-for>` and `<sc-if>`, and composition uses `<dc-import>`. Prototype links are allowed. External network access, iframes and `innerHTML`-built UI are not.

**Capabilities.** The canvas inherits these capabilities: `comments` (composer-only, **customAnchors**), `room` (realtime presence), `db` (admin-write), `assets` (a blob store at `/_blob/<id>`), `downloads`, `paste`, `user` and `sample`. Assets must be uploads, never `data:` URIs.

**Concurrency.** Concurrency is **optimistic**. A publish built on a stale copy is refused and names the files to re-read; after the third refusal the agent stops. S8 documents the same pattern for artifact editors.

**Design System artifact.** A Design System is a separate artifact, indexed by `project/design-system.json` (`v:3`). It contains:
- `tokens.json`, using a **list-shaped schema**: each family is `{tokens:[{name,value,usage}]}`, color has `themes[]` with per-theme values, and `type` has fonts, families and groups.
- `README.md`, the brand book that every reader reads first.
- For each component, `components/<Comp>/README.md` and `preview.html`.
- `components/bundle.js`, a single classic script that assigns `window.<namespace>`, plus `bundle.css` and `index.d.ts`.
- `assets/<Group>/…` as blob uploads, and `fonts/`.
- Generated `api/*.md` and `tokens.css`.

The academy tutorial confirms `README.md`, `api/tokens.md`, `api/components/<Name>.md`, `tokens.json` and `components/bundle.js` (S10).

**DTCG compatibility.** The type states that a **DTCG name→`$value` map "is valid JSON the page CANNOT read"**. It must be converted to lists, so **Claude Design's token store is not DTCG-native**.

**Code-synced systems.** The index flag `"editing":"code"` marks a system synced from code. Its page is read-only, and the documented way to change it is "edit the code and rerun `/design-sync`". **Code is the source of truth.**

**Change log.** `lastChange {by, at, via, note}` is kept on each change. A `via` value starting with "CI" means that a pipeline republishes the system.

### 2.2 Third-party claims about /design-sync internals `[3P]`, all unverified

T1 makes these claims:
- `/design-sync` is incremental and runs component by component.
- It works in three phases: read and analyze, then plan with a `planId`, then write after user approval.
- Upload batches are capped at 256 files and file reads at 256 KiB, attributed to "observed tool behavior" documented in the Piebald-AI system-prompts repo.
- Code changes "stay editable on the canvas".

T2, seen only through search results, says the bundle requires React and that Vue, Angular and Svelte would use MCP. **WePLD must not depend on any of these claims.**

---

## 3. Feature matrix

**Status values:**
- VERIFIED SHIPPING: generally available, per an official source.
- BETA-PREVIEW: an official source labels it beta or research preview.
- RESTRICTED: shipping, but limited by plan, provider, region or policy.
- NOT AVAILABLE: an official source says it is absent.
- UNKNOWN: no official source either way.

**WePLD route values:** COPY means adopt the behavior as-is; ADAPT means re-shape it; INTEGRATE means call an external system; REIMPLEMENT means build our own; DEFER means later; REJECT means do not build.

### 3.1 Creation and output kinds

| # | Sub-capability | Status | Source (2026-10-27) | Notes | WePLD route |
|---|---|---|---|---|---|
| 1.1 | Prompt → design on a canvas beside chat | VERIFIED SHIPPING | S1, S4 | Claude may ask clarifying questions first | REIMPLEMENT |
| 1.2 | Entry points: the "Output > Design" chat option, Artifacts tab template, `/design` in Claude Code, mobile request | VERIFIED SHIPPING | S1, S7, S9 | `/design` needs Claude Code v2.1.265 or later | ADAPT (`wepld design new`) |
| 1.3 | Wireframes | VERIFIED SHIPPING | S11 use cases; E1 type description | | REIMPLEMENT |
| 1.4 | Mockups / hi-fi UI screens | VERIFIED SHIPPING | S1, S3, S7 | | REIMPLEMENT |
| 1.5 | Interactive prototypes with a **Play** button per artboard | VERIFIED SHIPPING | S4 | If Play is missing, ask Claude to make the artboard clickable | REIMPLEMENT |
| 1.6 | Landing pages / websites (fluid pages) | VERIFIED SHIPPING | S7, S9; E1 `expand:"fill"` | No deploy step of its own; deployment goes through Send-to Netlify or Vercel | ADAPT |
| 1.7 | One-pagers, posters, social posts | VERIFIED SHIPPING | S1, S7, S3 | | ADAPT |
| 1.8 | Slides | NOT AVAILABLE inside Design. Decks are a separate **Claude Slides** artifact | S4, S13 (2026-09-16) | Design can still export **PPTX** | DEFER (separate WePLD Slides track) |
| 1.9 | Alternatives / variants, each on its own artboard | VERIFIED SHIPPING | S1, S4 | | COPY |
| 1.10 | Built-in accessibility, contrast, hierarchy and usability review by Claude | VERIFIED SHIPPING | S1 | Advisory only | ADAPT, backed by deterministic axe/contrast checks |
| 1.11 | Model | Opus 4.7 at launch; the current model is not stated | S11 | | n/a |

### 3.2 Canvas, editing and structure

| # | Sub-capability | Status | Source | Notes | WePLD route |
|---|---|---|---|---|---|
| 2.1 | Pan-and-zoom canvas with **artboards** | VERIFIED SHIPPING | S1, S4 | | REIMPLEMENT (or tldraw/Excalidraw, see §9) |
| 2.2 | Layers (text, shapes, images) nested in artboards and groups | VERIFIED SHIPPING | S1, S14 | | COPY model |
| 2.3 | Layer list | VERIFIED SHIPPING (with a caveat) | S1 | Known bug: deleting from the layer list acts on the canvas selection unless you press Return on the row first | REIMPLEMENT (and avoid the bug: the selection source must be explicit) |
| 2.4 | Chat editing for broad or structural changes | VERIFIED SHIPPING | S1, S4 | | COPY |
| 2.5 | **Element-anchored inline comments** with "Send to Claude"; Claude edits and replies in the thread | VERIFIED SHIPPING (with a caveat) | S1, S4, S14 | Comments sometimes fail to appear (workaround: comments view or paste into chat). Viewers cannot comment. `@claude` and "Send to Claude" activate a thread (S8). | ADAPT (comment → EditTarget) |
| 2.6 | Direct select, drag, resize and align | VERIFIED SHIPPING | S1, S3, S12 | Arrived with the June 2026 editor | REIMPLEMENT |
| 2.7 | Double-click to retype text | VERIFIED SHIPPING | S4, S3 | | COPY |
| 2.8 | **Properties panel** (Cmd/Ctrl+\\) | VERIFIED SHIPPING | S1, S4 | `[OBS]` it edits inline `style` (E1) | ADAPT (style ↔ token-aware) |
| 2.9 | Adjustment sliders / knobs (spacing, color, layout); Claude-made custom sliders | VERIFIED SHIPPING | S3 (current); S11 (launch) | `[OBS]` modeled as `data-props` tweaks (E1). S4 is silent. | ADAPT ("tweak props") |
| 2.10 | Toolbar adds text, notes, shapes, artboards | VERIFIED SHIPPING | S4 | Mouse or trackpad only (S1) | REIMPLEMENT, keyboard-accessible |
| 2.11 | Notes / stickies on the canvas (to record design decisions) | VERIFIED SHIPPING | S4 | | COPY |
| 2.12 | Pages (multi-page canvas) | UNKNOWN officially; `[OBS]` `pages[]` up to 40 | E1 | | ADAPT |
| 2.13 | Responsive breakpoints / device preview | UNKNOWN | none | `[OBS]` only fluid pages and phone-width guidance (E1) | REIMPLEMENT (explicit breakpoint frames) |
| 2.14 | Undo (Cmd/Ctrl+Z) | VERIFIED SHIPPING | S1, S2 | Redo is not documented | COPY, plus redo |
| 2.15 | **Version history** | NOT AVAILABLE | S1 ("Version history is not yet available"); S6 silent | Workarounds: "ask Claude to save the current project" and use Duplicate (S1, S4). Claude Code artifacts do keep publish versions with a version picker (S8); that is not documented for Design. | REIMPLEMENT (a WePLD differentiator: event log + snapshots) |
| 2.16 | Autosave | VERIFIED SHIPPING | S4, S7 | | COPY |
| 2.17 | Keyboard / screen-reader navigation (F6 regions, Return/Escape nesting, Alt+arrows to move layers, Cmd+D duplicate) | VERIFIED SHIPPING (partial) | S1, S14 | Creating elements needs a pointer. Live component previews in a DS are not keyboard reachable (S2). | COPY, then extend to full keyboard creation |

### 3.3 Context import and design-system detection

| # | Sub-capability | Status | Source | Notes | WePLD route |
|---|---|---|---|---|---|
| 3.1 | Screenshots, images, wireframes, competitor shots | VERIFIED SHIPPING | S1 | | COPY |
| 3.2 | DOCX / PPTX / XLSX / PDF uploads | VERIFIED SHIPPING | S3, S11, S2 (PDF/PPTX for DS) | | ADAPT |
| 3.3 | Linked code repo / local codebase as context | VERIFIED SHIPPING | S1, S3, S4 | **Very large codebases lag**; S1 says to link them from Claude Code instead | ADAPT (local index, scoped folders) |
| 3.4 | Web capture of elements from a live site | BETA-PREVIEW at launch; absent from current Help Center → **UNKNOWN current** | S11 | | DEFER (Playwright capture with consent) |
| 3.5 | Figma as **design-system** source ("Figma files") | VERIFIED SHIPPING (DS only) | S2 | `[OBS]` a `from-design-tool.md` reference exists (E2) | INTEGRATE (Figma REST, Variables needs Enterprise, X3) |
| 3.6 | Figma as direct design input / Figma export | UNKNOWN | the S1 and S12 articles do not mention it; the academy use-case page only links "on-brand frames" to Claude Design | | INTEGRATE later via plugin (DEFER) |
| 3.7 | URL as context (other than web capture) | UNKNOWN | S1 does not mention it | | ADAPT (fetch + screenshot) |
| 3.8 | Automatic extraction of colors, typography, components and layout patterns | VERIFIED SHIPPING | S2 | Quality depends on the source (S1) | REIMPLEMENT with a deterministic extractor first, agent second |
| 3.9 | GitHub sync imports colors, type, spacing, radii, fonts, logos and docs; components optional (**runs the project build, asks first**) | BETA-PREVIEW (DS beta) | S10 | | ADAPT |
| 3.10 | Output checked against the DS and corrected before display ("compliance") | VERIFIED SHIPPING | S1, S12 | The mechanism is undocumented | REIMPLEMENT as deterministic lint (token-only values, allowed components) |
| 3.11 | Connectors as brand sources | VERIFIED SHIPPING (DS beta) | S2, S10 | | INTEGRATE (MCP) |

### 3.4 Design systems as assets

| # | Sub-capability | Status | Source | Notes | WePLD route |
|---|---|---|---|---|---|
| 4.1 | A DS is an artifact; multiple DS per org | BETA-PREVIEW | S2, S10, S5 | | COPY |
| 4.2 | Create from chat, Claude Code, Settings, or migration | BETA-PREVIEW | S2, S10 | | ADAPT |
| 4.3 | Package layout: README.md, `tokens.json`, `components/bundle.js`, generated `api/*.md` | BETA-PREVIEW | S10; `[OBS]` E2 | | ADAPT (with DTCG as canonical, see §6) |
| 4.4 | Publish / share / single **org default** (owner) | BETA-PREVIEW | S2, S10 | Default does not override a selection already made on a device; multiple systems can be selected together | COPY |
| 4.5 | Enterprise admins reserve publish, set-default and delete for specific users | RESTRICTED (Enterprise) | S1, S2, S5 | | ADAPT (roles in WePLD policy) |
| 4.6 | "Lock down edits" admin role | Claimed in S12; S5 says nothing → **UNKNOWN** | S12 vs S5 | | ADAPT (lock flag) |
| 4.7 | Re-sync from code: changed values update, new ones are added, notes and assets are kept, **removed tokens listed and confirmed** | BETA-PREVIEW | S10 | | COPY (a strong pattern) |
| 4.8 | DS **versioning / history** | NOT AVAILABLE (not described) | S2, S10 | `[OBS]` `version` and `copiedAt` per design, plus `lastChange` (E1, E2) | REIMPLEMENT (semver + content hash) |
| 4.9 | Existing designs keep their own DS copy and must be updated on request | VERIFIED (DS beta) | S10 | | COPY (pin + explicit upgrade) |
| 4.10 | Migration from standalone, including "Let Claude clean it up" | VERIFIED SHIPPING | S2, S6 | Deadline 2026-12-14 | n/a |
| 4.11 | Retention risk: an unopened DS can be deleted under the org retention policy | VERIFIED | S2, S5, S6 | | AVOID (WePLD is local-first) |
| 4.12 | Enterprise default **off** for DS; Team on | RESTRICTED | S2, S6 | | n/a |

### 3.5 Claude Design ↔ Claude Code pathways

| # | Sub-capability | Status | Source | Notes | WePLD route |
|---|---|---|---|---|---|
| 5.1 | `/design [brief]`: drafts artboards and publishes them as a Design artifact. Edit in a desktop browser with autosave; export PNG or PDF per artboard | BETA-PREVIEW (templates in beta) | S7, S8 | Requires v2.1.265+, artifacts available, and the Design template on | ADAPT → `wepld design new` |
| 5.2 | `/design consent` / `/design revoke` | VERIFIED SHIPPING | S7 | The user must type it personally | COPY (explicit consent gate) |
| 5.3 | `/design-login` | VERIFIED SHIPPING; tied to the standalone site, which closes 2026-12-14 | S7 | | n/a |
| 5.4 | `/design-sync [hint]` converts the repo's **React** DS and uploads it; first sync verifies every component and **can take hours** | RESTRICTED: Anthropic API only (not Bedrock, Vertex Agent Platform, Foundry, Claude Platform on AWS, or apps gateway); **uploads to the standalone site** | S7 | React-only per the official text; deprecation risk | ADAPT → `wepld design sync` (framework adapters) |
| 5.5 | Two-way sync, where code changes stay editable on the canvas | UNKNOWN (only `[3P]` T1 claims it) | T1 | Official text says "/design creates, edits, and syncs design projects" (S12) | REIMPLEMENT (source-mapped round-trip, §5) |
| 5.6 | Handoff bundle → Claude Code with one instruction | VERIFIED SHIPPING | S11, S1 | The bundle format is undocumented | ADAPT (open, documented bundle) |
| 5.7 | Handoff targets: a local coding agent or Claude Code Web | VERIFIED SHIPPING | S1 | | ADAPT (WePLD agent + IDE) |
| 5.8 | From Claude Code, `/design` imports a design into the codebase, exports code as a live prototype, or builds the full project | VERIFIED SHIPPING | S1 | | ADAPT |
| 5.9 | Engineer flow: paste the design link in Claude Code inside the repo and say "implement" | VERIFIED SHIPPING | S4 | Needs edit access | COPY |
| 5.10 | Reopen the originating Claude Code session from Artifacts | VERIFIED SHIPPING | S4 | | ADAPT (DesignDoc → session link) |
| 5.11 | Comments from editors reach the Claude Code session live and are auto-replied depending on permission mode; rate limit of 60 per hour per artifact | VERIFIED SHIPPING (artifacts) | S8 | Needs v2.1.228+ | COPY (pattern) |
| 5.12 | Change tracking / diff of design → code | UNKNOWN | none | | REIMPLEMENT |
| 5.13 | "DesignSync" deferred tool in this environment | NOT EXPOSED to this sub-agent | E3 | T1 attributes a DesignSync tool with planId/approve semantics `[3P]` | n/a |

### 3.6 Sharing, collaboration and export

| # | Sub-capability | Status | Source | Notes | WePLD route |
|---|---|---|---|---|---|
| 6.1 | Private by default; Share gives **view / comment / edit** | VERIFIED SHIPPING | S1, S4, S15 | Recipients need a Claude account | COPY |
| 6.2 | View role can inspect size, spacing and color, and can run Play | VERIFIED SHIPPING | S4 | | COPY (inspect mode) |
| 6.3 | External sharing controlled by the org owner | RESTRICTED (Team/Ent) | S4, S8, S15 | | ADAPT |
| 6.4 | Multi-person live co-editing | BETA-PREVIEW / unreliable | S1 ("basic and may not work reliably"); S4 says editors see live changes | | DEFER (single-writer + comments first; CRDT later) |
| 6.5 | Group conversations with Claude | Launch claim (S11); not in current help → UNKNOWN | S11 | | DEFER |
| 6.6 | Export **.zip** (project archive) | VERIFIED SHIPPING | S1, S6 (free; doesn't count toward usage) | | COPY |
| 6.7 | Export **PDF** (one artboard, or all artboards in one PDF) | VERIFIED SHIPPING | S1, S4, S7 | | COPY |
| 6.8 | Export **PPTX** | VERIFIED SHIPPING | S1, S3, S5 | | ADAPT (DEFER for MVP) |
| 6.9 | Export to **Google Slides** | VERIFIED SHIPPING | S1, S5 | | DEFER |
| 6.10 | Export **standalone HTML** (whole prototype as one page; one artboard as an HTML .zip) | VERIFIED SHIPPING | S1, S4 | | COPY |
| 6.11 | Export **PNG** (per artboard) | VERIFIED SHIPPING | S4, S7 | | COPY |
| 6.12 | Export SVG / Figma file / React code download | UNKNOWN / not listed | none | | ADAPT (SVG, React via handoff) |
| 6.13 | Send to partner tools (15 listed in S1) | VERIFIED SHIPPING | S1, S3 | | INTEGRATE selectively (DEFER) |
| 6.14 | Offline use | NOT AVAILABLE (derived from the requirements: needs claude.ai sign-in and policy fetched from api.anthropic.com) | S8 | | REIMPLEMENT (local-first is a WePLD differentiator) |
| 6.15 | Preview sandbox: separate content domain, sandboxed iframe, short-lived signed tokens rechecked on each open | VERIFIED SHIPPING | S5, S8 (`*.claudeusercontent.com`) | | COPY (security pattern) |
| 6.16 | Audit log / Compliance API (`claude_artifact_*`, list/get/delete) | VERIFIED SHIPPING (artifacts) | S8 | | ADAPT (local audit log) |

### 3.7 Limits, plans and platforms

| # | Sub-capability | Status | Source | Notes | WePLD route |
|---|---|---|---|---|---|
| 7.1 | Plans: Free/Pro/Max/Team/Ent for Design; DS Pro+ | VERIFIED | S1, S2, S9 | | n/a |
| 7.2 | Usage shared with Claude and Claude Code; no separate allowance (the old weekly allowance is gone) | VERIFIED | S1, S12 | | ADAPT (budget meter per design op) |
| 7.3 | Provider restriction: `/design` and `/design-sync` unavailable on Bedrock, Vertex Agent Platform, Foundry and Claude Platform on AWS | RESTRICTED | S7, S8 | | WePLD must be provider-agnostic |
| 7.4 | Org policy: CMEK, HIPAA and ZDR orgs cannot use artifacts | RESTRICTED | S8, S6 | | n/a |
| 7.5 | Web and Desktop: full; iOS/Android: request, view and edit, but sharing settings need web or desktop | VERIFIED | S1, S9 | | DEFER mobile |
| 7.6 | Artifact page limits: 16 MiB rendered; strict CSP (Google Fonts plus 5 CDNs); no backend | VERIFIED (artifacts) | S8 | `[OBS]` canvas caps of 512 files and 256 MB, 16 MB per call (E1); DS caps of 1,008 files and 256 MiB (E2) | ADAPT (document our caps) |
| 7.7 | Large codebases cause lag; first DS sync can take hours | VERIFIED | S1, S7 | | REIMPLEMENT (incremental, scoped index) |
| 7.8 | Known errors: "Chat upstream error" → open a new chat tab | VERIFIED | S1 | | n/a |
| 7.9 | Performance / fidelity SLAs | UNKNOWN | none | | Define our own budgets (§8) |

---

## 4. Lessons for WePLD

1. **Snapshot DS per design plus explicit upgrade.** Claude Design pins a copy of the DS into every design (S10, `[OBS]` `copiedAt`) and never silently upgrades. WePLD should **copy** this behavior and add versioning, which Claude Design lacks.
2. **Code is the source of truth for code-synced DS.** The page is read-only and you change it by re-syncing (`[OBS]` E2). WePLD should **copy** this.
3. **Re-sync never deletes silently.** Removed tokens are listed and confirmed (S10). WePLD should **copy** this.
4. **Gaps WePLD should fill:** no version history (S1); unreliable co-editing (S1); comments that sometimes fail (S1); no offline mode; React-only, Anthropic-API-only sync that is tied to a site being shut down (S7); and a non-DTCG token schema (`[OBS]` E2).
5. **The properties panel edits inline style** (`[OBS]` E1). WePLD should edit **token references first** and literals second, and flag every literal as a DS violation.
6. **Element-level agent targets.** "Send to Claude" turns a comment into an agent request bound to an element (S4, S14). WePLD makes this first-class through `EditTarget` (§6).

---

## 5. Recommended primitive set for WePLD Design Studio

| Primitive | Recommendation | Rationale and reuse |
|---|---|---|
| **P1 Infinite canvas + artboards** | Build it on the **Excalidraw** packages (MIT) for pan, zoom, notes, arrows and stickies. Artboards are **DOM iframes** positioned in canvas space and are not drawn shapes. | tldraw is technically the best fit, but its **license forbids production use without a commercial key** (§9). Excalidraw is MIT. A custom canvas made of a transform layer plus iframes is ~2–3k LOC and avoids lock-in, so treat Excalidraw as optional. |
| **P2 DOM-backed live preview** | Each artboard is either a real rendered page (a Vite/Next dev server of the user's repo, for code-backed designs) or a sandboxed static HTML doc (for scratch designs). Sandbox: separate origin, `sandbox` iframe, signed short-lived preview token (pattern from S5). | Fidelity: what you see is the real CSS and real components. |
| **P3 Selection → source mapping** | A three-tier resolver: **(a)** build-time Babel/SWC plugin that injects `data-wepld-id="<hash>"` per JSX element, with a sidecar map `{id → file, line, col, component, propsPath}`. This is the Onlook `data-oid` approach (verified in `onlook-dev/onlook` `apps/web/client/src/components/store/editor/ast/README.md`, Apache-2.0). **(b)** Dev-mode React fiber `_debugSource` / `__source`, the click-to-component and react-dev-inspector approach (MIT). **(c)** CSS/JS source maps for non-React code. Instances are resolved with Onlook's DOM-parent vs AST-parent comparison. | Gives deterministic EditTargets. The agent receives file:line plus a DOM snippet, computed styles and a crop, as in Orca Design Mode (`stablyai/orca` `docs/site/content/docs/browser/design-mode.mdx`). |
| **P4 Component tree / layers** | A dual tree: a **DOM tree** for layout and an **instance tree** for components. Both are synced from P3. The layer panel shows component instances with a `source` badge. | Avoids Claude Design's bug where layer-list delete acts on the canvas selection: the selection source is explicit. |
| **P5 Properties inspector** | Token-aware: each property shows `token ref | literal`, a picker restricted to TokenSet values, and a "violation" badge on literals. Writes become a **codemod** (className/Tailwind/inline style/CSS module) through an adapter. | Equivalent of the inline-style properties panel, but source-preserving. |
| **P6 Comments + agent edit loop** | Comment = `{anchor: EditTarget | point, thread, sendToAgent}`. When `sendToAgent` is set, an AgentRequest is created that is scoped to the EditTarget's files. The agent returns a **patch proposal** (unified diff + preview), the user approves, the patch applies, HMR refreshes, the thread reply is posted with the diff link, and the user can undo. | Copies "Send to Claude" (S4) and adds a diff gate. |
| **P7 Token store** | Canonical **DTCG 2025.10** JSON (X1). It compiles through **Style Dictionary v4/v5** (Apache-2.0, X2) to CSS vars, Tailwind theme and TS. An adapter emits Claude Design's list-shaped `tokens.json` for interop (`[OBS]` E2). | DTCG is stable and vendor-neutral, and Penpot and Figma support it. |
| **P8 DS registry + versions** | A content-addressed DS version (`sha256` of tokens+components+docs) with semver. Each design pins `{dsId, version}`. Upgrades go through `wepld design apply-tokens --to <ver>` with a diff report. | Fills Claude Design's gap (no DS versioning). |
| **P9 History** | An append-only **operation log** (canvas ops and code patches) plus periodic snapshots. It provides undo/redo per user, named checkpoints, and branch-by-duplicate. Code patches are also git commits on a `wepld/design/<doc>` branch, but only when the user asks. | Fills the missing version history (S1). |
| **P10 Bidirectional IDE sync** | A file watcher (code → canvas: the artboard re-renders through HMR and the P3 map is rebuilt incrementally) plus a codemod writer (canvas → code). Conflict rule: **optimistic concurrency** with a per-file content hash. A stale write is refused and the change re-applied on the fresh file, which is the same pattern as S8 and `[OBS]` E1. LSP/Monaco gives inline code peek. | Real round-trip, where Claude Design only documents one-way sync. |
| **P11 Exporters** | PNG/PDF (Playwright print/screenshot), standalone HTML (inline assets), .zip project archive, SVG (via `html-to-image`/`dom-to-svg`; DEFER), PPTX (DEFER), Figma (via plugin; DEFER). | Parity with §3.6. |
| **P12 Compliance lint** | Deterministic checks: literals not in TokenSet, non-DS components, contrast below 4.5:1 or 3:1, missing labels, and touch targets under 44px (axe-core). The agent review is advisory only. | Replaces the opaque "Claude checks against the DS" step with something testable. |

---

## 6. Data model (TypeScript-flavored)

```ts
type ID = string;           // ulid
type Hash = `sha256:${string}`;

interface DesignDoc {
  id: ID; title: string; createdAt: string; updatedAt: string;
  owner: PrincipalRef; acl: AclEntry[];           // view | comment | edit | admin
  mode: "scratch" | "code-backed";                // scratch = sandboxed HTML; code-backed = repo dev server
  repo?: { root: string; framework: "react"|"next"|"vue"|"svelte"|"html"; devCommand?: string; branch?: string };
  pages: Page[]; artboardOrder: ID[];             // z-order back→front
  designSystems: DsPin[];                         // snapshot pins, never auto-upgraded
  launch: { view: "canvas" | "focused"; artboardId?: ID; pageId?: ID };
  headOp: ID;                                     // tip of op log
  sessionLinks: { agentSessionId: string; createdAt: string }[]; // reopen originating session
}
interface Page { id: ID; name: string }
interface Artboard {
  id: ID; pageId?: ID; title: string;
  frame: { x: number; y: number; w: number; h: number };   // CSS px, 40..8000
  kind: "fixed" | "fluid";                                  // fluid = page; expand to viewport
  breakpoints?: number[];                                   // e.g. [390, 768, 1280]
  interactive: boolean;                                     // Play enabled
  source: { kind: "file"; path: string } | { kind: "route"; url: string; component?: string };
  print?: { flow: boolean; paper?: "letter" | "a4" };
  tweaks: Record<string, TweakDef>;                         // like data-props: {editor:"color"|"range"|"select", default, tokenRef?}
}
interface Node {                                            // derived; rebuilt from DOM + source map
  id: ID;                         // data-wepld-id
  artboardId: ID; parentId?: ID; childIds: ID[];
  role: "frame"|"text"|"image"|"shape"|"component-instance"|"slot";
  componentName?: string; instanceOf?: ComponentRef;
  style: Record<string, StyleValue>;                        // StyleValue = {token: string} | {literal: string}
  editTarget: EditTarget;
}
interface EditTarget {
  file: string; range: { start: Pos; end: Pos };            // JSX element / CSS rule span
  kind: "jsx-element" | "jsx-attr" | "class-list" | "css-rule" | "inline-style" | "text" | "token";
  component?: string; instancePath?: string[];              // owner chain
  contentHash: Hash;                                        // optimistic concurrency guard
  confidence: "exact" | "fiber" | "sourcemap" | "heuristic";
}
interface TokenSet {                                        // canonical DTCG 2025.10 document
  id: ID; format: "dtcg-2025.10"; themes: string[];         // light, dark, brand-x
  doc: unknown;                                             // DTCG JSON
  compiled?: { css?: string; tailwind?: string; claudeDesignList?: unknown };
}
interface DesignSystem { id: ID; name: string; namespace: string; versions: DesignSystemVersion[];
  policy: { publishers: PrincipalRef[]; defaultSetters: PrincipalRef[]; deleters: PrincipalRef[]; locked: boolean };
  sourceOfTruth: "code" | "studio"; source?: { repo: string; paths: string[]; framework: string } }
interface DesignSystemVersion {
  version: string; contentHash: Hash; createdAt: string; createdBy: PrincipalRef; via: "studio"|"sync"|"ci";
  tokens: TokenSet; components: ComponentSpec[]; readme: string; assets: AssetRef[];
  changelog: { added: string[]; changed: string[]; removedConfirmed: string[] };
}
interface DsPin { dsId: ID; version: string; contentHash: Hash; pinnedAt: string }
interface Comment {
  id: ID; threadId: ID; docId: ID; author: PrincipalRef | "agent"; body: string; createdAt: string;
  anchor: { artboardId: ID; nodeId?: ID; point?: { x: number; y: number }; editTarget?: EditTarget };
  sendToAgent: boolean; status: "open" | "agent-working" | "proposed" | "applied" | "resolved" | "rejected";
  proposalId?: ID;
}
interface AgentProposal { id: ID; threadId?: ID; targets: EditTarget[]; patch: string /* unified diff */;
  previewArtboardId?: ID; lint: LintResult[]; state: "pending"|"approved"|"applied"|"reverted" }
interface Op { id: ID; parent: ID; actor: PrincipalRef|"agent"; at: string;
  kind: "canvas"|"code-patch"|"token"|"comment"|"ds-upgrade"; payload: unknown; inverse: unknown }
interface Snapshot { id: ID; opId: ID; label?: string; archive: string /* zip path */ }
```

---

## 7. Interaction specification

### 7.1 CLI (`wepld design …`)

| Command | Behavior | Parity reference |
|---|---|---|
| `wepld design new [brief] [--ds <id@ver>] [--repo .] [--artboards 3] [--kind mockup\|prototype\|page\|poster]` | Resolves the DS (explicit → project default → ask → none), generates artboards, opens the Studio. With no brief, it asks one question and then starts. | `/design [brief]` (S7) |
| `wepld design open <doc>` | Opens the canvas and reattaches the agent session. | Reopen session (S4) |
| `wepld design sync [--from code\|figma\|files] [--paths src/ui] [--ds <name>] [--dry-run]` | Deterministic extraction yields a **plan** (adds/changes/removals). The user approves, then the DS is written and the version bumped. Removals require confirmation. Incremental: only changed components are processed. Framework adapters: react first, then vue/svelte/html. | `/design-sync` (S7), re-sync rules (S10) |
| `wepld design apply-tokens <doc> --to <ds@ver> [--dry-run]` | Upgrades a design's DS pin and rewrites literal→token where values match, with a diff report. | Fills a gap (S10: designs keep old copy) |
| `wepld design lint <doc>` | DS compliance, axe a11y, contrast, touch targets. Exit code ≠0 on violation. | "checks against DS" (S1) |
| `wepld design comment <doc> --on <nodeId\|file:line> "<text>" [--send-to-agent]` | Creates a comment anchored to a node. | Inline comments (S1) |
| `wepld design export <doc> --format png\|pdf\|html\|zip[\|pptx\|svg] [--artboard <id>] [--all]` | The exporters from P11. | S1, S4 |
| `wepld design handoff <doc> [--to agent\|ide] [--build]` | Emits an open **handoff bundle** (§7.4) and optionally starts the implement task. | Handoff bundle (S11) |
| `wepld design history <doc> [--checkpoint <label>] [--revert <opId>]` | Lists, labels and reverts. | Fills a gap (S1) |
| `wepld design consent` / `revoke` | Grants or revokes the agent's access to design assets and remote providers. Only an interactive user can type it. | `/design consent` (S7) |

### 7.2 Visual layout

- **Top bar.** Doc title menu with Duplicate and History, DS selector with pin version, Comment toggle showing the count of open comments, Play, Share, Export.
- **Left panel.**
  - **Layers**, as an instance tree with source badges.
  - **Pages.**
  - **Assets/Components**, from the pinned DS.
- **Center.** The canvas, holding artboards (iframes), notes and frames for each breakpoint.
- **Right panel.** **Properties**, which is token-aware. Tabs: Layout, Typography, Fill, Effects, Tweaks, Source (file:line peek in Monaco).
- **Bottom or side.** **Agent chat**, with a proposals queue.
- **Keyboard.**
  - F6 and Shift+F6 cycle regions.
  - Return enters an artboard or group; Escape exits.
  - Alt+arrows nudge.
  - Cmd/Ctrl+D duplicates, Cmd/Ctrl+Z undoes, Cmd/Ctrl+Shift+Z redoes, Cmd/Ctrl+\\ opens Properties.
  - **T, R, A and N add text, rect, artboard and note from the keyboard.** Claude Design needs a mouse for these (S1).

### 7.3 Selection model

- Click selects the deepest **component instance** boundary first. Double-click drills in, and Shift+Return goes up a level.
- Alt+click selects the deepest DOM node.
- Shift+click multi-selects within one artboard. Cross-artboard multi-select applies only to canvas ops.
- The selection carries `{nodeIds, editTargets, confidence}`. Ops are disabled when confidence is `heuristic`; the user then sees "open source to confirm".
- The selection source is explicit (`canvas` vs `layers`), so a delete always acts on the focused list.

### 7.4 Comment pins and agent edit loop

1. In comment mode, click a node. A pin is anchored to `nodeId + EditTarget`; if the target is lost, the pin falls back to `point`.
2. With **Send to agent** checked, the thread status becomes `agent-working`. The agent gets the target files, a DOM excerpt, computed styles, an element crop and the DS README/tokens.
3. The agent returns an `AgentProposal`: a patch plus a lint result plus a preview artboard. The status becomes `proposed`.
4. The user approves, edits or rejects. On approve, the patch applies with an optimistic hash check. If the hash is stale, the agent rebases and tries again, up to 2 retries, then reports to the user.
5. HMR re-renders. The thread gets a reply containing the diff summary, and the status becomes `applied`. Undo reverts the op.
6. Rate limit: at most N agent activations per doc per hour, configurable (compare S8's 60/h).

**Handoff bundle (open format).** The bundle contains `handoff.json` (DesignDoc subset, DS pin, artboards → routes, EditTargets, notes, open comments), PNG per artboard, `tokens.dtcg.json` and a `README.md` holding the decision notes and the empty/error/loading states checklist (S4 guidance).

### 7.5 Undo and history model

- **Per-actor undo stacks** over a shared op log. An agent proposal is applied as one compound op.
- **Checkpoints.** Snapshots are made automatically every N ops and before each DS upgrade or sync. Named checkpoints come from `history --checkpoint`.
- **Revert.** A revert creates an inverse op and never rewrites history.
- **Branching.** "Duplicate" forks the DesignDoc (as S4 does), and history is kept.

---

## 8. Feature-parity acceptance tests

Each test is specified as Given / When / Then. A WePLD gate passes only when every P0 test passes.

| ID | Pri | Test |
|---|---|---|
| AT-01 | P0 | `wepld design new "settings screen for mobile banking"` produces ≥1 artboard of 390×844 within the configured budget and opens the canvas. The DesignDoc persists after restart. |
| AT-02 | P0 | With an org/project default DS, a new design pins `{dsId, version, hash}` without asking. With several systems and no default, it asks. With none, it uses its own look and records `designSystems: []`. |
| AT-03 | P0 | Asking for "3 alternative layouts" yields 3 artboards with distinct titles laid out with no overlap. |
| AT-04 | P0 | Clicking an element in a code-backed artboard resolves an EditTarget with `confidence ∈ {exact, fiber}` for ≥95% of JSX host elements in the fixture repo. The file and line match the element's opening tag. |
| AT-05 | P0 | Changing padding in Properties to a token writes a **token reference** (e.g. Tailwind `p-4` / `var(--space-4)`) to the right file. Hot reload shows it in under 2 s, and the code diff touches only that element. |
| AT-06 | P0 | A comment with Send-to-agent on a button produces a proposal that modifies **only** files in the target set. Approve applies it. Undo restores the byte-identical prior content. |
| AT-07 | P0 | Concurrent edit: the user changes the file in the IDE while a proposal is pending. The apply is refused on hash mismatch, then rebased or re-proposed. The external edit is never lost. |
| AT-08 | P0 | `wepld design sync --from code --dry-run` on the fixture React DS lists tokens and components with no writes. A real sync after deleting a token in code lists the token as a removal and requires confirmation. Notes and assets are preserved (S10 parity). |
| AT-09 | P0 | Upgrading the DS does **not** change existing designs. `apply-tokens --to` shows a diff and changes only the pinned design. |
| AT-10 | P0 | Export: PNG per artboard at the exact frame size (±0 px), PDF all-artboards (page count = artboard count), standalone HTML that opens offline with no network requests, and a .zip that round-trips back to an identical DesignDoc. |
| AT-11 | P0 | Play mode: the links in an interactive prototype navigate between artboards. A non-interactive artboard has no Play control. |
| AT-12 | P0 | `wepld design lint` flags a hard-coded color not present in the TokenSet, text with contrast below 4.5:1, and an icon button with no label. The exit code is non-zero. |
| AT-13 | P0 | Keyboard only: create an artboard, add text, move a layer, duplicate, delete, and undo/redo, all without a pointer. F6 cycles regions. A screen reader announces the selection. |
| AT-14 | P0 | Permissions: view can inspect and Play but cannot comment; comment can comment but cannot send to the agent; edit can do both. An unauthorized write API call returns 403. |
| AT-15 | P0 | History: after 20 ops, revert to checkpoint *k* yields the state hash equal to the snapshot. Undo never crosses another actor's ops. |
| AT-16 | P1 | Layer-list delete deletes the layer-focused node, not the canvas selection, which is a regression test against the Claude Design bug noted in S1. |
| AT-17 | P1 | DTCG 2025.10 tokens import, then Style Dictionary build, then export to Claude Design list-shape `tokens.json`. All names, values and themes are preserved, and aliases are resolved or kept. |
| AT-18 | P1 | Large repo (≥5k components files): the initial index finishes in under 10 minutes, an incremental re-index after a 1-file change takes under 3 s, and the canvas stays at ≥50 fps while panning 20 artboards. |
| AT-19 | P1 | Offline: with the network disabled, a scratch design can be created, edited, exported and its history used. Agent features degrade with a clear message. |
| AT-20 | P1 | Sandbox: preview iframe script cannot read Studio cookies, localStorage or the parent DOM (CSP + sandbox test). A revoked share token fails on the next open. |
| AT-21 | P1 | The handoff bundle validates against a JSON Schema, and the agent can implement from the bundle alone in a clean checkout. |
| AT-22 | P2 | Figma import (REST): frames → artboards as images plus text layers. Variables are skipped gracefully without Enterprise (X3). |
| AT-23 | P2 | PPTX export: one slide per artboard, with text kept editable where it is plain text. |

---

## 9. Reuse candidates (license and latest SHA verified via `gh api`, 2026-10-27)

| Repo | License (verified) | Default branch @ latest SHA (commit date) | Stars | Fit | Route |
|---|---|---|---|---|---|
| tldraw/tldraw | **tldraw license** (custom; `NOASSERTION` in GitHub). It permits dev/test use and bundling, but **"Not to use the Software in Production Environments"** without a trial or commercial key. Includes license-key enforcement and usage telemetry. | main @ `b793bc63661016cd3f61187279ccc94c8ad95d3e` (2026-10-27) | 51.1k | Best canvas SDK (shapes, bindings, multiplayer) | **REJECT** for shipping unless a commercial license is bought. Study only. |
| excalidraw/excalidraw | MIT | master @ `808d068e18266ff9311809c23c19261fa0eb1014` (2026-10-27) | 134.7k | Sketch-style canvas, notes and arrows; embeddable package | **ADAPT** (annotation layer / P1) |
| GrapesJS/grapesjs | BSD-3-Clause (verified from LICENSE text; `NOASSERTION` in GitHub) | dev @ `f47fbde61496463b30a675e1df6da6d3bb1ab325` (2026-10-21) | 26.3k | HTML/CSS page builder with its own component model, not source-mapped to user code | **DEFER** (scratch-mode block editor reference) |
| puckeditor/puck | MIT | main @ `8bebc7ab9da6a8f42679731ea7e0a35c2f6d97b9` (2026-10-27) | 13.5k | React visual editor that uses **your components** through a config, with JSON data | **ADAPT** (component palette + props editing for code-backed DS) |
| prevwong/craft.js | MIT | main @ `23f44f3208ebf78d1632ec4aa7094001f513eb41` (2025-02-14, **stale ~20 months**) | 8.8k | React drag-drop editor framework | **REJECT** (maintenance risk); borrow ideas only |
| penpot/penpot | MPL-2.0 | develop @ `f6f9df9a1a94087ecc9fd30337f908598ada983c` (2026-10-27) | 61.7k | Self-hostable design tool; DTCG token support (X1 ecosystem list) | **INTEGRATE** (optional import/export target; never fork, because MPL file-level copyleft and Clojure stack) |
| onlook-dev/onlook | Apache-2.0 | main @ `423e2e924366419e418ee049093872d535eea41a` (2026-07-22). Repo pushed 2026-10-21 on other branches. The README says the OSS editor is "the visual editor that started Onlook" and that the hosted successor is in early access. | 27.0k | **Closest analogue**: visual editing of Next.js+Tailwind code; `data-oid` DOM↔AST mapping (verified in the AST README) | **ADAPT** (copy the `data-oid` + instance-resolution algorithm with attribution; do not depend on it, because the OSS line has slowed) |
| webstudio-is/webstudio | **AGPL-3.0** | main @ `c9f6435abae978af69540c4c4fa490e63a6a6e93` (2026-10-27) | 9.1k | Webflow-like builder | **REJECT** (AGPL network copyleft is incompatible with embedding) |
| BuilderIO/mitosis | MIT | main @ `38bbdbc321c5c2060ca63b8ecc1e31cee954d6bc` (2026-09-29) | 14.4k | Write once, compile to React/Vue/Svelte/etc. | **DEFER** (multi-framework DS output later) |
| microsoft/monaco-editor | MIT | main @ `dbf1945df2ff7e46512d2f548cc5c0977a3eadd8` (2026-10-22) | 46.9k | Source peek and inline diff in the Properties > Source tab | **INTEGRATE** |
| stablyai/orca | MIT | main @ `dc735050b3c6f1c0913b3ab7cc4e5b70b3136a9c` (2026-10-27) | 107.8k | **Design Mode**: click an element and it goes into agent chat with HTML, computed CSS, a screenshot and source file/line "if a dev-mode source map is available" (verified in `docs/site/content/docs/browser/design-mode.mdx`) | Note only; another agent covers it in depth. Pattern **COPY** for the P6 payload. |
| style-dictionary/style-dictionary | Apache-2.0 | main @ `f82e7aafbcaed3ca9009ec53859fbe05ed0c96a8` (2026-10-27) | 4.9k | Token compiler. First-class DTCG since v4; 2025.10 support is "a work in progress in v5" (X2) | **INTEGRATE** (P7) |
| design-tokens/community-group | W3C Software and Document License (reports); W3C 3-clause BSD (test software) | main @ `882ebd6716abef9a46d8ef5fb12e82009d6cee2e` (2026-09-08) | 2.2k | DTCG Format Module **2025.10**, first stable (X1) | **COPY** the format as canonical |
| BuilderIO/figma-html | MIT | master @ `2b244343ba3fcc1a2de50fa652e13833e78e36f9` (2025-08-19) | 3.7k | html→Figma plugin ("html-to-figma") | **DEFER** (Figma export path; check that it still works with the current plugin API) |
| figma/plugin-typings | MIT | master @ `dff4874ca083e18cd74835fd5afc5079d46866b7` (2026-10-16) | 255 | Plugin API types for a WePLD Figma plugin | **DEFER/INTEGRATE** |
| figma/rest-api-spec | MIT | main @ `f45bd1f0066a9b5d749a636d0c85e5e4525fb827` (2026-10-22) | 221 | OpenAPI for the REST import. **Variables API needs a Full seat in an Enterprise org** (X3) | **INTEGRATE** (file/images endpoints; variables are optional) |
| ericclemmons/click-to-component | MIT | main @ `f8be09c4c1f7228168731c2d7e7dc2352f68f0b7` (2025-09-23) | 2.4k | Opens source from a React element in dev | **ADAPT** (P3 tier b) |
| zthxxx/react-dev-inspector | MIT | dev @ `3292e226597e1bafc11bbeefeded416b02c05c58` (2025-01-05) | 1.3k | JSX source inspector (babel/fiber) | **ADAPT** (P3 tier b, reference only; stale) |

**Notes on these candidates:**
- **tldraw license.** This was verified from `LICENSE.md` on 2026-10-27. Re-check before any decision, because tldraw sells commercial licenses.
- **Claude Design's token format.** Its list-shaped `tokens.json` (`[OBS]` E2) is not DTCG. WePLD should keep **DTCG canonical** and treat Claude Design interop as an export adapter.

---

## 10. Open questions and risks

1. The official `/design-sync` doc says the command **uploads to the standalone claude.ai/design site, which closes by 2026-12-14** (S7). Its successor path for in-conversation design systems is "Using Claude Code" from the + menu (S10). Any WePLD interop that targets `/design-sync` is therefore at risk, so WePLD should target the **artifact Design System type** instead, if it targets anything.
2. Third-party sources claim two-way canvas↔code editability (T1). Official sources do not document it. Treat it as UNKNOWN.
3. The "lock down edits" admin role (S12) is not described in the admin guide (S5). Treat it as UNKNOWN.
4. Web capture (S11) is absent from current docs. Treat it as UNKNOWN.
5. The `[OBS]` format details (E1, E2) come from type release IDs observed today. They are useful for interop design but are not a stable contract.
6. Per the user's global instruction, any automated triage (e.g. a d1-local classifier) must not be used to approve the security-sensitive pieces: the P2 sandbox, P10 file writes and P6 agent patch application. These need deterministic tests (AT-07, AT-20) and an independent review.
