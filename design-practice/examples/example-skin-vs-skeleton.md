# Example — Skin vs Skeleton (the AI-plastic vs human-made diff)

> The clearest proof this skill works: the same task management list, generated two ways. Left: AI-plastic (one prompt, no discipline). Right: this skill (five-layer, 1:1 restore). The differences are exactly where the article says AI fails — states, permissions, focus, empty, micro-interactions.

## The setup

Same input both times: *"做一个团队用的任务管理列表页"*

## The AI-plastic version (what this skill refuses)

What a generic AI UI generator produces from that one line:

```text
┌────────────────────────────────────────────────┐
│  Tasks                              [+ New ▾]  │  ← two primary buttons (IA fail)
├────────────────────────────────────────────────┤
│  ✓ Fix login bug          @alex    today       │  ← no hover/pressed state
│  ✓ Design review          @sam     today       │  ← no loading skeleton
│  ✓ API refactor           @lee     tomorrow    │  ← no empty state at all
│  ✓ …                                            │
└────────────────────────────────────────────────┘

states: default only
empty state: (not drawn — "暂无数据" if asked)
error: global toast "操作失败"
focus ring: removed for "clean look"
permission: viewer sees [+ New] button that 403s on click
micro-interaction: hover changes bg color 5%
loading: bare spinner blocking whole page
```

**Symptoms (mapped to failure modes):**
- two primary actions → IA unclear (Failure #3)
- default state only → sunny-day UI (Failure #2)
- "暂无数据" empty → four-word tell (Failure #4)
- global toast error → not in-place (Failure #12)
- no focus ring → accessibility fail (Failure #6)
- viewer 403 on click → permission matrix missing (Failure: object-state-permission absent)
- hover-only-color → plastic micro-interaction (Failure #11)
- bare spinner → hides structure (Failure: loading)

**Diagnosis**: skin without skeleton. Head enemy. Eight pretty drafts of this would still be skin without skeleton.

## The human-made version (what this skill produces)

Same task, run through this skill's pipeline:

```text
┌─────────────────────────────────────────────────────────────┐
│ TOPBAR  [logo]  search            [notif] [avatar ▾]        │
├──────────┬──────────────────────────────────┬────────────────┤
│ SIDEBAR  │ MAIN: today's tasks             │ DRAWER (closed)│
│          │ ┌────────────────────────────┐   │                │
│ ▸ Today  │ │ □ Fix login bug   @alex ⚠│   │  (opens on    │
│ ▸ Week   │ │   due today · blocked      │   │   row click)  │
│ ▸ Proj…  │ └────────────────────────────┘   │                │
│          │ ┌────────────────────────────┐   │                │
│          │ │ □ Design review  @sam      │   │                │
│          │ │   due today                │   │                │
│          │ └────────────────────────────┘   │                │
│          │                                  │                │
│          │ [＋ New task]   primary          │                │
└──────────┴──────────────────────────────────┴────────────────┘

ONE primary (New task). Drawer for detail. Sidebar for nav.
```

### Where the human version differs (all 8 failure modes fixed)

| Failure | Plastic | Human (this skill) |
| --- | --- | --- |
| #1 skin-without-skeleton | 8 pretty drafts, no deep layers | five-layer drafts (A1 task-flow + A3 object-state-permission + A2 state-matrix + A4 system + B1 structure) |
| #2 default-only | default state only | 8 button states (default/hover/pressed/focus/disabled/loading/success/error) + 5 data states (loading/empty-3/error/permission/offline) |
| #3 two primaries | [New] + [filter ▾] both blue | one primary (New); filter is a secondary button |
| #4 "暂无数据" | four words | three-classified: initial (illustration + "还没有任务. 创建第一个." + CTA) / filter ("没有符合当前筛选." + clear) / permission ("你暂时没有权限." + request) |
| #5 hardcoded colors | `style="color:#2563EB"` | `button.primary.bg` → `color.state.primary` → `blue-600` (three-layer tokens) |
| #6 no focus ring | removed for clean | `:focus-visible` 2px ring, outside, never removed |
| #7 modal abuse | every action is a modal | drawer for detail (preserves list); modal only for destructive delete |
| #8 "Agent said done" | self-claims done | self-check list, P0/P1/P2, three-gate QA |
| #9 feature creep | added Gantt + calendar + AI-summary | cut — non-goals enforced from Task Card |
| #10 skipped Stage 1 | straight to hi-fi | Stage 1 low-fi drafts first, Stage 2 restores 1:1 |
| #11 plastic micro-interaction | hover changes color 5% | four-pack: pressed scale 0.98, drag shadow, toggle slide, drawer slide 240ms ease-out |
| #12 global toast error | "操作失败" toast | inline error at the row + retry, preserving filter |
| (bonus) permission | viewer sees [+New] that 403s | viewer's [+New] is disabled + tooltip "need editor role" — from A3 matrix |

## The single most damning diff: object-state-permission

The plastic version has **no concept** of:
- task lifecycle (draft / active / done / archived / soft-deleted)
- role × state × action (what viewer vs editor vs admin can do at each state)
- see-but-can't-act (button visible but disabled-with-reason)

These are the skeleton. The plastic UI has buttons that look right but 403 on click, deletes that are instant (no soft-delete window), archived tasks that disappear forever (no restore), draft tasks visible to viewers (privacy hole).

The human version sources every button's enabled-state, every list's filter, every error's wording from the A3 matrix. That's why it works.

## The micro-interaction diff (close-up)

**Plastic Save button:**
```css
.btn:hover { background: #1e40af; }   /* slightly darker blue, that's it */
```

**Human Save button (this skill):**
```css
.btn { background: var(--color-state-primary); transition: all 100ms var(--easing-standard); }
.btn:hover { background: var(--color-state-hover); cursor: pointer; }
.btn[data-pressed="true"] { background: var(--color-state-active); transform: scale(0.98); }
.btn:focus-visible { outline: 2px solid var(--color-border-focus); outline-offset: 2px; }
.btn[disabled] { opacity: 0.5; cursor: not-allowed; }
.btn[data-loading="true"] { /* spinner + label swap, pointer-events: none */ }
.btn[data-success="true"] { /* 200ms green flash → default */ }
.btn[data-error="true"] { animation: shake 200ms; }
@media (prefers-reduced-motion: reduce) { /* all motion → instant */ }
```

A user can't articulate why the second feels human and the first feels plastic. But they feel it. The second responds to press, focuses for keyboard, blocks re-click while saving, shakes on error, respects their motion preference. The first changes color on hover.

## Why this example exists

This is the proof the skill works. If you read this side-by-side and the human version doesn't feel visibly more "made by someone who cared", the skill has failed. Every difference maps to a specific article line and a specific failure mode. Nothing here is decoration — it's all skeleton.

## How to use this example

When demonstrating the skill:
1. Show the plastic version first.
2. Ask "what's wrong with this?" — most people say "it's fine" or "I can't put my finger on it".
3. Show the human version.
4. Walk the 12-row diff table. Each difference is a specific discipline the skill enforced.
5. End with: "the plastic version took one prompt; the human version took a Task Card + five-layer drafts + 1:1 restore + three-gate QA. Discipline, not talent."
