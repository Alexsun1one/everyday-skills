# Component: Table / List Row (3 densities)

Data density is a product skill. Article line 1483: AI's default is "全摊开" — everything on one page. A well-tuned row at the right density is the difference between "scan 50 items" and "scroll forever".

## The 3 densities (Linear / Material / shadcn consensus)

| Density | Row height | Cell padding-y | Font | Use when |
| --- | --- | --- | --- | --- |
| **compact** | 32px (`h-8`) | 4px (`py-1`) | 13px (`text-[13px]`) or 14px | admin tables, audit logs, power-user data dumps |
| **comfortable** (default) | 40px (`h-10`) | 8px (`py-2`) | 14px (`text-sm`) | most product tables, task lists, contacts |
| **spacious** | 48px (`h-12`) | 12px (`py-3`) | 14px (`text-sm`) | customer-facing, mobile, scannable content |

Linear uses 32px or 40px exclusively — they never go higher because their users are power users. A consumer product should default to comfortable or spacious.

## Row anatomy (left to right)

```text
┌─row────────────────────────────────────────────────────────────────┐
│ [select] [primary-text] [secondary-text] [badge] ... [actions-hover]│
│   ☐       Task title      due·assignee   status      ⋯ hover-only  │
└────────────────────────────────────────────────────────────────────┘
  16px     flex-1           shrink-0       shrink-0     shrink-0
  gap      gap-2            gap-1          gap-1        gap-1
```

## Spec table (comfortable density, 40px)

| Token | Value |
| --- | --- |
| row height | 40px (`h-10`) |
| cell padding-x | 16px (`px-4`) first/last cell, 12px (`px-3`) middle |
| cell padding-y | 8px (`py-2`) |
| border between rows | 1px `color.border.default` (#F3F4F6 — very light) |
| hover bg | `color.bg.muted` (#F9FAFB) |
| selected bg | `color.state.primary` at 8% opacity (#EEF2FF) |
| font primary | 14px / 500, `color.text.primary` |
| font secondary | 13px / 400, `color.text.secondary` |
| checkbox | 16px (`size-4`), left-aligned, see `checkbox.md` |
| avatar | 24px circle (`size-6`), see `avatar.md` |
| badge | 20px tall (`h-5`), 12px padding-x, see `badge.md` |
| actions | appear on ROW HOVER, ghost icon buttons, see `button.md` |
| truncate | single-line ellipsis on primary text with tooltip on hover |
| focus | row gets 2px inset ring on `:focus-visible` (keyboard nav) |

## States

| State | Visual | Behavior |
| --- | --- | --- |
| default | white bg, 1px bottom border | click row opens detail (drawer or page) |
| hover | bg `color.bg.muted`, actions appear (ghost icon buttons fade in) | cursor pointer |
| selected | bg `color.state.primary` at 8% opacity, left 2px primary border | persists until deselected |
| focus | 2px inset ring `color.border.focus` | keyboard reachable (Tab + Enter to open) |
| loading | row shows skeleton (rectangle matching cell shapes, gray-200 pulse) | see `skeleton.md` |
| empty | empty state component replaces the table body | see `empty-state.md` |
| error | error state replaces the table body (header preserved), retry button | preserves filters |
| drag (reorder) | row scale 1.01, shadow lg, opacity 0.9, placeholder shows drop zone | snap back if invalid drop |

## Prompt fragment (English)

```text
Table/list row spec (Linear-inspired, 3 densities):
- default density: COMFORTABLE — 40px row height, 8px vertical padding, 14px font
- compact density: 32px row height, 4px vertical padding, 13-14px font (for power-user data)
- spacious density: 48px row height, 12px vertical padding, 14px font (for consumer/mobile)
- row border: 1px SOLID #F3F4F6 between rows (very light, almost invisible — NOT heavy lines)
- row hover: background #F9FAFB (gray-50), 100ms ease-out
- row selected: background #EEF2FF (primary at 8% opacity) PLUS 2px left border in #5E6AD2
- row focus: 2px INSET ring #5E6AD2 (for keyboard navigation)

row anatomy (left to right):
- selection checkbox: 16px, padding-left 16px, vertically centered
- primary text: 14px weight 500 #111827, single-line truncate with ellipsis, tooltip on hover with full text
- secondary text (metadata): 13px weight 400 #6B7280, gap 8px from primary
- status badge: 20px tall, padding 0 8px, see badge spec
- avatar (if assignee): 24px circle, gap 8px
- actions: GHOST ICON BUTTONS, appear ONLY on row hover (not always visible), fade in 100ms

NEVER:
- put a primary button inside a row (use ghost/secondary only; primary is page-level)
- show all actions always (noise — hide low-frequency ones in a ⋯ menu)
- use heavy row borders (#9CA3AF) — use #F3F4F6 almost-invisible
- forget the empty state (table body becomes empty-state component, header preserved)
- forget the loading skeleton (row skeletons matching cell shapes, NOT bare spinner)
- make rows non-keyboard-navigable (Tab + Enter must reach and open each row)
```

## Prompt fragment (Chinese)

```text
表格/列表行规格(Linear 风格,3 种密度):
- 默认密度:COMFORTABLE——行高 40px,上下内边距 8px,字号 14px
- 紧凑密度:行高 32px,上下内边距 4px,字号 13-14px(给数据密集的后台/审计日志/日志查看器)
- 宽松密度:行高 48px,上下内边距 12px,字号 14px(给消费者/移动端)
- 行间分隔线:1px 实线 #F3F4F6(极浅,几乎看不见——不是粗线)
- 行 hover:背景 #F9FAFB(gray-50),100ms ease-out
- 行选中:背景 #EEF2FF(主色 8% 透明度)加 左侧 2px #5E6AD2 边框
- 行 focus:2px 内嵌环 #5E6AD2(键盘导航用)

行结构(从左到右):
- 选择 checkbox:16px,左内边距 16px,垂直居中
- 主文本:14px 字重 500 #111827,单行省略+hover 显示完整 tooltip
- 次文本(元数据):13px 字重 400 #6B7280,距主文本 8px
- 状态 badge:高 20px,左右内边距 8px,见 badge 规格
- 头像(如有指派人):24px 圆形,间距 8px
- 操作:幽灵图标按钮,只在 行 hover 时出现(不要一直显示),100ms 淡入

绝对不要:
- 在行里放主按钮(用 ghost/secondary;主按钮是页面级)
- 所有操作一直显示(把低频的收进 ⋯ 菜单)
- 用粗行边框(#9CA3AF)——用 #F3F4F6 几乎看不见的
- 忘了空状态(表格主体变成空状态组件,表头保留)
- 忘了加载骨架(行骨架匹配单元格形状,不是裸 spinner)
- 行不可键盘导航(Tab + Enter 必须能到每行并打开)
```

## Tailwind classes

```tsx
<table className="w-full">
  <tbody className="divide-y divide-[--color-border-default]">
    {rows.map(row => (
      <tr
        key={row.id}
        onClick={() => openDetail(row)}
        className="h-10 cursor-pointer transition-colors hover:bg-[--color-bg-muted] focus-within:ring-2 focus-within:ring-inset focus-within:ring-[--color-border-focus] data-[selected=true]:bg-[--color-state-primary]/8 data-[selected=true]:shadow-[inset_2px_0_0_var(--color-state-primary)]"
        data-selected={row.selected}
      >
        <td className="w-12 px-4"><Checkbox checked={row.selected} /></td>
        <td className="px-3">
          <span className="block truncate text-sm font-medium text-[--color-text-primary]">{row.title}</span>
        </td>
        <td className="px-3 text-[13px] text-[--color-text-secondary]">{row.due}</td>
        <td className="px-3"><Badge>{row.status}</Badge></td>
        <td className="px-3"><Avatar src={row.assignee.avatar} size={24} /></td>
        <td className="px-3 text-right opacity-0 transition-opacity group-hover:opacity-100">
          <IconButton aria-label="More">⋯</IconButton>
        </td>
      </tr>
    ))}
  </tbody>
</table>
```

## Density toggle (optional, for power tools)

If you offer a density toggle (Linear does, Notion does), it's a small segmented control in the table toolbar:

```text
[≡ compact] [≡ comfortable ✓] [≡ spacious]
```

Persist the choice per user (localStorage or user preference).

## Reverse examples

| Aspect | Plastic | Human |
| --- | --- | --- |
| density | one default for everyone | 3 options, default comfortable, persisted per user |
| row border | heavy #9CA3AF | near-invisible #F3F4F6 |
| actions | always visible, cluttering | fade in on row hover |
| empty | "暂无数据" four words | empty-state component, 3-classified |
| loading | bare spinner center | row skeletons matching cell shapes |
| primary text | wraps to 2 lines, breaks layout | truncate single-line + tooltip |
| keyboard | mouse-only | Tab reaches every row, Enter opens |

## Composes with

- `checkbox.md` — row selection (16px, left-aligned)
- `avatar.md` — assignee column (24px circle)
- `badge.md` — status column (20px tall pill)
- `button.md` — row-hover actions (ghost icon buttons only)
- `empty-state.md` — replaces tbody when no data
- `skeleton.md` — replaces tbody while loading
- `drawer.md` — opens on row click, preserves list scroll

## Failure modes

| Failure | Fix |
| --- | --- |
| primary button in row | demote to ghost; page-level primary only |
| heavy row borders | switch to #F3F4F6 |
| actions always visible | fade in on hover, hide low-freq in ⋯ |
| wraps text | truncate + tooltip |
| no empty/loading | replace tbody with empty-state / skeleton |
| non-keyboard-navigable | Tab + Enter must work |
