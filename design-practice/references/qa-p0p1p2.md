# QA — P0 / P1 / P2 Checklist (priority-gated human verification)

> Article line 2113-2131. The Agent self-checks first, then a human verifies with this priority-gated list. P0 blocks ship; P1 blocks same-day ship; P2 is polish.

## 统一输出格式(所有 qa-* 文件的 AI 验收员必须遵守)

> 出处:原文行 1799-1821。**所有 qa-*.md 的 AI 验收员提示词输出必须用同一个五段式格式**——这样人能横向比对不同维度的验收结果,Agent 也能把多次验收合并成一张总表。原文金句(行 1813):"**请逐条引用你检查到的具体位置,不要只说原则。**"

```text
验收输出格式(五段式):
- P0 必须修:会导致主任务失败、数据丢失、无法访问、严重误操作的问题
- P1 应该修:明显影响体验、效率或理解的问题
- P2 可以优化:不影响主任务但影响精致度的问题
- 通过项:已经做对的地方(简列,不夸奖)
- 需人工复核:AI 无法确认的地方(如真实手感、品牌调性、业务边界判断)

每条必须包含:
- 具体位置(文件名 + 行号 / DOM selector / 截图坐标)
- 为什么是问题(对照原文哪条规则 / 哪条 qa-* 检查项)
- 应该怎么改(可执行的修正方向,不是"改进一下")
```

**横向比对约定**:同一页面跑完 `qa-p0p1p2` / `qa-page-five-questions` / `qa-state-acceptance` / `qa-a11y` / `qa-responsive` / `qa-bad-data` 六张表后,把所有 P0 项合并成一张总 P0 列表去修——不要按表逐张修,会遗漏交叉项。

## "AI 不能当最终裁判"的两种失败模式(原文行 1793-1795)

> 原文金句:"AI 很适合做第一轮验收,因为它不累,可以按清单反复查。**但 AI 不能当最终裁判,因为它可能漏,也可能自信地说错。**"

AI 验收有两种失败模式,都要靠人补:

| 失败模式 | 长什么样 | 怎么补 |
|---|---|---|
| **假阴性(可能漏)** | AI 报"全过",但实际状态/边界/权限有洞 | 人走关键路径(创建→编辑→提交→失败→重试→返回),手测 |
| **假阳性(自信地说错)** | AI 报"P0 必修",但其实那条规则不适用本场景 | 人判断业务边界(如"这个 delete 不需要二次确认,因为是软删") |

**层级:Agent self-check(必要) → 人工走关键路径(权威) → Ship 决策**。原文行 2111:"**不要被'已完成'这句话安慰。**"

## Priority levels

| Level | Meaning | Action |
| --- | --- | --- |
| **P0** | blocks ship — critical failure, user cannot complete task or data is lost | must fix before ship |
| **P1** | blocks same-day ship — major usability or accessibility issue | fix within hours |
| **P2** | polish — minor inconsistency, copy refinement, motion tweak | fix when convenient |

## Agent self-check (run BEFORE handing to human)

```text
AGENT SELF-CHECK
================
1. Main task can run start to end? [P0]
2. One primary button per screen? [P0 if violated]
3. Covers loading / empty (3-kind) / error / permission / offline? [P0]
4. Form / comment submit failure preserves user input? [P0]
5. Drawer has ESC + focus trap + focus return? [P1]
6. Uses design tokens, no hardcoded values? [P1]
7. Has edge data (long text, empty fields, expired dates)? [P1]
8. Has mobile layout? [P1]
9. Cut non-MVP features (no Gantt / calendar / AI-summary unless asked)? [P1]
10. No inaccessible buttons (icon button without aria-label, low-contrast text)? [P1]

Output:
- pass items
- fail items (with P-level)
- files to modify
- code snippets to fix
- still-need-human-confirm items
```

Article line 2113: **"不要直接说'完成'. 请按下面清单自查你刚才生成的实现."** The Agent doesn't get to say "done" — it reports pass/fail against the list.

## P0 — blocks ship

```text
P0 CHECKS (must all pass to ship)
==================================
[ ] Main task start-to-end works (no dead-ends, no stuck states)
[ ] No repeat-submit risk (loading blocks re-click on all submit buttons)
[ ] Form input preserved on network failure (no data loss)
[ ] No visible button that 403s on click (permission matrix enforced)
[ ] Empty states are classified (no "暂无数据")
[ ] Errors are in-place (no global "操作失败" for field errors)
[ ] Loading uses skeletons (not bare spinner that hides structure)
[ ] No crash on edge data (long text, empty fields, special chars, expired dates)
[ ] Object-state-permission matrix fully enforced (every role × state × action)
[ ] Offline doesn't fake success (drafts queued, "will sync" banner)
```

## P1 — blocks same-day ship

```text
P1 CHECKS (fix within hours)
=============================
[ ] All 8 button states present (not just default + hover)
[ ] Focus rings visible (focus-visible, 2px, outside)
[ ] Drawer / modal have focus trap + ESC + focus return
[ ] aria-label on all icon buttons
[ ] aria-busy on loading buttons
[ ] Semantic HTML (button for action, a for nav, not div)
[ ] No hardcoded colors / spacing / fonts (all via tokens)
[ ] Mobile layout works (sidebar folds, filters move to drawer)
[ ] Dark mode via token swap (not separate page)
[ ] prefers-reduced-motion respected
[ ] Copy is human and specific (not "request failed")
[ ] Typography scale consistent (no orphan sizes)
[ ] Spacing on 4/8 grid (no 13px margins)
[ ] One primary action per screen
```

## P2 — polish

```text
P2 CHECKS (fix when convenient)
===============================
[ ] Micro-interactions feel physical (pressed scale, drag shadow, toggle slide)
[ ] Motion uses ease-out / standard (no linear except loops)
[ ] Toast auto-dismiss pauses on hover
[ ] Success feedback is brief (200ms flash, not permanent green)
[ ] Empty state illustrations feel warm (not generic)
[ ] Copy tone consistent across the app
[ ] Transitions match spatial logic (drawer slides from right, not fades)
[ ] Keyboard shortcuts documented (in a ? help panel)
[ ] Hover states differ enough to read (not 2% darken)
[ ] Skeleton shapes match content shapes (not generic gray bars)
```

## The human verification step

After the Agent self-checks, a human (or the user) verifies with this sequence:

```text
HUMAN VERIFY
============
1. Walk the main task as a real user (start → done). Note any hesitation.
2. Walk each breaking state with edge data:
   - loading: throttle network to slow 3G, watch skeletons
   - empty: fresh account with no data, then with no-match filter, then with wrong role
   - error: kill network mid-submit, check draft survives
   - permission: log in as viewer, try to create / edit / delete
   - offline: toggle offline mid-typing, check draft queued
3. Keyboard-only pass: unplug mouse, do the main task with Tab/Enter/ESC only.
4. Mobile pass: resize to mobile, check sidebar folds and filters drawer.
5. Dark mode pass: toggle theme, check contrast and token swap.
6. Walk the P0 list, then P1, then P2.
```

If any P0 fails → block ship, fix, re-verify. If P1 fails → fix before end of day. P2 → backlog.

## The "Agent said done" trap

Article line 2111: **"不要被'已完成'这句话安慰."**

When the Agent self-check reports all-pass but a human walk finds issues, trust the human walk. The Agent's self-check is necessary but not sufficient — it can't feel hesitation, can't spot a slightly-wrong tone, can't judge if a motion feels physical.

The hierarchy: **Agent self-check (necessary) → Human walk (authoritative) → Ship decision**.

## Failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| Skipped Agent self-check | "looks done" without list | mandatory self-check output |
| P0 rubber-stamp | all P0 pass without checking | human walk is authoritative |
| Ship on P0 fail | "we'll fix in v2" | P0 blocks ship, no exceptions |
| P1 treated as P2 | "polish later" forgotten | P1 blocks same-day ship |
| No edge data | only happy path tested | test long text, empty, special chars, expired |
