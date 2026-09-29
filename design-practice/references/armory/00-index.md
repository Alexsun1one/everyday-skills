# 00 — 风格路由表(选哪本弹药)

意图进来先选风格。每行:风格名 → 对应 tokens 文件 → 一句话特质 → 适用场景 → **不要用在**。

| 风格 | Tokens 文件 | 一句话特质 | 适用场景 | 不要用在 |
|------|------------|----------|--------|--------|
| **Linear 风** | `01-tokens-linear.md` | 深色优先、6/12/9999 三档 radius、4px 基、克制功能色 | SaaS 后台、任务/项目管理、开发者工具 | 营销首页、儿童/教育、强品牌插画 |
| **Stripe 风** | `02-tokens-stripe.md` | 8px 基、细到 2px、靛蓝 #533afd 单电压、pill CTA、Sohne 字 | 金融、支付、定价页、营销 | 内容密集型后台、深色优先产品 |
| **Notion 风** | `03-tokens-notion.md` | 4px 基、5px 按钮 radius、24px 卡片、黑色单 CTA、Inter | 文档、知识库、编辑器、白板 | 数据密集型表格、金融 |
| **Material 3 / Android** | `04-tokens-material3.md` | 4dp 基、shape 阶 4/8/12/16/28、tonal elevation、Roboto | Android 应用、跨平台、Expressive 风 | 苹果生态、Linear 风克制后台 |
| **Apple HIG / iOS** | 见 `case-studies.md` Apple 节 + 原文行 2412-2442 的 HIG 拆解提示词（待建独立 tokens 文件） | 8pt 基 4pt 细分、44pt 触控硬底线、SF Pro、Liquid Glass | iOS/iPadOS/macOS 原生应用 | Web 后台、Windows、安卓优先 |
| **shadcn / Tailwind 默认** | `05-tokens-tailwind-shadcn.md` | h-9 默认按钮、rounded-md、Tailwind scale、组件代码归你 | 现代 React/Web 应用、快速搭建 | 强品牌一致性要求、需要原生手感 |

## 路由决策树

```
用户说"Linear 风"        → 01
用户说"Stripe 风"/"支付" → 02
用户说"Notion 风"/"文档" → 03
用户说"Android"/"Material" → 04
用户说"iOS"/"苹果原生"   → 04(HIG 节)
用户没指定,要做 Web 后台 → 默认 01 + 05 混(克制 + Tailwind)
用户没指定,要做营销页    → 默认 02(Stripe 营销调)
用户没指定,要做内容/编辑 → 默认 03
用户要做原生移动         → 04(M3 或 HIG 二选一,看平台)
```

## 混用规则

- **同一产品只用一种基线风格**——别把 Linear 的 radius 和 Stripe 的颜色混。
- tokens 层可借(例如 Linear 风借 Tailwind 间距链),但语义/组件 token 必须重新映射到当前风格。
- 状态/动效库(`10-` ~ `43-`)跨风格通用——任何风格都得满足 8 态/微交互四件套。

## 选完后

1. 读对应 tokens 文件,把表里值代入 Stage 2 还原提示词。
2. 按 `30-` ~ `35-` 选业务模式。
3. 按 `40-` ~ `43-` 选微交互。
4. 检查 `14-basic-modal-drawer-toast.md` 的浮层是否被弹药覆盖。
