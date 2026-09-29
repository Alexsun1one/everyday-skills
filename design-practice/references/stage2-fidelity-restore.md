# Stage 2 — Fidelity Restore Contract (1:1 against Stage 1 drafts)

> Stage 2 restores the chosen Stage-1 drafts into hi-fi. It is NOT a fresh generation. This file is the contract — break it and you've produced an AI-invented UI, not a faithful restore.

## The contract

**Stage 2 output maps 1:1 to the chosen Stage-1 drafts.**

Concretely:
- Every block in the Stage-1 ASCII wireframe → a real block in the restored UI
- Every state in the Stage-1 state matrix → a real state in the restored UI
- Every cell in the Stage-1 object-state-permission matrix → enforced in the restored UI
- Every container choice in the Stage-1 IA draft → preserved in the restored UI
- Every token in the Stage-1 system draft → used in the restored UI
- Every non-goal in the Stage-1 Task Card → NOT in the restored UI

Stage 2's freedom is in **paint** (tokens, typography, micro-interactions, motion). Stage 2's prison is **structure** — it cannot add, remove, or move blocks vs Stage 1.

## The 1:1 mapping table (mandatory output)

Every Stage 2 output includes this table, mapping each Stage-1 element to its Stage-2 implementation:

```text
FIDELITY TABLE
==============
Stage 1 draft: [draft name]

BLOCKS:
| Stage 1 (ASCII)           | Stage 2 (component)         | Status |
|---------------------------|-----------------------------|--------|
| TOPBAR with search+avatar | <TopBar> with Search, Avatar | 1:1    |
| SIDEBAR with 4 items      | <Sidebar> with 4 nav items  | 1:1    |
| MAIN task list            | <TaskList>                  | 1:1    |
| DRAWER task detail        | <TaskDrawer>                | 1:1    |
| [＋ New task] primary     | <Button variant="primary">  | 1:1    |

STATES (from state-matrix draft):
| Stage 1 state   | Stage 2 implementation          | Status |
|-----------------|---------------------------------|--------|
| loading         | <Skeleton> rows × N             | 1:1    |
| empty-initial   | <EmptyState kind="initial">     | 1:1    |
| empty-filter    | <EmptyState kind="filter">      | 1:1    |
| empty-permission| <EmptyState kind="permission">  | 1:1    |
| error           | <ErrorState inline + retry>     | 1:1    |

OBJECT-STATE-PERMISSION (from object-state-permission draft):
| Cell (role × state × action) | Stage 2 enforcement         | Status |
|------------------------------|-----------------------------|--------|
| viewer × active × edit       | button disabled + tooltip   | 1:1    |
| editor × done × delete       | button hidden               | 1:1    |
| admin × archived × restore   | button enabled in archive   | 1:1    |
| ...                          | ...                         | ...    |

CONTAINERS (from IA draft):
| Stage 1 container | Stage 2 implementation       | Status |
|-------------------|------------------------------|--------|
| page              | full-screen route            | 1:1    |
| drawer            | <Drawer side="right">        | 1:1    |
| modal (confirm)   | <Modal> for destructive only | 1:1    |

NON-GOALS (from Task Card):
| Non-goal             | Present in Stage 2? | Status |
|----------------------|---------------------|--------|
| no Gantt chart       | absent              | ✓      |
| no calendar view     | absent              | ✓      |
| no time-tracking     | absent              | ✓      |
| no mobile this round | desktop-only        | ✓      |
```

If any row reads "drifted" or "added", the restore failed — regenerate.

## What Stage 2 CAN do (paint freedom)

- Choose final token values (within the Stage-1 token draft's structure)
- Pick typography refinements (font weights, letter-spacing)
- Add micro-interactions (button 8 states, hover scales, drawer slides)
- Add motion (within motion-discipline rules)
- Add final copy (within the Stage-1 wording formulas)
- Add accessibility polish (aria-labels, focus management, keyboard shortcuts)

These are the paint. They don't change structure.

## What Stage 2 CANNOT do (structure prison)

- Add a block that wasn't in any Stage-1 draft (no surprise charts, calendars, AI-summary panels)
- Remove a block that was in a Stage-1 draft
- Change a container (e.g. drawer → modal) without a Stage-1 tradeoff note justifying it
- Add a state that wasn't in the Stage-1 state matrix
- Skip a state that was in the Stage-1 state matrix
- Change the IA (e.g. move nav from sidebar to top bar)
- Add a feature that's in the Task Card's non-goals
- Skip a permission rule from the object-state-permission matrix

Any of these = drift = regenerate.

## The drift detector

Symptoms that Stage 2 has drifted from Stage 1:

| Symptom | What it means | Fix |
| --- | --- | --- |
| A block appears with no Stage-1 source | AI invented it | remove, or regenerate |
| A state is missing | AI skipped the hard part | add it from the matrix |
| A container changed | AI "improved" the IA | revert to Stage-1 choice |
| A non-goal appeared | AI added a feature | remove |
| Permission rule ignored | viewer can edit when they shouldn't | enforce from matrix |
| Button has 3 states instead of 8 | AI defaulted to plastic | restore all 8 |

When you detect drift, name it explicitly: **"Stage 2 drifted from Stage 1: [specific drift]. Regenerating 1:1."**

## The handoff QA (before declaring done)

```text
FIDELITY QA
===========
1. Every Stage-1 block has a Stage-2 implementation? [yes/no]
2. Every Stage-1 state is implemented? [yes/no]
3. Every object-state-permission cell is enforced? [yes/no]
4. Every container choice preserved? [yes/no]
5. Every Task Card non-goal absent? [yes/no]
6. No drift (no added/removed/moved blocks)? [yes/no]

If any answer is "no", the restore is incomplete — do not ship.
```

## Why this contract exists

Article line 2099: **"AI 很爱加戏,它觉得多就是好."** Without the contract, Stage 2 will add features (charts! calendars! AI-summary!) because more feels like more. With the contract, Stage 2 is forced to faithfully restore what Stage 1 decided, and the five-layer discipline survives into the final UI.

The contract is what makes this skill different from "AI UI generator". A generator generates; this skill restores.
