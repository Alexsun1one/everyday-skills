# Workflow Layer(原文权威工作流层)

> 出处:《设计的实践》第 10 编 + 第 12 编
> 定位:Agent 执行流程的**权威版本**,替代任何 agent 自己拼凑的流程。
>
> **为什么单独抽出来**:`references/agent-playbook.md` 是我之前自己写的 11 步流程,**作者原文其实有更权威、更精炼的"10 步工作流"(第 10 编)和"8 步项目实战"(第 12 编)**。这两个工作流是作者从大量项目里提炼的,经过原文反复打磨,应该作为 Agent 执行的源头。这一层把原文工作流逐字冻结。

## 文件索引

| 顺序 | 文件 | 出处 | 一句话 |
|---|---|---|---|
| 1 | `01-ten-step-flow.md` | 第 10 编 | 想法 → 上线的 10 步(压缩全书) |
| 2 | `02-design-task-brief.md` | 第 10 编 | 设计任务单模板(替代 stage1-task-card) |
| 3 | `03-ai-collaboration-roles.md` | 第 10 编 | AI 协作三角色(调研员/草图员/执行员) |
| 4 | `04-p0p1p2-review.md` | 第 10 编 | P0/P1/P2 评审分级严格定义 |
| 5 | `05-eight-step-project.md` | 第 12 编 | 完整项目实战 8 步(任务管理 SaaS 案例) |

## 使用纪律

1. **`01-ten-step-flow.md` 是总流程** — Agent 执行任何任务都按这 10 步走。
2. **`05-eight-step-project.md` 是 10 步在具体项目里的展开** — 做复杂产品时按这 8 步走。
3. **`02/03/04` 是 10 步里关键节点的细节模板** — 第 2 步用 02,第 7 步用 03,第 9 步用 04。

## 与 agent-playbook 的关系

`references/agent-playbook.md` 是**简版执行手册**(给 Agent 看的速查)。
`workflow/` 是**完整版权威流程**(给设计判断用的)。
两者不冲突,Agent 先读 playbook 建立框架,具体节点深入到 workflow/。
