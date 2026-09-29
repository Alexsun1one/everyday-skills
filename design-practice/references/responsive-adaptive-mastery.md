---
type: reference
created: 2026-06-28
priority: P0
pairs-with: references/qa-responsive.md · references/craft-details-invisible.md · tooling/render-critique.mjs
covers: quality-landscape.md → E.18 Responsive art direction
source: The #1 failure caught by the real-product stress-test (fixed desktop grid + overflow:hidden silently breaks on mobile). CSSWG specs (Grid, Container Queries), Apple HIG, Material 3, and the responsive craft of Linear / Stripe / Vercel / Family.
---

# Responsive & Adaptive Mastery — the craft of layouts that survive every screen

> `qa-responsive.md` is the *acceptance checklist* ("at each breakpoint, does X hold?"). This is the *craft layer* — the **how**: fluid type, container queries, the `overflow:hidden` trap, and the one principle agents miss: **responsive ≠ reflow — the information architecture changes.** The failure that exposed this gap: a desktop grid with `overflow:hidden` looked fine in screenshots and passed the static gate, then silently clipped content on a 375px phone. The static harness can't catch this; it must be *designed for* from the first rule, not patched.

## The one principle — responsive ≠ reflow, the IA changes
Naive responsive = "make the columns stack." Real responsive = **the whole shape of the interface changes per viewport**, because the user's hands, posture, and attention span change. Going narrow does **three things, in this order:**
1. **Collapse chrome** — top nav → hamburger drawer; sidebar → bottom tab-bar or hidden-behind-menu; toolbars → overflow menu (`⋯`).
2. **Change the data shape** — a dense table is **not** "shrunk to scroll," it becomes a **card list** (right way below). A multi-column dashboard becomes a **priority stack**, highest-signal card first.
3. **Change the input model** — hover affordances vanish, targets grow, the primary action becomes full-width and reachable by the thumb.

If you only do #1, you get "works but worse." All three is world-class.

## The responsive bar is product-type-dependent (judge against INTENDED reach)
Responsive integrity is not one universal bar — it's judged against where the product is actually used:
- **Marketing / landing / editorial / consumer** → **mobile-first is mandatory.** Most traffic is a phone; a clipped hero or an overflowing nav is a launch blocker. Bar: flawless at 360–390px.
- **Desktop power-tools** (IDE, dense analytics dashboard, trading terminal, multi-pane CRM) → harder to make responsive, but **NOT exempt from it.** They still owe genuine mobile quality: reflow the IA — file tree → drawer, dense table → labeled cards, multi-pane → priority stack, fixed-`px` widths → fluid (`min-width:0` + minmax grids), tiny text → ≥12px, hit areas → ≥44px. Linear, GitHub, Notion, Stripe's dashboard, Figma's viewer all reflow to real mobile — **that is the bar.** "Dense" is a reason to design the reflow *carefully*, never a license to skip it.
- **Hybrid** (SaaS with both a marketing site and an app) → decide *per surface*: the marketing surface is mobile-first; the app reflows to real mobile too.

**The harness flags clipping regardless of product type — that's correct.** It is telling you "this is not usable at 360px." The answer is almost always **reflow it to real mobile quality.** The one unacceptable outcome — the one the harness exists to catch — is **a desktop layout that silently clips 30+ elements off-screen on a phone**: that's not a design decision, it's an untested page.

### Degradation is a LAST RESORT, never a shortcut
A graceful `min-width` + "open on desktop" state is acceptable in a **real shipped product** only for a genuinely desktop-only professional tool (a multi-track NLE, a node-graph canvas) where mobile is a true non-goal — and even then it is a deliberate, flagged compromise to revisit, never a way to dodge responsive work. **It is never acceptable in a showcase, a capability demo, or anything meant to prove quality** — there, you reflow it. If you reach for a "best on desktop" wall to make the harness pass, you are skipping the actual job. Quality means the IA *changes* and stays usable on a phone — not a wall that hides that you never did the work.

## 1. Mobile-first, and content-driven breakpoints
- **Mobile-first CSS**: base styles target the smallest screen; add complexity with `min-width` media queries. Mobile is the default — if a query fails to load or a device is narrower than you imagined, the layout still holds. Desktop-first (`max-width`) leaves mobile as a degraded afterthought.
- **Content-driven, not device-width-driven breakpoints.** Don't write `@media (max-width: 768px)` "because iPad." Narrow the viewport slowly and **place a breakpoint at the exact width where the layout breaks** — where two columns start touching, where a label truncates, where a row wraps ugly. Device widths are a moving target; your content's breaking points are not. Device breakpoints are fine as a *starting* set (Tailwind's `sm/md/lg/xl`) — but the final placement is driven by *your* content.

## 2. Intrinsic / fluid layouts — let the layout compute itself
The world-class move: **zero or few breakpoints**, because the layout adapts intrinsically. Three tools, each with a job:

```css
/* a) Grid auto-fit + minmax — a card grid that re-columns itself, no media query at all */
.grid {
  display: grid; gap: 1rem;
  /* min(100%, 18rem) prevents overflow when the container is narrower than 18rem */
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr));
}

/* b) flex-wrap — toolbars, chip rows, action groups; no query needed */
.toolbar { display: flex; flex-wrap: wrap; gap: .5rem; }

/* c) container queries — a component responds to ITS container, not the viewport */
.card-host { container-type: inline-size; }
@container (width > 30rem) {
  .card { grid-template-columns: auto 1fr; }   /* side-by-side when it has room */
}
```
**When each:** `auto-fit` for a repeating **card grid** (gallery, results, dashboard tiles). `flex-wrap` for a simple **wrap-and-go** row (buttons, tags). **Container queries** when the component's layout depends on **where it's placed** — a card renders compact in a 240px sidebar but expanded in a full-width main. This is what makes a **design system** component truly portable; viewport queries can't, because the same component lives at different widths on the same page. (Container queries are baseline-supported across all current browsers since 2023.)

## 3. Fluid type & space with `clamp()`
`clamp(min, preferred, max)` lets a value grow with the viewport without a single breakpoint. The middle term is `base + slope·vw` so it scales smoothly between floors and ceilings.

```css
:root {
  /* fluid type scale — floor at mobile, ceiling at desktop */
  --fs-display: clamp(2rem,    1.1rem + 4vw,  3.5rem);
  --fs-h1:      clamp(1.5rem,  1.1rem + 1.8vw, 2.25rem);
  --fs-h2:      clamp(1.25rem, 1.05rem + 1vw,  1.5rem);
  --fs-body:    clamp(1rem,    .92rem + .35vw, 1.125rem);
  --fs-small:   .875rem;                       /* 14px floor — never go below 12px */
  /* fluid space scale */
  --s-3: clamp(.75rem, .5rem + 1vw,  1.5rem);
  --s-4: clamp(1rem,   .6rem + 1.6vw, 2rem);
  --s-6: clamp(1.5rem, .8rem + 3vw,   3rem);
}
```
Rules: type **never** goes below 12px (small text is a contrast *and* legibility failure). Body text **16px** on mobile. Inside a container-query host, swap `vw` for **container units** (`cqi` = 1% of the container's inline size) so the component scales to its box, not the window. Pair with `tabular-nums` and negative display tracking (see `craft-details-invisible.md` §1–2).

## 4. Viewport units that actually work — `dvh/svh/lvh` + safe areas
- **Never use `100vh` for full-height mobile layouts** — on iOS Safari it includes the area behind the browser chrome and your fixed footer is hidden behind the toolbar. Use **`100dvh`** (dynamic — shrinks as the URL bar shows) for app-shell heights, `100svh` (smallest) when you must guarantee nothing is ever clipped, `100lvh` (largest) rarely.
- **Notch & home indicator:** add `viewport-fit=cover` to the `<meta name="viewport">`, then pad with real safe insets — never hardcode a guess.
```css
meta: <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
.app-shell   { min-height: 100dvh; }
.bottom-bar  { padding-bottom: env(safe-area-inset-bottom); }
.centerpiece { padding: env(safe-area-inset-top) env(safe-area-inset-right) 0 env(safe-area-inset-left); }
```

## 5. Touch ergonomics — targets, thumb zone, hover ≠ tap
- **Target size ≥ 44×44 CSS px** (Apple HIG 44pt; Material 3 48dp). WCAG 2.2 **2.5.8 Target Size (Minimum)** sets the AA bar at **24×24** with exceptions (inline links, etc.) and **2.5.5 Target Size (AAA)** at **44×44**. Aim for 44; never below 24. Use generous **`padding`/hit-area padding**, not a tiny visual + invisible gap.
- **Thumb zone:** on phones the comfortable reach is the **lower ⅔, biased to the bottom-right** (right-handed) — put the primary action there, not top-right. Bottom sheets and sticky action bars win on mobile for this reason.
- **Hover ≠ tap.** There is no hover on touch. Anything *revealed* only on hover (a tooltip, a row's action buttons, a dropdown) is **invisible to half your users**. Gate hover-only styles behind `@media (hover: hover) and (pointer: fine)`, and **always provide a tap/touch path** to the same content.
```css
.row .actions { opacity: 0; }                         /* default: hidden */
@media (hover: hover) and (pointer: fine) {
  .row:hover .actions { opacity: 1; }                 /* mouse users: on hover */
}
/* touch / keyboard users: actions revealed on row focus or always-on below a width */
@container (width < 40rem) { .row .actions { opacity: 1; } }
```
- **`@media (pointer: coarse)`** detects touch-primary devices — use it to enlarge targets, disable custom cursors/drag affordances, and replace hover-reveals. Add `touch-action: manipulation` on buttons to kill the 300ms double-tap delay; `touch-action: pan-x` on horizontal carousels so they don't fight the browser's back-swipe.
- **iOS input zoom:** inputs with `font-size < 16px` auto-zoom on focus. Set input font-size ≥ `1rem`.

## 6. Responsive images — no layout shift, right bytes
```html
<img src="https://example.com/hero-960.jpg"
     srcset="https://example.com/hero-480.jpg 480w, https://example.com/hero-960.jpg 960w, https://example.com/hero-1600.jpg 1600w"
     sizes="(max-width: 640px) 100vw, 50vw"
     width="960" height="540"
     alt="…"
     loading="lazy" fetchpriority="high">
```
- **`width`+`height` (or `aspect-ratio`)** reserves the box so the image never causes CLS. `aspect-ratio` is the modern, content-agnostic way to hold a shape.
- **`srcset`+`sizes`** send the right resolution per viewport — don't ship a 2MB hero to a phone.
- **`loading="lazy"`** for below-the-fold; **`fetchpriority="high"`** + `loading="eager"` for the LCP image. (See `quality-landscape.md` §17 — LCP/CLS are a11y-adjacent: slow/janky pages exclude users on slow devices.)

## 7. Collapsing a dense table on mobile — the RIGHT way (not the naive way)
The **naive** failure: make a table scroll, or just stack every `<td>` under each other. Scrolling a table horizontally hides columns; stacking cells **loses the header↔value association** — a phone user sees "2,847" with no idea it's the *Amount* column.

The **right** way keeps semantics (`<table>`) but reskins each row into a **labeled card** so every value carries its column header:
```css
@media (max-width: 40rem) {
  table.dense thead { display: none; }                /* column heads move into cells */
  table.dense, table.dense tbody, table.dense tr, table.dense td { display: block; }
  table.dense tr {
    margin-bottom: var(--s-3); border: 1px solid var(--border); border-radius: 12px; padding: var(--s-3);
  }
  table.dense td { display: flex; justify-content: space-between; gap: 1rem; text-align: right; }
  table.dense td::before {            /* the column header, now a left-aligned label */
    content: attr(data-label); font-weight: 600; text-align: left; color: var(--text-faint);
  }
}
```
```html
<tr>
  <td data-label="Customer">Acme</td>
  <td data-label="Amount">¥2,847</td>
  <td data-label="Status">Paid</td>
</tr>
```
Even cleaner when you control the component: render a **dedicated card list** for narrow and a real table for wide, toggled by container query — each structure built for its shape, not one tortured into both. Either way, **the association is preserved** — that's the test.

## Anti-patterns gallery (each is a screenshot that "looks fine" but is broken)
- **Fixed `px` widths** (`width: 1200px`, `min-width: 1024px`) → guaranteed horizontal overflow on a phone.
- **`overflow: hidden` to "fix" overflow** → the #1 culprit. It doesn't fix anything; it *clips* content out of existence. A user can't scroll to what they can't see. Fix the layout, don't mask it.
- **Desktop grid on phone** → columns collapse to ~30px, text wraps one word per line.
- **Tap targets `< 24px`** → unusable; an icon button with no padding is un-tappable.
- **Text `< 12px`** → illegible; also a contrast failure.
- **Horizontal scroll trap** → the *whole page* scrolls sideways (a wide element leaks out) instead of a single inner box scrolling in place. The fix: contain wide content (tables, code) in a `max-width:100%; overflow:auto` wrapper, and use `overflow-x: clip` on `<body>` as a backstop so the page itself can never pan.
- **Hover-only affordances** → half your users never see them (see §5).
- **`100vh` mobile full-height** → fixed footer eaten by the URL bar (see §4).

## Self-test checklist (run per breakpoint: 360 / 390 / 768 / 1024 / 1280 / 1536 px)
```
□ Page never scrolls horizontally at ANY width (overflow-x is clipped on body)
□ No fixed px / min-width locking the layout above the viewport
□ No overflow:hidden masking real content (verify: temporarily remove it — does content appear?)
□ Card grid uses auto-fit/minmax (or container queries), not a hardcoded cols count
□ Type uses clamp() floors; nothing < 12px; body ≥ 16px on mobile
□ Full-height shells use dvh/svh, not vh
□ Notch/home-bar handled via env(safe-area-inset-*) + viewport-fit=cover
□ Touch targets ≥ 44px (never < 24px); primary action in the thumb zone / full-width on mobile
□ Every hover-revealed affordance has a tap/focus path (@media hover:hover gate + coarse fallback)
□ Images: width/height or aspect-ratio (no CLS), srcset+sizes, lazy below fold
□ Dense data: table→labeled-card (association preserved) OR contained horizontal scroll — never page-scroll
□ Nav → drawer; dashboard → priority stack; the IA actually changes, not just reflow
□ Inputs ≥ 16px font-size (no iOS zoom)
```

## What world-class does — concrete references
- **Linear** — its command palette, sidebar, and issue table restructure across breakpoints; container-query-style components that work in any rail width. The bar for "feels native at every size."
- **Stripe** — docs + dashboard: fluid type, sticky-then-stacking sidebars, tables that degrade to cards with full label association.
- **Vercel** — marketing + dashboard: container queries for portable cards, `100dvh` app shells, no horizontal scroll anywhere.
- **Family** — mobile-first, bottom-anchored actions, generous touch targets.
- **Apple HIG** — 44pt targets, thumb-zone ergonomics, safe areas. **Material 3** — 48dp targets, adaptive layouts (compact/medium/expanded) as a first-class responsive spec (`m3.material.io`).
- Specs: CSSWG **CSS Grid** + **CSS Containment Module L3** (Container Queries), **CSS Values L4** (`clamp`, `min`/`max`), **CSS Viewport Units L4** (`dvh/svh/lvh`), **Media Queries L4** (`hover`, `pointer`).

> **Integration:** this is the craft behind `quality-landscape.md` §18 (Responsive art direction) and the `[auto]` overflow check in `render-critique.mjs`. The acceptance pass lives in `qa-responsive.md`. Rule of thumb the harness can't see: **if removing `overflow:hidden` reveals content that was being hidden, the layout is broken — fix it, don't mask it.**
