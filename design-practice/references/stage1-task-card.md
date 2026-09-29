# Stage 1 — Task Card (the entry ticket)

> No Task Card, no Stage 1. The Anti-Plastic Test in `SKILL.md` is a gate — if the user's input can't answer these fields, you force them to fill this card before generating anything.

## Why a Task Card

Article line 2018: *"任务卡一句话:别让 Agent 猜'做什么'. 你要把用户、场景、任务、成功标准、非目标、状态边界一次说清楚. 说得越清楚,AI 越像助手;说得越含糊,AI 越像老虎机."*

A vague idea ("做一个任务管理 App") fed straight to an AI produces a plastic UI — generic, sunny-day, no states. The Task Card forces the user to commit before the AI guesses. It is the difference between ordering a meal and asking the kitchen to surprise you.

## Template

```text
TASK CARD
=========

user:
  - who: [role, e.g. "project manager at a 20-person software team"]
  - scenario: [when/where, e.g. "daily standup prep, morning, laptop, slightly rushed"]
  - device: [desktop / mobile / both]
  - mood: [rushed / focused / anxious / bored — affects wording and density]

core task:
  - one sentence: [the thing they came to do, e.g. "see what's due today and reassign what's blocked"]
  - the main flow: [arrival → step → step → done, in 3-5 nodes]

success criteria:
  - [how we know it's done, e.g. "user can reassign 5 tasks in under 60s without losing their place in the list"]

non-goals (THIS ROUND):
  - [what we are NOT doing, e.g. "no Gantt chart, no time-tracking, no mobile this round"]

risks (where it breaks):
  - [the real failure points, e.g. "network slow at standup time; assignee has no permission; due-date passed"]

states that can break (name ≥3):
  - loading: [when, how long]
  - empty: [which of 3 kinds: initial / filter / permission]
  - error: [which failure, what must survive]
  - permission: [which role hits which wall]
  - offline: [what survives locally]

data objects & lifecycle:
  - object: [e.g. Task]
  - states: [e.g. draft → active → done → archived → deleted]
  - key fields: [e.g. title, assignee, due, status, project]

permission roles:
  - viewer: [can do X]
  - editor: [can do Y]
  - admin: [can do Z]
  - author: [special rights on own objects]

one primary action per screen:
  - [confirm: yes/no. if no, IA is wrong, fix before generating]
```

## How to fill it with the user

Don't send the user a blank template and wait. **Ask one short question at a time**, in this order:

1. "谁会用这个?在什么场景下用?" (fills `user`)
2. "他来这想办成哪一件事?" (fills `core task`)
3. "怎么算办成了?" (fills `success criteria`)
4. "这次先不做什么?" (fills `non-goals` — the most important field, because AI will otherwise add features)
5. "什么时候会出事?加载慢、没数据、报错、没权限、断网,哪种最真实?" (fills `states that can break`)
6. "数据是什么?有哪些状态?谁能改?" (fills `objects & roles`)

Stop after 3 questions if the user is impatient — you can fill the rest from inference and confirm. But never generate Stage 1 without `core task` + `states that can break` + `non-goals`.

## Failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| No non-goals | "做全功能" → AI adds charts, calendar, AI-summary | force 3 non-goals before generating |
| Generic states | "loading, empty, error" with no scenario | ask "when specifically? how long? what must survive?" |
| No objects | UI has no data model underneath | ask "what's a row in the list? what fields? what states?" |
| Multiple primaries | "create, edit, delete are all important" | one primary per screen — demote the rest |
| Goal is "look like X" | "make it look like Linear" | push back: "Linear's look comes from restraint; what's YOUR task?" |

## The one-line sanity check

After the card is filled, read it back as one sentence:

> "A [user] in [scenario] comes to [core task], and we'll know it worked when [success criteria]; this round we're NOT doing [non-goals]; the most likely breakage is [states]; the data is [objects] with [roles]."

If that sentence reads true and specific, proceed. If it reads like it could describe any product, the card isn't filled — go back.
