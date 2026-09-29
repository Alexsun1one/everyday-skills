# Stage 1 — The Five-Layer Blade (soul of this skill)

> Read this FIRST before any Stage 1 work. The Five-Layer Blade is what makes this skill different from every "AI UI generator" on the planet. If you skip this, you will produce skin without skeleton — the exact failure this skill exists to refuse.

## The one insight

AI-generated UI dies one way: **skin without skeleton** (article line 3253). AI is fast hands that don't know weight (line 1611). It draws buttons, lays out cards, generates a whole dashboard — but without discipline it skips states, skips empty states, skips permissions, skips errors, skips the data lifecycle, skips design tokens. It looks like a UI, but it has no skeleton under the skin.

The article's case-dissection blade (line 3257) is the cure. It dissects any great product into five layers, from the outside in:

```
① Task      → ② Structure  → ③ State     → ④ System     → ⑤ Tradeoff
任务          结构            状态           系统           取舍
```

**This skill reverses the blade** — instead of dissecting a finished product INTO five layers, we GENERATE five layers and assemble them INTO a product. Every Stage-1 draft digs ONE layer to the bone. The drafts then combine (mosaic) into a complete product that has skeleton as well as skin.

## The five layers

### ① Task layer — 用户办哪件事,主流程怎么走顺

**Dig target:** the user's errand, end to end. Where they come from, what they came to do, how the main flow runs smooth, where they easily get stuck, what counts as "done".

**What AI skips:** business value, success criteria, non-goals. AI happily draws a beautiful dashboard that doesn't serve any real errand.

**Draft type:** a **task-flow draft** — only the main flow, drawn as a Mermaid flowchart (no visual fuss). Nodes = steps, edges = handoffs, branches = the few real decision points. Side-channels for the recoveries (back / cancel / save-draft).

**Layer-relevant formats:** Mermaid (flow) + Markdown (step rationale).

**Pass criterion:** a reader who has never seen the product can trace the user from arrival to done, and name the one step where things most often break.

### ② Structure layer — 页面/导航/容器/分组怎么安排

**Dig target:** information architecture — pages, navigation, container choice (page / drawer / modal / popover / split-pane), grouping, hierarchy, sense-of-place (does the user know where they are?).

**What AI skips:** container logic. AI puts everything on one page (line 1483: "筛选项全摊开,操作按钮全放出来,设置项全堆在一个页面"). It draws a full-page filter wall instead of progressive disclosure.

**Draft type:** an **IA draft** (Type B) — one genuine structural variant. Sidebar+list+drawer / kanban+click-expand / single-column+inline-edit / two-pane-constant / card-grid+modal. Each must differ in IA, not in paint.

**Layer-relevant formats:** ASCII wireframe (block layout) + grayscale image-wireframe prompt (proportion/rhythm).

**Pass criterion:** one sentence says how this IA genuinely differs from the other variants. If you can't say it, it's a reskin — cut it.

### ③ State layer — 加载/空/错/权限/离线怎么稳住用户

**Dig target:** the breaking moments — not the sunny day. Loading, empty (three kinds), error, permission-denied, offline, repeat-click, invalid-data, long-text overflow.

**What AI skips:** everything except the default state. Article line 1281: "默认态是天气晴朗的时候,状态才是下雨、堵车、停电、信号差的时候."

**Draft type:** a **state-matrix draft** — one wireframe per breaking moment, plus the full **8-state × 4-column matrix** (state / visual / copy / behavior) for the core interactive component.

**Layer-relevant formats:** Mermaid (state-transition diagram) + Markdown (the 8×4 matrix table).

**Pass criterion:** name ≥3 real, content-specific breaking moments (not generic "loading/empty/error"). Empty must be three-classified (initial / filter / permission). Error must be in-place (where it breaks, there it explains).

### ④ System layer — 令牌/组件/模式/一致性

**Dig target:** the design system — token three layers, component inventory, reusable patterns, dark-mode strategy, the rules that keep the product consistent as it grows.

**What AI skips:** tokens. AI hardcodes `#2563EB` inside a button instead of `button.primary.bg`, and the product becomes unmaintainable (line 973).

**Draft type:** a **system draft** — a Markdown doc with the primitive palette, the semantic token mapping, the component inventory (Button / Input / Table / Drawer / EmptyState / ErrorState / Toast / Skeleton), the reusable patterns (list+detail-drawer, filter-drawer, confirm-destructive).

**Layer-relevant formats:** Markdown (token + component tables). Mermaid optional (token hierarchy).

**Pass criterion:** a developer could build the component library from this doc alone, without seeing the final UI.

### ⑤ Tradeoff layer — 为什么这样,不那样,删了什么

**Dig target:** the judgment itself — why this container, why this state wording, why this got cut, what the cost of every choice is. The article's line 3506: "学世界级产品,不要学皮肤,要学判断."

**What AI skips:** the negative space. AI adds features (charts! calendars! AI-summary!) because more feels like more. Article line 2099: "AI 很爱加戏." A real product is defined as much by what it doesn't do.

**Draft type:** a **tradeoff note** attached to every other draft (not a standalone draft). Answers: good / cost / fit / unfit / **which of the five layers does this dig** / **how does it 拼 into the whole product**.

**Layer-relevant formats:** Markdown.

**Pass criterion:** the note names a real scene where this choice hurts. If a tradeoff has no cost, it isn't a tradeoff — it's a wish.

## How the layers compose — the mosaic

The five layers are not a checklist; they are a **mosaic** that assembles into a product:

```
① Task        → answers "what is this for"
② Structure   → answers "where does everything go"
③ State       → answers "what happens when it breaks"
④ System      → answers "how does it stay consistent"
⑤ Tradeoff    → answers "why this, not that"
```

A product missing any layer has a specific failure:
- missing ① → pretty UI, no point
- missing ② → clutter, everything on one page
- missing ③ → sunny-day UI, crashes on real use
- missing ④ → unmaintainable, drifts apart across teams
- missing ⑤ → bloated, no identity

**The Mosaic-coverage QA gate** (see `qa-mosaic-check.md`): before Stage 2, confirm every layer has at least one draft. A run with 8 Structure drafts and zero Task/State/System drafts has failed — it's eight skins, no skeleton.

## The falsifiable test for Stage 1

State your draft plan as a sentence with a *because*:

> "I'm digging the **State** layer *because* the user's draft is lost on network failure, and only a state-matrix draft can force the recovery path into the design before the pretty pixels bury it."

If you can't finish the *because* with a structural reason, you picked by habit — go back to the blade.
