---
type: reference
created: 2026-06-28
priority: P0
pairs-with: references/craft-details-invisible.md · tooling/behavior-audit.mjs
source: Emil Kowalski (animations), Rauno Freiberg (invisible details), Linear / Stripe / Vercel / Family interaction craft
---

# Liveness — the micro-interactions that make a UI feel alive (not a static facade)

> The behavior gate proves a control *works*. This layer is the next bar: does it feel **alive** — does it respond to your presence, your press, your wait? This is the world-class layer (Linear/Stripe/Vercel/Rauno/Emil). Sun's words: "鼠标移上去有个轻微变化 · 一道亮光从左到右很克制地划过去 · 文字上那种". Each below has a name, a technique, a "when", and the discipline. **Restraint is the rule — one or two alive moments per surface, never everywhere.**

## The principle
A great UI is **responsive to the human in three moments**: when you **approach** it (hover), when you **act on** it (press/focus), and when you **wait** for it (loading/working). Dead UI ignores all three. The craft is to acknowledge each — subtly, with ease-out timing — so the interface feels like it's *paying attention*.

---

## 1. Hover micro-feedback (响应在场)
Every interactive element must change *something* on hover — bg lighten, border firm up, a 1px lift, a faint glow, an icon nudge, the accent warming. Not for decoration: it tells the user "this is reachable." The amount is tiny; the timing is everything.
```css
.row { transition: background-color 120ms cubic-bezier(.4,0,.2,1); }
.row:hover { background: var(--surface-hover); }
.btn { transition: background-color 120ms ease-out, transform 120ms ease-out, box-shadow 120ms ease-out; }
.btn:hover { background: var(--btn-bg-hover); box-shadow: var(--hl); }
.card:hover { transform: translateY(-2px); box-shadow: var(--shadow-lift); } /* the "lift" */
```
- **Audit test:** hover the element → did *any* computed value change (bg/border/color/transform/shadow/opacity)? No change = no feedback = flag.
- Rauno's rule: feedback **during** interaction signals "this is possible," not just on completion.

## 2. Shimmer / sheen sweep (掠光 — the light that slides across)
A restrained highlight that travels **left→right** across an element. Two uses: **skeleton loaders** (content pending) and **"working / syncing / processing"** states (a task running). Restraint = low-opacity, slow (~1.4–2s), no color, just a soft sheen.
```css
/* skeleton */
.skeleton { position: relative; overflow: hidden; background: var(--surface-2); border-radius: 6px; }
.skeleton::after {
  content: ""; position: absolute; inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,.06), transparent);
  transform: translateX(-100%);
  animation: sweep 1.6s cubic-bezier(.4,0,.2,1) infinite;
}
@keyframes sweep { to { transform: translateX(100%); } }   /* transform-only = GPU-safe */
```
- For a "working" chip/bar, same sweep at even lower opacity over the accent. **It must stop under `prefers-reduced-motion`** (swap to a static dim state).
- Why transform-not-background-position: composited, no repaint (see craft-details).

## 3. Gradient text shimmer (文字掠光 — the "thinking/generating" text)
The AI-working / processing label: a soft highlight sweeps across the *text* itself. Restrained, monochrome-ish, slow.
```css
.working-text {
  background: linear-gradient(90deg, var(--text-faint) 30%, var(--text) 50%, var(--text-faint) 70%);
  background-size: 200% 100%;
  -webkit-background-clip: text; background-clip: text; color: transparent;
  animation: text-sheen 2.2s ease-in-out infinite;
}
@keyframes text-sheen { to { background-position: -200% 0; } }
@media (prefers-reduced-motion: reduce){ .working-text { animation: none; color: var(--text-faint); } }
```
- Use ONLY for genuine in-progress states ("Generating…", "Syncing…"). Never decorative.

## 4. Cursor-follow spotlight (活的表面 — Linear/Vercel hero cards)
A faint radial glow that follows the cursor across a card/surface. Makes a flat panel feel responsive and premium. JS tracks the pointer into a CSS var; the glow is a `radial-gradient` at that point.
```js
card.addEventListener('pointermove', e => {
  const r = card.getBoundingClientRect();
  card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
  card.style.setProperty('--my', (e.clientY - r.top) + 'px');
});
```
```css
.card::before { content:""; position:absolute; inset:0; opacity:0; transition:opacity 200ms ease-out;
  background: radial-gradient(220px circle at var(--mx) var(--my), rgba(255,255,255,.06), transparent 70%); }
.card:hover::before { opacity:1; }
```
- One signature surface per page, not all of them.

## 5. Press feedback (触感)
On `:active`, a tiny `scale(.97–.98)` + one step darker; springs back on release. The element feels physically pressed. (Remove from high-frequency keyboard-repeat actions.)
```css
.btn:active { transform: scale(.98); }
```

## 6. Focus glow (crafted focus-visible, never removed)
Keyboard focus gets a crafted ring (offset + radius matched), optionally a faint glow. This is accessibility AND liveness.
```css
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.input:focus-visible { box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 30%, transparent); }
```

## 7. Staggered entrance (编排感)
Lists/cards enter with a small per-item delay (≤60ms step) — choreographed, not all-at-once. One reveal, not on every scroll. Off under reduced-motion (content visible by default — see the reveal-gating lesson).

## 8. State-change transition (不硬切)
When data changes (a status pill flips, a number updates, a tab switches) — cross-fade/slide the change over ~150ms, don't hard-swap. A value that updates uses `tabular-nums` so it doesn't reflow.

## The discipline (or it becomes noise)
- **ease-out**, feedback **≤200ms** (ambient loops like sweep/sheen may be 1.4–2.2s); **transform/opacity only**; **interruptible**; **always `prefers-reduced-motion`-guarded**; **never** on keyboard-repeat / high-frequency actions.
- **Restraint:** approach + act + wait, acknowledged subtly. One or two *signature* alive moments (a spotlight surface, a sheen) — the rest is quiet feedback. Liveness everywhere = a casino.

## Liveness audit (extends the behavior gate)
- [ ] Every interactive element changes on **hover** (auto-checkable: hover → computed style delta).
- [ ] **Press** feedback on primary controls (`:active` scale/darken).
- [ ] **focus-visible** crafted, never removed.
- [ ] Loading uses a **skeleton sweep**, not a bare spinner / nothing.
- [ ] "Working/processing" states have a **restrained sheen or text-shimmer**, not a frozen label.
- [ ] One **signature** alive moment (cursor-spotlight / choreographed entrance) — exactly one or two.
- [ ] **All** of it disabled/calmed under `prefers-reduced-motion`.
- [ ] Nothing animates a keyboard-repeat / high-frequency action.

> `tooling/behavior-audit.mjs` now checks the hover-delta automatically (does hovering actually change the element?) — a dead-static element that never responds to the cursor is flagged the same way a dead button is. The felt timing/呼吸感 of these is judged by **driving + recording motion** (`drive.mjs`), never a still.
