---
name: busy-town
description: Generate or plan publish-grade images that turn a workflow, system, team, process, division of labor, or organization into a warm hand-painted busy town where anthropomorphic animal townsfolk are hard at work — a top-down town panorama, a cutaway building, a two-page spread comparison, or a trade close-up — in the watercolor / gouache storybook look of busy illustrated towns. Use when a user wants to explain or illustrate how a process runs end to end, how a team divides work, how parts of a system cooperate, a user journey, an org chart, an industry, a production line, a comparison of two ways of working, or a system's internal cooperation as cooperating animal characters inside a hand-painted town. Trigger words include 忙忙碌碌, 小镇, 忙碌镇, 动物干活, 剖面图, 全景镇, 谁在做什么, 分工, 协作, 流程, 旅程, 工序, "把流程画成镇子", "用动物讲清楚这个系统", "画出谁在忙什么". Especially good for making abstract cooperation feel warm, concrete, and full of simultaneous life: show the roles, show how they hand off and cooperate, show the whole thing turning. Do not use for: a single-quote card (use a card skill), a social click-cover (use a cover skill), realistic product renders, 3D-rendered towns, flat vector cartoons, claymation, voxel/Minecraft, or reproducing Richard Scarry's original characters, scenes, or copyrighted likenesses.
---

# busy-town（Progressive Disclosure 瘦身入口）

> **Fleet Progressive Disclosure**: 默认只读本页脊柱。完整旧正文在 `references/full-rulebook.md`（默认不读）。需要细节时按节打开 full-rulebook，禁止通读当仪式。

## 何时用

见下方保留脊柱 / frontmatter description。若任务只需短约束，优先 vault `04-Prompts/UI铁律-速查卡.md`（仅 UI 类）。

## 阅读预算（硬）

1. 读完本页即可开工  
2. 卡住再查 `references/full-rulebook.md` 相关小节  
3. 有 scripts/data 则按需跑脚本，勿灌全表  

## 保留脊柱（摘自原文前部）

# Busy Town / 忙忙碌碌小镇

Busy Town turns an idea that has **cooperation** — roles, handoffs, a division of labor, a system running — into a warm hand-painted town scene where the townsfolk's work *is* the diagram.

默认面向中文图像/文档配图；用户使用英文时再切换英文输出。Use this skill when a concept is made of cooperating parts: a workflow, a team, a system, a user journey, an org, an industry, a process. **The town is the diagram. Animal characters are the verbs, the handoff between them is the grammar, the building is the container, and the street is the sequence.** If the idea is a single mood or one number with no "who works with whom / how does the whole thing turn", a town adds nothing — use a card or cover skill instead. The animals are never decoration; the way they hand off and cooperate must carry the meaning.

This skill exists because a flowchart of boxes and arrows, a sequence diagram, and a swimlane chart all lose something a busy town keeps: you can *see* who hands off to whom (one animal passes an object to the next), what the order is (animals line up along a street as one sequence of stations), how many roles there are (each window and each vehicle is a post), and that everything is happening *at once* (the whole page is busy). Division of labor, cooperation, sequence, and simultaneity become warm, visible life.

## Skill Boundaries — When to Use This, Not a Neighbor

Before anything else, confirm this is the right skill. The fastest failure is using a town for something a town can't do.

| The source is about… | Use | Why |
| --- | --- | --- |
| who hands off to whom / how does it run end to end / division of labor / simultaneity | **busy-town** | only a town can show cooperation + simultaneity warmly |
| a structure with parts that snap together / modules / dependencies / a prompt's anatomy | **lego-town** | bricks show *structural* assembly (snap/stack/wall), not character cooperation |
| one conceptual action performed on one object / a single paper-operator doing X to Y | **paper-operators** | one actor + one tool + one action, not a cooperating cast |
| one sentence / a quote / a number / one feeling | **quote-cards / cover-pop** | no cooperation to show |
| a realistic product render / a logo | neither | towns are explanatory, not photographic |

Borderline calls:
- "A microservice architecture" → if the article is about **how services cooperate** (handoffs, routing, the gateway), use **busy-town**; if it's about **how the system is structured** (layers, modules, dependencies), use **lego-town**. Read the source's verb: *cooperate* → town; *assemble* → bricks.
- "A user journey" → if it's about **roles the user passes through** (a customer meets 4 employees), use **busy-town**; if it's about **the path itself** (one traveler crossing terrain), use **paper-operators**.
- "A single concept's anatomy" (what's inside a good X) → **lego-town** exploded view, not a town.

If you cannot point at cooperation in the source, do not use this skill.

## Workflow

The workflow is not a checklist — each step has a **why** and a **failure mode**. Skip a step only if you can name why it doesn't apply.

### 1. Read the source — and classify the input
Read the source material. First **classify what kind of input** you have, because each is read differently:
- **A one-liner** ("画一下我们的订单流程"): the source is thin — you must **pull particulars from the user** (how many steps? who owns each? where does it hurt?) before drawing. A one-liner cannot drive a precise town; ask the one short question.
- **A paragraph / article / doc**: the source is rich — mine it for the real role names, the real step count, the real bottleneck, the real tradeoff. These particulars are what lock the image to this document (see Swap Test).
- **An existing image** ("改一下这张图"): the source is a picture — describe what's there, name what must stay invariant vs what changes. Use the image-edit template, not a fresh prompt.
- **Meeting notes / a transcript**: the source is noisy — extract the *decisions* and the *open questions*; a town of "what we agreed" beats a town of "everything that was said".
- **A comparison request** ("对比一下 A 和 B"): the source is two-headed — both sides must be drawn from the **same** town template or the comparison dies.

**Why:** the input type fixes how much you must invent vs extract. **Failure mode:** treating a one-liner like an article and inventing generic roles that fail the Swap Test.

### 2. Find the cooperation anchor — the one running whole


## 完整规则书

→ `references/full-rulebook.md`
