# Stage 2 — Button 8 States (the loudest human-made evidence)

> Buttons are where users decide if a UI feels human or plastic. This file is the 8-state spec — the strongest "a human made this" signal in the whole skill.

## Why

Article line 1281: **"一个按钮至少要有默认、悬停、按下、聚焦、禁用、加载、成功、失败这些状态. 不要只画默认态. 默认态是天气晴朗的时候,状态才是下雨、堵车、停电、信号差的时候."**

Article line 766: **"自定义按钮必须有'按下'状态:你按下去,它得有反应,哪怕只是颜色暗一下. 没反应,用户就会怀疑'我是不是没点上?'."**

Article line 1285: **"很多 AI 生成的界面为了干净,把 focus ring 直接去掉. 截图是干净了,用键盘的人就没路走了."**

The 8 states are non-negotiable. A button with only default + hover is an AI-plastic button.

## The 8 states

| # | State | Visual | Copy | Behavior | CSS hint |
|---|---|---|---|---| --- |
| 1 | **default** | `button.primary.bg` | label, e.g. "Save" | clickable, cursor pointer | base |
| 2 | **hover** | bg darken 8% (`color.state.hover`) | same | cursor pointer, 100ms transition | `:hover` |
| 3 | **active (pressed)** | bg darken 16% (`color.state.active`), scale 0.98 | same | pressed feedback, spring back on release | `:active` |
| 4 | **focus** | 2px ring outside, `color.border.focus` (NEVER removed) | same | keyboard reachable, focus-visible | `:focus-visible` |
| 5 | **disabled** | 40% opacity, no shadow, cursor not-allowed | same + tooltip explaining why | NOT clickable, aria-disabled | `[disabled]` + tooltip |
| 6 | **loading** | spinner (16px) left of label, bg unchanged | label → "Saving…" | BLOCK re-click (the article's P0 bug: repeat-submit double-charge) | `aria-busy="true"`, `pointer-events: none` |
| 7 | **success** | flash green border/bg 200ms → back to default | toast: "Saved" | confirm done, allow next action | transition + toast |
| 8 | **error** | shake 200ms (3px horizontal), focus ring red | inline: "Save failed — retry" | keep input, allow retry, DON'T lose draft | shake animation + inline error |

## The anti-plastic tells

| Plastic button (AI default) | Human button (this skill) |
| --- | --- |
| default + hover only | all 8 states |
| hover changes color only | hover changes color + cursor + transition timing |
| no pressed state | pressed darkens more + scale 0.98 (feels physical) |
| no focus ring (removed "for clean look") | focus-visible ring, 2px, outside the button |
| disabled = gray, no explanation | disabled + tooltip "fill required fields first" |
| loading = full overlay blocking the label | loading = spinner + label change, button shape preserved |
| error = red toast at top of page | error = shake the button + inline message next to it |
| repeat-click = new request each time | loading state blocks re-click (double-submit protection) |

## The repeat-submit protection (P0)

Article line 1283: **"用户点'支付',按钮没变化,用户心里没底,又点几下;系统没有防重复提交,最后可能扣款多次."**

Every submit button MUST:
- enter loading state on click (label → "Saving…", spinner, `aria-busy`)
- set `pointer-events: none` or `disabled` to block re-click
- stay loading until success or error returns
- on success: exit loading, brief success state, then default
- on error: exit loading, enter error state, allow retry

This is not optional. A payment button without this is a financial accident waiting to happen.

## Focus ring — never removed (article line 1285)

The focus ring is the keyboard user's road. Removing it "for a clean look" is removing accessibility.

```css
/* correct */
button:focus-visible {
  outline: 2px solid var(--color-border-focus);
  outline-offset: 2px;
}

/* WRONG — AI's favorite shortcut */
button:focus { outline: none; }  /* never do this */
```

Use `:focus-visible` (not `:focus`) so the ring only shows for keyboard navigation, not mouse clicks — this keeps it clean for mouse users AND accessible for keyboard users.

## Disabled-with-reason

Article line 11778: disabled must explain why.

- Bad: button grayed out, no explanation. User doesn't know if it's a bug, a permission issue, or missing input.
- Good: button grayed out + tooltip on hover: "Fill all required fields to enable Save."
- Good: button grayed out + helper text below: "You need editor role to edit this task."

The reason comes from the object-state-permission matrix (`stage1-object-state-permission.md`) — disabled = some condition in the matrix isn't met.

## Success and error feedback

- **Success**: 200ms green flash on the button → toast ("Saved") → button back to default. Don't leave the button green forever — that's confusing.
- **Error**: 200ms horizontal shake (3px) + focus ring turns red + inline error message next to the button ("Save failed — check your network and retry"). Never a global "操作失败" toast for a button error.

## Implementation skeleton

```tsx
function Button({ loading, error, disabled, onClick, children }) {
  const [pressed, setPressed] = useState(false);
  return (
    <button
      className="btn"
      disabled={disabled || loading}
      aria-busy={loading}
      aria-disabled={disabled}
      onClick={loading ? undefined : onClick}
      onMouseDown={() => setPressed(true)}
      onMouseUp={() => setPressed(false)}
      onMouseLeave={() => setPressed(false)}
      data-pressed={pressed}
      data-error={!!error}
    >
      {loading && <Spinner size={16} />}
      <span>{loading ? 'Saving…' : children}</span>
      {disabled && !loading && (
        <Tooltip>Fill required fields to enable.</Tooltip>
      )}
    </button>
  );
}
```

```css
.btn { /* default */ background: var(--color-state-primary); transition: all 100ms var(--easing-standard); }
.btn:hover { background: var(--color-state-hover); cursor: pointer; }
.btn[data-pressed="true"] { background: var(--color-state-active); transform: scale(0.98); }
.btn:focus-visible { outline: 2px solid var(--color-border-focus); outline-offset: 2px; }
.btn[disabled], .btn[aria-busy="true"] { opacity: 0.4; cursor: not-allowed; pointer-events: none; }
.btn[data-error="true"] { animation: shake 200ms; outline-color: var(--color-danger); }
@keyframes shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-3px)} 75%{transform:translateX(3px)} }
```

## Failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| Only default + hover | plastic button | add all 8 states |
| No focus ring | removed for "clean" | `:focus-visible` mandatory |
| No repeat-submit protection | loading doesn't block re-click | `aria-busy` + `pointer-events: none` |
| Disabled without reason | grayed, no tooltip | add tooltip from permission matrix |
| Error = global toast | "操作失败" at page top | inline error + shake |
| Success stays green forever | button stuck in success | 200ms flash → default |
