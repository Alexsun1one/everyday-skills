# Master Styles / 大师视觉语言

> 让任何一张图变"高级"：把世界顶级艺术家/设计师的视觉拆成可迁移的 token，套到你自己的内容上——不是浅薄的「in the style of 某某」套皮。

Master Styles 是这套技能里的**审美引擎**。它面向所有想让图"看起来像真设计师做的、像杂志封面、像画廊作品"的人。它不画某位大师的名作，而是借用大师**遵守的规则**，用到你自己的主题上。

一个大师真正被记住的是**规则**，不是那张画。Müller-Brockmann 的签名是"一切都吸附到数学网格"，不是他的音乐会海报；Noma Bar 的签名是"空白处自己拼出第二个真实图像"，不是那张枪脸；Platon 的签名是"一张脸是虚空里唯一的事件，光来自镜头正上方"，不是他拍的普京。这个 skill 把这些规则提取成可迁移的 token，混一两个，让主题当主角，拒绝套皮。

## 它解决什么问题

普通人想要"高级感"时常踩两个坑：要么直接 `in the style of 某大师`（结果出一张名作的仿品或一团没结构的"氛围"），要么把六种风格糊在一起变成一锅泥。两种都很廉价。

Master Styles 用三条铁律顶住：

- **提取，不复制**：借方法和克制，绝不复制大师的实际母题/构图/字标。如果你的图让人认出"这是《吻》"而不是"这是把金箔奢华用到一个咖啡品牌上"，就失败了。
- **混 1–2 个 token，不是 6 个**：从一个大师拿**结构**，从另一个拿**配色/光**，再加一条两者都遵守的**克制原则**。多了就是泥。
- **主题永远是主角**：风格服务内容。风格盖过主题，就往回收。

研究是真扒了的：25 位大师（瑞士网格、Cassandre、Saul Bass、Paula Scher、Vignelli、Sagmeister、Malika Favre、Noma Bar、Niemann、Haugomat、Rothko、Mondrian、Hockney、Matisse 剪纸、Klimt、北斋、Hopper、Platon、Irving Penn、Annie Leibovitz、原研哉/MUJI、田中一光、横尾忠则…）。每位只提取**可迁移的视觉规则**（构图/配色/留白/光/克制）+ 反套皮迁移说明，并人工校对了易混淆的流派归属（如 Favre 属 Pop/Op 而非 Art Deco）；这是设计语言提取，不是生平考据。

## 适合谁

适合：想把封面/卡片/插画/海报/肖像做出"高级感、设计师级、编辑级"的人，以及想给其他 skill（封面、卡片、排名卡）叠一层审美的人。

不适合：想复制某大师名作、做 logo、或只要一张大白光写实照片（不需要艺术指导）的场景。

## 工作流

1. 读用户的主题，和要做什么（X 的封面 / Y 的卡片 / Z 的肖像）。
2. 定想要的"感觉"：优雅 / 冲击 / 温暖 / 庄重 / 叙事 / 奢华 / 喧闹。
3. **按你需要的 token 选大师，不是按名气**（见 `references/blending.md`）。
4. 从一个大师拿结构 token，从另一个拿配色/光 token（1–2 个，绝不 6 个）。
5. 定一条两者共同遵守的克制原则。
6. 跑「token 迁移测试」：这是 token 不是戏服吗？避开了名作吗？主题还是主角吗？
7. 读命中大师的 `references/master-library.md` + `references/token-axes.md`。
8. 用 `references/prompt-template.md` 出最终提示词，把 token 套到主题上。
9. 一次生成一张。
10. 用 `references/qa-checklist.md` 验收，复制名作/戏服套皮/糊太多风格/盖过主题就重做。

## 当审美引擎用

Master Styles 能叠在别的 skill 上：先用对应 skill 规划内容（封面、卡片、排名卡），再让 Master Styles 提供艺术指导——比如排名卡用「Platon 式紧贴虚空肖像 + 瑞士网格」，封面用「Hopper 斜射光 + 原研哉留白」。先定内容，再叠一两个 token。

## 安装

### Codex

```bash
mkdir -p ~/.codex/skills
cp -R master-styles ~/.codex/skills/master-styles
```

```text
用 $master-styles 把这张「咖啡品牌封面」做高级：要优雅感。先规划，给我结构 token、配色/光 token、克制原则，再给最终提示词。
```

### 其他 Agent

把 `SKILL.md` 和 `references/` 当项目指令 / 规则 / workflow prompt 贴入即可。核心链路：
`主题 -> 想要的感觉 -> 按 token 选大师 -> 结构 token + 配色/光 token + 克制 -> 套到主题 -> QA`。

注意：跨 Agent 复用的是"提取 token + 套用 + 反套皮"的工作流；最终成图取决于图像模型。

## License

MIT. 见仓库根目录 [`LICENSE`](../LICENSE)。
