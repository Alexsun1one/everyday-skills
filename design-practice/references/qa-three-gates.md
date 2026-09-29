# QA — Three Gates (design / engineering / product)

> Article line 2314-2350. Every Stage-2 output passes three gates before it ships. No gate, no ship.

## Why three gates

A single "looks good" check mixes concerns and misses things. Splitting into three forces each concern to be examined on its own terms:

- **Design gate** — is it usable and visually disciplined?
- **Engineering gate** — is it maintainable and accessible?
- **Product gate** — does it serve the task and respect non-goals?

Each gate has its own checklist and its own failure modes. Failing one gate doesn't fail the others — you fix that gate's issues and re-check.

## Gate 1 — Design

Asks: did it keep visual and interaction discipline?

```text
DESIGN GATE
===========
[ ] One primary action per screen? (no two blue buttons)
[ ] Uses design tokens (no hardcoded colors / spacing / fonts)?
[ ] Information hierarchy clear? (user knows what to look at first)
[ ] Container choices correct? (drawer for sub-task, modal for interrupt)
[ ] All 8 button states present?
[ ] Empty state is three-classified (not "暂无数据")?
[ ] Errors are in-place (not global toasts)?
[ ] Focus rings present and visible?
[ ] Loading uses skeletons (not bare spinners)?
[ ] Typography scale consistent (no orphan font sizes)?
```

Failure examples:
- two primary buttons → IA unclear → fail design gate
- `style="color: #2563EB"` hardcoded → tokens skipped → fail
- "暂无数据" → empty state abuse → fail

## Gate 2 — Engineering

Asks: is it maintainable and accessible?

```text
ENGINEERING GATE
================
[ ] Components properly split (Button, Input, TaskList, Drawer, EmptyState, ErrorState, ...)?
[ ] State managed centrally (not scattered)?
[ ] No duplicate code / logic?
[ ] No hardcoded values (colors, spacing, copy strings)?
[ ] Error handling and retry reliable (drafts preserved)?
[ ] Keyboard accessible (Tab reaches everything, focus trap in modals/drawers)?
[ ] ARIA correct (aria-label on icon buttons, aria-busy on loading, aria-disabled)?
[ ] Semantic HTML (button for actions, a for navigation, not div for everything)?
[ ] prefers-reduced-motion respected?
[ ] Responsive (desktop primary, mobile folds correctly)?
[ ] Dark mode works via token swap (not a separate page)?
```

Failure examples:
- one giant component with all logic → fail
- `<div onClick>` for a button → fail semantic HTML
- icon button without aria-label → fail accessibility
- spinner that blocks the whole page → fail error handling

## Gate 3 — Product

Asks: does it serve the task and respect the non-goals?

```text
PRODUCT GATE
============
[ ] Main task can be completed start to finish?
[ ] User can recover from each breaking state (loading / empty / error / permission / offline)?
[ ] Forms preserve user input on failure?
[ ] Object-state-permission matrix enforced (no 403 on visible buttons)?
[ ] No features beyond MVP (non-goals from Task Card absent)?
[ ] Mobile layout works (or explicitly deferred)?
[ ] Edge data handled (long text, empty fields, expired dates, special chars)?
[ ] Performance acceptable (skeleton under 100ms, no layout thrash)?
[ ] Copy is human (not "request failed", "operation invalid")?
[ ] Sense of place (user knows where they are in the app)?
```

Failure examples:
- can't complete the main task → fail (critical)
- viewer sees a Create button that 403s → fail permission
- AI added a Gantt chart that wasn't in MVP → fail non-goals
- "操作失败" generic toast → fail copy

## How the gates interact

```
Stage 2 output
     ↓
DESIGN gate ── fail ──→ fix design issues, regenerate
     ↓ pass
ENGINEERING gate ── fail ──→ fix eng issues, regenerate
     ↓ pass
PRODUCT gate ── fail ──→ fix product issues, regenerate
     ↓ pass
SHIP
```

You can fail multiple gates in one pass — list all failures, fix them together, re-run all three. Don't ship until all three pass.

## The "looks done" trap

Article line 2111: **"Agent 写完代码,经常会说'已完成'. 不要被这句话安慰. 完成不是它说了算,是验收清单说了算."**

The three gates are the antidote. "Done" only counts when all three gates pass with checkmarks on every line.

## Failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| Skipped gates | "looks done" | all three gates mandatory, no exceptions |
| Mixed concerns | design issues hides eng issues | each gate is independent |
| Rubber-stamp | all gates pass without checking | every line must be checked, not just signed off |
| Ship on first fail | one gate fails, ship anyway | all three must pass |
