# Component: Badge / Tag / Pill

Small status labels. Article line 1444: every product has status indicators — AI uses inconsistent sizes (one is 18px, another 22px). Freeze the spec.

## Spec table (pixel-exact)

| Token | Value |
| --- | --- |
| height | 20px (`h-5`) default, 24px (`h-6`) large |
| padding-x | 8px (`px-2`) default, 12px (`px-3`) large |
| padding-y | 0 |
| radius | 9999px (`rounded-full`) — pill, ALWAYS |
| font | 12px / 500 (`text-xs font-medium`) default, 13px large |
| line-height | 1 (centered) |
| border | none or 1px subtle |
| icon (optional) | 12px (`size-3`), 4px gap left of label |
| dot (status indicator) | 6px circle (`size-1.5`), 6px gap left of label |

## Variants by purpose

| Variant | Bg | Text | Use |
| --- | --- | --- | --- |
| neutral | `color.bg.muted` (#F3F4F6) | `color.text.secondary` (#6B7280) | default, informational |
| success | green-100 (#DCFCE7) | green-700 (#15803D) | done, active, healthy |
| warning | amber-100 (#FEF3C7) | amber-700 (#B45309) | pending, at-risk |
| danger | red-100 (#FEE2E2) | red-700 (#B91C1C) | failed, blocked, overdue |
| info | blue-100 (#DBEAFE) | blue-700 (#1D4ED8) | in-progress, synced |
| outline | transparent | `color.text.secondary` + 1px border | secondary tag, removable |

## Status dot variant (no bg, just colored dot + label)

For denser contexts (table rows, list items):

```text
● Done          ← green dot
● In progress   ← blue dot
● Overdue       ← red dot
```

- dot: 6px circle, colored, 6px gap right of label
- label: 13px secondary text
- no bg, no border

## Removable tag (with X)

```text
[design ×]  ← chip with remove button
```

- X icon: 12px, 4px gap right of label
- hover on X: bg darken slightly, cursor pointer
- click X: removes the tag (with optional undo toast)

## States

| State | Visual |
| --- | --- |
| default | variant bg + text |
| hover (removable) | bg darken slightly, X icon appears |
| disabled | opacity 0.5 |

## Prompt fragment (English)

```text
Badge/tag/pill spec (pixel-exact):
- container: 20px tall (24px large), padding 0 horizontal 8px (12px large), 0 vertical
- radius: 9999px (pill) — ALWAYS pill, never square corners
- typography: 12px weight 500 (13px large), line-height 1, centered vertically
- icon (optional): 12px, 4px gap LEFT of label
- status dot (optional): 6px circle, 6px gap LEFT of label, colored by status

variants (bg / text pairs):
- neutral:   bg #F3F4F6  text #6B7280  (default, informational)
- success:   bg #DCFCE7  text #15803D  (done, active, healthy)
- warning:   bg #FEF3C7  text #B45309  (pending, at-risk)
- danger:    bg #FEE2E2  text #B91C1C  (failed, blocked, overdue)
- info:      bg #DBEAFE  text #1D4ED8  (in-progress, synced)
- outline:   bg transparent  text #6B7280  + 1px #E5E7EB border (removable tags)

removable tag:
- X icon 12px, 4px gap RIGHT of label
- hover on tag: bg darken slightly, X becomes visible/clickable
- click X: removes tag (toast undo optional)

NEVER:
- use square corners on a badge (always pill 9999px)
- mix sizes within the same context (all 20px or all 24px, not both)
- use bare color names ("red badge") — use the variant token (danger)
- use a badge for primary actions (badges label, they don't act)
- use status dot larger than 6px (gets noisy in dense lists)
```

## Prompt fragment (Chinese)

```text
徽章/标签/胶囊规格(精确到像素):
- 容器:高 20px(大 24px),内边距 上下0 左右8px(大 12px)
- 圆角:9999px(胶囊)——永远是胶囊,绝不方角
- 字体:12px 字重 500(大 13px),行高 1,垂直居中
- 图标(可选):12px,距文字左侧 4px
- 状态点(可选):6px 圆点,距文字左侧 6px,按状态着色

变体(背景/文字 配对):
- neutral(中性):背景 #F3F4F6  文字 #6B7280(默认、信息)
- success(成功):背景 #DCFCE7  文字 #15803D(完成、活跃、健康)
- warning(警告):背景 #FEF3C7  文字 #B45309(待处理、有风险)
- danger(危险):背景 #FEE2E2  文字 #B91C1C(失败、阻塞、逾期)
- info(信息):背景 #DBEAFE  文字 #1D4ED8(进行中、已同步)
- outline(描边):背景透明  文字 #6B7280 + 1px #E5E7EB 边框(可移除标签)

可移除标签:
- X 图标 12px,距文字右侧 4px
- 标签 hover:背景略加深,X 变可见/可点
- 点 X:移除标签(可选 toast 撤销)

绝对不要:
- 徽章用方角(永远胶囊 9999px)
- 同一上下文里混用尺寸(全 20px 或全 24px,不要混)
- 用裸颜色名("红色徽章")——用变体 token(danger)
- 用徽章做主操作(徽章是标签,不是动作)
- 状态点大于 6px(密集列表里会变吵)
```

## Tailwind classes

```tsx
// default badge
<span className="inline-flex h-5 items-center gap-1 rounded-full bg-[--color-bg-muted] px-2 text-xs font-medium text-[--color-text-secondary]">
  <span className="size-1.5 rounded-full bg-[--color-success]" />  {/* status dot */}
  Done
</span>

// success variant
<span className="inline-flex h-5 items-center rounded-full bg-[--color-success]/15 px-2 text-xs font-medium text-[--color-success]">
  Active
</span>

// removable tag
<span className="group inline-flex h-6 items-center gap-1 rounded-full border border-[--color-border-default] px-3 text-xs font-medium text-[--color-text-secondary]">
  design
  <button aria-label="Remove tag" className="size-3 opacity-0 transition-opacity group-hover:opacity-100 hover:text-[--color-text-primary]">×</button>
</span>
```

## Reverse examples

| Aspect | Plastic | Human |
| --- | --- | --- |
| corners | square or inconsistent | always pill 9999px |
| sizes | 18px here, 22px there | all 20px (or all 24px large) |
| color naming | "red badge" | variant token (danger) |
| removable X | always visible (noisy) | appears on hover |
| status dot | 8px+ (noisy) | 6px |

## Composes with

- `table-row.md` — status column
- `card.md` — header status indicator
- `avatar.md` — presence dot uses same 6px spec

## Failure modes

| Failure | Fix |
| --- | --- |
| square corners | change to rounded-full |
| mixed sizes | pick one (20px default) |
| bare color names | use variant tokens |
| noisy always-visible X | fade in on hover |
