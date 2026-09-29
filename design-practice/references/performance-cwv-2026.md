---
type: reference
created: 2026-06-28
priority: P0
scope: web performance, Core Web Vitals, perceived performance
sources:
  - https://web.dev/articles/vitals
  - https://web.dev/articles/defining-core-web-vitals-thresholds
  - https://web.dev/articles/optimize-lcp
  - https://web.dev/articles/content-visibility
  - https://web.dev/articles/font-best-practices
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images
  - https://github.com/GoogleChrome/web-vitals
---

# Performance CWV 2026 - performance is a design-quality dimension

Performance is not an engineering cleanup pass. It is part of the visual language. A slow page changes the product's perceived character: premium becomes heavy, calm becomes dead, and polished motion becomes jank.

The design-practice bar: a page is not world-class if it only looks good in a screenshot. It must load its main content quickly, respond to input without hesitation, and never shift under the user's finger.

## Core Web Vitals 2026: hard targets

Google's current Core Web Vitals are LCP, INP, and CLS. INP replaced FID as a stable Core Web Vital in 2024. The thresholds are evaluated at the 75th percentile of page views, segmented across mobile and desktop.

| Metric | What it measures | Good | Needs work | Poor | Design implication |
| --- | --- | ---: | ---: | ---: | --- |
| LCP | Largest Contentful Paint: when the main content likely loaded | `<= 2.5s` | `> 2.5s` to `<= 4.0s` | `> 4.0s` | Hero media, web fonts, SSR, and render-blocking CSS are design decisions. |
| INP | Interaction to Next Paint: responsiveness across interactions | `<= 200ms` | `> 200ms` to `<= 500ms` | `> 500ms` | Heavy client JS, layout work, and delayed feedback make the UI feel broken. |
| CLS | Cumulative Layout Shift: unexpected visual movement | `<= 0.1` | `> 0.1` to `<= 0.25` | `> 0.25` | Unsized images, late fonts, ads, embeds, and injected banners are visual-quality failures. |

Sources: [web.dev Web Vitals](https://web.dev/articles/vitals), [threshold methodology](https://web.dev/articles/defining-core-web-vitals-thresholds), [INP became stable in 2024](https://web.dev/articles/vitals).

## The design interpretation

### LCP is the hero contract

The LCP element is usually the hero image, headline block, product screenshot, or first major content panel. If that element is hidden behind client-side rendering, lazy-loaded media, or a late web font, the first impression is slow by design.

Do this:
- Put the likely LCP element in the initial HTML.
- If the LCP is an image, expose `src` or `srcset` in the HTML, not a JavaScript `data-src`.
- Never `loading="lazy"` the LCP image.
- Add `fetchpriority="high"` to the one likely LCP image, or at most one to two critical images.
- Use `preload` for a CSS background LCP image or critical web font only when it cannot otherwise be discovered early.
- Avoid hiding the hero behind A/B scripts, animation gates, or delayed hydration.

```html
<img
  src="/hero-1280.avif"
  srcset="/hero-640.avif 640w, /hero-1280.avif 1280w, /hero-1920.avif 1920w"
  sizes="(width < 768px) 100vw, 1280px"
  width="1280"
  height="720"
  fetchpriority="high"
  alt="Real product dashboard showing active incidents and owners">
```

Reference: [Optimize LCP](https://web.dev/articles/optimize-lcp), [MDN responsive images](https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images).

### INP is the "does it listen?" contract

INP is not only about click handlers. It is about whether the product acknowledges a human action quickly. The visual feedback should happen under `100ms` whenever possible, because the user needs to feel causality before the full operation completes.

Do this:
- Split expensive work from the input path. Update the pressed state now; compute later.
- Avoid rendering the whole page after a keystroke, filter change, drag, or tab switch.
- Keep animation and state transitions on `transform` and `opacity`.
- Virtualize long lists and keep table updates scoped to the rows that changed.
- Defer chart rendering, syntax highlighting, map rendering, and heavy editors until visible or requested.
- Prefer Server Components, streaming, or islands so static content does not hydrate as one large app.

Design smell: a save button that shows no pressed state while waiting for the server. That is an INP and trust failure even if the request succeeds.

### CLS is the "do not betray the eye" contract

Layout shift reads as amateur because the page moves after the user has already started scanning or tapping.

Do this:
- Always set `width` and `height` or `aspect-ratio` on images, video, embeds, skeletons, charts, and ad slots.
- Reserve space for async sections. A skeleton must match the final content's approximate geometry.
- Use `font-display` plus `size-adjust` or similar fallback metrics to reduce font swap shift.
- Insert banners, cookie notices, and toasts in reserved regions or overlay layers, not above already-read content.
- Use `content-visibility: auto` with `contain-intrinsic-size` for long below-fold sections so they do not create scrollbar jitter.

Reference: [Optimize CLS](https://web.dev/articles/optimize-cls), [content-visibility](https://web.dev/articles/content-visibility).

## Budgets for design-practice output

These are not universal laws. They are the skill's default budgets for a polished product UI or brand page in 2026. Tighten for mobile-first consumer pages; loosen only for real product complexity.

| Budget | Default target | Hard stop | Notes |
| --- | ---: | ---: | --- |
| Initial route JS, public/marketing page | `<= 150KB` compressed | `> 200KB` | Static sections should not hydrate. Use islands/RSC. |
| Initial route JS, authenticated app shell | `<= 250KB` compressed | `> 350KB` | Route-level split tables, editors, charts, and command palettes. |
| Added JS per lazy feature | `<= 50KB` compressed | `> 90KB` | Heavy editors, maps, and charts load on intent or visibility. |
| Route CSS | `<= 50KB` compressed | `> 80KB` | Critical above-fold CSS first; remove unused generated utility bloat. |
| Critical inline CSS | `<= 14KB` compressed | `> 25KB` | Enough for layout, type, hero, skeleton, focus, and shell. |
| Above-fold image bytes | `<= 350KB` total | `> 700KB` | One hero can be rich; everything else must earn bytes. |
| LCP image | `<= 200KB` preferred | `> 400KB` | AVIF/WebP, correct crop, correct slot size. |
| Font files used before LCP | `<= 70KB` total | `> 120KB` | WOFF2, subset, max one display and one text family. |
| Third-party scripts before interaction | `0KB` preferred | `> 30KB` | Analytics after consent/idle unless product-critical. |
| Long tasks during load | `0` over `100ms` | Any repeated `> 50ms` tasks | Lab proxy for INP risk. |
| CLS | `<= 0.05` design-practice target | `> 0.1` | The Google good threshold is 0.1; aim lower. |

## Image strategy

Use images as real content, not wallpaper.

- Format: AVIF first, WebP fallback, PNG only for sharp UI transparency, SVG only for icons/logos/technical vector.
- Sizing: generate actual variants for mobile, tablet, desktop, and wide desktop. Do not ship a 2400px image into a 390px slot.
- Art direction: use `<picture>` when the mobile crop needs a different subject framing. Cropping the same desktop screenshot down to unreadable mobile is a design failure.
- Priority: the likely LCP image gets `fetchpriority="high"` and is not lazy-loaded. Below-fold images use `loading="lazy"` and `decoding="async"`.
- Stability: every image has `width` and `height`, or a stable `aspect-ratio`.
- Product screenshots: use real zoomable states. If the screenshot text falls apart at 2x zoom, it is not a credible product image.

```html
<picture>
  <source media="(width < 720px)" srcset="/feature-mobile.avif" type="image/avif">
  <source media="(width >= 720px)" srcset="/feature-desktop.avif" type="image/avif">
  <img src="/feature-desktop.webp" width="1440" height="900" loading="lazy" decoding="async" alt="Filtered issues list grouped by owner">
</picture>
```

## Font-loading strategy

Fonts carry brand, but invisible text destroys trust.

- Use WOFF2 only.
- Use at most two families before interaction: one text/display family plus optional mono for code, IDs, and numbers.
- Subset with `unicode-range`. Latin and CJK should not ship as one huge universal file.
- Preload only the one face needed for first paint. Preloading every weight steals bandwidth from the LCP image.
- Use `font-display: optional` for body text when performance matters most.
- Use `font-display: swap` for a brand display face only if fallback metrics are tuned enough to avoid obvious shift.
- Avoid icon fonts. Use inline SVG or an icon component set.
- Use `size-adjust`, `ascent-override`, `descent-override`, or a carefully matched fallback stack for reduced CLS.

Reference: [web.dev font best practices](https://web.dev/articles/font-best-practices), [MDN font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display).

## CSS and rendering strategy

- Inline or early-load only the CSS needed for above-fold layout, typography, buttons, skeletons, focus rings, and hero.
- Defer page-specific decorative CSS below the first viewport.
- Remove unused CSS after utility generation. Do not ship every possible class to every page.
- Use containment: `content-visibility: auto` plus `contain-intrinsic-size` for long repeated sections below the fold.
- Prefer `transform` and `opacity` for animation. `height`, `width`, `top`, `left`, and `filter` can become layout or paint bottlenecks.

```css
.below-fold-section {
  content-visibility: auto;
  contain-intrinsic-size: auto 720px;
}
```

## JavaScript architecture

### RSC, streaming, and islands

Default principle: static content is server-rendered HTML. Only the controls that need state, browser APIs, gestures, or local interactivity become client JavaScript.

- React Server Components / Next.js: keep layouts and content sections as Server Components. Use `"use client"` only at the leaf where event handlers or browser APIs are required. Next.js explicitly notes this reduces client JS and can stream UI progressively.
- Streaming: show shared layouts and route skeletons while the dynamic part resolves. In Next.js, `loading.tsx` creates immediate visual feedback and wraps route content in a Suspense boundary.
- Islands: in Astro-style architecture, render most of the page as static HTML and hydrate only interactive widgets. This avoids monolithic JS payloads.
- Code split by route and intent. The charting library loads when the analytics tab opens; the command palette loads when the shortcut or button is used.

Sources: [Next.js Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), [Next.js streaming](https://nextjs.org/docs/app/getting-started/linking-and-navigating#streaming), [Astro islands](https://docs.astro.build/en/concepts/islands/).

## Perceived performance craft

### Skeletons vs spinners

Use a spinner only for a small, indeterminate, local action where no shape is known: button submit, inline retry, short upload wait.

Use a skeleton when the user is waiting for a content region. The skeleton must mirror the final layout, not draw generic gray bars. A table skeleton has rows, cells, and reserved columns. A profile skeleton has avatar, name, metadata, and actions. A chart skeleton reserves the exact chart rectangle.

Bad: full-page spinner while loading a dashboard.

Good: sidebar and header render immediately; table rows show skeletons; filter bar is usable; slow chart panel streams later.

### Optimistic UI

Optimistic UI is a promise. Use it only when rollback is clear.

- Toggle, star, archive, reorder: optimistic is usually right.
- Payment, permission change, destructive delete: show pressed feedback immediately, but do not claim success until confirmed.
- When optimistic state fails, keep the user's intent visible: "Couldn't archive. Restored the item. Retry."

### Less than 100ms feedback

Every intentional input gets visible feedback in under `100ms`: pressed button, active row, pending chip, local count update, or subtle busy state. This is independent from server completion.

### Do not block on full data

Linear's current homepage example even includes the product idea "Render UI before state sync when minimum required state is present, instead of blocking on full refresh." That is the right mental model for product UI: render the stable shell and minimum meaningful state first, then enrich.

Apply it everywhere:
- Render navigation, title, filters, and empty-state frame immediately.
- Load primary list before secondary analytics.
- Show cached data with a stale marker while refreshing.
- Keep shared layouts interactive during route transitions.

### Use `content-visibility` without creating a fake page

`content-visibility: auto` is for below-fold, long, independent chunks. Do not use it on the first viewport, sticky navigation, focusable active controls, or anything whose size must be exact at first paint. Pair it with a realistic `contain-intrinsic-size`.

## How an agent can self-measure

### Lighthouse

Use Lighthouse for lab regression checks. It cannot measure real INP because lab runs do not include real user input, but Total Blocking Time is a useful proxy for INP risk.

```bash
npx lighthouse http://localhost:3000 \
  --preset=desktop \
  --only-categories=performance \
  --output=json \
  --output-path=./lighthouse-performance.json
```

Also run mobile emulation before claiming quality:

```bash
npx lighthouse http://localhost:3000 \
  --only-categories=performance \
  --output=html \
  --output-path=./lighthouse-mobile.html
```

### PageSpeed Insights

Use [PageSpeed Insights](https://pagespeed.web.dev/) for a public URL. It combines lab Lighthouse with CrUX field data when available. It is the quickest way to catch "works locally, slow in the real world."

### Chrome DevTools

Run:
- Performance panel: record page load and one critical interaction. Look for long tasks, forced reflow, layout shift, and delayed paint.
- Network panel: disable cache, inspect the LCP image priority, font discovery, unused JS, and third-party scripts.
- Coverage panel: find unused CSS and JS.
- Rendering panel: enable layout shift regions.

### `web-vitals` library

For product work, add real-user measurement. The `web-vitals` library is the small official wrapper that reports LCP, INP, and CLS in a way aligned with Google tools.

```ts
import { onCLS, onINP, onLCP } from 'web-vitals';

function send(metric: unknown) {
  const body = JSON.stringify(metric);
  navigator.sendBeacon?.('/analytics/web-vitals', body) ||
    fetch('/analytics/web-vitals', { body, method: 'POST', keepalive: true });
}

onCLS(send);
onINP(send);
onLCP(send);
```

Reference: [GoogleChrome/web-vitals](https://github.com/GoogleChrome/web-vitals).

## Perf self-test checklist

- [ ] LCP `<= 2.5s` at p75, and design-practice target `<= 2.0s` for public pages.
- [ ] INP `<= 200ms` at p75; every tap/press has visible feedback under `100ms`.
- [ ] CLS `<= 0.1`, target `<= 0.05`.
- [ ] Likely LCP element is in initial HTML.
- [ ] LCP image is not lazy-loaded and uses `fetchpriority="high"` only if it is truly the LCP candidate.
- [ ] All images, videos, embeds, skeletons, and charts reserve stable dimensions.
- [ ] Responsive images use `srcset`/`sizes` or `<picture>` with art-directed crops.
- [ ] Above-fold image bytes stay within budget.
- [ ] WOFF2 fonts only; max two families; fonts are subset; only one critical face is preloaded.
- [ ] `font-display` strategy is intentional: `optional` for body, `swap` only when brand value beats the swap risk.
- [ ] Initial route JS is within budget; interactive islands are leaf-level.
- [ ] Charts, editors, maps, command palettes, and heavy modals are lazy-loaded by route, visibility, or user intent.
- [ ] No repeated long tasks over `50ms` during load or critical interactions.
- [ ] Skeletons match final geometry; no full-page spinner for a data page.
- [ ] Slow routes stream a shell and loading UI instead of blocking.
- [ ] Below-fold heavy sections use `content-visibility: auto` with `contain-intrinsic-size`.
- [ ] Lighthouse mobile and desktop were run.
- [ ] Chrome DevTools Performance recording exists for one load and one critical interaction.
- [ ] Field instrumentation exists for LCP, INP, and CLS before launch.

## Budget table to paste into a task

| Area | Pass condition |
| --- | --- |
| CWV | LCP `<= 2.5s`, INP `<= 200ms`, CLS `<= 0.1` at p75. |
| Design-practice target | LCP `<= 2.0s`, CLS `<= 0.05`, immediate feedback `<100ms`. |
| JS | Public route `<=150KB` compressed; app shell `<=250KB`; lazy feature `<=50KB`. |
| CSS | Route CSS `<=50KB`; critical CSS `<=14KB`; no unused utility bulk. |
| Images | LCP image `<=200KB` preferred; above-fold images `<=350KB`; AVIF/WebP; stable dimensions. |
| Fonts | WOFF2 only; `<=70KB` before LCP; subset; one preloaded face max. |
| Rendering | No layout shift from async content; `content-visibility` for long below-fold sections. |
| Measurement | Lighthouse mobile/desktop, DevTools trace, and `web-vitals` RUM for shipped products. |
