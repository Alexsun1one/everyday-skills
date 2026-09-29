# 04 — 响应式不只是"320px 不溢出",是每个断点的艺术指导

> 与 `references/qa-responsive.md` 的分工:那份是**验收**——"移动/平板/桌面没坏、不溢出、能点"。本文件是**创作前置**——每个断点是一种**不同的构图**,不是同一张图缩小。`qa-responsive` 回答"没坏吗",本文件回答"每个尺寸下这是不是最好的构图"。先本文件定艺术指导,再 qa-responsive 验收。

## 0. 核心心法:响应式 = 同一内容,N 套构图

塑料响应式 = 桌面稿直接 `transform: scale()` 缩到手机,文字糊、栅格塌、CTA 跑到折叠下面。**移动端不是"缩小的桌面",是一个独立的、用户场景完全不同的构图**——手机用户单手、拇指操作、网络慢、注意力碎、垂直滚动。

所以每个断点要问三个艺术指导问题:
1. **这尺寸下,什么内容该砍?**(装饰、次要、桌面专属交互)
2. **什么该折叠/换形态?**(长列表→手风琴、表格→卡片、hover→tap)
3. **什么该换序?**(CTA 必须拇指够得着;主信息必须在折叠上方)

---

## 1. 移动优先(Mobile-first)—— CSS 书写顺序的硬规则

**先写移动端基础样式,再用 `min-width` 媒体查询向上增强。** 不要桌面优先 + `max-width` 向下覆盖。

### 为什么
- **移动用户网络慢**:移动优先 = 移动端只下载基础 CSS;桌面增强才加载额外规则。桌面优先 = 移动端先下载桌面 CSS 再被覆盖,浪费带宽。
- **强制克制**:先给最小屏设计,天然逼你砍掉装饰,只留核心。
- **渐进增强**思维:基础体验人人有,大屏是锦上添花。

### CSS
```css
/* ✅ 移动优先:基础(手机)在前,大屏 min-width 增强 */
.hero { padding: 48px 20px; text-align: left; }       /* 手机:单列,左对齐 */
@media (min-width: 768px)  { .hero { padding: 80px 48px; } }
@media (min-width: 1024px) { .hero { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; padding: 120px 64px; } }
@media (min-width: 1440px) { .hero { padding: 160px 96px; max-width: 1280px; margin-inline: auto; } }

/* ❌ 桌面优先(塑料):先写桌面,再用 max-width 一层层砍——移动端白下载一堆被覆盖的规则 */
```

---

## 2. 断点表(390 / 768 / 1024 / 1440)及每个断点的构图重排意图

| 断点 | 设备 | 布局重排意图 | 该砍/折叠/换序 |
|------|------|------------|--------------|
| **<390px** | 小手机 | 全单列,一切堆叠 | 砍装饰大图;导航→汉堡;CTA→sticky 底栏 |
| **390–767px** | 标准手机 | 单列为主,小卡组可 2 列 | 长列表→手风琴;表格→卡片;buy box 常驻可见 |
| **768–1023px** | 平板竖屏 | 2 列布局出现,窄侧栏可出现 | hero 可左右分栏;次要导航可常驻 |
| **1024–1439px** | 小笔记本/桌面 | 完整多列,侧栏+内容 | 3 列 feature、完整导航、hover 交互启用 |
| **≥1440px** | 宽屏桌面 | 内容容器封顶 1200-1280px 居中,或故意出血用宽 | **不让内容铺满 2400px**(段落宽到 1800px 不可读);宽屏给更大留白或出血视觉 |

### 每个断点的"构图意图"(不是"能放下",是"这样排最好看")

**手机(<768):**
```
┌─────────────┐
│ ☰      logo │  导航折叠成汉堡
├─────────────┤
│             │
│  H1 价值主张 │  hero 单列左对齐(不居中——
│  (fluid 大字)│  居中在窄屏显得空、弱)
│  副标        │
│  [主CTA 满]  │  CTA 满宽或大,拇指够得着
│             │
├─────────────┤
│  feature    │  feature 改单列堆叠(不平铺)
│  (纵向叙事)  │  或 2 列小卡
└─────────────┘
[sticky 底栏 CTA]  滚动时常驻一个 CTA
```

**平板(768-1023):**
```
┌──────────────────────┐
│ nav 常驻  logo   CTA │
├───────────┬──────────┤
│           │          │
│  H1+副标  │  产品图  │  hero 左右分栏出现
│  [CTA]    │  (出血)   │
│           │          │
├───────────┴──────────┤
│  feature 2 列        │
└──────────────────────┘
```

**桌面(≥1024):**
```
┌────────────────────────────────────┐
│ nav 全展开         logo      CTA   │
├────────────────┬───────────────────┤
│                │                   │
│  H1 价值主张   │   真实产品截图    │  完整分栏 + 出血
│  副标          │   (偏右出血)      │
│  [主CTA][次CTA]│                   │
│  信任 logo     │                   │
├────────────────┴───────────────────┤
│  feature 3 列 / 不对称 bento        │
└────────────────────────────────────┘
```

**宽屏(≥1440):**
```
┌ ········································· ┐
│   ┌──────────────────────────────────┐     │  内容封顶 1200-1280px
│   │         居中内容区               │     │  两侧大留白
│   │   (不再随屏变宽)                 │     │  或:故意出血一张大视觉
│   └──────────────────────────────────┘     │  用满超宽
└ ········································· ·┘
```

### 宽屏红线:**绝不让正文/段落随屏宽无限拉伸**
> 段落宽到 1200px+ 时,视线跳行丢字,不可读。容器**封顶**(常见 1200-1280px 内容区)居中,两侧留白。**或**故意让某张视觉出血用满超宽,但文字仍封顶。AI 常犯:整页 `width: 100%` 无封顶,在 4K 屏上文字拉成一条横线。

---

## 3. Fluid Type —— `clamp()` 具体公式(字号随屏流式缩放)

### 为什么 fluid
固定字号在桌面合适、在手机太大或太小。`clamp(min, pref, max)` 让字号在两个极值间**线性流式缩放**,任何屏宽都刚好,无需每个断点重写字号。这是 2024+ 标准做法(UTOPIA 项目 utopia.fyi 是权威)。

### 公式
```css
font-size: clamp(MIN, PREF, MAX);
/* PREF = baseline + slope × vw,使字号在 Wmin→Wmax 屏宽间从 Smin→Smax 线性变化 */
```

**推导**(以 H1 为例,希望 320px 屏=32px,1240px 屏=52px):
- slope = (52 - 32) / (1240 - 320) × 100 = 20/920 × 100 ≈ 2.17vw
- baseline = 32 - 2.17 × 320 / 100 ≈ 32 - 6.94 ≈ 25.06px ≈ 1.56rem
- → `clamp(2rem, 1.56rem + 2.17vw, 3.25rem)`(min/max 用 rem,PREF 含 rem+vw)

### 可直接抄的 fluid type 阶梯(基于 16px root)
| Token | `clamp()` 值 | 实际范围(320→1240px) |
|-------|-------------|---------------------|
| `display` | `clamp(2.5rem, 1.2rem + 4.5vw, 5rem)` | 40px → 80px |
| `h1` | `clamp(2rem, 1.56rem + 2.2vw, 3.25rem)` | 32px → 52px |
| `h2` | `clamp(1.5rem, 1.22rem + 1.5vw, 2.25rem)` | 24px → 36px |
| `h3` | `clamp(1.25rem, 1.1rem + 0.8vw, 1.5rem)` | 20px → 24px |
| `body` | `clamp(1rem, 0.96rem + 0.2vw, 1.125rem)` | 16px → 18px |
| `small` | `0.875rem`(固定,14px,小字不流式) | 14px |

```css
:root { font-size: 100%; } /* 别改 root,所有 rem 基于此 */
.h1 { font-size: clamp(2rem, 1.56rem + 2.2vw, 3.25rem); line-height: 1.1; letter-spacing: -0.02em; }
.body { font-size: clamp(1rem, 0.96rem + 0.2vw, 1.125rem); line-height: 1.65; }
```

**纪律**:
- **line-height 随字号反变**:大字 line-height 紧(1.05-1.2),正文松(1.5-1.75)。fluid 字号配 fluid line-height 太复杂——给每个 token 固定 line-height 即可(上表)。
- **正文字号最小 16px**:别为了"多塞内容"把正文降到 14px(不可读,无障碍违规)。14px 仅限元信息/图注。
- **letter-spacing 大字负、小字零**(见 style-linear.md progressive tracking)。

---

## 4. Fluid Spacing —— 间距也流式

section 间距、容器 padding 同样用 clamp,随屏流式:

```css
.section { padding-block: clamp(3.5rem, 2.5rem + 4vw, 7.5rem); } /* 56px → 120px */
.container { padding-inline: clamp(1.25rem, 0.8rem + 2vw, 4rem); } /* 20px → 64px */
.section-gap { margin-block: clamp(4rem, 2rem + 8vw, 10rem); } /* 64px → 160px */
```

---

## 5. Container Queries —— 组件随"容器"适配,不是随"视口"

### 为什么
传统 `@media (min-width)` 查询的是**整个视口**。但一个卡片组件可能放在窄侧栏(300px)也可能放在主内容区(800px)——视口一样大,容器不一样。Container Query 让组件**随它所在的容器尺寸**适配,是真正可复用组件的关键。

### CSS
```css
/* 声明容器 */
.card-wrap { container-type: inline-size; container-name: card; }

/* 窄容器:纵向 */
.card { display: flex; flex-direction: column; gap: 12px; }
/* 宽容器(≥400px):横向 */
@container card (min-width: 400px) {
  .card { flex-direction: row; align-items: center; gap: 24px; }
}
```

### 用例
- **卡片组件**:窄容器纵向、宽容器横向,同一组件不同容器自适应。
- **侧栏 vs 主区**:导航/搜索框在窄侧栏紧凑、宽主区舒展。
- **可嵌入的小部件**:在不同宿主页面尺寸下自适应。

> **2024+ 主流浏览器全支持 container queries**。能用就用——它让组件真正"插哪都好看",而不是"插主区好看、插侧栏塌掉"。

---

## 6. 小屏该砍 / 该折叠 / 该换序 —— 艺术指导清单

### 该砍(移除,不是藏)
- 装饰性大背景图(移动端服务更小的或去掉,减 LCP 负担,见 `05`)。
- 桌面专属的 hover 提示、鼠标跟随视差(移动无鼠标)。
- 次要的侧栏推荐、装饰性插画列。
- 重复的导航(桌面顶栏 + 侧栏 → 移动只留汉堡)。

### 该折叠/换形态
| 桌面形态 | 移动形态 |
|---------|---------|
| 多列 feature 网格 | 单列堆叠 或 2 列小卡 |
| 宽数据表格 | 卡片列表(每行一卡) |
| 长筛选侧栏 | 抽屉/底部 sheet,点"筛选"展开 |
| 多步骤横向流程 | 纵向步骤 |
| hover 显示的操作 | 常驻 tap 按钮 |
| 长文章 TOC 侧栏 | 顶部"目录"按钮展开 |

### 该换序(order / source order)
- **CTA 必须拇指够得着**:桌面 CTA 在 hero 右上;移动端要么在 hero 内满宽大按钮,要么 sticky 底栏常驻。
- **主信息必须在折叠上方(the fold)**:移动用户首屏只看到顶部一屏,关键价值主张 + 主 CTA 必须在第一屏。
- **buy box 优先**:商品页移动端,buy box(价格+CTA)在图集之后**立刻**出现,不能埋在详情下面。
- **用 CSS `order` 或调整 DOM source order**(优先调 DOM,对 SEO 和屏幕阅读器更好;CSS order 仅做视觉重排)。

```css
/* ✅ 移动端 buy box 提到图集前(DOM 里图集在前,视觉用 order 提前 buy box) */
@media (max-width: 767px) {
  .gallery { order: 2; }
  .buy-box { order: 1; } /* 价格+CTA 先于大图集 */
}
```

---

## 7. 触控目标 —— 移动端硬底线

- **最小触控区 44×44px**(iOS HIG)/ 48×48px(Material)。视觉按钮可以小,但**点击 hitbox** 必须达标(用 padding 撑大不可见命中区)。
- **相邻可点元素间距 ≥8px**,防误触。
- **移动端去掉 hover 依赖**:hover 态在触屏上是"粘滞"的(点一下触发 hover 不消失),关键操作不能只在 hover 出现。

```css
/* 视觉小但命中区够 */
.icon-btn { width: 36px; height: 36px; }              /* 视觉 36 */
.icon-btn::before { content:''; position:absolute; inset:-6px; } /* hitbox 撑到 48 */
```

---

## 8. 图片艺术指导 —— `<picture>` 按断点服务"不同构图"

不只是服务不同**尺寸**,是不同**构图裁切**(art direction):桌面宽幅 hero 裁切 vs 移动端竖构图裁切。

```html
<picture>
  <source media="(min-width: 1024px)" srcset="hero-wide.jpg">
  <source media="(min-width: 768px)"  srcset="hero-tablet.jpg">
  <img src="https://example.com/hero-mobile.jpg" alt="..." width="800" height="600" loading="eager">
</picture>
```
- 桌面服务宽幅(主体居中/偏右),移动服务竖构图(主体居中放大)。
- **必须给 `width`/`height`**(防 CLS,见 `05`)。
- **首屏图 `loading="eager"`,其余 `loading="lazy"`**。

---

## 反塑料证据(响应式艺术指导的"人做的"信号)

- [ ] 移动优先书写(`min-width` 增强,非 `max-width` 砍)
- [ ] 字号用 `clamp()` 流式,正文字号最小 16px
- [ ] 桌面/平板/手机是三种构图,不是一张图缩放
- [ ] 宽屏内容封顶 1200-1280px,正文不无限拉伸
- [ ] 用了 container queries 让组件随容器适配
- [ ] 小屏砍了装饰、折叠了长列表/表格、CTA 换序到拇指区
- [ ] 移动端触控目标 ≥44px,无 hover 依赖
- [ ] 图片用 `<picture>` 按断点服务不同构图裁切
- [ ] 配合 `qa-responsive.md` 验收三断点不溢出

## 常见塌方表

| 塌成什么 | 病因 | 修复 |
|---------|------|------|
| 手机上桌面稿缩成糊一团 | 桌面优先 + scale | 移动优先 + 每断点重排 |
| 宽屏文字拉成横线 | 容器无 max-width | 封顶 1200-1280px 居中 |
| 手机字号忽大忽小 | 每断点硬写字号 | 用 `clamp()` 流式 |
| 组件插侧栏就塌 | 用视口 media query | 改 container query |
| 手机点不准 | 触控目标 <44px / 间距 <8px | 撑 hitbox 到 44px+ |
| 手机 CTA 够不着 | CTA 在桌面右上,移动没换序 | sticky 底栏或 hero 内满宽 |
| 手机关键信息在折叠下 | 没做"fold 上方"艺术指导 | 主信息+主CTA 上提 |
