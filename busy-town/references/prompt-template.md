# Prompt Template / 提示词模板

Planning template, final generation template, and an image-edit template. Use these after walking the workflow in `SKILL.md` and filling the Intent Brief + Collaboration Test.

## 1. Planning Template (returned before generation)

Return this in the user's language before generating any image. It is the output contract from `SKILL.md`.

```text
cooperation anchor:
reader takeaway:
domain & tone:
relationship type:
the roles (animal jobs):
how they cooperate (handoff grammar):
mode (panorama / cutaway / two-page / close-up):
lead animal (or none, with reason):
town world / district:
elements & state coding:
composition:
labels (shop signs / banners / flags / livery; 3-6 simple, more when roles/steps/groups need them):
series plan (only when planning more than one image):
final image prompt:
QA risks:
```

## 2. Final Image Prompt Template

The final prompt handed to the image model. Structure it in this order so nothing important gets dropped. Keep it in the user's language (Chinese by default).

```text
[EDIUM] 手绘水彩 / 水粉绘本插画，温暖米白纸张纹理，柔和湿画法晕染，淡淡的铅笔/墨水底稿透出来，笔触可见，手作的不完美感。

[SCENE — from the chosen mode]
全景镇：从正上方俯瞰一整座小镇，无透视消失点，百科全书式均衡布局，每个街区/街道/广场都在同时运转，到处都有动物在干活，一艘热气球漂浮在小镇上方作为俯瞰标志。
剖面楼：一栋多层建筑从正面剖开，露出每一层楼和每一扇窗，每层一个工位、一只动物在干活，楼层之间有梯子/管道/滑槽/升降机相连，可见内部管线和货架。
对照页：左右两页画同一座小镇，布局完全相同，只有协作状态/密度不同，一条河/一条主街穿过中缝把两页连成同一个世界，每页上方一道横幅标注（旧做法/新做法）。
职业特写：一只动物占画面主体，正在做它的活计，周围呈放射状或网格状摊开它的工具和产出，每件工具带手写标签，背景是一间简化工坊或街角，不是完整小镇。

[COOPERATION — the relationship, rendered physically]
{relationship rendered as character cooperation: 动物沿主街排成一道工序 / 两只动物在交接一个包裹 / 岔口有守卫在分流车辆 / 广场上司秤员在称量两只写明标签的木箱 / 一栋塔楼每层一个工位 / 闸口检查员在盖章放行或退货 / ……}。
角色之间的协作本身就是关系，不要在镇子上画箭头；街道布局和角色的动作承担含义。

[CAST — 3-7 lead animals, vary species]
{列出每只动物：种属 + 职业 + 行头 + 动作 + 表情}。例如：一只穿绿围裙的熊面包师在揉面（皱眉用力的表情）；一只背挎包的猫邮递员蹬自行车送信（轻松的表情）；一只戴绿眼罩的獾审计员在翻账本（专注的表情）。
背景再点缀若干匿名镇民（不同种属，各忙各的）。
所有角色都是原创的，不是任何绘本原作里的具名角色；圆胖友好比例，简笔表情，绝不写实、绝不恐怖谷。

[TOWN WORLD — domain-appropriate]
{镇子类型 + 街区 + 载具 + 道具}。例如：磨坊河边镇，主街一排工坊，磨坊水车在转，码头有船卸货，板车在工坊间运麻袋。

[STATE CODING — 1-2 channels max]
{状态编码}：烟囱冒烟=正在运转；屋顶红旗=告警/受阻；屋顶绿格旗=完成/出货；打瞌睡的助手=等上游交货；闸口盖章=通过/退货；单一金色铃铛=这一站是焦点。

[LABELS — hand-painted, 3-6 short, in user's language]
{每块招牌/横幅/三角旗/篷布字/车身字/木箱印章/楼层牌/路牌上的具体文字}。中文标签每条 2-6 字，手写体，贴在物件上，不要漂浮文字，不要乱码假字。

[COMPOSITION]
16:9 横图（默认）/ 1:1 或 4:5（卡片或对照页时）。
一个焦点的协作区，周围是丰盛但克制的忙碌细节，前景动作 + 中景铺子 + 远景天际线，三层景深。
配色：砖红、芥末黄、鼠尾草绿、灰蓝、陶土红、米白、暖棕木，外加一两个语义点缀色（红/绿/金）。

[HARD NEGATIVES]
不要 3D 渲染、不要扁平矢量卡通、不要黏土/橡皮泥、不要体素/Minecraft 方块、不要 AI 高光过度插画、不要等距低多边形游戏风、不要可爱吉祥物贴纸。
不要任何绘本原作里的具名角色（不画 Huckle / Sally / Lowly 虫 / Mr. Frumble / Bananas Gorilla / Sergeant Murphy 等）或其标志造型。
不要 PPT 流程图图标、不要 UI 仪表盘徽章/进度条/KPI 瓦片、不要漂浮界面文字、不要乱码假中文、不要彩虹配色堆砌、不要动物对着镜头挥手卖萌。
动物不是装饰：如果把它拿掉不影响关系，就不要画。
```

Fill the `{...}` placeholders from the Collaboration Test output. Keep the HARD NEGATIVES block — it is what keeps the medium honest.

## 3. Variation Prompt (when the user asks 换一版 / 再来一张)

Keep the cooperation, roles, focal zone, labels, mode, and state semantics **identical**. Rotate 3–4 surface axes. Append to the final prompt:

```text
变体（语义不变，表面轮换）：
- 机位：{新机位，如 从南侧低空斜俯瞰}
- 镇子布局：{新布局，如 围绕中央广场的网格，主街从西向东}
- 主角种属：{同职业换种属，如 熊面包师 → 猪面包师}
- 天气/时间：{新天气/时间，如 柔和的阴天正午}
- 保留：关系、角色协作、焦点区、标签含义、状态编码语义、模式。
```

## 4. Image-Edit Template (when editing an existing image)

When the user gives an existing image to edit, describe the edit as a delta on the same scene:

```text
基于这张图做编辑，不重画整图：
- 保留：{镇子世界、角色、协作结构、焦点区、招牌文字、状态编码}。
- 修改：{具体改动，如 把右上角面包房的烟囱改成冒烟；把横幅文字从「加工」改成「烘焙」}。
- 不改：关系、协作、模式、整体构图。
说明改动是否需要外部叠字（招牌文字糊时建议留空招牌后期叠字）。
```

## Label-Rendering Notes

- For Chinese labels, the model often blurs characters. When labels must be crisp, use the **"留空招牌 + 编辑器叠字"** path: prompt for hand-painted blank signboards / banners / flags of the right shape and size in the right places, and overlay the text in post.
- If the user did not ask for editable text, attempt native rendered labels first (shorter labels render better); note any text that may need manual overlay in the output contract.
- Prefer 2–6 character Chinese labels; longer labels render worse.

## Anti-Patterns in Prompts

- Starting the prompt with style adjectives before staking the cooperation — cooperation comes first.
- Listing every state-coding channel — pick 1–2 (see `state-coding.md`).
- Forgetting the HARD NEGATIVES block — the medium drifts to 3D / flat-vector without it.
- Asking for a named copyrighted character — recast as original (see `style-dna.md`).
- Adding giant arrows — the street and the animals' cooperation do the work.
