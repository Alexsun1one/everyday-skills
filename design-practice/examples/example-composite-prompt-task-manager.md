# Example: Composite Prompt — Task Manager Page

This shows how the pixel-precise component dictionary composes into **one page-level prompt**. The user says "做个任务管理页"; the skill doesn't say "make a task manager" — it emits the prompt below, with every component's spec frozen in.

Feed this composite prompt to an image model (for the visual) OR a code agent (for the implementation). Either way, the output is near-deterministic because there's no room to invent pixels.

## The user's one-line intent

```
做个任务管理页
```

## The skill's response — composite prompt (English)

```text
PAGE: Task manager — list view with detail drawer

LAYOUT (3-zone shell, from components/nav-sidebar.md):
- top bar: 56px tall, bg #FFFFFF, 1px #E5E7EB bottom border, sticky
  - LEFT: mobile menu toggle (hidden desktop) + breadcrumb "Projects / Acme Inc / Tasks"
  - RIGHT: notifications bell (24px, red dot if unread, 8px gap) + user avatar (32px circle, opens menu)
- sidebar: 240px wide, bg #FFFFFF, 1px #E5E7EB right border, padding 12px
  - nav items: 36px tall, 12px padding-x, radius 8px, 18px icon + 12px gap + 14px label
  - active item (Tasks): bg #5E6AD2 at 8% opacity, text #111827, icon primary-tinted, aria-current="page"
  - hover item: bg #F9FAFB, 100ms
  - footer: "+ New task" primary button (full width, 36px tall)
- main content: flex-1, bg #F9FAFB (canvas), padding 24px

MAIN CONTENT:
- page header: "Tasks" 24px/600 + description "14 active, 3 due this week" 14px/secondary, 16px below
- toolbar: row with [search input 320px] [filter button ghost] [density toggle segmented] [view toggle list/board], 16px gap, 24px below header
- table (comfortable density, from components/table-row.md):
  - header row: 40px tall, bg #F9FAFB, 12px #6B7280 uppercase 11px/500 labels, 1px #F3F4F6 bottom border
  - body rows: 40px tall, bg #FFFFFF, 1px #F3F4F6 between rows (near-invisible)
    - row anatomy L→R: [checkbox 16px, padding-left 16px] [task title 14px/500 truncate+tooltip] [assignee avatar 24px circle] [due date 13px secondary] [status badge 20px pill] [⋯ actions ghost icon, appears on row hover]
  - row hover: bg #F9FAFB, ⋯ actions fade in 100ms
  - row selected: bg #5E6AD2 at 8% + 2px left primary border
  - row click: opens right-side drawer (below)
  - keyboard: Tab reaches each row, Enter opens, focus = 2px inset primary ring

STATES (mandatory, from components/*.md):
- loading: table body shows 8 skeleton rows (rectangle blocks matching cell shapes, bg #F3F4F6 pulse animation). Toolbar stays visible.
- empty INITIAL (new team, no tasks): table body replaced by empty-state component
    - illustration 96px grayscale line art (folder with +)
    - title 16px/600: "Create your first task"
    - description 14px/secondary: "Tasks help you track what needs to get done. Start by creating one."
    - CTA: primary button "+ New task"
- empty NO-RESULTS (filters matched nothing): different empty-state
    - illustration 64px (magnifier)
    - title: "No tasks match your filters"
    - description: echoes active filters as chips "Status=Done · Assignee=You"
    - CTA: secondary button "Clear filters"
- empty ERROR (failed to load): third empty-state
    - illustration 64px (warning triangle)
    - title: "Couldn't load tasks"
    - description: "Check your connection and try again. Your filters are preserved."
    - CTA: secondary button "Retry"
- row error: row stays in list, badge turns danger "Failed", tooltip on hover explains

DETAIL DRAWER (opens on row click, from components/drawer.md):
- width 480px, full height, slides from right 240ms cubic-bezier(0.22, 1, 0.36, 1)
- overlay bg-black/40 fade 200ms
- header 16/24 padding: title "Edit task" 16px/600 + description "Changes save when you click Save." 14px/secondary + X close icon button right, 1px bottom border
- content 24px padding, scrollable:
  - form fields (from components/input.md):
    - "Task title" text input (36px tall, 12/8 padding, radius 8px, 1px #E5E7EB border, focus = 2px #5E6AD2 border + 2px ring outside = 4px accent)
    - "Description" textarea (same border/focus rules, min-height 96px)
    - "Assignee" select (avatar 24px + name + chevron)
    - "Due date" date picker
    - "Status" select (badge preview + chevron)
  - each field: label 14px/500 above (6px gap), helper 12px/secondary below (4px gap), error replaces helper when fires
  - validation: on blur (not per keystroke); once in error, re-validate per keystroke
- footer 16/24 padding, 1px top border, right-aligned:
  - Cancel (secondary) + Save (primary), 8px gap
  - dirty state: if user edited, ESC / overlay-click triggers discard-confirm modal (not silent close)
  - Save click: button enters loading (spinner 16px left of label "Saving…", aria-busy, BLOCKS re-click — prevents double-submit)
  - Save success: 200ms green flash on button → revert, drawer stays open, toast "Task saved" top-right 4000ms
  - Save error: 200ms horizontal shake on button, focus ring red, inline error below button "Save failed — retry", draft preserved

DELETE (from components/modal.md + toast.md):
- row ⋯ menu → "Delete" → destructive modal
- modal 448px, centered, overlay bg-black/50
- header: ⚠ icon 24px danger + "Delete task" 16px/600
- content: "This will permanently delete 'Fix login bug' and remove all comments. This cannot be undone." 14px/secondary
- footer: Cancel (secondary, AUTOFOCUS — safe default) + "Delete task" (destructive red)
- NO overlay-click close, NO ESC close (prevent muscle-memory dismissal)
- on confirm: modal closes, row animates out (collapse 200ms), toast appears "Task deleted" + [Undo] action (persistent 8000ms)
- Undo: row animates back in, toast dismisses

TOKENS (from references/stage2-design-tokens.md):
- color.state.primary = #5E6AD2 (Linear violet) — single accent, used for: active nav item, primary buttons, focus rings, selected row, links
- color.bg.canvas = #F9FAFB (page bg), color.bg.surface = #FFFFFF (cards/inputs), color.bg.muted = #F9FAFB (hover)
- color.text.primary = #111827, color.text.secondary = #6B7280
- color.border.default = #E5E7EB, color.border.focus = #5E6AD2, color.danger = #DC2626
- font: Inter var, weights 400/500/600 (or 510/590 if using Linear's custom axis)
- spacing: 4px grid (4/8/12/16/24/32/48/64/96…), NO off-grid values
- radius: 4px (chips) / 8px (buttons, inputs — workhorse) / 12px (cards) / 9999px (badges only)
- motion: 100ms (hover/press) / 180ms (default — Linear timing) / 240ms (drawer/modal enter), cubic-bezier(0.22, 1, 0.36, 1), pressed scale 0.97

ABSOLUTE NEVER (the plastic tells this spec refuses):
- remove focus ring "for clean look"
- "暂无数据" four-word empty state
- two primary buttons on one screen
- modal for the edit form (use drawer — preserves list context)
- silent drawer close on unsaved changes
- allow re-click during Save loading
- "OK" / "Confirm" as destructive button label (use the verb "Delete task")
- default focus on Confirm in destructive modal (must be Cancel)
- table with heavy row borders (use #F3F4F6 near-invisible)
- row actions always visible (hide in ⋯, show on hover)
- non-keyboard-navigable table (Tab + Enter must work)
- off-grid padding (no 13px, 17px, 22px — only 4px multiples)
- mix radius within the page (badges 9999px, buttons/inputs 8px, cards 12px, that's it)
- bare color names ("red badge") — use variant tokens (danger)
```

## The same composite prompt (Chinese, for CN-flavored output)

```text
页面:任务管理——列表视图 + 详情抽屉

布局(三区框架,见 components/nav-sidebar.md):
- 顶栏:高 56px,背景 #FFFFFF,1px #E5E7EB 下边框,sticky
  - 左:移动端菜单切换(桌面隐藏)+ 面包屑"项目 / Acme Inc / 任务"
  - 右:通知铃铛(24px,未读红点,间距 8px)+ 用户头像(32px 圆,点开菜单)
- 侧边栏:宽 240px,背景 #FFFFFF,1px #E5E7EB 右边框,内边距 12px
  - 导航项:高 36px,左右内边距 12px,圆角 8px,18px 图标 + 12px 间距 + 14px 标签
  - 激活项(任务):背景 #5E6AD2 8% 透明度,文字 #111827,图标主色调,aria-current="page"
  - hover 项:背景 #F9FAFB,100ms
  - 底部:"+ 新建任务"主按钮(全宽,高 36px)
- 主内容:flex-1,背景 #F9FAFB(画布),内边距 24px

主内容:
- 页头:"任务" 24px/600 + 描述"14 个进行中,3 个本周到期" 14px/secondary,距顶部 16px
- 工具栏:一行 [搜索框 320px] [筛选按钮 ghost] [密度切换分段] [视图切换 列表/看板],间距 16px,距页头 24px
- 表格(舒适密度,见 components/table-row.md):
  - 表头行:高 40px,背景 #F9FAFB,12px #6B7280 大写 11px/500 标签,1px #F3F4F6 下边框
  - 正文行:高 40px,背景 #FFFFFF,行间 1px #F3F4F6(极浅,几乎看不见)
    - 行结构 从左到右:[checkbox 16px,左内边距 16px] [任务标题 14px/500 单行省略+tooltip] [指派人头像 24px 圆] [截止日 13px secondary] [状态 badge 20px 胶囊] [⋯ 操作 ghost 图标,行 hover 时出现]
  - 行 hover:背景 #F9FAFB,⋯ 操作 100ms 淡入
  - 行选中:背景 #5E6AD2 8% + 左侧 2px 主色边框
  - 行点击:打开右侧抽屉(见下)
  - 键盘:Tab 到每行,Enter 打开,focus = 2px 内嵌主色环

状态(强制,见 components/*.md):
- 加载:表体显示 8 行骨架(匹配单元格形状的矩形块,背景 #F3F4F6 脉冲)。工具栏保留。
- 空状态 初始(新团队无任务):表体替换为空状态组件
    - 插图 96px 灰度线稿(带 + 的文件夹)
    - 标题 16px/600:"创建你的第一个任务"
    - 描述 14px/secondary:"任务帮你跟踪要做的事。先创建一个吧。"
    - CTA:主按钮"+ 新建任务"
- 空状态 无结果(筛选无匹配):不同的空状态
    - 插图 64px(放大镜)
    - 标题:"没有任务匹配你的筛选"
    - 描述:回显当前筛选为芯片"状态=已完成 · 指派=你"
    - CTA:secondary 按钮"清除筛选"
- 空状态 错误(加载失败):第三个空状态
    - 插图 64px(警告三角)
    - 标题:"无法加载任务"
    - 描述:"请检查网络后重试。你的筛选会保留。"
    - CTA:secondary 按钮"重试"
- 行错误:行留在列表里,badge 变 danger"失败",hover tooltip 解释

详情抽屉(行点击打开,见 components/drawer.md):
- 宽 480px,全高,从右滑入 240ms cubic-bezier(0.22, 1, 0.36, 1)
- 遮罩 bg-black/40 淡入 200ms
- 头部 内边距 16/24:标题"编辑任务" 16px/600 + 描述"点击保存时更改生效。" 14px/secondary + 右侧 X 关闭图标按钮,1px 下边框
- 内容 内边距 24px,可滚动:
  - 表单字段(见 components/input.md):
    - "任务标题"文本框(高 36px,内边距 12/8,圆角 8px,1px #E5E7EB 边框,focus = 2px #5E6AD2 边框 + 外侧 2px 环 = 总共 4px 强调)
    - "描述"textarea(同样边框/focus 规则,最小高 96px)
    - "指派人"选择器(头像 24px + 名字 + 箭头)
    - "截止日期"日期选择器
    - "状态"选择器(badge 预览 + 箭头)
  - 每个字段:标签 14px/500 在上方(间距 6px),辅助文字 12px/secondary 在下方(间距 4px),出错时辅助被错误替换
  - 校验:失焦时(不要每输入一字);一旦出错,之后每输入一字重新校验
- 底部 内边距 16/24,1px 上边框,右对齐:
  - 取消(secondary)+ 保存(主),间距 8px
  - dirty 态:用户改了,ESC / 点遮罩 触发放弃确认弹窗(不要静默关闭)
  - 点保存:按钮进入 loading(spinner 16px 在"保存中…"文字左侧,aria-busy,屏蔽重复点击——防重复提交)
  - 保存成功:按钮 200ms 闪绿 → 恢复,抽屉保持打开,右上角 toast"任务已保存"4000ms
  - 保存失败:按钮 200ms 横向抖动,focus 环变红,按钮下方就地错误"保存失败——重试",草稿保留

删除(见 components/modal.md + toast.md):
- 行 ⋯ 菜单 →"删除"→ 破坏性模态
- 模态 448px,居中,遮罩 bg-black/50
- 头部:⚠ 图标 24px danger +"删除任务" 16px/600
- 内容:"此操作将永久删除'修复登录 bug'并移除所有评论。不可撤销。" 14px/secondary
- 底部:取消(secondary,自动聚焦——安全默认)+"删除任务"(destructive 红)
- 不允许点遮罩关闭,不允许 ESC 关闭(防肌肉记忆误删)
- 确认后:模态关闭,行动画消失(折叠 200ms),toast 出现"任务已删除" + [撤销] 操作(持续 8000ms)
- 撤销:行动画回来,toast 消失

令牌(见 references/stage2-design-tokens.md):
- color.state.primary = #5E6AD2(Linear 紫)——单一强调色,用于:激活导航项、主按钮、focus 环、选中行、链接
- color.bg.canvas = #F9FAFB(页面底),color.bg.surface = #FFFFFF(卡片/输入),color.bg.muted = #F9FAFB(hover)
- color.text.primary = #111827,color.text.secondary = #6B7280
- color.border.default = #E5E7EB,color.border.focus = #5E6AD2,color.danger = #DC2626
- 字体:Inter var,字重 400/500/600(或用 Linear 自定义轴 510/590)
- 间距:4px 网格(4/8/12/16/24/32/48/64/96…),不要离格值
- 圆角:4px(芯片)/ 8px(按钮、输入——主力)/ 12px(卡片)/ 9999px(仅徽章)
- 动效:100ms(hover/按下)/ 180ms(默认——Linear 时序)/ 240ms(抽屉/模态进入),cubic-bezier(0.22, 1, 0.36, 1),按下 scale 0.97

绝对不要(本规格拒绝的塑料特征):
- 为了"干净"删掉 focus ring
- "暂无数据"四个字的空状态
- 一屏两个主按钮
- 编辑表单用模态(用抽屉——保留列表上下文)
- 有未保存修改时静默关闭抽屉
- 保存 loading 时还允许重复点击
- 破坏性按钮用"确定"/"确认"(用动词"删除任务")
- 破坏性模态默认聚焦在确认(必须在取消)
- 表格用粗行边框(用 #F3F4F6 几乎看不见)
- 行操作一直显示(收进 ⋯,hover 时显示)
- 表格不能键盘导航(Tab + Enter 必须能用)
- 离格内边距(不要 13、17、22——只要 4 的倍数)
- 同页混用圆角(badge 9999px,按钮/输入 8px,卡片 12px,就这些)
- 用裸颜色名("红色徽章")——用变体 token(danger)
```

## Why this composite prompt is near-deterministic

Count the frozen decisions in it:
- **Layout**: 3-zone shell, 56px top bar, 240px sidebar, exact nav item spec
- **Table**: 40px rows, exact cell anatomy, hover/selected/keyboard behavior
- **3 distinct empty states** with distinct illustrations, titles, CTAs
- **Drawer**: 480px, exact animation, dirty-confirm, focus trap
- **Form**: input 36px, 4px focus accent, blur-then-live validation, draft preserved
- **Save flow**: loading blocks re-click, success = flash + toast, error = shake + inline
- **Delete flow**: destructive modal, Cancel autofocus, verb label, no overlay-close, undo toast
- **Tokens**: every color/spacing/radius/motion value named, no invention
- **~25 "absolute never" rules** catching the specific plastic tells

An image model or code agent receiving this has **no room to drift** — it's not "make a task manager", it's "make exactly this task manager with these exact pixels". That's the precision layer the component dictionary buys.

## How to extend this pattern

When the user asks for a different page (settings, dashboard, kanban, form-wizard):
1. Identify the components (most pages reuse the Tier-1 twelve).
2. Pull each component's Prompt Fragment from `components/<name>.md`.
3. Stitch them into a page-level composite prompt with the layout + tokens + absolute-never list.
4. Add page-specific states (a dashboard needs chart-loading skeletons; a wizard needs step-state variants).

The component dictionary is the **reusable precision substrate**; the composite prompt is the **page-level assembly**.
