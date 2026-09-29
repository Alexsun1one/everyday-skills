# Component: Toast (system feedback)

Transient feedback that doesn't block. Article line 1390: AI either never confirms or spams global toasts for field errors. A toast is for **system-level outcomes the user needs to know but doesn't need to act on right now**.

## When to use toast vs inline vs modal

| Feedback type | Use |
| --- | --- |
| **Toast** | system outcome (saved, exported, synced), background event (new comment), undo prompt |
| **Inline (at element)** | field-level error, button-level error, inline validation |
| **Modal** | blocking alert requiring decision, destructive confirm |
| **Banner (top of page)** | persistent system status (offline mode, read-only mode) |

Never use a toast for a field error — use inline. Article line 11711.

## Spec table (pixel-exact)

| Token | Value |
| --- | --- |
| width | 360px default, 320px small, 480px for undo actions |
| min-height | 56px |
| bg | `color.bg.surface` (#FFFFFF) OR `color.bg.inverse` (#111827 for dark toast) |
| border | 1px `color.border.default` |
| radius | 8px (`rounded-md`) |
| padding | 12px 16px (`px-4 py-3`) |
| shadow | `shadow-lg` |
| position | top-right (default) or bottom-center (mobile), 16px from edge |
| z-index | 70 (above modal=60, above drawer=50) |
| enter animation | 240ms cubic-bezier(0.22, 1, 0.36, 1), slide+fade from right (or up on mobile) |
| exit animation | 200ms ease-in, slide+fade out |
| auto-dismiss | 4000ms success, 6000ms error, persistent for action-required (undo) |
| hover (desktop) | pauses auto-dismiss timer |
| stack | newest on bottom, max 3 visible, older ones queue |

## Toast anatomy

```text
success:                              action (undo):
┌─────────────────────────┐           ┌──────────────────────────────┐
│ ✓  Task saved           │           │ Task deleted    [ Undo ]      │
└─────────────────────────┘           └──────────────────────────────┘
  ↑ icon   ↑ message                    ↑ message       ↑ text button

error:                                loading/info:
┌─────────────────────────┐           ┌─────────────────────────┐
│ ✕  Export failed. Retry │           │ ⟳ Syncing 47 items...   │
└─────────────────────────┘           └─────────────────────────┘
  ↑ icon   ↑ message + action          ↑ spinner + message
```

## Variants

| Variant | Icon | Color accent | Duration |
| --- | --- | --- | --- |
| success | ✓ check | green left-border 4px OR green icon | 4000ms |
| error | ✕ x | red left-border 4px + "Retry" action | 6000ms |
| info | ℹ i | blue accent | 4000ms |
| warning | ⚠ triangle | amber accent | 5000ms |
| loading | spinner | neutral | persistent until resolved |
| action (undo) | none | neutral + text button | persistent (8000ms max) |

## States

| State | Visual | Behavior |
| --- | --- | --- |
| entering | slide+fade from right (240ms ease-out) | — |
| visible | static, accent left border or icon | auto-dismiss timer running; hover pauses |
| hover | dismiss timer paused | cursor default |
| with action | action button right-aligned, clickable; **action button inherits `button.md` focus-visible rule (2px primary ring outside, offset 2px) — keyboard users must reach it** | clicking action dismisses toast + runs action |
| exiting | slide+fade out (200ms ease-in) | — |

## Prompt fragment (English)

```text
Toast spec (transient system feedback, pixel-exact):
- container: 360px wide, min-height 56px, padding 12px horizontal 16px vertical
- background: #FFFFFF (light) OR #111827 (dark/inverse); 1px #E5E7EB border; radius 8px; shadow-lg
- position: top-right (16px from top + right) on desktop; bottom-center (16px from bottom) on mobile
- enter: slide+fade from right, 240ms cubic-bezier(0.22, 1, 0.36, 1)
- exit: slide+fade out, 200ms ease-in
- auto-dismiss: 4000ms (success/info), 6000ms (error), persistent (action-required like undo, max 8000ms)
- HOVER pauses auto-dismiss timer (desktop)
- z-index: 70 (above modal=60, above drawer=50)

anatomy:
- icon left (24px): ✓ for success, ✕ for error, ℹ for info, ⚠ for warning, spinner for loading
- message middle: 14px #111827 (on light) or #F9FAFB (on dark), single-line truncate if long
- action right (optional): text button (ghost), e.g. "Retry", "Undo", "View"
  → the action button INHERITS button.md focus-visible rule (2px primary ring outside, offset 2px) — keyboard users must Tab to it
- accent: 4px left border in variant color (green/red/blue/amber) OR colored icon

variants:
- success: ✓ icon green, 4000ms, "Task saved"
- error: ✕ icon red, 6000ms, "Export failed" + [Retry] action
- info: ℹ icon blue, 4000ms, "Syncing complete"
- warning: ⚠ icon amber, 5000ms, "Storage 90% full"
- loading: spinner neutral, persistent, "Syncing 47 items..."
- undo/action: no icon, neutral, persistent (8000ms), "Task deleted" + [Undo]

NEVER:
- use toast for field-level error (use inline below the field)
- use toast for destructive confirm (use modal)
- auto-dismiss an error toast too fast (user needs to read + maybe retry)
- block the action button (toast is non-blocking — if blocking needed, use modal)
- stack more than 3 visible (queue the rest)
- forget hover-pause (user mid-read, toast vanishes)
```

## Prompt fragment (Chinese)

```text
Toast 规格(瞬时系统反馈,精确到像素):
- 容器:宽 360px,最小高 56px,内边距 上下12px 左右16px
- 背景:#FFFFFF(浅)或 #111827(深/反色);1px #E5E7EB 边框;圆角 8px;shadow-lg
- 位置:桌面端右上角(距上、距右各 16px);移动端底部居中(距底 16px)
- 进入:从右滑入+淡入,240ms cubic-bezier(0.22, 1, 0.36, 1)
- 退出:滑出+淡出,200ms ease-in
- 自动消失:4000ms(成功/信息),6000ms(错误),持续显示(需要操作的如撤销,最多 8000ms)
- HOVER 暂停自动消失计时器(桌面端)
- z-index:70(高于 modal=60,高于 drawer=50)

结构:
- 左侧图标(24px):✓ 成功,✕ 错误,ℹ 信息,⚠ 警告,spinner 加载
- 中间信息:14px #111827(浅底)或 #F9FAFB(深底),长了单行省略
- 右侧操作(可选):文字按钮(ghost),如"重试"、"撤销"、"查看"
  → 操作按钮继承 button.md 的 focus-visible 规则(外侧 2px 主色环,offset 2px)——键盘用户必须能 Tab 到它
- 强调:左侧 4px 变体色边框(绿/红/蓝/琥珀)或彩色图标

变体:
- 成功:✓ 绿色图标,4000ms,"任务已保存"
- 错误:✕ 红色图标,6000ms,"导出失败" + [重试] 按钮
- 信息:ℹ 蓝色图标,4000ms,"同步完成"
- 警告:⚠ 琥珀图标,5000ms,"存储已用 90%"
- 加载:spinner 中性色,持续显示,"正在同步 47 项..."
- 撤销/操作:无图标,中性,持续(8000ms),"任务已删除" + [撤销]

绝对不要:
- 用 toast 报字段级错误(用字段下方的就地错误)
- 用 toast 做破坏性确认(用 modal)
- 错误 toast 消失太快(用户要读 + 可能重试)
- 阻塞操作按钮(toast 是非阻塞的——要阻塞就用 modal)
- 同时显示超过 3 个(其余排队)
- 忘了 hover 暂停(用户读到一半 toast 没了)
```

## Tailwind classes

```tsx
// success toast (top-right)
<div
  role="status"
  aria-live="polite"
  className="fixed right-4 top-4 z-70 flex w-[360px] items-start gap-3 rounded-md border border-[--color-border-default] bg-[--color-bg-surface] px-4 py-3 shadow-lg"
>
  <span className="size-5 shrink-0 text-[--color-success]">✓</span>
  <p className="flex-1 text-sm text-[--color-text-primary]">Task saved</p>
</div>

// error toast with action
<div role="alert" aria-live="assertive" className="... border-l-4 border-l-[--color-danger] ...">
  <span className="size-5 text-[--color-danger]">✕</span>
  <p className="flex-1 text-sm">Export failed</p>
  <button className="text-sm font-medium text-[--color-primary] hover:underline">Retry</button>
</div>
```

## Reverse examples

| Aspect | Plastic | Human |
| --- | --- | --- |
| field errors | global toast "operation failed" | inline at field |
| success duration | 1000ms (vanishes) | 4000ms (read it) |
| hover behavior | keeps ticking | pauses |
| error with retry | no action | "Retry" text button |
| undo | none | action toast with Undo |
| stacking | pile up | max 3, queue rest |
| aria-live | missing | polite for status, assertive for alert |

## Composes with

- `button.md` — text button actions inside toast
- `input.md` — never (field errors go inline, not toast)

## Failure modes

| Failure | Fix |
| --- | --- |
| field error as toast | move inline below field |
| too-short duration | 4000 success, 6000 error |
| no hover pause | pause timer on mouseenter |
| no undo for deletions | add undo action toast |
| stacking overflow | cap at 3, queue rest |
| missing aria-live | add role + aria-live |
