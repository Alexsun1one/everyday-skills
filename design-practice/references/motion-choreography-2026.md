---
type: reference
created: 2026-06-28
priority: P0
scope: motion design, CSS animation, UI choreography
sources:
  - https://developer.chrome.com/docs/web-platform/view-transitions/
  - https://developer.chrome.com/docs/web-platform/view-transitions/cross-document
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations
  - https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@starting-style
  - https://developer.mozilla.org/en-US/docs/Web/CSS/transition-behavior
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
---

# Motion Choreography 2026 - motion with purpose, hierarchy, and causality

World-class motion does not mean "everything fades in." It means motion explains the interface.

Motion has three jobs:
1. Orient: show where the user came from and where the object went.
2. Give feedback: acknowledge a press, drag, submit, load, save, or failure.
3. Show causality: make one state feel caused by the previous state.

If an animation does none of those, remove it.

## Motion tokens

| Token | Duration | Easing | Use |
| --- | ---: | --- | --- |
| `instant-feedback` | `80-120ms` | `cubic-bezier(.2,0,0,1)` | Button press, row hover, selected state. |
| `micro` | `120-180ms` | ease-out | Toggle, chip change, tooltip, status pill. |
| `standard` | `180-250ms` | `cubic-bezier(.16,1,.3,1)` | Dropdown, popover, tab panel, list insert. |
| `large` | `250-350ms` | ease-out or spring | Drawer, modal, page transition, shared element. |
| `ambient` | `1.4-2.4s` loop | linear or ease-in-out | Skeleton sheen, generating shimmer, progress. |

Default rule: `150-250ms` for most UI. Faster for feedback, slower only when a large surface changes.

## Principles

### Purpose first

Every animation must answer:
- What changed?
- What object owns the change?
- Where did it come from?
- What should the user understand after the motion?

Bad: every section fades up because it entered the viewport.

Good: a newly created issue slides into the top of the list; the row flashes subtly; the count increments with tabular numbers. The motion says "your object now exists here."

### Ease-out for entrances

Entrances should start with momentum and settle. Use `ease-out` or a spring with low bounce. Linear timing is for clocks, progress bars, and infinite loops, not UI state changes.

```css
:root {
  --ease-out-premium: cubic-bezier(.16, 1, .3, 1);
  --ease-standard: cubic-bezier(.4, 0, .2, 1);
}
```

### Transform and opacity first

Animate `transform` and `opacity`. They are the default compositor-safe pair.

Avoid animating `top`, `left`, `width`, `height`, `margin`, and layout-dependent `filter` effects in high-frequency interactions. If a layout property must change, isolate it, keep it short, and verify in Chrome DevTools Performance.

### Stagger with hierarchy

Stagger is not confetti. Use it when a group has an order:
- Command menu results: `20-30ms` per row.
- Feature trio: lead element first, supporting items `40-60ms` apart.
- Toast stack: newest first.

Never stagger twenty cards on every scroll. The user came to read, not watch a parade.

### Respect reduced motion

`prefers-reduced-motion` is not optional. Replace spatial motion with opacity, instant state change, or a static affordance. Keep progress indicators that convey real progress, but remove decorative scale, parallax, and long travel.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    scroll-behavior: auto !important;
  }

  [data-motion="decorative"],
  .scroll-reveal,
  .parallax-layer {
    animation: none !important;
    transition: none !important;
    transform: none !important;
  }
}
```

Source: [MDN prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion).

## Modern techniques

### View Transitions API

Use View Transitions when the user needs visual continuity between two UI states.

Best uses:
- Gallery card to detail page.
- Product screenshot thumbnail to full-size screenshot.
- Kanban card moving between columns after filter/sort.
- Multi-page docs or marketing pages where same-origin navigation should feel spatial.

Same-document transition:

```js
function updateView() {
  if (!document.startViewTransition) {
    applyStateChange();
    return;
  }

  document.startViewTransition(() => applyStateChange());
}
```

Shared element:

```css
.issue-row[data-id="ENG-2703"] {
  view-transition-name: issue-eng-2703;
}
```

Cross-document transitions are now practical for same-origin multi-page apps. Both pages opt in with CSS:

```css
@view-transition {
  navigation: auto;
}
```

Chrome's docs describe same-document support from Chrome 111 and cross-document support from Chrome 126. Cross-document transitions are same-origin and opt-in. Sources: [Chrome View Transitions overview](https://developer.chrome.com/docs/web-platform/view-transitions/), [cross-document View Transitions](https://developer.chrome.com/docs/web-platform/view-transitions/cross-document).

Design discipline:
- Name only the objects that need continuity.
- Do not transition the whole page if only one object changed.
- Disable or simplify under reduced motion.
- Do not use a shared element if the source and destination are conceptually different objects.

### CSS scroll-driven animations

Use scroll-driven animations for scroll progress, reading indicators, pinned explanations, and subtle section-linked transforms. They are not a license to animate every block.

```css
.progress {
  transform-origin: left;
  animation: grow linear both;
  animation-timeline: scroll(root block);
}

@keyframes grow {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
```

Use `view()` timelines when the subject's visibility should drive the animation:

```css
.section-figure {
  animation: settle both ease-out;
  animation-timeline: view(block);
  animation-range: entry 10% cover 35%;
}

@keyframes settle {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}
```

MDN notes that scroll-driven animations animate along a scroll-based timeline rather than the default time-based document timeline, and that `animation-timeline` can use scroll progress or view progress timelines. Sources: [MDN scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations), [MDN animation-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline).

Design discipline:
- Use for one narrative mechanism per page, not every section.
- Add `@supports` fallback.
- Keep text readable if the animation does not run.
- Never make critical content depend on scroll animation completion.

### Spring vs cubic-bezier

Use cubic-bezier when:
- The transition is deterministic UI: tooltip, dropdown, tab switch, popover, toast.
- The animation should feel precise and quiet.
- You can express it with `transform` and `opacity` in CSS.

Use spring when:
- The user directly manipulates the object: drag, swipe, resize, reorder.
- The element is a shared object moving across space.
- You need interruption and velocity inheritance.

Spring rules:
- Low bounce for professional SaaS.
- Higher bounce only for consumer delight and small objects.
- Always interruptible.
- Never use spring for high-frequency typing, table updates, or critical enterprise flows.

### Shared-element transitions

Shared-element motion is the strongest way to show causality. A card becomes a detail view. A small avatar becomes a profile header. A screenshot expands into a modal.

Pattern:
1. User clicks source object.
2. Source object keeps identity through `view-transition-name`.
3. Destination shows the same object at higher detail.
4. Secondary content fades or slides after the shared object lands.

Bad: everything crossfades at once.

Good: the object travels, then the supporting UI follows.

### `@starting-style` and `transition-behavior: allow-discrete`

Use these for elements that enter from `display: none`, top layer, popover, dialog, or DOM insertion. They remove the old hack of keeping invisible elements mounted only to animate them.

```css
[popover] {
  opacity: 0;
  transform: translateY(6px) scale(.98);
  transition:
    opacity 180ms var(--ease-out-premium),
    transform 180ms var(--ease-out-premium),
    display 180ms allow-discrete,
    overlay 180ms allow-discrete;
}

[popover]:popover-open {
  opacity: 1;
  transform: translateY(0) scale(1);
}

@starting-style {
  [popover]:popover-open {
    opacity: 0;
    transform: translateY(6px) scale(.98);
  }
}
```

MDN describes `@starting-style` as starting values for first-style transitions, and `transition-behavior: allow-discrete` as enabling transitions for discrete properties such as `display`. Sources: [MDN @starting-style](https://developer.mozilla.org/en-US/docs/Web/CSS/@starting-style), [MDN transition-behavior](https://developer.mozilla.org/en-US/docs/Web/CSS/transition-behavior).

## The tell: AI motion vs crafted motion

| AI motion | Why it reads as AI | Crafted motion |
| --- | --- | --- |
| Every section uses the same `fade-in-up`. | No hierarchy. The page feels generated by a loop. | Only stateful or high-value moments move. The rest is still. |
| Animation starts when scrolled into view, regardless of meaning. | Viewport entry is not a user intent. | Motion follows action: click, submit, create, filter, navigate. |
| All cards stagger evenly. | The layout has no lead, no supporting cast, no editorial rhythm. | Lead moves first, dependent elements follow, irrelevant elements do not move. |
| Everything lasts `300ms ease`. | Same timing for a chip and a modal destroys scale. | Duration scales with object size and frequency. |
| Decorative parallax and floating blobs. | Motion is compensating for weak content. | Product objects move: rows, panels, values, previews, handles. |
| No reduced-motion branch. | Accessibility is missing from the craft. | Motion gracefully collapses to opacity or instant state. |
| `transition: all`. | Sloppy implementation, accidental layout animation. | Explicit properties, mostly `transform` and `opacity`. |

The hard question: "If I remove this motion, what understanding disappears?" If the answer is "none," remove it.

## Exemplars and what to copy

### Family

[Family](https://family.co/) makes a complex crypto wallet feel approachable by turning activity, onboarding, asset organization, transaction analysis, and monitoring into understandable product moments. Their site explicitly sells "Wallet activity you can understand," "Details that matter," real-time monitoring, and micro-interactions.

Copy:
- Motion should reduce fear in complex domains.
- Transaction state changes need continuity, not theatrical flair.
- Onboarding motion should add meaning to the step, not only speed it up.

### Linear

[Linear](https://linear.app/) uses dense product objects: issues, cycles, labels, activity, diffs, agents, dashboards. The current homepage shows real-feeling issue IDs, labels, owners, project status, and agent workflows rather than generic feature cards.

Copy:
- Motion belongs to product operations: create issue, triage, move status, review diff.
- The product's speed promise means feedback must be immediate and quiet.
- Dense UI should use micro motion, not page-wide spectacle.

### Vercel

[Vercel](https://vercel.com/) is restrained, technical, and architectural. The homepage organizes product families and platform concepts rather than decorating every block.

Copy:
- Use one or two signature transitions for the technical story.
- Keep the rest crisp. White/black technical surfaces look worse when over-animated.
- Motion should reveal infrastructure relationships, not swirl around them.

### Stripe

[Stripe](https://stripe.com/) uses modular product storytelling, concrete financial numbers, customer proof, and the slanted brand motif. Their current page foregrounds payments volume, uptime, currencies, subscriptions, APIs, and customer case studies.

Copy:
- Motion can connect system scale to business proof.
- Use data and real modules as moving objects.
- A restrained brand motif beats generic fades.

### Arc

[Arc](https://arc.net/) frames the browser as a calm, personal place with Spaces, Profiles, Split View, Themes, privacy, and setup. Its motion language should be spatial because the product is spatial.

Copy:
- Navigation motion should preserve the sense of place.
- Playfulness works when it is tied to browser organization.
- Do not confuse cute motion with causal motion.

### Raycast

[Raycast](https://www.raycast.com/) sells "Your shortcut to everything" and calls itself fast, ergonomic, reliable. A launcher cannot afford decorative latency.

Copy:
- Keyboard-first products need instant feedback, not cinematic transitions.
- The best motion may be a 100ms highlight, a command result settle, or a progress hint.
- The user's mental flow is more important than visual flourish.

## Motion self-test checklist

- [ ] Every animation has a purpose: orient, feedback, or causality.
- [ ] No page-wide "all sections fade up" pattern.
- [ ] Entrances use ease-out; exits are faster or quieter.
- [ ] Feedback appears under `100ms`.
- [ ] Most UI motion stays `150-250ms`; large surfaces stay under `350ms`.
- [ ] Only `transform` and `opacity` animate in frequent interactions.
- [ ] No `transition: all` on product surfaces.
- [ ] Stagger exists only where order matters.
- [ ] Shared-element transitions are used only for the same conceptual object.
- [ ] View Transitions API has a fallback for unsupported browsers.
- [ ] Scroll-driven animation is progressive enhancement; content is readable without it.
- [ ] Popovers/dialogs/top-layer elements use `@starting-style` and `allow-discrete` when needed.
- [ ] Reduced-motion mode removes parallax, long travel, and decorative motion.
- [ ] One interaction trace was recorded in DevTools Performance.
- [ ] The page still feels premium when all decorative motion is disabled.
