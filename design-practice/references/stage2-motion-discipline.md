# Stage 2 — Motion Discipline (time, easing, direction, reduced-motion)

> Article line 1398: **"现实世界里的动作,很少突然开始、突然停止. 抽屉滑出,菜单展开,卡片进入,都会有加速、减速. 这就是缓动."** Motion is grammar, not fireworks.

## The motion five-question (article line 515)

Before adding ANY motion, answer:

1. **Why does it move?** (meaning: orientation, feedback, state-change, hierarchy — not decoration)
2. **What moves?** (the whole element, a part, the bg — be specific)
3. **Where does it move from / to?** (direction must match spatial logic)
4. **How long?** (use tokens, don't invent durations)
5. **What if the user hates motion?** (reduced-motion fallback)

If you can't answer #1 with a meaning beyond "it looks nice", don't add the motion.

## Duration tokens (from `stage2-design-tokens.md`)

| Token | Duration | Use for |
| --- | --- | --- |
| `duration.fast` | 100ms | micro: hover, press, toggle, color shift |
| `duration.normal` | 200ms | small: tooltip, popover, toast, badge change |
| `duration.slow` | 300ms | medium: drawer, modal, expand-collapse, page transition |

Rule of thumb (article line 1433):
- small things move fast (button press: 100ms)
- large things move slower (drawer: 240-300ms)
- frequent actions move fast (toggle: 100ms)
- rare transitions can be slower (page change: 300ms)
- **feedback must be fast** (under 100ms feels instant)

## Easing tokens

| Token | Curve | Use for |
| --- | --- | --- |
| `easing.ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | **entrance** — things appearing (drawer in, modal in, toast in). Fast start, slow end. |
| `easing.ease-in` | `cubic-bezier(0.7, 0, 0.84, 0)` | **exit** — things disappearing (drawer out, modal out). Slow start, fast end. |
| `easing.standard` | `cubic-bezier(0.4, 0, 0.2, 1)` | **general** — most transitions. |
| `linear` | `linear` | **only** for continuous loops (spinner, progress bar). Never for state changes. |

Article line 1400: **"我们不用把名词背得很玄."** Don't reach for fancy curves; these four cover 99% of cases.

## Direction (spatial logic)

Motion direction must match the user's mental model of space:

| Element | Enters from | Exits to | Why |
| --- | --- | --- | --- |
| right drawer | right edge, sliding left | slides right, off-screen | it "lives" on the right |
| modal | center, scale 0.95 → 1.0 + fade | scale 1.0 → 0.95 + fade | it "lives" in center |
| tooltip | the trigger, scale 0.9 → 1.0 + fade | reverse | it "lives" on the trigger |
| toast | top-right, sliding down + fade | slides up + fade | it "lives" in top-right |
| dropdown | the trigger, expanding down | collapse up | it "lives" below the trigger |
| list item (new) | top of list, slide down + fade | (n/a) | new items "arrive" |
| list item (deleted) | (n/a) | collapse height + fade | deleted items "leave" |

**Wrong**: a drawer that fades in without sliding. A modal that slides from the left. A tooltip that scales up from center. These break spatial logic and feel wrong even if the user can't say why.

## What moves and what stays

- **Move the thing that changed**, not the whole page.
- A new list item slides in; the rest of the list stays put.
- A drawer slides in; the page underneath stays put.
- Don't trigger layout shifts on unrelated elements — that's jank.

## Reduced-motion (article line 1430)

Some users get motion-sick or have vestibular disorders. `prefers-reduced-motion` is non-negotiable:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

In reduced-motion mode:
- drawers/modals/tooltips appear instantly (no slide)
- shakes and bounces become instant state changes
- progress bars still work (they convey real progress)
- spinner still spins (it's a continuous loop, not a transition)

## Motion DON'Ts

- **Don't animate everything.** Article line 1430: motion should be rare and meaningful. A page where every element bounces on load is exhausting.
- **Don't use `linear` for state changes.** It feels mechanical.
- **Don't make important actions slow.** A save button that takes 500ms to respond feels broken.
- **Don't parallax.** It's a 2015 fad that hurts performance and accessibility.
- **Don't auto-play carousels.** They pull attention from the user's task.
- **Don't animate on scroll-trigger for everything.** One or two reveal-on-scroll moments are fine; animating every section is noise.

## Failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| Everything moves | exhausting, can't focus | rare + meaningful; cut decorative motion |
| `linear` easing on state change | robotic | use ease-out / standard |
| Wrong direction | drawer fades instead of slides | match spatial logic |
| No reduced-motion | accessibility fail | `@media (prefers-reduced-motion)` mandatory |
| Slow feedback | button takes 500ms to react | feedback under 100ms |
| Parallax / auto-carousel | 2015 fad, hurts perf | cut |
