# Style DNA — Notion 风(温暖反流派 / 知识协作 / 消费者亲和)

> 当产品是给**非工程师**用的(知识管理、协作、教育、写作、笔记、CRM、消费者 App),Linear/Stripe 的冷调工程感会让产品显得冰冷、难懂、像"工具"而不是"伙伴"。Notion 风是反流派——温暖、亲和、像纸、像本子、像朋友写给你的笔记。

## 这家风格的灵魂

一句话:**纸感、温暖、人味、像自家人的笔记本**。

Notion 的视觉决策全部围绕"破冰"——**把冰冷的数字界面变得像纸和墨水**。它用奶油底(不是纯白)、serif 标题(不是 sans)、手绘风 emoji/插画(不是 line icon)、温暖橙色调 accent(不是冷紫/蓝)、圆角 4-8px(不是 6/12 工程感)、极轻阴影或几乎无阴影(像纸贴在桌面上)。每一个决策都在说:"我不是工具,我是你的笔记"。

## 1. 配色策略

### 配色哲学:温暖中性 + 多彩柔和 accent

| 类别 | Token | Hex | 用途 |
|---|---|---|---|
| Canvas | `color.canvas` (Cream) | `#FFFDF7` 或 `#FBF9F4` | 页面背景(奶油,**不是纯白**——破冰的第一步) |
| Surface | `color.surface` | `#FFFFFF` | 卡片、面板(纯白卡片浮在奶油画布上) |
| Primary text | `color.ink` (Charcoal) | `#1F1F1F` 或 `#2F2F2F` | 主文本(深炭,**不是纯黑**) |
| Secondary text | `color.text.gray` | `#6B6B6B` 或 `#787774` | 次文本 |
| Tertiary text | `color.text.faint` | `#9B9B9B` | 弱文本、timestamp |
| Border | `color.border` | `#E9E5DA` 或 `#E3E2DE` | 暖灰发丝线 |
| **Default accent** | **`color.default`** | **`#1F1F1F`**(近黑) | **默认按钮、强调**——Notion 反流派:多数 CTA 是黑色而不是彩色 |
| **Brand accent** | **`color.orange`** | **`#D9730D`** | **品牌橙——logo、focus、强调链接** |
| Accent red | `color.red` | `#E03E3E` | 危险、删除 |
| Accent pink | `color.pink` | `#AD1A72` | pink block、tag |
| Accent blue | `color.blue` | `#0B6E99` | blue block、info tag |
| Accent purple | `color.purple` | `#6940A5` | purple block |
| Accent yellow | `color.yellow` | `#DFAB01` | warn、highlight |
| Accent green | `color.green` | `#0F7B6C` | success、done |
| Accent gray | `color.gray` | `#777572` | tag、block icon |

### 配色铁律

> Notion 风是**多彩的**——但每个 accent 都是**柔和、降饱和、纸感**版本,不是 web 鲜艳的纯色。每个 block 可带一个 colored accent(red/pink/purple/blue/yellow/green),但都用做语义 block 装饰,**不是** CTA 颜色。
>
> **多数 CTA 是黑色** `#1F1F1F`——这是 Notion 反流派最辨识的决策。

## 2. 字体系统

### Font family:sans-serif 工具字体 + serif 编辑标题(双字体配对)

| Token | Family | 用途 |
|---|---|---|
| `font.ui` | Inter Variable(原 Notion 自有;web 端通用近似)| 所有 UI、正文、按钮 |
| `font.display` | serif(如 Lyon、GT Sectra;免费替代 Source Serif、Lora)| 营销页大标题(给"印刷品/笔记本"气质) |
| `font.mono` | ui-monospace、SFMono-Regular、Menlo | 代码块、行内 code |
| `font.cjk` | PingFang SC、Hiragino Sans、Microsoft YaHei | 中文字回退 |

### Weight system

| Weight | 用途 |
|---|---| 
| 400 | body |
| 500 | emphasis、UI label |
| 600 | section heading |
| 700 | hero serif title |

### Tracking

Notion 风的 tracking 比工程感松一点——大字 -0.01em 到 -0.02em(很轻的负),body 0,小字 0。**不像 Linear 那样紧**——纸感是松弛的。

### 字号阶梯

| Token | Size | Weight | 用途 |
|---|---|---|---|
| `t-hero` | 56-72px | 700 serif | 营销 hero(serif) |
| `t-h1` | 40px | 700 | 页面 H1 |
| `t-h2` | 30px | 600 | 分区 |
| `t-h3` | 24px | 600 | 子标题 |
| `t-body` | 16px | 400 | 正文 |
| `t-body-sm` | 14px | 400 | UI 正文 |
| `t-label` | 14px | 500 | UI 标签 |
| `t-meta` | 12-13px | 400 | timestamp、tag |

## 3. 圆角阶梯(Notion 用 4/8 两档)

| Token | Value | 用途 |
|---|---|---|
| `radius.small` | 4px | 按钮、输入框、tag、badge |
| `radius.medium` | 8px | 卡片、panel、callout、image |

> Notion **不用 12px+** 圆角——12+ 偏现代工程感,8px 是它的最大值,守住亲和但不甜腻。

## 4. 阴影 / elevation 哲学 —— 极轻、纸贴桌面

### 核心原则

> **阴影极轻**——卡片浮在画布上像纸贴桌面,不是悬空浮窗。多数情况只用 1px 暖灰边框 + 极轻 shadow。**绝禁**重 drop shadow。

### 3 档 Shadow

| Name | Value | 用途 |
|---|---|---|
| `shadow.card` | `rgba(15, 15, 15, 0.05) 0px 0px 0px 1px, rgba(15, 15, 15, 0.04) 0px 3px 6px` | 卡片(1px border + 极轻阴影) |
| `shadow.popover` | `rgba(15, 15, 15, 0.05) 0px 0px 0px 1px, rgba(15, 15, 15, 0.1) 0px 3px 6px, rgba(15, 15, 15, 0.2) 0px 9px 24px` | popover、菜单(三段式但都极轻) |
| `shadow.drag` | `rgba(15, 15, 15, 0.05) 0px 0px 0px 1px, rgba(15, 15, 15, 0.2) 0px 12px 24px` | 拖拽中的 block |

### Focus ring(Notion 是橙色 2px)

focus state:`box-shadow: 0 0 0 2px rgba(217, 115, 13, 0.4)`(Notion 橙 2px halo)。

## 5. 间距气质——松、呼吸、像纸

Notion 用 4px 网格,但**用得松**——段落间宽松,行间松弛,line-height 1.6-1.7。每个 block 之间至少 8-12px 空隙。**不像 Linear 那样密集**——Linear 是仪表盘密度,Notion 是笔记本呼吸。

| 用途 | 值 |
|---|---|
| block 之间 | 4-8px |
| 段落 line-height | 1.6-1.7 |
| 卡片 padding | 16-24px |
| 卡片之间 | 16-24px |
| 段间隙 | 64-96px |

## 6. 动效曲线——温和、慢、有手

| Property | Duration | Timing |
|---|---|---|
| color / bg | 150-200ms | ease-out |
| popover 开 | 100ms | ease-out |
| modal 入 | 200ms | ease-out |
| block drag | 200ms | cubic-bezier(0.4, 0, 0.2, 1) |
| hover lift | 150ms | ease |

## 7. 图标体系——绑定 Phosphor Duotone + 真实 emoji

**强制图标库:Phosphor Icons(Duotone 变体)**(9000+ icons,5 weights 含 Duotone,24×24,MIT)。

为什么不是 Lucide / Heroicons?
- Lucide/Heroicons 是 line-based、1.5-2px stroke、几何精确——**太工程感**
- Phosphor Duotone 有**两层填色**(主+次),手感更暖、更像手绘
- 配 Notion 的"纸和笔"气质

| 场景 | 用法 |
|---|---|
| block icon | 24px Phosphor Duotone,带 block color(red/pink/purple/blue/yellow/green/gray) |
| nav icon | 20px Phosphor Regular(不是 Duotone,导航要清晰) |
| 按钮 icon | 16px Phosphor Regular |
| 状态、装饰 | **真实 emoji**(📌📍💡✅🔥)——Notion 是少数能用 emoji 不土的产品,因为它整体气质就是亲和 |

**严禁** Phosphor + Lucide 混用。详见 `icon-systems.md`。

## 8. 签名组件(Notion 风独有的"人做的"证据)

### Block-based layout(签名)
- 所有内容是**块**——paragraph、heading、callout、image、embed
- 每个 block 高度自适应,block 之间松散垂直排列
- hover 时左侧出现 **drag handle**(⋮⋮)
- 这是 Notion 最辨识的结构——**不是表格布局,是块流**

### Callout(签名)
- 浅色背景框 + Duotone icon + 简短文字
- 用于强调、提示、引用
- 圆角 8px,padding 16px,带 colored background tint

### Colored Tag / Pill(签名)
- 6 种颜色(red/pink/purple/blue/yellow/green)+ gray
- 每种都是**柔和降饱和**版本
- 用做 block color、status tag、category badge

### Toggle Block(签名)
- 可折叠的块,左侧 ▶ 三角
- 点开向下展开内容
- 用于 FAQ、长说明、nested list

### Hover Toolbar(签名)
- 选中文字时浮出小型 toolbar(format/color/link)
- 极轻 shadow、白色背景、4px radius
- 仅在选中时出现

### Emoji Avatar / Cover(签名)
- 工作区、页面可设 emoji 作为 icon
- 文档顶部可设 cover image
- emoji 是一等公民(不是装饰)——这是反流派核心

### Black Primary Button(签名反流派)
- 多数 primary CTA 是**黑色** `#1F1F1F` + 白字
- 而不是品牌橙
- 营销页用 brand orange `#D9730D` 做 accent

## 9. 反塑料证据(Notion 风的"人做的"信号)

- [ ] **奶油底**(`#FFFDF7` / `#FBF9F4`,不是纯白)
- [ ] **serif hero title**(营销页)
- [ ] **多数 CTA 是黑色** `#1F1F1F`(不是彩色)
- [ ] **block-based layout**(不是表格网格)
- [ ] **drag handle** 在 block hover 时出现
- [ ] **callout block**(浅色 tint + Duotone icon + 简短文字)
- [ ] **colored tags**(6 种柔和色 + gray)
- [ ] **真实 emoji** 作为页面 icon / 装饰
- [ ] **Phosphor Duotone** 图标(不是 Lucide)
- [ ] **圆角 4/8**(不用 6/12)
- [ ] **极轻 shadow**(像纸贴桌面)
- [ ] **line-height 1.6-1.7**(松、呼吸)
- [ ] **block 之间 4-8px 空隙**

## 10. 反派警示

| 塌成的塑料样 | 病因 | 修复 |
|---|---|---|
| 看起来像通用 CMS / wiki | 纯白背景 | 改奶油底 |
| 看起来冷 | sans-serif 标题 | 营销页用 serif |
| 像玩具 | emoji 用得太多 | emoji 只作为 icon/装饰,不替代按钮文字 |
| 杂牌图标 | Lucide + emoji 混用 | 全 Phosphor Duotone,emoji 仅作页面 icon |
| 像 Linear | 重 shadow / 深色 / 6px radius | 改极轻 shadow / 奶油 / 4-8px radius |
| 太甜 | 6 种 accent 全用 | 一屏最多 2-3 种 accent |
| 像表格 grid | 用了 table layout | 改 block 流 |

## Prompt Fragment(可复制)

### English

```text
Visual style: Notion-inspired (warm, paper-like, knowledge-collaboration aesthetic — anti-cold-engineering).

COLOR (warm cream + multi-soft-accents):
- canvas: #FFFDF7 or #FBF9F4 (cream, NEVER pure #FFFFFF — the warm paper feel is non-negotiable)
- surface: #FFFFFF for cards (white cards float on cream canvas)
- text: #1F1F1F / #2F2F2F (charcoal, NEVER pure #000)
- secondary text: #6B6B6B; tertiary #9B9B9B
- border: #E9E5DA (warm gray hairline)
- DEFAULT BUTTONS: black #1F1F1F with white text (counter-convention — most CTAs are black, NOT colored)
- BRAND accent: #D9730D (Notion orange — logo, focus ring, marketing CTA)
- 6 soft semantic accents for blocks/tags: red #E03E3E, pink #AD1A72, blue #0B6E99, purple #6940A5, yellow #DFAB01, green #0F7B6C
- ALL accents are DESATURATED and PAPER-LIKE, never web-vivid

TYPOGRAPHY (dual-family):
- UI font: Inter Variable (closest free to Notion's font)
- DISPLAY font: serif (Lyon/GT Sectra feel; free: Source Serif / Lora) for marketing hero titles
- weights: body 400, emphasis 500, section 600, hero 700
- tracking: hero -0.01em to -0.02em (light negative, LOOSER than Linear), body 0
- line-height: 1.6-1.7 (BREATHING room, NOT tight)

RADIUS: only 2 values
- small: 4px (buttons, inputs, tags, badges)
- medium: 8px (cards, panels, callouts, images)
- NEVER 6px (Linear) or 12px+ (modern engineering)

ELEVATION (paper-on-desk):
- shadows are EXTREMELY light, like paper resting on a desk
- shadow.card: rgba(15,15,15,0.05) 0px 0px 0px 1px, rgba(15,15,15,0.04) 0px 3px 6px
- shadow.popover: rgba(15,15,15,0.05) 0px 0px 0px 1px, rgba(15,15,15,0.1) 0px 3px 6px, rgba(15,15,15,0.2) 0px 9px 24px
- focus: 0 0 0 2px rgba(217,115,13,0.4) (Notion orange 2px halo)
- NEVER heavy drop shadow

SPACING (loose, breathing):
- block gap: 4-8px
- card padding: 16-24px
- card gap: 16-24px
- section gap: 64-96px
- NEVER Linear-style dense dashboard packing

SIGNATURE STRUCTURE:
- BLOCK-BASED LAYOUT (not grid/table) — all content is blocks vertically stacked with breathing room
- DRAG HANDLE (⋮⋮) appears on left of blocks on hover
- CALLOUT BLOCK: soft-tinted bg + Phosphor Duotone icon + short text, 8px radius, 16px padding
- COLORED TAGS: 6 soft accents + gray, desaturated paper-like
- TOGGLE BLOCK: ▶ triangle collapsible
- HOVER TEXT TOOLBAR: appears on selection, white bg, 4px radius, ultra-light shadow
- EMOJI: first-class — used as page icons, workspace icons, NOT in button text
- BLACK PRIMARY BUTTON: most CTAs are #1F1F1F + white text (counter-convention)

MOTION:
- color/bg: 150-200ms ease-out
- popover open: 100ms ease-out
- modal in: 200ms ease-out
- block drag: 200ms cubic-bezier(0.4, 0, 0.2, 1)

ICONS: Phosphor Icons (Duotone variant primary, Regular for nav/buttons)
- block icon: 24px Duotone with block color
- nav icon: 20px Regular
- button icon: 16px Regular
- EMOJI: real emoji as page/workspace icons, decorative — NEVER inside button text
- NEVER mix with Lucide / Heroicons (their line-precision breaks the paper feel)

NEVER:
- use pure #FFFFFF as canvas (use cream)
- use pure #000 as text (use charcoal)
- use 6px/12px radius (use 4/8)
- use heavy drop shadow
- make all CTAs colored (most should be black)
- mix Phosphor with Lucide
- use emoji inside button text
- use table/grid layout (use block flow)
- use line-height < 1.5 (use 1.6-1.7)
- use desaturated-vivid web colors (use paper-soft tones)
```

### 中文

```text
视觉风格:Notion 风(温暖反流派,纸感,知识协作气质——反冰冷工程)。

配色(奶油 + 多柔和 accent):
- 画布:#FFFDF7 或 #FBF9F4(奶油,绝不用纯 #FFFFFF——暖纸感不可省)
- 表面:#FFFFFF 卡片浮在奶油画布上
- 文字:#1F1F1F / #2F2F2F(炭灰,绝不用纯 #000)
- 次文本:#6B6B6B;弱 #9B9B9B
- 边框:#E9E5DA(暖灰发丝线)
- 默认按钮:黑 #1F1F1F + 白字(反常规——多数 CTA 是黑色,不是彩色)
- 品牌 accent:#D9730D(Notion 橙——logo、focus ring、营销 CTA)
- 6 种柔和语义 accent 用于 block/tag:red #E03E3E、pink #AD1A72、blue #0B6E99、purple #6940A5、yellow #DFAB01、green #0F7B6C
- 所有 accent 都降饱和、纸感,绝不 web 鲜艳

字体(双字体配对):
- UI 字体:Inter Variable(最接近 Notion 字体的免费方案)
- 营销字体:serif(Lyon/GT Sectra 气质;免费:Source Serif / Lora)用于营销 hero 标题
- 字重:body 400,emphasise 500,section 600,hero 700
- tracking:hero -0.01em 到 -0.02em(轻负,比 Linear 松),body 0
- line-height:1.6-1.7(呼吸,不紧凑)

圆角:只用两档
- small:4px(按钮、输入、tag、badge)
- medium:8px(卡片、panel、callout、image)
- 绝不用 6px(Linear)或 12px+(现代工程)

ELEVATION(纸贴桌面):
- 阴影极轻,像纸贴桌面
- shadow.card:rgba(15,15,15,0.05) 0px 0px 0px 1px, rgba(15,15,15,0.04) 0px 3px 6px
- shadow.popover:rgba(15,15,15,0.05) 0px 0px 0px 1px, rgba(15,15,15,0.1) 0px 3px 6px, rgba(15,15,15,0.2) 0px 9px 24px
- focus:0 0 0 2px rgba(217,115,13,0.4)(Notion 橙 2px halo)
- 绝禁重 drop shadow

间距(松、呼吸):
- block 之间:4-8px
- 卡片 padding:16-24px
- 卡片之间:16-24px
- 段间隙:64-96px
- 绝不像 Linear 那样仪表盘密集

签名结构:
- BLOCK-BASED 布局(不是 grid/table)——所有内容是垂直 block 流,带呼吸
- DRAG HANDLE(⋮⋮)在 block hover 时出现
- CALLOUT 块:浅色 tint + Phosphor Duotone icon + 简短文字,8px radius,16px padding
- COLORED TAGS:6 种柔和 accent + gray,降饱和纸感
- TOGGLE 块:▶ 三角可折叠
- HOVER 文本工具栏:选中时浮出,白底,4px radius,极轻 shadow
- EMOJI:一等公民——用作页面/工作区 icon,装饰用,绝不进按钮文字
- 黑色 PRIMARY 按钮:多数 CTA 是 #1F1F1F + 白字(反常规)

动效:
- color/bg:150-200ms ease-out
- popover 开:100ms ease-out
- modal 入:200ms ease-out
- block drag:200ms cubic-bezier(0.4, 0, 0.2, 1)

图标:Phosphor Icons(Duotone 为主,Regular 用于 nav/按钮)
- block icon:24px Duotone + block color
- nav icon:20px Regular
- 按钮 icon:16px Regular
- EMOJI:真实 emoji 用作页面/工作区 icon,装饰用——绝不进按钮文字
- 绝不与 Lucide / Heroicons 混用(它们的线条精确感破坏纸感)

绝对不要:
- 用纯 #FFFFFF 作画布(用奶油)
- 用纯 #000 作文字(用炭灰)
- 用 6px/12px 圆角(用 4/8)
- 用重 drop shadow
- 把所有 CTA 做成彩色(多数应是黑色)
- Phosphor 混 Lucide
- emoji 进按钮文字
- 用 table/grid 布局(用 block 流)
- line-height < 1.5(用 1.6-1.7)
- 用饱和鲜艳色(用纸感柔和色)
```

## 权威信源

- designmd.cc/benchmarks/notion
- styleextract.com/notion-design-system
- refero.styles(notion 标签)
- notion.so/design blog
- "Notion's design philosophy" 多篇 Medium/UX Collective 文章

## 与其他风格的关系

- 想要**深色工程工具**(开发者/项目管理)→ 切到 `style-linear.md`
- 想要**白底编辑式**(支付/金融/营销)→ 切到 `style-stripe.md`
- 想要**极客纯黑**(hosting/平台)→ 切到 `style-vercel.md`
- Notion 风适合**给非工程师的产品**——知识管理、笔记、协作、教育、消费者 App。**绝禁**用在企业后台、数据密集 dashboard、工程工具——那会显得不够严肃。
