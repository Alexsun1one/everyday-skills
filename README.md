# Everyday Skills / 普通人也能用的 Agent 技能

> 一套面向普通人的 Agent 视觉技能：不靠设计师，也能做出能发布的封面、表情包、知识卡片。

[English](README.en.md)

Everyday Skills 是一组可安装、可开源、跨 Agent 的「技能包」。每一个技能都不是滤镜或模板，而是一套**严谨的工作流**：先判断该不该做，再把模糊的想法逼成清晰的方案，最后交给图像模型生成一张能直接发布的图。

它继承自 [Paper Operators / 纸片人](../skillsdesign) 的方法论——**用一套严格的技能骨架，把一件普通人做不好的事，做到可发布质量**——但每个技能有自己的视觉身份和质量标准。

## 共享的工作流 DNA

每个技能都长着同一副骨架：

1. **决策闸门**：先问「这张图到底该不该做、为谁做」。挡掉空心的、凑数的、装饰性的输出。
2. **结构化规划契约**：把意图拆成目标读者、核心承诺、原型、层级……最后落到一句最终提示词。
3. **按题材自动路由审美**：每个技能读懂题材后**自动**选对的视觉调性（诗人→水墨、球星→运动卡、国学卡→书法、知识→瑞士网格），把 [`master-styles`](master-styles/) 这个**共享审美引擎**的可迁移 token 套到内容上。用户**不需要报风格名**，master-styles 也**不是一个让用户单独调用的 skill**，而是被各技能自动调用的引擎。
4. **Style DNA + 反模板规则**：明确写出「不要做成什么」（微商风、PPT、土味、AI 塑料感），这是质量护城河。
5. **QA 验收清单**：明确的 accept / regenerate / repair，做不到就重做。

换工具不换方法：Codex、Claude Code、Cursor、Hermes Agent、OpenClaw 都能用同一套规则，只要它能遵循普通 Markdown 指令。

## 技能清单

**日常线**——普通人高频、上手即用：

| 技能 | 中文名 | 干的活 | 适合谁 |
| --- | --- | --- | --- |
| [`cover-pop`](cover-pop/) | 社交封面 | 小红书 / 公众号 / 视频 / 朋友圈封面，主打「被点开」 | 所有发内容的人 |
| [`sticker-set`](sticker-set/) | 表情包套图 | 一个原创角色一整套表情，带中文梗 | 想做自己表情包的人 |
| [`quote-cards`](quote-cards/) | 金句 / 知识卡片 | 把一句话、一条干货变成可收藏的排版卡 | 做知识分享、读书笔记的人 |

**高级线**——更强的 harness，做出"设计师级"的东西：

| 技能 | 中文名 | 干的活 | 适合谁 |
| --- | --- | --- | --- |
| [`rank-cards`](rank-cards/) | 排名 / 段位卡 | 球星历史地位、GOAT 金字塔、Top N 段位卡（通用到作家/音乐家/导演） | 做排名盘点、发视频号的人 |
| [`gif-stickers`](gif-stickers/) | 动图表情包 | 把照片/头像或一个主题做成会动的 GIF 表情：A 生成几帧叠成动图、B 照片+动态文字（确定性渲染，已实测） | 想做会动的表情/主题套图的人 |
| [`master-styles`](master-styles/) | 大师视觉语言 | 提取世界顶级艺术家的可迁移视觉 token，让任何图变"高级"；可叠在其他 skill 上当审美引擎 | 想要高级感 / 设计师级视觉的人 |

每个技能都是自包含的：`SKILL.md` + `references/` + 自己的 `README.md`，可以单独拎出去开源。

### cover-pop — 社交封面

封面只有一个任务：让对的人停下来点进去。它帮你想清楚「谁在刷、为什么停、点进来得到什么」，再写出缩略图能读的标题，做成不土不微商的封面。决策闸门叫**停下测试**。

### sticker-set — 表情包套图

一套表情的难点是：所有图得像同一个角色（一致性），且每张都对应一个真实的聊天瞬间（有用）。它用「先出角色设定图、再派生每张表情」的方法锁住一致性，决策闸门叫**聊天场景测试**。

### quote-cards — 金句 / 知识卡片

卡片是给人收藏转发的，不是来骗点击的。质量全在排版：一个主信息、清楚的层级、克制的留白——而不是塞满的 PPT 或微商海报。决策闸门叫**收藏测试**。

### rank-cards — 排名 / 段位卡

视频号上很火的球星段位卡那类。它不是普通生图，是一套排版 + 选图 harness：所有头像走**同一条 pipeline**（同裁切/同底/同双色调/同描边，像一个摄影师同一天拍的），排名**依据和范围印在卡上**（把暴论变判断）。同一套 harness 通用——足球、篮球、作家、音乐家只换三个适配项。决策闸门叫**排名成立测试**。

### master-styles — 大师视觉语言（审美引擎）

让任何图变"高级"的引擎。不画大师名作，而是把世界顶级艺术家**遵守的规则**拆成可迁移 token（配色逻辑、构图、负空间、光、克制原则），混一两个套到你的内容上。25 位大师只提取**可迁移的视觉规则**并标注反套皮迁移、人工校对了易混淆的流派归属（如 Favre 属 Pop/Op 而非 Art Deco），非生平考据。可单独用，也可**叠在其他 skill 上**当艺术指导。决策闸门叫**token 迁移测试**（反套皮）。

## 快速开始

### Codex

把任意一个技能目录复制进 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R cover-pop ~/.codex/skills/cover-pop
```

重启后调用：

```text
用 $cover-pop 给这个选题做一张小红书封面：「3 步写出不尬的朋友圈文案」。先规划，先别生成。
```

### 其他 Agent（Claude Code / Cursor / Hermes / OpenClaw）

不需要 Codex Skill 格式。把对应技能的 `SKILL.md` 和 `references/` 当作项目指令 / 规则 / workflow prompt 贴入即可。接入细节见 [`agent-guides/README.md`](agent-guides/README.md)，更多示例见 [`examples/prompts.md`](examples/prompts.md)。

注意：跨 Agent 复用的是「规划 + 提示词 + QA」工作流；最终成图质量取决于图像模型，尤其是中文文字的渲染。文字渲染不干净时，按各技能 `prompt-template.md` 里的 text-fix 流程修，或先留空文字框、再在编辑器里叠字。

## 仓库结构

```text
everyday-skills/
├── README.md
├── README.en.md
├── LICENSE
├── NOTICE.md
├── agent-guides/
│   └── README.md
├── examples/
│   └── prompts.md
├── cover-pop/         # 社交封面
├── sticker-set/       # 表情包套图
├── quote-cards/       # 金句 / 知识卡片
├── rank-cards/        # 排名 / 段位卡
└── master-styles/     # 大师视觉语言（审美引擎）

每个技能目录都是 SKILL.md + README.md + references/ 的自包含结构。
```

## 后续

这套技能会陆续增补、陆续开源。更完整的拆解、提示词和实践复盘，会写在公众号「正在逐渐AI化」。如果你也关心怎么让 AI 图不再像模板、怎么把普通人做不好的事做成可复用的工作流，欢迎关注。

## License

MIT. 见 [`LICENSE`](LICENSE)。
