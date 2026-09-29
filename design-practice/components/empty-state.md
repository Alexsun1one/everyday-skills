# Component: Empty State (3 classifications)

Article line 11681 (paraphrased): the empty state is where AI is laziest — "暂无数据" four words. A real empty state **diagnoses which kind of empty it is** and gives the user the right next move.

## The 3 classifications of empty (article core)

| Kind | Why it's empty | Right response |
| --- | --- | --- |
| **initial** | user has never created anything here | explain value + primary CTA to create first item |
| **no results** | user filtered/searched and nothing matched | show the active filters + clear-filters action |
| **error** | something failed loading the data | explain what failed + retry action (preserve filters) |

The same "no data" screen needs 3 different designs. AI conflates them into one "暂无数据".

## Spec table (pixel-exact)

| Token | Value |
| --- | --- |
| container padding | 48px vertical 24px horizontal (`py-12 px-6`) |
| max-width | 448px (`max-w-md`) centered |
| text-align | center |
| illustration | 64px-120px (`size-16` to `size-30`), grayscale or single-accent line art |
| title | 16px weight 600 (`text-base font-semibold`) |
| description | 14px weight 400 secondary (`text-sm text-secondary`) |
| gap title→desc | 8px |
| gap desc→action | 24px |
| action | primary button (initial), secondary/ghost button (no-results), secondary+primary retry pair (error) |

## The 3 empty states side by side

### 1. Initial empty (user has nothing yet)

```text
┌─────────────────────────────────────┐
│                                      │
│         [📁 illustration 96px]       │
│                                      │
│        Create your first task        │  ← 16px/600
│                                      │
│  Tasks help you track what needs     │  ← 14px/400 secondary
│  to get done. Start by creating one. │
│                                      │
│         [ + New task ]               │  ← primary button
│                                      │
└─────────────────────────────────────┘
```

- **Title**: action-oriented ("Create your first task" not "No tasks")
- **Description**: explains value ("Tasks help you track what needs to get done")
- **CTA**: primary button, verb label, opens the creation flow

### 2. No-results empty (filters/search matched nothing)

```text
┌─────────────────────────────────────┐
│                                      │
│         [🔍 illustration 64px]       │
│                                      │
│      No tasks match your filters     │  ← shows what user did
│                                      │
│  Active filters: Status=Done,        │  ← echoes the filters
│  Assignee=You                        │
│                                      │
│     [ Clear filters ]                │  ← secondary/ghost button
│                                      │
└─────────────────────────────────────┘
```

- **Title**: explains the match failure ("No tasks match your filters")
- **Description**: echoes active filters so user understands why
- **CTA**: secondary/ghost "Clear filters" (not a primary — the user's intent was correct, the data just isn't there)

### 3. Error empty (failed to load)

```text
┌─────────────────────────────────────┐
│                                      │
│         [⚠ illustration 64px]        │
│                                      │
│      Couldn't load tasks             │  ← what failed
│                                      │
│  Check your connection and try       │  ← specific recovery hint
│  again. Your filters are preserved.  │
│                                      │
│         [ Retry ]                    │  ← secondary button
│                                      │
└─────────────────────────────────────┘
```

- **Title**: what failed ("Couldn't load tasks")
- **Description**: specific recovery hint + reassurance ("filters preserved")
- **CTA**: secondary "Retry" (NOT primary — this is a recovery, not a creation)

## Prompt fragment (English)

```text
Empty state spec (3 classifications, pixel-exact):
- container: padding 48px vertical 24px horizontal, max-width 448px centered, text-align center
- illustration: 64-120px, grayscale OR single-accent line art (NOT decorative emoji, NOT stock photo)
- title: 16px weight 600 #111827
- description: 14px weight 400 #6B7280, gap 8px below title
- action: gap 24px below description, button per variant

THREE classifications (you MUST pick the right one — they are NOT interchangeable):

1. INITIAL EMPTY (user has never created anything):
   - title: action-oriented ("Create your first task" NOT "No tasks")
   - description: explains the VALUE ("Tasks help you track what needs to get done")
   - CTA: PRIMARY button, verb label, opens creation flow

2. NO-RESULTS EMPTY (filters/search matched nothing):
   - title: explains match failure ("No tasks match your filters")
   - description: ECHOES active filters ("Active filters: Status=Done, Assignee=You")
   - CTA: SECONDARY/GHOST button "Clear filters" (NOT primary — user's intent was correct, data just isn't there)

3. ERROR EMPTY (failed to load):
   - title: what failed ("Couldn't load tasks")
   - description: specific recovery hint + reassurance ("Check your connection. Your filters are preserved.")
   - CTA: SECONDARY button "Retry" (NOT primary — this is recovery, not creation)

NEVER:
- use "暂无数据" / "No data" / "Nothing here" as the title (lazy, unhelpful)
- use the same empty state for all three kinds (they need different CTAs)
- use decorative emoji as illustration (🍔 🎉 ❌ are not illustrations)
- use a primary button on no-results or error (wrong hierarchy)
- forget to echo the active filters on no-results (user needs to understand why)
- forget to preserve filters on error retry (don't make user re-filter)
- use a stock photo (breaks product fiction)
```

## Prompt fragment (Chinese)

```text
空状态规格(3 种分类,精确到像素):
- 容器:内边距 上下48px 左右24px,最大宽 448px 居中,文字居中
- 插图:64-120px,灰度或单色线稿(不要装饰性 emoji,不要图库照片)
- 标题:16px 字重 600 #111827
- 描述:14px 字重 400 #6B7280,距标题 8px
- 操作:距描述 24px,按变体选按钮

三种分类(必须选对——它们不可互换):

1. 初始空(用户从没创建过任何东西):
   - 标题:行动导向("创建你的第一个任务" 不是 "暂无任务")
   - 描述:解释价值("任务帮你跟踪要做的事")
   - CTA:主按钮,动词标签,打开创建流程

2. 无结果空(筛选/搜索没匹配到):
   - 标题:解释匹配失败("没有任务匹配你的筛选")
   - 描述:回显当前筛选("当前筛选:状态=已完成,指派=你")
   - CTA:secondary/ghost 按钮"清除筛选"(不要主按钮——用户意图是对的,只是数据没有)

3. 错误空(加载失败):
   - 标题:什么失败了("无法加载任务")
   - 描述:具体的恢复提示 + 安抚("请检查网络后重试。你的筛选会保留。")
   - CTA:secondary 按钮"重试"(不要主按钮——这是恢复,不是创建)

绝对不要:
- 用 "暂无数据" / "No data" / "Nothing here" 当标题(懒,没用)
- 三种空用同一个空状态(它们的 CTA 不同)
- 用装饰性 emoji 当插图(🍔 🎉 ❌ 不是插图)
- 无结果或错误用主按钮(层级错了)
- 无结果忘了回显当前筛选(用户要理解为什么没数据)
- 错误重试忘了保留筛选(别让用户重新筛一遍)
- 用图库照片(破坏产品虚构)
```

## Tailwind classes

```tsx
// initial empty
<div className="flex flex-col items-center justify-center px-6 py-12 text-center">
  <div className="mb-6 size-24 text-[--color-text-secondary]">{/* line-art illustration */}</div>
  <h3 className="text-base font-semibold text-[--color-text-primary]">Create your first task</h3>
  <p className="mt-2 max-w-sm text-sm text-[--color-text-secondary]">Tasks help you track what needs to get done. Start by creating one.</p>
  <Button className="mt-6" onClick={openNewTask}>+ New task</Button>
</div>

// no-results empty
<div className="...">
  <div className="...">{/* magnifier illustration */}</div>
  <h3 className="...">No tasks match your filters</h3>
  <p className="...">Active filters: <Chip>Status=Done</Chip> <Chip>Assignee=You</Chip></p>
  <Button variant="secondary" onClick={clearFilters}>Clear filters</Button>
</div>

// error empty
<div className="...">
  <div className="...">{/* warning illustration */}</div>
  <h3 className="...">Couldn't load tasks</h3>
  <p className="...">Check your connection and try again. Your filters are preserved.</p>
  <Button variant="secondary" onClick={retry}>Retry</Button>
</div>
```

## Reverse examples

| Aspect | Plastic | Human |
| --- | --- | --- |
| classification | one "暂无数据" for all | 3 distinct states |
| title | "No data" | action-oriented or diagnosis |
| description | none | value explanation, filter echo, or recovery hint |
| CTA | none or always primary | matched to kind: primary (initial), secondary (no-results/error) |
| illustration | emoji 🎉 | grayscale line art |
| filter echo | missing | shown on no-results |
| filter preserve | lost on retry | preserved |

## Composes with

- `button.md` — primary (initial), secondary (no-results/error)
- `table-row.md` — replaces tbody when empty
- `badge.md` — filter chips on no-results

## Failure modes

| Failure | Fix |
| --- | --- |
| "暂无数据" title | diagnose kind, write action-oriented title |
| same state for all 3 | split into initial/no-results/error |
| emoji as illustration | grayscale line art |
| primary on no-results | demote to secondary |
| no filter echo | list active filters |
| filters lost on retry | preserve in retry request |
