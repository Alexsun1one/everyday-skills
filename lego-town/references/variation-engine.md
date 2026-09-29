# Variation Engine / 变化引擎

同一请求跑两次，不该像同一张照片的轻微调色——读者应感到「换了一版搭建取景」，却仍能三秒内读出同一结构。本文件解决「每张图都长得一样」的僵化感：**语义不变，表面自由**。与 `connection-grammar.md`、`state-coding.md`、`modes.md`、`style-dna.md` 配合；写最终 image prompt 前，为同一 build anchor 分配可见差异。

## 核心原则：语义不变，表面自由

| Invariants（永不漂移） | Free variables（必须变化） |
| --- | --- |
| **relationship type** + **connection grammar**（stack / row / wall / gear / seesaw / fork / bridge） | **机位与高度**：3/4 hero、俯视、低角仰拍 |
| **focal module** 及其结构角色 | **baseplate 布局**：街区排列、道路走向、留白区位置 |
| 各 **label** 的 **含义**（语言可换，语义不可改） | **focus accent 轮换**（黄/蓝/绿/橙择一，见 `state-coding.md`） |
| 所选 **mode** 工种及签名要素（成品/说明书/爆炸图/盒面） | **minifig** 0–3、姿态、角色道具（须过 Minifig Test） |
| **state-coding**：露点=待建、盖片=完成、透明=活信号、裂砖=失败 | **道具密度**、背景天际线高低 |
| **Build Test** 的 parts 清单与 stud grammar | **光照/时段/季节天气** |
| **Original-Bricks**（无 LEGO® logo、授权角色、真实套装） | **搭建粒度**：chunky 粗块 vs fine 细砖（模块边界不变） |
| 读者 **takeaway** 一句话 | **画幅/裁切**、**砖面年代感**、**ground/sweep** |

**硬规则**：free variables 再怎么摆，换成「一根箭头」后关系仍须成立；变体之间 **≥3 条 free axes** 必须不同，否则不算新图。

**何时启用**：用户未要求变体时，首次生成仍用 seed index=0 取默认组合；说「再来一张」「换一版」或同一 anchor 要配图组时，index 递增并强制拉开 axes。Instruction Sheet 变体可换 panel 排布（横/竖格），但 step 编号与 parts call-out 含义不动。

---

## 变化轴（旋钮）与砖面选项

每条轴写明**可摆动幅度**——超过则伤义。

| 轴 | 砖面选项 | 可摆动边界 |
| --- | --- | --- |
| **机位** | 3/4 hero（略俯 15–25°，焦点占 40–55%）；top-down 俯视路网；low-angle 仰拍承重塔/闸门/跷跷板 | 不可低到看不见 stack 层数；俯视时焦点仍须最大最亮 |
| **Baseplate 布局** | 道路横贯/纵贯/L 形；留白区换边；对照类左右 mirror | 模块相对位置不变（谁在上、谁在左）；swapped module 差异点不动 |
| **Focus accent** | 轮换唯一焦点色：黄=注意、蓝=活路由、绿=完成、橙=施工中 | 始终 **一块** 饱和焦点，只换「哪块模块穿色」 |
| **Minifig** | 0=静态 dependency 塔/爆炸解剖；1=builder 半搭/inspector 闸口/courier 接力；2–3=handoff 或双端 tug anchor | 禁止 waving 吉祥物；人数变但 **角色职能** 须仍服务同一 relation |
| **道具/天际线** | 中景路标/花坛 ±30%；背景低砖天际线 无/低/中 三档 | 不得遮挡 label 与 fork 判据砖 |
| **光照/天气** | studio 默认；golden hour 暖侧光；overcast 低对比；细雪顶/透明雨感仅氛围 | state 色偏须仍可辨；pass/fail 编码不因天气改义 |
| **粒度** | chunky：2×4/4×4 模块体；fine：1×1/plate 层理缘 | 模块数量与连接类型不变 |
| **画幅/裁切** | 16:9 默认；1:1/4:5；近景或全景 | 须仍见全连接路径（整段 road/stack/gear train） |
| **砖面/地面** | 新 ABS 高光 vs 微磨损哑光；白 sweep / 灰 baseplate 网格 / tan 生活底板 | 禁 voxel；抬高=活跃 的标高语义不变 |

---

## Variation Seed / 变化种子

**目的**：同一 request 重跑时 **确定性地不同**。

```text
seed = hash(request_text + canonical_build_summary) + iteration_index
```

`canonical_build_summary` = relationship + mode + parts + stud grammar 一句（不含 free axes）。`iteration_index`：首次 = 0，「换一版」= 1，「再来一张」= 2…

**映射**（对 seed 取模）：

| seed % N | 映射 |
| --- | --- |
| % 3 | camera：0=3/4，1=top-down，2=low-angle |
| % 4 | accent：0=黄，1=蓝，2=绿，3=橙 |
| % 3 | minifig：0=0，1=1，2=2（关系需要才用 2–3） |
| % 4 | light：0=studio，1=golden，2=overcast，3=instruction-flat |
| % 3 | granularity：0=default，1=chunky，2=fine |
| % 2 | layout mirror：0=default，1=左右对调（仅 contrast/split 类） |

### Worked Example / 算例

**Request**：「RAG 流水线：检索 → 重排 → 生成，依赖共享向量库底座。」

**Canonical**：`Sequence & Handoff | Instruction Sheet | [检索][重排][生成] on foundation slab | row + numbered stations`

| | Run A（index=0） | Run B（index=1） |
| --- | --- | --- |
| camera | 3/4 hero | top-down |
| accent | 黄 on 重排站 | 蓝 on 活路由 |
| minifig | 1 courier | 0 |
| light | studio | golden hour |
| granularity | default | fine（站台 1×2 plate 缘） |
| layout | 道路左→右 | 道路下→上（顺序不变） |

两图 **看起来** 像两次搭建取景；**教会** 同一顺序交接与共享地基——label「检索/重排/生成/向量库」含义不变，mode 仍为说明书 numbered steps。

> **实测验证（落差最大的 free axis）：** 真实出图证明，用户要「完全换一版」时，**整体更换原生元素世界**（工厂传送带 ↔ 水乡船闸／铁路道岔，见 `native-elements.md`、`creative-divergence.md`）是反差最大的一招——同样的 1/2/3 编号站、同样「检索／重排／生成」印字砖、同样「向量库」地基，一版是 3/4 机位蓝焦点传送带工厂，一版是俯视黄焦点水闸水乡，肉眼像两件作品却讲同一结构。要最强反同质，优先换世界（再叠机位／焦点／小人仔），而非只换 hue／zoom。

---

## 「换 N 版 / 再来一张不一样的」工作流

触发词：`换一版`、`再来一张`、`give me N variations`、`同结构不同画面`。

1. **冻结 invariants**：relationship、mode、focal module、parts、labels 含义、state-coding。
2. **分配 seed**（index 0…N−1），映射 ≥3 free axes；手动时列出「本版变了哪三条」。
3. **写 N 份 image prompt**，首部 `variation: k/N | changed axes: …`。
4. **互相对照**：任意两版 focal、grammar、label 语义、mode **完全一致**；可见差异 ≥3 轴。
5. 系列链中变体仅作「同一步平行配图」，不破坏 progression。

**禁止**：借变体改关系（dependency→sequence）、改 label 义、instruction 改成品却称「只换色」。

---

## Anti-Sameness Checklist / 反雷同清单

**Fail — 假变体**：仅 hue/zoom/sweep 灰度微调，机位/布局/minifig/光照/粒度全同；像同图滤镜或 prompt 复制粘贴。

**Fail — 伤义变体**：focal 换位改 takeaway；stack 变 arrow-pile；fork 判据砖消失；双 focus accent；去掉 foundation slab；LEGO® logo/授权脸/真实套装。

**Pass — 真变体**：闭眼轮廓不同（俯视 vs 低角、有无 courier、道路走向不同）；三秒测试 takeaway 同句可复述；`qa-checklist.md` invariants 仍过；mode 签名要素仍在（说明书仍有 numbered steps + call-out box，爆炸图仍有对齐 float + drop-line）。

**快检口诀**：`同义？` → invariants 逐条勾；`不同？` → 至少三轴可点名；`仍像乐高小镇？` → studs、ABS、Original-Bricks，非 voxel 非箭头图。

---

## 读者心理 / Why Variety

配图读者会 **扫读疲劳**。若张张都是「灰底 + 3/4 黄焦点 + 左侧道路」，结构再对也像模板。变化引擎 **刷新注意力**，同时 **零成本复习** 同一关系——variety 是糖衣，semantics 是药，**绝不为糖改药方**。要「统一系列感」时缩小摆动（只换 accent 与机位），仍须避免像素级克隆。

---

## Accept / Regenerate

**Accept**：与另一版 **肉眼可见不同**（≥3 free axes）；**语义完全一致**（relationship、grammar、focal、label 义、mode、state-coding 未漂移）；仍过 Build Test / Minifig Test；符合 `style-dna.md` 与 Original-Bricks；**唯一** focus accent；prompt 写明 `changed axes` 可溯 seed。

**Regenerate**：

- 两张输出仅 trivial 差异（同机位同布局同角色，像重复曝光）。
- 「变体」改了关系、标签义、模式，或弄丢连接几何（箭头化、模块换位改义）。
- 为变化引入 voxel 感、授权元素、双焦点、或 decorative minifig。
- 变化后三秒读不出原结构，或 takeaway 需改口才能成立。
