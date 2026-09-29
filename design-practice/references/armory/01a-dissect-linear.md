---
type: armory-dissect
created: 2026-06-27
source: 原文行 2353-2383（第十一编 二 拆 Linear）+ armory/01-tokens-linear.md
priority: P0
---

# Linear 五层刀法完整拆解

> 出处:原文行 2353-2383。`armory/01-tokens-linear.md` 只拆了 ④System 层（color/space/radius/font/component token），本文件拆 ①Task ②Structure ③State ⑤Tradeoff 四层。两者配合,才是"拆 Linear 拆到骨头"。
>
> 用法:用户说"Linear 风"→ armory/01 给 tokens（④System 层）;用户说"拆 Linear 给我看"→ 本文件给五层完整拆解。

## ① Task 层 — Linear 把哪条主流程做顺了

**核心用户**:每天处理 issue、项目、冲刺、优先级的软件团队。
**核心任务**:高速处理任务——看、搜、筛、改、分配、关闭、跳转。
**Linear 把"高速处理"做顺的具体表现**:

| 观察 | 为什么这样设计 |
|---|---|
| 列表密度高（issue 标题、状态、优先级、负责人、项目归属在一行内扫读） | 老用户一屏看 20+ 条 issue,不浪费时间在滚动上 |
| 快捷键全覆盖（C 创建、/ 搜索、G+X 跳转、⌘K 命令面板） | 老用户要速度,鼠标是减速器 |
| 命令面板 ⌘K 是主入口 | 任何动作都能从 ⌘K 起手,不需要找按钮在哪 |
| 创建 issue 用 inline 快速输入,不开模态 | 创建是高频,模态打断流;inline 创建保持上下文 |
| 跳转用 ⌘K 不用面包屑 | 跳转是高频,键盘比鼠标快 |

**反塑料锚点**:Linear 的"高级感"不是来自暗色,而是来自**不打扰**——老用户用 8 小时不放烟花,它是一把锋利的刀,不是装饰品。

## ② Structure 层 — Linear 的信息为什么这样安排

| 观察 | 为什么这样安排 |
|---|---|
| 三栏布局:左 sidebar（workspace/项目/视图）+ 中列表（issue 表）+ 右详情（点开抽屉/二级） | 三栏是任务处理的"工作台"结构:导航在左、列表在中、详情在右,不切换上下文 |
| sidebar 默认收起低频项（团队设置、回收站） | 高频在顶（Inbox/My Issues/Views）,低频进折叠 |
| issue 详情不开新页,用右侧抽屉/二级面板 | 保持列表上下文,关闭抽屉列表还在原位（**坐标感 5 件套的关键:列表滚动位置保留**） |
| 分割线弱（1px 弱边框,只在 surface 间出现） | 任务内容是主角,边框不能抢话 |
| 列表项 hover 才显示操作（编辑/分配/状态切换） | 默认安静,hover 时给高频用户他要的工具 |

**反塑料锚点**:Linear 的"克制"不是没东西,而是**让该出现的时刻才出现**——hover 操作、收起的低频项、列表/详情不切换上下文。

## ③ State 层 — Linear 出事时怎么稳住用户

| 状态 | Linear 怎么做 |
|---|---|
| loading | 列表骨架（行骨架匹配行结构,不是 spinner）;详情抽屉骨架（标题/属性/描述三块骨架） |
| empty（initial） | "没有 issue。创建第一个 issue。" + inline 输入框,不开模态 |
| empty（filter） | "当前筛选下没有 issue。" + 显示当前筛选 chip + 清除按钮 |
| empty（permission） | viewer 看不到 draft 状态的 issue,看不到就是看不到,不弹权限错误 |
| error（网络） | "网络异常,刚才的操作没生效,可以重试" + 重试按钮,**输入内容保留** |
| error（权限） | Create 按钮 disabled + tooltip "You need editor role"——而不是点了才 403 |
| 重复提交保护 | 提交时按钮进入 loading + disabled,不可重复点 |
| 离线 | 顶部 banner "当前离线,你的修改会暂存,联网后同步"——持续显示 |

**反塑料锚点**:Linear 的"状态安静但明确"——任务状态（todo/progress/done/cancelled）、优先级（urgent/high/medium/low）、负责人（avatar）、项目归属（chip）都能在一行内扫读,但互相不吵架。

## ④ System 层 — 见 armory/01-tokens-linear.md

完整的 color/space/radius/font/component token 在 `armory/01-tokens-linear.md`。本层不重复。

## ⑤ Tradeoff 层 — Linear 敢砍什么

| Linear 砍了什么 | 为什么敢砍 |
|---|---|
| 砍甘特图（基础版没有,高级版才有） | 主任务（高速处理）不需要甘特,甘特是项目管理低频工具 |
| 砍日历视图（默认没有） | 同上,日历是另一种工作流,不是 Linear 的主任务 |
| 砍时间追踪（基础版没有） | 时间追踪是另一类工具（Toggl）,Linear 不抢 |
| 砉 AI 摘要（早期没有,后期才加） | 主任务是处理,不是阅读;AI 摘要是辅助,不是核心 |
| 砍多余的颜色（只有主色 + 状态色,没有装饰色） | 状态色要"说话",装饰色会"抢话",所以不要装饰色 |
| 砍重型模态（创建用 inline 不用模态） | 模态打断流,创建是高频,所以 inline |

**反塑料锚点**:学 Linear 最容易学歪的就是"什么都加"——以为加更多功能更接近 Linear。原文行 2371:**"你如果只抄它的暗色,却把所有功能都摊在页面上,那不是 Linear 风格,是穿着 Linear 外套的功能集市。"**

## 给生成阶段的提示词片段

```text
Linear 风生成要求（除了 token,还要满足以下五层判断）:

① Task 层:
- 用户来高速处理任务,不是欣赏界面
- 列表密度优先,一屏扫读 ≥20 条
- 快捷键全覆盖,⌘K 是主入口
- 创建用 inline 不用模态（高频动作不开模态）

② Structure 层:
- 三栏（左导航 + 中列表 + 右详情抽屉）
- 详情不开新页,用抽屉保持列表上下文
- **关闭抽屉后,列表滚动位置必须保留**（反塑料锚点）
- 分割线弱,1px 弱边框只在 surface 间

③ State 层:
- 8 态按钮 + 5 态数据模块全过
- 权限错误:Create disabled + tooltip,不点才知道
- 网络错误:重试按钮 + 输入保留
- 离线:顶部 banner 持续显示

④ System 层:
- 见 armory/01-tokens-linear.md 全套 token

⑤ Tradeoff 层:
- 这一轮不做甘特/日历/时间追踪/AI 摘要（除非用户明确要）
- 砍装饰色,只留主色 + 状态色
- 创建用 inline,详情用抽屉,不用模态
```
