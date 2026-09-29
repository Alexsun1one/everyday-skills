# Prompt Templates — for spec / image-model / code-agent

> Article line 1753-1822. Three prompt templates that encode this skill's discipline. Use them when invoking other AIs (image models, code agents) so they obey the five-layer rules.

## 先诊断你的 prompt 是不是"坏提示词"(原文行 867-904)

> 原文金句(行 872):"**帮我写一套好看的 SaaS 设计规范,要高级一点,参考 Linear 和 Stripe。**" —— 这是教科书级坏提示词。

**坏提示词的 7 个缺失**(任一缺失都让模型只能靠想象补洞,补得越多越危险):

```text
诊断你的 prompt:
□ 用户是谁?(缺 = 坏)
□ 产品干什么?(缺 = 坏)
□ 页面类型?(缺 = 坏)
□ 组件范围?(缺 = 坏)
□ 暗色模式/响应式断点?(缺 = 坏)
□ 状态要不要补?(缺 = 坏)
□ 输出格式?(缺 = 坏)

缺 ≥3 项 = 坏提示词,必须补齐 5 要素再生成。
缺 0-2 项 = 可接受,但建议补齐。
```

**坏提示词的反面教材**(原文行 1014,图像模型场景):"把模型当插画师,它会给你一张漂亮图:卡片很多、渐变好看、图标精致,但仔细一看——按钮没状态,表格没空态,筛选没逻辑,移动端不知道怎么办,真实数据一多就崩。"

**好提示词的 5 要素**(原文行 880-901,所有 Template 共享):角色 / 背景 / 任务 / 约束 / 输出格式。下面的 Template 1-6 都自带这 5 要素,直接套即可。

## Template 1 — Spec generation (for a text LLM)

When you want a text LLM to write a design spec for a page, encode the discipline:

```text
You are a senior product designer. Write a design spec for [page/feature] that obeys world-class discipline. Do NOT write a single pretty picture — write the skeleton first.

[CONTEXT]
product: [type]
target user: [who, scenario]
core task: [the errand]
success criteria: [how we know it's done]
non-goals (THIS ROUND): [what we're NOT doing]
key risks: [where it breaks]

[DESIGN CONSTRAINTS]
1. Use design tokens — no hardcoded colors / spacing / fonts in components.
2. Colors in three layers: primitive / semantic / component.
3. Spacing on the 4/8 grid.
4. Every interactive component covers: default / hover / active / focus / disabled / loading / success / error.
5. Every data module covers: empty (3 kinds — initial / filter / permission) / loading / error / offline.
6. One primary action per screen.
7. Complex sub-tasks use drawers; only hard interrupts use modals.
8. WCAG contrast: body ≥ 4.5:1, large ≥ 3:1.
9. Explain how each bad-design failure mode is avoided.

[OUTPUT FORMAT]
1. Design principles (3-5)
2. Information architecture (page / drawer / modal / popover choices with rationale)
3. Visual tokens (primitive / semantic / component tables)
4. Component spec (per component: states matrix)
5. Interaction state matrix (8 states × visual / copy / behavior)
6. Empty / error states (three-classified)
7. Object-state-permission matrix (object lifecycle × role × action)
8. AI-generation QA checklist
9. Self-critique: what's still missing?
```

## Template 2 — Image model (for a UI visual)

When you want an image model to draw a UI, encode the low-fi + states discipline:

```text
Grayscale wireframe of a [product type] screen. Do NOT generate a polished hi-fi render — generate a low-fi structural wireframe.

[LAYOUT]
- top bar: [description]
- main area: [description]
- side panel / drawer: [description]
- footer / status: [description]

[CONTENT]
- placeholder content only (lorem ipsum, generic labels) — NO real data, NO real logos
- show [N] items in the list with realistic but generic content

[STATES — draw at least 3 of these as separate frames]
1. default (data present)
2. loading (skeleton, NOT spinner)
3. empty — initial (illustration + value statement + primary CTA)
4. empty — filter (current filters as chips + clear button)
5. empty — permission (lock icon + explanation)
6. error (inline error + retry, preserving input)

[TRADEOFFS — 主动做出取舍决策,这是和"结构""状态"并列的第三根支柱(原文行 1016-1022)]
- 哪些信息常驻主区域(用户每次来都要看的)
- 哪些信息收进右侧抽屉/二级 tab(次重要,但需要时能快速到)
- 哪些动作收进"更多菜单" ⋯(低频,如导出/归档/批量)
- 哪些信息本页完全不出现(non-goals — 明确"这不是本页要解决的")
- **一屏只保留一个主按钮,在结构图里明确标出它是谁**(违反这条 wireframe 直接废)
- 输出一段"为什么这么取舍"的说明(不是"放这里好看",而是"主任务用户 80% 时间只需要 A,所以 B/C 进抽屉")

[STYLE — IRON RULE]
- grayscale only, NO color, NO gradient, NO shadow
- hand-drawn wireframe feel, thin gray lines
- annotations allowed (small labels pointing to blocks)
- 16:9 desktop, 1440px feel

[DO NOT]
- add color, gradient, or shadow
- make it look polished or final
- include real photos, logos, or people
- add charts, calendars, or features not listed above
- skip the state frames
```

If the model returns color or polish, REJECT and regenerate with stronger negatives.

## Template 3 — Code agent (for a coding agent like Codex / Cursor)

When you want a code agent to implement a page, encode the states + tokens + non-goals discipline:

```text
You are a senior frontend engineer. Implement [page] in React + TypeScript + Tailwind. Do NOT just implement the default state — implement the full product.

[TECH STACK]
- React + TypeScript
- Tailwind, but ALL values via design token CSS variables (no hardcoded colors / spacing)
- Components split: [list — TaskListPage, TaskToolbar, TaskTable, TaskDetailDrawer, EmptyState, ErrorState, LoadingSkeleton, Toast]

[MUST COVER — product states, not just default]
1. Default: task list with realistic mock data
2. Loading: table area shows skeleton (matching row shape), NOT bare spinner
3. Empty — initial: illustration + "还没有任务. 创建第一个任务." + primary CTA
4. Empty — filter: "没有符合当前筛选条件的任务." + clear-filters button
5. Empty — permission: "你暂时没有权限查看这些任务." + request-access button
6. Error: inline error in the list area + retry, FILTER CONDITIONS PRESERVED
7. Permission denied: Create button disabled + tooltip "You need editor role"
8. Detail drawer: opens on row click, slides from right, ESC to close, focus trap, focus returns to row on close
9. Save: button enters loading (aria-busy, spinner, label "Saving…"), BLOCKS re-click
10. Save failure: button shakes 200ms + inline "Save failed — retry", DRAFT PRESERVED
11. Keyboard: Tab reaches all controls, focus-visible rings, ⌘K command palette
12. Responsive: mobile hides sidebar (hamburger), filters move to drawer
13. Dark mode: via token swap, no separate page

[OBJECT-STATE-PERMISSION ENFORCEMENT]
object: Task, states: draft / active / done / archived / soft-deleted
- viewer: can view active/done, cannot see draft/archived, all edit actions disabled with tooltip
- editor: can view/edit active/done, cannot delete
- admin: full power including archive/restore/hard-delete
- author: special — can edit own draft, restore own soft-deleted within 30d

[DO NOT]
- add Gantt chart, calendar view, time-tracking, AI-summary (this round's non-goals)
- hardcode any color / spacing / font size
- skip any of the 13 must-cover states
- use `<div onClick>` for buttons (use semantic HTML)
- remove focus rings "for clean look"

[OUTPUT]
1. File structure
2. Component responsibilities
3. State management approach
4. State coverage table (which file implements which state)
5. Self-check against the 13 must-cover items (pass / fail per item)
6. Files needing human review
```

Article line 2099: the `[DO NOT]` block is critical. Code agents add features because more feels like more. The non-goals are a prison, not a suggestion.

## Template 4 — Vibe Coding 六阶段总提示词(gate 型,原文行 1376-1414 verbatim)

> 适用:从零做一个完整 MVP,需要强制 Agent "每阶段等我确认后再进入下一阶段"。**这个 prompt 最重要的一句是"不要直接写代码" + "每阶段等我确认"**——它把 Agent 从"乱发挥"拉回"按流程办事"。

```text
你是一位资深产品设计师、前端架构师和可用性评审,请和我一起用 Vibe Coding 做一个可运行但可靠的 MVP。

重要规则:
不要直接写代码。请按阶段工作,每阶段等我确认后再进入下一阶段。

阶段 1:产品任务澄清
- 明确目标用户、场景、核心任务、成功标准、非目标、风险。

阶段 2:信息架构
- 输出页面结构、容器选择、主次层级、响应式变化。
- 一屏只能有一个主按钮。

阶段 3:状态矩阵
- 覆盖 default / loading / empty / error / permission denied / offline。
- 所有交互组件覆盖 hover / active / focus / disabled / loading。

阶段 4:视觉与设计令牌
- 颜色使用 primitive / semantic / component 三层。
- 间距使用 4/8 点网格。
- 不允许组件直接写死颜色、字号、间距。
- 对比度满足 WCAG。

阶段 5:代码实现
- 使用指定技术栈。
- 拆分清晰组件。
- 补齐可访问性:键盘、焦点、aria、语义标签。
- 不加入非 MVP 功能。

阶段 6:验收
- 按清单自查。
- 输出未通过项和修改建议。
- 明确仍需人工确认的内容。

当前产品想法:
【在这里写你的想法】

请先执行阶段 1,只输出任务澄清,不要写代码。
```

**使用纪律**:Agent 每阶段输出后**强制停下等用户回复"继续"**。Agent 不能自己一路从阶段 1 写到阶段 6——那是没 gate 的"乱发挥"。

## Template 5 — Vibe Coding 单页实战提示词(四步版,原文行 1565-1601 verbatim)

> 适用:做一个**单页**功能(不是完整 App),要求 Agent 先建设计系统最小包、再实现页面、再自检。和 Template 4 的区别:Template 4 是多阶段 MVP,Template 5 是单页快速实战。

```text
你是我的产品设计 + 前端实现搭档。我们要用 React + TypeScript + Tailwind 做一个【产品类型】的【模块名】。

请严格按以下流程工作,不要一次性生成整个 App。

第一步:先复述产品任务书
- 用户、核心任务、成功标准、约束、边界状态。

第二步:建立设计系统最小包
- semantic colors (bg.page, bg.surface, text.primary, text.secondary, border.default, action.primary, danger, success, warning)
- spacing (4/8 点网格)
- radius (sm/md/lg/full)
- shadow (sm/md/lg)
- 基础组件:Button (primary/secondary/ghost/danger + disabled/loading/focus)、Input (label 常驻 + error/disabled/focus)、EmptyState (说明+原因+下一步)、Toast (只用于短反馈)
- 所有页面必须使用这些 token 和组件,不允许直接写死颜色和间距。

第三步:只实现【页面名】
- 覆盖 8 态 + 5 数据状态 + 权限矩阵 + 响应式 + 深色模式。
- 不加入本页不需要的功能。

第四步:输出自检报告
- 按 P0/P1/P2 五段式输出。
- 没有通过自检前,不要继续实现下一页。
```

**使用纪律**:第二步的设计系统最小包是 gate——Agent 不能跳过建包直接写页面。第三步只能写**指定的那一页**,不允许写"顺手把别的页也写了"(原文反复警告"不要一口吞整个 App")。

## Template 6 — 设计系统最小包开工命令(原文行 1452-1467 verbatim)

> 适用:任何 Vibe Coding 流程的**前置阶段**。在写任何页面之前,先冻结 token + 4 个基础组件。和 Template 4 阶段 4 / Template 5 第二步的关系:那两个是嵌在大流程里,这个是可独立调用的"建包 prompt"。

```text
在写任何页面之前,先建立设计系统最小包:

1. 定义 CSS variables:
   - semantic colors:bg.page, bg.surface, text.primary, text.secondary, border.default, action.primary, danger, success, warning
   - spacing:4/8 点网格 (4/8/12/16/20/24/32/40/48/64)
   - radius:sm (4) / md (8) / lg (12) / full (9999)
   - shadow:sm / md / lg

2. 定义基础组件:
   - Button:primary / secondary / ghost / danger,覆盖 disabled / loading / focus
   - Input:label 常驻,覆盖 error / disabled / focus
   - EmptyState:必须包含说明、原因、下一步行动
   - Toast:只用于短反馈,不承载复杂错误

3. 所有页面必须使用这些 token 和组件,不允许直接写死颜色和间距。

输出:
- 完整的 CSS variables 定义(tailwind.css :root 段)
- 4 个基础组件的 React + TypeScript 实现
- 一份"如何在新页面里只用 token、不写死值"的 3 条规则
```

## The discipline embedded in all three

All three templates encode:

1. **Five-layer skeleton before skin** — spec asks for IA + states + system + permissions, not just visuals
2. **States mandatory** — all three list the 8 button states + 5 data states explicitly
3. **Tokens mandatory** — no hardcoded values
4. **Non-goals enforced** — the DO NOT block is a prison
5. **Self-check** — every template ends with "self-critique" or "self-check", never "done"

## Failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| Spec without states | "design a dashboard" | add the must-cover states list |
| Image prompt without low-fi rule | model returns hi-fi | add grayscale-only DO NOT block |
| Code prompt without non-goals | agent adds charts / calendar | DO NOT block is mandatory |
| No self-check | agent says "done" | every template ends with self-check |
