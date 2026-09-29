---
type: reference
created: 2026-06-27
priority: P0
pairs-with: tooling/render-critique.mjs · references/stage3-render-refine-loop.md · references/craft-details-invisible.md
---

# The 10-Dimension Rubric — the scoring spine of the render→critique→refine loop

> This is the measurable quality bar that Stage 3 runs on every rendered page. The harness (`tooling/render-critique.mjs`) auto-scores the objective dims from real signals and **refuses to fake** the three judgment dims — it hands the agent the screenshots and the agent scores those by *looking*. No competitor formalizes this; it is the moat. The gate stops "bad"; the rubric drives "great."

## The two-tier design (why it's trustworthy)
- **Auto-scored** (harness, objective): contrast/a11y, color/token, state coverage, motion, performance, responsive, spacing. Backed by axe-core, computed CSS, multi-viewport render.
- **Visual-judgment** (agent looking at screenshots): hierarchy, typography, restraint/originality. The harness emits the screenshots + measured signals and marks these `needs_visual_judgment` — it never invents a number it can't defend.

## The Gate (binary — must pass before scoring "great")
A page **FAILS** the gate if ANY of: console errors present · any critical/serious axe violation · the page pans horizontally at 390×844 · **content clipped past the viewport, or a fixed/min-width grid that doesn't adapt at 390/360** (the `overflow:hidden`-masked fixed desktop grid — render-critique's real mobile audit catches this even when there's no page-scroll). Gate failures are not "low scores" — they are "not shippable." Fix them first, every iteration.

## The 10 dimensions

| # | Dimension | Tier | 0–2 (broken) | 3 (correct) | 4–5 (crafted → SSS) |
|---|---|---|---|---|---|
| 1 | **Hierarchy 视觉层级** | visual | everything same weight; no focal point | clear primary action | one unmistakable focal anchor in 1s; 5-3-2 weight; eye lands right |
| 2 | **Spacing & rhythm 间距节奏** | auto | random off-grid values | mostly on 4/8 | strict 4/8 rhythm; optical alignment; confident whitespace |
| 3 | **Typography 字体** | visual | default Inter-mush; size-only hierarchy | real scale + 2-3 weights | characterful face; sans+mono pair; tracking-by-size; tabular nums |
| 4 | **Contrast & a11y 对比可访问性** | auto | axe serious; faint text <4.5:1; modal w/o focus-trap | AA passes; focus-visible; keyboard-reachable | AA+ incl. tiny labels; APG patterns (dialog trap/Esc/return, tabs roving); ARIA complete; reduced-motion — see `a11y-depth.md` + behavior-audit `a11yDepth` |
| 5 | **Color & token discipline 色彩token** | auto | hardcoded; indigo-default; rainbow | tokens + ≤5 colors | one owned accent in ≤3 roles; semantic tiers; per-color tuning |
| 6 | **State coverage 状态完整** | auto | happy-path only | hover/focus/active + 1-2 data states | all of hover/focus/active/disabled/loading/empty/error/permission designed |
| 7 | **Motion 动效** | auto | layout-prop animation; >500ms feedback; no reduced-motion | ease-out, composited | real curves; one entrance moment; interruptible; reduced-motion |
| 8 | **Performance 性能** | auto | layout shift; bloated DOM | CLS≈0 | optimistic/skeleton; no shift; lean DOM; LCP fast |
| 9 | **Responsive integrity 响应式** | auto | content clips at 390/360 (fixed grid masked by overflow:hidden); page pans sideways | no clipping; IA reflows; ≥24px touch | real adaptation per breakpoint (nav→drawer, table→labeled-cards), ≥44px touch, fluid `clamp()` type, container queries — not just reflow; see `responsive-adaptive-mastery.md` |
| 10 | **Restraint & originality 克制原创** | visual | AI-median; card-tiling; could-remove-half | clean, no slop | a point of view + one signature; anti-median; nothing removable |

## The loop protocol (how the rubric is used)
1. Generate the page (grounded in `tokens/00-token-synthesis.md` + the chosen direction from `world-class-teardowns/00-moodboard-tokens.md`).
2. Run `node tooling/render-critique.mjs <file>` → `report.json` + `report.md` + 3 screenshots.
3. If the **gate FAILS**, fix those first (they're named in the report).
4. **LOOK at the 3 screenshots** and score dims 1/3/10 (the harness won't).
5. Take the **single weakest dimension** as the work item — fix only it.
6. Re-run. Repeat until **all 10 ≥ 4** OR a hard cap of **4 iterations** (then deliver best-so-far + flag remaining gaps).
7. Once all dims ≥4, run the **Compound-Craft Audit** in `craft-details-invisible.md` — each unticked box is a 0.1 between 4/5 and SSS.

## Honest-scoring rules (anti-self-deception)
- Never accept first output. The weakest dim is always the next job.
- Never score a `needs_visual_judgment` dim from code — look at the pixels (zoom in; see `[[zoom-in-scrutiny-and-imagegen-ui-rule]]`).
- Genre bar: utility tools → dim 10 = *invisible perfection* (no wow moment). Brand/landing → dim 10 = *one composed moment* + the craft layer.
- Responsive (dim 9) is judged against **intended reach**: landing / consumer = mobile-first mandatory; desktop power-tool (IDE / dense dashboard) = a `min-width` + graceful "built for desktop" degradation is acceptable — but **silent clipping at 360px is never a design decision, it's an untested page**. See `responsive-adaptive-mastery.md`.
- If the harness signal looks wrong (e.g. spacing over-counts computed sub-pixels), say so and fix the harness — don't game the page to a false number.
