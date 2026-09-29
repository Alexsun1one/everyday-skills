# 03 — Notion Design Tokens 母版

来源(交叉验证):
- designmd.co/d/notion
- styleextract.com/vault/notion
- refero.styles
- duply.ai/notion/design-md

## 颜色 — Primitive

| Token | Hex | 用途 |
|------|-----|------|
| `color.canvas` | `#FFFFFF` | 页面背景 |
| `color.surface` | `#FFFFFF` | 卡片 |
| `color.surface-warm` | `#F6F5F4` | 区块/侧边栏 |
| `color.ink` | `#000000` | 主文本(纯黑,AAA) |
| `color.body` | `#1D1D1F` | 正文变体 |
| `color.secondary` | `#615D59` | 次文本(AA on white) |
| `color.muted` | `#9B9A97` | 弱文本 |
| `color.hairline` | `#E5E5E7` | 1px 分隔 |
| `color.hairline-strong` | `#D3D3D2` | 强分隔 |
| `color.accent-blue` | `#097FE8` | 单一 CTA(签名蓝) |
| `color.accent-bg-blue` | `#E8F2FF` | 蓝 hover/选中底 |
| `color.accent-red` | `#E03E3E` | 删除/危险 |
| `color.accent-green` | `#0F7B6C` | 成功 |
| `color.accent-amber` | `#D9730D` | 警告 |

> Dark mode: `canvas: #1C1C1E`, `surface: #2C2C2E`, `ink: #F7F6F3`, `hairline: #3A3A3C`。

## 间距 — 4px 基,9 档

| Token | Value | 用途 |
|------|-------|------|
| `space.1` | `4px` | icon-文字 |
| `space.2` | `8px` | 小内距(button) |
| `space.3` | `12px` | 输入 |
| `space.4` | `16px` | 元素间隙 |
| `space.5` | `20px` | — |
| `space.6` | `24px` | 卡片内 |
| `space.8` | `32px` | 卡片间 |
| `space.10` | `40px` | — |
| `space.12` | `48px` | section |
| `space.16` | `64px` | 大 section |
| `space.20` | `80px` | 营销 section |

> 实测 Notion 主导节奏:**8px 出现 131 次,24px 出现 63 次,16px 出现 39 次**。

## Radius

| Token | Value | 用途 |
|------|-------|------|
| `radius.xs` | `4px` | button(实测)/ chip |
| `radius.sm` | `5px` | button 备用(refero 数据)/ input |
| `radius.md` | `8px` | 小 UI 元素 |
| `radius.lg` | `12px` | 卡片(refero)/ agent tile |
| `radius.xl` | `16px` | feature card |
| `radius.pill` | `9999px` | 头像/状态 dot(不是按钮) |

> Notion 卡片实测 **r12 / p24**;按钮实测 **r4-5 / 5×10 内距**(非常紧凑)。

## 字体

| Token | Family | Weight | 用途 |
|------|--------|--------|------|
| `font.ui` | Inter / NotionInter(自定义) | 400 / 600 / 700 | 全 UI |
| `font.mono` | ui-monospace / SF Mono | 400 | 内联代码 |

## Type scale

| Token | Size / Weight / Line | 用途 |
|------|------|------|
| `text.hero` | 54 / 700 / 1.1 / -0.02em | hero |
| `text.h1` | 40 / 700 / 1.2 / -0.02em | 页面标题 |
| `text.h2` | 30 / 700 / 1.25 / -0.02em | section |
| `text.h3` | 24 / 600 / 1.3 | 子标题 |
| `text.body-l` | 18 / 400 / 1.6 | lead |
| `text.body` | 16 / 400 / 1.6 | 正文 |
| `text.body-sm` | 14 / 400 / 1.5 | 卡片正文 |
| `text.label` | 14 / 600 / 1.4 | nav/button |
| `text.caption` | 12 / 400 / 1.4 | 元数据 |
| `text.button` | 14 / 600 / 1.2 | 按钮文字 |

## 组件层 token

```css
button.primary {
  background: #000000;
  color: #FFFFFF;
  border-radius: 6px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.2;
  transition: opacity 150ms ease;
}
button.primary:hover { opacity: 0.88; }
button.primary:focus-visible {
  outline: 2px solid #097FE8;
  outline-offset: 2px;
}
button.secondary {
  background: transparent;
  border: 1.5px solid #000000;
  color: #000000;
  border-radius: 6px;
  padding: 7px 15px;
}
card {
  background: #FFFFFF;
  border: 1px solid #E5E5E7;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
card.feature {
  border-radius: 16px;
  padding: 32px;
}
input {
  background: #FFFFFF;
  border: 1px solid #E5E5E7;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 14px;
  color: #000000;
  height: 32px;
}
input:focus {
  border-color: #097FE8;
  box-shadow: 0 0 0 2px rgba(9, 127, 232, 0.3);
  outline: none;
}
nav {
  background: #FFFFFF;
  height: 60px;
  padding: 0 24px;
  border-bottom: 1px solid #E5E5E7;
}
```

## 阴影

```css
shadow.sm:  0 1px 3px rgba(0, 0, 0, 0.08);
shadow.md:  0 4px 12px rgba(0, 0, 0, 0.10);
shadow.card: rgba(25, 25, 25, 0.027) 0px 15px 35px 0px;  /* 多层软 */
shadow.lg:  0 12px 32px rgba(0, 0, 0, 0.12);
```

## 动效

| Token | Value | 用途 |
|------|-------|------|
| `motion.fast` | `150ms` | opacity / color hover |
| `motion.base` | `200ms` | 卡片浮起 |
| `motion.slow` | `300ms` | 模态进出 |
| `motion.keyframe` | `fadeIn`, `slideUp` | CSS keyframe |
| `motion.easing` | `ease` | 默认 |

## 还原时的硬规矩

1. **primary 按钮是黑色 `#000000`,不是蓝**——蓝色 `#097FE8` 只用于单一最关键 CTA 或 hover/focus。Notion 的克制来自"几乎不用色"。
2. **button padding 紧凑**:实测 `5×10` 或 `8×16`,别臃肿。
3. **卡片 r16 / p24**——产品 mockup 卡可以 r12。
4. **背景多为 `#FFFFFF`,局部加 `#F6F5F4` 暖底**区分区域。
5. **multi-layer soft shadow** 是 Notion 标志:`rgba(25,25,25,0.027)` 多层堆。
6. **页面 max-width: 1200px**,section gap 80px。
