# GIF Stickers / 会动的表情包

> 把一个角色、一张照片或一个梗，变成「会动、能直接甩进对话框」的循环动图表情：微信 GIF、LINE 动态贴纸、Telegram / Discord / X 动图。

GIF Stickers 面向所有想做「会动的表情」的普通人——给原创小角色做一套动图、给一个梗加上动起来的大字、用自己的照片做一个动态头像表情。它不是一个动图滤镜，而是一套动态表情工作流：先在「真脸闸门」上诚实地决定要不要动你本人的脸，再选一个对得上聊天瞬间的动作，最后跑脚本把帧编码成一个无缝循环、压得进平台体积、文字清楚的真 GIF。

静态表情是一句回复，动起来的表情是一句带心跳的回复——但前提是循环无缝、文件压得进平台的字节预算、字还清楚。

这是这个 skill 家族里第一个混合型：拼装这一步是字节、不是提示词，所以 agent 要真正**跑脚本**把帧编码成 GIF——纯 Pillow（如果机器上正好有 `gifsicle` 就顺手再压一压），整条流水线里没有任何图像模型。这让它可以自包含、能开源：编码器除了 Pillow 什么都不需要，不调任何托管服务、不依赖你装不上的黑盒二进制。

## 它解决什么问题

普通人做动图表情常掉进几个坑：循环接不上（最后一帧跳回第一帧，一卡一卡）、文件太大发不出去（微信 / Telegram 有字节上限）、文字糊成一团（动起来更看不清），还有最要命的一个——**以为「用我的照片做动图」=「我本人在动」，结果 AI 把五官重画了一遍**。

GIF Stickers 想要另一种状态：

- 循环无缝：最后一帧融回第一帧，cyclic 或 boomerang 来回，不卡顿
- 文件压得进平台预算：发得出去才算做完，超了就降帧 / 缩尺寸重渲，绝不硬压成品
- 文字大、有描边、看得清：cap-height ≥ 画布 38%，描边 ≥ 8px @240px，动起来也清楚
- 一整套看起来是同一个角色：同一个身份块 + 同一个 seed，整套不跑偏
- 对「要不要动你本人的脸」这件事**先说实话**：会改脸就提前讲清楚，不偷偷把你换成「AI 版的你」

一句话判断：如果这个动起来的表情，循环接不上、发不出去、或者它根本没让一个静态图多说出任何东西，那它就还没做完。

## 两种模式（在闸门上二选一，别猜）

这个 skill 有两种模式，每个表情在**真脸闸门**上明确选一个：

- **模式 A — 帧生成动图（frame-gen）。** 生成 2–8 帧一致的主体帧（从一个你自己拥有的主题，或者通过编辑一张参考照片），再拼成循环。适合快速出主题套图和原创角色。**诚实地讲：** 编辑真照片会**改写 / 风格化那张脸**——出来的是一个「像你」的形象，不是保真的你本人。需要**图像生成 + 代码执行**。
- **模式 B — 照片 + 动态文字（photo + kinetic）。** 照片**一像素不动**（逐字节保真），只动叠加上去的文字和廉价的照片运动（Ken-Burns、bounce、果冻、boomerang）。没有任何图像模型碰像素，文字永远清楚。**只需要代码执行**，不需要图像模型。`scripts/kinetic_text.py` 就是端到端干这件事的。

两种模式最后都汇到**同一个接口**——一个零填充帧目录 + 一个小小的 `manifest.json`（这个帧契约写在 `references/render-pipeline.md` 里），交给同一个确定性拼装器 `scripts/assemble.py`。拼装器永远不知道这些帧是图像模型画的还是 Pillow 画的。

## 真脸闸门：这个 skill 的诚实底线

最先跑、在任何外观和帧工作之前——而且答案来自需求本身，不是猜的。它是这个 skill 的招牌闸门，也是整套东西的诚实脊梁，写在 `SKILL.md`（Face-Truth Gate）里，inline 就能查到完整路由逻辑。

核心规则（硬性、按优先级，前面的规则赢、会让后面的规则压根触发不到）：

1. **任何时候表达过「要保留我的脸」——这一票否决一切。** 用户只要在对话里任何位置说过「保留我的脸 / 用我本人 / 别改我长相」，或者把自拍当「我」传上来，规则 1 直接生效，后面的「改脸同意」问题压根问不到。**没有任何图像模型碰像素。** 这是诚实脊梁——一句轻飘飘的「随便改吧」也压不过更早表达过的保脸意图。
2. 主体是纯主题（你自己拥有这个身份）→ 模式 A，循环最干净。
3. 用户照片 / 头像、且**没有**保脸意图 → 在路由去模式 A 之前，**先逐字打印那段诚实告知**，再问那个把代价讲清楚的同意问题。只有一个知情的「接受」才路由到**模式 A（编辑分支）**，封顶 2–3 个动作变体。任何「不接受」、任何犹豫、或者沉默 → 模式 B。
4. 「来一整套 / 16 / 24 / 主题包」→ 模式 A（只有帧生成能便宜地批量出一套）——除非规则 1 已经生效。
5. 真脸有歧义 → **默认模式 B**，并问一句：「要保留你照片里真实的脸，还是可以做成 AI 风格化的你？」拿不准的时候，永远选 B。
6. 既要保真脸、又要一套快速套图 → **拆任务**：保真脸的走 B，套图走 A。绝不逼一次生成同时干两件事。

规则 3 的同意问题，必须在用户回答**之前**就把代价讲成大白话——绝不是软绵绵的一句「可以改吗？」：

```text
要把你的照片做成会动的，AI 会重新合成你的五官（眼睛、颧骨、皮肤都是重画的）——
这不是你本人的脸，是一个「AI 版的你」。动作越大越不像你本人。接受吗？
  接受 → 模式 A（编辑分支，做 AI 风格化的你，封顶 2–3 个动作）
  不接受 / 想保留真脸 → 模式 B（照片一像素不动，只动文字和特效）
```

如果动起来并没有让这个笑点多说出任何东西，就发一张**静态**表情（用 sticker-set）——一张什么都没循环的图，在字节预算下就是死重量。

## 适合谁

适合：想做微信动态表情、LINE / Telegram / Discord 动态贴纸、群聊动图、原创小 IP 动图、给自己照片做动态头像表情的所有人。

不适合：手绘静态表情套图（用 sticker-set）、单张封面（用 cover-pop）、logo、视频剪辑，以及真正的「会说话的头像 / 对口型面部动画」——那个需要视频模型，这个 skill 做不了，它做的是 2–8 帧循环，不是流畅面部动画。

## 工作流

1. 读需求：主体来源、是否要保真脸、交付物、聊天瞬间、目标平台。
2. 跑**真脸闸门**（见上，完整逻辑在 `SKILL.md` 的 Face-Truth Gate），路由到模式 A 还是模式 B——答案来自需求，不是猜的。
3. 按主体气质路由外观（国潮 / 古风 → 水墨，萌宠 → 圆润流行，热血 → bold pop…）进共享的 master-styles tokens——同时喂给模式 A 的提示词和模式 B 的文字配色，让两种模式看起来是一家人（`references/style-routing.md`）。
4. 规划的是**一套**，不是 8 个随机循环：一个身份块 + 固定 seed、一张 set-manifest、一张「聊天瞬间 → 表情」映射、各平台套图数量（见 `references/frame-generation.md` 里的批量 / SET 章节）。
5. 从聊天瞬间为每个表情挑**一个主导动作**（+ ≤1 个叠加层），用 `references/motion-library.md`——是聊天瞬间挑动作，用户永远不用报 preset 名字。
6. 按模式产帧，参 `references/prompt-template.md`：模式 A 走「先定妆图、分叉不串联、固定 seed」；模式 B 走 `scripts/kinetic_text.py`（在纯色底或真照片上叠描边文字 + 廉价照片运动）。
7. 产出帧契约（`out/<name>/frames/f%04d.png` + `manifest.json`，写在 `references/render-pipeline.md` 里）——两种模式产出同一个形状。`kinetic_text.py` 会替你写好这个。
8. 用 `scripts/assemble.py` 确定性拼装：它按排序顺序加载帧、缝合循环、写出一个压好的小 GIF（见下面的「拼装」）。
9. 按平台导出：默认保留透明，或对会丢 alpha 的平台（微信 / X）传 `--flatten RRGGBB`，参 `references/platform-specs.md`。
10. 校验字节——尺寸、大小、fps、帧数、循环——用 `scripts/verify_output.py`，不合规就拒发（见下面的「校验」）。
11. 用 `references/qa-checklist.md` 跑 QA，把失败分流到 接受 / 重生成 / 修复。

## 帧契约（两种模式产出同一个形状）

两种模式都往 `out/<name>/` 里产出**同一个形状**，拼装器只读这个——它永远不知道像素是图像模型还是 Pillow 画的。完整 schema 在 `references/render-pipeline.md`，形状是：

```text
out/<name>/
  frames/f0000.png, f0001.png, ...   # 零填充、尺寸一致、主体配准 ≤3px
  manifest.json:
    {
      "name":          "<name>",
      "mode":          "A" | "B",
      "fps":           25 | 20 | 10 | 5 | 4 | 2,
      "frame_count":   2-8（有效帧；boomerang 之后再展开）,
      "loop_strategy": "cyclic" | "boomerang" | "directional",
      "canvas":        [w, h],          # 正方形，≥240 创作分辨率
      "chat_moment":   "笑死",
      "caption":       "在吗…" | null,
      "platforms":     ["wechat", "line", ...]
    }
```

`scripts/kinetic_text.py` 会替你写好 `frames/f%04d.png` + `manifest.json`（模式 B）。模式 A 则用一小段 inline 的 Pillow 裁切循环（`Image.open(sheet).crop(box).save(...)` 几行就够）把你的定妆图 / 九宫格切成同样的 `frames/f%04d.png` 布局，再手写一份对应的 `manifest.json`——没有单独的切图脚本，几行 Pillow 就解决。

## 拼装（确定性，agent 真跑脚本）

这一步**没有图像模型**。agent 跑 `scripts/assemble.py`——流水线是固定的，只有输入变：

```bash
python3 scripts/assemble.py --in out/xiaosi --flatten FFFFFF --out out/xiaosi/wechat.gif
```

1. **纯 Pillow，不需要 ffmpeg。** `assemble.py` 只用 Pillow 建 GIF；如果机器上正好有 `gifsicle` 就用它再压小一点，但永远不是必需。没有探测工具这一步，也没有 `brew install` 闸门——编码器总是能跑。
2. **帧卫生内建。** `assemble.py` 按排序顺序加载 `frames/f%04d.png`，所以帧顺序和缝合对齐都替你处理好了——你不用手动对齐帧。
3. **透明 vs 纯底。** 省略 `--flatten` 保留透明；对会丢 alpha 的平台（微信、X）传 `--flatten RRGGBB`（例如 `--flatten FFFFFF`），让主体落在干净纯底上，而不是带一圈黑边。
4. **可选 fps 覆盖。** `assemble.py --fps N` 在编码时重新计时，如果你想偏离 manifest 里的 fps。

时序是硬约束：只有 fps ∈ {25, 20, 10, 5, 4, 2} 能整除成整数厘秒；写别的值，播放会漂移。这正好是 `kinetic_text.py --fps` 接受的那些值。

## 动作与默认外观

生成前先读 `references/motion-library.md`。核心 DNA：

- 每个表情**一个主导动作**；其余都是 sub-12% 的点缀；叠加层 ≤1。
- 循环无缝：最后一帧融回第一帧（cyclic，或来回的 boomerang）。`assemble.py` 遵循 manifest 里的 `loop_strategy`。
- 巨大描边文字：cap-height ≥ 画布 38%，描边 ≥ 8px @240px，一圈轮廓；纯色填充、抗锯齿描边。`kinetic_text.py --cap-ratio` 控制 cap-height，`--size 240` 是创作 / 输出边长。
- 动作在前 70%，后 30% 落到一个静止 rest 姿势——那是大家会截图的那一帧（`--preset hold` 就是显式的 settle preset）。
- 文字 ≤5 个词；情绪靠动作扛，不靠段落。
- 正方形画布，主体居中留安全边距，透明或纯底；循环时长 0.6–1.8s；fps 只能是 {25, 20, 10, 5, 4, 2}（GIF delay 是整数厘秒——这是 `kinetic_text.py --fps` 接受的值）。
- 模式 A：整套同一个身份块 + 同一个 seed，每帧只变**恰好一个**元素。
- 模式 B：真照片不动，外观全在文字系统上。用 `kinetic_text.py --font /path/to/bold-CJK.ttf` 给一个粗体中文字体；不给的话脚本会自动探测系统中文字体（STHeiti / Hiragino / PingFang / Noto）。没有随包附带的字体可指——要么传路径，要么让它自动探测。
- 不做癫痫闪烁（WCAG 2.3.1）：每秒 ≤3 次局部辉光，绝不全屏亮度猛砸；严格平台上 FLASH→POP、GLITCH→SHAKE（`flash` / `shake` preset 就是这对安全替换）。
- 绝不伪造成品 GIF：编码器是纯 Pillow，所以它总能跑——但如果缺帧或 manifest 坏了，**停下来说清楚**，而不是发一个坏文件。

## 外观路由（按主体气质自动，两种模式共享）

外观是**按主体气质路由**的，不是手挑，进共享的 master-styles token 引擎，让模式 A 的帧和模式 B 的文字看起来是一家人（`references/style-routing.md`）。国潮 / 古风 / 古装 / 武侠 / 仙侠 / 神兽 → 水墨 / 工笔（宣纸底、朱砂红 + 石青强调、小小印章——文化盖过卖萌）；可爱 / 萌宠 → Zagnoli 圆润流行；hype / 热血 / gaming → bold pop + 速度线；丧 / 摆烂 / 打工人 → 去饱和暗调；高级 / 商务克制 → 减法扁平（sub-12% 动作）。路由**一次**，然后把这个调性锁进身份 DNA。干净的主体禁止堆料——绝不把它们路由到极繁动作。

## 套图设计

一个包是**一套**，不是 8 个随机循环。一致性层锁一次，然后从它派生每一个表情——`references/frame-generation.md` 的批量 / SET 章节讲全了：

- **身份块**（模式 A）：3–5 个固定特征——轮廓、配色（2–4 个固定角色色）、头型、线条粗细、一个标志性小配件——声明**一次**、整套冻结。每帧只变恰好一个元素。
- **固定 seed**（模式 A）：整套一个 seed；同 seed 派生让帧不跑偏。
- **set-manifest：** 每个表情一行——`(label, chat_moment, 那个唯一变的元素, motion_preset, loop_strategy)`。
- **聊天瞬间 → 表情映射：** 每个表情都对得上一个具体聊天瞬间；对不上的砍掉。
- **平台套图数量**是护栏不是建议：微信 16 或 24（全动 **或** 全静，绝不混）；LINE 8 / 16 / 24。不允许的数量直接拒绝。

## 平台与字节预算

这条流水线只出一个容器：GIF，按平台调参。各平台上限和「安全目标」在 `references/platform-specs.md`；你真正会拧的旋钮是 `assemble.py --flatten` 和 `--fps`：

- **微信** — GIF，丢 alpha；用 `--flatten FFFFFF`（纯白底）拼装。套图数量 16 / 24，全动或全静。
- **LINE** — GIF；保留 alpha（省略 `--flatten`）；套图数量 8 / 16 / 24。
- **Telegram / Discord** — GIF；≤256KB 的 emoji 预算通常要更少帧 + 纯 / 透明底 + boomerang。
- **X（Twitter）** — 丢 alpha；用 `--flatten` 拼装，并按无 alpha 设计。
- **generic** — GIF，保留透明（省略 `--flatten`）。

文件超预算时，沿这把梯子往上爬：**重跑 `assemble.py` 降 `--fps`，或用 `kinetic_text.py --size` 缩小尺寸重渲帧**，直到压进平台字节上限——永远**从帧重新编码**，绝不去重压成品 GIF。

## 校验（不合规就拒发）

编码后，agent 对目标平台跑 `scripts/verify_output.py`，**拒绝**不合规的输出——尺寸、字节大小、fps、帧数、循环标志全部要过：

```bash
python3 scripts/verify_output.py --file out/xiaosi/wechat.gif --platform wechat
```

任何一项违规它就非零退出。一个 401KB 或 260×260 的微信 GIF 直接挂；不靠肉眼、不将就发。如果挂在大小上，走字节预算梯子（修复：重跑 `assemble.py` 降 `--fps` / 缩 `--size`，不是重生成）；如果挂在帧数或循环上，在 manifest 里修缝、重新拼装。

## 端到端示例（已测试）

完整可跑的 demo——模式 B，从一张照片到一个校验过的微信 GIF：

```bash
python3 scripts/kinetic_text.py --base photo.png --text 笑死 --preset bounce --frames 12 --fps 10 --size 240 --out out/xiaosi
python3 scripts/assemble.py --in out/xiaosi --flatten FFFFFF --out out/xiaosi/wechat.gif
python3 scripts/verify_output.py --file out/xiaosi/wechat.gif --platform wechat
```

`kinetic_text.py` 接受 `--base PHOTO`（留空给一个纯底）、`--text`、`--preset {pop|bounce|shake|flash|hold}`、`--frames N`、`--fps {25|20|10|5|4|2}`、`--size 240`、`--pos {top|bottom}`、`--loop {cyclic|boomerang|directional}`、`--cap-ratio F`、`--font PATH`、`--out DIR`。完整 demo 和样例输出见 `scripts/README.md`。

样例 GIF 都在 `examples/` 里，是真跑出来的：

- `examples/demo-xiaosi-240.gif` — 模式 B，「笑死」bounce，微信白底。
- `examples/demo-zantong-transparent.gif` — 模式 B，透明底（LINE / generic）。
- `examples/set-wave.gif`、`examples/set-clap.gif`、`examples/set-cheer.gif`、`examples/set-jump.gif` — 一套同角色循环，演示「一套是一套」。

## 安装

### Codex

```bash
mkdir -p ~/.codex/skills
cp -R gif-stickers ~/.codex/skills/gif-stickers
```

重启后：

```text
用 $gif-stickers 把「笑死」做成一个会动的微信表情，照片里的脸别改。先规划，先别生成。
```

### 其他 Agent（Claude Code / Cursor / Hermes / OpenClaw）

不需要 Codex Skill 格式，把 `SKILL.md`、`references/` 和 `scripts/` 当作项目指令 / 规则 / workflow prompt 贴入即可。核心链路是：
`真脸闸门（A/B） -> 按气质路由外观 -> 规划一套 -> 选动作 -> 产帧 -> assemble.py 拼装 -> verify_output.py 校验 -> QA`。

注意：这个 skill 是混合型，拼装和校验是**跑代码**，不是提示词。模式 A 需要**图像生成 + 代码执行**；模式 B 只需要**代码执行**（不碰图像模型）。编码器是**纯 Pillow**——没有 ffmpeg / gifski 依赖要探测，`gifsicle` 只在存在时顺手再压。一个只能出图、不能跑脚本的纯聊天 agent 可以产模式 A 的帧，但跑不了 `assemble.py` 编码 GIF、也批不了套图——它得把 `frames/` + `manifest.json` 交给别处拼装，或者直接说做不了。绝不伪造一个成品动图文件。

## License

MIT. 见仓库根目录 [`LICENSE`](../LICENSE)。
