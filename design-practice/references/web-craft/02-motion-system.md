# 02 — Web 动效系统(可直接抄进代码)

> 与 `references/stage2-motion-discipline.md` 的分工:那份是**SaaS 内部页**的动效语法(状态过渡、direction 表、五问)。本文件是它的"**大舞台版**"——网页还多了**首屏入场编排、scroll 触发、GPU 合成层、可打断性、session 级动效预算**。两者共用 token;本文件补 stage2 没覆盖的网页特有部分。已有 stage2 token 的,沿用;网页新增的在下面。

## 0. 一句话总纲

**动效是语法,不是烟花。** 每一段动效必须能回答"它为什么动"。AI 网页的动效塑料味来自两个极端:**要么什么都不动(死)**,要么**什么都 fade-in-up 从头到尾浮(累)**。顶级网页的动效是**克制的、即时响应的、只在关键节点发生的、永远不挡用户操作的**。

下面 8 条铁律是 web 动效的全部纪律。每条给 token + CSS + 反例。

---

## 铁律 1:UI 响应一律 ease-out,不用 ease-in

### 为什么
`ease-out` = 快起慢收(曲线前半陡、后半缓)。元素**一开始就动**,然后**稳稳停住**——读作"即时响应"。`ease-in` = 慢起快收——元素**先犹豫再加速**——读作"卡顿 / 在加载"。

**人脑对"开始移动"的延迟极敏感**(<100ms 就觉得慢)。ease-out 让动效在前 30% 时间就走完大半位移,骗过这个敏感度。ease-in 把位移堆在后半段,正好踩在敏感点上。

### token(沿用 stage2-motion-discipline.md)

| Token | 曲线 | 用途 |
|-------|------|------|
| `ease.out` | `cubic-bezier(0.16, 1, 0.3, 1)` | **入场/出现/交互响应**(主力,网页 80% 用它) |
| `ease.in` | `cubic-bezier(0.7, 0, 0.84, 0)` | **仅退场/消失**(元素加速离开) |
| `ease.standard` | `cubic-bezier(0.4, 0, 0.2, 1)` | 通用状态变化(颜色/尺寸) |

> **规则:默认全用 `ease.out`。`ease.in` 只用于"元素消失/退场",绝不用于入场或交互响应。** 入场用 ease-in 是 web 动效最常见的塑料 tell。

### CSS
```css
/* 正解:菜单从触发点打开,快起慢收 */
.menu { transform-origin: top right; opacity: 0; transform: translateY(-4px) scale(0.98); }
.menu.open { opacity: 1; transform: none; transition: opacity 200ms cubic-bezier(0.16,1,0.3,1), transform 200ms cubic-bezier(0.16,1,0.3,1); }
```

### 反例对照
| 场景 | 塑料(AI 默认) | 顶级 |
|------|--------------|------|
| 下拉打开 | `transition: all .3s ease-in` —— 慢起,像在加载 | `ease-out` 200ms —— 即时弹出再稳住 |
| 按钮按下反馈 | 无动画 / `ease-in` | `ease-out` 100ms,press 即响应 |
| 元素退场 | `ease-out` 慢悠悠消失 | `ease.in` 加速离开(或干脆 150ms ease-out 缩短) |

---

## 铁律 2:大部分动画 ≤300ms,超过读作卡顿

### 为什么
人眼对 >300ms 的状态过渡开始读作"延迟"。但**这不是绝对的**——要分两类:

- **交互响应类**(用户触发的:悬停、按下、打开菜单、切换 tab):**硬上限 300ms**,理想 100-200ms。这类动效挡在用户操作路径上,慢 = 阻碍。
- **入场编排类**(首屏 hero 文字逐行出现、scroll 触发的 reveal):可到 **400-700ms**。这类是**非阻塞的装饰**,用户不在等它完成。但若它**延迟了用户的第一次可交互**,就是错的。

### token

| Token | 时长 | 用途 |
|-------|------|------|
| `dur.micro` | 100ms | 微反馈:hover、press、focus ring、toggle |
| `dur.fast` | 150-200ms | 小元素:tooltip、badge、链接颜色、tab 切换 |
| `dur.normal` | 200-300ms | 中等:菜单、popover、抽屉、面板 |
| `dur.slow` | 400-700ms | **仅入场编排/scroll reveal**(非阻塞) |

### 反例对照
| 场景 | 塑料 | 顶级 |
|------|------|------|
| hover | `transition: all .5s` —— 鼠标移上去半秒才变 | 100-150ms ease-out |
| 菜单打开 | 600ms —— 等得心烦 | 200ms ease-out |
| 首屏文字入场 | 1.2s 慢慢浮起 —— 挡着内容 | 500ms ease-out + 60ms 错峰,**不挡第一次点击** |
| 列表项删除 | 300ms 整行淡出 | 150-200ms 高度塌缩 + 淡出 |

> **关键判断:这段动效挡不挡用户的下一步操作?** 挡 → ≤300ms。不挡(纯装饰)→ 可放宽,但仍要克制。

---

## 铁律 3:只动 `transform` 和 `opacity`(GPU 合成层)

### 为什么
浏览器渲染管线:**Style → Layout → Paint → Composite**。不同 CSS 属性触发不同阶段,代价天差地别:

| 属性 | 触发阶段 | 代价 | 能不能动 |
|------|---------|------|---------|
| `transform` `opacity` | **仅 Composite** | 极低(GPU 层移动/合成) | ✅ **只动这两个** |
| `filter` `backdrop-filter` | Paint + Composite | 中(重绘 + 合成) | ⚠️ 小面积可以 |
| `background-color` `color` `box-shadow` | Paint(重绘) | 中 | ⚠️ 小面积可以 |
| `width` `height` `margin` `padding` `top` `left` | **Layout(重排)** | **极高,整棵树重算** | ❌ **绝不动** |

**动 `width`/`margin`/`top` 会让浏览器对整个受影响子树重新计算布局**——一帧掉到 16.6ms(60fps 预算)以下就是肉眼可见卡顿。`transform`/`opacity` 走合成层,不动布局,几乎免费。

### CSS:用 transform 替代布局属性

```css
/* ❌ 塑料:动 margin 触发 layout,滚动时掉帧 */
.card { margin-top: 0; transition: margin-top .3s; }
.card:hover { margin-top: -8px; }

/* ✅ 顶级:动 transform,仅合成层 */
.card { transform: translateY(0); transition: transform .3s cubic-bezier(0.16,1,0.3,1); }
.card:hover { transform: translateY(-2px); }

/* ❌ 塑料:折叠面板动 height,每次测高 + 重排 */
.expand { height: 0; transition: height .3s; }
.expand.open { height: 200px; }

/* ✅ 顶级:用 grid 0fr→1fr,免测高,不触发 layout 抖动 */
.expand { display: grid; grid-template-rows: 0fr; transition: grid-template-rows .3s cubic-bezier(0.4,0,0.2,1); }
.expand > div { overflow: hidden; }
.expand.open { grid-template-rows: 1fr; }
```

### 优化层:`will-change` 与 `contain`(用对是加速,用错是灾难)
```css
/* ✅ 仅对即将动起来的元素加,用完移除 —— 否则每个元素都建 GPU 层,内存爆 */
.menu { will-change: transform, opacity; }
/* JS:动画结束后 element.style.willChange = 'auto'; */

/* ✅ 限制重排范围:列表项各自 contain,某项动不影响兄弟 */
.list-item { contain: layout paint; }
```

### 反例对照
| 场景 | 塑料 | 顶级 |
|------|------|------|
| 卡片 hover 上浮 | 动 `margin-top` / `top` | 动 `transform: translateY()` |
| 模态框入场 | 动 `width`/`height` 从 0 展开 | 动 `transform: scale()` + `opacity` |
| 侧栏滑出 | 动 `left`/`margin-left` | 动 `transform: translateX()` |
| 卡片阴影 hover | 动 `box-shadow`(重绘) | 用伪元素叠一层 + 动它的 `opacity`(只合成) |

---

## 铁律 4:动效必须可打断(interruptible),不能锁住用户

### 为什么
最破坏体验的动效:**用户在动画进行中想操作,但元素被动画锁住,操作无响应或跳帧**。例:菜单 300ms 打开中,用户立刻鼠标移开想关——如果动效"不可打断",它会先播完打开再播关闭,用户看到菜单闪一下又关,像 bug。

**CSS `transition` 天然可打断**:你中途改目标值,它会从当前计算值平滑过渡到新值。**出问题的是 JS 驱动的 `@keyframes` 和 `setTimeout` 链**——它们"提交"了一整段序列,中途不可改。

### 规则
1. **优先用 CSS `transition`**(天然可打断),少用 `@keyframes` 动画。
2. **不要用 `setTimeout` 链编排动效**——用 `transitionend` 事件或 Web Animations API。
3. **JS 动画用 Web Animations API**(`element.animate()`),它支持 `commit()` + 反向播放,可中途打断重定向。
4. **hover 这类"用户可能反复进出"的交互,绝不锁**——离开时立刻从当前位置过渡回默认。
5. **永远不阻塞输入**:动效进行中,元素必须保持可点击/可聚焦(`pointer-events` 不要因为动画设成 none,除非是 loading)。

### CSS:transition 天然可打断
```css
/* 用户反复 hover 也不卡:每次状态变化都从当前位置继续 */
.btn { transition: background-color 150ms cubic-bezier(0.16,1,0.3,1); }
```

### JS:用 WAAPI 做可打断的入场
```js
// ✅ 可打断:新动画会取消旧的
function reveal(el) {
  el.getAnimations().forEach(a => a.cancel()); // 先取消进行中的
  el.animate(
    [{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }],
    { duration: 400, easing: 'cubic-bezier(0.16,1,0.3,1)', fill: 'forwards' }
  );
}
```

### 反例对照
| 场景 | 塑料 | 顶级 |
|------|------|------|
| 菜单开关 | 打开动画必须播完才能关 | 中途移开立即从当前位置关 |
| Toast 误触 | 进场动画期间点不掉 | 进场中也能点关闭 |
| 列表删除连击 | 第一次删除动画没完,第二次卡住 | 每次操作立刻接管当前状态 |

---

## 铁律 5:高频动作(键盘驱动、每天看 100 次)去掉动效

### 为什么
**动效有 session 级预算。** 一个用户每次按 ↓ 切换列表项都看 200ms 动画,看 100 次就累积 20 秒纯等待——他觉得"这工具慢"。**Linear 的 ⌘K 命令面板选中项几乎零动效**,Rauno Freiberg 的站点接近零动效——专业用户每天用 100 次的东西,动效是负担不是 delight。

### 规则:session 频次 → 动效预算
| 用户操作频率 | 动效策略 |
|------------|---------|
| 每天/每 session >10 次(键盘导航、⌘K、tab 切换、列表选中、分页) | **≤100ms 或零动效** |
| 每天 1-10 次(打开抽屉、切换视图、提交表单) | 150-200ms |
| 一次性(首屏入场、scroll reveal、页面过渡) | 可 400-700ms |

### 反例对照
| 场景 | 塑料 | 顶级 |
|------|------|------|
| ⌘K 命令面板选中项 | 每按 ↑↓ 都 200ms 滑动高亮 | 即时跳,无动效(或 ≤80ms) |
| Tab 切换 | 每次切换都 300ms 内容淡入 | ≤120ms 或即时 |
| 表格行选中 | 行高亮渐变 200ms | ≤80ms 即时 |

---

## 铁律 6:必须 respect `prefers-reduced-motion`

### 为什么
前庭功能紊乱、晕动症、注意力障碍的用户,动效会引发生理不适。`prefers-reduced-motion: reduce` 是**无障碍硬底线**,不是可选。web-craft 所有动效都必须有这个兜底。

### CSS(全局兜底,放在样式最底)
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

### JS:scroll reveal 在 reduced-motion 下根本不触发
```js
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!reduce) {
  // 才注册 IntersectionObserver 做渐入
} else {
  // 直接显示所有内容,opacity:1,无动画
  document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('is-visible'));
}
```

> **reduced-motion 模式下:元素直接到位(不滑、不淡、不弹);spinner 仍转(它是连续进度指示,不是过渡);进度条仍走。** 见 stage2-motion-discipline.md 的 reduced-motion 节。

---

## 铁律 7:spring/物理曲线 vs 缓动——什么时候用哪个

### 为什么
两种动效曲线本质不同:
- **缓动(easing)**:固定时长 + 固定曲线,可预测、可调、快。适合**离散状态过渡**(打开/关闭、出现/消失、切换)。
- **spring(物理弹簧)**:基于质量/刚度/阻力的物理模拟,**有动量、会过冲**。适合**带真实惯性的手势**(拖拽抛掷、下拉刷新、滑动删除、物理滚动)。

### 规则:**状态过渡用缓动;惯性手势用 spring。**
```
离散状态(打开菜单/切换 tab/模态入场) → 缓动(可预测,不过冲)
惯性手势(拖拽卡片抛出/下拉刷新回弹/swipe 删除) → spring(物理真实)
```

**Linear 著名地禁用 spring/bounce 用于状态过渡**(见 style-linear.md:绝禁 `cubic-bezier(0.34,1.56,0.64,1)`)——专业工具不要惊喜式过冲。但 Linear 的拖拽排序用物理 spring,因为那是真实惯性。

### CSS 的局限
CSS 原生**没有** spring 函数(2024+ 才有 `linear()` 可近似弹簧曲线)。要做真 spring:
- **手势场景**:用 JS framer-motion / Popmotion / WAAPI + 物理参数。
- **纯 CSS 状态过渡**:别假装做 spring(用 `cubic-bezier(0.34,1.56,0.64,1)` 这种带过冲的曲线模拟)——它会在所有元素上无差别过冲,廉价。**老实缓动。**

### 反例对照
| 场景 | 塑料 | 顶级 |
|------|------|------|
| 模态框入场 | `cubic-bezier(0.34,1.56,0.64,1)` 弹一下 | `cubic-bezier(0.16,1,0.3,1)` 稳稳到位 |
| 拖拽卡片抛出 | 固定缓动,感觉"被吸附" | spring,感觉"被甩出去"(真实惯性) |
| 切换开关 | bounce 回弹 | 150ms ease-out |

---

## 铁律 8:入场/出场要有空间一致性(从哪里来,回哪里去)

### 为什么
**元素从它"居住的位置"生长出来**,而不是凭空在中心淡入。一个下拉菜单从触发按钮"长出来",读作"它属于这个按钮"。在中心淡入,读作"它从虚无中弹出"——廉价。人脑对空间起源有预期,违背就"说不出哪里怪"。

### 规则:`transform-origin` 必须匹配元素的空间归属
| 元素 | 从哪里出现 | transform-origin | 动效 |
|------|-----------|-----------------|------|
| 下拉菜单 | 触发按钮下方 | `top center` | scale 0.98→1 + translateY(-4px→0) |
| 右键菜单 | 鼠标点 | 鼠标坐标 | 同上,origin 在点击点 |
| tooltip | 触发元素 | 触发侧 | scale 0.9→1 + fade |
| 抽屉 | 屏幕边缘 | 该边缘 | translateX/Y 从边缘滑入 |
| 模态框 | 屏幕中心 | `center` | scale 0.96→1 + fade(它住在中心) |
| toast | 角落 | 该角 | 从角滑入 |
| 首屏 hero 文字 | 原位 | 默认 | translateY(8px→0) + fade(轻微上浮,不是大位移) |

### CSS
```css
/* ✅ 下拉从触发点长出 */
.dropdown { transform-origin: top center; opacity: 0; transform: scale(0.98) translateY(-4px);
  transition: opacity 150ms cubic-bezier(0.16,1,0.3,1), transform 150ms cubic-bezier(0.16,1,0.3,1); }
.dropdown.open { opacity: 1; transform: none; }

/* ❌ 塑料:在中心淡入,与触发点无关 */
.dropdown { opacity: 0; transform: scale(0.5); } /* 从屏幕中心缩放,失去归属感 */
```

### 反例对照
| 场景 | 塑料 | 顶级 |
|------|------|------|
| 点击按钮开菜单 | 菜单在屏幕中心淡入 | 从按钮下方 scale 出 |
| hover 出 tooltip | tooltip 从远处飞来 | 从触发元素 scale 出 |
| 模态框 | 从左上角滑入(它不住那) | 从中心 scale(它住中心) |

---

## 入场编排(首屏 hero 文字)— 唯一允许"编排"的地方

首屏 hero 可以做**一次性的逐行/逐元素入场**,这是网页唯一合理的大编排。纪律:

```css
/* hero 文字逐行上浮,60-80ms 错峰 */
.hero-line { opacity: 0; transform: translateY(10px);
  animation: heroIn 500ms cubic-bezier(0.16,1,0.3,1) forwards; }
.hero-line:nth-child(1) { animation-delay: 0ms; }
.hero-line:nth-child(2) { animation-delay: 70ms; }
.hero-line:nth-child(3) { animation-delay: 140ms; }
@keyframes heroIn { to { opacity: 1; transform: none; } }
```

**铁律**:
1. **只在首屏、只在首次加载**做一次。滚动回来的 section 不要重新编排。
2. **总时长 <1s**(首行到末行结束),且**不挡第一次点击**(CTA 出现后立即可点,不等动画完)。
3. **位移 ≤10-12px**——大位移(20px+)显得拖沓。
4. **错峰 60-80ms**,不要 200ms(太慢显得逐个排队)。

---

## 反塑料证据(web 动效的"人做的"信号)

- [ ] 交互响应用 `ease-out`,不用 `ease-in` 入场
- [ ] 用户触发的动效 ≤300ms
- [ ] 只动 `transform`/`opacity`,不动 layout 属性
- [ ] hover/高频操作不锁(可打断)
- [ ] ⌘K / 键盘导航 / 列表选中:零动效或 ≤100ms
- [ ] `prefers-reduced-motion` 全局兜底 + JS 不触发 reveal
- [ ] 状态过渡用缓动,手势用 spring,不混
- [ ] 入场从空间归属点生长(transform-origin 正确)
- [ ] 首屏编排 <1s、不挡首次点击、位移 ≤12px

## 常见塌方表

| 塌成什么 | 病因 | 修复 |
|---------|------|------|
| 滚动时整页掉帧 | 动了 `margin`/`top`/`width`(layout) | 换成 `transform` |
| 菜单打开像在加载 | 用了 `ease-in` | 换 `cubic-bezier(0.16,1,0.3,1)` |
| 用户连点操作卡顿 | 动效不可打断(setTimeout 链) | 改 CSS transition 或 WAAPI |
| 专业用户嫌慢 | 高频操作带了 200ms 动效 | ⌘K/列表选中改 ≤100ms 或零 |
| 状态切换莫名弹一下 | 用 bounce 曲线模拟 spring | 改缓动,spring 只给手势 |
| 动效在 reduced-motion 还播 | 缺全局兜底 | 加 `@media (prefers-reduced-motion: reduce)` |
| 元素凭空中心淡入 | transform-origin 没设对 | origin 设到触发点/归属边 |
