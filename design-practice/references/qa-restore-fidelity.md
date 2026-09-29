# QA — Restore Fidelity Check (Stage 1 vs Stage 2 structure diff)

> This is the structural complement to `stage2-fidelity-restore.md`. That file is the contract; this file is how you verify the contract was honored.

## Why a separate check

The fidelity contract (`stage2-fidelity-restore.md`) says Stage 2 maps 1:1 to Stage 1. But contracts can be violated silently — AI drifts, features creep, states get skipped. This check is the post-restore audit that catches drift.

Article line 2099: **"AI 很爱加戏,它觉得多就是好."** The fidelity check is what catches the added charts, the skipped states, the changed containers.

## The diff procedure

Take the chosen Stage-1 drafts and the Stage-2 output. Produce a three-column diff:

```text
RESTORE FIDELITY DIFF
=====================
| Stage 1 element                | Stage 2 implementation              | Verdict |
|--------------------------------|--------------------------------------|---------|
| ASCII block: TOPBAR            | <TopBar>                             | MATCH   |
| ASCII block: SIDEBAR (4 items) | <Sidebar> with 4 nav items           | MATCH   |
| ASCII block: MAIN task list    | <TaskList>                           | MATCH   |
| ASCII block: DRAWER            | <Drawer>                             | MATCH   |
| (not in Stage 1)               | <Chart> analytics panel              | ADDED ✗ |
| (not in Stage 1)               | calendar view                        | ADDED ✗ |
| State: loading                 | <Skeleton>                           | MATCH   |
| State: empty-initial           | <EmptyState kind="initial">          | MATCH   |
| State: empty-filter            | (missing)                            | MISSING ✗ |
| State: error                   | global toast instead of inline       | DRIFT ✗ |
| Permission: viewer × edit      | button visible, 403 on click         | FAIL ✗ |
| Container: drawer for detail   | page navigation instead              | DRIFT ✗ |
| Non-goal: no Gantt             | absent                               | OK ✓    |
| Non-goal: no calendar          | (calendar added — see above)         | FAIL ✗ |
```

Verdicts:
- **MATCH** — Stage 2 faithfully implements Stage 1
- **ADDED** — Stage 2 has something Stage 1 didn't (usually AI adding features)
- **MISSING** — Stage 1 had it, Stage 2 skipped (usually AI avoiding hard work)
- **DRIFT** — Stage 2 has it but differently (e.g. global toast instead of inline error)
- **FAIL** — a rule was violated (permission ignored, non-goal added)
- **OK** — non-goal correctly absent

Any non-MATCH / non-OK verdict = regenerate that part.

## Layer-by-layer audit

### Blocks audit (from Stage 1 ASCII wireframe)
For each block in the ASCII wireframe, find its Stage 2 implementation.

```text
BLOCKS AUDIT
============
Stage 1 TOPBAR ──→ Stage 2 <TopBar>? ──── MATCH
Stage 1 SIDEBAR ──→ Stage 2 <Sidebar>? ── MATCH
Stage 1 MAIN ────→ Stage 2 <TaskList>? ── MATCH
Stage 1 DRAWER ──→ Stage 2 <Drawer>? ──── MATCH
Stage 1 FOOTER ──→ Stage 2 ??? ────────── MISSING (was it cut intentionally?)
```

### States audit (from Stage 1 state-matrix draft)
For each state in the 8×4 matrix, find its Stage 2 implementation.

```text
STATES AUDIT (core component: Button)
=====================================
Stage 1 default  ──→ Stage 2 default styles? ───── MATCH
Stage 1 hover    ──→ Stage 2 :hover? ───────────── MATCH
Stage 1 pressed  ──→ Stage 2 :active scale 0.98? ── MATCH
Stage 1 focus    ──→ Stage 2 :focus-visible ring? ── MATCH
Stage 1 disabled ──→ Stage 2 [disabled] + tooltip? ── MATCH
Stage 1 loading  ──→ Stage 2 aria-busy + spinner? ── MATCH
Stage 1 success  ──→ Stage 2 200ms green flash? ─── MATCH
Stage 1 error    ──→ Stage 2 shake + inline? ────── DRIFT (was global toast)
```

### Object-state-permission audit (from Stage 1 object-state-permission draft)
For each role × state × action cell, verify Stage 2 enforces it.

```text
PERMISSION AUDIT
================
viewer × draft × view ────→ viewer sees draft? ──── FAIL (viewer can't see draft at all)
viewer × active × edit ──→ button disabled + tooltip? ── MATCH
editor × done × edit ────→ admin-only reopen? ────── MATCH
admin × archived × delete → hard-delete button? ──── MISSING
```

### Container audit (from Stage 1 IA draft)
For each container choice in the IA draft, verify Stage 2 uses it.

```text
CONTAINER AUDIT
===============
Stage 1 page (main) ────→ Stage 2 full route? ───── MATCH
Stage 1 drawer (detail) → Stage 2 <Drawer>? ──────── DRIFT (was page navigation)
Stage 1 modal (delete) ─→ Stage 2 <Modal>? ───────── MATCH
```

### Non-goal audit (from Task Card)
For each non-goal in the Task Card, verify Stage 2 doesn't have it.

```text
NON-GOAL AUDIT
==============
Task Card: "no Gantt chart" ────→ absent? ──── OK ✓
Task Card: "no calendar view" ──→ absent? ──── FAIL (calendar was added)
Task Card: "no time-tracking" ──→ absent? ──── OK ✓
Task Card: "no mobile this round" → desktop-only? ── DRIFT (mobile layout added)
```

## Verdict

After the diff, the verdict is one of:

- **SHIPPABLE** — all MATCH / OK, no ADDED / MISSING / DRIFT / FAIL
- **REGENERATE** — any ADDED / MISSING / DRIFT / FAIL → fix that part, re-diff
- **RECONSIDER STAGE 1** — if Stage 2 legitimately needs something Stage 1 didn't have, go back to Stage 1 and add it there, then re-restore (don't sneak it into Stage 2)

## The "AI added features" tell

The most common fidelity failure is AI adding features Stage 1 didn't decide on:

- a chart panel "to make it look richer"
- a calendar view "because task apps have calendars"
- an AI-summary panel "because it's 2026"
- a welcome modal "for onboarding"
- a dark-mode toggle "for completeness"

These are ALL drift. Stage 2 doesn't get to decide product scope — that's Stage 1's job (and the Task Card's non-goals). If a feature is genuinely needed, go back to Stage 1, add a draft for it, get the user to confirm, THEN restore. Never sneak it in.

## Failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| No diff produced | "looks faithful" without checking | mandatory diff output |
| ADDED features accepted | charts / calendars / AI-summary | remove, or back to Stage 1 |
| MISSING states | loading / empty / error skipped | add from Stage 1 matrix |
| DRIFT on container | drawer → page | revert to Stage 1 choice |
| Permission FAIL | viewer can edit | enforce from matrix |
| Non-goal snuck in | calendar added despite non-goal | remove |
