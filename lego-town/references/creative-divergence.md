# Creative Divergence / 创意发散

创意发散不是把画面做花；它是在进入最终 prompt 前，先把同一个结构试搭成几种**不同但都能承重意义**的积木世界，再收敛到最清楚、最新鲜、最适合用户意图的一种。Every fresh idea still has to pass `connection-grammar.md`, `brick-library.md`, `modes.md`, and `style-dna.md`: the physical brick connection must carry the exact relation.

## Core Rule / 先发散再收敛

对任何非平凡请求，先做 2-4 个不同 build concepts，再选一个。非平凡请求包括：系统、流程、prompt、文档结构、策略关系、知识图谱、团队协作、产品机制、复杂对比、带多个步骤的说明、或用户说"想要更有创意/不要死板"。简单请求可以只给一个小 build；即便如此，也要避免无脑套 Baseplate Town / 小镇地图。

### Concept Sketch Format / 候选草图格式

- **metaphor world / 隐喻世界**：工厂地面、运河水闸镇、地铁换乘图、邮政分拣厅、港口装卸区、实验台、庭院花圃、维修车库。
- **mode / 成像模式**：Finished Build / 成品、Instruction Sheet / 说明书、Exploded View / 爆炸图、Box Art / 盒面。
- **build archetype / 搭建原型**：Load-Bearing Stack、Conveyor Line、Brick Seesaw、Gear Train、A/B Split Plate、Checkpoint Gate、Walled District、Build Machine、Road Fork、Funnel Hopper、Tug Anchors、Baseplate Town。
- **minifig framing / 小人仔视角**：Builder mid-snap、Inspector at gate、Courier riding route、Operator at lever、Surveyor mapping, or none because the build alone carries it.
每个候选只写 1-2 行；先证明概念不同，不要先写灯光、镜头或装饰。

## Diverge Then Converge Flow / 发散收敛流程

1. Name the source anchor: what structure is actually worth building.
2. Name the primary relation from `connection-grammar.md`.
3. Draft 2-4 concept sketches with different worlds, modes, archetypes, and minifig framings.
4. Reject any candidate whose brick connection does not carry the relation.
5. Pick the strongest candidate, or present the sketches and let the user choose when taste matters.
6. Only after the pick, write the full Build Test and final image prompt.

收敛标准：不是"最炫"，而是"最能让读者在三秒内看见关系，同时不是上一张图的复刻"。

## Worked Mini Example / 小样例

Request: "把一个 AI 客服系统的意图识别、知识检索、工具调用、人工转接画成一张图。"
Concept A — **postal sorting hall + Finished Build + Checkpoint Gate / Conveyor Line + Inspector**：用户消息是一块包裹砖，在分拣厅被意图门盖章，沿 conveyor 进入知识库货架、工具工作台，异常件转人工柜台。
Concept B — **canal-lock town + Instruction Sheet + Sluice Gate / Road Fork + Operator**：水流代表请求，先过意图水闸，再按水位/规则进入知识渠、工具渠或人工渠；说明书面板显示每一步增加的闸门与渠道。
Concept C — **subway interchange + Exploded View + Road Fork / Funnel Hopper + Guide**：请求列车在换乘站分流，三条轨道浮起展示各自组件，最终在答复站汇流成一个输出模块。
Pick: Concept A. Why: 客服系统的核心是"分类、分拣、转送、异常转人工"，postal sorting hall 的实体动作最贴近；Checkpoint Gate 能清楚显示边界/过滤，Conveyor Line 能显示顺序与交接，Inspector 的盖章动作让"意图识别"不是抽象标签。

## Techniques To Escape The Obvious / 逃出默认原型

### Re-cast The Domain World / 换一个世界

不要把所有软件系统都画成服务器小镇。先问：这个关系在真实世界里像什么？

- **factory floor**：Conveyor Line、Build Machine、Checkpoint Gate；适合 sequence / transformation / boundary。
- **canal-lock town**：sluice gate、water level、holding basin；适合 rate limiting / backpressure / threshold。
- **subway map**：rails, interchange, platform gates；适合 routing / branch / merge。
- **postal sorting hall**：parcels, sorting chutes, bins; 适合 classification / handoff / exception.
- **toolbox drawer / modular plug-in bay**：prompt optionality、configuration、extension slots.
- **harbor docks / shared workshop bench / tug-anchor span**：organization ownership、resource contention、tension.

换世界后，仍要让 bricks/plates/tiles/slopes/baseplate 的连接关系可见；世界只是帮助选机制，不是背景皮肤。

### Swap The Mode / 换成像模式

- **Finished Build / 成品**：适合一次看全局、依赖、边界、对比、系统地图。
- **Instruction Sheet / 说明书**：适合 prompt、workflow、setup、multi-step process；读者看到"先放底板，再加砖"。
- **Exploded View / 爆炸图**：适合 anatomy、components、"what is inside"; 能把层级和接口拆开。
- **Box Art / 盒面**：适合封面和一眼定位，但不要用它隐藏复杂结构。

If every answer keeps becoming Finished Build, force an Instruction Sheet or Exploded View candidate before deciding.

### Invert Scale / 反转尺度

- **one giant single brick close-up**：一块 2×4 砖被剖开，内部 tube、clutch、stud label 展示一个概念的组成；适合"一个机制的 anatomy"。
- **whole town from above**：多个 district、roads、gates、hoppers 构成系统；适合 rich system。
- **macro workstation**：只拍一个 gate、one lever、one rail switch；适合一个关键关系。
- **tiny pocket build**：一块 8×8 plate 上只有三件东西；适合 simple claim，避免过度小镇化。

### Shift POV Through A Minifig / 用小人仔换视角

- reader rides the conveyor as a tiny Courier: sequence becomes embodied.
- Inspector stands at the Checkpoint Gate: boundary/filter becomes an event.
- Operator holds the lever: causality is the moment of trigger.
- Surveyor looks down at a half-built baseplate: planning and optional paths become visible.
- Builder snaps a missing brick into an exposed stud slot: work-in-progress and dependency become tactile.

If removing the minifig changes nothing, cut it and pick a stronger build mechanism.

### Hunt The Mechanism / 找意外但贴切的积木机关

- A loose coupling may be clearer as a ball-and-socket joint than a bridge.
- A scheduling loop may be clearer as a turntable than a gear train.
- Auth may be clearer as a key-and-lock brick than a generic gate.
- Feature flags may be clearer as a swappable colored module on a rail than an A/B Split Plate.
- Backpressure may be clearer as a sluice/water-lock than a blocked road.

Unexpected is good only when it is more exact.

## Fresh Brick Metaphor Library / 新鲜积木隐喻库

Use these when the base archetypes feel too predictable. Each line maps metaphor → relation served → `connection-grammar.md` family.

- **claw crane pick / 抓斗吊车** → selection, picking one item from many bins → Boundary, Filter & Threshold.
- **ball-and-socket joint / 球窝关节** → flexible or loose coupling, adjustable interface → Connection.
- **minifig tug-of-war over one shared plate / 小人仔拔河抢同一块板** → contention for a shared resource → Tension & Equilibrium.
- **modular plug-in bay with spare studded slots / 可插拔模块舱** → extensibility, optionality, future module slots → Divergence & Convergence / Connection.
- **scaffold around a half-built tower / 半成品塔外脚手架** → work-in-progress, temporary support, migration in flight → Transformation / Dependency.
- **spinning turntable / 旋转转盘** → cycles, rotation, scheduling, round-robin allocation → Feedback Loop.
- **sluice gate / canal lock / 水闸船闸** → rate limiting, backpressure, controlled flow → Boundary, Filter & Threshold.
- **key-and-lock brick / 钥匙锁扣砖** → auth, permission, access control → Boundary, Filter & Threshold.
- **swappable colored module on a rail / 轨道上的换色模块** → configuration, feature flag, environment switch → Contrast & Opposition / Transformation.
- **domino cascade of plates / 多米诺板片连锁** → chain reaction, trigger propagation → Causality & Trigger.
Pick one unexpected mechanism and make it load-bearing.

## Adaptive Complexity / 复杂度自适应

- **one simple claim** → tiny 8×8 or 12×12 build: one foundation, one module, one label, maybe no minifig.
- **two options or before/after** → A/B Split Plate or Before/After Twin: matched builds, one highlighted difference.
- **one process** → Instruction Sheet or Conveyor Line: 3-5 numbered stations, one handoff object.
- **one anatomy** → Exploded View: ≤7 modules, aligned drop-lines, ghost preview.
- **rich system** → Baseplate Town / Walled District: districts, roads, gates, one focal route; keep side buildings quiet.
- **strategy or tension** → Brick Seesaw / Tug Anchors: visible forces, weights, anchors, residual risk part.

Overbuilding is a failure: a tiny thought does not need a metropolis. Underbuilding is also a failure: a rich system should not be reduced to one cute brick.

## Freshness Budget / 新鲜度预算

Rotate worlds and archetypes across a user's requests. Track the last 3-5 outputs mentally:

- if the last image was a Baseplate Town, try Instruction Sheet, Exploded View, or a macro mechanism.
- if the last two used Conveyor Line, try canal-lock, postal sorting, rail switch, or Build Machine.
- if every software topic becomes gray-blue engineering town, switch district: workshop, harbor, school lab, garden plot, archive room, subway station.
- keep semantic constants stable inside a series: the same color and same brick type must mean the same thing.
- vary the metaphor world between independent requests; do not vary it inside one series unless the user asks for a new direction.

Freshness is budgeted after correctness. The first budget is relation accuracy; the second is readability; the third is novelty.

## Guardrail / 创意护栏

A fresh metaphor is valid only if it still passes the Build Test and the connection grammar:

- dependency still needs physical support, load path, or removable foundation.
- sequence still needs order, handoff, stations, or assembly steps.
- boundary still needs a gate, wall, lock, sieve, or pass/fail sorting.
- feedback still needs returning influence: gears, loop conveyor, governor, turntable, or repeating dispatch.
- tension still needs visible pull, anchors, counterweight, or held equilibrium.
- divergence/convergence still needs a fork, switch, lanes, hopper, junction, or criteria tile.

If the metaphor is clever but the relationship is no longer visible, regenerate. In the final image prompt, name the chosen concept, relation, mode, and archetype; describe the physical connection before the atmosphere; attach labels to tiles/signboards/plinths/road signs/call-outs; keep Original-Bricks rules from `style-dna.md`; run Build Test and Minifig Test before finalizing.

## Accept / Regenerate

Accept if:

- 2-4 genuinely distinct concepts were considered for a non-trivial request.
- The concepts vary at least two of: metaphor world, mode, build archetype, minifig framing, scale, POV.
- The chosen concept is fresh enough that it does not look like the last default output.
- The chosen concept still uses bricks/plates/tiles/slopes/baseplate connections as load-bearing meaning.
- The primary relation from `connection-grammar.md` is visible without relying on a generic arrow or paragraph label.
- Any unexpected mechanism is apt, tactile, and physically tied to the relation.
- Build Test and Minifig Test both pass.

Regenerate if:

- It defaulted to the obvious archetype with no alternatives considered.
- All candidates are the same town with different decorations.
- "Creative" means only extra props, skyline, color, or minifig charm.
- The metaphor became decorative and lost dependency, sequence, boundary, feedback, divergence, tension, or another named relation.
- The minifig became a mascot instead of a POV/action carrier.
- It violates Original-Bricks IP rules from `style-dna.md`.
