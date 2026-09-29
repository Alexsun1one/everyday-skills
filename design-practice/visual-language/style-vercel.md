# Style DNA — Vercel 风(极客纯黑 / 高对比 / bento grid)

> 开发平台、hosting、框架、极客工具营销页的事实标准。Vercel 风是 Linear 的更极端版本——Linear 还保留 violet accent,Vercel 是**纯黑 + 纯白 + 一个饱和 accent**,几何点纹背景,bento grid 布局,极简到极致。传达"前沿、极客、高性能"。

## 这家风格的灵魂

一句话:**极致极简,极简即高性能的视觉证据**。

Vercel 的视觉系统建立在一个工程信念上——"工具的性能通过它的克制证明"。它用**纯黑 `#000000`**(不像 Linear 用近黑带蓝调)、**几何点纹背景**、**一个饱和 accent**(早期蓝、近期多色,但每屏一个)、**bento grid 布局**(模块卡片网格)、**Geist 字体家族**(Vercel 自研)。每一个决策都在说:"我是为开发者做的,我不需要讨好你"。

## 1. 配色策略

### 配色哲学:纯黑白 + 单饱和 accent + 几何点纹

| 类别 | Token | Hex | 用途 |
|---|---|---|---|
| Canvas (dark) | `color.canvas` | **`#000000`** | 营销页画布(**纯黑**——Vercel 与 Linear 的区别就在这,Linear 用 `#08090A` 近黑,Vercel 用纯黑) |
| Canvas (light) | `color.canvas.light` | `#FFFFFF` | 浅色模式画布(纯白) |
| Surface | `color.surface` | `#0A0A0A` | 抬升卡片(比 canvas 稍亮的深灰) |
| Surface 2 | `color.surface.2` | `#111111` | 二级面板 |
| Surface 3 | `color.surface.3` | `#171717` | popover、modal |
| Border | `color.border` | `rgba(255,255,255,0.1)` | 标准 1px 边框 |
| Border strong | `color.border.strong` | `rgba(255,255,255,0.2)` | 强边框 |
| Text primary | `color.text` | `#FFFFFF` | 主文本(纯白 on 纯黑——极限对比) |
| Text secondary | `color.text.secondary` | `#888888` 或 `#A1A1A1` | 次文本 |
| Text tertiary | `color.text.tertiary` | `#666666` | 弱文本 |
| **Brand accent** | **`color.accent`** | **`#0070F3`(经典 Vercel 蓝)** | 单一 accent——CTA、链接、focus。或现代变体:粉 `#FF0080`、绿 `#00DC82`、紫 `#7928CA`、橙 `#F5A623`——**但每屏一个,不混** |
| Gradient | `color.gradient` | `linear-gradient(90deg, #0070F3, #7928CA)` | 偶尔 hero accent gradient(蓝→紫) |
| Geometric bg | `bg.dotgrid` | `radial-gradient(circle, rgba(255,255,255,0.06) 1px, transparent 1px) 0 0 / 16px 16px` | 几何点纹背景(Vercel 签名) |
| Geometric bg alt | `bg.grid` | `linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px) 0 0 / 32px 32px` | 网格背景(替代) |

### 配色铁律

> **纯黑 `#000000` + 纯白 `#FFFFFF`** 的极限对比——Vercel 不像 Linear 那样用近黑近白。这是它与 Linear 的视觉分界线。
>
> **每屏一个饱和 accent**——蓝、粉、绿、紫、橙中选一,**不混**。混了就塌。
>
> **几何点纹或网格背景**——Vercel 营销页几乎都有这个签名背景纹理。

## 2. 字体系统

### Font family:Geist 字体家族(Vercel 自研)

| Token | Family | 用途 |
|---|---|---|
| `font.sans` | **Geist Sans**(Vercel 自研,2023 发布;免费开源,SIL)| 所有 UI、正文 |
| `font.mono` | **Geist Mono**(Vercel 自研)| 代码、URL、technical label |
| 免费替代 | Inter Variable(气质最接近) | 如果 Geist 不可用 |

### Weight system

| Weight | 用途 |
|---|---|
| 400 | body |
| 500 | emphasis、UI label |
| 600 | heading |
| 700 | hero title |

### Tracking

Vercel 用**中等负 tracking**——hero -0.02em,body 0。不像 Linear 那么紧,也不像 Notion 那么松。

### 字号阶梯

| Token | Size | Weight | LH | LS | 用途 |
|---|---|---|---|---|---|
| `t-hero` | 64-96px | 700 | 1.0 | -0.03em | 营销 hero(极大) |
| `t-h1` | 48-56px | 700 | 1.05 | -0.02em | 页面主标题 |
| `t-h2` | 32-40px | 600 | 1.1 | -0.01em | 分区 |
| `t-h3` | 24px | 600 | 1.2 | 0 | 子标题 |
| `t-body` | 16px | 400 | 1.5 | 0 | 正文 |
| `t-body-sm` | 14px | 400 | 1.5 | 0 | UI 正文 |
| `t-mono` | 14px | 400 | 1.4 | 0 | 代码、URL |

## 3. 圆角阶梯(Vercel 用 4/6/8/12)

| Token | Value | 用途 |
|---|---|---|
| `radius.sm` | 4px | tag、badge |
| `radius.md` | 6px | 按钮、输入框 |
| `radius.lg` | 8px | bento card |
| `radius.xl` | 12px | 大型 feature card |

> Vercel 比 Linear 圆角谱宽(Linear 严格 6/12/9999)。4-12 都用,根据元素重要性递增。

## 4. 阴影 / elevation 哲学

### 核心原则

> **几乎无阴影**——Vercel 靠**边框 + 背景对比**创造 elevation,不是 drop shadow。卡片用 `rgba(255,255,255,0.1)` border + hover 时 border 变亮 + 极轻外发光 accent。

### Shadow(只在 hover 时浮现)

| Name | Value | 用途 |
|---|---|---|
| `shadow.none` | none | 默认(所有 card) |
| `shadow.hover` | `0 0 0 1px rgba(255,255,255,0.2), 0 8px 24px rgba(0,0,0,0.3)` | card hover 时(1px 亮 border + 轻 drop) |
| `shadow.accent` | `0 0 0 1px var(--accent), 0 0 24px rgba(0,112,243,0.3)` | accent card hover(发光感) |
| `shadow.popover` | `0 0 0 1px rgba(255,255,255,0.1), 0 16px 32px rgba(0,0,0,0.5)` | popover、modal |

### Focus ring

focus state:`0 0 0 2px var(--accent)`(纯 accent 2px,不是 halo,不是双层)——Vercel 比 Linear 更克制。

## 5. 间距气质——bento grid 严密对齐

| 用途 | 值 |
|---|---|
| bento card gap | 8-16px(严密对齐) |
| bento card padding | 24-32px |
| 段间隙 | 64-96px |
| hero 内容 max-width | 1024-1280px |

## 6. 动效曲线——快速、克制、几何

| Property | Duration | Timing |
|---|---|---|
| hover | 150ms | ease-out |
| popover | 150ms | ease-out |
| modal | 200ms | ease-out |
| page transition | 200-300ms | `cubic-bezier(0.4, 0, 0.2, 1)` |
| gradient hero anim | 4-8s | linear(无限循环) |

## 7. 图标体系——Lucide 或自定

**强制图标库:Lucide**(Vercel 官方设计系统用 Lucide 风格图标)。

| 场景 | 用法 |
|---|---|
| 按钮 icon | 16-20px Lucide,stroke 2px |
| bento card icon | 24px Lucide,带 accent 色 |
| nav icon | 20px |
| arrow | 长箭头(`→` Lucide arrow-right)——Vercel 签名"了解更多"链接都用 trailing arrow |

**严禁**与 Heroicons/Phosphor 混用。如果 Lucide 没有,**自定 SVG 匹配 24×24、2px stroke、几何精确**。详见 `icon-systems.md`。

## 8. 签名组件(Vercel 风独有的"人做的"证据)

### Bento Grid(签名)
- 营销页 feature 用**模块化卡片网格**——大小不一,严密对齐
- 每个 card 一个 feature,带 icon + 标题 + 描述
- card 之间 8-16px gap,内部 24-32px padding
- card hover:border 变亮 + 轻 drop shadow

### Geometric Background(签名)
- 几何点纹(`radial-gradient` 点阵)或网格(`linear-gradient` 双向)
- `rgba(255,255,255,0.06)` 强度
- 几乎每个 Vercel hero 都有这个

### Trailing Arrow Link(签名)
- 所有"了解更多"链接用 `→` trailing arrow
- hover 时 arrow 微移右
- 极 Vercel 的视觉签名

### Mono Code Block(签名)
- Geist Mono,带 syntax highlight
- 圆角 8px,border 1px,深背景 `#0A0A0A`
- 行号、命令提示符 `$` 或 `→`

### Gradient Hero Accent(签名)
- hero 标题或背景偶用蓝→紫 gradient
- `linear-gradient(90deg, #0070F3, #7928CA)`
- 用于营销页强调

### Pill Badge(签名)
- `NEW`、`BETA`、`ANNOUNCING` 等 pill badge
- 实色或 accent outline
- 圆角 9999px,padding 4px 12px

## 9. 反塑料证据(Vercel 风的"人做的"信号)

- [ ] **纯黑 `#000000` + 纯白 `#FFFFFF`**(极限对比,不是近黑近白)
- [ ] **几何点纹或网格背景**(几乎所有 hero)
- [ ] **bento grid 布局**(严密对齐的卡片网格)
- [ ] **每屏一个饱和 accent**(不混蓝粉绿紫橙)
- [ ] **trailing arrow 链接**(`→` 在每个"了解更多")
- [ ] **Geist Sans / Mono**(或 Inter 替代)
- [ ] **几乎无 shadow**(靠 border + hover 亮 border)
- [ ] **mono code block**(Geist Mono)
- [ ] **pill badge**(`NEW`/`BETA`/`ANNOUNCING`)

## 10. 反派警示

| 塌成的塑料样 | 病因 | 修复 |
|---|---|---|
| 看起来像 Linear | 用了近黑 `#08090A` | 改纯黑 `#000000` |
| 像通用 dashboard | 没有 bento grid | 改 bento 网格布局 |
| 像玩具 | 多个 accent 混用 | 每屏一个 accent |
| 像廉价模板 | 用了 emoji | 改 Lucide icon |
| 像没骨架 | 没几何背景 | 加点纹或网格 |
| 像博客 | 没用 trailing arrow | 链接加 `→` |

## Prompt Fragment(可复制)

### English

```text
Visual style: Vercel-inspired (extreme minimalism, pure black, high contrast, bento grid, geek-forward).

COLOR (extreme contrast):
- canvas: pure #000000 (DARK default — this is Vercel's signature, vs Linear's #08090A near-black)
- light variant: pure #FFFFFF
- surface ladder: #0A0A0A → #111111 → #171717 (subtle gray lift from pure black)
- border: rgba(255,255,255,0.1) default, rgba(255,255,255,0.2) strong
- text: pure #FFFFFF primary / #888888 secondary / #666666 tertiary (extreme contrast)
- ONE saturated accent per screen (NEVER mix):
  - classic Vercel blue #0070F3
  - modern variants: pink #FF0080, green #00DC82, purple #7928CA, orange #F5A623
- gradient: linear-gradient(90deg, #0070F3, #7928CA) for occasional hero accent
- SIGNATURE BACKGROUND: geometric dot-grid or line-grid
  - dot-grid: radial-gradient(circle, rgba(255,255,255,0.06) 1px, transparent 1px) 0 0 / 16px 16px
  - line-grid: linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px) 0 0 / 32px 32px

TYPOGRAPHY:
- font: Geist Sans (Vercel's own, free OSS, SIL) or Inter Variable as closest free alt
- mono: Geist Mono for code, URLs, technical labels
- weights: body 400, emphasis 500, heading 600, hero 700
- tracking: hero -0.03em, h1 -0.02em, body 0
- hero size: 64-96px (EXTREMELY large)
- line-height: 1.0-1.1 for hero, 1.5 for body

RADIUS (wider range than Linear):
- 4px for tags/badges
- 6px for buttons/inputs
- 8px for bento cards
- 12px for large feature cards

ELEVATION (almost no shadow):
- default cards: NO shadow, just 1px border
- card hover: 0 0 0 1px rgba(255,255,255,0.2), 0 8px 24px rgba(0,0,0,0.3) (brighter border + light drop)
- accent card hover: 0 0 0 1px var(--accent), 0 0 24px rgba(0,112,243,0.3) (glow)
- popover: 0 0 0 1px rgba(255,255,255,0.1), 0 16px 32px rgba(0,0,0,0.5)
- focus: 0 0 0 2px var(--accent) (pure 2px accent, NOT halo, NOT double-layer — more restrained than Linear)

SPACING (bento grid discipline):
- bento card gap: 8-16px (tight geometric alignment)
- bento card padding: 24-32px
- section gap: 64-96px
- hero max-width: 1024-1280px

SIGNATURE STRUCTURE:
- BENTO GRID: modular card grid of varying sizes, tight alignment, each card = one feature with icon+title+desc
- GEOMETRIC BACKGROUND: dot-grid or line-grid on nearly every hero
- TRAILING ARROW LINKS: all "learn more" links use → arrow, hover shifts arrow right
- MONO CODE BLOCK: Geist Mono, syntax highlight, 8px radius, 1px border, #0A0A0A bg
- GRADIENT HERO ACCENT: occasional blue→purple linear gradient for hero emphasis
- PILL BADGES: NEW/BETA/ANNOUNCING, solid or accent outline, 9999px radius, 4px 12px padding

MOTION:
- hover: 150ms ease-out
- popover: 150ms ease-out
- modal: 200ms ease-out
- page transition: 200-300ms cubic-bezier(0.4, 0, 0.2, 1)
- gradient hero animation: 4-8s linear infinite (subtle)

ICONS: Lucide ONLY (or custom SVG matching 24×24 / 2px stroke / geometric precision)
- button icon: 16-20px
- bento card icon: 24px with accent color
- nav icon: 20px
- NEVER mix libraries, NEVER emoji

NEVER:
- use near-black #08090A (use pure #000 — that's the Vercel/Linear dividing line)
- use near-white #F7F8F8 (use pure #FFFFFF in light mode)
- mix multiple saturated accents in one viewport
- use drop shadows by default (use border + hover-brighter-border)
- use emoji icons
- use bento grid with uneven gaps (must be geometrically aligned)
- skip the geometric dot-grid or line-grid background on hero
```

### 中文

```text
视觉风格:Vercel 风(极致极简,纯黑,高对比,bento grid,极客气质)。

配色(极限对比):
- 画布:纯 #000000(DARK 默认——Vercel 签名,vs Linear 的 #08090A 近黑)
- 浅色变体:纯 #FFFFFF
- 表面阶梯:#0A0A0A → #111111 → #171717(从纯黑微微抬升的灰)
- 边框:默认 rgba(255,255,255,0.1),强 rgba(255,255,255,0.2)
- 文字:纯 #FFFFFF 主 / #888888 次 / #666666 弱(极限对比)
- 每屏一个饱和 accent(绝不混):
  - 经典 Vercel 蓝 #0070F3
  - 现代变体:粉 #FF0080、绿 #00DC82、紫 #7928CA、橙 #F5A623
- 渐变:linear-gradient(90deg, #0070F3, #7928CA) 偶尔用于 hero accent
- 签名背景:几何点纹或网格
  - 点纹:radial-gradient(circle, rgba(255,255,255,0.06) 1px, transparent 1px) 0 0 / 16px 16px
  - 网格:linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px) 0 0 / 32px 32px

字体:
- 字体:Geist Sans(Vercel 自研,免费开源,SIL),或 Inter 变量最接近免费替代
- 等宽:Geist Mono 用于代码、URL、technical label
- 字重:body 400,emphasise 500,heading 600,hero 700
- tracking:hero -0.03em,h1 -0.02em,body 0
- hero 字号:64-96px(极大)
- line-height:hero 1.0-1.1,body 1.5

圆角(比 Linear 谱宽):
- 4px 用于 tag/badge
- 6px 用于按钮/输入
- 8px 用于 bento card
- 12px 用于大 feature card

ELEVATION(几乎无 shadow):
- 默认卡片:无 shadow,仅 1px 边框
- card hover:0 0 0 1px rgba(255,255,255,0.2), 0 8px 24px rgba(0,0,0,0.3)(亮 border + 轻 drop)
- accent card hover:0 0 0 1px var(--accent), 0 0 24px rgba(0,112,243,0.3)(发光)
- popover:0 0 0 1px rgba(255,255,255,0.1), 0 16px 32px rgba(0,0,0,0.5)
- focus:0 0 0 2px var(--accent)(纯 2px accent,不是 halo,不是双层——比 Linear 更克制)

间距(bento grid 严密):
- bento card gap:8-16px(几何严密对齐)
- bento card padding:24-32px
- 段间隙:64-96px
- hero max-width:1024-1280px

签名结构:
- BENTO GRID:模块化卡片网格,大小不一,严密对齐,每个 card 一个 feature + icon + 标题 + 描述
- GEOMETRIC BACKGROUND:几何点纹或网格,几乎每个 hero 都有
- TRAILING ARROW LINK:所有"了解更多"用 → trailing arrow,hover 时 arrow 微移右
- MONO CODE BLOCK:Geist Mono,syntax highlight,8px radius,1px border,#0A0A0A 底
- GRADIENT HERO ACCENT:偶尔蓝→紫 linear gradient 强调
- PILL BADGE:NEW/BETA/ANNOUNCING,实色或 accent outline,9999px radius,4px 12px padding

动效:
- hover:150ms ease-out
- popover:150ms ease-out
- modal:200ms ease-out
- 页面过渡:200-300ms cubic-bezier(0.4, 0, 0.2, 1)
- gradient hero 动画:4-8s linear 无限(微妙)

图标:仅 Lucide(或自定 SVG 匹配 24×24 / 2px stroke / 几何精确)
- 按钮 icon:16-20px
- bento card icon:24px + accent 色
- nav icon:20px
- 绝不混库,绝不 emoji

绝对不要:
- 用近黑 #08090A(用纯 #000——这是 Vercel 与 Linear 的视觉分界线)
- 用近白 #F7F8F8(浅色模式用纯 #FFFFFF)
- 同视口混多个饱和 accent
- 默认用 drop shadow(用 border + hover 亮 border)
- 用 emoji icon
- bento grid 间距不齐(必须几何对齐)
- hero 不加几何点纹或网格背景
```

## 权威信源

- welovedaily.net "Vercel's Aesthetic — How to build a developer brand"
- brainy.ink "Vercel aesthetic" 同质化分析
- vercel.com/blog(自家设计哲学)
- vercel.com/geist(字体家族)
- designmd.cc/benchmarks/vercel

## 与其他风格的关系

- 想要**深色工程工具**(开发者/项目管理,带 violet accent)→ 切到 `style-linear.md`
- 想要**白底编辑式**(支付/金融/营销)→ 切到 `style-stripe.md`
- 想要**温暖反流派**(知识/协作/教育)→ 切到 `style-notion.md`
- Vercel 风适合**开发平台、hosting、框架、极客工具的营销页**——纯黑 + bento + 几何点纹是极客签名。**绝禁**用在消费者、金融、教育产品——会显得冰冷、难懂、像"工程师给工程师看的东西"。
