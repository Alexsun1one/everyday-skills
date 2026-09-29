# Component: Button

The loudest "human-made" signal in any UI. Done wrong (plastic), it's a colored rectangle. Done right, it has weight, response, recovery. Every interactive surface in your page inherits from this spec.

## Spec table (pixel-exact)

| Token | Primary | Secondary | Ghost | Icon | Destructive |
| --- | --- | --- | --- | --- | --- |
| height | 36px (`h-9`) | 36px (`h-9`) | 36px (`h-9`) | 36px (`size-9`) | 36px (`h-9`) |
| padding-x | 16px (`px-4`) | 16px (`px-4`) | 12px (`px-3`) | — | 16px (`px-4`) |
| padding-y | 8px (`py-2`) | 8px (`py-2`) | 8px (`py-2`) | — | 8px (`py-2`) |
| radius | 8px (`rounded-md`) | 8px | 8px | 8px | 8px |
| font | 14px / 500 (`text-sm font-medium`) | same | same | — | same |
| gap (icon+label) | 8px (`gap-2`) | 8px | 8px | — | 8px |
| icon size | 16px (`size-4`) | 16px | 16px | 18px (`size-[18px]`) | 16px |
| bg default | `color.state.primary` (#5E6AD2 or #2563EB) | `color.bg.surface` (#FFFFFF) | transparent | transparent | `color.danger` (#DC2626) |
| bg hover | darken 8% (#535CC4) | `color.bg.muted` (#F9FAFB) | `color.bg.muted` | `color.bg.muted` | darken 8% (#B91C1C) |
| bg pressed | darken 16% + scale 0.97 | `color.bg.muted` + scale 0.97 | `color.bg.muted` + scale 0.97 | scale 0.97 | darken 16% + scale 0.97 |
| border | none | 1px `color.border.default` (#E5E7EB) | none | none | none |
| text color | `color.text.inverse` (#FFFFFF) | `color.text.primary` (#111827) | `color.text.primary` | — | #FFFFFF |
| focus ring | 2px outside, `color.border.focus` (#5E6AD2), offset 2px | same | same | same | same |
| disabled | opacity 0.5, cursor not-allowed, tooltip required | same | same | same | same |
| min tap target | 44×44px (iOS) / 48×48px (Material) — pad with hitbox if visual is smaller | | | | |

**One primary per screen.** Article line 1279. If two buttons compete for primary, the IA is wrong.

## 8-state matrix

| State | Visual | Copy | Behavior |
| --- | --- | --- | --- |
| default | primary bg, no shadow | label verb ("Save", "Create task") | cursor pointer |
| hover | bg darken 8%, 100ms ease-out | same | cursor pointer |
| active (pressed) | bg darken 16%, **scale 0.97**, 100ms ease-out | same | spring back on release |
| focus | 2px ring outside, offset 2px — **never removed** | same | keyboard reachable (`:focus-visible`) |
| disabled | opacity 0.5, no shadow, cursor not-allowed | label + tooltip "fill required fields" | aria-disabled, NOT clickable |
| loading | spinner 16px left of label, label → "Saving…", `aria-busy`, pointer-events none | "Saving…" | **BLOCK re-click** (P0: prevents double-submit) |
| success | 200ms green flash → default, then toast | toast "Saved" | confirm done |
| error | 200ms horizontal shake (3px), focus ring → red, inline error message | "Save failed — retry" inline | keep draft, allow retry |

## Prompt fragment (English, copy-paste into image/code prompt)

```text
Button spec (Linear-inspired, pixel-exact):
- container: 36px tall, padding 16px horizontal 8px vertical, radius 8px, NO shadow
- typography: 14px, weight 500 (medium), label color #FFFFFF on primary
- primary variant: bg #5E6AD2 (Linear violet) OR #2563EB (blue) — pick one, use consistently
- hover: darken bg 8%, 100ms ease-out transition
- pressed: darken bg 16% AND scale(0.97) — tactile feedback mandatory
- focus: 2px solid #5E6AD2 ring OUTSIDE the button, offset 2px — use :focus-visible, never :focus
- disabled: opacity 0.5, cursor not-allowed, tooltip explaining why ("fill required fields")
- loading: 16px spinner LEFT of label, label swaps to "Saving…", aria-busy=true, BLOCK re-click
- success: 200ms green flash on container → revert to default, toast "Saved" appears top-right
- error: 200ms horizontal shake (translateX -3px/3px/0), focus ring turns red, inline error below button
- one primary per screen — demote others to secondary/ghost
- icon+label: 16px icon, 8px gap, icon inherits label color
- min tap target 44×44px (pad invisible hitbox if visual button is smaller)

NEVER:
- remove focus ring "for clean look" (it's the keyboard user's road)
- use bare spinner that hides the label
- allow repeat-clicks during loading (double-submit is a P0 financial bug)
- use pill radius (9999px) on primary — reserved for badges only
- put two primary buttons on one screen
```

## Prompt fragment (Chinese, copy-paste)

```text
按钮规格(Linear 风格,精确到像素):
- 容器:高 36px,内边距 左右16px 上下8px,圆角 8px,无阴影
- 字体:14px,字重 500(medium),主按钮文字 #FFFFFF
- primary 变体:背景 #5E6AD2(Linear 紫)或 #2563EB(蓝)——二选一,全程统一
- hover:背景加深 8%,100ms ease-out 过渡
- pressed(按下):背景加深 16% 且 scale(0.97)——必须有按下手感
- focus:2px 实线 #5E6AD2 环 在按钮外侧,offset 2px——用 :focus-visible,绝不用 :focus
- disabled:透明度 0.5,光标 not-allowed,必须有 tooltip 解释原因("请先填写必填字段")
- loading:16px spinner 在文字左边,文字变成"保存中…",aria-busy=true,屏蔽重复点击
- success:容器闪绿 200ms → 恢复默认,右上角弹 toast"已保存"
- error:200ms 横向抖动(translateX -3px/3px/0),focus 环变红,按钮下方就地报错
- 一屏只有一个主按钮——其他降级为 secondary/ghost
- 图标+文字:16px 图标,8px 间距,图标继承文字颜色
- 最小触控区 44×44px(按钮视觉小就加不可见的 hitbox)

绝对不要:
- 为了"干净"删掉 focus ring(那是键盘用户的路)
- 用裸 spinner 盖住文字
- loading 时还允许重复点击(重复提交是 P0 财务事故)
- 主按钮用胶囊圆角 9999px(那是徽章专用)
- 一屏放两个主按钮
```

## Tailwind classes

```tsx
// primary
<button className="inline-flex h-9 items-center justify-center gap-2 rounded-md bg-[--color-state-primary] px-4 py-2 text-sm font-medium text-white transition-all duration-100 ease-out hover:bg-[--color-state-hover] active:scale-[0.97] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[--color-border-focus] focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 aria-busy:pointer-events-none" aria-busy={loading}>

// secondary (outline)
<button className="... border border-[--color-border-default] bg-[--color-bg-surface] text-[--color-text-primary] hover:bg-[--color-bg-muted] ...">

// ghost
<button className="... bg-transparent text-[--color-text-primary] hover:bg-[--color-bg-muted] ...">

// icon-only
<button className="inline-flex size-9 items-center justify-center rounded-md ... aria-label='Action name'">
```

## Reverse examples

| Aspect | Plastic (AI default) | Human (this spec) |
| --- | --- | --- |
| states | default + hover only | all 8 |
| hover | bg changes color only | bg darken 8% + cursor + 100ms transition |
| pressed | missing | darken 16% + scale 0.97 (feels physical) |
| focus ring | removed "for clean look" | `:focus-visible` 2px outside, offset 2px |
| disabled | gray, no explanation | opacity 0.5 + tooltip "fill required fields" |
| loading | full overlay hiding label | spinner + label swap, shape preserved |
| error | global toast "操作失败" | shake + inline message next to button |
| repeat-click | new request each click | loading blocks re-click (P0 protection) |
| radius | pill 9999px | 8px (md) — pill is for badges only |

## Composes with

- `table-row.md` — action buttons appear on row hover (secondary/ghost, never primary in a list)
- `drawer.md` — save button in drawer footer
- `modal.md` — confirm button (destructive variant) + cancel (ghost)
- `empty-state.md` — primary CTA in initial-empty
- `input.md` — submit button below form

## Failure modes

| Failure | Fix |
| --- | --- |
| two primary buttons on one screen | demote one to secondary; fix IA |
| pill radius on primary | change to 8px (md) |
| missing pressed state | add active:scale-[0.97] + darken |
| no focus-visible | add focus-visible:ring-2 ring-offset-2 |
| loading allows re-click | add aria-busy + pointer-events-none |
