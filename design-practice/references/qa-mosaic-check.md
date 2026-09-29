# QA — Mosaic Coverage Check (did all five layers get a draft?)

> This is the structural integrity check for Stage 1. The Five-Layer Blade promises skeleton, not just skin. This check verifies the skeleton is actually there.

## Why

Article line 3253: **"你看到的是皮肤,不是骨架."** A Stage-1 run can look productive (8 drafts!) and still be skin-without-skeleton if all 8 are Type B structure drafts with zero Type A depth drafts. The mosaic check catches that.

## The five-layer coverage table

Every Stage-1 run emits this table as part of its output:

```text
FIVE-LAYER COVERAGE
===================
① Task       → covered by: [draft name(s)] or NONE
② Structure  → covered by: [draft name(s)] or NONE
③ State      → covered by: [draft name(s)] or NONE
④ System     → covered by: [draft name(s)] or NONE
⑤ Tradeoff   → covered by: [every draft's tradeoff note] or NONE
```

## Pass criterion

**All five layers must have at least one draft.** No exceptions.

- ① Task covered + ②③④⑤ covered → **PASS**
- Any layer = NONE → **FAIL — add a draft for that layer**

## Minimum per layer

| Layer | Minimum |
| --- | --- |
| ① Task | 1 task-flow draft (Mermaid + Markdown) |
| ② Structure | 3 IA variants (Type B, genuine differences) |
| ③ State | 1 state-matrix draft (8×4 matrix) + 1 object-state-permission draft (mandatory) |
| ④ System | 1 system draft (token three layers + component inventory) |
| ⑤ Tradeoff | every draft has a tradeoff note attached |

Layer ③ is double-weighted: state-matrix AND object-state-permission are both required. Skipping object-state-permission is the single most common skeleton-gap.

## The common failure: all-Type-B runs

```text
FAILING RUN EXAMPLE
===================
drafts: B1 sidebar+drawer, B2 kanban, B3 inline, B4 two-pane, B5 card-grid, B6 timeline, B7 calendar, B8 graph

FIVE-LAYER COVERAGE:
① Task       → NONE  ✗
② Structure  → covered by B1-B8 ✓
③ State      → NONE  ✗
④ System     → NONE  ✗
⑤ Tradeoff   → covered (each B has a note) ✓

VERDICT: FAIL — three layers missing. This is 8 skins, no skeleton. Add Type A drafts for ①③④.
```

The fix: cut 3-4 Type B drafts, add Type A drafts (task-flow, state-matrix, object-state-permission, system). Aim for 5-8 total with both types.

## The object-state-permission mandatory rule

Layer ③ requires BOTH:
- a state-matrix draft (loading / empty-3 / error / permission / offline wireframes + 8×4 matrix)
- an object-state-permission draft (object lifecycle + role × state × action matrix)

The object-state-permission draft is **the single hardest deep layer** (article line 611). It's the skeleton under the skin. A run without it has failed even if the other layers are covered.

## The tradeoff coverage rule

Layer ⑤ (Tradeoff) is covered by the tradeoff NOTES attached to every other draft. If any draft is missing its tradeoff note, layer ⑤ is partially uncovered — fail.

## The mosaic assembly

After coverage passes, the run must also emit the **mosaic view**: which drafts combine into a complete product, which are either/or alternatives.

```text
MOSAIC VIEW
===========
combines into product (all needed):
  - A1 task-flow          (the spine)
  - A3 object-state-perm  (the skeleton)
  - A2 state-matrix       (the nervous system)
  - A4 system             (the skin consistency)
  + one of: B1 / B2 / B4  (the body shape — user picks)

either/or alternatives (pick one):
  - B1 sidebar+drawer  vs  B4 two-pane  (both preserve context; pick by density need)
  - B2 kanban          vs  B3 inline    (pick by status-axis vs time-axis)

non-combining (standalone, not for this product):
  - B5 card-grid  (unfit for task management — would fit an asset library)
  - B6 timeline   (unfit — would fit a scheduling product)
```

If the mosaic view can't say which drafts combine vs which are either/or, the drafts aren't differentiated enough — back to divergence.

## Verdict

After the mosaic check:

- **PASS** — all five layers covered, mosaic view clear, ready for Stage 2
- **FAIL — missing layers** — add Type A drafts for uncovered layers
- **FAIL — no object-state-permission** — add it, no excuses
- **FAIL — no mosaic view** — drafts not differentiated, re-diverge
- **FAIL — all-Type-B** — skin without skeleton, restructure the run

## Failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| All-Type-B run | 8 skins no skeleton | cut B, add A (task-flow, state-matrix, object-state-permission, system) |
| Missing object-state-permission | no role × state matrix | mandatory — add it |
| Tradeoff notes missing | layer ⑤ uncovered | every draft needs a note |
| No mosaic view | can't say what combines | drafts not differentiated, re-diverge |
| Layer ④ (System) skipped | "we'll do tokens later" | system draft is part of skeleton, do it now |
