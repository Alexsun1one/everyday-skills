# 05 — 把 Core Web Vitals 当设计约束

> 性能不是"上线后优化",是**设计约束**——它在画线稿阶段就决定了你能不能用那张 4K 大图、那套 5 个字重的字体、那段 scroll 监听。本文件把每个性能指标**翻译成设计师/前端要做(或不做)的具体动作**。AI 网页的性能塑料味:首屏白屏 3 秒、字体加载时整页跳动、图片把版面顶下去、滚动掉帧——全是"上线后才发现"的病,而病因在设计阶段。

## 0. 三大核心指标及目标值(Google Core Web Vitals,2026 现行)

| 指标 | 测什么 | 🟢 好 | 🟠 需改进 | 🔴 差 |
|------|--------|-------|----------|------|
| **LCP** Largest Contentful Paint | 加载速度(最大内容元素渲染完成) | **<2.5s** | 2.5-4s | >4s |
| **INP** Interaction to Next Paint | 交互响应(用户操作到下一帧渲染的最长延迟) | **<200ms** | 200-500ms | >500ms |
| **CLS** Cumulative Layout Shift | 视觉稳定(加载过程中元素位移累积) | **<0.1** | 0.1-0.25 | >0.25 |

> INP 在 2024 年 3 月正式取代 FID,成为交互指标。它不是"第一次交互的延迟",而是**所有交互中 worst-case 的延迟**——所以一段卡顿的 scroll 动效就能把它打红。

**总纲**:这三个数不是给运维看的报表,是**设计师在选图、选字体、选动效时必须守的红线**。下面逐个翻译。

---

## 1. LCP < 2.5s —— "首屏最大内容多久能看见"

### LCP 元素通常是
首屏的 **hero 大图** 或 **hero 大标题文字**。优化**只盯这一个元素**——其余内容慢一点不影响 LCP。

### 设计师/前端要做的具体动作
1. **绝不 lazy-load LCP 图**——这是最常见错误。首屏大图必须 `loading="eager"` + `fetchpriority="high"`。lazy 只给折叠下方图。
2. **预加载 LCP 图和字体**:
   ```html
   <link rel="preload" as="image" href="hero.avif" fetchpriority="high">
   <link rel="preload" as="font" type="font/woff2" href="brand.woff2" crossorigin>
   ```
3. **LCP 图用现代格式 + 响应式**:`<picture>` AVIF > WebP > JPEG,配 `srcset` 按设备服务正确分辨率(别给手机塞 4000px 图)。
4. **别让 render-blocking CSS/JS 挡住首屏**:内联关键 CSS(critical CSS),defer 所有非首屏 JS。
5. **服务器首字节响应(TTFB)<0.8s**——这通常是后端/CDN 的事,但设计师要知道:首屏图再快,TTFB 慢,LCP 也红。
6. **首屏预算**:关键 CSS <34KB(压缩)、内联;首屏 JS 尽量为 0 或 <50KB。

### 反例对照
| 场景 | 塑料(AI 默认) | 顶级 |
|------|--------------|------|
| hero 大图 | `loading="lazy"`(首屏图被懒加载,LCP 炸) | `eager` + `fetchpriority="high"` + preload |
| 图格式 | 原始 JPEG/PNG 2MB+ | AVIF/WebP + srcset,首屏 <200KB |
| 第三方脚本 | 顶部同步加载埋点/客服 | `defer`/`async`,交互后或空闲加载 |
| CSS | 一个大 CSS 文件阻塞渲染 | 内联 critical + 异步加载剩余 |

---

## 2. CLS < 0.1 —— "加载时版面不要乱跳"

### CLS 的三大病因(全是设计阶段能防的)
1. **图片/视频/iframe 没有预留尺寸** → 加载完把下方内容顶下去。
2. **字体加载后文字尺寸变** → 整段重排,所有元素位移。
3. **后注入的元素**(cookie 条、广告、banner)把内容往下推。

### 设计师/前端要做的具体动作
1. **所有图片/视频/iframe 必须给尺寸**——`width`+`height` 属性,或 CSS `aspect-ratio`。这是 CLS #1 病因,#1 解法。
   ```html
   <!-- ✅ 有尺寸,加载不位移 -->
   <img src="https://example.com/hero.avif" width="1600" height="900" alt="...">
   <!-- 或 CSS -->
   .hero-img { aspect-ratio: 16 / 9; width: 100%; }
   ```
2. **字体加载用 metric matching**(见下节字体策略),消除 swap 时的位移。
3. **cookie 条/banner 用 overlay(`position: fixed/absolute`)覆盖,不要 push 内容**。底部 banner 用 fixed 底栏浮在上面,不要让正文 margin 让位。
4. **广告位/动态内容预留占位**(固定高度的空 slot),内容填入时不位移。
5. **动效只用 transform/opacity**(见 `02-motion-system.md` 铁律 3)——它们不触发 layout,不产生 shift。动 width/margin = CLS 来源。

### 反例对照
| 场景 | 塑料 | 顶级 |
|------|------|------|
| hero 图 | 无 width/height,加载完顶下 CTA | `aspect-ratio` 预留 |
| 字体 | 默认加载,swap 时整页跳 | font metric override 匹配 |
| cookie 条 | push 正文向下 | `position: fixed` 浮层覆盖 |
| 列表项入场 | 动 margin 推开兄弟 | 动 transform(不占位) |

---

## 3. INP < 200ms —— "点下去多久有反应"

### INP 测什么
用户**任意一次交互**(点击/键入/滚动)到浏览器**画出下一帧**的最长延迟。一段卡顿的 scroll 动效、一个长 JS 任务、一次 forced reflow,都能把它打红。

### 设计师/前端要做的具体动作
1. **动效只用 transform/opacity**(见 `02` 铁律 3)——动 layout 属性会让主线程重排,直接拖高 INP。这是动效纪律和 INP 的直接关联。
2. **不在 scroll/input 上跑重 JS**——scroll 监听里别算布局、别操作 DOM。用 `requestAnimationFrame` 节流,或用 CSS scroll-driven animations(跑合成线程,见 `03`)。scroll 监听必须 `passive: true`。
3. **拆分长 JS 任务**(long task >50ms 阻塞主线程):用 `requestIdleCallback` / `setTimeout(0)` / `scheduler.yield()` 让出主线程。
4. **避免 layout thrashing(强制同步重排)**:别在循环里"读 offsetWidth 再写 style"——读后写会强制浏览器同步重排。批量读、批量写。
5. **第三方脚本(分析/客服/A-B 测试)是 INP 头号杀手**——延迟加载,交互后或空闲再加载。
6. **高频操作去掉动效**(见 `02` 铁律 5)——⌘K、列表选中、tab 切换零动效或 ≤100ms,直接降 INP。

### 反例对照
| 场景 | 塑料 | 顶级 |
|------|------|------|
| 滚动 | JS scroll 监听改 DOM | CSS scroll-driven / passive + rAF |
| 卡片 hover | 动 margin(重排) | 动 transform(合成) |
| 列表渲染 | 一次性渲染 1000 项 | 虚拟列表 / 分批 yield |
| 第三方 | 顶部同步加载 5 个 SDK | 延迟到交互后 |

---

## 4. 字体加载策略 —— 防 FOUT/CLS 的硬规则

### 三种 `font-display` 策略(选哪个看场景)
| 值 | 行为 | 代价 | 适用 |
|----|------|------|------|
| `swap` | 立刻显示 fallback 文字,字体加载完替换 | FOUT(无样式文字闪一下)+ 可能位移 | **正文/UI 默认**(优先可读性) |
| `optional` | 给字体极短窗口(~100ms),没加载完就**永不替换** | 不位移,但可能不显示品牌字体 | **对 CLS 极敏感**的正文 |
| `block` | 文字隐形最多 3s 再显 fallback | FOIT(隐形文字,像加载卡住) | **❌ 避免** |

```css
@font-face {
  font-family: 'Brand';
  src: url('brand-subset.woff2') format('woff2');
  font-display: swap;            /* ✅ 正文默认 swap */
  font-weight: 510;
}
```

### 消除字体 swap 位移(metric matching)
字体加载完,若 fallback 与 web font 字宽不同,整段文字重排 → CLS。用 font metric override 让 fallback 尺寸匹配 web font:
```css
@font-face {
  font-family: 'Brand-Fallback';
  src: local('Arial');
  size-adjust: 98%;        /* 微调,让 Arial 与 Brand 字宽接近 */
  ascent-override: 92%;
  descent-override: 22%;
}
body { font-family: 'Brand', 'Brand-Fallback', sans-serif; }
```

### 字体性能铁律
1. **子集化(subset)**:只打包页面用到的字形。CJK 字体动辄数 MB,**必须子集化**(用到的汉字才打包),否则 LCP 必炸。
2. **预加载首屏字体 woff2**:`<link rel="preload" as="font" crossorigin>`(必须 `crossorigin`,否则 preload 不生效)。
3. **限制字重/字族数量**:每多一个字重 = 一个请求 + 渲染负担。正文 1 个字重(可变字体 Variable Font 一个文件覆盖全字重,优先用)。
4. **变长字体优先**:一个 Variable Font 文件覆盖 100-900 全字重,比加载 5 个静态字重省 80% 流量(Linear 的 Inter Variable 就是这么做的)。
5. **本地 fallback**:`src: local('Inter')` 优先用系统已装的,省下载。

### 反例对照
| 场景 | 塑料 | 顶级 |
|------|------|------|
| 字重 | 加载 Regular/Bold/Semibold 三个静态文件 | 一个 Variable Font 文件 |
| CJK 字体 | 加载完整 4MB 字体 | 子集化到用到的字,<200KB |
| 加载策略 | `font-display: block`(隐形 3s) | `swap` + metric matching |
| 预加载 | 无 preload,字体晚于 CSS 才请求 | `rel="preload"` + crossorigin |

---

## 5. 图片策略 —— 格式 / 尺寸 / 懒加载边界

### 格式优先级
AVIF(比 JPEG 小 ~50%) > WebP(小 ~30%) > JPEG/PNG fallback。用 `<picture>` 多源 + fallback:
```html
<picture>
  <source type="image/avif" srcset="hero.avif">
  <source type="image/webp" srcset="hero.webp">
  <img src="https://example.com/hero.jpg" width="1600" height="900" alt="..." loading="eager" decoding="async" fetchpriority="high">
</picture>
```

### 响应式分辨率(别给手机塞 4K 图)
```html
<img src="https://example.com/hero-800.jpg"
     srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1600.jpg 1600w, hero-2400.jpg 2400w"
     sizes="(max-width: 768px) 100vw, 50vw"
     width="1600" height="900" alt="...">
```
`sizes` 告诉浏览器"这图在手机占满屏宽、桌面占半屏",浏览器按设备 DPR 自动选最合适的分辨率文件。

### 懒加载边界
| 图位置 | `loading` | `fetchpriority` |
|--------|----------|----------------|
| 首屏 / LCP 图 | `eager` | `high` |
| 折叠下方图 | `lazy` | `low` / 默认 |

**铁律:绝不对首屏/LCP 图用 lazy**——它会等主线程空闲才加载,LCP 炸。

### 其他
- `decoding="async"` 让图片异步解码,不阻塞主线程。
- 装饰性图用 CSS `background`(可被浏览器优化),但**承载内容的图必须用 `<img>`**(无障碍 + 可被索引)。

---

## 6. 感知性能 —— 让"慢"感觉"快"

### 骨架屏 vs spinner
- **骨架屏(skeleton)**:用灰块占位,显示"即将出现的内容结构"。**用于 >300ms 的内容加载**——它预演了版面,降低感知等待。
- **spinner**:转圈。**用于短时的不确定操作**(<2s),或无法预知结构的加载。
- **判断**:**能预知结构就用骨架,不能就用 spinner**。骨架屏必须**尺寸匹配最终内容**,否则骨架→真实内容又是一次 CLS。
- **<300ms 的操作:不给任何指示,直接显示结果**(指示器会闪一下反而显得卡)。

### 乐观更新(Optimistic Update)
用户点"点赞/提交/收藏",**立即在本地反映成功状态**,再异步和服务器对账。失败再回滚。**感觉即时**。
```
用户点"赞" → 立刻 ❤️+1(本地) → 后台请求 → 成功确认 / 失败回滚 + toast
```
适用:幂等的、低风险的、用户期望即时的操作(点赞、收藏、勾选)。不适用:支付、删除(这些必须等服务器确认)。

### 进度反馈梯度
| 操作时长 | 反馈 |
|---------|------|
| <300ms | 无指示(直接出结果) |
| 300ms-2s | spinner / 内联 loading |
| >2s | 进度条(给"还要多久"的预期) |
| >10s | 分步进度 / 允许后台进行 |

### 预取(prefetch)下一页
用户 hover 导航链接 / 页面空闲时,**预取下一页资源**,点击时秒开。这是 Linear/Vercel 导航感觉"瞬时"的秘密。

---

## 7. 首屏预算(Above-the-fold budget)

上线前给首屏一个预算,超标就砍:
- **关键 CSS**:内联,<34KB(压缩后)。其余 CSS 异步加载。
- **首屏 JS**:尽量为 0(静态页)/ <50KB(交互页)。非首屏 JS 全 `defer`。
- **首屏图**:<200KB(AVIF/WebP)。
- **第三方脚本**:首屏 0 个(分析/客服/A-B 全部延迟到交互后或空闲)。
- **目标**:4G 网络下,首屏有用内容 <1s 可见,LCP <2.5s。

> **第三方脚本是性能头号杀手。** 一个客服 widget + 一个分析 SDK + 一个 A-B 测试脚本,加起来能拖垮 LCP 和 INP。规则:**首屏不加载任何非必要第三方脚本**。

---

## 反塑料证据(性能即设计的"人做的"信号)

- [ ] LCP 图 `eager` + `fetchpriority="high"` + preload,不 lazy
- [ ] 所有图/视频/iframe 有 `width`+`height` 或 `aspect-ratio`(防 CLS)
- [ ] 字体 `font-display: swap` + 子集化 + metric matching(防 FOUT/CLS)
- [ ] 变长字体优先,字重数量最小化
- [ ] 动效只 transform/opacity,不触发 layout(降 INP + CLS)
- [ ] scroll 监听 `passive` + 不跑重 JS
- [ ] 第三方脚本延迟到交互后/空闲加载
- [ ] 懒加载边界清晰:首屏 eager,折叠下 lazy
- [ ] >300ms 加载用骨架屏(尺寸匹配),<300ms 无指示
- [ ] 首屏预算:CSS<34KB / 首屏 JS≈0 / 图<200KB / 第三方 0

## 常见塌方表

| 塌成什么 | 病因 | 修复 |
|---------|------|------|
| 首屏白屏 3 秒 | LCP 图 lazy + 大 CSS 阻塞 | eager+preload + 内联 critical CSS |
| 加载时版面乱跳 | 图无尺寸 / 字体 swap 位移 | aspect-ratio + font metric matching |
| 滚动掉帧、点击慢 | 动 layout 属性 / scroll 跑重 JS | transform/opacity + passive 监听 |
| CJK 页面巨慢 | 加载完整 CJK 字体 | 子集化到用到的字 |
| 字体加载文字隐形 | `font-display: block` | 改 `swap` |
| 感觉慢 | 全用 spinner | >300ms 改骨架屏 + 乐观更新 |
| 第三方拖垮 | 顶部同步加载 SDK | 延迟到交互后 |
