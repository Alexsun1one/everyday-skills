# Stage 1 — Low-Fidelity Iron Rule

> Stage 1 is low-fi. No color, no gradient, no shadow, no real data. Any "prettiness" in Stage 1 is a failure signal — AI is skipping ahead to Stage 2. This file is the rule and the enforcement.

## The rule

Article line 4008: **"画低保真线框:只画盒子,不急着上颜色."**
Article line 7462: **"不要直接给高保真视觉,先把任务、信息、行动说清楚."**
Article line 5497: **"低保真结构 → 视觉系统 → 组件状态 → 真实测试"** — low-fi comes FIRST, explicitly before the visual system.

Stage 1 = low-fi only. Stage 2 = hi-fi restore. Skipping Stage 1 to draw a hi-fi UI is the cardinal failure of this skill.

## What "low-fi" means here

### Allowed
- ASCII wireframes (box-drawing chars, no color)
- Mermaid diagrams (default theme)
- Grayscale image-wireframes (NO color, NO gradient, NO shadow — see `stage1-output-formats.md` Format 3)
- Markdown tables (blocks, states, permissions)
- Placeholder content ("Task title", "assignee", "lorem ipsum")
- Annotations (small labels pointing to blocks)

### Forbidden
- Any color other than grayscale (no hue, no saturation)
- Any gradient
- Any shadow / depth / bevel / glass
- Real photos, real logos, real brand assets
- Real data (real names, real numbers from production)
- Polished, "final-looking" rendering
- Any hint of "this is done"

## Why so strict

Three reasons, all from the article:

1. **Prettiness lies.** A beautiful hi-fi UI hides missing states, missing permissions, missing object models. Low-fi forces the structure to stand on its own — if it works in grayscale wireframe, it works; if it only works in color, the color is hiding a flaw.

2. **AI skips ahead when allowed.** The moment AI is allowed to render hi-fi in Stage 1, it will — because hi-fi looks like progress. But hi-fi without the five-layer skeleton is the exact plastic UI this skill refuses.

3. **Stage 2 needs a target.** Stage 2 restores against Stage 1. If Stage 1 is already hi-fi, there's nothing to restore — Stage 2 just copies, and the five-layer discipline is lost.

## The grayscale image-wireframe contract

When using an image model for Format 3 (grayscale wireframe), the prompt MUST include:

```text
style:
- grayscale only, NO color, NO gradient, NO shadow, NO real photos
- hand-drawn wireframe feel, thin gray lines, neutral gray fills
- placeholder content, no real brand
- annotations allowed (small labels pointing to blocks)

do NOT:
- add color, gradient, or shadow
- make it look polished or final
- include real data, real logos, real people
- add charts, calendars, or features not in the layout description
```

If the image model returns something colorful or polished, REJECT it and regenerate with stronger negatives. Don't accept "almost grayscale" — that's the thin end of the wedge.

## The "AI skipped ahead" detector

Symptoms that AI is skipping Stage 1 and jumping to Stage 2:

| Symptom | What it means | Fix |
| --- | --- | --- |
| Draft has color | AI rendered hi-fi | reject, regenerate with grayscale-only |
| Draft has real-looking data | AI invented polished content | reject, regenerate with placeholders |
| Draft has shadows / depth | AI made it look "done" | reject, regenerate flat |
| Draft is one polished screen, no states | AI drew a screenshot, not a draft | reject, regenerate with state variants |
| Draft has features not in Task Card | AI added charts / calendars / AI-summary | reject, enforce non-goals |

When you detect any of these, call it out explicitly in the output: **"This draft skipped Stage 1 and rendered as Stage 2 — rejected. Regenerating low-fi."**

## The Stage 1 → Stage 2 handoff

Stage 1 hands Stage 2 a stack of low-fi drafts + the five-layer coverage. Stage 2's job is to restore them hi-fi, 1:1 against the drafts (see `stage2-fidelity-restore.md`).

The handoff contract:

```text
Stage 1 output:
  - 5-8 low-fi drafts (no color, no gradient, no shadow)
  - each draft: layer-relevant formats + state variants + tradeoff note
  - mosaic view (which combine, which either/or)
  - five-layer coverage table (every layer covered)
  - recommendation (combination + reason)

Stage 2 input (the chosen combination):
  - the drafts the user picked
  - the five-layer coverage (must be complete)
  - the Task Card (source of truth for non-goals)
```

Stage 2 cannot add features that aren't in the Stage 1 drafts. Stage 2 cannot change the IA of a Stage 1 draft. Stage 2's freedom is in paint (tokens, typography, micro-interactions), not structure.

## Enforcement

This rule is a gate, not a guideline. If Stage 1 output violates it:

1. The output is rejected.
2. The failure is named ("skipped Stage 1, rendered hi-fi").
3. The output is regenerated low-fi.

There is no "pretty enough to keep" exception. A pretty Stage 1 draft is a failed Stage 1 draft.
