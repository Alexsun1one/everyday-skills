# web-craft 扩展包索引 —— 让 design-practice 会做"真正的网页"

> design-practice 的默认肌肉记忆是 **B 端 SaaS 后台**(dashboard / 表格 / 表单 / list-detail / settings)。这些是"工具内部页"——用户已经登录,有任务场,有状态矩阵。本扩展补它的最大偏科:**工具外部的网页**——落地页、品牌官网、编辑型长页、作品集、文档站、沉浸式滚动叙事。这些页的"活"不是"完成任务",而是**捕获注意力、建立信任、引导转化**。两套页用同一套组件字典,但**动线、节奏、构图、动效纪律完全不同**。

## 这个扩展包要杀的"塑料"

AI 生成的"网页"有一个高度一致的指纹:

1. **首屏 = 居中大标题 + 渐变文字 + 一句副标 + 居中双 CTA + 下面一张产品截图漂在彩色 blob 渐变上。** 每一个 AI 落地页都长这样。这是 2023-2026 最浓的塑料味。
2. **Feature 区 = 3 列等宽 icon 卡片网格。** 六个 lucide 图标塞进六个圆角卡片,每张卡一个标题一句话。没有密度差,没有信息层级,没有构图意图。(根治见 `06-anti-card-tiling.md`。)
3. **所有元素 scroll-triggered fade-in-up,全页从头到尾渐入。** 每滚一格浮一格,像幻灯片。读不下去。(根治见 `03-scroll-storytelling.md`。)
4. **响应式 = 只保证 320px 不溢出,其他全等比缩小。** 大屏设计直接缩到手机,文字糊、栅格塌、构图死。(根治见 `04-responsive-art-direction.md`。)
5. **动画 = 一切都 `transition: all 0.3s ease`。** 动 margin / width / box-shadow,首屏掉帧。ease 用错方向。不可打断。(根治见 `02-motion-system.md`。)

这五条是 web-craft 的全部敌人。每个文件都对准其中一条或几条。

## 7 个文件各管什么

| 文件 | 管什么 | 什么时候读它 | 杀哪条塑料 |
|------|--------|------------|-----------|
| **00-index.md** | 本索引 + 路由 | 任何"网页"任务先读这页选路由 | — |
| **01-page-archetypes.md** | 网页原型库(landing / brand / editorial / portfolio / docs / pricing / product) | 定了"做什么页"但还没想清楚这页的"活"和"动线" | 1, 2(选错原型=全盘错) |
| **02-motion-system.md** | web 动效系统(token / GPU 合成 / 可打断 / reduced-motion) | 写任何 CSS transition / animation / scroll 动效之前 | 5 |
| **03-scroll-storytelling.md** | 滚动叙事 / 长页节奏(pin / parallax / IntersectionObserver 防土味纪律) | 做滚动叙事页 / 编辑型长页 / 品牌长页 | 3 |
| **04-responsive-art-direction.md** | 每个断点的艺术指导(fluid type / container queries / 换序折叠) | 出了桌面稿,要做移动 / 平板 / 超宽屏 | 4 |
| **05-performance-as-design.md** | Core Web Vitals 当设计约束(LCP / CLS / INP / 字体 / 图片) | 交付前定性能预算;或字体图片策略选型 | 5(性能塑料:掉帧、位移、慢首屏) |
| **06-anti-card-tiling.md** ⭐ | 反卡片平铺 → 高级布局系统(编辑型栅格 / bento / bleed / 杂志式 / 高密度) | feature 区、能力展示区、任何"想放一堆东西"的地方——AI 默认给你卡片网格,这页给你替代 | **2(核心塑料)** |

## 路由:用户要做什么页 → 先读哪个

```
"做个落地页 / 营销首页"           → 01 (landing 原型) → 06 (feature 区别平铺) → 03 (首屏节奏)
"做个品牌官网"                    → 01 (brand 原型)  → 03 (滚动叙事) → 04 (大屏艺术指导)
"做个编辑型长文 / 博客 / 报道"    → 01 (editorial 原型) → 04 (阅读流) → 05 (字体性能)
"做个作品集 / personal site"      → 01 (portfolio 原型) → 06 (别平铺作品) → 03 (轻量滚动)
"做个文档站"                      → 01 (docs 原型)   → 04 (多栏→单栏) → 05 (搜索/字体)
"做个定价页"                      → 01 (pricing 原型) → 06 (档位对比表别做卡片)
"做个电商商品详情页"              → 01 (product 原型) → 05 (图片/CLS) → 04 (移动图集)
"做沉浸式滚动叙事(类 Apple 产品页)" → 03 优先 → 02 (动效纪律) → 05 (pin 的性能代价)
"动画怎么做才不塑料"              → 02
"手机上怎么排版"                  → 04
"页面太慢 / 字体闪 / 图把版面顶下去" → 05
"feature 区/能力区怎么不平铺卡片"  → 06
```

## 和已有层级怎么配合(不重复造轮子)

design-practice 已有的层级负责"工具内部页"的骨架。web-craft **不改写**它们,**复用**它们的产出,只在"网页特有"的地方加层:

| 已有层级 | 已有产出 | web-craft 怎么用 |
|---------|---------|----------------|
| `visual-language/style-*.md` | 配色 / 字体 / 圆角 / elevation 的 Prompt Fragment | **网页也照搬同一份 style DNA**。网页不是新风格,是同一套 DNA 用在更大的画布上。style-linear 的 #08090A 画布、weight 510、单 accent 制——在落地页上一样成立。 |
| `references/stage2-motion-discipline.md` | SaaS 内部动效语法(duration / easing / direction / reduced-motion 五问) | **web-craft 的 `02-motion-system.md` 是它的"大舞台版"**——内部页动效是 100-300ms 的状态过渡;网页动效还要管 scroll-choreography、entrance 编排、GPU 合成层。两者共用 token,02 补 scroll 和编排那部分。 |
| `references/qa-responsive.md` | 多设备 QA 清单(mobile/tablelet/desktop 不溢出) | **web-craft 的 `04` 是它的"设计前置版"**——QA 是验收"没坏",04 是创作"每个断点是另一种构图"。先 04 再 qa-responsive。 |
| `patterns/` | list-detail / complex-flow / container-decision 等 B 端骨架 | 网页里出现"登录""定价对比""文档目录"等**仍走 patterns**。web-craft 不发明这些,只在网页语境里调它们。 |
| `components/` | 按钮 8 态 / input / drawer 等 | **网页的按钮/输入/弹层照样从 components 取像素值**。网页不是另起一套组件,是同一套组件在更大画布、更稀疏密度下排版。 |

**一句话**:已有层级管"组件和骨架的精确度",web-craft 管"网页的**动线、节奏、构图、性能**"——这是已有层级没覆盖、而 AI 网页塑料味最浓的地方。

## 用 web-craft 的工作流(嵌在既有 pipeline 里)

1. **Zero gate**:Intent Brief 照常。但 `GOAL` 字段多半是 **转化 / 激活 / 留存 / 信息消费 / 探索**,而不是 B 端的"生产力"。`风格 DNA` 照 `intent-reading.md` 路由。
2. **选原型**:读 `01-page-archetypes.md`,定"这是哪种网页原型",抄它的动线 + section 清单 + 反塑料铁律。
3. **构图决策**:feature 区 / 能力区 / 作品区 → 读 `06-anti-card-tiling.md`,**先定"不平铺"用什么布局系统**,再画线稿。这是 AI 网页与顶级网页分叉的第一道关。
4. **动效预算**:读 `02-motion-system.md`,定 token(ease-out、≤300ms、只动 transform+opacity),写进 CSS。
5. **长页/叙事**:若原型含滚动叙事,读 `03-scroll-storytelling.md`,定 section 节奏 + 哪几处 pin / 哪几处渐入(克制)。
6. **响应式艺术指导**:读 `04`,每个断点定一个"重排意图",写 clamp() 和 grid。
7. **性能预算**:读 `05`,定 LCP/CLS/INP 目标,定字体和图片策略。
8. **Stage 2 还原 + QA**:照常走 components 像素还原 + qa-responsive / qa-a11y / qa-three-gates。

> web-craft 不替代任何既有 gate。它是"在 Intent Brief 之后、Stage 1 线稿之前"插入的一组**网页专属判断卡**。
