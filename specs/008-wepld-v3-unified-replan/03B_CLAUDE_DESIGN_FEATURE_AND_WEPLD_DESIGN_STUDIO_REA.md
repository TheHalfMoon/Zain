# 03B — Claude Design Feature REA and Zain Design Studio (synthesis)

```text
FULL_REA = research/R03B_CLAUDE_DESIGN.md (feature matrix, data model, CLI + visual interaction spec, AT-01..AT-23)
SOURCES = 15 official sources (Help Center, claude.com/product/design, Academy, code.claude.com commands/artifacts,
          2026-04-17 launch post, release notes), accessed 2026-10-27; [OBS] = artifact-type descriptions read in this
          environment (read-only, nothing published); [3P] = third-party, unverified
SCOPE = the DESIGN FEATURE (creation/editing). Zain's own visual identity is separate and Zain-owned.
```

## 1. What Claude Design does (verified)

- **Timeline:** research preview 2026-04-17 → inside any conversation, Claude Code and Artifacts on all plans incl.
  Free (2026-09-16) → Enterprise on by default (2026-10-15) → standalone claude.ai/design closes 2026-12-14.
  Templates and design systems are labelled beta; design systems are Pro+.
- **Pipeline:** prompt → design-system resolution → canvas of artboards with nested layers → chat edits, element-anchored
  comments ("Send to Claude"), drag/resize/align, double-click text, Properties panel, spacing/color sliders, autosave,
  duplicate, undo → share/export → hand off to Claude Code.
- **Outputs:** wireframes, mockups, hi-fi UI, clickable prototypes (Play per artboard), landing pages, one-pagers,
  posters. Slides are a separate product (Design can export PPTX).
- **Export (each verified separately):** .zip, PDF, PPTX, Google Slides, standalone HTML, PNG per artboard, "send to"
  15 partner tools, Claude Code handoff.
- **Storage format [OBS]:** `canvas.json` index + one HTML file per artboard; Properties panel edits inline styles; each
  design keeps its own copy of the design system; stale-copy saves refused; code-synced design systems are read-only
  (change code, re-sync); `tokens.json` is **not** W3C DTCG.
- **Limits:** no version history; multi-person editing officially unreliable; inline comments sometimes missing; adding
  elements needs a mouse; large codebases lag; no offline; not on Bedrock/Vertex/Foundry/CMEK/HIPAA/ZDR.
- **UNKNOWN:** Figma export, web capture, responsive breakpoints, admin edit-lock role, true two-way canvas↔code sync.
- **`/design-sync`:** React design systems only, Anthropic API only, uploads to the standalone site that closes
  2026-12-14 → Zain interop targets exported HTML/zip and the Design System artifact *format*, not the sync endpoint.

## 2. Where Zain can beat it (falsifiable targets)

| Claude Design gap | Zain Design Studio target | Test |
|---|---|---|
| No version history | Operation log + snapshots per design doc, git-versioned | AT-history |
| Non-DTCG tokens | DTCG 2025.10 as canonical token format; Style Dictionary transforms | AT-tokens |
| Design system copied per design | Versioned design-system registry with explicit pins and upgrade diff | AT-ds-pin |
| No offline | Fully local canvas, preview, tokens; models optional | AT-offline |
| Keyboard gaps | Keyboard-complete creation (insert, select, nudge, align) | AT-a11y |
| Code handoff one-way | Bidirectional: element → source location (EditTarget with file/range/hash/confidence) and source edit → canvas refresh; stale-write refusal | AT-sync |
| Single model | Any worker; agent edits as proposals approved via Core grants | AT-agent-proposal |

## 3. Primitive set and donor decisions

| Primitive | Donor / basis | License (verified) | Route |
|---|---|---|---|
| Canvas of iframe artboards (pan/zoom, multi-artboard) | Zain-built on React; Excalidraw for freeform sketch layer | Excalidraw MIT | ADAPT |
| Live sandboxed preview (project dev server or static HTML) | T3 in-app browser/webviews | MIT | ADAPT |
| Element pick → payload (DOM path, styles, screenshot crop) | Orca Design Mode guest scripts | MIT | PORT |
| Element → source mapping (3 tiers: build-time ids, React dev info, source maps) | Onlook `data-oid` approach; click-to-component / react-dev-inspector | Apache-2.0 / MIT | ADAPT |
| Layer tree + properties panel (token-aware) | Puck patterns | MIT | ADAPT |
| Comments → agent proposal → approve → patch | Zain (Core grant on file writes) | — | BUILD |
| Token store (DTCG) + transforms | DTCG spec; Style Dictionary | W3C / Apache-2.0 | COPY spec / INTEGRATE |
| Code editor alongside | Monaco | MIT | INTEGRATE |
| Exports: HTML/zip, PNG, PDF (print-to-PDF via Chromium), PPTX (later) | Electron `printToPDF`; pptx via a permissive lib (candidate) | — | ADAPT / DEFER PPTX |
| Penpot interop (self-hostable design tool) | Penpot | MPL-2.0 | INTEGRATE (file-level only) |
| tldraw | — | custom license forbids production use without key | **REJECT** |
| Webstudio | — | AGPL-3.0 | **REJECT** |
| Craft.js | — | MIT but dormant since 2025-02 | **REJECT** |

## 4. Interaction specification (summary; full spec R03B §7)

- **CLI:** `zain design new|open|sync|apply-tokens|lint|comment|export|handoff|history|consent`.
- **Layout:** left = pages/artboards + layer tree; center = canvas; right = properties (tokens first) + comments; bottom
  = code (Monaco) for the selected EditTarget; composer docked with element chips.
- **Selection model:** click selects a node in the live DOM; resolver returns EditTarget(s) with confidence; low
  confidence → user picks among candidates; multi-select across artboards.
- **Agent edit loop:** comment pin → agent proposal (patch + preview diff) → Core `effect.propose{FS_WRITE}` → user
  approves → write → canvas refresh → history op recorded.
- **Undo/history:** op log (local) + git commits at checkpoints; undo across agent and human ops in one stack.

## 5. Data model (summary)

`DesignDoc, Artboard, Node, EditTarget{file, range, content_hash, confidence}, TokenSet(DTCG), DesignSystem{version},
DesignSystemPin, Comment, AgentProposal, Op, Snapshot` (R03B §6). Stored as project files under `design/` (git), indexed
by Brain.

## 6. Acceptance (23 tests; 15 P0)

AT-01..AT-23 in R03B §8 cover source mapping accuracy, edit conflict refusal, safe design-system re-sync, export
fidelity, keyboard-only use, permissions (agent writes require grants), history, offline, and preview sandbox isolation
(no preview script can reach Server RPC or Core). Phase 7 exit requires all P0 tests green on Windows.
