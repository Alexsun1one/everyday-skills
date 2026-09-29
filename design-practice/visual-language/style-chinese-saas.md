# Style DNA — 中文 SaaS 风(微信/知乎/小红书/飞书系)

> skill 默认面向中文产品(见 SKILL.md 第 10 行),但前 4 个风格 DNA 全是西方产品(Linear/Stripe/Notion/Vercel)。当用户的 audience 是**中国大陆消费者、SMB、企业用户**,前 4 个风格会让产品看起来"像海外的",失去本土亲切感。
>
> 这一页冻结中国主流互联网产品的视觉 DNA——不是抄它们,是抽取它们的**视觉判断**:中性色阶配饱和品牌色、PingFang SC 主导、卡片堆叠的"瀑布感"、圆角更柔(8-12px 而不是 Linear 的 6px)、阴影更柔更轻、line-height 给中文留呼吸(1.7-1.8 而不是英文的 1.5)。

## 这家风格的灵魂

一句话:**中性灰底 + 饱和品牌色 + PingFang SC + 柔圆角 + 瀑布卡片 = 中国互联网产品的本土亲切感**。

中文 SaaS 视觉 DNA 的共同点:
- **底色是中性灰白**(不是 Linear 的近黑,也不是 Notion 的奶油)
- **品牌色饱和度高于西方**(微信绿 #07C160、知乎蓝 #0084FF、小红书红 #FE2C55、飞书青 #1456F0)——中国品牌识别靠饱和色,西方靠克制
- **字体以 PingFang SC / 思源黑体为主导**——CJK 字符宽度统一,字重 400/500 为主,绝不用 Inter 主导(Inter 不含中文)
- **圆角偏柔(8-12px)**——比 Linear(6px)柔和,比 Notion(4-8px)圆润,符合中文产品"亲和"气质
- **卡片堆叠瀑布感**——多卡片并列、错落、信息密度高(飞书、小红书、知乎都是)
- **图标偏"装饰性"**——不是 Linear 的几何线、不是 Stripe 的克制,中文产品 icon 多带颜色、带背景圆、更"可爱"
- **line-height 1.7-1.8**——中文字符密度高于英文,行距必须松,否则"挤"

## 1. 配色策略

### 配色哲学:中性灰底 + 饱和品牌色 + 柔和语义色

| 类别 | Token | Hex | 用途 |
|---|---|---|---|
| Canvas | `color.canvas` | `#F5F6F7`(微信灰)/ `#FFFFFF` | 页面背景(微冷调灰白) |
| Surface | `color.surface` | `#FFFFFF` | 卡片、面板 |
| Surface 2 | `color.surface.2` | `#F7F8FA` | 抬升卡片、表格行 hover |
| Primary text | `color.text` | `#1A1A1A` 或 `#1F1F1F` | 主文本(纯近黑) |
| Secondary text | `color.text.secondary` | `#5F6368` 或 `#6B6B6B` | 次文本 |
| Tertiary text | `color.text.tertiary` | `#9AA0A6` | 弱文本 |
| Disabled text | `color.text.disabled` | `#BDC1C6` | 禁用 |
| Border | `color.border` | `#E8EAED` 或 `#EBEBEC` | 1px 发丝线 |
| Border strong | `color.border.strong` | `#DADCE0` | 强边框 |

### 4 大品牌色路由(选一个,不混)

| 品牌色 | Hex | 代表产品 | 气质 |
|---|---|---|---|
| **微信绿 WeChat Green** | `#07C160` | 微信、企业微信、微信支付 | 亲和、支付、社交 |
| **知乎蓝 Zhihu Blue** | `#0084FF` | 知乎、得到 | 知性、问答、内容 |
| **小红书红 Xiaohongshu Red** | `#FE2C55` | 小红书、抖音 | 年轻、潮流、消费 |
| **飞书青 Feishu Blue** | `#1456F0` | 飞书、钉钉、企业 SaaS | 企业、效率、协作 |

> **选哪个看产品类型**——支付/社交→微信绿,知识/内容→知乎蓝,消费/潮流→小红书红,企业/协作→飞书青。**绝不混**。

### 语义色

| Token | Hex | 用途 |
|---|---|---|
| `color.success` | `#00A870` | 成功(偏青绿,不纯绿) |
| `color.warning` | `#FF8800` | 警告 |
| `color.danger` | `#F5483B` 或 `#FA5151` | 错误(中文产品常用 #FA5151,比西方 #EF4444 柔) |
| `color.info` | `#0084FF` | 信息(常与品牌色合并) |

## 2. 字体系统 —— 中文排版核心

### Font family(CJK 必须主导)

```css
font-family:
  -apple-system,          /* iOS/macOS 系统字体 */
  BlinkMacSystemFont,
  "PingFang SC",          /* 苹方,中文 SaaS 默认 */
  "Hiragino Sans GB",     /* macOS 老版回退 */
  "Microsoft YaHei",      /* Windows 微软雅黑 */
  "Source Han Sans CN",   /* 思源黑体跨平台 */
  "Noto Sans CJK SC",     /* Linux 跨平台 */
  sans-serif,
  "Apple Color Emoji",    /* emoji */
  "Segoe UI Emoji";
```

> **铁律:中文产品字体第一栈必须是 PingFang SC,绝不能是 Inter**。Inter 不含中文字符,中文会回退到系统默认,导致中英不协调。中文必须主导,英文作回退。

### Weight system(中文 SaaS 的字重)

| Weight | 用途 |
|---|---|
| 400 | body(中文 Regular) |
| 500 | 强调、UI label、按钮(中文 Medium) |
| 600 | 标题(中文 Semibold) |
| 700 | hero(中文 Bold) |

> 中文不用 weight 510(Linear 的技巧)——中文字符笔画密,400 和 500 之间不需要微调,直接用整百字重。

### 中文排版规则(核心差异)

| 规则 | 西方惯例 | 中文 SaaS | 为什么 |
|---|---|---|---|
| **line-height** | 1.5 | **1.7-1.8** | 中文字符全宽,行距必须松,否则视觉"挤" |
| **letter-spacing** | -0.01em 到 -0.03em(负) | **0 到 +0.02em(正或零)** | 中文不需要负 tracking,反而要微松 |
| **段落 margin** | 16px | **24px(1.5em)** | 中文段落间需要更多呼吸 |
| **首行缩进** | 不缩进 | **不缩进(SaaS 场景)** | 古籍缩进,但 SaaS 不用 |
| **中英混排间距** | 无 | **加 1/4 em 空隙** | 中英字符紧贴视觉不舒服 |
| **标点** | 半角 | **半角(数字/英文)+ 全角(中文)** | 见下方标点规则 |
| **数字** | Inter / Geist Mono | **PingFang SC 或 SF Pro**(中文 SaaS) | 整体协调 |

### 中英混排间距(常被忽略)

```css
/* 中英混排时,自动加 1/4 em 间隙 */
.cn-en-mixed {
  text-autospace: ideograph-alpha;
  text-autospace: ideograph-numeric;
}
```

或手动:中文段落里"使用 React 框架"中间手动加空格(中文 SaaS 写作惯例)。例如:
- ✅ "我们使用 React 框架,提高开发效率 30%。"
- ❌ "我们使用React框架,提高开发效率30%。" (英文/数字紧贴中文,视觉拥挤)

### 标点规则

| 场景 | 正确 | 错误 |
|---|---|---|
| 中文内标点 | 全角(",。!?) | 半角 (",.!?)(英文感) |
| 中英混排中包英文 | 中文外全角,英文内半角 | 全部半角或全部全角 |
| 数字+单位 | "30%"("30%")| "30 %" (空格错) |
| 引号 | 中文用「」或""(中文 SaaS 偏好 "")| 英文 "" |

## 3. 圆角阶梯(中文 SaaS 偏柔)

| Token | Value | 用途 |
|---|---|---|
| `radius.sm` | 6px | tag、badge、小按钮 |
| `radius.md` | 8px | 按钮、输入框(中文 SaaS 主流) |
| `radius.lg` | 12px | 卡片、panel |
| `radius.xl` | 16px | 大卡片、modal |
| `radius.pill` | 9999px | 头像、pill badge |

> 中文 SaaS 圆角普遍**比 Linear 柔**(Linear 6px,中文 SaaS 8-12px),比 Notion 圆(Notion 4-8px,中文 SaaS 8-16px)。这是"亲和"气质的视觉证据。

## 4. 阴影 / elevation 哲学 —— 柔、浅、叠

### 核心原则

中文 SaaS 阴影**比 Linear 柔**(Linear 多层精确),**比 Stripe 多**(Stripe 几乎无)。中文产品常用**柔和的扩散阴影**,让卡片"飘起来"的视觉感更强。

### 4 档 Shadow

| Name | Value | 用途 |
|---|---|---|
| `shadow.card` | `rgba(0, 0, 0, 0.04) 0px 2px 8px` | 卡片默认(极柔) |
| `shadow.card.hover` | `rgba(0, 0, 0, 0.08) 0px 4px 16px` | 卡片 hover |
| `shadow.popover` | `rgba(0, 0, 0, 0.08) 0px 8px 24px, rgba(0, 0, 0, 0.04) 0px 2px 8px` | popover、菜单 |
| `shadow.modal` | `rgba(0, 0, 0, 0.16) 0px 16px 48px` | modal |
| `shadow.drawer` | `rgba(0, 0, 0, 0.12) -4px 0px 24px` | 右侧 drawer(drawer 在右,阴影向左) |

### Focus ring(品牌色 2px)

focus state:`box-shadow: 0 0 0 2px var(--brand-color-light)`(品牌色淡版 2px halo)。

## 5. 间距气质 —— 卡片瀑布感

中文 SaaS 间距偏**紧凑但不拥挤**——多卡片并列、信息密度高(小红书、知乎、飞书都是)。但 line-height 给中文呼吸。

| 用途 | 值 |
|---|---|
| 卡片 padding | 16-24px |
| 卡片 gap | 12-16px |
| 段落 line-height | 1.7-1.8 |
| 段落 margin | 24px |
| 段间隙 | 48-64px |
| 网格 gap | 12-24px |

## 6. 动效曲线 —— 柔和、有"弹性"

中文 SaaS 动效比 Linear **更柔、更有"弹性"**——Linear 绝禁 bounce,中文 SaaS 偶尔允许 micro-bounce(按钮按下的小弹回)传达"轻快"。

| Property | Duration | Timing |
|---|---|---|
| hover | 200ms | `ease-out` |
| 卡片 hover lift | 200ms | `cubic-bezier(0.4, 0, 0.2, 1)` |
| drawer 开 | 300ms | `cubic-bezier(0.16, 1, 0.3, 1)` |
| modal 入 | 250ms | `cubic-bezier(0.16, 1, 0.3, 1)` |
| 按钮按下 | 100ms | `cubic-bezier(0.4, 0, 0.2, 1)` + scale 0.97 |
| toast 入 | 200ms | `ease-out` + translateY 微弹 |

## 7. 图标体系 —— 装饰性彩色 icon

### 中文 SaaS 的 icon 特点

中文产品 icon **比西方更"装饰性"**:
- 带背景圆(实色或淡色填充圆 + 白色 icon)
- 多色(小红书、抖音的 icon 库是彩色的)
- 比 Lucide 的 outline 更"可爱"

### 推荐图标库

| 库 | 适用 |
|---|---|
| **IconPark**(字节跳动开源)| 飞书风、字节风,2000+ icons,多色 + outline 都支持 |
| **Tabler Icons** + 自定彩色背景圆 | 通用 SaaS |
| **Remix Icon**(蚂蚁设计师主导)| 国内团队常用,2200+ icons |

> **绝禁** Lucide 单库主导——Lucide 的西方几何感在中文产品里显得"不亲切"。如果用 Lucide,必须给 icon 加**背景圆 + 彩色填充**改造。

## 8. 签名组件(中文 SaaS 独有)

### 卡片瀑布流(签名)
- 多卡片错落排列(小红书、知乎首页)
- 不是 grid 等宽,是 masonry 错落
- 卡片之间 12-16px gap

### 装饰性 icon + 彩色背景圆(签名)
- icon 不是孤立线条,是"圆底 + 白 icon"组合
- 用于功能区、特性介绍、nav
- 颜色 = 品牌色或语义色

### 微信式绿色按钮(签名)
- 主 CTA 用品牌色(微信绿/知乎蓝)
- 圆角 8px,padding 12px 24px
- weight 500
- 配中文文案

### 富文本编辑器 block(签名)
- 飞书文档、语雀、Notion 中文版都是
- block 化但比 Notion 更"工具感"
- 工具栏在顶部,hover 显示 block handle

### 数字大字 + 单位小字(签名)
- 中文 SaaS 常用"大数字 + 小单位"突出指标
- 例如 "30%" 显示成大 30 + 小 %(视觉对比)
- 用于 dashboard、增长指标

## 9. 反塑料证据(中文 SaaS 的"人做的"信号)

- [ ] **字体第一栈是 PingFang SC**(不是 Inter)
- [ ] **line-height 1.7-1.8**(不是 1.5)
- [ ] **中英混排加空格**("使用 React 框架"不是"使用React框架")
- [ ] **圆角 8-12px**(不是 Linear 的 6px,不是 Notion 的 4px)
- [ ] **品牌色饱和**(微信绿/知乎蓝/小红书红/飞书青,不是 Linear 紫)
- [ ] **阴影柔**(rgba 0.04-0.08,不是 Linear 的多层精确)
- [ ] **icon 带背景圆**(不是孤立 Lucide 线条)
- [ ] **数字大字 + 单位小字**(中文 SaaS 习惯)
- [ ] **半角数字 + 全角中文标点**(不混)
- [ ] **卡片瀑布感**(不是 Linear 的密集表格)

## 10. 反派警示

| 塌成的塑料样 | 病因 | 修复 |
|---|---|---|
| 看起来像"海外翻译版" | 字体用 Inter 主导 | 改 PingFang SC 第一栈 |
| 中英挤在一起 | 没加中英空格 | "使用 React 框架"(加空格) |
| 中文挤 | line-height 1.5 | 改 1.7-1.8 |
| 太冷冰冰 | 用 Linear 紫色 accent | 换中文品牌色(微信绿/知乎蓝) |
| 太克制 | 用 Lucide 孤立 icon | 加彩色背景圆 |
| 像表格 dashboard | 信息密度太高 | 改卡片瀑布流 |
| 圆角太硬 | 用 6px | 改 8-12px |
| 标点混乱 | 半角全角混 | 中文内全角,数字英文内半角 |

## Prompt Fragment(可复制)

### English

```text
Visual style: Chinese SaaS aesthetic (WeChat / Zhihu / Xiaohongshu / Feishu lineage — local-friendly, warm, dense, character-rich).

COLOR (neutral gray + saturated brand):
- canvas: #F5F6F7 (cool gray-white, WeChat-style)
- surface: #FFFFFF for cards
- surface raised: #F7F8FA for hover
- text: #1A1A1A primary / #5F6368 secondary / #9AA0A6 tertiary / #BDC1C6 disabled
- border: #E8EAED default, #DADCE0 strong
- ONE saturated brand color (choose by product type):
  - WeChat Green #07C160 (payment/social)
  - Zhihu Blue #0084FF (knowledge/content)
  - Xiaohongshu Red #FE2C55 (consumer/trend)
  - Feishu Blue #1456F0 (enterprise/collaboration)
- semantic: success #00A870, warning #FF8800, danger #FA5151 (softer than Western), info = brand

TYPOGRAPHY (CJK-LED — CRITICAL):
- font-family FIRST: -apple-system, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Source Han Sans CN", "Noto Sans CJK SC", sans-serif
- NEVER let Inter lead (Inter has no CJK glyphs)
- weights: body 400 / UI 500 / heading 600 / hero 700 (integer weights, NOT 510)
- line-height: 1.7-1.8 for body (CJK needs breathing room, NOT Western 1.5)
- letter-spacing: 0 to +0.02em (CJK does NOT use negative tracking)
- paragraph margin: 24px (1.5em)
- MIXED CN-EN SPACING: add 1/4 em space between CN and EN/numbers
  - ✅ "我们使用 React 框架,提高效率 30%"
  - ❌ "我们使用React框架,提高效率30%"
- PUNCTUATION: full-width inside CN sentences (,。!?), half-width inside EN/digits

RADIUS (softer than Linear):
- 6px for small tags/badges
- 8px for buttons/inputs (mainstream CN SaaS)
- 12px for cards/panels
- 16px for large cards/modals
- 9999px for avatars/pills

ELEVATION (soft, diffused):
- shadow.card: rgba(0,0,0,0.04) 0px 2px 8px (default)
- shadow.card.hover: rgba(0,0,0,0.08) 0px 4px 16px
- shadow.popover: rgba(0,0,0,0.08) 0px 8px 24px, rgba(0,0,0,0.04) 0px 2px 8px
- shadow.modal: rgba(0,0,0,0.16) 0px 16px 48px
- focus: 0 0 0 2px var(--brand-color-light) (brand halo)

SPACING (card waterfall, dense but breathing):
- card padding: 16-24px
- card gap: 12-16px
- grid gap: 12-24px
- section gap: 48-64px
- body line-height 1.7-1.8 (CJK breathing)

MOTION (soft, slightly bouncy allowed):
- hover: 200ms ease-out
- card lift: 200ms cubic-bezier(0.4, 0, 0.2, 1)
- drawer in: 300ms cubic-bezier(0.16, 1, 0.3, 1)
- button press: 100ms + scale 0.97
- micro-bounce OK (CN SaaS allows slight bounce for playful feel)

ICONS (decorative, NEVER bare Lucide):
- IconPark (ByteDance, 2000+, multi-color + outline) OR Remix Icon (Ant designer, 2200+)
- signature: icon WITH colored background circle (white icon on filled circle)
- NEVER bare outline icons (too cold for CN market)
- if using Lucide, wrap each in colored circle bg

SIGNATURE STRUCTURE:
- CARD WATERFALL: masonry-style multi-card layout (Xiaohongshu/Zhihu home)
- DECORATIVE ICON + BG CIRCLE: feature icons are not bare lines, they're "circle + icon" combos
- BRAND-COLOR CTA: main button in WeChat/Zhihu/Xiaohongshu/Feishu color, 8px radius, weight 500
- BIG NUMBER + SMALL UNIT: dashboard metrics show large digits + small unit (30 + %)
- RICH TEXT BLOCK: Feishu/Yuque style, toolbar on top, block handle on hover

NEVER:
- use Inter as primary font (use PingFang SC)
- use line-height 1.5 (use 1.7-1.8 for CJK)
- use negative letter-spacing (use 0 to +0.02em)
- use Linear violet accent (use CN brand color)
- use bare outline icons (wrap in colored circle)
- use 6px radius (use 8-12px)
- mix half-width/full-width punctuation randomly
- crowd CN-EN text without spacing
```

### 中文

```text
视觉风格:中文 SaaS 风(微信/知乎/小红书/飞书系 — 本土亲切、温暖、密集、字符丰富)。

配色(中性灰 + 饱和品牌色):
- 画布:#F5F6F7(微冷灰白,微信风)
- 表面:#FFFFFF 卡片
- 抬升表面:#F7F8FA hover
- 文字:#1A1A1A 主 / #5F6368 次 / #9AA0A6 弱 / #BDC1C6 禁用
- 边框:#E8EAED 默认,#DADCE0 强
- 一个饱和品牌色(按产品类型选):
  - 微信绿 #07C160(支付/社交)
  - 知乎蓝 #0084FF(知识/内容)
  - 小红书红 #FE2C55(消费/潮流)
  - 飞书青 #1456F0(企业/协作)
- 语义:success #00A870 / warning #FF8800 / danger #FA5151(比西方柔)/ info = 品牌色

字体(CJK 主导 — 关键):
- 字体第一栈:-apple-system, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Source Han Sans CN", "Noto Sans CJK SC", sans-serif
- 绝不让 Inter 主导(Inter 不含中文字形)
- 字重:body 400 / UI 500 / heading 600 / hero 700(整百字重,不用 510)
- line-height:body 1.7-1.8(CJK 需要呼吸,不是西方的 1.5)
- letter-spacing:0 到 +0.02em(CJK 不用负 tracking)
- 段落 margin:24px(1.5em)
- 中英混排加 1/4 em 空隙:
  - ✅ "我们使用 React 框架,提高效率 30%"
  - ❌ "我们使用React框架,提高效率30%"
- 标点:中文内全角(,。!?),数字英文内半角

圆角(比 Linear 柔):
- 6px 用于小 tag/badge
- 8px 用于按钮/输入(中文 SaaS 主流)
- 12px 用于卡片/面板
- 16px 用于大卡片/modal
- 9999px 用于头像/pill

ELEVATION(柔、扩散):
- shadow.card:rgba(0,0,0,0.04) 0px 2px 8px(默认)
- shadow.card.hover:rgba(0,0,0,0.08) 0px 4px 16px
- shadow.popover:rgba(0,0,0,0.08) 0px 8px 24px, rgba(0,0,0,0.04) 0px 2px 8px
- shadow.modal:rgba(0,0,0,0.16) 0px 16px 48px
- focus:0 0 0 2px var(--brand-color-light)(品牌色 halo)

间距(卡片瀑布感,密集但呼吸):
- 卡片 padding:16-24px
- 卡片 gap:12-16px
- 网格 gap:12-24px
- 段间隙:48-64px
- body line-height 1.7-1.8(CJK 呼吸)

动效(柔、轻微弹性允许):
- hover:200ms ease-out
- 卡片 lift:200ms cubic-bezier(0.4, 0, 0.2, 1)
- drawer 入:300ms cubic-bezier(0.16, 1, 0.3, 1)
- 按钮按:100ms + scale 0.97
- micro-bounce 可接受(中文 SaaS 允许微弹,传达轻快)

图标(装饰性,绝禁裸 Lucide):
- IconPark(字节,2000+,多色 + outline)或 Remix Icon(蚂蚁,2200+)
- 签名:icon 带彩色背景圆(白 icon 在实色圆上)
- 绝禁裸 outline icon(对中文市场太冷)
- 如果用 Lucide,必须包在彩色圆里

签名结构:
- 卡片瀑布流:小红书/知乎首页的 masonry 错落卡片
- 装饰 icon + 背景圆:feature icon 不是裸线,是"圆 + icon"组合
- 品牌色 CTA:主按钮用品牌色(微信绿/知乎蓝),8px radius,weight 500
- 数字大字 + 单位小字:dashboard 指标"30 + %"
- 富文本 block:飞书/语雀风,顶部工具栏,hover 显示 block handle

绝对不要:
- 用 Inter 作主字体(用 PingFang SC)
- 用 line-height 1.5(用 1.7-1.8 给 CJK 呼吸)
- 用负 letter-spacing(用 0 到 +0.02em)
- 用 Linear 紫 accent(用中文品牌色)
- 用裸 outline icon(包彩色圆)
- 用 6px 圆角(用 8-12px)
- 半角全角标点混用
- 中英文字紧贴不加空格
```

## 权威信源

- 字节 DesignC vestibule:design.bytedance.com
- 蚂蚁 Ant Design:ant.design(中文企业 SaaS 公约)
- Arco Design(字节开源)
- TDesign(腾讯开源)
- 微信小程序设计指南:developers.weixin.qq.com/miniprogram/design
- 飞书设计体系:lark.design

## 与其他风格的关系

- 想要**深色工程工具**(开发者)→ 切到 `style-linear.md`
- 想要**白底编辑式**(金融/支付)→ 切到 `style-stripe.md`
- 想要**温暖反流派**(知识协作,西方语境)→ 切到 `style-notion.md`
- 想要**极客纯黑**(hosting/平台)→ 切到 `style-vercel.md`
- **中文 SaaS 风适合中国大陆受众的产品**——当 audience 是中文消费者/SMB/企业用户时,前 4 个西方风格会让产品"像海外的",失去本土亲切感。**绝禁**用在面向海外开发者的产品。
