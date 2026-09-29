# Worked Examples / 样例(走通 harness)

Three end-to-end plans produced by following `SKILL.md` → Build Test → Output Contract. They show the harness composing across references. Use them as templates; they are plans, not generated images.

---

## Example 1 — 一个好提示词的结构(说明书模式)

**Source:** 把"一个好的提示词由哪几部分组成"讲清楚,给文档配图。

**Build Test**
```text
buildable structure: yes
source anchor: 一个提示词 = 系统设定 + 上下文 + 指令 + 输出格式(+ 可选示例)
domain & tone: AI/prompt;instructional
relationship type: Sequence & Handoff(按顺序拼装)+ Hierarchy(必需/可选)
the parts: 系统底板 / 上下文砖 / 指令梁 / 输出格式片 / (可选)示例砖
how they connect: 在底板上按 1→4 顺序往上扣;示例砖是"可选件",虚搭在侧
the assembled meaning: 提示词是按顺序、由必需+可选零件拼起来的,不是一段话
mode: instruction sheet
minifig: 1 个 Operator/搭建师,正在把"指令梁"扣上去(装配进行中)
what breaks if flattened: bullet list 丢掉"顺序"和"哪些可选",读者以为四块平权
forbidden drift: 体素方块 / 在砖堆上画箭头 / 乐高 logo
```

**Output Contract**
```text
build anchor: 提示词的四步装配 + 一个可选件
reader takeaway: 好提示词是按顺序拼起来的,系统在最底,示例可选
domain & tone: AI/prompt;教学、克制
relationship type: 顺序装配 + 必需/可选层级
the parts (modules): 系统底板 / 上下文砖(米白)/ 指令梁(蓝=核心动作)/ 输出格式片(平滑片=定稿)/ 示例砖(橙=可选,虚搭)
how they connect (stud grammar): 底板承载,逐层往上扣紧;示例砖不扣紧、悬在侧边表示可选
mode: 说明书 Instruction Sheet
build archetype: Conveyor/Step-Stack(编号步骤逐步叠装)
minifig roles: Operator ×1,手持指令梁正往上扣(装配进行中)——加分:显示"在拼",不是已完成
baseplate world / district: prompt assembly bench(浅色工作台)
elements & state coding: 蓝=核心指令(焦点色);露点=还能加(示例槽);盖平滑片=输出已定稿;橙=可选件
composition: 4 个编号步骤面板(横向),每步新件悬在投影连线上;右上角放成品预览缩略图;每步一个零件清单框
labels: 步骤①系统 ②上下文 ③指令 ④输出 + 角标"示例·可选";清单框示意 砖×N(留空印字片,编辑器叠中文)
series plan: (单图)
final image prompt: 见 prompt-template.md 的 Final + Instruction Sheet 附加块,填入以上字段
QA risks: 中文多行→走留空叠字;别让四步看起来平权(用高度/编号强调顺序);别把示例砖画成必需
```

---

## Example 2 — 微服务架构(成品模式 · 服务小镇)

**Source:** 把一套微服务架构画成一座积木小镇,放进架构文档首图。

**Build Test**
```text
buildable structure: yes
source anchor: 网关 → 三个服务 → 共享数据库;鉴权在入口卡口
domain & tone: software/architecture;analytical
relationship type: Dependency(都压在数据库地基上)+ Connection(网关用路连通)+ Boundary(鉴权卡口)
the parts: 网关楼 / 订单服务 / 用户服务 / 库存服务 / 数据库地基板 / 鉴权关卡
how they connect: 三个服务楼都坐在同一块数据库地基板上(依赖);网关用主干道连到各楼(连接);道路入口有一道闸门=鉴权(边界)
the assembled meaning: 三个服务都依赖同一个数据库,流量从带鉴权的网关进来
mode: finished build
minifig: 1 个 Inspector 站在鉴权关卡旁盖章(检查在发生);可选 1 个 Maintainer 在某服务楼旁
what breaks if flattened: 方框箭头图看不出"共享地基"这个隐藏的强依赖
forbidden drift: 漂亮但没路没标签的城市 / 通用 3D 块
```

**Output Contract**
```text
build anchor: 三服务共用一块数据库地基,流量经鉴权网关进入
reader takeaway: 数据库是大家的共同地基,拔掉它整座小镇塌
domain & tone: 软件架构;冷静、专业
relationship type: 依赖(主)+ 连接(次)+ 边界(三)
the parts (modules): 网关楼 / 订单·用户·库存三栋服务楼 / 数据库地基板(灰,承重)/ 鉴权关卡(闸门)
how they connect (stud grammar): 三栋楼叠扣在同一地基板上=依赖;蓝色主干道从网关连到各楼=连接;入口闸门=边界
mode: 成品 Finished Build(影棚级套装照)
build archetype: Baseplate Town + Load-Bearing Foundation Slab
minifig roles: Inspector ×1 在闸门盖"通过"章(检查在发生)
baseplate world / district: service town(服务小镇)
elements & state coding: 蓝=活跃请求主干道(焦点);灰=结构/地基;闸门arm抬起=放行;一栋楼留点空地基槽=可扩展
composition: 一栋焦点楼(网关)略抬高,三服务楼围绕,后排低矮天际线做景深;主干道贯穿;四周留白底板
labels: 网关/订单/用户/库存/数据库/鉴权 印字招牌;路牌标流向
series plan: (单图;若做系列→见下)
final image prompt: 见 prompt-template.md 的 Final Generation Prompt,填入以上字段
QA risks: 别变成漂亮但啥也不解释的城市→强化"共享地基"这个焦点;招牌中文留空叠字
```

**若扩成系列(series-and-chaining):** 空底板(开场)→ 铺数据库地基+连路(展开)→ 加鉴权关卡+故障某服务裂砖(转折)→ 全镇点亮、裂砖被补砖修好(收束)。贯穿轴:Construction;母题:那道鉴权闸门的"通过"章,转折时变"拒绝",收束时回到"通过"。

---

## Example 3 — 一篇好 README 的构成(爆炸图模式 · 非工程域示例)

**Source:** "一篇好的 README 由哪些部分组成",做知识科普配图。

**Build Test**
```text
buildable structure: yes
source anchor: README = 标题 + 一句话简介 + 安装 + 用法示例 + 配置 + 许可证
domain & tone: education/docs;清晰、友好
relationship type: Hierarchy/Containment + 装配顺序(从上到下)
the parts: 标题块 / 简介片 / 安装砖 / 用法示例砖 / 配置砖 / 许可证片
how they connect: 沿一条竖轴爆炸分解,每块悬在自己的卡槽上,虚线连到主体
the assembled meaning: README 是几块"必须有"的标准件按顺序叠成的
mode: exploded view
minifig: none(零件自己说清楚,不需要演员)
what breaks if flattened: 平铺清单看不出"从上到下的阅读顺序"和"哪块是地基(标题)"
forbidden drift: Minecraft 方块 / 把它做成 box art 把零件藏起来
```

**Output Contract**
```text
build anchor: README 六个标准件的竖向爆炸分解
reader takeaway: 一篇合格 README 就是这几块标准件,缺一块就少一块
domain & tone: 文档科普;友好、克制
relationship type: 层级/包含 + 自上而下装配顺序
the parts (modules): 标题块(底,最大)/ 简介片 / 安装砖 / 用法示例砖(绿=最常被用,焦点)/ 配置砖 / 许可证片(顶,小)
how they connect (stud grammar): 沿一条竖轴各就各位悬浮,虚线投影连到装配位;顺序=阅读顺序
mode: 爆炸图 Exploded View
build archetype: Exploded Stack(≤7 模块)
minifig roles: none(理由:零件+标签已足够清楚,加人是装饰)
baseplate world / district: 浅色页面/技术分解图底
elements & state coding: 绿=用法示例(焦点,最常被读);灰=其余标准件;旁边一个半透明"成品 README"幽灵做参照
composition: 六块沿竖轴对齐悬浮,细虚线连到各自卡槽;每块一根引线接印字标签;右侧淡淡的成品幽灵
labels: 标题/简介/安装/用法/配置/许可证 印字片(中文留空叠字)
series plan: (单图)
final image prompt: 见 prompt-template.md 的 Final + Exploded View 附加块
QA risks: 别让零件乱飘→必须对齐+投影连线;≤7 块别超载;别藏进盒子(那是 box art)
```

---

这三例覆盖了三种模式(说明书 / 成品 / 爆炸图)、三种关系主线(顺序装配 / 依赖 / 层级)、有/无小人仔两种情况,以及一个非工程域(README 科普),正好对应 QA 清单里"showcase 至少一张非工程域"的要求。
