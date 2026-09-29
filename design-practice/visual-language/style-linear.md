# Style DNA — Linear 风(深色优先 / 严肃工程工具)

> 2026 年事实上的 SaaS 视觉公约。70% 新 B2B SaaS 采用其变体。当用户没指定风格时,**默认用这一家**。这一家也是 skill 冻结最深的一家——从配色到字重到动效曲线,精确到 hex 和 cubic-bezier。

## 这家风格的灵魂

一句话:**严肃工程工具,节制即高级**。

Linear 的视觉系统建立在一个克制的信念上——"给工程师用的软件,必须像工具本身一样精确、快速、不装饰"。它的视觉决策全部从这个信念长出来:近黑画布(不是纯黑)、单一 violet accent(不是多色)、Inter var 510 字重(不是 500 也不是 600)、luminance stacking(不是 drop shadow)。每一条都是"反塑料"证据。

## 1. 配色策略

### 配色哲学:单 accent 制

整个系统**只有一个 chromatic color**——Linear violet `#5E6AD2`。它出现在:品牌标记、focus ring、每屏一个 primary CTA、链接。**绝不**出现在:装饰、渐变、多个按钮、背景 wash。其他全是冷灰中性阶。

> 反塑料证据:`#5E6AD2` 每屏出现不超过 3 次。如果出现 5+ 次,就是塑料(没有节制的彩虹)。

### 完整 token 表(dark 默认)

| Token | Hex | 用途 |
|---|---|---|
| `color.canvas` | `#08090A` | 营销页画布(近黑,带微蓝调,绝不用纯 #000000) |
| `color.surface.base` | `#0F1011` | 应用基础面板 |
| `color.surface.level2` | `#141516` | 抬升卡片 |
| `color.surface.level3` | `#18191A` | 二级面板 |
| `color.surface.level4` | `#191A1B` | popover、modal 容器 |
| `color.surface.raised` | `#1F2023` | 卡片、输入框填充、hover 表面 |
| `color.text.primary` | `#F7F8F8` | 主文本(AAA on canvas) |
| `color.text.secondary` | `#D0D6E0` | 次文本 |
| `color.text.tertiary` | `#8A8F98` | 弱文本、元数据、时间戳 |
| `color.text.disabled` | `#62666D` | 禁用 |
| `color.brand.primary` | `#5E6AD2` | **唯一 chromatic accent**——链接、focus、primary CTA |
| `color.brand.hover` | `#828FFF` | brand hover(更亮) |
| `color.brand.pressed` | `#4B57C8` | brand pressed(更深) |
| `color.danger` | `#EB5757` | 错误 |
| `color.warning` | `#F2C94C` | 警告 |
| `color.success` | `#4CB782` | 成功(偏青绿,不是纯绿) |
| `color.border.default` | `rgba(255,255,255,0.05)` | 标准分隔 |
| `color.border.strong` | `rgba(255,255,255,0.08)` | 强分隔 |
| `color.border.hairline` | `#2A2E33` | 1px 发丝线 |
| `color.border.micro` | `rgba(255,255,255,0.02)` | 几乎不可见 |
| `color.inset.light` | `rgba(0,0,0,0.03)` | 凹陷面板浅阴影 |
| `color.inset.deep` | `rgba(0,0,0,0.4)` | 凹陷面板深阴影 |
| `color.overlay` | `rgba(0,0,0,0.5)` | modal/dialog 遮罩 |

### Light 模式变体

把 canvas→`#FFFFFF`、surface→`#F7F8F8`、text.primary→`#1A1B1E`、border→`#E5E7EB`。accent `#5E6AD2` 不变。

> Linear 是 dark 默认,light 是次要支持。**反过来做就塌了**。

## 2. 字体系统

### Font family

| Token | Family | 用途 |
|---|---|---|
| `font.ui` | Inter Variable + OpenType `cv01` (single-story a) + `ss03` (geometric alternates) | 所有 UI |
| `font.mono` | Berkeley Mono | 代码、键盘键(⌘K 芯片)、行内 ID |

> **必须开 `cv01` 和 `ss03`**——不开就是通用 Inter,开完就是 Linear 的几何工程感。`font-feature-settings: "cv01", "ss03";`

### Weight system(Linear 的字重签名)

| Weight | 值 | 角色 |
|---|---|---|
| `weight.deemphasis` | 300 | 弱 |
| `weight.body` | 400 | 正文 |
| **`weight.ui`** | **510** | **UI 强调——Linear 最辨识的字重决策** |
| `weight.semibold` | 590 | 标题、强调 |

> **weight 510 是 Linear 最辨识的字体决策。** 它精确卡在 Regular (400) 和 Semibold (600) 之间,只有 Inter Variable 的连续字重轴能取到。500 太轻,600 太重,**只有 510 对**。CSS:`font-variation-settings: 'wght' 510;`。任何代替(500/600)都会塌。

### Progressive tracking(大字紧、小字松)

Linear 对字号施加成比例的负字间距——大字越紧,小字回正。补偿大字母看起来过松的视错觉。

| 字号 | letter-spacing |
|---|---|
| 64-80px (display) | -1.5px 到 -3.0px |
| 48px (h1) | -0.96px |
| 32px (h2) | -0.5px |
| 24px (h3) | -0.22px |
| 20px (h4) | -0.1px |
| 16px (body) | 0 |
| <16px | 0 |

> 不开 progressive tracking = 大字看起来散,塑料信号。

### 完整字号阶梯

| Token | Size | Weight | LH | LS | 用途 |
|---|---|---|---|---|---|
| `t-display` | 64-80px | 590 | 1.05 | -1.5~-3.0 | 营销 hero |
| `t-h1` | 48px | 590 | 1.1 | -0.96px | 页面主标题 |
| `t-h2` | 32px | 590 | 1.15 | -0.5px | 分区标题 |
| `t-h3` | 24px | 590 | 1.2 | -0.22px | 子标题 |
| `t-h4` | 20px | 510 | 1.3 | -0.1px | 段落标题 |
| `t-body` | 16px | 400 | 1.5 | 0 | 正文 |
| `t-body-sm` | 15px | 400 | 1.55 | 0 | 紧凑正文(Linear 著名的 15px/1.6) |
| `t-label` | 14px | 510 | 1.4 | 0 | UI 标签、按钮 |
| `t-meta` | 13px | 400 | 1.4 | 0 | 元数据 |
| `t-micro` | 12px | 400 | 1.4 | 0 | timestamp、小标签 |
| `t-mono` | 14px | 510 | 1.4 | 0 | 代码、键盘键(Berkeley Mono) |

## 3. 圆角阶梯(Linear 只用三档)

| Token | Value | 用途 |
|---|---|---|
| `radius.xs` | 4px | 键盘键、小芯片 |
| `radius.control` | 6px | **所有控件**(按钮、输入框、chip) |
| `radius.container` | 12px | 卡片、面板、modal |
| `radius.pill` | 9999px | 仅头像、pill badge |

> **不要用 8px。** Linear 严格守 6/12/9999。用 8px 就是不像 Linear。

## 4. 阴影 / elevation 哲学 —— Luminance Stacking

### 核心原则

> **关键概念:** 在深色优先系统里,没有头顶光源向下投射阴影。标准 `box-shadow` 在深色背景上看起来不自然、沉重。Linear 改用 **luminance stacking**——抬升的元素用**更亮(more luminous)的背景**。一个 popover 之所以"在上面",不是因为它有阴影,而是因为它的表面更亮。
>
> 阴影**只**用于浮层(Level 3+),且是多 Semi-transparent 层叠加,不是单层强阴影。关键洞察:`rgba(0,0,0,...)` 阴影在浅色主题有效,但在深色主题看起来像打了个洞。`rgba(255,255,255,...)` 背景叠加创造真实深度。

### 6 级 Elevation

| Level | 用途 | Background | Border | Shadow |
|---|---|---|---|---|
| 0 — Canvas | 营销页基础 | `#08090A` | none | none |
| 1 — Surface | 应用基础面板 | `#0F1011` | none | none |
| 2 — Card | 抬升卡片 / 内容区 | `rgba(255,255,255,0.05)` 应用于 Level 1 | `rgba(255,255,255,0.05)` | none(靠 luminance) |
| 3 — Popover | 下拉、tooltip 容器 | `#191A1B` | `rgba(255,255,255,0.08)` | `rgba(0,0,0,0.15) 0 4px 12px, rgba(0,0,0,0.2) 0 8px 24px, inset 0 0 0 1px rgba(255,255,255,0.08)` |
| 4 — Modal | 对话框、modal 容器 | `#191A1B` | `rgba(255,255,255,0.08)` | `rgba(0,0,0,0.2) 0 0 0px 100vmax, rgba(0,0,0,0.3) 0 16px 48px, inset 0 0 0 1px rgba(255,255,255,0.1)` |
| 5 — Recessed | 凹陷面板(下沉感) | `rgba(0,0,0,0.2)` 应用于容器 | `rgba(0,0,0,0.3)` | `inset 0 0 0 1px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3)` |

### 6 个 Shadow token

| Token | Value |
|---|---|
| `shadow-none` | none |
| `shadow-card` | none(Level 2 仅 luminance) |
| `shadow-popover` | `rgba(0,0,0,0.15) 0 4px 12px, rgba(0,0,0,0.2) 0 8px 24px, inset 0 0 0 1px rgba(255,255,255,0.08)` |
| `shadow-modal` | `rgba(0,0,0,0.2) 0 16px 48px, rgba(0,0,0,0.3) 0 32px 72px, inset 0 0 0 1px rgba(255,255,255,0.1)` |
| `shadow-inset` | `inset 0 0 0 1px rgba(0,0,0,0.4), inset 0 2px 4px rgba(0,0,0,0.3)` |
| **`shadow-focus`** | **`0 0 0 2px rgba(94,106,210,0.4), 0 0 0 4px rgba(94,106,210,0.2)`** —— **双层 box-shadow,所有交互元素的 focus ring** |

### Surface lift gradient

抬升面板用这个 gradient(模拟 luminance stacking):
`linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%)`

### Top bar 毛玻璃

顶栏:`background: rgba(8,9,10,0.85); backdrop-filter: blur(12px) saturate(180%);`

## 5. 间距气质——紧、密、工具感

Linear 用 4px 网格,但**用得紧**——8px 内组件、16px 区块、24-32px 段、80-96px 营销 band。营销页是"段间极大空间、段内极高密度"的对比。**不像 Notion 那样处处呼吸**——Linear 是仪表盘密度。

| 用途 | 值 |
|---|---|
| 图标-文字间隙 | 6-8px |
| 组件内 padding | 12-16px |
| 元素标准间隙 | 8-12px |
| 卡片/容器内边距 | 24px |
| 段落间隙 | 40-48px |
| 营销 band 间隙 | 96-160px |

## 6. 动效曲线 —— Linear 的动效哲学

### 哲学:**受控、利落、绝不弹性**

> Linear 动画**快、精确、绝不俏皮**。交互模型是专业工具——每个过渡必须感觉即时、有目的。**没有 bouncy spring、没有 overshoot、没有 elastic 回弹**。`ease-default`(easeOutQuad)给交互清脆开头 + 平滑收尾;modal 入场用 `ease-enter`(easeOutQuart)自信到达。**如果一个动画引人注意它本身,就是太慢或太弹——裁掉它。**

### 6 档 Duration

| Token | Value | 用途 |
|---|---|---|
| `duration.instant` | 0ms | 即时状态变化 |
| `duration.micro` | 100ms | focus ring 出现、checkbox 勾选 |
| `duration.fast` | 150ms | 按钮 hover、链接颜色、border color |
| `duration.normal` | 200ms | 状态变化、tab 切换、badge 过渡 |
| `duration.moderate` | 300ms | 下拉开、modal 入、面板滑 |
| `duration.slow` | 500ms | 页面过渡、复杂编排 |

### 5 个 Easing 函数

| Token | Value | 用途 |
|---|---|---|
| `ease.default` | `cubic-bezier(0.25, 0.46, 0.45, 0.94)` | easeOutQuad——通用过渡(Linear 主力) |
| `ease.enter` | `cubic-bezier(0.165, 0.84, 0.44, 1)` | easeOutQuart——modal/popover 入场 |
| `ease.material` | `cubic-bezier(0.4, 0, 0.2, 1)` | Material 默认,用于重定位 |
| `ease.in` | `cubic-bezier(0.4, 0, 1, 1)` | 元素退场——减速退 |
| `ease.out` | `cubic-bezier(0, 0, 0.2, 1)` | 元素入场——不弹 |

> **绝禁:** `cubic-bezier(0.34, 1.56, 0.64, 1)`(spring/bounce)。Linear 是工作工具——弹跳动画破坏专业、专注氛围。

### 常见过渡查表

| 交互 | Property | Duration | Easing |
|---|---|---|---|
| 按钮 hover bg | `background-color` | 150ms | ease-default |
| 按钮按下 | `transform (scale 0.98)` | 100ms | ease-material |
| focus ring 出现 | `box-shadow` | 100ms | ease-default |
| 输入框 focus border | `border-color, box-shadow` | 150ms | ease-default |
| 卡片 hover | `background-color` | 150ms | ease-default |
| 下拉开 | `opacity, transform (translateY -4px→0)` | 200ms | ease-enter |

## 7. 图标体系——绑定 Lucide

**强制图标库:Lucide** (1500+ 图标,MIT,24×24 网格,2px stroke,active 维护的 Feather fork)。

| 场景 | Lucide 用法 |
|---|---|
| 按钮 icon | 16px (`size-4`),stroke 2px,与文字 gap 8px |
| 导航 icon | 18px (`size-[18px]`),stroke 2px,激活态用 accent 色 |
| 输入框前后 icon | 16px,gray-500 |
| 表格行操作 icon | 16px,ghost,行 hover 时淡入 |
| toolbar icon | 20px (`size-5`),stroke 2px |

**严禁:** 引入第二个图标库(Phosphor、Heroicons、react-icons)。混用是 amateur 信号——不同 stroke 宽度、不同网格、不同视觉重量,在同一界面里看起来就是杂牌军。如果 Lucide 没有需要的图标,**自定 SVG 匹配 Lucide 风格**(24×24、2px stroke、round caps),不要引入第二个库。

详见 `icon-systems.md`。

## 8. 反塑料证据(Linear 风的"人做的"信号)

这是验收 Linear 风产物"是不是塑料"的清单。每条都要勾到。

- [ ] **weight 510**(不是 500、不是 600)——开 `font-variation-settings: 'wght' 510`
- [ ] **OpenType `cv01` + `ss03`** 开启
- [ ] **progressive tracking**(大字负、小字零)
- [ ] **luminance stacking**(深色模式抬升靠提亮表面,不是 drop shadow)
- [ ] **单 accent 制**(`#5E6AD2` 每屏 ≤3 次)
- [ ] **focus ring 双层 box-shadow**(`0 0 0 2px rgba(94,106,210,0.4), 0 0 0 4px rgba(94,106,210,0.2)`)
- [ ] **pressed scale 0.98**(不是 0.95、不是 1)
- [ ] **6 级 elevation**(不是一层 box-shadow 打天下)
- [ ] **圆角 6/12/9999**(不用 8)
- [ ] **顶栏 backdrop-filter blur(12px) saturate(180%)**
- [ ] **绝禁 bounce easing**
- [ ] **单 Lucide 图标库**(不混)

## 9. 反派警示(Linear 风最容易塌成什么塑料样)

| 塌成的塑料样 | 病因 | 修复 |
|---|---|---|
| 看起来像通用深色 SaaS | weight 用了 500/600 而不是 510 | 改 `font-variation-settings: 'wght' 510` |
| 像贴纸 | 用了 drop shadow 而不是 luminance stacking | 抬升元素用 `rgba(255,255,255,0.05)` 背景 |
| 彩虹 | `#5E6AD2` 出现在 5+ 处 | 每屏 accent ≤3 次 |
| 模糊焦点 | focus ring 用单层 outline | 改双层 box-shadow(2px+4px) |
| 太俏皮 | 用了 bounce/spring easing | 换 ease-default / ease-enter |
| 杂牌图标 | Lucide + Heroicons 混用 | 全部 Lucide |
| 不像 Linear 像通用 dashboard | 没开 cv01/ss03 | `font-feature-settings: "cv01", "ss03"` |

## Prompt Fragment(可复制)

### English

```text
Visual style: Linear-inspired (dark-first, precision tool aesthetic).

COLOR (single-accent discipline):
- canvas: #08090A (near-black with blue cast, NEVER pure #000)
- surface ladder: #0F1011 → #141516 → #18191A → #191A1B → #1F2023
- text: primary #F7F8F8 / secondary #D0D6E0 / tertiary #8A8F98 / disabled #62666D
- ONE chromatic accent: #5E6AD2 (Linear violet) — appears ≤3 times per screen (focus ring, primary CTA, brand)
- border: default rgba(255,255,255,0.05), hairline #2A2E33
- semantic: danger #EB5757, warning #F2C94C, success #4CB782 (never pure green)
- light variant: canvas #FFFFFF, surface #F7F8F8, text #1A1B1E, border #E5E7EB

TYPOGRAPHY (Linear's signature):
- font: Inter Variable with font-feature-settings: "cv01", "ss03" (geometric alternates — non-negotiable)
- mono: Berkeley Mono for code, keyboard keys (⌘K chips), inline IDs
- WEIGHT 510 for UI emphasis — font-variation-settings: 'wght' 510 (NOT 500, NOT 600)
- weight 590 for headings, 400 for body, 300 for de-emphasis
- progressive tracking: 64px → -1.5px; 48px → -0.96px; 32px → -0.5px; 24px → -0.22px; ≤16px → 0
- body: 15px / 1.6 (Linear's famous tight reading rhythm)

ELEVATION (luminance stacking — CRITICAL):
- in dark mode: elevated elements have BRIGHTER bg (rgba(255,255,255,0.05)), NOT drop shadows
- drop shadows ONLY for Level 3+ floating (popover/modal), and they are MULTI-LAYER semi-transparent
- 6 levels: Canvas #08090A → Surface #0F1011 → Card rgba(255,255,255,0.05) → Popover #191A1B → Modal #191A1B → Recessed rgba(0,0,0,0.2)
- shadow.focus = 0 0 0 2px rgba(94,106,210,0.4), 0 0 0 4px rgba(94,106,210,0.2) — DOUBLE-LAYER box-shadow
- top bar: background rgba(8,9,10,0.85); backdrop-filter: blur(12px) saturate(180%)

RADIUS (only 3 values):
- controls: 6px (buttons, inputs, chips) — NEVER 8px
- containers: 12px (cards, panels, modals)
- pills: 9999px (avatars, status badges only — NEVER primary buttons)

SPACING (4px grid, dense tool feel):
- icon-text gap: 6-8px
- component padding: 12-16px
- element gap: 8-12px
- card padding: 24px
- section gap: 40-48px
- marketing band gap: 96-160px

MOTION (controlled, snappy, NEVER bouncy):
- 6 durations: 0ms / 100ms / 150ms / 200ms / 300ms / 500ms
- ease.default = cubic-bezier(0.25, 0.46, 0.45, 0.94) (easeOutQuad)
- ease.enter = cubic-bezier(0.165, 0.84, 0.44, 1) (easeOutQuart, for modal/popover)
- pressed scale: 0.98 (NOT 0.95, NOT 1)
- FORBIDDEN: cubic-bezier(0.34, 1.56, 0.64, 1) (spring/bounce)

ICONS:
- Lucide ONLY (1500+ icons, 24×24, 2px stroke, MIT)
- button icon: 16px, gap 8px
- nav icon: 18px, active state uses #5E6AD2
- NEVER mix libraries (no Phosphor, no Heroicons alongside)

NEVER:
- use pure #000000 (use #08090A with blue cast)
- use 500 or 600 weight (use 510)
- skip cv01/ss03 OpenType features
- use drop shadow on cards (use luminance stacking)
- use single-layer outline for focus (use double-layer box-shadow)
- use 8px radius (use 6/12)
- use bounce/spring easing
- mix icon libraries
- show #5E6AD2 more than 3× per screen
```

### 中文

```text
视觉风格:Linear 风(深色优先,精密工具气质)。

配色(单 accent 制):
- 画布:#08090A(近黑带微蓝调,绝不用纯 #000)
- 表面阶梯:#0F1011 → #141516 → #18191A → #191A1B → #1F2023
- 文字:主 #F7F8F8 / 次 #D0D6E0 / 弱 #8A8F98 / 禁用 #62666D
- 单一 chromatic accent:#5E6AD2(Linear 紫)——每屏 ≤3 次(focus、primary CTA、品牌)
- 边框:默认 rgba(255,255,255,0.05),发丝线 #2A2E33
- 语义:danger #EB5757 / warning #F2C94C / success #4CB782(绝不纯绿)
- 浅色变体:画布 #FFFFFF,表面 #F7F8F8,文字 #1A1B1E,边框 #E5E7EB

字体(Linear 签名):
- 字体:Inter Variable + font-feature-settings: "cv01", "ss03"(几何变体——不可省)
- 等宽:Berkeley Mono 用于代码、键盘键(⌘K 芯片)、行内 ID
- 字重 510 用于 UI 强调——font-variation-settings: 'wght' 510(不是 500,不是 600)
- 标题 590,正文 400,弱 300
- progressive tracking:64px → -1.5px;48px → -0.96px;32px → -0.5px;24px → -0.22px;≤16px → 0
- 正文:15px / 1.6(Linear 著名的紧凑阅读节奏)

ELEVATION(luminance stacking——关键):
- 深色模式下:抬升元素用更亮背景(rgba(255,255,255,0.05)),不是 drop shadow
- drop shadow 仅用于 Level 3+ 浮层(popover/modal),且多层 Semi-transparent 叠加
- 6 级:Canvas #08090A → Surface #0F1011 → Card rgba(255,255,255,0.05) → Popover #191A1B → Modal #191A1B → Recessed rgba(0,0,0,0.2)
- shadow.focus = 0 0 0 2px rgba(94,106,210,0.4), 0 0 0 4px rgba(94,106,210,0.2)——双层 box-shadow
- 顶栏:background rgba(8,9,10,0.85);backdrop-filter: blur(12px) saturate(180%)

圆角(只用三档):
- 控件:6px(按钮、输入框、chip)——绝不用 8px
- 容器:12px(卡片、面板、modal)
- pill:9999px(仅头像、状态 badge——绝不主按钮)

间距(4px 网格,密集工具感):
- 图标-文字间隙:6-8px
- 组件 padding:12-16px
- 元素标准间隙:8-12px
- 卡片 padding:24px
- 段间隙:40-48px
- 营销 band 间隙:96-160px

动效(受控、利落,绝不弹):
- 6 档时长:0ms / 100ms / 150ms / 200ms / 300ms / 500ms
- ease.default = cubic-bezier(0.25, 0.46, 0.45, 0.94)(easeOutQuad)
- ease.enter = cubic-bezier(0.165, 0.84, 0.44, 1)(easeOutQuart,modal/popover 入场)
- 按下 scale:0.98(不是 0.95,不是 1)
- 绝禁:cubic-bezier(0.34, 1.56, 0.64, 1)(spring/bounce)

图标:
- 仅 Lucide(1500+,24×24,2px stroke,MIT)
- 按钮 icon:16px,间距 8px
- 导航 icon:18px,激活态用 #5E6AD2
- 绝不混库(不要 Phosphor、不要 Heroicons 并存)

绝对不要:
- 用纯 #000000(用带蓝调的 #08090A)
- 用 500 或 600 字重(用 510)
- 跳过 cv01/ss03 OpenType 特性
- 卡片用 drop shadow(用 luminance stacking)
- focus 用单层 outline(用双层 box-shadow)
- 用 8px 圆角(用 6/12)
- 用 bounce/spring easing
- 混用图标库
- #5E6AD2 每屏出现超 3 次
```

## 权威信源

- designmd.cc/benchmarks/linear
- github.com/soulcore-dev/soul-design-md `designs/linear/DESIGN.md`(1122 行,最完整)
- styles.refero.design/style/90ce5883
- designlang.app/gallery/linear-app
- welovedaily.net "Linear's Brand System — Speed as a Visual Language"

## 与其他风格的关系

- 想要**白底编辑式**(支付/金融/营销)→ 切到 `style-stripe.md`
- 想要**温暖反流派**(知识/协作/教育)→ 切到 `style-notion.md`
- 想要**极客纯黑**(hosting/平台)→ 切到 `style-vercel.md`
- Linear 是默认。其他风格是"故意偏离 Linear"——选其他必须有理由(产品类型、受众、品牌),不是装饰。
