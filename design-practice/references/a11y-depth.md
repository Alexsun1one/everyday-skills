---
type: reference
created: 2026-06-28
priority: P0
pairs-with: references/qa-a11y.md · references/micro-interactions-liveness.md · tooling/behavior-audit.mjs
covers: quality-landscape.md → F.20 Accessibility depth · D.16 Keyboard & input ergonomics
source: The real audit found focus-trap / keyboard / ARIA gaps that axe did NOT catch (axe stops at contrast & static DOM). W3C WCAG 2.2 (w3.org/TR/WCAG22) and WAI-ARIA Authoring Practices Guide (APG).
---

# A11y Depth — accessibility beyond color contrast (what axe misses)

> `qa-a11y.md` is the *acceptance checklist* (the 7 basics, incl. contrast). This is the *depth layer*: the **WCAG 2.2 criteria and ARIA APG keyboard/focus behavior that automated tools like axe do not catch**, because they require *driving* the UI — opening a dialog, tabbing through tabs, closing an overlay and checking where focus went. The real audit found pages that passed axe but trapped focus, leaked Tab behind a modal, and gave comboboxes no keyboard path. Axe checks the DOM; this checks the **behavior**. Verdict tags: `[auto]` harness can check · `[drive]` must drive the live UI · `[read]` read the code.

## 1. WCAG 2.2 — the newer success criteria (AA unless noted)
These are the 2.2 additions that agents routinely miss, and that the contrast-only audit never touches:
- **2.4.11 Focus Not Obscured (Minimum) [AA]** — when a control receives focus it must not be *entirely* hidden (e.g. behind a sticky header). Fix: `scroll-padding-block-start` on `<html>` and `scroll-margin` on targets so focused/anchored elements clear sticky bars. **2.4.12 (AAA)** = not obscured *at all*.
- **2.5.7 Dragging Movements [AA]** — anything doable by dragging (a slider, a reorder handle, a map pan) must have a **non-dragging alternative** (buttons, arrow keys, +/- steppers). Don't ship drag-only.
- **2.5.8 Target Size (Minimum) [AA]** — ≥ **24×24 CSS px**, with exceptions (inline links, in-sentence, UA-controlled). **2.5.5 Target Size [AAA]** = ≥ **44×44**. Design to 44; never below 24. (Same rule as responsive §5.)
- **3.2.6 Consistent Help [AA]** — if help mechanisms (contact, chat, FAQ) appear on multiple pages, they appear in the **same relative order** each time.
- **3.3.7 Redundant Entry [AA]** — don't make the user re-enter info already provided in the same process (auto-fill or let it carry).
- **3.3.8 Accessible Authentication (Minimum) [AA]** — no cognitive-function test (password, puzzle) without an alternative (passkey, paste, autofill, webauthn). Don't block paste.

## 2. ARIA Authoring Practices (APG) — the required keyboard + focus behavior
The golden rule first: **"No ARIA is better than bad ARIA"** — if native HTML works (`<button>`, `<details>`, `<dialog>`, native `<select>`), use it. ARIA adds *semantics* but **not behavior** — you must wire the keyboard yourself. For each pattern, the behavior below is **non-optional**:

**Dialog / Modal** `[drive]`
- Focus moves **into** the dialog on open; **trapped** within (Tab/Shift+Tab cycles inside, never escapes to the page behind). **Esc** closes it. On close, focus **returns to the element that opened it**.
- `role="dialog"` (or `<dialog>`), `aria-modal="true"`, `aria-labelledby` (title) and `aria-describedby` (description). Inert the background (`inert` attribute on siblings) so it's both unfocusable and hidden from AT.
```js
const last = document.activeElement;          // remember trigger
dialog.showModal();                            // <dialog> traps focus for free + Esc
// …on close:
dialog.close(); last.focus();                  // return focus
```

**Tabs** `[drive]` — **roving tabindex**: only the **active** tab is in the tab order (`tabindex="0"`); the rest are `tabindex="-1"`. **Tab** moves focus out to the panel — it does **not** move between tabs. Between tabs you move with **Left/Right arrows** (Up/Down if vertical), **Home/End** to first/last. Activation follows focus (auto) or on **Space/Enter** (manual). Each tab `aria-controls` its panel; the active tab `aria-selected="true"`; the panel `role="tabpanel"` + `aria-labelledby`.
```html
<div role="tablist">
  <button role="tab" id="t1" aria-selected="true" aria-controls="p1" tabindex="0">Overview</button>
  <button role="tab" id="t2" aria-selected="false" aria-controls="p2" tabindex="-1">Activity</button>
</div>
<div role="tabpanel" id="p1" aria-labelledby="t1" tabindex="0">…</div>
```

**Combobox / Autocomplete** `[drive]` — input is focusable and in tab order. **Alt+Down** opens the list; **Down/Up** moves the highlighted option (use **`aria-activedescendant`** to point at it, keeping focus in the input); **Enter** selects; **Esc** closes without selecting; typing filters. `role="combobox"` + `aria-expanded` on the input; `aria-controls` → the `role="listbox"`; each option `role="option"` + `aria-selected`.

**Disclosure / Accordion** `[drive]` — header is a `<button>` with `aria-expanded` and `aria-controls` → the panel id. **Enter/Space** toggles. (Prefer native `<details>`/`<summary>` — semantics, keyboard, and focus are free.)

**Menu / Menubar** `[drive]` — arrow keys navigate between `role="menuitem"`s; **Enter/Space** activates; **Esc** closes and returns focus to the trigger. Reserve `role="menu"` for genuine application menus (File/Edit-style) — **not** for site navigation (a `<nav>` + links is correct there; misusing `menu` breaks it for SR users).

**Tooltip** `[read]` — `role="tooltip"`, associated to its trigger via `aria-describedby`. Must appear on **focus as well as hover** (keyboard users exist), and dismiss on **Esc** / blur. A hover-only tooltip is invisible to keyboard and most screen readers.

## 3. Focus management
- **`:focus-visible`**, never bare `:focus` removed — show the ring only for keyboard/programmatic focus, not mouse clicks. `:focus-within` styles a container when any descendant is focused (good for inputs-with-icons).
- **Never `outline: none` without a replacement.** Modern move: don't touch `outline` at all; if you craft a custom ring, ensure it meets **Focus Appearance** (≥ 2 CSS px, ≥ 3:1 contrast against adjacent colors) and is visible on every background (use `outline-offset` + a ring color that contrasts both).
- **Logical tab order = DOM order.** Don't fight it with positive `tabindex` (it is an anti-pattern and a maintenance trap). Reorder the DOM instead. Use `tabindex="0"` for focusable custom widgets, `tabindex="-1"` for elements you focus programmatically (moving into a dialog, skip-to targets).
- **Skip-link** as the first focusable element: "Skip to main content" → jumps to `<main id="main" tabindex="-1">`. Visually hidden until focused.
- **Focus-return on overlay close** (modal/drawer/menu) — see Dialog. This is the #1 thing axe misses and the #1 thing users feel.
- **One `<main>`.** Don't nest or repeat it.

## 4. Keyboard-complete operation
Everything a mouse can do, the keyboard can do too — and at the **same granularity** (no "keyboard works but only the primary action"). `[drive]` test: put the mouse away and complete the core 动线 (open → fill → submit → see result → undo/cancel). If any step needs a pointer, it fails. No `:hover`-only reveals (responsive §5), no drag-only (2.5.7), no `onclick` on a `<div>` (use `<button>` — it gives focus + Enter/Space for free).

## 5. Screen-reader semantics — landmarks, headings, live regions
- **Landmarks** via native elements: `<header>`/`<footer>`, `<nav>` (give it `aria-label` when there's more than one), `<main>`, `<aside>`, `<form>`, `<search>`. They let SR users jump by region.
- **Heading order never skips** (`h1` → `h3` is a failure). One `h1` per view; use level to reflect structure, not size (size is CSS).
- **Name / Role / Value (4.1.2):** every interactive element exposes all three. Icon-only buttons need an `aria-label`; status pills need a role or implicit name.
- **`aria-live` regions for async/toasts:**
  - `role="status"` (= `aria-live="polite"`) — non-urgent: "Saved", "3 results", loading-complete. Announced when the user pauses.
  - `role="alert"` (= `aria-live="assertive"`) — urgent: form errors, "Connection lost." Use sparingly — assertive interrupts.
  - Inject the node (or toggle its text) **after** it's in the live region, or the SR may not announce it.
- **`aria-busy="true"`** on a region mid-update so the SR doesn't read a half-loaded mess; clear it when done. Tie to your skeleton states (`micro-interactions-liveness.md`).

## 6. `prefers-reduced-motion` — honored for ALL motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important; animation-iteration-count: 1 !important;
    transition-duration: .01ms !important; scroll-behavior: auto !important;
  }
}
```
No parallax, no auto-carousel, no infinite shimmer/sweep for users who opted out — swap to a static, equally-informative state. Motion must never be the **only** way information is conveyed (pair every motion cue with text/icon).

## 7. Forms a11y — labels, hints, errors, summary
```html
<label for="email">Email</label>                       <!-- every input has a label -->
<input id="email" type="email" required
       aria-describedby="email-hint email-err"
       aria-invalid="true">                             <!-- set when validation fails -->
<p id="email-hint">We'll never share it.</p>
<p id="email-err" role="alert">Enter a valid email address.</p>
```
- **`<label for="id">`** (or wrap the input in the label). Placeholder is **never** a label — it vanishes on input and fails contrast.
- **`aria-describedby`** links the input to its hint **and** its error message.
- **`aria-invalid="true"`** on fields that failed; **`required`** / `aria-required="true"` for mandatory.
- **Error summary** at the top of the form on submit failure (a list, each error linking/anchoring to its field), announced via `role="alert"` or `aria-live`. Don't scatter errors a screen-reader user has to hunt for. Validate on submit (and optionally on blur), not on every keystroke.

## Self-test checklist — mapped to what can verify it
```
WCAG 2.2
□ Focused control never entirely hidden behind sticky header          [drive]  2.4.11
□ scroll-padding/scroll-margin set so focus clears sticky bars         [read]
□ Every drag interaction has a non-drag alternative (keys/buttons)     [drive]  2.5.7
□ All targets ≥ 24px; aim 44px                                        [auto]   2.5.8
□ Help/contact/chat in consistent order across pages                  [read]   3.2.6
□ No re-entry of already-given info; paste allowed on auth            [drive]  3.3.7/.8

APG behavior (axe CANNOT catch these — must drive)
□ Modal: Tab cycles inside (never escapes), Esc closes, focus returns  [drive]
□ Background inert/unfocusable while a modal is open                  [drive]
□ Tabs: roving tabindex, arrows move, Tab exits to panel              [drive]
□ Combobox: opens, arrow-navigates, Enter selects, Esc cancels        [drive]
□ Disclosure: Enter/Space toggles, aria-expanded set                  [drive]
□ Menus: arrows navigate, Esc closes + returns focus                  [drive]
□ Tooltips appear on focus (not hover-only), Esc dismisses            [read]

Focus & keyboard
□ :focus-visible used; no bare outline:none w/o replacement           [read]
□ Focus ring ≥3:1 contrast, visible on every background               [auto]
□ Tab order == visual/DOM order; no positive tabindex                 [drive]
□ Skip-link present, first focusable, targets <main tabindex=-1>      [read]
□ Core 动线 completable with mouse disabled                           [drive]

Semantics & live regions
□ Landmarks present; exactly one <main>                               [auto]
□ Headings don't skip levels; one h1                                  [auto]
□ Icon-only controls have aria-label; status has role/name            [auto]
□ Toasts/async use role=status (polite) or role=alert (assertive)     [read]
□ Updating regions set aria-busy mid-fetch, cleared after             [read]

Motion & forms
□ prefers-reduced-motion media query; all motion calmed               [read]
□ Motion never the sole carrier of info                              [see]
□ Every input has a <label>; placeholder is not the label             [auto]
□ Errors: aria-invalid + aria-describedby + a top error summary       [read]
```

## Sources
- **WCAG 2.2** — `w3.org/TR/WCAG22` (the AA criteria cited above). How to Meet WCAG (Quick Reference): `w3.org/WAI/WCAG22/quickref`.
- **WAI-ARIA Authoring Practices Guide (APG)** — `w3.org/WAI/ARIA/apg/patterns` — the canonical keyboard + ARIA behavior for Dialog, Tabs, Combobox, Disclosure, Menu, Tooltip. This is the source of truth for §2.
- **"No ARIA is better than bad ARIA"** + the five rules of ARIA — `w3.org/WAI/ARIA/apg/practices`.
- Real products to study: **Linear** (keyboard-first, `⌘K`, focus craft), **Vercel** (forms + toasts + reduced-motion), **Stripe** (dialog/drawer focus-return, error summaries), **GitHub** (tabs, menus, skip-link).
- Tools: **axe DevTools** (catches contrast + static DOM — the floor), **WAVE**, **Lighthouse a11y** (automated only), plus **NVDA / VoiceOver** and a **keyboard-only** pass for everything tagged `[drive]` (the layer axe can't reach).

> **Integration:** this is the craft behind `quality-landscape.md` §20 (Accessibility depth) and §16 (Keyboard & input ergonomics), and the keyboard/focus half of `behavior-audit.mjs`. The acceptance pass lives in `qa-a11y.md`. The rule the harness can't see: **axe passing ≠ accessible.** Open every modal, tab through every pattern, close it, and check where focus lands — that `[drive]` pass is where the real gaps live.
