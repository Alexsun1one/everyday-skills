# Component: Drawer (right-side panel)

Article line 1383: AI's container disease is putting everything in modals. A drawer is for **detail that preserves list context** — the list stays visible on the left, the detail slides in from the right.

## When to use drawer vs modal vs page

| Container | Use when | Don't use when |
| --- | --- | --- |
| **Drawer** (right slide-in) | editing/viewing detail without losing list context; 30-50% width | need full attention, or detail is very long |
| **Modal** (center, blocks) | destructive confirm, short focused task (login), blocking alert | forms, lists, anything scrollable |
| **Page** (full navigation) | primary task flow, anything with its own URL | quick edits, secondary info |
| **Popover** (anchored) | tiny contextual info, inline picker | anything >300px wide |
| **Split-pane** | master-detail always visible together | occasional detail lookups |

Article line 1341: AI defaults to modal for everything. Resist.

## Spec table (pixel-exact)

| Token | Value |
| --- | --- |
| width | 480px default (`w-[480px]`), 640px large, 320px small |
| height | 100vh (full height) |
| bg | `color.bg.surface` (#FFFFFF) |
| border-left | 1px `color.border.default` (#E5E7EB) |
| shadow | `shadow-2xl` (only because it overlays) |
| header padding | 16px 24px (`px-6 py-4`) |
| content padding | 24px (`p-6`) |
| footer padding | 16px 24px, border-top 1px |
| enter animation | 240ms cubic-bezier(0.22, 1, 0.36, 1), translateX(100%) → 0 |
| exit animation | 200ms ease-in, 0 → translateX(100%) |
| overlay | `bg-black/40`, fade in 200ms |
| z-index | 50 (below modal at 60, below toast at 70) |
| close affordances | ESC key + overlay click + X icon button top-right |
| body scroll | locked when drawer open (`overflow: hidden` on body) |
| focus trap | focus moves into drawer, Tab cycles inside, returns to trigger on close |

## Drawer anatomy

```text
┌─overlay bg-black/40 fade 200ms────────────────────────────┐
│                                              ┌─drawer─────┐│
│   [list stays visible]                       │ header     ││
│   ┌─row─────────┐                            │  ────────  ││
│   │ task A   ✓  │  ← user clicked this row   │ content    ││
│   ├─row─────────┤                            │  (scroll)  ││
│   │ task B      │                            │            ││
│   └─────────────┘                            │  ────────  ││
│                                              │ footer     ││
│                                              │ [Cancel]   ││
│                                              │  [Save]    ││
│                                              └────────────┘│
└────────────────────────────────────────────────────────────┘
```

## States

| State | Visual | Behavior |
| --- | --- | --- |
| entering | slides in from right, 240ms ease-out | overlay fades in parallel |
| open | static, content scrollable | focus trapped, ESC closes, overlay click closes |
| dirty (unsaved changes) | footer Save button enabled; ESC/click shows confirm modal | "discard changes?" |
| exiting | slides out to right, 200ms ease-in | overlay fades parallel, focus returns to trigger |
| loading (save in progress) | footer Save shows loading state, drawer not closable | block close until done |

## Prompt fragment (English)

```text
Drawer spec (right-side detail panel, pixel-exact):
- container: 480px wide (640px for long forms, 320px for tiny detail), full viewport height
- background: #FFFFFF, 1px #E5E7EB left border, shadow-2xl (overlays only)
- enter: slide from right, 240ms cubic-bezier(0.22, 1, 0.36, 1)
- exit: slide to right, 200ms ease-in
- overlay: bg-black at 40% opacity, fade in 200ms; CLICK on overlay closes drawer
- ESC key closes drawer; X icon button top-right closes drawer
- when open: body scroll LOCKED (overflow hidden), focus TRAPPED inside drawer (Tab cycles), focus returns to trigger button on close
- header: padding 16/24, title 16px weight 600, description 14px secondary, X icon button right, 1px border-bottom
- content: padding 24px, scrollable if exceeds height
- footer: padding 16/24, 1px border-top, actions right-aligned (Cancel secondary + Save primary), 8px gap
- dirty state: if user edited anything, ESC/overlay-click triggers "discard changes?" confirm modal (NOT silent close)
- z-index: 50 (below modal=60, below toast=70)

NEVER:
- close drawer silently when there are unsaved changes (data loss)
- allow body to scroll behind the drawer
- skip focus trap (keyboard users get lost)
- use drawer for destructive confirm (use modal — drawer is non-blocking context)
- put a primary button in the header (footer is for actions)
```

## Prompt fragment (Chinese)

```text
抽屉规格(右侧详情面板,精确到像素):
- 容器:宽 480px(长表单 640px,小详情 320px),高 100vh
- 背景:#FFFFFF,左侧 1px #E5E7EB 边框,shadow-2xl(仅因为浮层)
- 进入:从右滑入,240ms cubic-bezier(0.22, 1, 0.36, 1)
- 退出:向右滑出,200ms ease-in
- 遮罩:bg-black 40% 透明度,200ms 淡入;点击遮罩关闭抽屉
- ESC 键关闭抽屉;右上角 X 图标按钮关闭抽屉
- 打开时:body 滚动锁定(overflow hidden),焦点陷阱在抽屉内(Tab 循环),关闭后焦点回到触发按钮
- 头部:内边距 16/24,标题 16px 字重 600,描述 14px secondary,右侧 X 图标按钮,1px 下边框
- 内容:内边距 24px,超出高度则滚动
- 底部:内边距 16/24,1px 上边框,操作右对齐(Cancel secondary + Save primary),间距 8px
- dirty 态:用户改了任何东西,ESC/点击遮罩 触发"放弃修改?"确认弹窗(不要静默关闭)
- z-index:50(低于 modal=60,低于 toast=70)

绝对不要:
- 有未保存修改时静默关闭抽屉(丢数据)
- 抽屉打开时还允许 body 滚动
- 跳过焦点陷阱(键盘用户会迷路)
- 用抽屉做破坏性确认(用 modal——抽屉是非阻塞的上下文)
- 头部放主按钮(操作放底部)
```

## Tailwind classes

```tsx
<Dialog>
  <DialogTrigger asChild><Button>Open</Button></DialogTrigger>
  <DialogContent className="fixed inset-y-0 right-0 top-0 z-50 flex h-full w-[480px] max-w-full flex-col border-l border-[--color-border-default] bg-[--color-bg-surface] p-0 shadow-2xl data-[state=open]:animate-in data-[state=open]:slide-in-from-right data-[state=closed]:animate-out data-[state=closed]:slide-out-to-right duration-200">
    {/* header */}
    <div className="flex items-start justify-between border-b border-[--color-border-default] px-6 py-4">
      <div>
        <DialogTitle className="text-base font-semibold">Edit task</DialogTitle>
        <DialogDescription className="mt-1 text-sm text-[--color-text-secondary]">Changes save when you click Save.</DialogDescription>
      </div>
      <DialogClose asChild><IconButton aria-label="Close" variant="ghost">×</IconButton></DialogClose>
    </div>
    {/* content scrollable */}
    <div className="flex-1 overflow-y-auto p-6">{/* form */}</div>
    {/* footer */}
    <div className="flex justify-end gap-2 border-t border-[--color-border-default] px-6 py-4">
      <DialogClose asChild><Button variant="secondary">Cancel</Button></DialogClose>
      <Button aria-busy={saving} onClick={save}>Save</Button>
    </div>
  </DialogContent>
</Dialog>
```

## Reverse examples

| Aspect | Plastic | Human |
| --- | --- | --- |
| unsaved changes | silent close, data lost | "discard?" confirm modal |
| body scroll | scrolls behind | locked |
| focus | lost to background | trapped, returns to trigger |
| ESC | not handled | closes (with dirty check) |
| width | full screen on desktop | 480px preserves list context |
| animation | none or 500ms+ | 240ms in / 200ms out (Linear timing) |

## Composes with

- `button.md` — footer primary/secondary, header X icon
- `input.md` — form fields inside
- `modal.md` — discard-changes confirm nested inside drawer
- `table-row.md` — drawer opens on row click, list scroll preserved

## Failure modes

| Failure | Fix |
| --- | --- |
| silent close on dirty | add discard-confirm modal |
| body scroll leaks | overflow:hidden on body when open |
| focus lost | focus trap + return-to-trigger |
| ESC not handled | add ESC handler with dirty check |
| full-screen on desktop | cap at 480-640px |
