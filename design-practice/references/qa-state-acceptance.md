# 6 类组件状态验收表 — State Acceptance

> AI 生成 UI 第二常见失败模式:**默认态做得漂亮,其他状态全塌**。用户点不动、加载数据时白屏、出错时一行红字、空状态一个 div——这些都是塑料信号。
>
> 这一页冻结:每个核心组件类型的**必验状态清单**、**事故场景**、**修复动作**。生成完每一类组件,都要过这张表。

## 错误态三件事(铁律)

> 在进 6 类验收之前,先冻结错误态的硬规矩——**任何错误状态都必须传达三件事**:
>
> 1. **WHAT** — 发生了什么(用用户听得懂的话,不是 stack trace)
> 2. **WHY** — 为什么发生(可选,但如果知道就告诉用户)
> 3. **HOW** — 怎么办(重试 / 联系支持 / 修改输入 / 重新登录)
>
> 任何错误状态少了这三条中任何一条,就是失败的。

错误状态的好与坏:

| 坏 | 好 |
|---|---|
| "出错了" | "无法保存修改——网络连接中断。请检查网络后重试。" |
| "Error 500" | "服务器暂时无法响应。我们的团队已收到通知。30 秒后自动重试,或[手动重试]。" |
| "无效输入" | "邮箱格式不正确——应该是 name@example.com 的形式。" |
| 红边框(无文字)| 输入框红边框 + 下方红色文字"必填,不能为空"+ 图标提示 |

## 6 类组件 × 必验状态表

### 1. 按钮 Button

| 状态 | 必验 | 事故场景 | 动作 |
|---|---|---|---|
| default | 视觉清晰,层级正确 | - | 套 `button.md` 规范 |
| hover | 背景变化 + cursor pointer | 移动端没有 hover(要确认不依赖 hover 透露信息) | 检查移动端是否用 active 替代 |
| active/pressed | scale 0.97-0.98 + 颜色加深 | 没有按下手感 | 加 transform: scale(0.98) |
| focus-visible | 双层 box-shadow ring(2px+4px)| 单层 outline 或无 ring | 套 `style-linear.md` shadow.focus |
| disabled | 灰色 + cursor not-allowed + opacity 0.5 | 用户点了没反应以为坏了 | 加 tooltip 解释为什么 disabled |
| loading | spinner + 文字变"处理中..." + 按钮禁用 | 提交后没反馈,用户连点多次 | 加 loading state 防双击 |
| error | 红色边框/背景 + 错误 icon | 失败后没视觉反馈 | 加 shake 动画或红色 flash |
| success(短暂)| 绿色对勾闪过(可选)| - | 仅在确认型按钮 |

### 2. 输入框 Input

| 状态 | 必验 | 事故场景 | 动作 |
|---|---|---|---|
| default | placeholder + label 清晰 | 没有 label 只有 placeholder | 必须有 label,placeholder 是提示不是替代 |
| focus | border accent + 双层 ring + cursor text | 单层 outline | 套 `input.md` 双层 focus ring |
| filled | 内容显示完整,不截断 | 长内容被截断 | 加 title 属性显示完整 |
| error | 红色 border + 下方红色文字 + icon | 只有红边框没文字 | 三件事:WHAT(红了)+ WHY(文字)+ HOW(怎么改)|
| disabled | 灰色背景 + not-allowed | 看不出为什么 disabled | 加 tooltip 解释 |
| required | label 后加 * 红色 | 没标识 required | label 后加 `<span class="text-danger">*</span>` |
| password | 显示/隐藏切换按钮 | 没切换按钮 | 右侧加 eye/eye-off icon button |

### 3. 表格 Table

| 状态 | 必验 | 事故场景 | 动作 |
|---|---|---|---|
| empty | "暂无数据"插画 + 解释 + 创建 CTA | 一个空 div 或 "No data" | 套 `empty-state.md` initial 分类 |
| loading | skeleton 行(不是 spinner)| 全屏 spinner 阻塞 | 用 skeleton 行占位,保持结构稳定 |
| error | 表格区域显示错误态 + retry | 表格空白无解释 | 错误三件事 |
| sorting | 表头可点击 + 当前排序列箭头 | 看不出哪列在排序 | 表头加 ↑↓ icon + active 列高亮 |
| pagination | 上一页/下一页 + 页码 + 每页条数 | 只有上一页/下一页 | 加页码 + 跳转 + 每页条数选择 |
| row hover | 行背景变化 + 行操作 icon 出现 | 行操作始终显示太乱 | 行操作默认隐藏,hover 时淡入 |
| row selected | checkbox + 行背景 accent | 看不出哪些行被选 | checkbox + 行背景变 accent light |
| row density | 紧凑/标准/宽松切换 | 固定一种密度 | 套 `table-row.md` 三档高度 |
| sticky header | 滚动时表头吸顶 | 表头跟着滚走 | position: sticky; top: 0 |

### 4. 抽屉 Drawer

| 状态 | 必验 | 事故场景 | 动作 |
|---|---|---|---|
| closed | 默认不可见 | - | - |
| opening | 从右滑入 200-300ms ease-out | 瞬间出现无动画 | transform: translateX(100%) → 0 |
| open | 内容完整 + 关闭按钮 + ESC 关闭 + 点遮罩关闭 | 关闭方式不全 | 三种关闭方式都要支持 |
| **dirty(关键)** | 用户改了未保存 → 关闭前确认 | 改完直接关闭丢数据 | 关闭前弹确认 modal:"你有未保存的修改,确定丢弃?" |
| submitting | 保存按钮 loading + 整个 drawer 不能交互 | 保存时用户还能改其他字段 | drawer 加 pointer-events: none + opacity 0.7 |
| error | 错误提示在 drawer 顶部 + 不关闭 drawer | 错误时 drawer 关了用户看不到 | 错误留在 drawer 内,不关闭 |
| focus trap | Tab 在 drawer 内循环 | Tab 跑到背景 | 套 focus trap 逻辑 |

### 5. Toast 通知

| 状态 | 必验 | 事故场景 | 动作 |
|---|---|---|---|
| success | 绿色 + 对勾 + 简短文字 | 太长太啰嗦 | 一句话 + 可选详情链接 |
| error | 红色 + X + 三件事文字 | 只说"出错了" | 三件事:WHAT + WHY + HOW |
| warning | 黄色 + ! + 简短文字 | 与 error 混淆 | warning 是可继续,error 是阻塞 |
| info | 蓝色 + i + 中性信息 | 滥用 spam | 仅重要信息才 toast |
| loading | spinner + "处理中..." | 任务完前自动消失 | loading toast 不能 auto-dismiss |
| auto-dismiss | 4-6 秒后自动消失 | 太短用户没读完 | error toast 不 auto-dismiss,要手动关 |
| hover pause | hover 时暂停计时 | 用户没读完就消失了 | mouseenter 暂停,mouseleave 继续 |
| action button | 右侧可点击 action("撤销") | action 没有焦点环 | 套 `button.md` focus-visible 规则 |
| stacking | 多个 toast 垂直堆叠,新在下 | 互相覆盖 | flex column + gap 8px |
| aria-live | 屏幕阅读器播报 | 无障碍缺失 | aria-live="polite"(info/success),"assertive"(error)|

### 6. 空状态 Empty State

| 状态 | 必验 | 事故场景 | 动作 |
|---|---|---|---|
| initial | 用户第一次来,没数据 | 显示"No items" | 插画 + "创建你的第一个 X" + CTA |
| no-results | 搜索/筛选后无结果 | 显示"No items" | 插画 + "没有匹配的 X" + 清除筛选 CTA |
| error | 加载失败 | 显示"No items" | 插画 + 错误三件事 + retry CTA |
| permission | 没权限看 | 显示"No items"(误导)| 解释需要什么角色 + 联系管理员 |
| offline | 网络断 | 显示"No items" | 网络断提示 + retry |
| partial | 部分数据加载失败 | 整个区域空白 | 显示已加载部分 + 失败部分 retry |

## 状态验收清单(每条打勾)

```text
页面 / 组件:_____________

按钮(每个 primary button):
□ 8 状态全(default/hover/pressed/focus/disabled/loading/error/success)
□ pressed scale 0.98
□ focus 双层 box-shadow
□ disabled 有 tooltip 解释

输入框(每个 input):
□ 7 状态全(default/focus/filled/error/disabled/required/password)
□ 错误三件事(红边框 + 文字 + icon)
□ password 有显示切换
□ label 不是 placeholder

表格(每个 table):
□ 9 状态全(empty/loading/error/sorting/pagination/hover/selected/density/sticky)
□ empty 是插画不是 "No data"
□ loading 是 skeleton 不是 spinner
□ sticky header 吸顶

抽屉(每个 drawer):
□ 7 状态全(closed/opening/open/dirty/submitting/error/focus-trap)
□ dirty 关闭前确认(关键!)
□ focus trap 限制 Tab

Toast(每个 toast 类型):
□ 6 变体全(success/error/warning/info/loading/action)
□ error 不 auto-dismiss
□ hover 暂停计时
□ action button 有 focus ring
□ aria-live 设置

空状态(每个 empty 区):
□ 三分类(initial/no-results/error)区分清楚
□ 每类有插画 + 文字 + CTA
□ permission 和 offline 不显示成"空"
```

## AI 验收员提示词

```text
你是一个严格的 UI 状态验收员。审查下面这个组件的所有状态。

组件:[提供截图或 URL]

预期状态:
- 按钮:8 状态(default/hover/pressed/focus/disabled/loading/error/success)
- 输入框:7 状态(default/focus/filled/error/disabled/required/password)
- 表格:9 状态(empty/loading/error/sorting/pagination/hover/selected/density/sticky)
- 抽屉:7 状态(closed/opening/open/dirty/submitting/error/focus-trap)
- Toast:6 变体(success/error/warning/info/loading/action)
- 空状态:3 分类(initial/no-results/error)+ permission/offline 区分

对每个状态:
1. 是否实现?(是/否/N/A)
2. 如果实现,是否正确?(视觉/交互/文案)
3. 如果缺失,有什么事故场景?

特别检查:
- pressed scale 是否 0.97-0.98(不是 1,不是 0.95)?
- focus ring 是否双层 box-shadow(不是单层 outline)?
- error toast 是否不 auto-dismiss?
- drawer dirty state 是否关闭前确认?
- empty 状态是否区分 initial/no-results/error 三类?

输出:每条状态打勾或打叉,失败的给具体修复建议。
```

## 与 SKILL.md 的关系

SKILL.md 的 "Three-Gate QA" 的 Engineering Gate 必须包含这一页的状态验收。任何组件实现完,都要跑这张表。

## 与其他 QA 文档的关系

- **页面五问** `qa-page-five-questions.md`:页面级总验收
- **状态验收**(本页):组件级状态验收
- **a11y** `qa-a11y.md`:无障碍验收
- **响应式** `qa-responsive.md`:多端验收
- **坏数据** `qa-bad-data.md`:边界数据验收
