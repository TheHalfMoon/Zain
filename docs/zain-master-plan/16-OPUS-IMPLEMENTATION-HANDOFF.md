# 16 — Implementation Handoff

```text
FOR      = the implementing agent (Opus or another authorized agent) and the founder
STATUS   = execution is NOT authorized by this document; the founder must authorize moving from planning to execution
IDENTITY = the product is Zain; the repository and every artifact stay private; nothing is published
```

## 1. What the repository contains today

- `main` @ `0a843a2`: Rust Core (`crates/contracts`, `crates/core`: identity, read-only git topology, evidence store,
  `wepld` CLI), a Tauri status window that will be retired, 260 static tests, and 85k lines of governance scripts
  (01 §3). Nothing of the selected architecture exists.
- `docs/r0a-opus-start-20261102` @ `23bea38`: the V3 plan (`specs/008-wepld-v3-unified-replan/`), 176 tasks with
  contracts, the R0a work order, and the validator `plan_graph.py`.
- `docs/zain-master-plan-20261108` (this branch, **local only**): this master plan, its registries and `zmp.py`.

## 2. Selected architecture

Hard fork of T3 Code (Electron desktop, Node server, React UI) as shell, server and orchestration. The existing Rust
core is kept, and the Zain Trusted Core (policy decision, ledger, coverage, approvals) is built as new modules inside
it. Orca modules are ported only where listed. V3 ADR-001..024 and this plan's ADR-Z01..Z07 govern (05).

## 3. Approved-for-reuse sources (subject to admission at task time)

ADAPT: T3 Code, Orca (Design Mode, TUI-agent catalog, Linear, computer use; diff comments are a rewrite), Alibaba
Open Code Review (R3 engine), PStack and cursor-team-kit (licensed folders only), mattpocock/skills (not the `pr`
skill), Desktop Commander MCP, Codex Windows sandbox set. INTEGRATE: Monaco, monaco-languageclient,
@vscode/debugprotocol, monaco-vscode-api (only if Z-20 picks it), MCP and ACP SDKs, OpenCode, Playwright, rusqlite,
Cedar, Excalidraw, Style Dictionary, windows-service-rs, Ollama, llama.cpp, LM Studio (external), Opengrep (external),
the user-provided Claude Agent SDK (never bundled). KEEP: Zain Rust core crates. Everything else is REFERENCE, DEFER or REJECT (04).

## 4. Completed work and remaining blockers

| Done | Evidence |
|---|---|
| V3 A-01: main CI re-run green | gh run 36589753362 success |
| Z-05: registries, validator, mutation suite | 15-VALIDATION-EVIDENCE.md (DONE_UNREVIEWED) |
| Audit, research, plan documents 00–17, four EGM review passes with dispositions | this directory; 14 |

| Blocker | Unblocked by |
|---|---|
| Repository public | Founder: Z-01 (DEC-02) |
| No authorized independent reviewer | Founder: Z-06 (DEC-01) |
| Disk capacity | Founder: Z-07 (DEC-12) |
| Isolated account, provider route | Founder: Z-09, Z-10 |
| Founder decisions DEC-01..DEC-15 (six before Q-00) | Founder: Z-25 |

## 5. Working process for every task

Research → plan → implement → test → review → repair → integrate → verify.

1. Read the contract: Z tasks in 11; V3 tasks in `specs/008-wepld-v3-unified-replan/14_TASK_CATALOG.md`.
2. Check every prerequisite and gate edge in `registry/zain-dependency-edges.csv` is DONE or NOT_NEEDED.
3. Inspect the relevant code and the V3 source references (R11/R12 file manifests).
4. Preserve existing work. Never discard a branch, file or PR without founder approval.
5. Write the tests first; implement the smallest complete vertical slice.
6. Run the required tests and gates on the real artifact; record numbers.
7. Independent review per V3 ADR-011: T2 needs the founder plus security review; model review is advisory for T2.
   If no route exists, stop at DONE_UNREVIEWED and say so. Later tasks may start on DONE_UNREVIEWED prerequisites,
   but a milestone exit needs DONE.
8. Fix findings; re-run affected tests.
9. Record evidence in the backlog (`status`, `status_evidence`), run `zmp.py render` and `zmp.py check`.
10. Mark DONE only when all gates pass and review is recorded. An agent's own narrative, its own test run or another
    instance of the same model is not independent review.

**Branches and PRs.** One task (or one tightly coupled pair) per branch, named `zmp/<task-id>-<slug>` or
`v3/<task-id>-<slug>`. Build work for R0a stays on a local `build/first-working` branch and is never pushed while
the repository is public. Keep PRs small (target under 600 changed lines excluding generated or vendored files).
Merge only after: required tests green, independent review recorded, `zmp.py check` green, founder approval for T2.
Never auto-merge. Roll back by reverting the merge commit; never force-push shared branches.

**Interruption and resumption.** Durable state lives in the backlog CSV and the V3 status ledger. After any
interruption: read 17-MASTER-PLAN-STATUS.md, run `zmp.py check`, look for tasks with status IN_PROGRESS, read their
`status_evidence`, then continue. Each session ends with an updated status row and a one-paragraph handoff note in
17 §4.

## 6. The next task

**Founder first:** Z-25 (DEC-01, DEC-02, DEC-04, DEC-07, DEC-08, DEC-12), Z-06 (reviewer route; the founder's own
review always qualifies), Z-01 (make the repository private before any push). These are minutes of founder time.

**First agent task, safe now:** **Z-03** (public-exposure assessment, read-only), together with **Z-18** (incident
close-out, read-only). Neither changes the repository or the machine.

**First engineering unit after M0:** V3 **Q-00** (R0a admission record: source pin per DEC-04, toolchain, licenses,
LOCAL_ONLY route, capacity), with Z-07 and Z-08. Files to investigate: `pingdotgg/t3code` at the chosen pin
(`package.json`, `pnpm-lock.yaml`, `.github/workflows/release.yml`, `release-desktop.yml`,
`scripts/build-desktop-artifact.ts`, `apps/desktop/package.json`), V3 `24_FIRST_WORKING_BUILD.md`,
`OPUS_R0A_BUILD_EXECUTION_2026-11-02.md`, `R0A_FEASIBILITY_READINESS.md`, `research/R11_T3_FILE_MANIFEST.md`. If
DEC-04 re-pins, re-run the R02 §10 seam inventory and re-check the V3 18 citations first. In parallel, Z-29 runs a
one-day trial of the upstream T3 release in the isolated account.

## 7. Tools

Use: Claude Opus for design and synthesis; local `git`, `gh` (read-only unless the founder authorizes a write),
Python with `-I`, Node and pnpm at the pinned versions, Playwright for Electron, Opengrep, local secret scanning.
Use OpenCode or DeepSeek and the Alibaba OCR CLI only on content whose data class their route is authorized for
(DEC-01). d1-local is advisory triage only and never approves. Do not use Codex as the primary research or
engineering agent (founder instruction). Do not install system-wide software or download files without founder
approval.

## 8. Required checks before any merge

`python -I docs/zain-master-plan/tools/zmp.py check` (exit 0) ·
`python -I docs/zain-master-plan/tools/test_zmp_mutations.py` (all cases rejected) ·
`python -I specs/008-wepld-v3-unified-replan/tools/plan_graph.py --check` (exit 0) · the task's own tests and gates.

## 9. Full product readiness

The first release (R0b, founder daily driver) is ready when GATE-R0B-EXIT is MET on one installer SHA-256 (12 §2).
Zain 1.0 is GATE-R0-EXIT; R1 is GATE-R1-EXIT. Readiness never authorizes publication.

## 10. Prohibited until the founder authorizes

- Pushing to the public repository; changing repository visibility or settings; deleting branches or PRs.
- Publishing, releasing, deploying, creating a website, or publishing packages.
- Paid services, paid APIs, hosted runners with billing, or code signing purchases.
- Sending private content to any model or service not authorized for its data class.
- Destructive filesystem actions (deleting founder files, history rewrites), creating OS accounts, changing system or
  security settings.
- Starting implementation beyond read-only M0 tasks.
