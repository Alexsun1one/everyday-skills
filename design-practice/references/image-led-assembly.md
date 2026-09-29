---
type: reference
created: 2026-06-28
priority: P0
pairs-with: references/world-class-teardowns/00-moodboard-tokens.md · references/stage1-output-formats.md · references/stage2-fidelity-restore.md · tooling/behavior-audit.mjs
covers: the image-gen branch of Stage 2 — for VISUAL-LED pages only
source: user insight (2026-06-28) — "if the page is assembled from images, the image model should slice it cleanly from the start; the skeletons we already build are the slice map; but only for THAT kind of page, not every page."
---

# Image-Led Pages — the Slice-and-Assemble workflow (生图拼页 = 切图装配)

> This resolves the tension between two things this skill already holds firmly:
> 1. **The skeleton-first discipline** (Stage 1 produces 骨架图: ASCII / Mermaid / grayscale image-wireframes).
> 2. **The hard image-gen rule** (`world-class-teardowns/00-moodboard-tokens.md`): image-gen is for brand / editorial / hero mood ONLY — **never** a whole-page product-UI reference, because a generated "UI screenshot" is skin-without-skeleton — fake data, gibberish text on zoom, off-grid, wobbly alignment, dead controls.
>
> The reconciliation: for visual-led pages, **don't generate one flat whole-page image and restore it 1:1.** Generate the design **already sliced to the skeleton's regions** — as *assets* (backgrounds, textures, illustrations, hero art), never as baked-in UI. The real text, layout, and interactivity are always coded as real DOM on top. **The skeleton is the slice map; image-gen fills each slice's skin; code always owns the skeleton.** This is the old front-end craft of 切图 (slicing a PSD into assets + assembling) reborn for the AI era.

## The page-type gate — this path is NOT for every page
Decide FIRST. This branch applies to ONE family of pages; the other family must never touch it.

| Page family | Examples | Path |
|---|---|---|
| **Utility / product UI** | SaaS dashboard, CRM, settings, list-detail, admin, editor, forms, data tables | **NO image-gen.** Skeleton → real code + real components, grounded in real shipped-product tokens (`tokens/`). Image-gen here = the塌房 failure. |
| **Visual-led** | brand / marketing / landing / editorial / story / product launch / hero / portfolio | **The slice-and-assemble path below.** Image-gen contributes its real strength (mood, art direction, composition) — but only as sliced assets under a real-coded skeleton. |

If you cannot say which family the page is in, default to **utility / no-image-gen** — it is never wrong to build structure from a wireframe; it is often wrong to build it from a picture.

> Even within a visual-led page, the gate is **per-region**: the hero band may be image-led, while the pricing table, the nav, and the FAQ are pure-coded utility regions. Mixed is normal — slice by region, not by page.

## The core principle — generate ASSETS, never a UI screenshot
What the image model is allowed to produce, sliced per region:
- ✅ **Backgrounds / textures / gradients-with-grain / atmospheric fields** (full-bleed, behind real content).
- ✅ **Illustrations / spot art / 3D objects / editorial imagery** — ideally **transparent-background PNG** so they drop onto a coded layout.
- ✅ **Hero / cover imagery** where the image *is* the content (a photograph-grade brand moment) — with NO live UI baked in.
- ❌ **NEVER**: baked-in body text, headings, labels, numbers, buttons, inputs, nav bars, cards-with-data, "a screenshot of the page." Anything a user reads or clicks is **real DOM**, added in code. (Baked text is the zoom-gibberish tell; baked controls are the dead-facade tell.)

The test: **zoom the final rendered page to 400%.** Every glyph must stay razor-crisp (it's real web type) and every control must respond (it's a real element). If text blurs or a button is decorative, you baked UI into the image — regenerate as an asset, code the UI.

## The skeleton IS the slice map
We already build the skeleton in Stage 1 (the grayscale image-wireframe + the ASCII/Markdown structure). For a visual-led page, that skeleton does double duty: it **names the regions and the real content slots**, which is exactly the slice plan.

```
Stage 1 skeleton (already done)            →   per-region treatment decision
┌──────────────────────────────┐
│  HERO  [headline slot]        │  region: hero      → generated atmospheric bg (asset) + REAL coded headline/CTA on top
│        [sub] [CTA]            │
├──────────────────────────────┤
│  FEATURE BAND  ▢ ▢ ▢          │  region: features  → 3 generated transparent spot-illustrations + REAL coded text/grid
├──────────────────────────────┤
│  STORY  [img] [copy]          │  region: story     → generated editorial image (asset) + REAL coded prose
├──────────────────────────────┤
│  PRICING  [table]             │  region: pricing   → PURE CODE (utility region — no image-gen)
├──────────────────────────────┤
│  FAQ / FOOTER                 │  region: footer    → PURE CODE
└──────────────────────────────┘
```
Annotate each skeleton region with its treatment — `bg-asset` / `spot-asset` / `hero-asset` / `pure-code` — *before* generating anything. That annotated skeleton is the brief for the image model.

## The workflow (visual-led page)
1. **Skeleton first** (Stage 1) — never skip to a picture. Name regions + real content slots.
2. **Annotate each region** with its treatment (table above). Most regions are `pure-code`; only the genuinely image-led ones get assets.
3. **Generate per-region assets** (Codex / image-gen), one focused prompt per slice — see the prompt recipe below. Transparent background for spot art; full-bleed for backgrounds; **explicitly "no text, no UI, no buttons in the image."**
4. **Code the real skeleton** — real semantic HTML, real web type (the licensed/variable display face from the chosen direction), the 4/8 grid, real interactive controls, real content. Place the generated assets as `background-image`, `<img>`, or absolutely-positioned illustration layers *behind/within* the real DOM.
5. **Composite craft** — the seam between asset and code is where it lives or dies: the headline sits in real optical alignment over the bg; the spot art aligns to the grid; the asset's color is pulled into the page tokens (don't let a generated teal fight the coded palette).
6. **Verify** — run the loop on the *assembled* page: `render-critique.mjs` (gate + 10-dim, incl. the real responsive check), `behavior-audit.mjs` (controls real, `liveRatio≥80%`, `nakedNativeControls:0`), and the **400% zoom scrutiny** (text crisp, nothing baked). The image-gen rule is satisfied because no UI was generated — only assets.

## Prompt recipe — how to ask Codex / image-gen for a clean slice
- **One region, one asset, one prompt.** Don't ask for "a landing page"; ask for "a full-bleed dark atmospheric background, warm amber light blooming from lower-left, fine film grain, no text, no UI elements, no logos, 2400×1400, edges that tile/fade for safe overlay."
- **Spot illustration:** "a single isometric [object], soft studio light, **transparent background (PNG)**, no text, no UI, centered with padding, consistent with [palette hexes]."
- **Lock the system:** pass the page's palette hexes + the mood word so assets share a family. Generate a **set** in one style, not one-offs that clash.
- **Reserve the type:** state "leave the upper third empty / negative space for a headline added in code" so the real headline has a home.
- **Never** prompt for "a hero with the headline '…'", "a pricing card", "a button", "a dashboard" — that's generating UI. Generate the *stage*, code the *actors*.

## Anti-patterns (the failures this path prevents)
- **Flat whole-page screenshot → restore 1:1.** The塌房 we caught: looks fine as a thumbnail, falls apart on zoom (fake data, gibberish text, off-grid), restores into a dead facade. Slice into assets instead.
- **Baked text / numbers / buttons in the image.** Blurs on zoom; can't be edited, translated, or made accessible; controls are dead. Text & controls are always code.
- **Using this path for a SaaS/dashboard.** Utility UI's skeleton comes from real-product references + code, never from a generated picture. Wrong family.
- **Asset palette fighting the coded palette.** Generated colors must be pulled into the token system, not left as a foreign accent.
- **One giant asset instead of per-region slices.** A single 8000px "everything" image can't be placed responsively and re-bakes the whole-screenshot problem at higher resolution.

## Where this sits in the pipeline
- Gate: the page-type decision happens at **Intent Brief** (visual-led vs utility) and is refined **per-region** at Stage 1.
- Assets are generated **between Stage 1 (skeleton) and Stage 2 (restore)** — the annotated skeleton is their brief.
- Assembly **is** Stage 2 for visual-led pages: restore the skeleton 1:1 in code, dropping assets into their slots; the fidelity contract (`stage2-fidelity-restore.md`) still holds.
- Verification is the same Stage 3 loop + behavior gate + the 400% zoom scrutiny (`[[zoom-in-scrutiny-and-imagegen-ui-rule]]`).

> One line to remember: **the skeleton is the slice map, image-gen fills each slice's skin, code always owns the skeleton — and this whole path is for visual-led pages only.**
