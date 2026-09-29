# A11y 七项验收 — Accessibility Acceptance

> 不做 a11y 验收,产物对**色盲、视障、键盘用户、屏幕阅读器用户**来说就是不可用的。AI 生成 UI 最常见的 a11y 缺陷:**只靠颜色传达状态、按钮没文字 label、输入框没 label、对比度不够、键盘不能导航**。
>
> 这一页冻结 7 项必检 a11y 项 + AI 验收员提示词。

## 7 项必检

### 1. 颜色对比度 Color Contrast

文字与背景的对比度必须达标。

| 内容类型 | WCAG AA(最低)| WCAG AAA(理想)|
|---|---|---|
| 正文文字(<18px)| 4.5:1 | 7:1 |
| 大字(≥18px 或 ≥14px bold)| 3:1 | 4.5:1 |
| UI 组件(icon、border、button)| 3:1 | - |

**检查工具:** Stark(浏览器插件)、contrast-ratio.com、Chrome DevTools 的 "Rendering" → "Emulate vision deficiencies"。

**常见失败:**
- `#999999` 文字 on 白底(对比度 2.85:1,失败)
- 浅灰 placeholder on 白底(常失败)
- 浅色 accent 按钮 on 浅色背景(常失败)
- brand color `#533AFD` on 白底:4.93:1 ✓ AA pass(Stripe accent 选这个值不是偶然)

### 2. 键盘可达 Keyboard Navigation

**所有交互元素**必须能用键盘操作。

**Tab 顺序** 必须符合视觉阅读顺序(从左到右,从上到下)。

**必验动作:**
- [ ] Tab 键能在所有按钮、链接、输入框、checkbox 之间移动
- [ ] Shift+Tab 能反向
- [ ] Enter / Space 能激活按钮
- [ ] ESC 能关闭 modal / drawer / popover
- [ ] 方向键能在 tablist、menu、grid 中移动
- [ ] Cmd/Ctrl+K 能打开 command palette(如果有)
- [ ] Tab 顺序符合视觉顺序(不是 DOM 顺序)

**常见失败:**
- 用 `<div onclick>` 而不是 `<button>` —— 键盘点不到
- modal 打开后 focus 还在背景——焦点丢失
- Tab 跑到关闭的 modal 后面——焦点陷阱失败
- 自定义 dropdown 用 mouse hover 触发——键盘打不开

**修复:** 所有交互元素用语义化 HTML(`<button>` `<a>` `<input>` `<select>`)或加 `tabindex="0"` + `role` + 键盘事件处理。

### 3. Focus 永远可见 Focus Visible

**任何用键盘 Tab 时,focus 必须可见**。

**绝禁:**
- `outline: none` 不补 `:focus-visible`
- focus 颜色与背景对比度 < 3:1
- focus 用 hover 替代

**标准 focus ring(套风格 DNA):**
- Linear:双层 box-shadow `0 0 0 2px rgba(94,106,210,0.4), 0 0 0 4px rgba(94,106,210,0.2)`
- Stripe:`0 0 0 3px rgba(99,91,255,0.1)`
- Vercel:`0 0 0 2px var(--accent)`
- Notion:`0 0 0 2px rgba(217,115,13,0.4)`

**鼠标点击不显示 focus ring**——用 `:focus-visible` 而不是 `:focus`。CSS:
```css
:focus { outline: none; }
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px var(--accent);
}
```

### 4. 语义化 HTML Semantic HTML

**用对的 HTML 元素**——让屏幕阅读器理解页面结构。

**必检:**
- [ ] 用 `<button>` 不是 `<div onclick>`(按钮)
- [ ] 用 `<a href>` 不是 `<span onclick>`(链接)
- [ ] 用 `<nav>` `<main>` `<aside>` `<footer>` `<header>` 区分页面区域
- [ ] 用 `<h1>` `<h2>` `<h3>` 标题层级(不跳级)
- [ ] 用 `<ul>` `<li>` 列表
- [ ] 用 `<fieldset>` `<legend>` 表单分组
- [ ] 用 `<table>` `<thead>` `<tbody>` `<th>` 表格
- [ ] 表单 input 有关联 `<label>`(`for` 指向 `id`)
- [ ] 图片有 `alt`(装饰图 `alt=""`)

**常见失败:**
- 整个应用一个 `<div>` 套到底
- `<div class="button">` 不是 `<button>`
- input 没有 label,只有 placeholder
- 装饰图 `alt="一个图标"`(应该是 `alt=""`)
- `<h1>` 后面直接 `<h4>`(跳级)

### 5. ARIA 正确使用 ARIA Proper Use

> **黄金铁律:** "No ARIA is better than bad ARIA." —— 如果能用原生 HTML 解决,不要加 ARIA。

**ARIA 五条铁律:**
1. 不要用 ARIA 替代语义化 HTML(`<button>` 比 `<div role="button">` 好)
2. 不要改变原生元素的语义(`<h2 role="button">` 错,用 `<button><h2>`)
3. 所有交互 ARIA 元素必须键盘可达
4. 不要用 `aria-visible="false"` 隐藏可聚焦元素(用 `display: none`)
5. 所有交互元素必须有可访问名(`aria-label` 或文字内容)

**必检:**
- [ ] icon-only 按钮有 `aria-label`
- [ ] modal 有 `role="dialog"` + `aria-modal="true"` + `aria-labelledby`
- [ ] toast 有 `aria-live`(info/success=polite,error=assertive)
- [ ] loading 有 `role="status"` + `aria-live="polite"`
- [ ] 动态内容更新用 `aria-live`
- [ ] 折叠区域有 `aria-expanded`
- [ ] 当前页 nav 项有 `aria-current="page"`
- [ ] 表格 header 有 `scope="col"` / `scope="row"`

### 6. 不只靠颜色传达信息 Don't Rely on Color Alone

**色盲用户(8% 男性、0.5% 女性)看不到颜色区别**。任何用颜色传达的状态,必须有**第二视觉线索**。

**常见失败:**
- 错误只显示红边框(没有 icon 或文字)
- 表格"激活"行只变绿(没有 icon)
- 图表线条只靠颜色区分(没有线型/标记)
- 必填字段只用红星(没有 "(必填)" 文字)
- 状态点只靠颜色(红=错误、绿=成功,没有形状)

**修复:** 颜色 + 形状 / icon / 文字。
- 错误:红边框 + ❌ icon + 文字"邮箱格式不正确"
- 激活:绿背景 + ✓ icon
- 图表:不同颜色 + 不同线型(实线/虚线/点线)+ 图例
- 必填:红星 + "(必填)" 文字
- 状态点:红圆 + ❌、绿圆 + ✓、黄圆 + !

### 7. 动效尊重用户偏好 Respect Motion Preferences

**前庭功能障碍用户**会因动效眩晕。必须尊重 `prefers-reduced-motion`。

**必检:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

- [ ] 所有动画在 reduced-motion 下基本禁用
- [ ] parallax 滚动在 reduced-motion 下禁用
- [ ] 自动轮播在 reduced-motion 下停止
- [ ] 不用纯动效传达关键信息(必须有文字/icon 等替代)

## 验收清单

```text
页面 URL:_____________

□ 1. 颜色对比度(Stark / Chrome DevTools 检查)
  □ 正文 ≥ 4.5:1
  □ 大字 ≥ 3:1
  □ UI 组件 ≥ 3:1

□ 2. 键盘可达
  □ Tab 顺序符合视觉顺序
  □ Shift+Tab 反向
  □ Enter/Space 激活按钮
  □ ESC 关闭 modal
  □ 方向键在 tablist/menu 移动

□ 3. Focus 永远可见
  □ :focus-visible 不是 :focus
  □ focus ring 对比度 ≥ 3:1
  □ 不用 outline: none 不补 ring

□ 4. 语义化 HTML
  □ <button> 不是 <div onclick>
  □ <a href> 不是 <span onclick>
  □ <nav>/<main>/<aside>/<footer>/<header>
  □ <h1>-<h3> 不跳级
  □ <label for> 关联 input

□ 5. ARIA 正确
  □ icon-only 按钮有 aria-label
  □ modal 有 role="dialog" + aria-modal + aria-labelledby
  □ toast 有 aria-live
  □ 折叠有 aria-expanded
  □ 当前 nav 有 aria-current="page"

□ 6. 不只靠颜色
  □ 错误有 icon + 文字(不只红边框)
  □ 图表有线型/标记区分(不只颜色)
  □ 必填有文字"(必填)"(不只红星)

□ 7. 动效尊重偏好
  □ prefers-reduced-motion 媒体查询
  □ 所有动画在 reduced-motion 下禁用
```

## AI 验收员提示词

```text
你是一个严格的 a11y 验收员(WCAG 2.1 AA 标准)。审查下面这个页面/组件。

页面 / 组件:[提供截图、HTML、或 URL]

按 7 项检查:

1. 颜色对比度
   - 用 WCAG 公式检查所有文字 vs 背景对比度
   - 正文 ≥ 4.5:1,大字 ≥ 3:1,UI 组件 ≥ 3:1
   - 列出任何失败的颜色对

2. 键盘可达
   - Tab 顺序是否符合视觉顺序?
   - 所有交互元素(按钮/链接/输入)能 Tab 到达?
   - modal/drawer 内焦点是否 trap?
   - ESC 能关闭浮层?
   - 用 <div onclick> 代替 <button>?(致命)

3. Focus 永远可见
   - 是否用 :focus-visible 不是 :focus?
   - focus ring 对比度 ≥ 3:1?
   - 有没有 outline: none 不补 ring?

4. 语义化 HTML
   - 是否用 <button> <a> <nav> <main> <h1>-<h3>?
   - input 是否有 <label for>?
   - 装饰图是否 alt=""?

5. ARIA 正确
   - icon-only 按钮是否有 aria-label?
   - modal 是否有 role="dialog" + aria-modal + aria-labelledby?
   - toast 是否有 aria-live(info=polite, error=assertive)?
   - 折叠是否有 aria-expanded?
   - 当前 nav 是否有 aria-current="page"?

6. 不只靠颜色
   - 错误状态是否只有红边框?(必须加 icon/文字)
   - 图表是否只靠颜色区分?(必须加线型/标记)
   - 必填是否只有红星?(必须加"(必填)")

7. 动效尊重偏好
   - 是否有 prefers-reduced-motion 媒体查询?
   - 所有动画在 reduced-motion 下是否禁用?

每项打勾或打叉,失败的具体指出修复点。
任何一项失败,这个页面就是 a11y 不合格,不能 ship。
```

## 工具推荐

| 工具 | 用途 |
|---|---|
| **axe DevTools** | 浏览器插件,自动扫 a11y 问题 |
| **Stark** | 浏览器插件,对比度 + 色盲模拟 |
| **Chrome Lighthouse** | 自动 a11y 审计 |
| **WAVE** | webaim.org/resources/wave,在线 a11y 审计 |
| **NVDA / VoiceOver** | 屏幕阅读器测试 |
| **Keyboard only** | 关掉鼠标,只用键盘操作 |

## 与 SKILL.md 的关系

SKILL.md 的 "Three-Gate QA" 的 Engineering Gate 必须包含这一页。任何页面生成完,都要过这 7 项。

## 权威信源

- WCAG 2.1(w3.org/TR/WCAG21)
- "No ARIA is better than bad ARIA" — W3C WAI-ARIA Authoring Practices
- "Semantic HTML" — MDN web docs
- Marcy Sutton 的 a11y 演讲
