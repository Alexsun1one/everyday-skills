# Stage 1 — Divergence (5-8 drafts, Type A + Type B, not reskins)

> A run with 8 drafts that all differ only in paint is a failed run. This file is how you avoid that.

## The rule

Every Stage-1 run emits **5-8 drafts**, and they MUST include BOTH:

- **≥2 Type A drafts** (depth drafts) — dig one layer deep. At least one MUST be the object-state-permission draft.
- **3-5 Type B drafts** (structure drafts) — genuine IA differences, not reskins.

A run with zero Type-A drafts is skin without skeleton — reject and regenerate. A run with 8 Type-B drafts and no Type-A is eight skins, no skeleton.

## Type A — depth drafts (dig one layer)

These don't compete with each other on structure; each one digs a different layer.

### A1. Task-flow draft (layer ①)
Only the main flow. Mermaid flowchart. Nodes = steps, edges = handoffs, branches = the few real decision points. Side-channels for recoveries (back, cancel, save-draft).

### A2. State-matrix draft (layer ③)
Only the breaking moments. One wireframe per breaking state (loading / empty-3-kind / error / permission / offline). Plus the 8-state × 4-column matrix for the core component.

### A3. Object-state-permission draft (layer ③, deep) — MANDATORY
The data lifecycle + permission matrix. See `stage1-object-state-permission.md`. **At least one of these per run. No exceptions.**

### A4. System draft (layer ④)
Token three layers + component inventory + reusable patterns. Markdown doc.

Pick at least 2 of {A1, A2, A3, A4}. A3 is mandatory, so really you pick 1 more from {A1, A2, A4}.

## Type B — structure drafts (real IA difference)

These compete on structure. Each must differ in IA, not in paint. The article's line 1483 warns: AI loves to "全摊开" — put everything on one page. Type B drafts force genuine container and grouping choices.

### B1. Sidebar + list + drawer
The classic productivity layout. List is the main real estate; detail opens in a right drawer that preserves list context.

### B2. Kanban + click-expand
Columns by status; click a card to expand inline or open a popover. Best for status-flow work.

### B3. Single-column + inline-edit
A feed-like list where each row expands inline to edit. Best for short items, mobile-first.

### B4. Two-pane constant (master-detail)
List on left always visible, detail on right always visible. Best for dense keyboard-driven work (think Mail.app).

### B5. Card grid + modal
Cards in a grid; click opens a modal. Best for visual items (images, assets) where scan-ability matters.

### B6. (your own variant)
Invent a 6th if the product calls for it — a timeline, a calendar, a graph canvas. But justify it with the task, not novelty.

Pick 3-5 of {B1..B6}. Don't pick two that are essentially the same (e.g. B1 sidebar+drawer vs B4 two-pane — pick one, they overlap).

## The one-sentence difference test

For every Type B draft, write one sentence: **"This differs from the others because [structural reason]."**

- Good: "B2 kanban differs because it makes status the primary axis; the others make time or assignee primary."
- Good: "B4 two-pane differs because both panes are always visible; the others hide detail until clicked."
- Bad: "B1 is cleaner." — that's paint, not structure.
- Bad: "B3 is more modern." — that's fashion, not structure.

If you can't write the sentence, the draft is a reskin — cut it and diverge again.

## How to diverge (anti-template)

Article line 1485: **"页面平铺的形式主义:不动脑子,一摊了之."** The cure is to think about the TASK, not the layout menu:

1. What's the user's primary axis? (time / status / assignee / project / priority) → make THAT the layout axis.
2. What context must stay visible during the main action? → that decides drawer vs page vs two-pane.
3. What's the density need? (scan 50 items vs edit 1 deeply) → that decides list vs card vs two-pane.
4. What's the recovery path? (where does cancel / undo / draft-save go) → that's where AI skips.

Diverge from the task, not from a layout gallery. Two drafts diverged from the task will genuinely differ; two drafts picked from a gallery will be reskins.

## Failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| All-Type-B run | 8 pretty layouts, no states / no permissions / no object model | force ≥2 Type A, regenerate |
| Reskin parade | B1-B5 differ only in color/spacing | one-sentence test; cut and re-diverge from task |
| Object-state-permission missing | no A3 draft | mandatory — add it, no excuses |
| "Invented" variants with no task reason | B6 is a graph because it looks cool | justify from task or cut |
| Too many variants (>8) | decision paralysis | cap at 8; 5-8 is the sweet spot |

## Output

After divergence, list the drafts as:

```text
drafts:
  A3 (mandatory): object-state-permission — [object name]
  A?: [task-flow / state-matrix / system] — [one-line topic]
  B1: sidebar+list+drawer — [one-line structural reason]
  B2: kanban — [one-line structural reason]
  B?: ...
total: [N] drafts, [M] Type A + [K] Type B
```

This list feeds the Mosaic view (`SKILL.md` D6) — which drafts combine into a product, which are either/or.
