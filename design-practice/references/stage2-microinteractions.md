# Stage 2 — Micro-interaction Four-Pack (trigger / rule / feedback / loop)

> Article line 1439: **"丹·萨法把微交互拆成四个零件:触发、规则、反馈、循环."** Hover-only-changes-color is the plastic tell. This file is the four-pack spec for every interaction.

## Why

Article line 1437: **"微交互就是那些很小、但会让人觉得'这个产品懂我'的细节. 开关的圆点滑过去,点赞的心轻轻跳一下,拖拽卡片时影子变深,输入错误时字段轻微震动,上传文件时进度一点一点走. 这些东西用户未必能说出来,但会感觉产品'顺'."**

AI skips micro-interactions because they're invisible in a screenshot. They're the difference between "looks like Linear" and "feels like Linear".

## The four-pack

Every micro-interaction decomposes into:

```
TRIGGER  →  RULE  →  FEEDBACK  →  LOOP/MODE
触发        规则     反馈         循环/模式
```

### Trigger (触发)
What starts it. A user action (click, hover, focus, type, drag) or a system event (data arrived, timer fired, error occurred).

### Rule (规则)
What should happen, logically. "On submit, validate; if valid, save; if invalid, mark errors." The rule is the contract — it's what the interaction promises.

### Feedback (反馈)
What the user perceives. Visual (color, scale, position), audio (rarely), haptic (mobile), copy (status text). Feedback must be **immediate** (under 100ms) and **honest** (don't show success before success).

### Loop / Mode (循环/模式)
What continues or changes scope. A loop runs repeatedly (progress bar updating). A mode changes the rules temporarily (drag-mode, edit-mode, selection-mode).

## Worked examples

### Button press

```
TRIGGER:  pointerdown on button
RULE:     enter pressed state; on pointerup, fire onClick
FEEDBACK: bg darken 16% (color.state.active), scale 0.98, 100ms ease-out
LOOP:     on pointerup → exit pressed, spring back to default (200ms ease-out)
```

### Toggle switch

```
TRIGGER:  click on toggle
RULE:     flip the state (on↔off); call onChange
FEEDBACK: knob slides 200ms ease-out; track bg changes (gray → blue); tiny shadow on knob
LOOP:     none (one-shot); but the new state persists visually until toggled again
```

### Drag a card (kanban)

```
TRIGGER:  pointerdown on card + move > 4px (avoid click misfire)
RULE:     enter drag-mode; card follows pointer; on drop, check valid zone; if valid, reorder; if invalid, snap back
FEEDBACK: card scale 1.02, shadow lg, opacity 0.9; placeholder shows in drop zone; invalid zone shows red
LOOP:     drag-mode persists until pointerup; card follows pointer in rAF loop
MODE:     while dragging, other interactions disabled (no accidental click on other cards)
```

### Input validation (form field)

```
TRIGGER:  blur on input (NOT on every keystroke — that's naggy)
RULE:     validate value against rules; if invalid, mark error; if valid, mark success
FEEDBACK: border → red (error) or green (success); inline message appears below; if error, field shakes 200ms
LOOP:     re-validate on every input while in error state (so user sees recovery live); exit error on first valid input
```

### Like / heart

```
TRIGGER:  click on heart
RULE:     toggle liked; optimistic update; call API; on failure, rollback
FEEDBACK: heart fills, scales 1.3 → 1.0 with ease-back; tiny particle burst (3 small hearts, optional)
LOOP:     none
```

### File upload

```
TRIGGER:  file selected (drop or pick)
RULE:     start upload; track progress; on done, show file; on error, allow retry
FEEDBACK: progress bar 0→100% in real time; file card appears with skeleton → real; error → red retry
LOOP:     progress updates per frame until complete
MODE:     upload-mode (multiple uploads can queue; each has independent state)
```

### Toast / notification

```
TRIGGER:  system event (save success, error, info)
RULE:     show toast for 4s; stack if multiple; on hover, pause auto-dismiss
FEEDBACK: slide in from top-right, 200ms ease-out; on dismiss, slide out + fade
LOOP:     countdown paused on hover; resumed on leave
MODE:     toast-mode (pointer events pass through except on the toast itself)
```

### Drawer open / close

```
TRIGGER:  click item in list (open) / ESC or click-outside or close-button (close)
RULE:     open: slide in from right, trap focus inside, preserve list state; close: slide out, return focus to trigger
FEEDBACK: drawer slides 240ms ease-out; backdrop fades in 200ms; list stays put
LOOP:     none
MODE:     drawer-mode (focus trapped, Tab cycles inside, ESC closes)
```

## The anti-plastic micro-interaction test

| Plastic (AI default) | Human (this skill) |
| --- | --- |
| hover = bg color change only | hover = color + cursor + 100ms transition |
| no pressed state | pressed = darken + scale 0.98 |
| no drag feedback | drag = scale + shadow + placeholder + snap-back |
| validation on every keystroke | validation on blur, re-validate while in error |
| optimistic update without rollback | optimistic + rollback on failure |
| progress bar with fake animation | progress reflects real bytes uploaded |
| toast auto-dismiss can't be paused | pause on hover |
| drawer without focus trap | focus trap + ESC + focus return |

## Timing tokens (article line 1433)

Borrow from `stage2-design-tokens.md`:

| Action | Duration | Easing |
| --- | --- | --- |
| micro (hover, press, toggle) | 100ms | ease-out |
| small (tooltip, popover, toast) | 200ms | ease-out |
| medium (drawer, modal, expand) | 240ms | ease-out |
| large (page transition) | 300ms | ease-in-out |

Never `linear` except for continuous loops (spinners, progress). Linear feels robotic.

## Reduced motion (article line 1430, accessibility)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

A user who sets reduced-motion gets instant state changes, no slides, no shakes. This is non-negotiable accessibility, not optional polish.

## Failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| Hover-only-color | plastic | four-pack: rule + feedback beyond color |
| No pressed | missing tactile feel | scale 0.98 + darken on `:active` |
| No focus-visible transition | keyboard users lose place | focus ring appears on focus |
| Validation nag | errors on every keystroke | validate on blur, re-validate in error |
| No rollback on optimistic | liked state stuck after API fail | rollback to previous state |
| Linear easing | robotic | ease-out / ease-in-out, never linear |
| No reduced-motion | accessibility fail | `@media (prefers-reduced-motion)` mandatory |
