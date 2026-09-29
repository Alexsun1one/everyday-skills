---
type: reference
created: 2026-06-28
priority: P0
role: the north-star — the total definition of "world-class" this skill is accountable to
---

# Quality Landscape — the total map of what "world-class" is made of

> This is the skill's north star: the **complete** set of dimensions a world-class web UI must satisfy — not the few a user happens to name. The rubric (`rubric-10d.md`), the behavior audit, `craft-details-invisible.md`, and `micro-interactions-liveness.md` are the *operational tools*; this file is the *standard they serve*. Authored to be exhaustive on purpose: if it's not here, it's a gap to add.
>
> Each dimension has a **verdict method**: `[auto]` the harness/behavior-audit can check it · `[see]` needs looking at a render · `[drive]` needs driving the live UI / recording motion · `[reason]` a judgment about fit. Most failures hide in the dimensions a static screenshot can't show — which is why "可交付" = static gate **+** behavior gate **+** drive-verify, never just a pretty frame.

## A. Foundation — is it the right thing at all
1. **Intent & fit** `[reason]` — serves the real job + audience + tone; one primary action per screen; nothing present that shouldn't be. *Wrong target → precise execution of the wrong thing.*
2. **Information architecture** `[reason]` — content organized by the user's model; labels are theirs not the org's; navigation reveals a sense of place.
3. **Flow / 动线 integrity** `[drive][reason]` — every entry has an exit; no dead-ends; the path "ready→acting→done" is unbroken; the next step is always obvious; back/cancel/undo exist. *Verify by clicking through, not by looking.*

## B. Skeleton — what survives ugly reality
4. **State completeness** `[see][auto-partial]` — default / hover / focus / active / disabled / **loading / empty / error / permission / partial / overflow** all designed. Empty states guide; errors say what+why+how.
5. **Edge & bad-data robustness** `[drive][see]` — 0 / 1 / 200 items; 80-char names; huge numbers; null; no-permission; i18n/CJK; survives the data being ugly.
6. **Error recovery & resilience** `[drive]` — draft survives a failure; undo; retry; offline; validation at the right moment; nothing destructive without confirm.
7. **System & maintainability** `[auto]` — tokens not hardcoded; reusable components; consistency; no one-off hacks. The skeleton under the skin.

## C. Composition — the eye and the page
8. **Hierarchy & focus** `[see]` — one unmistakable focal point in 1s; 5-3-2 weight; attention is directed, not left to the user.
9. **Typography craft** `[see]` — characterful face (sans+mono pair; serif-display where editorial); real scale; tracking inversely to size; **tabular-nums** on aligned numbers; precise weights (510/590); optical alignment.
10. **Color & token discipline** `[auto][see]` — ONE owned accent in ≤3 roles (never indigo-default); semantic tiers; per-color optical-weight tuning; restrained palette.
11. **Spacing, grid & composition** `[auto][see]` — strict 4/8 rhythm; optical (not mathematical) centering; **anti-card-tiling** (bento / asymmetry / density-earned, not a 3-card grid); intentional negative space.
12. **Surface & depth** `[see]` — luminance stacking (canvas→rail→card each a step); top-edge highlights; layered tinted shadows; **light themes tinted-not-white-on-white**; never pure #000.

## D. Behavior — look ≠ works (the static harness is blind here)
13. **Behavioral reality** `[auto]` — every control actually does something; **no naked native controls** (unstyled select/checkbox/range); **no dead buttons** (click→no change). `behavior-audit.mjs`: nakedNative=0, liveRatio≥80%.
14. **Liveness & micro-interaction** `[auto-partial][drive]` — responds to **approach** (hover micro-feedback), **act** (press scale, focus glow), **wait** (skeleton sheen / 掠光 / gradient-text shimmer); one signature alive moment (cursor-spotlight). See `micro-interactions-liveness.md`.
15. **Motion discipline** `[auto-partial][drive]` — ease-out; feedback ≤200ms; transform/opacity only; interruptible; **prefers-reduced-motion** honored; never on keyboard-repeat; spatial origin (things grow from their trigger). 呼吸感 judged by **recording motion**, never a still.
16. **Keyboard & input ergonomics** `[drive]` — full keyboard reachability; shortcuts + ⌘K; focus management; focus-trap in modals; roving tabindex; Esc closes; visible focus path.

## E. Performance & reach
17. **Perceived + real performance** `[auto]` — optimistic UI; skeleton-not-spinner; instant feedback; **no layout shift** (CLS<0.1; web-font CLS killed via self-hosted + size-adjust); LCP<2.5s; INP<200ms; lean DOM.
18. **Responsive art direction** `[auto][see]` — per-breakpoint *reflow* (not scaling); fluid type (clamp); container queries; ≥44px touch targets; mobile-first composition; **no horizontal page overflow** (wide content scrolls in its own box). **Judged against intended reach**: landing/consumer = mobile-first mandatory; desktop power-tool = `min-width` + graceful "built for desktop" degradation OK — but **silent clipping is never acceptable**, only an intentional degraded state is.
19. **Loading & reveal choreography** `[drive]` — sequenced reveal, content-first; skeletons match final layout (no shift on swap); reveal-gating so content is visible without JS / under reduced-motion (no blank-on-capture); no flash-of-unstyled.

## F. Accessibility, voice & soul
20. **Accessibility depth** `[auto][drive]` — semantic landmarks (one main); correct heading order; complete ARIA (tablist/dialog/listbox/tree, aria-sort); **AA+ contrast incl. tiny labels**; not-color-only; screen-reader flow makes sense. (Beyond just "axe passes".)
21. **Content & copy craft** `[see][reason]` — real content (no lorem); microcopy; error wording (plain, actionable); empty-state guidance; **no engineering jargon in UI** (core/adapter/MCP), **no AI-narration** ("powered by", "why this works").
22. **Restraint, originality & product fiction** `[see][reason]` — a clear point of view + ONE signature; could-anything-be-removed; anti-median; not a literal clone; feels like a real shipped product with a believable world, not a demo.

---

## How the tools cover the landscape (and where the gaps are)
| Tool | Covers | 
|---|---|
| `render-critique.mjs` (static gate + 10-dim) | 4,7,8,9,10,11,12,17,18,20 — **§18 responsive is now a REAL mobile audit** (clipping past viewport / fixed-min-width / page-vs-contained-scroll / touch <24-44px / text <12px — no longer fooled by `overflow:hidden`); **§17 real CWV** (CLS/LCP/INP) |
| `behavior-audit.mjs` (drive) | 13, 14(hover), **16 (keyboard focus-visible + dialog focus-trap/Esc), 20 (a11yDepth ARIA semantics)** — dead-button test now excludes disabled/active/file-dialog false-positives |
| `drive.mjs` + motion recording | 3,14,15,16,19 — the felt/flow layer |
| `craft-details-invisible.md` | 9,11,12 compound craft (4/5→SSS) |
| `micro-interactions-liveness.md` | 14,15 the alive layer |
| **round-2 craft refs** | `responsive-adaptive-mastery`→18 · `a11y-depth`→16,20 · `performance-cwv-2026`→17 · `motion-choreography-2026`→14,15 · `why-ai-pages-still-feel-ai-2026`→1,22 (the AI-tell diagnosis + counter-moves) · `image-led-assembly`→the image-gen branch of Stage 2 |
| human/agent judgment | 1,2,5,6,21,22 — fit, resilience, voice, soul |

> **Round-2 closures (2026-06-28, from a real-product stress-test):** §18 — the harness no longer false-passes a fixed desktop grid masked by `overflow:hidden`; it audits real clipping/fixed-width/touch/text at 390+360, with page-scroll-vs-contained-scroll and inline-link exemptions calibrated (it even caught a real mobile tab-overflow in our own Cadence reference). §16/§20 — behavior-audit now drives keyboard focus-visible + dialog focus-trap/Esc + ARIA semantics, the layer axe is blind to. The dead-button test now excludes legitimately-no-op controls (disabled / already-active toggle / file-dialog), so it stops over-counting good products. The remaining `[drive]`/`[reason]`-only dims (3, 5, 6, 15-feel, 19, 21, 22) are still judged by driving/looking — that's correct, not a gap.

**The standing rule (so I stop waiting to be told):** every render is judged against THIS list, not just the rubric's 10 auto-dims. A page is "world-class / 可交付" only when it clears the static gate **and** the behavior gate **and** a drive-through of the core 动线 **and** a motion check of liveness — and a human-judgment pass on fit/voice/soul. Anything on this list with no tool yet is the next thing to build into the harness.
