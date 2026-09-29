# 03 — 滚动叙事 / 长页动线

> 长页(品牌长页、产品发布页、编辑型报道、Apple 式 scrollytelling)的全部难点是**节奏**。AI 的长页塑料味来自一个默认动作:**每个 section 都 fade-in-up**,从头浮到尾——读起来像幻灯片,像在等动画,而不是在读内容。本文件给长页的节奏纪律、scroll 触发的克制法则、pin/sticky/parallax 的"防土味"边界。

## 0. 核心心法:滚动是用户在翻页,不是在放映

长页的动效第一原则:**用户滚动是为了看内容,不是为了看动画。** 每一段 scroll 动效都在和"用户想看的内容"抢注意力。所以——**大部分 section 根本不该有 scroll 动效**。克制是默认,动效是例外。

stage2-motion-discipline.md 已立此规:"Don't animate on scroll-trigger for everything. One or two reveal-on-scroll moments are fine; animating every section is noise." 本文件展开它。

---

## 1. 长页注意力曲线(先理解节奏的生理基础)

人滚动长页时,注意力不是平的,是一条曲线:

```
注意力
  ▲
  │  █                                          █
  │  █ █                                      █ █
  │  █   █                                  █   █
  │  █     █                            █       █
  │  █       █   █                  █          █
  │  █         █   █            █                █
  │  █           █   █      █                    █
  │  █             █   ███                       █
  └──────────────────────────────────────────────▶ 滚动位置
     Hero        S2        S3       S4        Final CTA
   (峰值)       (次峰)   (谷底)  (回升)      (次峰值)
```

**规律**:
- **Hero 是第一峰值**——注意力最高,放最硬的价值主张。
- 注意力随滚动**衰减**——中间会进入"谷底",用户开始 skim。
- **每个 section 的强标题/强视觉是一个"再激活尖峰"**——用它把衰减的注意力拽回来。
- **Final CTA 是第二峰值**——用户滚到底,做转化决策时注意力回升。

### 设计含义(硬规则)
1. **最硬的内容放峰值位**(Hero + Final CTA)。**不要把关键转化信息埋在"谷底"**(长 undifferentiated 中段)。
2. **中段每个 section 必须有强标题 + 视觉变化**来制造再激活尖峰——否则用户一路 skim 到底,中间全没看。
3. **section 高度要有变化**——不要每个 section 等高。高密度 section → 留白呼吸 section → 高密度,形成"密-疏-密"的节奏。等高 section 排下来 = 视觉催眠,加速 skim 跳过。

---

## 2. Section 节奏(间距与高度纪律)

| Token | 桌面 | 移动 | 用途 |
|-------|------|------|------|
| `section.gap` | 96-160px | 64-96px | section 之间(长页比 SaaS 内部页 40-48px 大 2-3 倍) |
| `section.gap.hero` | 120-200px | 80-120px | hero 与第一段之间(最大呼吸) |
| `section.padding-y` | 80-120px | 56-80px | section 内部上下 |

**节奏纪律**:
- **密-疏交替**:信息密集 section(feature 矩阵、数据可视化)后跟一个**大留白 section**(一句大字宣言 + 极多空白),让眼睛休息。
- **section 不等高**:有的 section 100vh(沉浸),有的 40vh(过渡句),有的 60vh(标准)。等高 = 催眠。
- **不要每个 section 都用同一个栅格宽度**:有的 full-bleed(出血大图),有的 1200px 容器,有的 800px 窄列——宽度变化也是节奏。

---

## 3. Scroll-triggered 渐入——克制法则(这是塑料重灾区)

### 铁律:**最多 2-3 处 reveal,不是每个 section**

整页从头到尾 fade-in-up = 最浓的 web 塑料味。它把"读内容"变成"等动画"。规则:

| 内容类型 | 该不该 reveal |
|---------|--------------|
| **首屏 hero** | 一次性入场编排(见 02,首屏只此一次) |
| **关键 section 标题(2-3 个)** | 可以轻 reveal(translateY 8px) |
| **普通 section 内容** | **不 reveal**,滚到就直接在 |
| **数据可视化 / 图表** | 可以 reveal(出现即进入视野,有"登场"感) |
| **正文段落** | **绝不 reveal**(打断阅读) |
| **每个 feature 卡** | **绝不**(这是 AI 默认,最塑料) |

> **判断标准:这个 reveal 是"给内容登场"还是"为了动而动"?** 如果去掉这个动画,内容立刻就在,用户完全没损失——那就别加。

### IntersectionObserver 实现要点(可直接抄)

```js
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!reduce) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target); // ✅ 触发一次后停止观察(性能 + 防重复触发)
      }
    });
  }, {
    rootMargin: '0px 0px -15% 0px', // ✅ 元素顶部进入视口底部上方 15% 时触发(不是完全可见才触发——太晚;不是刚露 1px——太早)
    threshold: 0                     // 元素任意部分进入 rootMargin 区域即触发
  });

  document.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));
} else {
  // ✅ reduced-motion:不注册 observer,内容直接可见
  document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('is-visible'));
}
```

```css
[data-reveal] { opacity: 0; transform: translateY(8px);
  transition: opacity 500ms cubic-bezier(0.16,1,0.3,1), transform 500ms cubic-bezier(0.16,1,0.3,1); }
[data-reveal].is-visible { opacity: 1; transform: none; }
```

**要点**:
1. **`rootMargin: '0px 0px -15% 0px'`**:把触发线下移到视口底部上方 15%。元素一进入这个"提前区"就触发,用户看到时动画已过半,读作"自然出现"而非"我在等它"。
2. **`unobserve` 触发后移除**:一次性,不重复触发。滚回去不要再浮一次。
3. **CSS 处理过渡,JS 只加 class**:不要在 JS 里算动画帧——掉帧。
4. **reduced-motion 跳过 observer,直接可见**。
5. **位移 ≤8px**,时长 ≤500ms。大位移 = 拖沓。

### 反例对照
| 场景 | 塑料(AI 默认) | 顶级 |
|------|--------------|------|
| 整页每个 section | 全部 fade-in-up | 仅 2-3 处关键节点 reveal |
| feature 卡 | 每张卡依次浮入(6 张排队) | 直接在,或整组一起轻 reveal |
| 正文段落 | 每段 scroll 渐入 | 永不 reveal |
| 触发时机 | 完全可见才触发(用户已等) | 进入底部 15% 提前区即触发 |

---

## 4. Pin / Sticky —— 默认用 CSS sticky,JS pin 是重工程

### CSS `position: sticky`(默认,几乎免费)
纯 CSS,GPU 友好,无 JS。用于"某元素在滚动一段后吸顶/吸边"。

| 场景 | 用法 |
|------|------|
| 编辑长文的章节目录(TOC) | `position: sticky; top: 80px;` 跟随滚动 |
| 商品页 buy box | sticky 在视口,图集滚而购买信息常驻 |
| 长文阅读进度章节高亮 | sticky TOC + IO 高亮当前节 |
| 导航栏吸顶 | `position: sticky; top: 0;` |

```css
.toc { position: sticky; top: 88px; align-self: start; max-height: calc(100vh - 100px); overflow: auto; }
```

### JS scroll-pinning(GSAP ScrollTrigger 等,重工程,慎用)
"面板 A 钉死在视口,面板 B 从下方滚上来覆盖它"——Apple 产品页的招牌 scrollytelling。

**纪律**:
1. **这是重工程,不是随手加**。需要精准的 scrub 同步、性能预算、reduced-motion 降级。做不好就 jank。
2. **整页最多 1-2 个 pin 段落**。Apple 一整页可能就 2-3 个 pin 时刻,不是 10 个。
3. **必须配 reduced-motion 降级**(pin 段在 reduced-motion 下变成普通堆叠,不钉)。
4. **优先用 2024+ CSS scroll-driven animations** 替代 JS pin(见下节),它跑在合成线程,不掉帧。

### 反例对照
| 场景 | 塑料 | 顶级 |
|------|------|------|
| TOC 跟随 | JS 监听 scroll 改 top(掉帧) | `position: sticky`(纯 CSS) |
| 沉浸式叙事 | 每段都 JS pin(整页 jank) | 1-2 段 pin,其余普通滚动 |
| buy box 常驻 | JS 算位置固定 | sticky |

---

## 5. Parallax —— 防土味纪律(默认别用)

### 为什么默认别用
Parallax(视差,不同层以不同速度滚动)是 **2015 年的潮流,大部分时候伤害性能和无障碍**。stage2 已禁。AI 爱给所有图片加视差——廉价、晕、掉帧。

### 如果非要用,五条硬边界(全部满足才允许)
1. **只动 `transform`/`opacity`**,绝不监听 scroll 改 `top`/`background-position`(触发 layout/paint,掉帧)。
2. **位移范围 ≤8% 视口高**(translateY ≤60-80px)。大位移 = 晕。
3. **绝不在文字/正文上加视差**——滚动时文字晃动不可读。只在背景图/装饰层。
4. **尊重 reduced-motion**——该模式下视差归零,正常滚动。
5. **优先用 CSS scroll-driven animations,不用 JS scroll 监听**。

### 2024+ CSS scroll-driven animations(现代正解,无 JS,不掉帧)
```css
/* 元素随滚动产生轻微视差 —— 跑在合成线程,不阻塞主线程 */
@supports (animation-timeline: scroll()) {
  .bg-layer {
    animation: parallax linear both;
    animation-timeline: scroll(root); /* 绑定页面滚动 */
  }
  @keyframes parallax {
    from { transform: translateY(0); }
    to   { transform: translateY(-60px); } /* 范围 ≤60px */
  }
}
@supports not (animation-timeline: scroll()) {
  .bg-layer { transform: none; } /* 不支持就静止 */
}
```

### 灾难场景(绝对禁止)
| 场景 | 为什么是灾难 |
|------|------------|
| 文字层视差 | 滚动时文字抖动,无法阅读 |
| JS scroll 监听改 background-position | 每帧重绘,jank |
| mouse-move 视差(每层随鼠标偏移) | 晕动症,廉价 |
| 多层视差叠在一起 | 视觉混乱,聚焦不了内容 |
| 移动端视差 | 移动设备性能 + 触屏滚动特性,必掉帧 |

### 反例对照
| 场景 | 塑料 | 顶级 |
|------|------|------|
| hero 背景图 | JS 改 `background-position-y`(掉帧) | CSS `animation-timeline: scroll()` translateY ≤60px |
| 全站每张图 | 都加视差 | 仅 hero 一处轻视差,其余静止 |
| 装饰 blob | 随鼠标飘 | 不动 |

---

## 6. 滚动进度条 —— 廉价但有效的"我在哪"信号

顶部一根 2-3px 细条,显示页面滚动百分比。给长页一个"还剩多少"的空间感。极克制,几乎免费。

```css
/* ✅ 现代:纯 CSS scroll-driven,无 JS */
@supports (animation-timeline: scroll()) {
  .scroll-progress {
    position: fixed; top: 0; left: 0; height: 2px; width: 100%;
    transform-origin: 0 50%; background: var(--accent);
    animation: progress-grow linear;
    animation-timeline: scroll(root);
  }
  @keyframes progress-grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
}
```

**纪律**:仅一根、仅顶部、仅 2-3px、仅 accent 色。不要做成侧边大圆环 + 百分比数字浮窗——那是过度设计。

---

## 7. Apple 式 scrollytelling(沉浸式叙事)——何时值得,何时不值得

Apple 产品页("MacBook 介绍")是 scrollytelling 的天花板:**滚动驱动视频/3D 模型旋转、文字与画面同步切换、pin 段落叙事**。

### 何时值得
- **单一重磅产品发布**(Apple、Tesla、高端硬件)——值得为这一个时刻做重工程。
- **品牌叙事核心段**(家族传承、设计哲学)——一页里 1-2 个 pin 时刻。

### 何时不值得(用普通滚动)
- **SaaS 落地页**——用户要快速了解功能,不要被叙事拖慢。
- **内容型/工具型页**——Docs、Pricing、Product 详情页,绝不 scrollytelling。
- **预算/工期有限**——scrollytelling 是 5-10 倍工作量,普通滚动 90% 场景够用。

### 实现红线(如果做)
1. **每段 pin ≤1 屏滚动距离**——pin 太长用户以为卡住。
2. **scrub 同步必须顺滑**——用 GSAP ScrollTrigger 的 scrub,或 CSS scroll-driven。
3. **必须有 fallback**:reduced-motion / 低性能设备 → 降级为普通堆叠 + 静态图。
4. **加载性能**:pin 段的视频/3D 必须 lazy,首屏不阻塞 LCP(见 `05-performance-as-design.md`)。

---

## 反塑料证据(滚动叙事的"人做的"信号)

- [ ] 整页 reveal 不超过 2-3 处(不是每 section)
- [ ] 正文段落永不 reveal
- [ ] reveal 用 `rootMargin: 0 0 -15% 0` 提前触发,不是完全可见才触发
- [ ] IO 触发后 `unobserve`(一次性)
- [ ] 默认 `position: sticky`,JS pin 仅 1-2 处沉浸段
- [ ] parallax:仅 hero 一处、仅背景层、≤60px、CSS scroll-driven
- [ ] 文字/正文无任何视差
- [ ] 滚动进度条仅一根 2-3px
- [ ] section 不等高,密-疏交替
- [ ] reduced-motion 下:不 reveal、不 pin、不 parallax,内容直接堆叠可见

## 常见塌方表

| 塌成什么 | 病因 | 修复 |
|---------|------|------|
| 整页像幻灯片 | 每 section fade-in-up | 砍到 2-3 处 reveal |
| 滚动掉帧 | JS scroll 监听改 layout/paint 属性 | CSS sticky + scroll-driven animation |
| 用户晕 | 多层 parallax / 文字视差 | 砍 parallax,仅 hero 背景一处 |
| 中段内容没人看 | 注意力谷底无再激活尖峰 | 中段加强标题 + 视觉变化 + 不等高 |
| pin 段以为卡住 | pin 距离 >1 屏 | 每段 pin ≤1 屏 |
| reduced-motion 还在动 | 缺降级 | IO 不注册 / pin 降级为堆叠 / parallax 归零 |
