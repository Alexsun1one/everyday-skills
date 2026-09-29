# Style DNA — Stripe 风(白底编辑式 / 可信金融科技)

> 支付、金融、SaaS 营销落地页的事实标准。Stripe 风的关键不是"好看",而是**可信感是通过一层层铺出来的**——白底+sohne-var 300 字重+单紫 accent+渐变 hero+真实产品截图当艺术品。每一个决策都传达"我靠谱、不浮夸、不喧哗"。

## 这家风格的灵魂

一句话:**权威靠克制,不靠音量**。

Stripe 的标志性决策是**所有标题用 weight 300**(不是粗体)——这是反常规选择。整个行业默认标题用粗体,Stripe 用 300 字重 + aggressive negative tracking(-0.020em 或更紧),传达"低声说话的权威"。配上单紫 `#533afd` accent + 编辑式留白 + 渐变 hero halo + 真实产品截图当艺术品,整体读起来像"由世界级字体铸造厂重新设计的金融机构"。

## 1. 配色策略

### 配色哲学:近单色画布 + 单紫 accent + 渐变装饰

| 类别 | Token | Hex | 用途 |
|---|---|---|---|
| Canvas | `color.canvas` (Mist) | `#E5EDF5` | 页面背景(冷调 off-white,**不是纯白**——纯白显冰冷) |
| Surface | `color.surface` | `#FFFFFF` | 卡片、面板 |
| Primary text | `color.ink` (Midnight Ink) | `#061B31` | 主文本、nav ink、深 CTA 文字(近黑蓝,**绝不纯黑**) |
| Secondary text | `color.steel` | `#50617A` | 次文本 |
| Tertiary text | `color.slate` | `#64748D` | 弱文本、eyebrow label |
| Quaternary text | `color.pewter` | `#7D8BA4` | footer 链接 |
| Border | `color.mist` | `#E5EDF5` | 1px 发丝线、卡片边框 |
| **Accent (唯一)** | **`color.electric-iris`** | **`#533AFD`** | **每屏一个 primary CTA、active nav、品牌焦点——画布上唯一允许承重的饱和色** |
| Accent hover | `color.lumen-violet` | `#8087FF` | hover/active wash、次链接、icon accent、soft brand halo |
| Gradient 端 | `color.dawn-bloom` | `radial-gradient(circle, rgb(127,125,252), rgb(244,75,204) 33%, rgb(229,237,245) 66%)` | hero gradient wash 的品红对位 |
| Gradient 起点 | `color.spectrum-veil` | `linear-gradient(90deg, rgb(114,50,241) 3.13%, rgb(251,118,250) 50%, rgb(255,207,94))` | 紫→粉→琥珀三色 hero/feature 段 wash |
| Decorative warm | `color.ember` | `#FF6118` | 渐变作品里的暖色 accent——**绝不作为功能 UI 色** |
| Decorative warm | `color.solar` | `#FFBB00` | 渐变高光 wash |
| Outline accent | `color.verdant` | `#81B81A` | 绿色描边 accent for tags、dividers、focused UI edges——**作为支持 accent,不作为状态色** |

### 配色铁律

> **绝不**用第二个饱和色作为 CTA。Ember 和 Solar 是**装饰专用**,不是功能色。
>
> **绝不**用纯白 `#FFFFFF` 作画布背景——用 Mist `#E5EDF5`,冷调 off-white 是品牌一部分。
>
> **绝不**用纯黑 `#000000` 作文字——用 Midnight Ink `#061B31`(近黑蓝)。

## 2. 字体系统

### Font family:sohne-var(单一字体管全部)

| Token | Family | 用途 |
|---|---|---|
| `font.display` | sohne-var + OpenType `ss01` + `tnum` | 所有——display、headline、body、UI label、按钮 |

> **必须开 `ss01`(alternate g)和 `tnum`(tabular numbers)**。sohne-var 是付费字体(Stripe 自有),免费替代用 Inter 变量 + weight 300(气质接近但不是 sohne)。

### Weight system(Stripe 的字体签名)

| Weight | 用途 |
|---|---|
| **300** | **所有 display 和 headline——反常规的"低声权威"** |
| 400 | body、UI label、按钮文字 |

> **绝禁 weight 600+** 用于标题——破坏低声权威体系。Stripe 的所有 H1/H2/H3 都是 300。这是 Stripe 最辨识的字体决策。

### Tracking(同样负、紧)

| 字号 | letter-spacing |
|---|---|
| 44-56px (display) | -0.025em 到 -0.030em |
| 34-48px (h1/h2) | -0.020em 或更紧 |
| body | 0 |
| eyebrow label | 0.12em uppercase |

> body 永远 0 或更紧——**绝不松于 0**。

### Gradient text(Stripe 签名)

所有 H1 和多数 H2 在营销页用 **gradient text fill**:`linear-gradient(Electric Iris #533AFD → Steel #50617A)`,创造"左亮右暗"效果。次要子句可保留实色 Midnight Ink 形成对比。

## 3. 圆角阶梯——只用 4px

| Token | Value | 用途 |
|---|---|---|
| `radius.all` | **4px** | **所有**——按钮、卡片、输入、tag、badge、pill |

> **绝不**用 8px+ 圆角在 Stripe 风。4px 是 Stripe 的硬规矩。所有元素对齐到这一个值。

## 4. 阴影 / elevation 哲学

### 核心原则:**平面优先,阴影仅给浮空 mockup**

> **绝不**给按钮、nav、标准卡片加 drop shadow。**阴影仅给浮空产品 mockup 和下拉菜单**。

### 4 档 Shadow

| Name | Value | 用途 |
|---|---|---|
| `shadow-sm` | `rgba(23, 23, 23, 0.06) 0px 3px 6px 0px` | 微弱浮空 |
| `shadow-xl-3` | `rgba(23, 23, 23, 0.08) 0px 15px 35px 0px` | 标准浮空 mockup |
| `shadow-xl-2` | `rgba(50, 50, 93, 0.12) 0px 16px 32px 0px` | 下拉菜单、popover |
| `shadow-xl` | `rgba(0, 0, 0, 0.2) 0px 0px 32px 8px` | 浮空产品 mockup(大、软、深) |

### Focus ring(不是 outline)

focus state 用 box-shadow:`rgba(99, 91, 255, 0.1) 0px 0px 0px 3px`(蓝色调 3px halo)。

## 5. 间距气质——编辑式留白

| 用途 | 值 |
|---|---|
| page max-width | 1200px |
| section gap | 80px |
| card padding | 24px |
| element gap | 16px |
| nav 高度 | 64px |
| nav 项 gap | 8px |
| eyebrow 到 headline | 16px |
| section body padding | 48-64px |

## 6. 动效曲线

| Property | Duration | Timing |
|---|---|---|
| color / fill / stroke / opacity | 0.3s | `cubic-bezier(0.25, 1, 0.5, 1)` |
| transform(标准) | 0.3s | `cubic-bezier(0.25, 1, 0.5, 1)` |
| transform(复杂) | 0.6s-0.8s | `cubic-bezier(0.16, 1, 0.3, 1)` 或 `cubic-bezier(0.165, 0.84, 0.44, 1)` |
| opacity 快 | 0.15s | linear |
| micro | 0.12s | ease |

## 7. 图标体系——绑定 Heroicons

**强制图标库:Heroicons**(Tailwind 团队官方,292 icons,outline 1.5px stroke / solid,24×24,深度绑定 Tailwind 生态)。

| 场景 | Heroicons 用法 |
|---|---|
| 按钮 icon | 16px,stroke 1.5px,outline 风格 |
| nav icon | 20px |
| ghost link icon | 18-20px,圆形 soft-gray 容器 |
| feature card icon | 24px,outline,放在 small circular container |

**严禁混用其他库**。Stripe 风的 iconography 极克制——line-based,1.5px stroke,mono-color(Slate 或 Midnight Ink),**绝不**用 emoji 或多彩 icon。详细见 `icon-systems.md`。

## 8. 签名组件(Stripe 风独有的"人做的"证据)

### Primary CTA Button(签名)
- 实色 Electric Iris `#533AFD` 填充
- 白色文字
- 4px radius
- padding `12px 16px`
- sohne-var 14-16px weight 400
- **trailing arrow glyph**(12px,inline arrow slot)——**这是 Stripe 按钮的签名**
- hover 用 10% 白色 overlay 提亮
- **绝无 drop shadow**

### Gradient Text Headline(签名)
- sohne-var 44-56px weight 300
- letter-spacing `-0.025em` 到 `-0.030em`
- fill 是 `linear-gradient(Electric Iris #533AFD → Steel #50617A)`(左亮右暗)
- 用于所有顶级页面标题
- 次要子句可保留实色 Midnight Ink

### Hero Gradient Halo(签名)
- 全屏 radial gradient 从 Electric Iris → magenta `#F72DF3` → Ember `#FF6118` → 溶入 Mist canvas
- 作为 background-layer blob,soft mask clip
- **总是**定位在右侧或标题文字背后
- 不是内容背景,是氛围光

### Floating Product Mockup(签名)
- 真实产品 UI(手机、checkout、dashboard)当作艺术品
- 浮在 card 表面 16-24px 上方
- soft shadow `rgba(0,0,0,0.2) 0px 0px 32px 8px`
- **绝不交互**——是插图

### Eyebrow Label
- sohne-var 12px weight 400
- Slate `#64748D`
- letter-spacing `0.12em` uppercase
- **无 bullet,无 dot**——只有文字
- 距下方 headline 16px

### Customer Logo Strip
- 单行,均匀分布
- 灰度 logo,24-32px 高,视觉重量一致
- **无 caption,无 divider,无 background**

## 9. 反塑料证据(Stripe 风的"人做的"信号)

- [ ] **所有标题 weight 300**(不是 500/600)
- [ ] **tracking -0.020em 或更紧** 在 display
- [ ] **gradient text headline**(Iris→Steel linear-gradient)
- [ ] **canvas 是 Mist `#E5EDF5`**(不是纯白)
- [ ] **文字是 Midnight Ink `#061B31`**(不是纯黑)
- [ ] **每屏一个 Electric Iris CTA**(不竞争)
- [ ] **按钮有 trailing arrow glyph**
- [ ] **绝禁按钮/nav/标准卡片 drop shadow**(只给浮空 mockup)
- [ ] **圆角全部 4px**(不混 8/12)
- [ ] **hero gradient halo 在右侧**
- [ ] **真实产品截图当艺术品**(不是抽象 icon)
- [ ] **sohne-var + ss01 + tnum**(或 Inter 300 替代)

## 10. 反派警示

| 塌成的塑料样 | 病因 | 修复 |
|---|---|---|
| 看起来像通用 SaaS 营销页 | 标题用了 500/600 字重 | 改 weight 300 |
| 像贴纸浮起 | 给按钮加了 drop shadow | 删掉——Stripe 按钮平 |
| 像彩虹 | 多个饱和 CTA | 每屏只一个 Electric Iris |
| 冰冷 | 纯白背景 | 改 Mist `#E5EDF5` |
| 像通用 dashboard | 没 gradient text headline | 加 Iris→Steel gradient fill |
| 像廉价模板 | 用了 emoji icon | 改 Heroicons line-based |
| 圆角杂乱 | 按钮 8px / 卡片 12px 混用 | 全部统一 4px |

## Prompt Fragment(可复制)

### English

```text
Visual style: Stripe-inspired (white-canvas, fintech editorial, whisper-authority).

COLOR:
- canvas: Mist #E5EDF5 (cool off-white, NEVER pure #FFFFFF)
- surface: #FFFFFF for cards
- text: Midnight Ink #061B31 (near-black blue, NEVER pure #000)
- secondary text: Steel #50617A; tertiary Slate #64748D; footer Pewter #7D8BA4
- ONE accent: Electric Iris #533AFD (per-viewport one primary CTA only)
- accent hover: Lumen Violet #8087FF
- gradient endpoints: Dawn Bloom (radial Iris→magenta→mist), Spectrum Veil (linear Iris→pink→amber)
- decorative warm: Ember #FF6118, Solar #FFBB00 (artwork ONLY, never functional UI)
- border: 1px Mist #E5EDF5

TYPOGRAPHY (Stripe's signature whisper-authority):
- font: sohne-var with font-feature-settings: "ss01", "tnum" (alternate g, tabular numbers)
  free alternative: Inter Variable at weight 300 (close but not identical)
- ALL HEADLINES at weight 300 (NOT 500/600 — this is the most recognizable Stripe choice)
- body/UI/buttons at weight 400
- tracking: display 44-56px → -0.025em to -0.030em; h1/h2 → -0.020em or tighter; body → 0
- gradient text headline: fill = linear-gradient(Electric Iris #533AFD → Steel #50617A), left-bright/right-dim
- eyebrow label: 12px weight 400 Slate, letter-spacing 0.12em UPPERCASE, no bullet/dot

RADIUS: 4px everywhere (buttons, cards, inputs, tags, badges) — NEVER 8px+

ELEVATION (flat-first):
- NO drop shadows on buttons, nav, or standard cards
- shadows ONLY for floating mockups and dropdowns:
  - shadow-sm: rgba(23,23,23,0.06) 0px 3px 6px 0px (subtle float)
  - shadow-xl-3: rgba(23,23,23,0.08) 0px 15px 35px 0px (standard mockup)
  - shadow-xl-2: rgba(50,50,93,0.12) 0px 16px 32px 0px (dropdowns/popovers)
  - shadow-xl: rgba(0,0,0,0.2) 0px 0px 32px 8px (large floating product mockup)
- focus: rgba(99,91,255,0.1) 0px 0px 0px 3px (3px iris halo, NOT outline)

LAYOUT (editorial):
- page max-width: 1200px
- section gap: 80px
- card padding: 24px
- element gap: 16px
- nav: 64px tall, 8px between items

SIGNATURE COMPONENTS:
- Primary CTA: filled #533AFD, white text, 4px radius, padding 12px 16px, sohne-var 14-16px weight 400, TRAILING ARROW GLYPH (12px inline arrow), hover 10% white overlay, NO shadow
- Gradient Headline: 44-56px weight 300, -0.025em to -0.030em, linear-gradient(Iris→Steel) fill
- Hero Halo: radial-gradient(Iris→magenta→Ember→mist), right-edge clipped, atmosphere only
- Product Mockup: real UI as art, 16-24px above card, shadow rgba(0,0,0,0.2) 0px 0px 32px 8px, NEVER interactive
- Eyebrow: 12px weight 400 Slate, 0.12em UPPERCASE, no bullet, 16px gap to headline
- Customer Logo Strip: single row, grayscale logos 24-32px, no caption/divider/bg

MOTION:
- color/fill/stroke/opacity: 0.3s cubic-bezier(0.25, 1, 0.5, 1)
- transform: 0.3s same easing, or 0.6-0.8s cubic-bezier(0.16, 1, 0.3, 1) for complex
- micro opacity: 0.12-0.15s

ICONS: Heroicons ONLY (Tailwind team, 292 icons, 1.5px stroke, 24×24)
- button: 16px outline; nav: 20px; ghost link: 18-20px in circular soft-gray container
- NEVER mix libraries, NEVER emoji, NEVER multi-color icons

NEVER:
- use weight 600+ for headlines
- use pure #FFFFFF as canvas (use Mist #E5EDF5)
- use pure #000 as text (use Midnight Ink #061B31)
- use 8px+ radius (use 4px)
- add drop shadows to buttons/nav/cards
- use Ember/Solar as functional CTA color (decorative only)
- use second saturated CTA same viewport
- use emoji icons or multi-color icons
```

### 中文

```text
视觉风格:Stripe 风(白底编辑式,可信金融科技,低声权威)。

配色:
- 画布:Mist #E5EDF5(冷调 off-white,绝不用纯 #FFFFFF)
- 表面:#FFFFFF 用于卡片
- 文字:Midnight Ink #061B31(近黑蓝,绝不用纯 #000)
- 次文本:Steel #50617A;弱:Slate #64748D;footer:Pewter #7D8BA4
- 单 accent:Electric Iris #533AFD(每屏一个 primary CTA)
- accent hover:Lumen Violet #8087FF
- 渐变端:Dawn Bloom(radial Iris→品红→mist)、Spectrum Veil(linear Iris→粉→琥珀)
- 装饰暖色:Ember #FF6118、Solar #FFBB00(仅艺术品,绝不功能 UI)
- 边框:1px Mist #E5EDF5

字体(Stripe 签名"低声权威"):
- 字体:sohne-var + font-feature-settings: "ss01", "tnum"(变体 g,等宽数字)
  免费替代:Inter 变量 weight 300(接近但不一致)
- 所有标题 weight 300(不是 500/600——这是最辨识的 Stripe 决策)
- body/UI/按钮 weight 400
- tracking:display 44-56px → -0.025em 到 -0.030em;h1/h2 → -0.020em 或更紧;body → 0
- gradient text headline:fill = linear-gradient(Electric Iris #533AFD → Steel #50617A),左亮右暗
- eyebrow label:12px weight 400 Slate,letter-spacing 0.12em 大写,无 bullet/dot

圆角:全部 4px(按钮、卡片、输入、tag、badge)——绝不用 8px+

ELEVATION(平面优先):
- 绝不给按钮、nav、标准卡片加 drop shadow
- 阴影仅给浮空 mockup 和下拉:
  - shadow-sm:rgba(23,23,23,0.06) 0px 3px 6px 0px(微弱浮空)
  - shadow-xl-3:rgba(23,23,23,0.08) 0px 15px 35px 0px(标准 mockup)
  - shadow-xl-2:rgba(50,50,93,0.12) 0px 16px 32px 0px(下拉/popover)
  - shadow-xl:rgba(0,0,0,0.2) 0px 0px 32px 8px(大浮空产品 mockup)
- focus:rgba(99,91,255,0.1) 0px 0px 0px 3px(3px iris halo,不是 outline)

布局(编辑式):
- 页面 max-width:1200px
- 段间隙:80px
- 卡片 padding:24px
- 元素 gap:16px
- nav:64px 高,项间 8px

签名组件:
- Primary CTA:实色 #533AFD,白字,4px radius,padding 12px 16px,sohne-var 14-16px weight 400,trailing arrow glyph(12px inline 箭头),hover 10% 白色 overlay,无阴影
- Gradient Headline:44-56px weight 300,-0.025em 到 -0.030em,linear-gradient(Iris→Steel) fill
- Hero Halo:radial-gradient(Iris→品红→Ember→mist),右侧 clip,氛围光
- Product Mockup:真实 UI 当艺术品,浮 card 上 16-24px,shadow rgba(0,0,0,0.2) 0px 0px 32px 8px,绝不交互
- Eyebrow:12px weight 400 Slate,0.12em 大写,无 bullet,距 headline 16px
- Customer Logo Strip:单行,灰度 logo 24-32px,无 caption/divider/底色

动效:
- color/fill/stroke/opacity:0.3s cubic-bezier(0.25, 1, 0.5, 1)
- transform:0.3s 同 easing,或 0.6-0.8s cubic-bezier(0.16, 1, 0.3, 1) 复杂场景
- micro opacity:0.12-0.15s

图标:仅 Heroicons(Tailwind 团队,292 icons,1.5px stroke,24×24)
- 按钮:16px outline;nav:20px;ghost link:18-20px 在圆形 soft-gray 容器
- 绝不混库,绝不 emoji,绝不多色 icon

绝对不要:
- 标题用 weight 600+
- 用纯 #FFFFFF 作画布(用 Mist #E5EDF5)
- 用纯 #000 作文字(用 Midnight Ink #061B31)
- 用 8px+ 圆角(用 4px)
- 给按钮/nav/卡片加 drop shadow
- 用 Ember/Solar 作功能 CTA 色(仅装饰)
- 同视口两个饱和 CTA
- 用 emoji 或多色 icon
```

## 权威信源

- designmd.cc/benchmarks/stripe
- duply.ai/stripe/design-md(完整 DESIGN.md)
- stripe.design(官方 design language study)
- styles.refero.design/style/48e5de76
- open-design.ai/systems/stripe

## 与其他风格的关系

- 想要**深色工程工具**(开发者/项目管理)→ 切到 `style-linear.md`
- 想要**温暖反流派**(知识/协作/教育)→ 切到 `style-notion.md`
- 想要**极客纯黑**(hosting/平台)→ 切到 `style-vercel.md`
- Stripe 风适合**营销落地页、支付流程、金融产品**——产品内 UI 通常切到 Linear 风(深色)或保持 Stripe 浅色变体。
