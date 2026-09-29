# Component: Checkbox / Radio / Switch (selection controls)

Three controls that look similar but mean different things. Article line 1463: AI conflates them — using a switch where a checkbox belongs, or radio where a checkbox belongs.

## When to use which

| Control | Use for |
| --- | --- |
| **Checkbox** | multi-select (zero or more options); independent toggle of a single boolean that has a clear on/off |
| **Radio** | mutually exclusive choice (exactly one of N); persistent setting |
| **Switch** | real-time toggle of a setting with immediate effect (no Save needed); system-level preference (dark mode, notifications) |

**Switch ≠ Checkbox.** Switch applies instantly (toggling dark mode changes the screen now). Checkbox requires a submit (checking "agree to terms" doesn't apply until you submit the form).

## Checkbox spec

| Token | Value |
| --- | --- |
| box size | 16px (`size-4`) default, 20px (`size-5`) large/touch |
| radius | 4px (`rounded`) — NOT pill (switches are pill, checkboxes are square-ish) |
| border default | 1.5px `color.border.strong` (#9CA3AF) |
| border hover | 1.5px `color.text.primary` (#111827) |
| border checked | none (filled) |
| bg checked | `color.state.primary` (#5E6AD2 or #2563EB) |
| checkmark | 12px white, centered, draw-in animation 150ms |
| indeterminate | horizontal white bar (12px × 2px) |
| label gap | 8px right of box |
| label | 14px / `color.text.primary` |
| focus ring | 2px outside, offset 2px, primary color |
| disabled | opacity 0.5, cursor not-allowed |
| error | border danger + error message below group |
| min tap target | 44×44px (pad invisible hitbox) |

### Checkbox states

| State | Visual |
| --- | --- |
| unchecked | 1.5px gray-400 border, white bg |
| hover | border darkens to gray-700 |
| checked | primary fill, white checkmark (draw-in 150ms) |
| indeterminate | primary fill, white horizontal bar |
| focus | 2px primary ring outside, offset 2px |
| disabled | opacity 0.5 |
| error | border red + group error message below |

## Radio spec

Same dimensions as checkbox but **circle**:

| Token | Value |
| --- | --- |
| circle size | 16px (`size-4`) |
| radius | 9999px (`rounded-full`) |
| border default | 1.5px `color.border.strong` |
| border hover | 1.5px `color.text.primary` |
| selected | 1.5px primary border + 6px primary dot inside (scale-in 150ms) |
| label gap | 8px |
| focus ring | 2px outside, offset 2px, primary |

### Radio states

| State | Visual |
| --- | --- |
| unselected | 1.5px gray-400 ring, white bg |
| hover | border darkens |
| selected | 1.5px primary ring + 6px primary dot (scale-in) |
| focus | 2px primary ring outside the radio |
| disabled | opacity 0.5 |

## Switch spec

| Token | Value |
| --- | --- |
| track width | 36px (`w-9`) |
| track height | 20px (`h-5`) |
| radius | 9999px (pill) |
| track off | `color.bg.muted` (#E5E7EB) |
| track on | `color.state.primary` |
| thumb | 16px circle (`size-4`), white, shadow-sm |
| thumb position off | 2px from left |
| thumb position on | 2px from right |
| transition | 200ms cubic-bezier(0.22, 1, 0.36, 1) for thumb slide + track color |
| label gap | 8px left of track |
| label | 14px / `color.text.primary` |
| focus ring | 2px outside the track, offset 2px, primary |
| disabled | opacity 0.5, no transition |
| loading | track gray, thumb centered, spinner inside thumb |

### Switch states

| State | Visual |
| --- | --- |
| off | gray track, thumb left |
| hover | track darken slightly |
| on | primary track, thumb right (slid 200ms ease-out) |
| focus | 2px primary ring outside the track |
| disabled | opacity 0.5 |
| loading | track gray, thumb spinner centered (during async apply) |

## Prompt fragment (English)

```text
Selection controls spec (3 distinct controls, pixel-exact):

CHECKBOX (multi-select or independent boolean with submit):
- box: 16px (20px large/touch), radius 4px (square-ish, NOT pill)
- border default: 1.5px #9CA3AF (gray-400)
- border hover: 1.5px #111827 (gray-900)
- checked: bg #5E6AD2 (primary), white checkmark 12px centered, draw-in 150ms
- indeterminate: bg #5E6AD2, white horizontal bar (12px × 2px)
- label: 14px #111827, 8px gap right of box
- focus: 2px #5E6AD2 ring OUTSIDE box, offset 2px
- disabled: opacity 0.5, cursor not-allowed
- min tap target: 44×44px (invisible hitbox padding)
- error: red border on box + error message BELOW THE GROUP (not per checkbox)

RADIO (mutually exclusive, exactly one of N):
- circle: 16px, radius 9999px (circle)
- border default: 1.5px #9CA3AF
- border hover: 1.5px #111827
- selected: 1.5px #5E6AD2 border + 6px #5E6AD2 dot inside (scale-in 150ms)
- label/focus/disabled: same as checkbox

SWITCH (real-time toggle, applies INSTANTLY — no Save):
- track: 36px wide × 20px tall, radius 9999px (pill)
- track off: #E5E7EB bg
- track on: #5E6AD2 bg
- thumb: 16px white circle, shadow-sm, slides 200ms cubic-bezier(0.22, 1, 0.36, 1)
- thumb off position: 2px from left
- thumb on position: 2px from right
- focus: 2px #5E6AD2 ring OUTSIDE track, offset 2px
- loading (async apply): track gray, thumb centered with spinner
- label: 14px #111827, 8px gap LEFT of track (label first, then switch)

WHEN TO USE WHICH:
- checkbox: multi-select (pick N of M) OR single boolean that requires submit
- radio: pick exactly 1 of N (mutually exclusive)
- switch: real-time toggle that applies instantly (dark mode, notifications)

NEVER:
- use a switch for a setting that requires Save (use checkbox)
- use a checkbox for a real-time toggle (use switch)
- use square corners on a switch (pill only)
- use pill corners on a checkbox (4px square-ish)
- put error message per-checkbox (it's a group error, below the group)
- skip focus ring on any of the three
- forget min tap target (44×44 with invisible padding)
```

## Prompt fragment (Chinese)

```text
选择控件规格(3 种独立控件,精确到像素):

CHECKBOX(多选 或 需提交的独立布尔):
- 方框:16px(大/触控 20px),圆角 4px(微方,不是胶囊)
- 默认边框:1.5px #9CA3AF(gray-400)
- hover 边框:1.5px #111827(gray-900)
- 选中:背景 #5E6AD2(主色),白色对勾 12px 居中,150ms 画入动画
- 半选:背景 #5E6AD2,白色横条(12px × 2px)
- 标签:14px #111827,距方框右侧 8px
- focus:2px #5E6AD2 环在方框外侧,offset 2px
- disabled:透明度 0.5,光标 not-allowed
- 最小触控区:44×44px(不可见的 hitbox 内边距)
- error:方框红边 + 错误信息在 整组下方(不是每个 checkbox 下面)

RADIO(互斥,从 N 选 1):
- 圆:16px,圆角 9999px(圆)
- 默认边框:1.5px #9CA3AF
- hover 边框:1.5px #111827
- 选中:1.5px #5E6AD2 边框 + 内部 6px #5E6AD2 圆点(150ms 放大入场)
- 标签/focus/disabled:同 checkbox

SWITCH(实时切换,立即生效——无需保存):
- 轨道:宽 36px × 高 20px,圆角 9999px(胶囊)
- 关闭态:#E5E7EB 背景
- 开启态:#5E6AD2 背景
- 滑块:16px 白色圆,shadow-sm,200ms cubic-bezier(0.22, 1, 0.36, 1) 滑动
- 关闭位置:距左 2px
- 开启位置:距右 2px
- focus:2px #5E6AD2 环在轨道外侧,offset 2px
- 加载中(异步应用):轨道灰,滑块居中带 spinner
- 标签:14px #111827,距轨道左侧 8px(标签在前,开关在后)

什么时候用哪个:
- checkbox:多选(从 M 选 N)或 需要提交的单布尔
- radio:互斥(从 N 选 1)
- switch:实时切换立即生效(深色模式、通知)

绝对不要:
- 需要保存的设置用 switch(用 checkbox)
- 实时切换用 checkbox(用 switch)
- switch 用方角(只能胶囊)
- checkbox 用胶囊角(只能 4px 微方)
- 每个 checkbox 一个错误信息(是组错误,放整组下面)
- 任何一个跳过 focus ring
- 忘了最小触控区(44×44 加不可见内边距)
```

## Tailwind classes

```tsx
// checkbox
<label className="inline-flex items-center gap-2">
  <input type="checkbox" className="size-4 rounded border-[1.5px] border-[--color-border-strong] text-[--color-state-primary] transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-[--color-border-focus] focus-visible:ring-offset-2 disabled:opacity-50" />
  <span className="text-sm text-[--color-text-primary]">Subscribe to updates</span>
</label>

// radio
<label className="inline-flex items-center gap-2">
  <input type="radio" className="size-4 rounded-full border-[1.5px] border-[--color-border-strong] text-[--color-state-primary] transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-[--color-border-focus] focus-visible:ring-offset-2" />
  <span className="text-sm">Option A</span>
</label>

// switch
<button role="switch" aria-checked={on} onClick={toggle} className="relative inline-flex h-5 w-9 items-center rounded-full transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-[--color-border-focus] focus-visible:ring-offset-2 aria-[checked=true]:bg-[--color-state-primary] aria-[checked=false]:bg-[--color-bg-muted]">
  <span className={cn("inline-block size-4 transform rounded-full bg-white shadow-sm transition-transform duration-200 ease-out", on ? "translate-x-[18px]" : "translate-x-0.5")} />
</button>
```

## Reverse examples

| Aspect | Plastic | Human |
| --- | --- | --- |
| control choice | switch for everything | matched to semantics (checkbox/radio/switch) |
| checkbox corners | pill | 4px square-ish |
| switch corners | square | pill |
| focus ring | missing | 2px outside, offset 2px |
| tap target | 16px (too small) | 44×44 with padding |
| group error | per-control | below the group |
| loading on switch | none | thumb spinner during async |

## Composes with

- `table-row.md` — row selection checkbox (16px)
- `input.md` — form fields with checkbox/radio groups
- `nav-sidebar.md` — settings panel switches (instant apply)

## Failure modes

| Failure | Fix |
| --- | --- |
| switch for save-required | switch to checkbox |
| checkbox corners pill | change to 4px |
| switch corners square | change to pill |
| missing focus ring | add focus-visible ring |
| tap target <44px | add invisible padding |
| per-control error | move below group |
