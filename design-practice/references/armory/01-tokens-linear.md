# 01 — Linear Design Tokens 母版

来源(交叉验证):
- designmd.cc/benchmarks/linear
- Reseed linear.app design system extracted
- VoltAgent awesome-design-md/linear.app/DESIGN.md
- Khalidabdi1/design-ai/linear/DESIGN.md
- soulcore-dev/soul-design-md/linear/DESIGN.md

## 颜色 — Primitive

| Token | Hex | 用途 |
|------|-----|------|
| `color.canvas` | `#0F1011` | 全局背景(深近黑) |
| `color.surface` | `#1A1B1E` | 卡片/面板背景 |
| `color.surface-elevated` | `#22252A` | 浮层/hover |
| `color.border` | `#2A2E33` | 1px 分隔 |
| `color.border-strong` | `#3A3F47` | 强分隔 |
| `color.text.primary` | `#F7F8F8` | 主文本(AAA on canvas) |
| `color.text.secondary` | `#D0D6E0` | 次文本 |
| `color.text.tertiary` | `#8A8F98` | 弱文本 |
| `color.text.disabled` | `#62666D` | 禁用 |
| `color.brand.primary` | `#5E6AD2` | 链接/focus,只用于交互 |
| `color.brand.hover` | `#6B7AD9` | brand hover |
| `color.danger` | `#EB5757` | 错误 |
| `color.warning` | `#F2C94C` | 警告 |
| `color.success` | `#5EB9D6` → 用 `#4CB782` | 成功(Linear 实际偏向青绿) |

> Linear 颜色adaptive,上表是 dark 默认。light 模式把 canvas→`#FFFFFF`、surface→`#F7F8F8`、text→`#1A1B1E`、border→`#E5E7EB`。

## 间距 — 4px 基,共 10 档

| Token | Value | 用途 |
|------|-------|------|
| `space.1` | `4px` | 图标-文字间隙 |
| `space.2` | `6px` | 微调 |
| `space.3` | `8px` | 小元素间隙 |
| `space.4` | `10px` | 输入内距 |
| `space.5` | `12px` | 按钮/输入 padding |
| `space.6` | `16px` | 元素标准间隙 |
| `space.7` | `20px` | 容器小内距 |
| `space.8` | `24px` | 卡片/容器内距 |
| `space.9` | `40px` | 段落间隙 |
| `space.10` | `48px` | 大段落间隙 |

## Radius — 只三档

| Token | Value | 用途 |
|------|-------|------|
| `radius.control` | `6px` | 所有控件(按钮/输入/chip) |
| `radius.container` | `12px` | 卡片/面板 |
| `radius.pill` | `9999px` | 头像/pill 按钮 |

> 别用 4px/8px,Linear 严格守 6/12/9999。

## 字体

| Token | Family | 用途 |
|------|--------|------|
| `font.ui` | `Inter Variable`(Linear Text 自定义 ≈ Inter) | 所有 UI |
| `font.mono` | `Berkeley Mono`(开源替代:`JetBrains Mono`) | 代码/ID/issue 编号 |

## Type scale

| Token | Size / Weight / Line / Tracking | 用途 |
|------|------|------|
| `text.hero` | 72 / 590 / 1.0 / -0.022em | hero |
| `text.page-title` | 64 / 590 / 1.06 / -0.022em | 页面标题 |
| `text.section` | 48 / 590 / 1.1 / -0.022em | section 标题 |
| `text.title-l` | 40 / 590 / 1.1 / -0.022em | 大标题 |
| `text.title-m` | 32 / 590 / 1.125 / -0.022em | 中标题 |
| `text.card-title` | 24 / 590 / 1.33 / -0.012em | 卡片标题 |
| `text.body` | 15 / 400 / 1.6 / -0.011em | 正文(产品内 14) |
| `text.body-sm` | 14 / 400 / 1.5 / -0.013em | 小正文 |
| `text.label` | 13 / 510 / 1.5 / -0.01em | 标签/按钮 |
| `text.micro` | 12 / 510 / 1.4 / 0 | 微文本/面包屑 |
| `text.mono` | 13 / 400 / 1.45 / 0 | 代码 |

## 控件高度 — 三档硬规矩

| Token | Value | 用途 |
|------|-------|------|
| `control.sm` | `24px` | 紧凑工具栏 |
| `control.md` | `40px` | 默认(主按钮、输入、select) |
| `control.lg` | `48px` | 营销/大型 CTA |
| `control.touch-min` | `40px` | 触控最小(产品内,不是营销) |

## 组件层 token(代入提示词)

```css
button.primary {
  background: #5E6AD2;
  color: #FFFFFF;
  border: 1px solid transparent;
  border-radius: 9999px;     /* pill 是 Linear 默认按钮 */
  min-height: 40px;
  padding: 0 18px;
  font-size: 14px;
  font-weight: 510;
  letter-spacing: -0.01em;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
  transition: background 150ms ease, transform 100ms ease;
}
button.primary:hover { background: #6B7AD9; }
button.primary:active { transform: scale(0.97); }
button.primary:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(94, 106, 210, 0.4);
}
button.secondary {
  background: rgba(255, 255, 255, 0.03);
  color: #F7F8F8;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 9999px;
  min-height: 40px;
  padding: 0 18px;
}
input {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid #2A2E33;
  border-radius: 6px;
  min-height: 32px;          /* Linear 内嵌输入比按钮矮 */
  padding: 8px 12px;
  color: #F7F8F8;
  font-size: 14px;
}
input:focus {
  border-color: #5E6AD2;
  box-shadow: 0 0 0 3px rgba(94, 106, 210, 0.3);
  outline: none;
}
card {
  background: #1A1B1E;
  border: 1px solid #2A2E33;
  border-radius: 12px;
  padding: 24px;
  /* Linear 不靠 drop-shadow 提升层级,靠 1px border + inset shadow */
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
}
```

## 动效

| Token | Value | 用途 |
|------|-------|------|
| `motion.duration.fast` | `100ms` | transform/active |
| `motion.duration.base` | `150ms` | color / bg / hover |
| `motion.duration.slow` | `200ms` | 大区域切换 |
| `motion.easing.standard` | `cubic-bezier(0.2, 0, 0, 1)` | 标准 |
| `motion.scale.active` | `transform: scale(0.97)` | 按下回弹 |

## 阴影(克制)

Linear 深色界面**不用 drop-shadow 拉层级**,改用 1px border + inset highlight。营销页才用:
```css
shadow.card: 0 4px 24px rgba(0, 0, 0, 0.2);
shadow.focus-ring: 0 0 0 3px rgba(94, 106, 210, 0.4);
```

## 还原时的硬规矩

1. **按钮全部 pill**(`border-radius: 9999px`),除非用户明确要 rectangular。
2. **深色优先**:Stage 2 默认输出 dark 主题;light 是变体不是主。
3. **brand 色 `#5E6AD2` 只用于交互**(链接、focus、primary 按钮)——绝不用于装饰。
4. **每屏只有一个 primary 按钮**——违反即失败。
5. **不用大阴影**——层级靠 1px border。
