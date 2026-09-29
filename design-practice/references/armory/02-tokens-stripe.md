# 02 — Stripe Design Tokens 母版

来源(交叉验证):
- docs.stripe.com/stripe-apps/style
- duply.ai/stripe/design-md
- explainx.ai Voltagent Stripe DESIGN.md
- shadcn.io/design/stripe
- asadravian/awesome-design-md-google-stitch/stripe/DESIGN.md

## 颜色 — Primitive

| Token | Hex | 用途 |
|------|-----|------|
| `color.canvas` | `#FFFFFF` | 页面背景 |
| `color.surface` | `#FFFFFF` | 卡片背景 |
| `color.ink` | `#0D253D` | 主文本(深海军,绝不用纯黑) |
| `color.body` | `#425466` | 次文本 |
| `color.muted` | `#8898AA` | 弱文本 |
| `color.hairline` | `#E5EDF5` | 标准 1px 分隔 |
| `color.hairline-strong` | `#061B31` | 深色分隔 |
| `color.brand.primary` | `#533AFD` | 单电压靛蓝,唯一填充色 |
| `color.brand.hover` | `#4434D4` | primary hover |
| `color.surface-dark` | `#1C1E54` | 深色装饰背景 |
| `color.danger` | `#DE3618` | 错误 |
| `color.success` | `#009688` | 成功 |

### 营销氛围色(gradient mesh)

cream `#FFF6E5`, sherbet `#FF9D5C`, orange `#FF6B3D`, lavender `#A5B4FC`, indigo `#533AFD`, ruby `#E64980` — 用于 hero 渐变背景。

## 间距 — 8px 基,小端密集

| Token | Value | 用途 |
|------|-------|------|
| `space.1` | `1px` | 发丝边 |
| `space.2` | `2px` | 微调 |
| `space.4` | `4px` | chip 内 |
| `space.6` | `6px` | 输入小内距 |
| `space.8` | `8px` | 按钮/输入基础内距 |
| `space.10` | `10px` | — |
| `space.11` | `11px` | — |
| `space.12` | `12px` | 输入横向 |
| `space.14` | `14px` | — |
| `space.16` | `16px` | 按钮/段落间隙 |
| `space.18` | `18px` | — |
| `space.20` | `20px` | — |
| `space.24` | `24px` | 容器中 |
| `space.32` | `32px` | 卡片大 |
| `space.40` | `40px` | section 间 |
| `space.48` | `48px` | — |
| `space.56` | `56px` | section-sm |
| `space.64` | `64px` | section |
| `space.96` | `96px` | section-lg |

> Stripe Apps(Dashboard 内)用语义 token:`0 / xxsmall 2 / xsmall 4 / small 8 / medium 16 / large 24 / xlarge 32 / xxlarge 48`。

## Radius — 7 档

| Token | Value | 用途 |
|------|-------|------|
| `radius.xs` | `2px` | checkbox 角 |
| `radius.sm` | `4px` | 产品内小按钮、chip |
| `radius.md` | `6px` | 输入/select/小卡 |
| `radius.lg` | `16px` | 卡片/截图框 |
| `radius.xl` | `32px` | 大装饰磁贴 |
| `radius.pill` | `9999px` | 所有 CTA 按钮 + badge |

## 字体

| Token | Family | 替代(开源) | 用途 |
|------|--------|----------|------|
| `font.display` | Sohne (variable) | Inter `font-weight: 300` + `font-feature-settings: "ss01"` | 标题/正文 |
| `font.mono` | Source Code Pro / Camphor Mono | — | 代码块 |

## Type scale(营销)

| Token | Size / Weight / Line / Tracking | 用途 |
|------|------|------|
| `text.hero` | 56 / 300 / 1.15 / -1.4em→-0.96 | hero |
| `text.title` | 48 / 300 / 1.2 / -0.8 | section 标题 |
| `text.subtitle` | 28 / 300 / 1.25 / -0.4 | 副标题 |
| `text.subhead` | 22 / 300 / 1.3 / -0.2 | 小标题 |
| `text.body-lg` | 18 / 300 / 1.5 / -0.1 | lead |
| `text.body` | 16 / 300 / 1.55 / 0 | 正文 |
| `text.body-sm` | 14 / 400 / 1.5 / 0 | 卡片正文 |
| `text.button` | 16 / 400 / 1.0 / 0 + `ss01` | 按钮文字 |
| `text.label` | 14 / 500 / 1.4 / 0 | nav 链接 |
| `text.code` | 14 / 400 / 1.6 / 0 + tnum | 代码 |

> 所有数字单元格开启 `font-variant-numeric: tabular-nums`——这是 Stripe 的金融 DNA 信号。

## 组件层 token

```css
button.primary {
  background: #533AFD;
  color: #FFFFFF;
  border-radius: 9999px;       /* pill 是 Stripe 标志 */
  padding: 8px 16px;
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 0;
  font-feature-settings: "ss01";
  box-shadow: none;
  transition: background 150ms ease;
}
button.primary:hover { background: #4434D4; }
button.primary:focus-visible {
  outline: 2px solid #533AFD;
  outline-offset: 2px;
}
card {
  background: #FFFFFF;
  border: 1px solid #E5EDF5;
  border-radius: 16px;
  padding: 32px;
  box-shadow:
    0 30px 45px -30px rgba(50, 50, 93, 0.25),
    0 18px 36px -18px rgba(0, 0, 0, 0.1);
  transition: box-shadow 200ms ease;
}
card.feature {
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 15px 35px 0 rgba(23, 23, 23, 0.08); /* ambient */
}
input {
  background: #FFFFFF;
  border: 1px solid #E5EDF5;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 16px;
  color: #0D253D;
}
input:focus {
  border-color: #533AFD;
  box-shadow: 0 0 0 3px rgba(83, 58, 253, 0.25);
  outline: none;
}
```

## 阴影

```css
shadow.standard: rgba(50,50,93,0.25) 0px 30px 45px -30px,
                 rgba(0,0,0,0.1) 0px 18px 36px -18px;
shadow.ambient:  rgba(23,23,23,0.08) 0px 15px 35px 0px;
shadow.tiny:     rgba(5,9,26,0.06) 0px 30px 40px -10px,
                 rgba(0,0,0,0.05) 0px 18px 36px -18px;
```

## 动效

| Token | Value | 用途 |
|------|-------|------|
| `motion.fast` | `150ms` | hover |
| `motion.base` | `200ms` | 卡片/阴影 |
| `motion.slow` | `300ms` | section 进场 |
| `motion.easing` | `ease` | 默认 |

## 还原时的硬规矩

1. **每屏一个填充按钮**(`#533AFD`)——和一个 secondary(outline/ghost)并列。Stripe 从不在一个 hero band 里放两个填充。
2. **所有 CTA 是 pill**——产品内可以 r4-6,但营销面 CTA 全 pill。
3. **深海军 `#0D253D` 不用纯黑**——所有正文都用它。
4. **数字必 `tnum`**——价格、金额、ID、时间戳。
5. **gradient mesh 只在 hero**——下面所有 section 必须白底干净。
6. **section 间留 64-96px**——别把节奏挤死。
