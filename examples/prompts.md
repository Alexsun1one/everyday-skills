# Example Prompts

Ready-to-use prompts for each skill. Replace `$skill` with a plain instruction (e.g. 「请按
Cover Pop 工作流处理」) on agents that do not use the `$` skill syntax.

## cover-pop / 社交封面

Plan a cover, don't generate yet:

```text
用 $cover-pop 给这个选题规划一张小红书封面：「3 步写出不尬的朋友圈文案」。
先规划，先别生成。给我目标读者、核心承诺、原型、标题、和最终提示词。
```

Generate a big-type cover:

```text
用 $cover-pop 生成一张「大字封面」。
平台：小红书 3:4。
标题主句：「不是你不自律，是目标定错了」。
要求：标题缩略图能读、一个底色一个强调色、不要微商风、不要 emoji 堆。
```

Generate a contrast / 避坑 cover:

```text
用 $cover-pop 生成一张「反差/避坑封面」。
选题：装修最容易踩的坑 vs 正确做法。
标题：「装修踩坑 vs 避坑」。左边 ✗ 错法、右边 ✓ 对法，红绿区分，留白干净。
```

## sticker-set / 表情包套图

Plan a pack:

```text
用 $sticker-set 帮我规划一套表情包：角色是一只圆滚滚的柴犬。
先锁角色 DNA（3-5 个固定特征），再列 8 个聊天场景 + 每张的 ≤6 字配文。先别生成。
```

Generate the model sheet first:

```text
用 $sticker-set 先出这套表情包的角色设定图（model sheet / 表情九宫格），
锁住轮廓、配色、头型、线条和一个标志物。方形 1:1，干净背景，先不要配文。
```

Then derive one sticker:

```text
用 $sticker-set 按上面的设定图，生成「已读不回」这张表情：
同一个柴犬角色，固定特征不变，新姿势 + 表情，配文「人呢」，方形 1:1，干净背景。
```

## quote-cards / 金句·知识卡片

Plan a card:

```text
用 $quote-cards 把这句话做成金句卡：「自律不是逼自己，是减少需要做选择的次数。」
先跑收藏测试：一个值得收藏的 idea 吗？给我层级（一眼先看到什么）、版式、配色，再给最终提示词。
```

Generate a tip-list card:

```text
用 $quote-cards 生成一张「干货清单卡」。
标题：「写封面标题的 5 个公式」。5 个短点，编号清楚，左对齐，一个强调色，留白大，
不要做成 PPT，不要平权项目符号。方形 1:1。
```

Generate a data card:

```text
用 $quote-cards 生成一张「数据卡」。
主角是一个大数字：「90%」，下面一行语境「的封面输在标题，而不是配图」，角落一行小来源。
克制配色、强层级、大留白。
```

## rank-cards / 排名·段位卡

Plan a ranking card:

```text
用 $rank-cards 做一张「历史最强后卫段位卡」。
先规划：定范围（现役/历史、只排中后卫）、排名依据（巅峰统治力）、tier 系统、人选分档、版式、头像 pipeline。先别生成。
```

Generate a podium cover:

```text
用 $rank-cards 生成一张领奖台版式的 GOAT 排名卡（封面，3:4）。
依据印在卡上：「按历史地位 · 仅限现役」。所有头像走同一 pipeline：统一胸像裁切、同一深色渐变底、统一双色调、同框线。
3-4 档，暖→冷配色，顶档只放 1-2 人，名字大且清楚。
```

Generalize to another domain (writers):

```text
用 $rank-cards 做一张「世界文学大师段位卡」。
适配：头像统一成同一种画风（全油画质感或全黑白调，别混），依据用「影响力/开创性/流传度」而不是奖项，道具用代表作书名。
档位：神/大师/名家。范围印在卡上。
```

## master-styles / 大师视觉语言

Elevate a cover:

```text
用 $master-styles 把一张「咖啡品牌封面」做高级，要优雅感。
先规划：给我结构 token（来自哪位大师/是什么）、配色·光 token（来自哪位）、一条共同克制原则、反套皮检查，再给最终提示词。不要复制任何名作。
```

Blend two masters (structure + palette/light):

```text
用 $master-styles 生成一张安静电影感的读书类封面。
混搭：结构用 Hopper 的低角度斜射光 + 长硬阴影；负空间用原研哉的大留白；共同克制：不要环境杂物、不要装饰。
主题是「深夜读书的书桌」。主题要当主角，别被风格盖过。
```

Use as an aesthetic engine over rank-cards:

```text
先用 $rank-cards 规划这张球星排名卡，再用 $master-styles 叠艺术指导：
肖像用 Platon 式紧贴虚空（紧裁、镜头正上方蝶光、中性虚空底）+ 布局用瑞士网格。克制：不要环境、不要装饰。
套到排名卡的头像 pipeline 和网格上。不要模仿 Platon 任何一张真实照片。
```

## Fixing mangled Chinese text

For any skill, when the image looks right but the text is wrong:

```text
重新渲染图里的文字为：「{正确文字}」。
干净正确的中文字形，不要糊、不要重影、不要乱码。保持构图不变。
如果清晰中文实在渲染不出来，就把文字区域留空，我自己在编辑器里叠字。
```
