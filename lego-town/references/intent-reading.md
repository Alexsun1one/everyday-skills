# Intent Reading / 读心·意图

A request like "把我们系统搭个图"、"做好看点"、"给这个提示词配张图"几乎从不携带真实需求。它是一个**结果**——用户心里有目标、有观众、有情绪，只是没说。本文件在选定 mode、关系、原型之前**先读心**：推断真实 goal、audience、tone，把它们翻译成具体的搭建决策，而不是机械套用一个模板。读完再去翻 `modes.md`、`domain-adaptation.md`、`brick-library.md`、`style-dna.md`。读心失败的标志，就是产出"结构没错但没用"——技术正确、却完全没回答用户真正想做的事。

**工作流位置**：在 SKILL.md 的流程里，读心发生在「读源材料 → 找 build anchor」之后、但「选关系 → 选 mode → 选原型」**之前**。先填第 6 节的 Intent Brief，再带着它去 Build Test。顺序错了——先按结构套出一个 Finished Build——就等于把 mode 决定权让给了"这是个系统"这种与意图无关的信号，于是高管要的是一锤定音的封面、你却交了一张密密麻麻的内部图。**goal 决定 mode，audience 调节密度与配色，tone 调节情绪编码**——三者冲突时，goal 优先级最高，因为它定义"这张图要达成什么"。

## 1. 真实 Goal / 读懂这张图到底想干嘛

绝大多数"搭个图"背后是这八种目标之一。先判别 goal，**goal 决定 mode、决定谁是主角、决定怎么打光**——而不是反过来。

- **impress（惊艳 / 炫一下）** → Box-Art，3/4 戏剧英雄机位，一个 bold focus accent，饱和自信配色，戏剧化的高级打光；hero build 是绝对主角，baseplate 留白大。
- **clarify（讲清楚）** → Instruction Sheet 或干净 Finished Build，clear readable labels，可选一个 Guide 向导指路；优先可读性，弱化炫技。
- **persuade（说服 / 打动）** → Box-Art hero + **那个唯一的核心赌注放上 plinth 底座**（Mayor 镇长站在旁边宣示所有权），自信配色 + 一个 bold accent；让读者一眼相信"这一招成立"。例如一个产品方案：把"靠一个核心模块取胜"做成一台立在 plinth 上的 hero build，其余零件退到背景天际线，accent 只给那一个赌注。
- **reassure（让人放心 / 稳）** → warm tan 暖色调，整齐的、已铺 tile 完工模块（mint-green 完成态），一个 Maintainer 维护员在修补那块 cracked brick；calm 平静表情；传达"已搞定 / 在掌控"。例如上线前的稳态图：管线整体 tidy 完工、铺满 tile，唯独一处 cracked 砖正被 Maintainer 拧扳手修着——画面在说"问题已知、在修"，而不是"一切完美"。
- **teach（教会）** → Instruction Sheet + Guide 向导 + 编号步骤 + 学习路径的 learning road；友好配色；每步只加一组零件，让读者跟着搭一遍。例如一个 prompt 教学：Step 1 放 System 底板，Step 2 卡上 Context 砖，Step 3 加 Instruction 梁，Step 4 盖 Format tile——读者看到的是"按顺序拼"，不是一张成品照片。
- **document（存档 / 记录）** → 干净 Finished Build，精确 labels，**不用小人仔**（避免拟人化干扰中立性），neutral gray/tan + 克制语义色，均匀无戏剧光；像一张可被引用的官方图。
- **sell（卖 / 营销）** → Box-Art + spec strip 规格条 + 核心益处 hero 立于 plinth + premium 打光；**original 自有品牌**（见 style-dna 的 Original-Bricks 规则，绝不上 LEGO logo）。
- **explore（探索 / 试一试）** → 小型、松散的 Exploded View 或 Finished Build，模块可随时换位，neutral-to-playful；低承诺、可推翻，鼓励"先搭出来看看"。

判别技巧：看用户的动词与场景。"能不能更吸引人/够不够撑场面"≈ impress 或 sell；"他们看不懂"≈ clarify 或 teach；"老板要拍板"≈ persuade；"我怕上线出事"≈ reassure；"存档/写进文档"≈ document。

## 2. Audience / 给谁看

同一套结构，换观众就换 mode、复杂度、标签密度与配色。**audience 是 mode 的隐形开关**——给高管和给同行工程师是两张完全不同的图。

| Audience | mode | 复杂度 | labels | palette |
| --- | --- | --- | --- | --- |
| execs 高管/老板 | Box-Art 或 Finished Build | 低（1 个焦点模块） | 少，1–3 个大字 | 自信饱和、一个 bold accent |
| engineers 工程师/同行 | Finished Build 或 Exploded View | 高（多模块、真实依赖） | 密、精确、术语全 | neutral gray + tan，语义色克制 |
| students 学生/新手 | Instruction Sheet | 低–中，分步骤 | 编号 + 短词 + Guide 指路 | 友好明快，别用全灰 |
| customers 客户/买家 | Box-Art | 低 | hero 益处 + 一行 | 暖、自信、premium |
| the user themselves 自己备忘 | 小 Finished Build | 中 | 精确够用即可 | neutral |
| a public post 推/圈/公众号 | Box-Art 或戏剧 Finished Build | 中（缩略图要立得住） | 极少、极大字 | 高对比 + 一个 dominant accent |

## 3. Tone & Emotional Register / 读情绪

用户用词的语气本身就是设计参数——**情绪直接驱动配色、小人仔表情、信息密度**（表情编码见 `style-dna.md` 的 Minifig Rules）。

- **urgent 急** → 一个 risk-coral 珊瑚警示 accent，strained 用力表情，极简、单一信息，**别过度装饰**，让读者最快抓到那一句。
- **proud 得意 / 自豪** → Box-Art hero，自信配色，核心模块立 plinth，Mayor 宣示，premium 打光，satisfied 满足微表情。
- **anxious 焦虑 / 担心** → 走 reassure：warm tan，整齐 mint-green 完工模块，Maintainer 在修 cracked brick，calm 平静表情——图本身就是安抚。
- **playful 好玩 / 有趣** → 明亮饱和配色，小人仔在做动作（不止站着），Instruction Sheet 也带点个性与节奏。
- **rigorous 严谨** → neutral gray/tan，精确 labels，**无小人仔或仅一个 Inspector 质检员**，均匀无戏剧光，Finished Build / Exploded View。

## 4. Ask vs Infer / 什么时候开口问

默认 **INFER（推断后直接做，并明说假设，让用户低成本纠正）**。只有当猜错的代价**昂贵且不可逆**时才 ASK，且只问 1–2 个尖锐问题。bar 很高——多数时候推断 + 阐明假设，比连珠提问更专业。

- **ASK（猜错就全废）**：观众会**整体翻转 mode**——"这是内部技术存档还是对外营销封面？"（document vs sell/persuade，两张完全不同的图）。
- **ASK**：Box-Art 的 hero banner **精确文案**必须对——这是会印在图上的字，错了难修。
- **ASK**：交付给客户/董事会的 deadline 场景，且语气必须安全——确认 tone 与受众再动手。
- **INFER（直接做 + 明说）**："做好看点" → 推断 impress，上 Box-Art 戏剧英雄机位，明说"我按'惊艳'做了，若要'严谨存档'说一声"。
- **INFER**："搭个图" + 结构清楚 → 推断 clarify，上 Finished Build + 清晰 labels，直接出图。
- **INFER**：形容词如"高级" → 套用下方形容词表，明说所选的配色与 accent。

## 5. 模糊形容词 → 具体积木决策

中文形容词是用户最常给的全部信息。把它们**机械翻译成 palette / density / 小人仔 / mode / 光线 / focus accent**，模糊瞬间变可执行。

| 形容词 | palette | density | 小人仔 | mode | 光线 | focus accent |
| --- | --- | --- | --- | --- | --- | --- |
| 高级 | dark bluish gray + warm tan + 一点金属/金 | 低 | 无 / Mayor 立 plinth | Box-Art / Finished Build | 戏剧 3/4 studio | 一个自信 accent |
| 可爱 | 柔和明黄/粉/浅蓝 | 中 | 一个 warm 日常小人仔 | 小 Finished Build / Instruction Sheet | 柔暖光 | 友好圆弧 accent |
| 专业 | neutral gray/tan + 克制语义色 | 高、精确 | Inspector / Operator | Finished Build / Exploded View | 均匀干净 studio | 精准语义 accent |
| 简洁 | white + light gray + 一色 | 低 | 无 | Finished Build / 单件 Exploded | 明亮均匀 | 单一模块 |
| 有意思 | 饱和原色 | 中–高 | 做动作的小人仔 | Instruction Sheet / Finished Build | 暖光 | 跳脱 accent |
| 干净 | white + tan + light gray | 低–中 | 无 | Finished Build | 明亮干净 | 单一焦点 |
| 有冲击力 | 深底 + 一色高饱和 | 中 | 可选 hero | Box-Art 戏剧 | 强烈侧光 | 一个 dominant accent |
| 温暖 | warm tan + 柔暖原色 | 中 | warm 日常 / Maintainer | 小 Finished Build | 暖柔光 | 暖色 accent |

形容词会叠加也会打架。"高级 + 有冲击力"叠加成 dark bluish gray 深底 + 一个高饱和 accent 的 Box-Art；"简洁 + 温暖"叠加成 white/tan 小 Finished Build + 暖柔光。当两个形容词冲突（如"专业 + 可爱"），**先说的那个通常主导**，另一个只做微调（professional 灰 tan 底 + 一处友好的圆弧 accent），而不是各取一半做出谁都不得罪的无趣图。拿不准时回到第 4 节：先问一句"主要是给谁、在什么场合用"。

## 6. Intent Brief / 动手前先填这张

planner 在进入 Build Test 与 Output Contract **之前**，先填这份 brief。它把读心结果固化成可被验收的承诺，也把"假设"显式写出来供用户低成本否决。

```text
intent brief:
- real goal (impress / clarify / persuade / reassure / teach / document / sell / explore):
- audience:
- tone / emotional register:
- one-line takeaway (读者看完该想什么 / 做什么):
- what success looks like to THIS user:
- assumptions stated (供低成本纠正):
- mode implied:
```

填完 brief，再用它的 goal/audience/tone 喂给 SKILL.md 的 Build Test 与 Output Contract——mode、原型、配色、小人仔都从 brief 顺出，而不是凭手感挑。

## 7. 用户只贴了 artifact，没说话

当用户直接粘一段 prompt / 一篇文档 / 一份 spec，零背景：**从 artifact 自身的体裁推断 goal**，不必追问。

- 系统/架构 spec、README、changelog、API 文档 → **document**（干净 Finished Build / Exploded View，中立、无小人仔、精确 labels）。
- 一个 prompt 的组成 → **teach / clarify**（Instruction Sheet，把 system/context/instruction/format 拆成编号步骤）。
- 一篇 pitch / 商业计划 / 方案 → **persuade**（Box-Art hero，核心赌注立 plinth）。
- 一份教程 / how-to → **teach**（Instruction Sheet + Guide）。
- 一段销售文案 / 落地页 → **sell**（Box-Art + spec strip）。
- 一份探索性草稿 / 头脑风暴 → **explore**（小型松散 Exploded View，可推翻）。

体裁指明 goal，goal 再按本文件其余章节落成具体搭建决策。

## 组合示例 / 读心在实战中长什么样

同一套源结构，**意图不同就是两张完全不同的图**。这就是本文件的全部论点——结构是常量，意图决定变量。

- **A：「把我们这套推荐系统搭个图，下周给老板看，要镇得住场子。」**
  - 字面是"搭个图"；真实 goal = **persuade / impress**（给老板、镇场子）；audience = **execs**；tone = **proud**。
  - 机械套模板的产出：Finished Build 全模块系统图，密密麻麻——工程师看得懂、老板三秒抓不到重点，镇不住场子。
  - 读心后的产出：**Box-Art**，3/4 戏剧英雄机位，只把"那个核心排序赌注"立 plinth（Mayor 镇长宣示所有权），其余零件退到背景天际线，**一个** bold accent，premium 打光。一张图就回答"你们到底靠什么赢"。
- **B：同一套推荐系统，但用户说「写进技术 wiki，给新人 onboarding 看。」**
  - real goal = **document / teach**；audience = **students / 新工程师**；tone = **rigorous**。
  - 产出：**Instruction Sheet** 或干净 **Exploded View**，精确 labels 把每个模块名写全，neutral gray/tan + 克制语义色，可放一个 Guide 指路，均匀无戏剧光，**无 Mayor、无戏剧机位**。

A 与 B 的零件库可以一样，但 mode、焦点、配色、小人仔、打光完全相反。**先读心，再选 mode**——否则你只是把同一个模板盖在不同的需求上。

## Accept / Regenerate

Accept：plan 体现了一个**被推断出来的真实 goal + audience + tone**；假设被显式 stated；mode、配色、小人仔、密度都从这份意图顺出，而不是套模板；模糊形容词已被翻译成具体积木决策。

Regenerate：机械套模板、没读心（结构技术上对、却没回答用户真正想做的事）；或推断很便宜却过度追问用户（该 INFER 时连珠 ASK）；或观众/情绪明显翻转了 mode 却没察觉。
