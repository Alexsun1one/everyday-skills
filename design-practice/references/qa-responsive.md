# 响应式断点验收表 — Responsive Acceptance

> AI 生成 UI 第三常见失败模式:**桌面好看,手机塌**——导航溢出、表格横向滚动、按钮挤成小字、modal 大于屏幕。这是塑料信号,因为真人做的产品会在每个断点都验收。
>
> 这一页冻结:三大端(桌面/平板/手机)的断点、每端的常见问题、修法。

## 三大端断点

参考 Tailwind v4 默认断点(2026 标准):

| 端 | 断点 | min-width | 典型设备 |
|---|---|---|---|
| **Mobile** | default | 0px | iPhone / Android 手机 |
| **SM** | `sm:` | 640px | 大手机横屏 / 小平板竖 |
| **Tablet** | `md:` | 768px | iPad 竖 |
| **LG** | `lg:` | 1024px | iPad 横 / 小笔记本 |
| **Desktop** | `xl:` | 1280px | 标准笔记本 / 桌面 |
| **2XL** | `2xl:` | 1536px | 大桌面 |

**移动优先 CSS 写法:** 默认 mobile,逐级 `min-width` 增加复杂度。

## 每端的必验清单

### Mobile(0-639px)— 默认

| 问题 | 修法 |
|---|---|
| **导航溢出** | 顶栏导航收进 hamburger menu(☰) |
| **多列布局塌** | grid-cols-1,所有列垂直堆叠 |
| **表格横向滚动** | 卡片化(每行变一张卡片)或 sticky 第一列 + 横向 scroll |
| **modal 大于屏幕** | modal 变全屏 sheet(底部滑入或全屏覆盖) |
| **drawer 宽度占满** | drawer 变全屏 sheet(从右或下滑入) |
| **按钮挤成小字** | 按钮 full-width,文字不缩字号(最小 14px) |
| **input 缩小** | input min-height 44px(苹果 HIG 触摸目标) |
| **文字太小** | body 最小 16px(iOS Safari 会强制 < 16px 的 input 放大) |
| **图片不缩** | img max-width: 100%; height: auto |
| **hover 信息丢失** | 移动端没 hover——所有 hover 透露的信息必须有替代(长按、tap 切换) |
| **触摸目标太小** | 所有可点击元素 min 44×44px(苹果 HIG)/ 48×48px(Material) |
| **手势冲突** | 横向 carousel 与浏览器返回手势冲突——加 touch-action |
| **键盘弹出遮挡** | 输入框 focus 时键盘弹出会遮挡——滚动到视口 |
| **安全区域** | iPhone 刘海/底部 bar——`env(safe-area-inset-*)` padding |

### Tablet(768-1023px)

| 问题 | 修法 |
|---|---|
| **导航放不下** | 部分主要项保留 + hamburger 收次要项 |
| **两列布局** | grid-cols-2(部分卡片两列) |
| **表格保留** | 表格还能用,但 row 高度可调紧凑 |
| **modal 大小** | modal 居中,max-width: 80vw |
| **drawer** | drawer 仍从右侧,宽度 min(400px, 90vw) |
| **侧栏** | 侧栏可折叠(图标-only 模式) |

### Desktop(≥1024px)

| 问题 | 修法 |
|---|---|
| **导航全展开** | 顶栏或侧栏所有项可见 |
| **三列布局** | grid-cols-3、grid-cols-4、grid-cols-6 |
| **表格完整** | 完整列 + sticky header + sorting + pagination |
| **modal 居中** | max-width 480-640px,垂直居中 |
| **drawer 右侧** | 宽度 400-480px,从右侧滑入 |
| **侧栏完整** | 完整 sidebar 240-280px |

## 关键组件的响应式行为

### 导航 Navigation

```text
Mobile (<768px):
  ☰ Hamburger → 全屏 drawer / sheet
  Logo + 1-2 个核心 CTA

Tablet (768-1023px):
  顶部水平导航(主要项)+ 次要项收 hamburger

Desktop (≥1024px):
  左侧 sidebar 240px(完整)+ 顶栏 56px
  或 顶栏 + 右侧 command palette (⌘K)
```

### 表格 Table

```text
Mobile:
  - 卡片化(每行变一张卡片,字段+值垂直排列)
  - 或 sticky 第一列 + 横向 scroll
  - 关键操作 icon-only 显示

Tablet:
  - 完整表格但 row 高度紧凑(32px)
  - 部分次要列隐藏

Desktop:
  - 完整表格,row 高度标准(40px)或宽松(48px)
  - 全列显示 + sorting + filtering + pagination
```

### 模态 Modal

```text
Mobile:
  - 全屏覆盖(100vw × 100vh)
  - 或底部 sheet(从下滑入,高度 80vh)
  - 关闭:tap 遮罩 / 顶部 ✕ / 顶部下拉手势

Tablet/Desktop:
  - 居中,max-width 480-640px
  - 高度自适应内容,max-height 85vh
  - 关闭:点遮罩 / ESC / 顶部 ✕
```

### 抽屉 Drawer

```text
Mobile:
  - 全屏 sheet(100vw,从右或下滑入)
  - 关闭:tap 遮罩 / ESC / 边缘 swipe

Tablet/Desktop:
  - 右侧,宽度 400-480px(标准)/ 640px(宽表单)
  - 关闭:tap 遮罩 / ESC / 顶部 ✕
```

### 表单 Form

```text
Mobile:
  - 单列(绝不多列)
  - input min-height 44-48px
  - 字号最小 16px(iOS 防 zoom)
  - 提交按钮 full-width

Tablet/Desktop:
  - 可两列(标签+输入 并排)
  - 标准 input 高度 36-40px
  - 提交按钮 auto width,右下角
```

### 卡片网格 Card Grid

```text
Mobile:
  - grid-cols-1(单列)
  - 卡片 full-width

Tablet (md):
  - grid-cols-2

Desktop (lg):
  - grid-cols-3 或 grid-cols-4

Desktop (xl):
  - grid-cols-4 或 grid-cols-6(bento grid)
```

## 验收清单(每端都要过)

```text
页面 URL:_____________

□ Mobile(375px iPhone / 360px Android)
  □ 导航收 hamburger
  □ 单列布局
  □ 表格卡片化或横向 scroll
  □ modal/drawer 全屏 sheet
  □ 按钮 full-width
  □ input min-height 44px
  □ 字号 ≥ 16px
  □ 触摸目标 ≥ 44×44px
  □ hover 信息有替代
  □ safe-area inset 处理

□ Tablet(768px iPad)
  □ 导航主要项 + hamburger
  □ 两列布局
  □ 表格紧凑可用
  □ modal 居中 80vw
  □ drawer 右侧 400px

□ Desktop(1280px+)
  □ 完整导航展开
  □ 三列或 bento grid
  □ 表格完整列
  □ modal 居中 480-640px
  □ drawer 右侧 400-480px
  □ 侧栏 240px

□ 跨端通用
  □ img max-width: 100%
  □ 文字不溢出容器(word-break/overflow-wrap)
  □ 触摸/鼠标都能操作
  □ 横屏竖屏切换不塌
  □ 缩放 50%-200% 不塌
```

## AI 验收员提示词

```text
你是一个严格的响应式验收员。审查下面这个页面在三大端的表现。

页面 URL:[提供]

对每个断点(375px / 768px / 1280px)分别评估:

Mobile(375px):
- 导航是否收 hamburger?
- 是否单列?
- 表格是否卡片化或横向 scroll?
- modal/drawer 是否全屏 sheet?
- 按钮是否 full-width?
- input 是否 min-height 44px?
- 字号是否 ≥ 16px?
- 触摸目标是否 ≥ 44×44px?

Tablet(768px):
- 导航是否主要项 + hamburger?
- 是否两列?
- modal 是否居中 80vw?

Desktop(1280px+):
- 导航是否完整展开?
- 是否三列或 bento?
- 表格是否完整列?
- modal 是否居中 480-640px?
- 侧栏是否 240px?

跨端:
- 图片是否 max-width: 100%?
- 文字是否溢出容器?
- 触摸和鼠标都能操作?
- 横竖屏切换不塌?

每端打勾或打叉,失败的具体指出修复点。
任何一端塌,这个页面就是响应式不合格。
```

## 工具推荐

| 工具 | 用途 |
|---|---|
| **Chrome DevTools Device Mode** | 模拟各种设备尺寸 |
| **Responsively App** | 多设备同时显示,scroll 同步 |
| **BrowserStack** | 真机测试 |
| **Xcode Simulator** | iOS 真机模拟 |
| **Android Studio Emulator** | Android 真机模拟 |

## 与 SKILL.md 的关系

SKILL.md 的 "Three-Gate QA" 的 Engineering Gate 必须包含这一页。任何页面生成完,都要在三端各过一遍。

## 权威信源

- Tailwind v4 默认断点(tailwindcss.com/docs/responsive-design)
- "Responsive Web Design" — Ethan Marcotte(原创文章)
- Apple Human Interface Guidelines — 触摸目标 44px
- Material Design — 触摸目标 48dp
