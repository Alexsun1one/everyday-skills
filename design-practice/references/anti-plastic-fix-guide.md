# 反塑料修复指南 — Anti-Plastic Fix Guide

> 检查出"weight 510 没开"很容易,但**怎么改成 510** 是另一回事。这一页是修复手册——每个反塑料证据失败后,**给出具体修复代码 / 工具 / 步骤**。
>
> 不只是检查清单,是**修复 playbook**。

## Linear 风修复

### 证据失败:weight 不是 510

**症状**:weight 用了 500 或 600,看起来"太轻"或"太重",不是 Linear 的几何工程感。

**修复**:

```css
/* 错:font-weight: 500; */
/* 错:font-weight: 600; */

/* 对:用 font-variation-settings 精确到 510 */
body {
  font-family: "Inter Variable", sans-serif;
  font-variation-settings: "wght" 510;  /* ← 关键 */
  font-feature-settings: "cv01", "ss03";  /* 几何变体也开 */
}

/* 标题用 590 */
h1, h2, h3 {
  font-variation-settings: "wght" 590;
}
```

**前提**:字体必须是 Inter Variable(变量字体)。如果用静态 Inter,只能取 100/200/.../900,无法取 510。先升级到 Inter Variable。

**验证**:浏览器 DevTools → Computed → font-variation-settings 应显示 `'wght' 510`。

---

### 证据失败:没开 cv01 / ss03

**症状**:Inter 看起来"普通",不是 Linear 的几何感(单层 a、几何变体)。

**修复**:

```css
body {
  font-family: "Inter Variable", sans-serif;
  font-feature-settings: "cv01", "ss03";  /* ← 关键 */
  /* cv01: 单层 a(更几何)*/
  /* ss03: 几何变体(更工程感)*/
}
```

**验证**:浏览器 DevTools → Elements → Computed → Font → 应看到 `cv01: 1, ss03: 1`。

---

### 证据失败:用了 drop shadow 而不是 luminance stacking

**症状**:深色模式卡片看起来"贴了个洞",不是真实抬升。

**修复**:

```css
/* 错:box-shadow: 0 4px 12px rgba(0,0,0,0.5); */

/* 对:抬升元素用更亮背景 */
.card {
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.05) 0%,
    rgba(255, 255, 255, 0.02) 100%
  );
  border: 1px solid rgba(255, 255, 255, 0.05);
}

/* 仅 popover/modal 用 drop shadow */
.popover {
  background: #191A1B;
  box-shadow:
    rgba(0,0,0,0.15) 0px 4px 12px,
    rgba(0,0,0,0.2) 0px 8px 24px,
    inset 0 0 0 1px rgba(255,255,255,0.08);
}
```

**关键洞察**:`rgba(0,0,0,...)` 阴影在深色背景看起来"像挖了个洞"。抬升靠**背景提亮**,不靠 shadow。shadow 仅给浮空层(popover/modal)。

---

### 证据失败:focus ring 是单层 outline

**症状**:focus 时一个细线,不像 Linear 的 halo。

**修复**:

```css
/* 错 */
:focus { outline: 2px solid #5E6AD2; }

/* 对:双层 box-shadow halo */
:focus { outline: none; }
:focus-visible {
  outline: none;
  box-shadow:
    0 0 0 2px rgba(94, 106, 210, 0.4),   /* 内环 */
    0 0 0 4px rgba(94, 106, 210, 0.2);   /* 外环 */
}
```

**为什么用 :focus-visible 不用 :focus**:鼠标点击不显示 ring(干净),键盘 Tab 显示 ring(可达)。`:focus-visible` 自动判断。

---

### 证据失败:用了 bounce easing

**症状**:动画有弹回,看起来"俏皮",不是 Linear 的"专业"。

**修复**:

```css
/* 错 */
.transition {
  transition: transform 300ms cubic-bezier(0.34, 1.56, 0.64, 1); /* spring/bounce */
}

/* 对:ease-default(easeOutQuad)*/
.transition {
  transition: transform 200ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* 对:modal 入场用 ease-enter(easeOutQuart)*/
.modal-enter {
  transition: transform 300ms cubic-bezier(0.165, 0.84, 0.44, 1);
}
```

---

### 证据失败:用了 8px 圆角

**症状**:按钮/卡片用了 8px,不是 Linear 的 6/12/9999 三档。

**修复**:

```css
/* 错:radius: 8px; */

/* 对:严格 6/12/9999 */
.button { border-radius: 6px; }       /* 控件 */
.card { border-radius: 12px; }       /* 容器 */
.avatar { border-radius: 9999px; }   /* 头像 */
.pill-badge { border-radius: 9999px; }
```

---

### 证据失败:#5E6AD2 出现 5+ 次

**症状**:accent 用太多,变成彩虹。

**修复**:审计每屏 accent 出现次数。规则:**每屏 ≤3 次**。

```text
每屏 accent 配额(3 次):
  1. focus ring(必有)
  2. primary CTA(主按钮)
  3. 链接 / active nav(选一)

其他都用中性色:
  - secondary button: 边框 + 透明底
  - ghost button: 仅文字
  - 状态色:用语义色(success 绿 / warning 黄 / danger 红)
  - icon:用 currentColor(继承文字色)
```

---

### 证据失败:顶栏没有 backdrop-filter

**症状**:顶栏纯色,不"穿透",看起来贴在顶上。

**修复**:

```css
.top-bar {
  background: rgba(8, 9, 10, 0.85);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  position: sticky;
  top: 0;
  z-index: 50;
}
```

## Stripe 风修复

### 证据失败:标题用了 weight 500/600

**症状**:标题看起来"重",不是 Stripe 的 whisper-authority。

**修复**:

```css
/* 错 */
h1 { font-weight: 600; }

/* 对:weight 300 */
h1 { font-weight: 300; }
h2 { font-weight: 300; }
h3 { font-weight: 300; }

/* body 才用 400 */
body { font-weight: 400; }
```

**前提**:用 sohne-var(Stripe 自有)或 Inter Variable 替代。静态字体取不到精确 weight,但 Inter Variable 300 也接近。

---

### 证据失败:画布用了纯白

**症状**:看起来冰冷,不像 Stripe 的暖调 off-white。

**修复**:

```css
/* 错:background: #FFFFFF; */

/* 对:Mist 冷调 off-white */
body { background: #E5EDF5; }
.card { background: #FFFFFF; }  /* 卡片才用纯白 */
```

---

### 证据失败:按钮有 drop shadow

**症状**:按钮"贴纸"感,不是 Stripe 的"平面可信"。

**修复**:

```css
/* 错 */
.button {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* 对:无 shadow */
.button {
  background: #533AFD;
  color: white;
  border: none;
  /* 无 box-shadow */
}
.button:hover {
  background: rgba(83, 58, 253, 0.9);  /* 10% 白 overlay 提亮 */
}
```

**例外**:仅 floating mockup(产品截图当艺术)允许 shadow。

---

### 证据失败:用了 8px 圆角

**修复**:

```css
/* 全部 4px */
.button, .card, .input, .tag, .badge {
  border-radius: 4px;
}
```

---

### 证据失败:没有 gradient text headline

**症状**:标题看起来普通,不是 Stripe 的签名。

**修复**:

```css
h1 {
  font-weight: 300;
  letter-spacing: -0.025em;
  background: linear-gradient(90deg, #533AFD 0%, #50617A 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  -webkit-text-fill-color: transparent;
}
```

---

### 证据失败:trailing arrow 没在按钮上

**修复**:

```html
<!-- Stripe 签名按钮:trailing arrow glyph -->
<button class="primary-cta">
  开始使用
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none"
       stroke="currentColor" stroke-width="2"
       stroke-linecap="round" stroke-linejoin="round">
    <line x1="5" y1="12" x2="19" y2="12"></line>
    <polyline points="12 5 19 12 12 19"></polyline>
  </svg>
</button>
```

## Notion 风修复

### 证据失败:画布是纯白

**修复**:

```css
body { background: #FFFDF7; }  /* 奶油 */
```

---

### 证据失败:所有 CTA 都是彩色

**修复**:多数 CTA 改成黑色。

```css
/* 默认 primary 改成黑色,不是品牌橙 */
.button-primary {
  background: #1F1F1F;  /* 黑色 */
  color: white;
}

/* 仅营销页用品牌橙 #D9730D */
.button-marketing {
  background: #D9730D;
  color: white;
}
```

---

### 证据失败:用了 Lucide(太冷)

**修复**:换 Phosphor Duotone。

```bash
# 安装
npm install @phosphor-icons/react

# 替换
# 旧:import { Settings } from 'lucide-react';
# 新:
import { Settings } from '@phosphor-icons/react/dist/ssr';

<Settings size={24} weight="duotone" color="#D9730D" />
```

---

### 证据失败:shadow 太重

**修复**:

```css
/* 错 */
.card { box-shadow: 0 8px 24px rgba(0,0,0,0.15); }

/* 对:极轻 */
.card {
  box-shadow:
    rgba(15, 15, 15, 0.05) 0px 0px 0px 1px,  /* 1px 边框 */
    rgba(15, 15, 15, 0.04) 0px 3px 6px;       /* 极轻 drop */
}
```

---

### 证据失败:不是 block 流(用了 grid)

**修复**:Notion 是 block 流,不是表格网格。

```css
/* 错:grid */
.content {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

/* 对:block 流 */
.content {
  display: flex;
  flex-direction: column;
  gap: 4px;  /* block 之间松 */
}
```

## Vercel 风修复

### 证据失败:用了近黑 #08090A(Linear 的)

**修复**:Vercel 用纯黑。

```css
body { background: #000000; }  /* 纯黑 */
```

---

### 证据失败:没有几何点纹背景

**修复**:

```css
.hero {
  background-color: #000000;
  background-image:
    radial-gradient(circle, rgba(255, 255, 255, 0.06) 1px, transparent 1px);
  background-size: 16px 16px;
  background-position: 0 0;
}
```

---

### 证据失败:没有 bento grid

**修复**:

```css
.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: minmax(180px, auto);
  gap: 12px;
}

/* 部分卡片跨多格 */
.feature-card-large {
  grid-column: span 2;
  grid-row: span 2;
}
```

---

### 证据失败:链接没有 trailing arrow

**修复**:

```html
<a class="learn-more" href="#">
  了解更多
  <span class="arrow">→</span>
</a>

<style>
.learn-more { display: inline-flex; align-items: center; gap: 4px; }
.arrow { transition: transform 150ms ease-out; }
.learn-more:hover .arrow { transform: translateX(2px); }
</style>
```

## 中文 SaaS 风修复

### 证据失败:字体第一栈是 Inter

**修复**:

```css
/* 错 */
body { font-family: "Inter", sans-serif; }

/* 对:PingFang SC 主导 */
body {
  font-family:
    -apple-system,
    BlinkMacSystemFont,
    "PingFang SC",
    "Hiragino Sans GB",
    "Microsoft YaHei",
    "Source Han Sans CN",
    "Noto Sans CJK SC",
    sans-serif;
}
```

---

### 证据失败:line-height 是 1.5(中文挤)

**修复**:

```css
body {
  line-height: 1.7;  /* 中文 SaaS 标准 */
}

p {
  line-height: 1.8;  /* 阅读段 */
}
```

---

### 证据失败:中英混排没空格

**修复**:中文段落里手动加空格(写作规范)。

```html
<!-- 错 -->
<p>我们使用React框架,提高效率30%。</p>

<!-- 对 -->
<p>我们使用 React 框架,提高效率 30%。</p>
```

或 CSS 自动(浏览器支持有限):

```css
p {
  text-autospace: ideograph-alpha;
  text-autospace: ideograph-numeric;
}
```

---

### 证据失败:用了裸 Lucide icon(太冷)

**修复**:给 icon 加彩色背景圆。

```html
<!-- 错:裸 Lucide -->
<svg class="lucide-icon"><!-- ... --></svg>

<!-- 对:Lucide 包在彩色圆里 -->
<div class="icon-circle" style="background: #07C160;">
  <svg class="lucide-icon" style="color: white;"><!-- ... --></svg>
</div>

<style>
.icon-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.icon-circle svg { width: 20px; height: 20px; }
</style>
```

---

### 证据失败:用了 Linear 紫色 accent

**修复**:换中文品牌色。

```css
/* 错 */
:root { --brand: #5E6AD2; }

/* 对:按产品类型选 */
:root {
  /* 微信绿(支付/社交)*/
  --brand: #07C160;
}
/* 或 */
:root {
  /* 知乎蓝(知识/内容)*/
  --brand: #0084FF;
}
/* 或 */
:root {
  /* 小红书红(消费/潮流)*/
  --brand: #FE2C55;
}
/* 或 */
:root {
  /* 飞书青(企业/协作)*/
  --brand: #1456F0;
}
```

---

### 证据失败:圆角是 6px(太硬)

**修复**:

```css
/* 错 */
.button { border-radius: 6px; }

/* 对:8-12px 柔 */
.button { border-radius: 8px; }
.card { border-radius: 12px; }
```

## 通用反塑料修复

### 修复:progressive tracking

```css
/* 大字紧、小字松 */
h1 { font-size: 48px; letter-spacing: -0.96px; }
h2 { font-size: 32px; letter-spacing: -0.5px; }
h3 { font-size: 24px; letter-spacing: -0.22px; }
h4 { font-size: 20px; letter-spacing: -0.1px; }
body { font-size: 16px; letter-spacing: 0; }  /* body 0 */
```

### 修复:pressed scale 0.98

```css
.button {
  transition: transform 100ms cubic-bezier(0.4, 0, 0.2, 1);
}
.button:active {
  transform: scale(0.98);  /* 不是 0.95,不是 1 */
}
```

### 修复:6 级 elevation

```css
.elevation-0 { background: var(--canvas); box-shadow: none; }
.elevation-1 { background: var(--surface); box-shadow: none; }
.elevation-2 { background: rgba(255,255,255,0.05); box-shadow: none; }  /* luminance */
.elevation-3 { background: #191A1B; box-shadow: var(--shadow-popover); }
.elevation-4 { background: #191A1B; box-shadow: var(--shadow-modal); }
.elevation-5 { background: rgba(0,0,0,0.2); box-shadow: var(--shadow-inset); }
```

### 修复:图标库混用

**审计**:跑一遍 import,grep 所有 icon 库。

```bash
# 在 src/ 跑
grep -r "lucide-react\|@heroicons\|@phosphor-icons\|@tabler/icons" src/ | sort | uniq -c
```

**修复**:选一个库,删除其他,替换所有用法。

## 修复后验证

每修一个证据,**重新跑反塑料检查**:

```text
□ 重跑 visual-language/style-*.md 的反塑料证据 checklist
□ 全部 ✓ 才算修完
□ 任何一个还是 ✗,继续修
□ 6 级 elevation 都验过
□ focus 双环测过(键盘 Tab 看看)
□ weight 510 在 DevTools Computed 确认
□ accent 出现次数 ≤3 在屏幕上数过
```

## 与 SKILL.md 的关系

SKILL.md 的多层自检 L3(皮肤层)检查出失败后,**调用这一页做修复**。检查是诊断,这一页是治疗。
