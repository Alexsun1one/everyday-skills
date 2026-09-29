# Real Site Teardowns

> ℹ️ **For real, measured numbers use `tokens/00-token-synthesis.md` + `tokens/real-extracted-tokens.md`** (computed CSS pulled live from 16 shipped sites). This file's value is the **qualitative** teardown — grid logic, what hard constraint each site solves, the 动线 — NOT its numbers, which are estimates. Treat numbers here as hypotheses; the `tokens/` files are ground truth.

Scope: official sites checked on 2026-06-27 where possible. Exact CSS values are not claimed unless stated by the site. Measurements below are **approx / 待主控用浏览器核实**. Use these as engineering hypotheses for token extraction, not as legal copies.

Source links:

- Linear: https://linear.app/
- Stripe: https://stripe.com/
- Vercel: https://vercel.com/
- Family: https://family.co/
- Arc: https://arc.net/
- Apple Vision Pro: https://www.apple.com/apple-vision-pro/
- Rauno: https://rauno.me/
- Igloo: https://www.igloo.inc/

## Linear

**What it solves:** Linear must feel like the fastest serious tool for product teams. The hard constraint is density without enterprise heaviness.

| Dimension | Teardown |
|---|---|
| Grid | Approx: centered max-width around 1120-1280px for marketing, app/product screenshots use layered dark surfaces. Content often uses strong center axis but breaks it with product UI depth. |
| Spacing | Approx: 8px micro scale, 24/32/48/80px section rhythm. Dark UI panels need 1px borders and subtle shadow/elevation. |
| Typography | Neutral grotesk, tight hierarchy, medium weights. Body usually quiet; screenshots carry the proof. |
| Motion | Fast and precise. Hover and reveal should feel under 250ms. Product UI interactions are the aesthetic, not ornamental animation. |
| Density | Medium on marketing, high in product surfaces. Density is controlled by row rhythm, keyboard affordances, and status chips. |
| Hard Constraint | Must sell speed and craft to users who hate bloated PM tools. Too much illustration weakens the promise. |
| Motion Path | Claim -> product surface -> workflow proof -> team/developer confidence -> conversion. |
| Tokens To Extract | Dark surface stack, command/menu affordances, subtle glow restraint, issue-row density, keyboard-first cues. |

## Stripe

**What it solves:** Stripe must make financial infrastructure feel powerful but trustworthy. The hard constraint is abstract complexity becoming legible.

| Dimension | Teardown |
|---|---|
| Grid | Approx: large 12-column marketing grid with overlapping product artifacts. Diagrams and API blocks often sit beside or behind editorial copy. |
| Spacing | Approx: wide gutters, 64-120px section spacing, dense proof modules embedded inside airy sections. |
| Typography | High-polish sans hierarchy, large display headings, small mono for API and developer proof. Gradient text is used as typographic accent, not page wallpaper. |
| Motion | Diagram/path reveals and hover layers can be 300-700ms; controls still need 150-250ms. |
| Density | Medium. Marketing is airy, but proof surfaces show real data/API/accounting pressure. |
| Hard Constraint | Must serve founders, finance, and developers at once. The page has to braid trust, API clarity, and ambition. |
| Motion Path | Category promise -> evidence diagram/API -> business outcomes -> trust/compliance -> CTA. |
| Tokens To Extract | Gradient headline, diagram lines, API proof card, nested product screenshots, financial blue palette. |

## Vercel

**What it solves:** Vercel must feel like the native home for frontend builders. The hard constraint is developer credibility plus launch energy.

| Dimension | Teardown |
|---|---|
| Grid | Approx: stark black/white modules, product proof, terminal/code surfaces, hard rectangular sections. Launch pages use bento modules with strong size contrast. |
| Spacing | Approx: 24/32px module gutters, large hero whitespace, tight code/terminal interior padding. |
| Typography | Geist-style neutral sans and mono. Large display can be very simple because proof surfaces carry complexity. |
| Motion | Snappy and technical. Page should avoid floaty brand animation unless tied to building/deploying. |
| Density | Medium-high for developer proof, low for stark brand moments. |
| Hard Constraint | Developers detect fake technical pages immediately. Terminal/code/build proof must look structurally real. |
| Motion Path | Build promise -> code/deploy proof -> framework ecosystem -> scale/trust -> start building. |
| Tokens To Extract | Pure black sections, mono proof, hard bento, dot/grid construction, one accent on active state. |

## Family

**What it solves:** Family needs to make crypto/wallet behavior feel human, premium, and safer than the category stereotype.

| Dimension | Teardown |
|---|---|
| Grid | Approx / 待核实: editorial product-story grid, app/device surfaces, large object moments, fewer dense modules. |
| Spacing | Approx: generous whitespace, 48-96px story sections, product screenshots with strong art direction. |
| Typography | Consumer-premium sans, more lifestyle/product story than enterprise SaaS. |
| Motion | Smooth product transitions, likely 300-600ms. Should feel tactile rather than technical. |
| Density | Low-medium. Complexity is hidden behind object and story. |
| Hard Constraint | Crypto products must reduce perceived risk without becoming bank-like or boring. |
| Motion Path | Identity/product object -> safety/control concept -> app proof -> everyday use -> download/CTA. |
| Tokens To Extract | App-as-object staging, softer premium palette, human-scale copy, controlled product animation. |

## Arc

**What it solves:** Arc must sell a new browser behavior. The hard constraint is explaining a changed mental model without feeling like enterprise onboarding.

| Dimension | Teardown |
|---|---|
| Grid | Approx: consumer product storytelling, browser chrome as hero object, feature sections that show interaction/state. |
| Spacing | Approx: large story beats, device/browser screenshots at strong scale, short copy blocks. |
| Typography | Friendly modern sans, less sterile than developer tools. |
| Motion | Product demonstrations need spatial continuity: sidebar, tab, canvas, and command movement should be comprehensible. |
| Density | Medium-low. Each section should teach one behavior. |
| Hard Constraint | The product changes habits. The page must reduce anxiety by showing the new interaction in context. |
| Motion Path | New browser promise -> visual model -> feature behavior -> migration confidence -> download. |
| Tokens To Extract | Browser chrome framing, feature-as-interaction, soft but precise motion, consumer trust copy. |

## Apple Vision Pro Product Page

**What it solves:** Apple must make a new device category feel inevitable and tangible. The hard constraint is explaining spatial computing with extremely controlled spectacle.

| Dimension | Teardown |
|---|---|
| Grid | Approx: full-bleed cinematic sections alternating with centered product copy and image-led proof. Layout often gives one idea the whole viewport. |
| Spacing | Approx: very large vertical rhythm, 120px+ section spacing on desktop, minimal competing elements. |
| Typography | Apple-style system typography, very large display with simple copy. Weight, leading, and contrast do the work. |
| Motion | Scroll-tied reveals, product rotations, fades, and video transitions. Motion is slower than SaaS UI and must feel physically grounded. |
| Density | Low per viewport, high across the full story. One concept at a time. |
| Hard Constraint | Hardware must be shown as real, desirable, and understandable; excessive UI overlays would reduce luxury. |
| Motion Path | Object awe -> use cases -> interface concept -> technical proof -> purchase/learn. |
| Tokens To Extract | Full-bleed product media, single-idea sections, large type restraint, physically plausible scroll motion. |

## Rauno

**What it solves:** Rauno's site/work must communicate craft through interaction details. The hard constraint is making minimal surfaces feel alive and exact.

| Dimension | Teardown |
|---|---|
| Grid | Approx / 待核实: sparse personal portfolio grid, interaction prototypes and writing arranged with strong negative space. |
| Spacing | Approx: restrained 8px system, generous page margins, small elements allowed to breathe. |
| Typography | Minimal sans with careful weights and tiny labels. Personality comes from motion and detail rather than decorative type. |
| Motion | Core asset. Micro-interactions should feel spring-like, interruptible, and physically coherent. |
| Density | Low-medium. Each interaction detail is isolated enough to be noticed. |
| Hard Constraint | A craft portfolio must prove taste directly; generic portfolio templates would fail. |
| Motion Path | Quiet index -> interaction artifact -> detail inspection -> credibility through craft. |
| Tokens To Extract | Tiny controls, hover physics, understated canvas, "one detail at a time" pacing. |

## Igloo

**What it solves:** Igloo-style studio pages need to show digital craft, technical confidence, and art direction without becoming an agency template.

| Dimension | Teardown |
|---|---|
| Grid | Approx / 待核实: likely project-led canvases, strong visual modules, kinetic transitions, and case-study pacing. |
| Spacing | Approx: large visual stages, varied section rhythm, project imagery gets priority over text blocks. |
| Typography | Studio-grade sans/display pairing; likely restrained labels plus strong project titles. |
| Motion | Higher than SaaS. Page transitions and scroll choreography can be part of the brand, but must not obscure content. |
| Density | Variable. Low for impact scenes, medium for project proof/case study details. |
| Hard Constraint | Must prove taste and execution fast. A normal agency grid feels interchangeable. |
| Motion Path | Visual hook -> project evidence -> craft/process -> client/result -> contact. |
| Tokens To Extract | Case-study staging, kinetic section transitions, image-led hierarchy, variable rhythm. |

## Extraction Notes For The Main Controller

1. Use browser measurement for exact values: container widths, CSS variables, radius, type sizes, transform durations, easing curves.
2. Compare visual token vs CSS token. If the site looks restrained but CSS has many colors, identify which colors actually appear above the fold.
3. Capture viewport screenshots at desktop and mobile. A world-class layout should preserve the same hierarchy, not just stack blocks.
4. Extract motion from DevTools Performance or computed styles where possible. If animations are JS-driven, record observed duration and easing as approx.
5. Do not copy brand assets. Extract grammar: grid, rhythm, proof placement, density, motion relationship, and signature move.

