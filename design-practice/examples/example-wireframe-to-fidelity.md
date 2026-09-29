# Example — Wireframe to Fidelity (Stage 1 → Stage 2 restore)

> A short example showing the 1:1 restore contract in action. The same Stage-1 draft, restored hi-fi, with the fidelity diff table proving no drift.

## Stage 1 — Low-fi draft (B1 sidebar+list+drawer)

```text
┌─────────────────────────────────────────────────────────────┐
│ TOPBAR  [logo]  search            [notif] [avatar ▾]        │
├──────────┬──────────────────────────────────┬────────────────┤
│ SIDEBAR  │ MAIN: today's tasks             │ DRAWER (opt)   │
│          │ ┌────────────────────────────┐   │ task detail    │
│ ▸ Today  │ │ □ Fix login bug   @alex ⚠│   │                │
│ ▸ Week   │ │   due today · blocked      │   │ assignee:      │
│ ▸ Proj…  │ └────────────────────────────┘   │ [@alex ▾]      │
│          │ ┌────────────────────────────┐   │                │
│          │ │ □ Design review  @sam      │   │ status: active │
│          │ │   due today                │   │                │
│          │ └────────────────────────────┘   │ [Save] primary │
│          │                                  │                │
│          │ [＋ New task]   primary          │                │
└──────────┴──────────────────────────────────┴────────────────┘

STATES (from A2 state-matrix draft):
- loading: row skeletons in MAIN
- empty-initial: illustration + "还没有任务" + [Create]
- empty-filter: "没有符合筛选" + [Clear filters]
- empty-permission: "你没有权限" + [Request access]
- error: inline error in MAIN + retry, filter preserved
- drawer open: slides from right, focus trap, ESC closes, focus returns to row

PERMISSION (from A3 matrix):
- viewer: [+ New] disabled + tooltip "need editor role"
- viewer: [Save] in drawer not shown
- editor: [+ New] enabled, [Save] enabled, delete hidden
- admin: all enabled
```

## Stage 2 — Hi-fi restore

The restored UI uses the same blocks, same containers, same states, same permission rules — only the paint changes (tokens, typography, motion).

```tsx
// App shell — 1:1 with Stage 1 ASCII
function TaskApp() {
  return (
    <div className="grid grid-cols-[200px_1fr_400px] h-screen">
      <Sidebar />          {/* Stage 1: SIDEBAR */}
      <TaskList />         {/* Stage 1: MAIN */}
      <TaskDrawer />       {/* Stage 1: DRAWER */}
    </div>
  );
}

function TaskList() {
  const { tasks, status, error } = useTasks();

  return (
    <main className="bg-[var(--color-bg-canvas)]">
      <TopBar />                                  {/* Stage 1: TOPBAR */}
      {status === 'loading' && <ListSkeleton />}  {/* Stage 1: loading state */}
      {status === 'error' && (                    {/* Stage 1: error state */}
        <ErrorState
          message="Couldn't load tasks."
          onRetry={refetch}
          filtersPreserved
        />
      )}
      {status === 'empty-initial' && (            {/* Stage 1: empty-initial */}
        <EmptyState
          kind="initial"
          value="还没有任务. 创建第一个任务,开始跟踪项目进展."
          cta={<Button variant="primary">+ Create task</Button>}
        />
      )}
      {status === 'empty-filter' && (             {/* Stage 1: empty-filter */}
        <EmptyState
          kind="filter"
          message="没有符合当前筛选条件的任务."
          cta={<Button variant="secondary">Clear filters</Button>}
        />
      )}
      {status === 'empty-permission' && (         {/* Stage 1: empty-permission */}
        <EmptyState
          kind="permission"
          message="你暂时没有权限查看这些任务."
          cta={<Button variant="secondary">Request access</Button>}
        />
      )}
      {status === 'success' && (
        <ul>
          {tasks.map(t => <TaskRow key={t.id} task={t} />)}
        </ul>
      )}
      <Button variant="primary" disabled={!canCreate} tooltip={!canCreate && 'Need editor role'}>
        + New task
      </Button>
    </main>
  );
}

function TaskDrawer() {
  // Stage 1: drawer with focus trap, ESC, focus return
  return (
    <Drawer side="right" aria-modal="true">
      <DrawerHeader onClose={closeDrawer} />
      <TaskDetail />
      <SaveButton onSave={saveTask} />  {/* 8 states from A2 */}
    </Drawer>
  );
}
```

## Fidelity diff table

```text
FIDELITY DIFF — B1 sidebar+list+drawer
=======================================
BLOCKS:
| Stage 1 (ASCII)        | Stage 2 (component)         | Verdict |
|------------------------|-----------------------------|---------|
| TOPBAR                 | <TopBar>                    | MATCH   |
| SIDEBAR                | <Sidebar>                   | MATCH   |
| MAIN task list         | <TaskList>                  | MATCH   |
| DRAWER task detail     | <TaskDrawer>                | MATCH   |
| [+ New task] primary   | <Button variant="primary">  | MATCH   |
| [Save] primary (drawer)| <SaveButton>                | MATCH   |

STATES (from A2):
| Stage 1 state          | Stage 2 implementation              | Verdict |
|------------------------|-------------------------------------|---------|
| loading                | <ListSkeleton>                      | MATCH   |
| empty-initial          | <EmptyState kind="initial">         | MATCH   |
| empty-filter           | <EmptyState kind="filter">          | MATCH   |
| empty-permission       | <EmptyState kind="permission">      | MATCH   |
| error (inline + retry) | <ErrorState filtersPreserved>       | MATCH   |
| drawer (focus trap)    | <Drawer aria-modal focus-trap>      | MATCH   |

PERMISSION (from A3):
| Cell (role × action)        | Stage 2 enforcement            | Verdict |
|------------------------------|--------------------------------|---------|
| viewer × create              | button disabled + tooltip      | MATCH   |
| viewer × save                | save button not rendered       | MATCH   |
| editor × create              | button enabled                 | MATCH   |
| editor × delete              | delete hidden                  | MATCH   |
| admin × all                  | all enabled                    | MATCH   |

CONTAINERS (from B1 draft):
| Stage 1 container | Stage 2 implementation         | Verdict |
|-------------------|--------------------------------|---------|
| page (main shell) | full-screen grid route         | MATCH   |
| drawer (detail)   | <Drawer side="right">          | MATCH   |
| (no modal here)   | (no modal here)                | MATCH   |

NON-GOALS (from Task Card):
| Non-goal             | Present in Stage 2? | Verdict |
|----------------------|---------------------|---------|
| no Gantt chart       | absent              | OK ✓    |
| no calendar view     | absent              | OK ✓    |
| no time-tracking     | absent              | OK ✓    |
| no mobile this round | desktop-only grid   | OK ✓    |

VERDICT: SHIPPABLE — all MATCH / OK, no ADDED / MISSING / DRIFT / FAIL.
```

## What this example proves

The restore contract isn't a vibe — it's a diffable table. Every Stage-1 element maps to exactly one Stage-2 implementation. Nothing was added (no charts, no AI-summary). Nothing was skipped (all 5 data states implemented). Nothing drifted (drawer is still a drawer, not a page).

This is what makes the skill different from "AI UI generator". A generator generates. This skill restores.

## The "what if Stage 2 wants to add something" case

Suppose during restore, the developer thinks "a small analytics widget in the sidebar would be nice."

**Wrong**: add it in Stage 2. → drift, fidelity FAIL.

**Right**: go back to Stage 1, add an A4-system draft describing the widget, get the user to confirm it's in scope (not a non-goal), THEN restore. The widget now has a Stage-1 source and the fidelity holds.

Stage 2 never decides product scope. That's Stage 1's job.
