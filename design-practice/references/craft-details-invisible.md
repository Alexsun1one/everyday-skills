---
type: reference
created: 2026-06-27
priority: P0
source: Rauno Freiberg (invisible details), Emil Kowalski (animations), real extracted tokens, and the v1→v3 CRM craft pass
---

# The Invisible Details — the compound-craft layer that separates 4/5 from 5/5

> **The thesis (from Sun):** good and great share the same bones — same five senses, same neural net. The difference is **countless tiny details, each worth ~0.1, that none-of-them-alone is visible, but 30–40 of them compound into a qualitative change (质变).** This file is that layer. It is what the rubric's three judgment dims (hierarchy / typography / restraint) are really measuring, and it is the work of the LAST loop iterations — after the gate already passes.
>
> **Genre truth:** for a **utility tool** (CRM, dashboard, settings) SSS = *invisible perfection* — every detail so right nothing distracts from the task; there is no "wow moment," and adding one is wrong. For **brand / landing / editorial** SSS = *one composed bold moment* + these details underneath. Apply the right bar for the genre (see `web-craft/01-page-archetypes.md`).

A page that passes the gate is "correct." A page that has *all* of the below is "crafted." Treat each as a checkable 0.1.

## 1. Numbers & data (the fastest tool-UI tell)
- `font-variant-numeric: tabular-nums` on **every** number that sits in a column or updates (totals, table values, counts, %). Proportional digits make columns wobble and values "jump" on change — the #1 data-UI amateur tell.
- Right-align numeric columns; align by decimal/unit.
- The currency/unit symbol one step **smaller + dimmer** than the figure, baseline-aligned (`¥`2,847,000, not ¥**2,847,000**).
- Big display numbers: tighten tracking to **-0.03 ~ -0.04em** (large type needs negative tracking; small type needs slightly positive).
- A value that updates must not change width → reserve with tabular-nums so layout never shifts.

## 2. Typography micro
- A face **with character** — Linear ships **Inter Variable at weights 510 / 590** (not 500/600); that off-integer weight is *why* its text "feels" different. Pair a **mono** for numbers/IDs (engineered signal); a **serif display** for editorial/luxury.
- `font-optical-sizing: auto`; `-webkit-font-smoothing: antialiased`; `text-rendering: optimizeLegibility`.
- Tracking scales **inversely** with size: display −0.035em, body −0.006em, all-caps eyebrows **+0.06–0.08em**.
- Line-height by role: display ~1.0–1.1, body ~1.5, dense table rows tighter. Body line-length 60–75ch.
- 2–4 weights total, never more. Weight + size + color carry hierarchy — not size alone.

## 3. Dark-surface craft (why a dark UI looks "made" vs flat)
- **Luminance stacking**: canvas is the deepest; each raised layer (sidebar → card → popover) steps subtly lighter. Never one flat black.
- **Top-edge highlight** on every raised surface: `box-shadow: inset 0 1px 0 rgba(255,255,255,.05)`. This single line is the loudest "crafted" signal in dark UI — it catches light like a real edge.
- Neutrals carry a faint hue (cool/warm), never pure `#000`/`#111`.
- Shadows are **layered + tinted toward the background**, never one fuzzy grey box. On dark UI, prefer the inset highlight + a soft ambient shadow over a hard drop shadow.

## 4. Color & contrast micro
- **One owned accent**, used in exactly ~3 roles (primary action / active state / focus). Not indigo-by-default — own a hue.
- Per-color **optical-weight tuning**: a green and a gray status badge at the *same* alpha don't read as equal weight; tune each (gray needs more, bright blue/green needs less) so the row feels even.
- De-emphasize secondary text by shifting **toward the background hue**, not just lowering to grey.
- Smallest text (12px) must still clear **WCAG AA 4.5:1** — the faint tier is where contrast quietly fails.

## 5. Spacing & grid
- Strict **4/8 rhythm**. Off-grid values (7/9/11/13/14) are an amateur tell even when "they look fine" — they break subliminal rhythm. (Hairlines 1–2px are fine.)
- **Optical, not mathematical, centering**: glyphs, triangles, icons with uneven mass need a nudge; mathematical center looks off.
- One consistent component padding scale; equal optical padding inside buttons/inputs/badges.
- Generous whitespace first, then remove — under-spacing reads cheap; confident space reads premium.

## 6. Iconography
- **One stroke width everywhere** (e.g. 1.5). Mixing 1.3/1.4/1.6 is an instant amateur signal.
- One library / one metaphor set; icons optically sized on a shared grid (16/20), baseline-aligned to adjacent text.
- Prefer a real screenshot/state-dot over a decorative icon; never colored-circle-around-an-icon repeated (the card-tiling tell).

## 7. Interaction micro (mostly invisible in a screenshot — but it's half the craft)
- Every interactive element answers **hover / focus / active / disabled**; data regions answer **loading / empty / error**.
- **Motion = ease-out, ≤300ms** for feedback; use real curves (`cubic-bezier(.4,0,.2,1)` standard, `(.16,1,.3,1)` premium reveal). `ease-in` never for enters.
- **Animate transform/opacity only** (composited). Color/background transitions are fine (cheap paint) but layout props (width/height/margin) drop frames.
- **`:focus-visible`** never removed; ring offset + radius matched to the element. Keyboard path must be visible.
- Active nav: a **2–3px accent bar** (inset box-shadow) + tinted icon — the sidebar craft signal.
- Row hover reveals its actions (opacity 0→1, 150ms); button press `scale(.98)`; everything **interruptible**.
- Respect `prefers-reduced-motion`. Remove motion from high-frequency/keyboard-repeat actions.
- Custom `::selection` tint; thin styled scrollbars on dark.

## 8. The one composed moment (brand/landing genres)
- Utility tools: **no** wow moment — invisible perfection only.
- Brand/landing: exactly **one** signature moment (a hero data-viz, a type treatment, a scroll reveal) — plus all the above underneath. Two "moments" = noise.

## 9. Edge & robustness micro
- Long text **truncates with ellipsis** (`max-width` + `overflow:hidden`) — never wraps a table cell into chaos.
- Empty / loading (skeleton, not spinner) / error states designed, not skipped — the skill's cardinal rule.
- Survives 320–390px (reflow, table scrolls in its own box, not the page) and 200+ rows.

## Compound-Craft Audit (the 4/5 → 5/5 checklist — run AFTER the gate passes)
Each is one 0.1. Aim to tick nearly all.
- [ ] tabular-nums on every column/updating number
- [ ] currency/unit symbol dimmed + smaller + baseline-aligned
- [ ] display tracking negative (−0.03~−0.04em); eyebrows positive
- [ ] a characterful face (not system-by-accident); sans+mono paired; 2–4 weights
- [ ] luminance stacking across layers
- [ ] top-edge inset highlight on raised surfaces
- [ ] neutrals carry a hue; no pure #000
- [ ] one owned accent in ≤3 roles; not indigo-default
- [ ] per-color badge optical-weight tuned
- [ ] smallest text passes AA 4.5:1
- [ ] strict 4/8 grid; no stray 7/9/11/14
- [ ] optical (not mathematical) centering on glyphs/icons
- [ ] one icon stroke width; one library; baseline-aligned
- [ ] hover/focus/active/disabled all present
- [ ] :focus-visible kept, ring crafted
- [ ] active-nav accent bar
- [ ] motion ease-out ≤300ms, transform/opacity only, interruptible
- [ ] prefers-reduced-motion respected
- [ ] ::selection + scrollbar styled
- [ ] long text ellipsis-truncates; layout never shifts on data change
- [ ] empty/loading(skeleton)/error designed
- [ ] exactly one composed moment (brand) OR zero (utility)
- [ ] final pass: could anything be removed? remove it.

> **How to use in the loop:** the harness gate (console/a11y/overflow) gets you to "correct." Then run this audit by *looking at the screenshots* and *reading the CSS* — each unticked box is a 0.1 left on the table. SSS is when nearly every box is ticked. That is the compound 质变, made checkable.
