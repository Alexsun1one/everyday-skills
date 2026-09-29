# 精读盲点清单：第 1-3 编（总论/视觉规范/组件库）

> 盲点总数：**12** ｜ P0：**3** ｜ P1：**6** ｜ P2：**3**
>
> 精读者：子任务（GLM），2026-06-27。原文 = `references/source-full.md` 行 1–630。对照文件 = `design-judgment/`、`visual-language/`、`components/`、`references/stage2-*.md`、`references/qa-*.md`、`references/armory/`、`references/case-studies.md`。

## 精读覆盖

- 开篇、目录（行 1–31）
- 第一编（行 32–286）：好设计五指标、三块样板、四原则、再看样板、两种病、实践循环、六大老规律
- 第二编（行 288–480）：颜色三层、对比度、配色章法、排版（字体/字阶/行高/字重）、间距网格、亲密性、对齐、阴影圆角图标、响应式 + 深色模式
- 第三编（行 482–626）：组件库哲学、按钮（一主帅 + 8 状态）、表单（标签常驻/错误就地/能自动就自动）、卡片导航反馈（卡片边界/导航三问/反馈容器 + 空状态）

---

## 盲点 1：配色策略总纲"中性灰托底 + 主色点睛 + 状态色各司其职"未冻结【P0】

- **原文出处**：第二编第一章（三），行 336–352，原文摘抄：「**一套中性灰托底**…**一个主色点睛**…**一组状态色守规矩**：成功用绿，警告用黄，危险用红，信息用蓝。不要把删除做成绿色，不要把成功做成红色…**强色小面积用**：强色像辣椒，少放提味，多放毁菜。**渐变要有理由**。」
- **方法论**：
  - 界面高级感七成来自灰阶稳定；主色要省着用，满屏主色 = 没主色
  - 状态色语义不可错位（删除不能绿、成功不能红）
  - 强色小面积点缀，渐变只在有品牌/引导理由时用
  - 颜色一句话总纲（行 352）：「大面积中性灰托底，小面积主色点睛，状态色各司其职，一切走语义令牌，所有文字守对比度」
- **关键数据**：5 条配色章法；"七成高级感来自灰阶"
- **案例**：Stripe 文档页（行 306）「大面积白灰黑中性色，蓝紫只在链接/重点/插图/关键行动上」；Linear（行 308）「大量灰阶暗色弱边框，主色用得很省」
- **提示词模板**：原文未单独给
- **检查清单**：原文未单独给（但总纲句本身就是清单）
- **现有 skill 是否已冻结**：**部分**。`stage2-design-tokens.md` 冻结了三层 token 技术（Primitive/Semantic/Component），`design-judgment/04-visual-hierarchy.md` 行 167 提到"主色用在哪 3 类（主按钮/状态/链接）— 不得超过"，但**没有任何文件冻结"中性灰托底 + 主色点睛 + 状态色守规矩 + 强色小面积 + 渐变要有理由"这条 5 点配色策略总纲**。
- **建议**：**新增到 `visual-language/README.md` 顶部新增"通用配色铁律"段**（在"4px 网格"之前），让所有风格文件共享。这是 AI 最容易翻车的"满屏 accent 滥用"根因。

---

## 盲点 2：整张卡片可点 vs 卡片内按钮可点 冲突规则未冻结【P0】

- **原文出处**：第三编第四章（一），行 608，原文摘抄：「还要想清楚：**整张卡片可点，还是卡片里的按钮可点？** 如果整张卡片可点，又在里面放一堆按钮，用户就会不知道点哪里触发什么。**卡片不能含糊，含糊就踩雷。**」
- **方法论**：
  - 卡片必须先定"是否整体可点"，二选一，不能含糊
  - 整张可点的卡片里，**不得**再放 primary/secondary 按钮（只能放 ghost icon 如 ⋯）
  - 内部有 primary 按钮的卡片，整张不可点（用 hover lift 暗示但不绑 onClick）
- **关键数据**：无具体数值，是规则
- **案例**：原文未举具体产品，但 Linear issue 列表行（整行可点 + 右侧 ghost 操作）是隐含正例
- **提示词模板**：原文未给
- **检查清单**：原文未给
- **现有 skill 是否已冻结**：**否**。`components/card.md` 行 42 冻结了 "interactive (clickable)" 变体（hover 加 shadow-md + cursor pointer），行 78 "header action: ghost icon button top-right (NOT primary)"——隐含触及但**没有明确写"整张可点 + 内部按钮"的冲突规则**。`components/table-row.md`（未读但 README 行 124 提到"action buttons appear on row hover, never primary in a list"）也只是部分触及。
- **建议**：**修订 `components/card.md`**，在 "Variants" 段后新增 "Click-target conflict rule" 小节，明确三种合法组合（整张可点 + 仅 ghost icon / 仅按钮可点 + 不可点容器 / 选中态 + 单一选中触发）。这是 AI 生成 dashboard 卡片网格时最常踩的雷。

---

## 盲点 3：Banner 组件缺失（持久性 inline message 容器）【P0】

- **原文出处**：第三编第四章（三），行 620，原文摘抄：「**保存成功，用 toast；权限不足，用 inline message 或 banner；删除危险，用确认弹窗**；列表为空，用空状态…加载较久，用骨架屏或进度提示稳住心。」
- **方法论**：
  - Banner = 持久性系统状态容器（区别于瞬时 toast）
  - 用于：权限不足、离线模式、只读模式、维护公告、强密码过期等
  - 通常置顶、不可自动消失、需要用户主动关闭或状态变更后消失
- **关键数据**：原文未给具体 spec
- **案例**：原文未举具体产品
- **提示词模板**：原文未给
- **检查清单**：原文未给
- **现有 skill 是否已冻结**：**否（组件文件缺失）**。`components/toast.md` 行 12 仅在分类表里提了一句"Banner (top of page): persistent system status (offline mode, read-only mode)"，但 components/ 目录**没有 banner.md**。`components/README.md` 行 67-79 的 Tier 2 清单里**也没有 banner**。
- **建议**：**新增 `components/banner.md`**，spec 参考 toast 但区分"持久 vs 瞬时"。AI 现在的处理是把权限不足/离线错误塞进 toast 自动消失——这正是原文反复点名的"反馈容器错位"病。

---

## 盲点 4：Superhuman "100ms 响应" 性能 SLA + 反面样板"功能堆成山" 未冻结【P1】

- **原文出处**：第 4 章，行 190–202，原文摘抄（Superhuman）：「它甚至有个出名的标准：**任何操作的响应都要在 100 毫秒以内**，慢了就算 bug。」；原文摘抄（反面样板）：「**功能多，不是优点，是包袱**…一个产品堆了三百个功能，用户只用得上三个…**做产品要敢于"伤其十指不如断其一指"**——把核心那几件事做到极致。」
- **方法论**：
  - 性能 SLA：100ms 内响应是"快"的硬指标（补充多尔蒂阈值 0.4s 的更严苛版本）
  - 产品哲学：功能多 ≠ 优点，敢做减法才是核心
  - 把核心 3 件事做到极致 > 把 100 件事都做得稀烂
- **关键数据**：100ms 阈值；"300 功能只用 3 个"
- **案例**：Superhuman（邮件客户端，红海杀出血路）；反面样板（"功能堆成山、用起来想骂娘"的产品）
- **提示词模板**：原文未给
- **检查清单**：原文未给
- **现有 skill 是否已冻结**：**否**。`references/case-studies.md` 只冻结了 Linear/Stripe/Apple/Notion 四家正例，**没有 Superhuman，没有反面样板**。`design-judgment/00-principles.md` 行 81 提到多尔蒂阈值 0.4s，但**没有 100ms 这条更严苛的性能 SLA**，也没有"功能多 = 包袱"的产品哲学。
- **建议**：**修订 `references/case-studies.md`**，新增 Superhuman 条目（rule = "speed as the product"）+ 反面样板条目（rule = "features are baggage unless ordered"）。这条强化"克制"原则的产品论据。

---

## 盲点 5：主按钮位置规则（右下 / 居中 / 跟随表单）未冻结【P1】

- **原文出处**：第三编第二章，原文 1–630 行**未直接给位置规则**（只讲了"一屏一个主帅"和按钮类型分工）。但实操中这是 AI 翻车高频点，且 `components/button.md` 的 Composes-with 段（行 122-128）隐含触及（drawer 保存按钮、modal 确认按钮、表单提交按钮）。
- **方法论**（从原文隐含规则 + 现有组件文件组合推断）：
  - Modal/Drawer：主按钮**右下角**，次按钮在其左侧（行序：cancel → primary）
  - 表单底部：主按钮**跟随表单右下**，与最后一个字段对齐
  - 全屏空状态：主按钮**居中**
  - 营销页 hero：主按钮**居中或左对齐跟随标题**
  - 列表/表格行内：**禁用主按钮**（只能 ghost/secondary/icon）
- **关键数据**：无
- **案例**：原文行 532 反例"页面右上角、列表顶部、空状态里都有一个蓝色主按钮，用户不知道哪个才是主入口"
- **提示词模板**：原文未给
- **检查清单**：原文未给
- **现有 skill 是否已冻结**：**部分**。`components/modal.md`、`drawer.md`（未读但 README 提到）应该有"footer 主按钮右下"，`components/empty-state.md` 行 50 "primary button, verb label, opens the creation flow" 隐含居中，`components/table-row.md` 提到 "never primary in a list"，但**没有任何文件把"主按钮位置规则"做成一张总览表**。
- **建议**：**修订 `components/button.md`**，新增 "Position rules by container" 小节（5 种容器 × 主按钮位置 × 反例）。这是 AI 容易"主按钮乱放"的根因。

---

## 盲点 6：行宽限制（中文 30-40 字、桌面正文 max-width）未冻结【P1】

- **原文出处**：第二编第二章（三），行 391，原文摘抄：「正文行宽也不能太长，**中文一行三四十字比较舒服**，一行拉到屏幕尽头，眼睛回行时容易迷路。」
- **方法论**：
  - 正文容器必须有 max-width，不能拉满屏宽
  - 中文 30–40 字/行；英文约 60–80 字符/行
  - 营销页 max-width 1200px、阅读型内容 max-width 680–768px、表单 max-width 480–640px
- **关键数据**：中文 30–40 字/行
- **案例**：原文未举具体产品
- **提示词模板**：原文未给
- **检查清单**：原文未给
- **现有 skill 是否已冻结**：**否**。`components/README.md` type scale 表只给了字号/行高，**没给行宽 max-width**。`references/qa-responsive.md` 行 60 提到 "modal 居中 max-width: 80vw" 但只针对 modal。`visual-language/style-stripe.md` 行 105 "page max-width: 1200px" 是营销页数值。但**没有任何文件冻结"中文 30-40 字/行"这条阅读型内容的行宽铁律**。
- **建议**：**修订 `components/README.md` 的 type scale 段**，在 weight 后新增 "measure (line length)" 行：阅读型 30-40 CJK 字 / 60-80 latin chars；同时**修订 `design-judgment/04-visual-hierarchy.md`** 在"留白"杠杆旁加一句"行宽也是留白的兄弟——拉满屏宽的正文 = 没有留白"。

---

## 盲点 7：对齐作为视觉层级第七杠杆（现有六杠杆漏了"对齐"）【P1】

- **原文出处**：第二编第三章（三），行 426–428，原文摘抄：「**对齐：横平竖直，是基本军容**…标题左边、输入框左边、按钮边界、卡片边界，都要落在同一套线上。对齐不是审美天赋，是较真。」+ 第二编第二章原话（行 358 引用 7.2）：「高手做层级，往往不是靠花哨颜色，而是靠**大小、字重、灰度、留白和对齐**。」
- **方法论**：
  - 对齐是基本军容，不对齐的界面"说不上哪里怪但显得不专业"
  - 所有元素边界（标题左/输入框左/按钮边界/卡片边界）必须落在同一套线上
  - 对齐是较真，不是审美天赋
- **关键数据**：无
- **案例**：原文未举具体产品（通用规则）
- **提示词模板**：原文未给
- **检查清单**：原文未给
- **现有 skill 是否已冻结**：**部分（漏一杠杆）**。`design-judgment/04-visual-hierarchy.md` 行 28-35 的六杠杆表是"大小/字重/颜色/位置/留白/分组"——**把"对齐"换成了"分组"**，且原文行 358 引用的 7.2 原话明确列了"对齐"，现有文件**没把对齐单列**。`components/README.md` 也没专门讲对齐。
- **建议**：**修订 `design-judgment/04-visual-hierarchy.md`**，把六杠杆改成七杠杆，新增"对齐"行（影响：建立军容；使用建议：所有边界落同一套线；AI 最常犯的错：标题/输入/按钮边界各偏几像素）。这是塑料感的重要来源。

---

## 盲点 8：表单"能自动就自动"原则（智能默认 / 邮编带城市 / 日期点选）未冻结【P1】

- **原文出处**：第三编第三章（三），行 583–585，原文摘抄：「**能自动就自动，能选择就别手打**。地址能根据邮编带出城市，就不要让用户重复填；日期能点选，就别要求手打格式；手机号能自动分段，就减少读错。**最好的表单，是没有表单；次好的表单，是只问非问不可的。**」
- **方法论**：
  - 表单设计的最高境界是消除表单（默认值、智能推断、单点登录）
  - 次好是只问非问不可的字段
  - 能自动填的不让用户手填（邮编→城市、IP→国家、URL→预览）
  - 能选择的不让用户手打（日期 picker、国家 selector、手机号分段）
- **关键数据**：无
- **案例**：原文未举具体产品（通用规则）
- **提示词模板**：原文未给
- **检查清单**：原文未给
- **现有 skill 是否已冻结**：**否**。`components/input.md` 冻结了 input 的 8 状态、focus ring、错误文案、校验时机，但**没有冻结"智能默认/自动填充/选择优于手打"这条表单减负原则**。`design-judgment/00-principles.md` 行 82 特斯勒定律只一句话"宁可让系统多担复杂（自动填、智能默认）"，但**没展开到表单设计**。
- **建议**：**修订 `components/input.md`**，在 Spec table 后新增 "Form reduction principle" 小节，列 5 条自动填充模式 + 3 条"选择优于手打"模式。这条是特斯勒定律在表单层的具体落地。

---

## 盲点 9：Tabs 组件 + 移动端 Bottom Tab 组件缺失【P1】

- **原文出处**：第三编第四章（二），行 612–614，原文摘抄：「**顶部栏、侧边栏、底部标签栏、面包屑**，不是随便选的装饰，而是不同产品结构的地图。Linear、Notion 这类生产力工具常用**侧边栏**…**移动 App 常用底部标签栏**，因为拇指可达、入口有限；复杂后台需要**面包屑**。」
- **方法论**：
  - 不同产品形态对应不同导航容器，不可混用
  - 桌面生产力 → sidebar（功能多、空间深、频繁切换）
  - 移动 App → bottom tab bar（拇指可达、入口 3-5 个为限）
  - 复杂后台 → breadcrumb（标识"我在组织/项目/任务/设置哪一层"）
- **关键数据**：底部标签栏入口 3-5 个
- **案例**：Linear、Notion（sidebar）；移动 App（bottom tab）；复杂后台（breadcrumb）
- **提示词模板**：原文未给
- **检查清单**：原文未给
- **现有 skill 是否已冻结**：**部分**。`components/nav-sidebar.md` 完整冻结了 sidebar + top bar + breadcrumb + ⌘K command palette。但：
  - **tabs.md 在 components/README.md 行 71 列在 Tier 2 待补**——还没建
  - **bottom-tab.md 完全没列**——移动端主导航组件缺失
- **建议**：**新增 `components/tabs.md`**（顶部/段控式 tabs，桌面端次级导航）+ **新增 `components/bottom-tab.md`**（移动端主导航，3-5 入口、icon + label、激活态 primary tint）。后者尤其重要，因为 AI 生成移动端 App 时容易直接套桌面 sidebar。

---

## 盲点 10：标签对齐三种取舍（顶 / 左 / 内联）未冻结【P2】

- **原文出处**：第三编第三章（一），行 575–577，原文摘抄：「**标签应该始终可见**。输入框内的提示可以作为辅助，但不能代替标签。尤其是长表单、金融表单、医疗表单、后台配置表单，用户必须随时知道自己在填什么。」
- **方法论**：
  - 顶对齐（label 在 input 上方）：默认推荐，扫描速度快，移动端必需
  - 左对齐（label 在 input 左侧）：桌面端长表单、字段名长时用，但扫描速度慢
  - 内联/浮动（label 在 input 内）：空间紧时用，但有"输入后消失"风险，必须有常驻备选
  - 长表单/金融/医疗/后台配置 → 标签必须始终可见（顶对齐或左对齐）
- **关键数据**：原文未给具体扫描速度数据
- **案例**：原文未举具体产品
- **提示词模板**：原文未给
- **检查清单**：原文未给
- **现有 skill 是否已冻结**：**部分**。`components/input.md` 行 21 冻结了顶对齐默认（"14px / 500, above input, 6px gap, always visible (no floating label unless space-constrained)"）——但**没有讲三种对齐的取舍**。
- **建议**：**修订 `components/input.md`**，在 label spec 行旁新增"Label alignment decision matrix"小表（顶/左/浮动 三种 × 各自适合场景 × 反例）。这是 P2 因为现有已默认顶对齐、AI 不太会错得太离谱。

---

## 盲点 11：可用性测试方法论"3 个新用户 5 秒看页面目的"具体操作未冻结【P2】

- **原文出处**：第一章，行 52，原文摘抄：「**目标清晰**｜"这是干什么的？"｜…｜**找 3 个新用户看 5 秒，说不出页面目的就重做**」
- **方法论**：
  - 5 秒测试：找 3 个新用户，给他们看页面 5 秒，让他们说出页面目的
  - 说不出 = 目标不清晰，重做
  - 这是"目标清晰"指标的可执行验收方法
- **关键数据**：3 个新用户、5 秒
- **案例**：原文未举具体测试案例
- **提示词模板**：原文未给（但行 110-123 的 5 指标审稿提示词是 AI 替代版）
- **检查清单**：原文未给
- **现有 skill 是否已冻结**：**部分**。`design-judgment/00-principles.md` 行 22 在 5 指标表里逐字复制了"找 3 个新用户看 5 秒"，行 123 判断卡自评表也有"用户 5 秒能说出页面目的吗？"——但**没有给 AI 怎么模拟这个测试**（用 GLM/GPT 扮演新用户审稿的提示词）。考虑到 AI 不做真人测试，这条作为**操作方法**确实较难冻结。
- **建议**：**P2 暂不新增**，理由：(1) 原文这条已逐字复制到 `00-principles.md`；(2) AI 工作流里替代品是"用 LLM 模拟新用户审稿"，这已在行 33-48 的 5 指标提示词中部分覆盖；(3) 真正的真人可用性测试不是 AI skill 的能力范围。如果未来要做"AI 模拟用户测试"功能，可新建 `references/ai-usability-test.md`。

---

## 盲点 12：字重梯度（原文说 600/700，现有只到 600）【P2】

- **原文出处**：第二编第二章（三），行 393，原文摘抄：「**字重是高手拉层级的暗器**。标题用 **600/700**，正文用 400，辅助说明用浅灰和常规字重。」
- **方法论**：
  - 标题字重 600 或 700（两档可选）
  - 正文 400
  - 辅助说明用浅灰 + 400（不靠字重，靠颜色）
- **关键数据**：标题 600/700
- **案例**：原文未举具体产品
- **提示词模板**：原文未给
- **检查清单**：原文未给
- **现有 skill 是否已冻结**：**部分**。`components/README.md` 行 124-127 weight 表只列 regular 400 / medium 500 / semibold 600——**没有 700 (bold)**。`design-judgment/04-visual-hierarchy.md` 行 92 权重 5 (第一眼) 写"字重 600-700"，已含 700。差异主要在 components/README.md 的 token 表。
- **建议**：**P2 修订 `components/README.md` weight 段**，补 `weight.bold = 700` 一行。理由：(1) 营销页大标题常用 700（Stripe 除外，Stripe 用 300）；(2) 现有 4-visual-hierarchy 已用 600-700，但 token 表缺 700 会让 AI 生成时只敢到 600。

---

## 已冻结且充分的（简列，证明对照过）

- **好设计五指标** → `design-judgment/00-principles.md` 行 18-31 完整冻结（含表格 + 验收方法 + 提示词逐字复制 + 自评卡）✓
- **5 指标提示词模板**（原文行 110-123）→ `00-principles.md` 行 33-48 逐字复制 ✓
- **四条根本原则**（层级/克制/一致/反馈）→ `00-principles.md` 行 52-63 完整冻结（含统帅原则 + 三样板口诀）✓
- **六大老规律**（菲茨/希克/米勒/雅各布/多尔蒂/特斯勒）→ `00-principles.md` 行 73-88 完整冻结（含雅各布特别强调 + 判断卡可勾选项）✓
- **两种病**（形式主义/教条主义）→ `00-principles.md` 行 92-99 完整冻结 ✓
- **实践-认识-再实践循环**（做→测→看卡壳→改）→ `00-principles.md` 行 103-113 冻结（含两句关键金句）✓
- **三块样板口诀**（Linear 减法 / Stripe 抠细节 / Apple 立规矩）→ `00-principles.md` 行 65-69 + `references/case-studies.md` 行 11-67 用 Five-Layer Blade 解剖 ✓
- **Notion "积木哲学"** → `case-studies.md` 行 55-67 完整冻结 ✓
- **视觉层级六杠杆**（大小/字重/颜色/位置/留白/分组）→ `design-judgment/04-visual-hierarchy.md` 行 28-35 完整冻结 ✓ [注：原文 7.2 原话还包括"对齐"，见盲点 7]
- **5-3-2 视觉权重法则** → `04-visual-hierarchy.md` 行 86-102 完整冻结 ✓
- **颜色三层 token**（Primitive/Semantic/Component）→ `references/stage2-design-tokens.md` 行 12-176 完整冻结（三层 + 每层完整列表）✓
- **WCAG 对比度**（正文 4.5:1 / 大字 3:1 / AAA 7:1）→ `references/qa-a11y.md` 行 9-26 + `stage2-design-tokens.md` 行 202-207 双重冻结 ✓
- **深色模式色温调整**（深灰不是纯黑、off-white 不是纯白、主色降饱和、表面越上越亮）→ `stage2-design-tokens.md` 行 182-200 完整冻结（DARK MODE semantic overrides）✓
- **8 点网格 / 4 倍数 spacing scale** → `components/README.md` 行 81-90 + `visual-language/README.md` 行 48-57 + `stage2-design-tokens.md` 行 211 三重冻结 ✓
- **亲密性原则**（关系近靠近、关系远拉开）→ `04-visual-hierarchy.md` 分组杠杆 + `stage2-design-tokens.md` space.layout 双重冻结 ✓
- **字阶 staircase**（12/14/16/18-20/24/30-32）→ `components/README.md` 行 113-127 type scale 完整冻结 ✓
- **行高规则**（标题紧 1.1-1.3、正文松 1.5）→ `components/README.md` type scale 表里每档都冻结 line-height ✓
- **字重梯度** → `components/README.md` 行 124-127（400/500/600，缺 700，见盲点 12）
- **阴影分级**（sm/md/lg/xl）→ `stage2-design-tokens.md` 行 64-68 + 每个 `visual-language/style-*.md` 第 4 节 ✓
- **圆角分级**（4/6/8/12/full）→ `components/README.md` 行 94-101 radius scale 完整冻结 ✓
- **图标出自一家**（绑定单一图标库，禁混用）→ `visual-language/icon-systems.md` + 每个 style 文件第 7 节 ✓
- **响应式断点 + 移动优先** → `references/qa-responsive.md` 行 11-20 完整冻结（Tailwind v4 6 档 + 移动优先写法）✓
- **按钮 8 状态**（默认/悬停/按下/聚焦/禁用/加载/成功/失败）→ `components/button.md` 行 28-38 完整冻结（含每状态的 visual/copy/behavior）✓
- **"一屏一个主帅"按钮规则** → `components/button.md` 行 25 + 行 80 + 失败模式行 134 完整冻结 ✓
- **按钮触控目标 44/48 px** → `components/button.md` 行 23 完整冻结 ✓
- **表单标签常驻**（不用 placeholder 当标签）→ `components/input.md` 行 21 + 行 71 + 失败模式行 159 三重冻结 ✓
- **错误就地具体可修**（不堆顶部 toast、说人话）→ `components/input.md` 行 18 + 行 66-68 + `toast.md` 行 14 双重冻结 ✓
- **校验时机**（失焦校验、出错后实时重校）→ `components/input.md` 行 62-64 完整冻结 ✓
- **失败保内容**（draft must survive）→ `input.md` 行 71 + `button.md` error 状态 + `empty-state.md` 错误空状态"filters preserved" 三重冻结 ✓
- **空状态三分**（initial / no-results / error）→ `components/empty-state.md` 行 5-13 + 行 30-128 完整冻结（三种状态各自的 title/desc/CTA + 反例）✓
- **反馈容器分类**（toast/inline/modal/banner 各司其职）→ `components/toast.md` 行 7-14 完整冻结（除 banner 组件文件缺失，见盲点 3）✓
- **导航三问**（我在哪/能去哪/怎么回）→ `components/nav-sidebar.md` 完整冻结（breadcrumb + sidebar active + ⌘K）✓

---

## 前 3 个最值得补的盲点（按 ROI 排序）

1. **【P0 盲点 1】配色策略总纲**——补到 `visual-language/README.md` 顶部。**理由**：这是 AI"满屏 accent 滥用 / 五颜六色彩虹页"的根因，原文 5 点章法（中性灰托底 + 主色点睛 + 状态色守规矩 + 强色小面积 + 渐变要有理由）一句话就能冻结进所有风格文件的共享公约段，影响所有产物。
2. **【P0 盲点 3】Banner 组件**——新增 `components/banner.md`。**理由**：权限不足、离线模式、只读模式、维护公告是产品级常见状态，但 skill 现在只有 toast（瞬时）没有 banner（持久），AI 会把所有持久状态塞进 toast 自动消失——这是原文行 620 直接点名的反馈容器错位病。
3. **【P0 盲点 2】整张卡片可点 vs 内部按钮可点 冲突规则**——修订 `components/card.md`。**理由**：AI 生成 dashboard / 列表卡片网格时最常出"整张可点 + 里面又三个按钮"的混乱，原文行 608 直接讲"含糊就踩雷"，是一条可立即冻结的硬规则。

> 补完这 3 个 P0，第 1-3 编的"影响 AI 产物塑料味"的核心盲点就清零了。P1 的 6 个建议在下一次精读循环里补（Superhuman 性能 SLA、主按钮位置、行宽限制、对齐杠杆、表单自动填充、Tabs/BottomTab 组件），P2 的 3 个可以最后批处理。
