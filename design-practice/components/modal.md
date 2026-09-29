# Component: Modal (centered, blocking)

Reserved for **destructive confirms, short focused tasks, blocking alerts**. Article line 1341: AI's container disease puts everything in modals — resist. Most "modal needs" are better served by a drawer or page.

## When modal is the right call

| Use modal for | Use drawer/page instead for |
| --- | --- |
| "Delete this? This cannot be undone." | editing a form (use drawer or page) |
| login / 2FA prompt | viewing detail (use drawer) |
| blocking alert ("session expired") | showing a list (use page) |
| short single-action confirm | multi-step wizards (use page) |
| payment confirmation | anything with scrollable content |

## Spec table (pixel-exact)

| Token | Value |
| --- | --- |
| width | 448px default (`max-w-md`), 576px large (`max-w-lg`), 320px small (`max-w-sm`) |
| max-height | 85vh; content scrolls if exceeded |
| bg | `color.bg.surface` (#FFFFFF) |
| border | none (overlay separates it) or 1px subtle |
| radius | 12px (`rounded-lg`) — matches card |
| shadow | `shadow-2xl` |
| header padding | 16px 24px (`px-6 py-4`) |
| content padding | 24px (`p-6`) |
| footer padding | 16px 24px, border-top 1px |
| enter animation | 200ms cubic-bezier(0.22, 1, 0.36, 1), opacity 0→1 + scale 0.96→1 |
| exit animation | 150ms ease-in, reverse |
| overlay | `bg-black/50`, fade in 200ms |
| z-index | 60 (above drawer=50, below toast=70) |
| close affordances | ESC + overlay click + X (BUT NOT for destructive — see below) |
| focus trap | mandatory |
| body scroll | locked |

## Destructive modal special rules

For destructive confirms (delete, discard, irreversible), the rules tighten:

| Rule | Why |
| --- | --- |
| **No overlay-click close** | prevent muscle-memory dismissal of destructive action |
| **No ESC close** | same |
| **X close allowed** | explicit cancel path remains |
| **Cancel is secondary (default focus)** | default action must be the safe one |
| **Confirm is destructive variant (red)** | visual warning matches stakes |
| **Confirm button requires the verb** | "Delete project" not "OK" — user reads what they're doing |
| **Type-to-confirm for high-stakes** | "type the project name to confirm" for org-level deletes |

## Modal anatomy (destructive confirm)

```text
┌─overlay bg-black/50 fade 200ms──────────────────────────┐
│                                                          │
│              ┌─modal 448px, radius 12px────────┐         │
│              │ ─── header 16/24 ─────          │         │
│              │ [⚠ icon 24px]  Delete project   │         │
│              │                                  │         │
│              │ ─── content 24px ─────          │         │
│              │ This will permanently delete    │         │
│              │ "Acme Inc" and remove 47        │         │
│              │ members. This cannot be undone. │         │
│              │                                  │         │
│              │ ─── footer 16/24 ─────          │         │
│              │      [Cancel]  [Delete project] │         │
│              │       default    destructive    │         │
│              └──────────────────────────────────┘        │
└──────────────────────────────────────────────────────────┘
```

## States

| State | Visual | Behavior |
| --- | --- | --- |
| entering | fade+scale-in 200ms | overlay fades parallel |
| open | static | focus trapped, focus starts on Cancel (safe default) |
| confirming (in progress) | Confirm button shows loading, X disabled, Cancel disabled | block dismissal until done |
| exiting | fade+scale-out 150ms | focus returns to trigger |

## Prompt fragment (English)

```text
Modal spec (centered blocking dialog, pixel-exact):
- container: 448px wide (576 large, 320 small), max-height 85vh (content scrolls if exceeded)
- background: #FFFFFF, radius 12px, shadow-2xl, no border (overlay separates it)
- enter: fade+scale, opacity 0→1 + scale(0.96)→1, 200ms cubic-bezier(0.22, 1, 0.36, 1)
- exit: reverse, 150ms ease-in
- overlay: bg-black at 50% opacity, fade 200ms
- header: padding 16/24, title 16px weight 600, optional 24px warning icon left of title, 1px border-bottom
- content: padding 24px, body text 14px #374151
- footer: padding 16/24, 1px border-top, actions right-aligned, Cancel (secondary) LEFT, Confirm (primary/destructive) RIGHT
- z-index: 60 (above drawer=50, below toast=70)
- focus: TRAPPED inside modal, focus moves to FIRST INTERACTIVE (or Cancel for destructive), returns to trigger on close
- body scroll LOCKED when modal open

DESTRUCTIVE MODAL (delete/discard/irreversible) — stricter rules:
- NO overlay-click close (prevent muscle-memory dismissal)
- NO ESC close (same reason)
- X close allowed (explicit cancel path)
- DEFAULT FOCUS on Cancel (the safe option)
- Confirm button is DESTRUCTIVE variant (red bg, white text)
- Confirm button label is the VERB: "Delete project" not "OK" — forces user to read what they're doing
- for org-level deletes: TYPE-TO-CONFIRM ("type the project name to confirm")

NEVER:
- use modal for forms, lists, or scrollable content (use drawer or page)
- allow overlay-click close on destructive modal
- default focus to Confirm on destructive (must be Cancel)
- use "OK" / "Confirm" as the destructive button label (use the verb)
- skip focus trap
- stack modals on modals (redesign the flow)
```

## Prompt fragment (Chinese)

```text
模态框规格(居中阻塞对话框,精确到像素):
- 容器:宽 448px(大 576,小 320),最大高 85vh(超出则内容滚动)
- 背景:#FFFFFF,圆角 12px,shadow-2xl,无边框(靠遮罩分隔)
- 进入:淡入+缩放,opacity 0→1 + scale(0.96)→1,200ms cubic-bezier(0.22, 1, 0.36, 1)
- 退出:反向,150ms ease-in
- 遮罩:bg-black 50% 透明度,200ms 淡入
- 头部:内边距 16/24,标题 16px 字重 600,可选 24px 警告图标在标题左侧,1px 下边框
- 内容:内边距 24px,正文 14px #374151
- 底部:内边距 16/24,1px 上边框,操作右对齐,Cancel(secondary)左,Confirm(primary/destructive)右
- z-index:60(高于 drawer=50,低于 toast=70)
- 焦点:陷阱在模态内,焦点移到第一个可交互元素(破坏性操作移到 Cancel),关闭后回到触发器
- 模态打开时 body 滚动锁定

破坏性模态(删除/放弃/不可逆)——更严的规则:
- 不允许点击遮罩关闭(防止肌肉记忆误删)
- 不允许 ESC 关闭(同上)
- 允许 X 关闭(显式取消路径)
- 默认焦点在 Cancel(安全选项)
- 确认按钮用 destructive 变体(红底白字)
- 确认按钮文字是动词:"删除项目" 不是 "确定"——逼用户读清楚要做什么
- 组织级删除:输入确认("输入项目名以确认")

绝对不要:
- 用模态做表单、列表、可滚动内容(用 drawer 或 page)
- 破坏性模态允许点遮罩关闭
- 破坏性模态默认焦点在 Confirm(必须在 Cancel)
- 用 "确定"/"确认" 当破坏性按钮文字(用动词)
- 跳过焦点陷阱
- 模态叠模态(重新设计流程)
```

## Tailwind classes

```tsx
<AlertDialog>
  <AlertDialogTrigger asChild><Button variant="destructive">Delete</Button></AlertDialogTrigger>
  <AlertDialogContent className="max-w-md rounded-lg border-0 bg-[--color-bg-surface] p-0 shadow-2xl">
    <AlertDialogHeader className="border-b border-[--color-border-default] px-6 py-4">
      <div className="flex items-start gap-3">
        <span className="size-6 text-[--color-danger]">⚠</span>
        <div>
          <AlertDialogTitle className="text-base font-semibold">Delete project</AlertDialogTitle>
          <AlertDialogDescription className="mt-1 text-sm text-[--color-text-secondary]">
            This will permanently delete "Acme Inc" and remove 47 members. This cannot be undone.
          </AlertDialogDescription>
        </div>
      </div>
    </AlertDialogHeader>
    <AlertDialogFooter className="flex justify-end gap-2 border-t border-[--color-border-default] px-6 py-4">
      <AlertDialogCancel autoFocus>Cancel</AlertDialogCancel>
      <AlertDialogAction className="bg-[--color-danger] text-white hover:bg-[--color-danger]/90">Delete project</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

## Reverse examples

| Aspect | Plastic | Human |
| --- | --- | --- |
| use frequency | everything is a modal | reserved for destructive + short focused |
| destructive default focus | Confirm (dangerous) | Cancel (safe) |
| destructive label | "OK" | "Delete project" (verb) |
| overlay click on destructive | closes silently | blocked |
| focus | lost | trapped + returns |
| body scroll | scrolls behind | locked |
| stacking | modal on modal | redesigned flow |

## Composes with

- `button.md` — footer Cancel + Confirm (destructive variant)
- `input.md` — type-to-confirm input for high-stakes deletes
- `drawer.md` — discard-changes modal nested inside dirty drawer

## Failure modes

| Failure | Fix |
| --- | --- |
| modal for forms | move to drawer or page |
| destructive allows overlay close | block overlay click on destructive |
| "OK" as destructive label | use the verb ("Delete project") |
| default focus on Confirm | move autoFocus to Cancel |
| no focus trap | add trap + return-to-trigger |
| modal stacking | redesign the flow |
