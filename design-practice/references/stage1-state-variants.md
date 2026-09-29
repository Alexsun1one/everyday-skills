# Stage 1 — State Variants (every draft carries them)

> No draft ships with only a default state. State variants are mandatory on every Stage-1 draft. This file is the spec.

## Why

Article line 714: **"好设计不是静态截图好看,而是用户从'准备做'到'做完了'的整条路径都可靠. 评价一个页面,不要只看默认态;一定要看加载、失败、空状态、权限不足、重复点击、离线、撤销这些'出事的时候'."**

A draft with only a default state is the definition of skin-without-skeleton. The state variants ARE the skeleton.

## The minimum (every draft)

Every Stage-1 draft carries at least:

- **loading** — what shows while data fetches (skeleton, not spinner — article line 1811: "用骨架屏,不要只画转圈")
- **empty** — the three classifications (see below), at minimum the one that fits this draft
- **error** — what shows when it breaks, in-place, with retry, preserving user input

For the **state-matrix draft (A2)**, the full set: loading + empty(3) + error + permission + offline.

## Empty-state three-classification (article line 11681-11709)

This is the single most-abused state. "暂无数据" is the four-word tell of an AI-generated UI. Always classify:

| Kind | Trigger | Wording formula | Action |
| --- | --- | --- | --- |
| **initial-empty** | user hasn't created anything yet | value + reason + first step | primary CTA: "Create your first [object]" |
| **filter-empty** | data exists but current filter has no match | acknowledge + clear path | secondary CTA: "Clear filters" |
| **permission-empty** | user has no permission to see | explain boundary + request path | "Request access" / "Switch account" |

### Wording — the formula

Article line 12680: **空状态文案公式 = 价值 + 当前原因 + 第一行动.**

- Bad: "暂无数据"
- Good (initial): "还没有任务. 创建第一个任务,开始跟踪项目进展." + [Create task]
- Good (filter): "没有符合当前筛选条件的任务." + [Clear filters]
- Good (permission): "你暂时没有权限查看这些任务." + [Request access]

The wording is content-specific. "暂无数据" could move to any product and mean the same nothing — it fails the Swap Test.

### Wireframe per kind

For the state-matrix draft, draw three ASCII wireframes (or three grayscale frames), one per kind. Each shows a different empty-state UI:

- initial-empty: illustration + value statement + primary CTA
- filter-empty: muted list area + current-filter chips + clear-filters button
- permission-empty: lock icon + permission explanation + request-access button

## Error — in-place, with retry, preserving input

Article line 11711: **"错误状态有一个朴素原则:哪里出错,哪里解释."**

- field error → inline next to the field
- row error → inline on that row
- list error → in the list area (table head preserved) + retry button
- page error → page-level error with retry (only if the whole page failed)
- global error → full-screen error page (only for total outage)

**Never** a global "操作失败" toast for a field error. That's the AI tell.

The error must:
- explain in human words (not "request failed")
- offer a recovery (retry / undo / contact-admin)
- preserve what the user already did (draft saved, filter kept, scroll position kept)

## Loading — skeleton, not spinner

Article line 1811: "用骨架屏,不要只画转圈." A spinner tells the user nothing about what's loading or how long. A skeleton shows the shape of what's coming, which feels faster and more honest.

- list loading → row skeletons (grey rectangles in row shape)
- detail loading → field skeletons in the detail layout
- button loading → spinner INSIDE the button + label change ("Save" → "Saving…") + re-click blocked

## Permission — see-but-can't-act

Article line 610: **"权限不是一句'无权限',而是一整套体验."**

A viewer who sees a "Create" button that 403s on click is a P0 bug. Encode:

- viewer sees the button **disabled** (not hidden, not enabled-then-fail)
- tooltip on the disabled button explains why ("You need editor role to create tasks")
- or the button is hidden and a banner explains the role boundary

The object-state-permission matrix (`stage1-object-state-permission.md`) is the source of truth — every see-but-can't-act state comes from a cell in that matrix.

## Offline — what survives locally

Article line 3644: **"草稿不能丢 — 用户写的内容消失."**

- inputs being typed → survive in local storage, restored on reconnect
- "save" during offline → queued, with a "will sync when online" banner
- never fake-success on offline — article line 3655: "数据不同步,信任崩塌"

## Wireframe format for state variants

State variants use **ASCII + Markdown**, not grayscale images. The point is structure, not paint.

```text
EMPTY — initial
┌─────────────────────────────┐
│                             │
│        [illustration]       │
│                             │
│   还没有任务.                │
│   创建第一个任务,            │
│   开始跟踪项目进展.          │
│                             │
│      [＋ Create task]       │  ← primary
│                             │
└─────────────────────────────┘

EMPTY — filter
┌─────────────────────────────┐
│  filters: [status:done] ×   │
│  ─────────────────────────  │
│  没有符合当前筛选条件的任务.  │
│                             │
│      [Clear filters]        │  ← secondary
└─────────────────────────────┘

EMPTY — permission
┌─────────────────────────────┐
│        🔒                   │
│   你暂时没有权限查看         │
│   这些任务.                  │
│                             │
│   [Request access]          │
└─────────────────────────────┘
```

## Failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| "暂无数据" | four-word empty | three-classification rewrite |
| Global error toast | "操作失败" for a field error | in-place error at the field |
| Spinner only | bare spinner, no skeleton | skeleton matching the content shape |
| See-but-can't-act | button visible, 403 on click | disabled-with-reason from the permission matrix |
| Fake-success offline | "Saved!" while offline | queue + "will sync" banner |
