---
type: audit-summary
created: 2026-06-27
source: _audit-1-3.md + _audit-4-6.md + _audit-7-9.md + _audit-10-12.md
note: 4 个精读子任务的全景汇总。交叉去重 + 按"对治 AI 味的直接性"重排 P0。
---

# 精读盲点全景汇总

## 总览

| 编 | 盲点数 | P0 | P1 | P2 |
|---|---|---|---|---|
| 第 1-3 编（总论/视觉/组件） | 12 | 3 | 6 | 3 |
| 第 4-6 编（动效/IA/LLM 命令） | 8 | 1 | 4 | 3 |
| 第 7-9 编（Agent/Vibe/验收） | 15 | 5 | 6 | 4 |
| 第 10-12 编（工作法/案例/实战） | 9 | 3 | 4 | 2 |
| **合计** | **44** | **12** | **20** | **12** |

## 12 个 P0（按"对治 AI 味的直接性"重排）

> 重排依据：CRM demo 翻车的三个直接证据 = 字重全 500 / 字号全 14-16 / accent 全 violet（"一屋子人同时喊话"）。哪个 P0 最能治这三个病，排前面。

### 第一梯队：直击 CRM demo 翻车根因（6 个）

| # | 盲点 | 出处 | 补法 | 治什么病 |
|---|---|---|---|---|
| **P0-1** | 配色策略总纲（中性灰托底+主色点睛+状态色守规矩+强色小面积+渐变要有理由） | 1-3 编 #1 / 行 336-352 | 新增到 `visual-language/README.md` 顶部 | 治"accent 全 violet"——AI 满屏主色 = 没主色 |
| **P0-2** | 整张卡片可点 vs 内部按钮可点 冲突规则 | 1-3 编 #2 / 行 608 | 修订 `components/card.md` | 治 dashboard 卡片网格"点哪都触发"混乱 |
| **P0-3** | Banner 组件（持久性 inline message） | 1-3 编 #3 / 行 620 | 新建 `components/banner.md` | 治"权限不足/离线塞进 toast 自动消失" |
| **P0-4** | AI 自审 prompt loop（生成中切换评审员挑刺） | 4-6 编 #1 / 行 906-935 | 新建 `references/ai-self-review-loop.md` | 重做 demo 时跑生成 loop，把 AI 味按在地上 |
| **P0-5** | 统一 P0/P1/P2 五段式输出格式（P0必修/P1应修/P2可优化/通过项/需人工复核） | 7-9 编 #9 / 行 1799-1821 | 修订 `qa-p0p1p2.md` 顶部 + 各 qa-* 统一 | 验收时横向可比对 |
| **P0-6** | 世界级打磨清单（带 gate：验收全过才准打磨） | 7-9 编 #11 / 行 1844-1864 | 新建 `references/qa-polish.md` | 治"打磨和修 bug 混在一起"——原文金句"提交失败会丢内容，动效再柔也没用" |

### 第二梯队：skill 完整性 P0（6 个，不直接阻塞 CRM demo）

| # | 盲点 | 出处 | 补法 |
|---|---|---|---|
| **P0-7** | 图像模型 prompt 缺"取舍"段（结构/状态/取舍三支柱只冻了两支柱） | 7-9 编 #1 / 行 1016-1022 | `prompt-templates.md` Template 2 加 `[TRADEOFFS]` |
| **P0-8** | Vibe Coding 六阶段总提示词（"每阶段等我确认"gate 型） | 7-9 编 #4 / 行 1376-1414 | `prompt-templates.md` 加 Template 4 |
| **P0-9** | Vibe Coding 四步版总提示词（单页实战版） | 7-9 编 #5 / 行 1565-1601 | `prompt-templates.md` 加 Template 5 |
| **P0-10** | 五层刀法的非 token 层完整拆解（Task/Structure/State/Tradeoff 层全缺，只有 System 层） | 10-12 编 #2 / 行 2339-2460 | 为 Linear/Stripe/Notion 各补 `armory/0Na-dissect-*.md` |
| **P0-11** | 坏页面改造四步（删/归/补/磨）——skill 只会"白纸→产品"，不会"坏→好" | 10-12 编 #3 / 行 2035-2069 | 新建 `workflow/07-rescue-bad-page.md` |
| **P0-12** | 设计复盘工作流（事故→规则沉淀六问）——闭环在"上线"就断 | 10-12 编 #1 / 行 2307-2323 | 新建 `workflow/06-incident-retrospect.md` |

## 20 个 P1（按主题归组）

### 视觉与组件细节（7 个，来自 1-3 编）
- Superhuman "100ms 响应" SLA + 反面样板"功能堆成山" → `case-studies.md`
- 主按钮位置规则（右下/居中/跟随表单）→ `components/button.md`
- 行宽限制（中文 30-40 字/行）→ `components/README.md` + `04-visual-hierarchy.md`
- 对齐作为视觉层级第七杠杆（现有六杠杆漏了"对齐"）→ `design-judgment/04-visual-hierarchy.md`
- 表单"能自动就自动"原则 → `components/input.md`
- Tabs + 移动端 Bottom Tab 组件缺失 → 新建 `components/tabs.md` + `bottom-tab.md`
- 标签对齐三种取舍（顶/左/内联）→ `components/input.md`

### 反馈与坐标感（2 个，来自 4-6 编）
- 任务级反馈链（click→pressed→loading→success/error 时间轴）→ 新建 `references/stage2-feedback-chain.md`
- 坐标感 5 件套（尤其"返回后保留列表滚动位置"反塑料锚点）→ `patterns/03` 或新建 `patterns/07-spatial-continuity.md`

### 提示词与任务卡（3 个，来自 4-6 编 + 7-9 编）
- 坏提示词 vs 好提示词对照诊断（7 项诊断点）→ `prompt-templates.md` 开头
- 跨工具分工矩阵（找料-推理-成文-落库）→ 新建 `references/tool-division.md`
- 产品任务书"差写法 vs 好写法"对照 + "设计约束"独立字段 → `stage1-task-card.md` + `workflow/02`

### Vibe Coding 细节（3 个，来自 7-9 编）
- 设计系统最小包的"开工命令"prompt → `prompt-templates.md` Template 6
- 页面交付顺序（列表→详情→创建→筛选→状态→移动→深色→设置/团队/通知最后）→ `workflow/05` 或新建 `workflow/06-page-delivery-order.md`
- "AI 不能当最终裁判"边界（假阴性 + 假阳性两种失败模式）→ `qa-p0p1p2.md`

### 团队工作法（5 个，来自 10-12 编）
- 每天看页面练眼睛的 5 层读图 checklist → `patterns/07` 或新建 `patterns/08`
- 一个月训练计划（4 周）→ 新建 `learning/one-month-plan.md`
- 需求评审/代码评审 7 问（设计评审已有）→ `workflow/04` 扩展
- AI 三件套打包概念（任务书+系统最小包+验收清单）→ 新建 `workflow/08-ai-three-pack.md`
- 设计任务单字段核对（信息结构四档/最危险的错误/是否撤销）→ `workflow/02-design-task-brief.md`

## 12 个 P2（略，详见各 audit 文件）

主要包括：字重梯度补 700、5 秒测试操作化、转场四类分类表、AI 易漏 6 件事整合表、产品气质字段、Apple HIG armory 悬空 bug、结语五习惯收束图、坏数据 7 类 vs 6 类口径差等。

## 已覆盖充分（无需补，证明对照过）

skill 已经冻结得很完整的部分（节选）：
- 好设计五指标 + 四原则 + 六大经典人机规律 → `design-judgment/00-principles.md`
- 视觉层级六杠杆 + 5-3-2 权重 → `design-judgment/04-visual-hierarchy.md`
- 三层 token + WCAG + 深色模式 + 8 点网格 + 字阶 + 阴影圆角分级 → `stage2-design-tokens.md`
- 按钮 8 状态 + 触控目标 44/48px + 一屏一个主帅 → `components/button.md`
- 空状态三分 + 反馈容器分类 + 导航三问 → `components/*`
- 时长缓动 + 微交互四件套 + prefers-reduced-motion → `stage2-motion-discipline.md` + `stage2-microinteractions.md`
- 渐进披露 + 容器决策树 → `patterns/06` + `patterns/03`
- Linear/Stripe/Notion 的 System 层 tokens 母版（质量高） → `armory/01-03`
- AI 协作三角色 + P0/P1/P2 评审分级 + 10 步流程 + 8 步实战 → `workflow/*`
- 案例拆解提示词 + 案例字典提示词 → `patterns/07`

## 给用户的决策建议

CRM demo 重做的核心目标是验证"Stage 0 判断卡能否治住一屋子人同时喊话"。**第一梯队的 6 个 P0 直击这个目标**——补完它们就足以让 demo 重做有意义。第二梯队的 6 个 P0 是 skill 完整性补强，不影响 demo 验证，可以 demo 之后补。
