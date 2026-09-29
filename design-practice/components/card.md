# Component: Card

The basic content container. Article line 1371 (paraphrased): a card is not a rectangle with a border — it's **information packaged into a unit**, with its own hierarchy, actions, and edges.

## Spec table (pixel-exact)

| Token | Value | Notes |
| --- | --- | --- |
| bg | `color.bg.surface` (#FFFFFF) | |
| border | 1px `color.border.default` (#E5E7EB) | hairline, not heavy |
| radius | 12px (`rounded-lg`) | matches Linear's card radius |
| padding (content) | 24px (`p-6`) default, 16px (`p-4`) compact | |
| shadow | none on default; `shadow-md` on hover IF clickable | subtle depth, not 2015 drop shadow |
| header padding | 16px 24px (`px-6 py-4`) | separated by 1px border-bottom |
| footer padding | 16px 24px (`px-6 py-4`) | separated by 1px border-top |
| gap between stacked cards | 16px (`gap-4`) | grid/flex gap, not margin on each |
| gap inside card (between sections) | 16px default, 8px tight | |

## Card anatomy

```text
┌─card radius 12px, 1px border #E5E7EB, bg #FFFFFF──────────┐
│ ┌─header (optional) padding 16/24, border-bottom 1px────┐ │
│ │ [title 16px/600]            [action-ghost button]      │ │
│ │ [description 14px/400 secondary]                       │ │
│ └────────────────────────────────────────────────────────┘ │
│ ┌─content padding 24px──────────────────────────────────┐ │
│ │ ...                                                    │ │
│ └────────────────────────────────────────────────────────┘ │
│ ┌─footer (optional) padding 16/24, border-top 1px───────┐ │
│ │            [secondary action]   [primary action]       │ │
│ └────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

## Click-target conflict rule (article line 608)

> 原文行 608:"**整张卡片可点,还是卡片里的按钮可点?如果整张卡片可点,又在里面放一堆按钮,用户就会不知道点哪里触发什么。卡片不能含糊,含糊就踩雷。**"

这是 AI 生成 dashboard / 列表卡片网格时**最常踩的雷**:整张卡片可点击打开详情,卡片里又放了三个 primary 按钮(编辑/删除/分享),用户点了"编辑"也触发了卡片点击跳详情——这是反馈通道冲突,用户瞬间失去控制感。

**卡片必须先定"是否整体可点",二选一,不能含糊。三种合法组合:**

| 组合 | 卡片本身 | 卡片内部允许的元素 | 典型场景 |
|---|---|---|---|
| **A. 整张可点(纯导航)** | 整张可点,hover 加 shadow-md,cursor pointer,**绑 onClick 跳详情** | **只允许 ghost icon**(右上角 ⋯ 更多菜单、角标徽章、纯展示性头像) | 任务列表项、CRM 联系人卡、文件列表行 |
| **B. 仅按钮可点(操作中心)** | 整张**不可点**(hover 不加 shadow-md,不绑 onClick) | 允许任意 primary/secondary 按钮(footer 主操作、行内编辑/删除) | 设置项卡、报表卡、需要原地操作的卡片 |
| **C. 选中态卡片(批量操作)** | 整张可点**仅用于勾选**(click 切换 selected,cursor pointer) | 允许 ghost icon 进入更多菜单,**禁止 primary 按钮**(选中后批量操作走工具栏) | 多选列表、批量管理页 |

### 反模式(原文行 608"含糊就踩雷")

| 反模式 | 为什么雷 | 修正 |
|---|---|---|
| 整张可点 + footer primary 按钮 | 点 primary 时事件冒泡触发卡片跳转 | 改成组合 B:整张不可点,footer 按钮可点 |
| 整张可点 + 行内三个图标按钮(编辑/删除/分享) | 三个图标按钮点击区域和卡片重叠,误触率高 | 改成组合 A:只留 ghost 更多菜单 ⋯,其余操作进菜单 |
| 卡片 hover 加 shadow-md 但 onClick 没绑 | 暗示可点但点不动,用户反复点试探 | 要么绑 onClick 走组合 A,要么去掉 shadow-md 走组合 B |
| 整张可点 + 卡片内放选中 checkbox | 点 checkbox 也触发卡片点击,状态错乱 | checkbox 用 `stopPropagation`,或走组合 C(整张 click = 切换选中) |

### Stage 2 完成后必跑的卡片冲突自查

```text
□ 每张卡片是否明确声明了组合 A/B/C?
□ 组合 A 卡片内部有没有遗漏的 primary/secondary 按钮?(应为 0)
□ 组合 B 卡片是否去掉了 hover shadow-md?(避免暗示可点)
□ 卡片内部按钮的 click 事件是否正确处理冒泡?(stopPropagation where needed)
□ 同一网格内是否混用了组合 A 和组合 B?(同一网格应统一组合)
```

## Variants

| Variant | When |
| --- | --- |
| **plain** | content card, no header/footer |
| **headed** | has title/description/action in header |
| **interactive** (clickable) | whole card clickable — hover lifts (shadow-md), cursor pointer |
| **selected** | 2px primary border replacing default, bg primary at 4% |
| **flat** (no border) | used when cards sit on a tinted bg section |
| **compact** | padding 16px instead of 24px — for dense grids |

## States

| State | Visual | Behavior |
| --- | --- | --- |
| default | white bg, 1px border | — |
| hover (interactive) | shadow-md lifts slightly, border darken | cursor pointer |
| selected | 2px primary border, bg primary at 4% | persists |
| focus (interactive) | 2px primary ring outside | keyboard reachable |
| loading | content area shows skeleton blocks | header stays |
| error | content area shows inline error + retry | header stays |

## Prompt fragment (English)

```text
Card spec (pixel-exact):
- container: bg #FFFFFF, 1px solid #E5E7EB border, radius 12px, padding 24px (16px compact)
- header (optional): padding 16px top/bottom 24px left/right, separated by 1px #F3F4F6 border-bottom
  - title: 16px weight 600 #111827
  - description: 14px weight 400 #6B7280 (gap 4px below title)
  - action: ghost icon button top-right (NOT primary)
- footer (optional): padding 16/24, separated by 1px #F3F4F6 border-top
  - actions: right-aligned, secondary first then primary, 8px gap
- interactive (clickable): hover adds shadow-md (0 4px 6px rgba(0,0,0,0.07)) + border darken, cursor pointer
  - focus: 2px #5E6AD2 ring outside the card, offset 2px
- selected: 2px #5E6AD2 border (replacing default), bg #5E6AD2 at 4% opacity
- gap between stacked cards: 16px (use grid/flex gap, not margin)
- gap inside card between sections: 16px default, 8px tight

NEVER:
- use heavy 2px+ borders on default cards (1px hairline only)
- use 2015 drop shadow (use subtle shadow-md on hover only)
- put a primary button in the header (use ghost/secondary there)
- mix radius within a card grid (all 12px)
- forget the header/footer divider border (cards look like a single block without it)
```

## Prompt fragment (Chinese)

```text
卡片规格(精确到像素):
- 容器:背景 #FFFFFF,1px 实线 #E5E7EB 边框,圆角 12px,内边距 24px(紧凑 16px)
- 头部(可选):内边距 上下16px 左右24px,1px #F3F4F6 下边框分隔
  - 标题:16px 字重 600 #111827
  - 描述:14px 字重 400 #6B7280(距标题 4px)
  - 操作:右上角 ghost 图标按钮(不是主按钮)
- 底部(可选):内边距 16/24,1px #F3F4F6 上边框分隔
  - 操作:右对齐,先 secondary 后 primary,间距 8px
- 可交互(可点击):hover 加 shadow-md(0 4px 6px rgba(0,0,0,0.07))+ 边框加深,光标 pointer
  - focus:卡片外侧 2px #5E6AD2 环,offset 2px
- 选中:2px #5E6AD2 边框(替换默认),背景 #5E6AD2 4% 透明度
- 卡片之间间距:16px(用 grid/flex gap,不要用 margin)
- 卡片内部区块间距:默认 16px,紧凑 8px

绝对不要:
- 默认卡片用 2px+ 粗边框(只用 1px 发丝线)
- 用 2015 的厚重投影(只在 hover 时用 shadow-md)
- 头部放主按钮(那里只放 ghost/secondary)
- 同一卡片网格里混用圆角(全部 12px)
- 忘了头/底部的分隔线(没有就看着像一坨)
```

## Tailwind classes

```tsx
// interactive card
<div
  role="button"
  tabIndex={0}
  className="rounded-lg border border-[--color-border-default] bg-[--color-bg-surface] p-6 shadow-none transition-all hover:border-[--color-border-strong] hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[--color-border-focus] focus-visible:ring-offset-2"
>
  {/* header */}
  <div className="-mx-6 -mt-6 mb-4 flex items-start justify-between border-b border-[--color-border-default] px-6 py-4">
    <div>
      <h3 className="text-base font-semibold text-[--color-text-primary]">Card title</h3>
      <p className="mt-1 text-sm text-[--color-text-secondary]">Short description</p>
    </div>
    <IconButton aria-label="More" variant="ghost">⋯</IconButton>
  </div>
  {/* content */}
  <div className="space-y-4">...</div>
  {/* footer */}
  <div className="-mx-6 -mb-6 mt-4 flex justify-end gap-2 border-t border-[--color-border-default] px-6 py-4">
    <Button variant="secondary">Cancel</Button>
    <Button variant="primary">Save</Button>
  </div>
</div>
```

## Reverse examples

| Aspect | Plastic | Human |
| --- | --- | --- |
| border | 2px+ heavy or none | 1px hairline #E5E7EB |
| shadow | heavy drop shadow always | none default, subtle shadow-md on hover only |
| header action | primary button | ghost icon button |
| dividers | none, looks like a block | 1px border separating header/content/footer |
| radius | mixed (4px here, 16px there) | consistent 12px throughout |
| padding | arbitrary (18px, 22px) | 24px default / 16px compact (4px grid) |

## Composes with

- `button.md` — footer actions, header ghost icon
- `badge.md` — status indicators in header
- `avatar.md` — author/assignee in header
- `table-row.md` — card wrapping a mini-table

## Failure modes

| Failure | Fix |
| --- | --- |
| heavy borders | 1px hairline only |
| heavy shadow always | none default, hover only |
| primary in header | use ghost icon |
| no dividers | add 1px border between sections |
| mixed radius | all 12px |
| off-grid padding | 24px / 16px only |
