# Stage 1 — Intent Routing (one-line idea → Task Card → five-layer slice)

> The entry point. A user gives a one-line idea; this file is how you route it into a Task Card and a five-layer slice plan, without skipping straight to a plastic UI.

## The routing pipeline

```text
one-line idea
     ↓
intent classification (what kind of product UI?)
     ↓
Task Card extraction (force the user to fill the gaps)
     ↓
five-layer slice plan (which drafts, which layers)
     ↓
Stage 1 generation
```

## Step 1 — classify the intent

Read the one-line idea and classify what kind of product UI it is. The classification tunes the Task Card questions and the default draft mix.

| Intent type | Signal words | Default draft mix |
| --- | --- | --- |
| **CRUD list-detail** | "管理 / 列表 / 任务 / 后台 / 数据" | heavy on object-state-permission + state-matrix + 3-5 IA variants |
| **Form / wizard** | "表单 / 创建 / 注册 / 报名 / 多步" | heavy on task-flow + state-matrix (validation errors) + container choice |
| **Dashboard / analytics** | "仪表盘 / 数据 / 报表 / 监控" | heavy on system (chart tokens) + state-matrix (loading / empty / error) + IA (density) |
| **Settings / config** | "设置 / 配置 / 偏好 / 权限" | heavy on object-state-permission (roles) + system (pattern library) |
| **Editor / canvas** | "编辑器 / 画布 / 文档 / 设计" | heavy on task-flow + container (immersive page) + system (toolbar patterns) |
| **Marketing / landing** | "落地页 / 首页 / 介绍 / 营销" | **route to cover-pop** — this skill is for usable product UI, not marketing |

If the intent is marketing/landing with no states/objects/permissions, push the user to `cover-pop` or `master-styles`. This skill refuses to generate one-shot pretty pages.

## Step 2 — Task Card extraction

The user's one-line idea is almost always too thin. Don't generate from it. Use the classification to ask the right follow-up questions (see `stage1-task-card.md` for the question order).

**Thin input handling:**

| Input thickness | What to do |
| --- | --- |
| One word ("任务管理") | ask all 6 Task Card questions one by one |
| One sentence ("团队用的任务管理 App") | ask 3 (non-goals, states-that-break, objects) — infer the rest |
| A paragraph (real spec) | mine it for the fields, confirm the gaps |
| A reference product ("like Linear but for X") | extract the JUDGMENT (restraint, keyboard-first), not the pixels; then fill the Task Card from the user's actual task |

**Reference-product trap:** when a user says "like Linear / Stripe / Notion", they almost always mean the JUDGMENT (Linear's restraint, Stripe's detail, Notion's blocks) — not the actual UI. Don't copy pixels; extract the rule (see `case-studies.md`).

## Step 3 — five-layer slice plan

From the Task Card, decide which drafts to generate. The plan must answer:

```text
slice plan:
  intent type: [CRUD list-detail / form / dashboard / settings / editor]
  must-have drafts:
    A3 object-state-permission: [object name] — mandatory
    A?: [task-flow / state-matrix / system — pick at least 1]
  structure drafts (3-5):
    B1 sidebar+list+drawer — [task reason]
    B2 kanban — [task reason]
    B?: ...
  layer coverage:
    ① Task: covered by [draft name]
    ② Structure: covered by [draft names]
    ③ State: covered by [draft names]
    ④ System: covered by [draft name]
    ⑤ Tradeoff: covered by [every draft's tradeoff note]
```

Every layer must have at least one draft. If layer ④ (System) has no draft and the product is a real product (not a one-shot), add a system draft. If layer ① (Task) is thin, the task-flow draft carries it.

## Step 4 — generate Stage 1

Hand the slice plan to the Stage-1 generation loop. Emit drafts in this order:

1. **Task Card** (force user confirmation before generating more)
2. **A3 object-state-permission** (the skeleton — do this early, it changes everything)
3. Other A drafts
4. B drafts (structure variants)
5. **Mosaic view** (which combine, which are either/or)
6. **Recommendation** (which combination, why)

## Common routing failures

| Failure | Symptom | Fix |
| --- | --- | --- |
| Skipped Task Card | went straight to drafts from one-line idea | gate: no Task Card, no drafts |
| Marketing request | "make me a beautiful landing page" | route to cover-pop |
| Copy-the-pixels | "make it look exactly like Linear" | extract the judgment, fill Task Card from user's task |
| Missing A3 | drafts generated, no object-state-permission | mandatory — add it before any B draft |
| All layers ≠ covered | 8 drafts, all structure, zero state/system | slice plan gate: every layer needs ≥1 draft |
