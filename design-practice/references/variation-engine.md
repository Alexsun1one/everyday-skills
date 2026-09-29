# 变化引擎 — Variation Engine

> 当用户说"给我多几个方案",AI 最容易塌的地方:**5 个方案看起来都是同一个**。同样的 hero、同样的卡片、同样的间距、同样的图标库,只是颜色换一换——这是塑料。
>
> 真正的变化引擎:**语义不变量(Invariants)保住,表面自由轴(Free axes)疯狂变**。这一页冻结怎么从同一个意图,生成 5-8 个**视觉上明显不同、语义上完全一致**的方案。

## 核心原则:Invariants vs Free Axes

### Invariants(语义不变量,绝不能变)

这些是 Intent Brief 冻结的——5 个方案必须完全一致:

```text
- GOAL(转化/激活/留存/生产力/...)
- AUDIENCE(开发者/消费者/企业/...)
- TONE(严肃/可信/温暖/极客/奢华)
- 主要任务(用户要做什么)
- 关键信息层级(什么最重要)
- 必须出现的核心组件(CTA、表单、列表)
- 必须覆盖的状态(loading/empty/error)
- a11y 标准
- 响应式要求
```

### Free Axes(表面自由轴,鼓励疯狂变)

这些可以变——通过组合它们,生成 5-8 个明显不同的方案:

```text
视觉轴(9 条,见下方详解):
1. 布局结构(grid vs block vs split vs asymmetric vs bento)
2. 信息密度(dense tool vs breathing editorial)
3. 视觉重心(top-heavy hero vs centered vs side-led vs bottom-up)
4. 配色策略(单色 / 单 accent / 多 accent / gradient / 暗色 / 浅色)
5. 字体配对(sans only / sans+serif display / serif hero / mono-led)
6. 图标与插画(Lucide line / Phosphor duotone / 自定 / 真实摄影 / 几何抽象)
7. 留白哲学(紧凑 / 标准 / 大呼吸 / 极简留白)
8. 装饰元素(无 / 几何点纹 / mesh gradient / 摄影背景 / 插画背景)
9. 动效气质(克制工程 / 编辑优雅 / 温暖手作 / 极客前沿)

业务轴(5 条,常被忽略但更重要的差异化维度):
10. 任务流顺序(用户先做什么——创建 vs 浏览 vs 邀请 vs 配置)
11. 入口位置(主功能从哪进——顶栏 vs 侧栏 vs 中央 hero vs ⌘K)
12. IA 优先级(信息架构哪个层级先——对象 vs 操作 vs 时间 vs 项目)
13. 默认视图(打开 App 第一眼——空状态引导 vs 最近 vs 推荐 vs 全部)
14. 对象粒度(主对象单位——单个 vs 批量 vs 集合 vs 流)
```

## 9 条变化轴详解

### 1. 布局结构 Layout

| 选项 | 描述 | 适合 |
|---|---|---|
| grid | 标准网格,3-4 列等宽 | dashboard、catalog |
| block | 垂直 block 流(Notion 风)| 文档、笔记 |
| split | 左右对半(文案 + 视觉)| 营销页 hero |
| asymmetric | 7/5 或 5/7 不对称 | 高端、editorial |
| bento | 大小不一的卡片网格(Vercel 风)| feature 展示 |
| single column | 单列居中 | 长文、博客 |
| full-bleed hero | hero 占满首屏 + 下方分段 | 营销落地页 |

### 2. 信息密度 Density

| 选项 | padding | gap | 适合 |
|---|---|---|---|
| dense(tool) | 8-16px | 4-8px | 后台、CRM、项目管理 |
| standard | 16-24px | 12-16px | 通用 SaaS |
| breathing | 24-32px | 24-32px | 营销页、消费者 |
| luxury | 32-48px | 48-80px | 高端品牌、editorial |

### 3. 视觉重心 Weight

| 选项 | 描述 |
|---|---|
| top-heavy | 所有视觉重量在首屏 hero,下方简洁 |
| centered | 内容垂直水平居中,极简对称 |
| side-led | 左侧导航主导,右侧内容 |
| bottom-up | 内容在下,顶部仅 logo + CTA(留白巨大) |
| distributed | 视觉重量均匀分布(常见 dashboard)|

### 4. 配色策略 Color

| 选项 | 描述 |
|---|---|
| monochrome dark | 深色单色 + 一个 accent(Linear/Vercel) |
| monochrome light | 浅色单色 + 一个 accent(Stripe) |
| warm cream | 奶油底 + 多柔和 accent(Notion) |
| gradient hero | hero 用 gradient mesh,其他单色 |
| full color | 多色块分割(少见,复古或大胆品牌)|

### 5. 字体配对 Typography

| 选项 | 描述 |
|---|---|
| sans only | Inter / Geist / sohne-var 一种字体管全部 |
| sans + serif display | sans UI + serif 大标题(editorial) |
| serif hero + sans body | serif 仅 hero,其他 sans |
| mono-led | mono 字体主导(开发者文档) |
| warm sans + serif | Notion 风双字体配对 |

### 6. 图标与插画 Imagery

| 选项 | 描述 |
|---|---|
| Lucide line | 几何线 icon,工程感 |
| Heroicons thin | 1.5px 细线,编辑感 |
| Phosphor duotone | 双层填色,手绘感 |
| 自定 SVG | 几何抽象,品牌定制 |
| 真实摄影 | 真实产品截图或摄影 |
| 抽象几何 | 几何形状装饰(圆/方/线) |
| 手绘插画 | Notion 风、Dropbox 风插画 |

### 7. 留白哲学 Whitespace

| 选项 | 描述 |
|---|---|
| tight | 紧凑,信息密度高 |
| standard | 标准,平衡 |
| breathing | 大量留白,呼吸 |
| luxury | 极简留白,奢华 |

### 8. 装饰元素 Decoration

| 选项 | 描述 |
|---|---|
| none | 无装饰,纯净 |
| geometric grid | 几何点纹或网格背景(Vercel) |
| mesh gradient | mesh gradient halo(Stripe) |
| 摄影背景 | 全屏摄影背景 |
| 插画背景 | 抽象插画装饰 |
| 玻璃毛玻璃 | backdrop-filter blur 毛玻璃卡片 |

### 9. 动效气质 Motion

| 选项 | 描述 |
|---|---|
| controlled engineering | 受控、利落、绝不弹(Linear) |
| editorial elegant | 优雅、慢、有韵律(Stripe) |
| warm handcrafted | 温和、慢、有手(Notion) |
| geek frontier | 快速、克制、几何(Vercel) |

## 业务轴详解(10-14)——常被忽略但更深的差异化

> 视觉轴只换"皮",业务轴换"骨"。同样是任务管理,5 个视觉变体看起来都像"任务管理",但 5 个业务变体看起来是**5 个不同产品**(Trello 强调拖 / Things 强调清单 / Notion 强调 block / Asana 强调时间线 / Linear 强调键盘)。

### 10. 任务流顺序 Task Flow Order

用户进来**先做什么**——同一个产品可以变出 4-5 种入口:

| 选项 | 描述 | 代表产品 |
|---|---|---|
| 先创建 | 进来第一动作就是 + 新建 | Things、Linear |
| 先浏览 | 进来看最近/今天的列表 | Todoist、Microsoft To Do |
| 先邀请 | 进来第一动作是拉团队 | 飞书任务、Notion |
| 先配置 | 进来先设项目/分类/标签 | Asana、ClickUp |
| 先模板 | 进来选模板开始 | Notion 模板库、Coda |

**生成变体时**:
- 变体 A:空状态 + 大 + 按钮(先创建)
- 变体 B:列表 hero(先浏览)
- 变体 C:邀请 modal(先邀请)
- 变体 D:配置向导(先配置)

### 11. 入口位置 Entry Position

主功能从**哪里**进:

| 选项 | 描述 | 适合 |
|---|---|---|
| 顶栏 CTA | 顶栏右侧 [+ 新建] | SaaS 通用 |
| 侧栏首项 | 侧栏第一项就是 [+ 新建] | Linear、Notion |
| 中央 hero CTA | 中央大按钮 | 营销页、空状态 |
| ⌘K command palette | 键盘 ⌘K 触发命令面板 | Linear、Raycast、Vercel |
| 浮动 FAB(右下角)+ | 移动端常见、桌面也有 | 移动 App、小红书 |
| 右键菜单 | 右键触发上下文操作 | 高级工具、Figma |

### 12. IA 优先级 IA Priority

信息架构哪个层级**先**:

| 选项 | 描述 | 代表产品 |
|---|---|---|
| 对象优先 | 先列对象(任务/文档) | Todoist |
| 项目优先 | 先列项目,展开看任务 | Asana、Trello |
| 时间优先 | 先按时间(今天/本周/未来)| Things、Microsoft To Do |
| 人员优先 | 先按人(我的/分配的/团队的)| 飞书 |
| 标签优先 | 先按标签/优先级筛选 | Linear、Jira |

**变体示例**(同一任务管理):
- 变体 A:今天 / 本周 / 全部(时间优先)
- 变体 B:项目 A / 项目 B / 项目 C(项目优先)
- 变体 C:@我 / @他人 / 团队(人员优先)

### 13. 默认视图 Default View

打开 App **第一眼**看到什么:

| 选项 | 描述 | 适合 |
|---|---|---|
| 空状态引导 | 新用户看插画 + CTA | 新产品、新用户 |
| 最近 | 上次操作的延续 | 留存产品 |
| 推荐 | AI 推荐 / 算法 feed | 内容产品(小红书)|
| 全部 | 完整列表 | 工具产品 |
| Today | 今日聚焦 | 日程类 |

### 14. 对象粒度 Object Granularity

主对象的**单位**:

| 选项 | 描述 | 代表产品 |
|---|---|---|
| 单个 | 一次操作一个对象 | Things |
| 批量 | 多选 + 批量操作 | Linear、Excel |
| 集合 | 按集合/项目看 | Notion database |
| 流 | 信息流式 | Twitter、Inbox |

## 业务轴驱动的差异化示例

**用户需求**:任务管理。

```text
变体 A (Trello 系):
  业务轴:任务流=先浏览 + 入口=顶栏 + IA=项目优先 + 默认=看板 + 粒度=单个拖拽
  视觉轴:kanban 布局 + 中等密度 + 色彩缤纷(每列一色)

变体 B (Things 系):
  业务轴:任务流=先创建 + 入口=中央 + IA=时间优先 + 默认=Today + 粒度=单个
  视觉轴:单列居中 + 大留白 + 极简(Notion 风温暖)

变体 C (Linear 系):
  业务轴:任务流=先浏览 + 入口=⌘K + IA=标签优先 + 默认=全部 + 粒度=批量
  视觉轴:侧栏+列表+drawer + 暗色 + 密集(Linear 风)

变体 D (Notion 系):
  业务轴:任务流=先邀请 + 入口=侧栏 + IA=项目优先(嵌套)+ 默认=空 + 粒度=集合
  视觉轴:block 流 + 奶油底 + 温暖(Notion 风)
```

**4 个变体看起来像 4 个完全不同的产品**,因为业务轴 + 视觉轴都变了。如果只变视觉轴,4 个还是"任务管理换皮"。

## 升级版 Anti-Sameness Checklist(14 轴)

5 个方案生成完,过这张清单。**任何两条方案在这 14 轴上完全一样,就是同质化**:

```text
检查方案 A vs B vs C vs D vs E:

视觉轴(1-9):
□ 布局结构:至少 3 种?
□ 信息密度:至少 2 种?
□ 视觉重心:至少 3 种?
□ 配色:至少 2 种?
□ 字体:至少 2 种?
□ 图标:至少 2 种?
□ 留白:至少 2 种?
□ 装饰:至少 2 种?
□ 动效:至少 2 种?

业务轴(10-14,更深差异化):
□ 任务流顺序:至少 2 种?(创建 vs 浏览 vs 邀请 vs 配置 vs 模板)
□ 入口位置:至少 2 种?(顶栏 vs 侧栏 vs 中央 vs ⌘K vs FAB)
□ IA 优先级:至少 2 种?(对象 vs 项目 vs 时间 vs 人员 vs 标签)
□ 默认视图:至少 2 种?(空 vs 最近 vs 推荐 vs 全部 vs Today)
□ 对象粒度:至少 2 种?(单个 vs 批量 vs 集合 vs 流)

如果视觉轴都一样但业务轴变了 → 仍然是好变体(更深差异化)
如果业务轴都一样只变视觉 → 警惕"换皮"
```

## 变化生成算法(seed-based)

```python
def generate_variations(intent_brief, n=5):
    """
    从 Intent Brief 生成 n 个明显不同的视觉方案。
    """
    invariants = extract_invariants(intent_brief)
    # GOAL / AUDIENCE / TONE / 主任务 / 关键组件 / 状态 / a11y / 响应式

    # 推荐风格 DNA 作为锚点
    primary_style = route_to_style_dna(intent_brief)

    variations = []

    # 方案 1:推荐风格的"标准"执行
    variations.append({
        'name': f'Standard {primary_style}',
        'axes': {
            'layout': 'standard',
            'density': 'standard',
            'weight': 'top-heavy',
            'color': primary_style.default_color,
            'typography': primary_style.default_type,
            'imagery': primary_style.default_icon,
            'whitespace': 'standard',
            'decoration': primary_style.default_decoration,
            'motion': primary_style.default_motion,
        }
    })

    # 方案 2-3:沿"布局"和"密度"轴变(最显眼的差异)
    variations.append({
        'name': f'Dense {primary_style} (tool feel)',
        'axes': variations[0].axes.copy(),
        'overrides': {'density': 'dense', 'layout': 'bento'}
    })
    variations.append({
        'name': f'Breathing {primary_style} (editorial feel)',
        'axes': variations[0].axes.copy(),
        'overrides': {'density': 'breathing', 'whitespace': 'breathing', 'layout': 'asymmetric'}
    })

    # 方案 4:跨风格 DNA(仍保 invariants)
    alt_style = alternative_style_for_audience(intent_brief.audience)
    variations.append({
        'name': f'Alt style: {alt_style}',
        'axes': alt_style.default_axes
    })

    # 方案 5:极端单轴变化(如全 mono 字体、全摄影背景、全抽象几何)
    variations.append({
        'name': 'Mono typography extreme',
        'axes': variations[0].axes.copy(),
        'overrides': {'typography': 'mono-led', 'imagery': 'abstract geometric'}
    })

    # 每个 variation 都通过 Anti-Sameness Checklist 验证
    for v in variations:
        assert passes_anti_sameness(v, variations)

    return variations
```

## Anti-Sameness Checklist(防同质化,9 轴版)

> ⚠️ 这版已被上方"升级版 Anti-Sameness Checklist(14 轴)"替代。**业务轴(10-14)是更深差异化**,优先用 14 轴版。
>
> 仅当用户明确说"我只要视觉变体,不要业务变化"时,用这版 9 轴。

```text
检查方案 A vs B vs C vs D vs E:

□ 布局结构:5 个方案用了至少 3 种不同布局?
□ 信息密度:至少 2 种不同密度(dense vs breathing)?
□ 视觉重心:至少 3 种不同重心位置?
□ 配色:至少 2 种不同配色策略?
□ 字体:至少 2 种不同字体配对?
□ 图标:至少 2 种不同图标/插画风格?
□ 留白:至少 2 种不同留白哲学?
□ 装饰:至少 2 种不同装饰元素(或 none)?
□ 动效:至少 2 种不同动效气质?

如果任何一轴 5 个方案都一样:
  → 强制至少 2 个方案改这一轴
```

## 反同质化的极端手段

当所有"温和变化"都看起来太像,用这些极端手段打破:

1. **极端密度对比**——一个方案 dense(40px row),一个方案 luxury(96px padding),差距大
2. **极端色彩对比**——一个深色单色,一个奶油多色
3. **极端字体对比**——一个 sans only,一个 serif hero
4. **极端布局对比**——一个 bento grid,一个 single column
5. **极端装饰对比**——一个 none(纯净),一个 mesh gradient(装饰满)

## 与 SKILL.md Stage 1 的关系

Stage 1 草稿生成器调用这一页:
1. 读 Intent Brief → 提取 invariants
2. 调用 `generate_variations(intent, n=5)` → 5 个明显不同的方案
3. 每个方案用 ASCII/Markdown 写 wireframe + IA + 状态矩阵 + 取舍说明
4. 每个方案过 Anti-Sameness Checklist → 失败的重新生成
5. 用户选 1 个 → 进 Stage 2 高保真还原

## 与其他文档的关系

- **intent-reading.md**:提供 invariants(Intent Brief)
- **style-linear/stripe/notion/vercel.md**:提供单风格的完整冻结 axes
- **components/**:每个方案都套用同样的组件规格(尺寸不变,只是视觉 token 变)

## 权威信源

- lego-town/references/variation-engine.md(用户旗舰 skill 标准)
- "Divergent Design Thinking" — IDEO Method Cards
- "10 Filters for Design Variation" — Refactoring UI
- "How to generate distinct design concepts" — Jared Spool
