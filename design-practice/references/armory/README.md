# Armory — 精确弹药库

弹药库的目的:**Stage 2 还原时,所有尺寸/状态/交互不允许靠感觉**——直接从下面查表代入。

每张表都从真实世界级产品逆向出来(Linear / Stripe / Notion / Apple / Material 3 / shadcn / Radix),精确到 px / ms / cubic-bezier。

## 怎么用

1. 用户说出意图(例如"任务管理页"+"Linear 风"),先路由到 `00-index.md` 找风格。
2. Stage 2 还原前,**必须**先读对应风格文件,把里面的精确值代入提示词。
3. 任何"差不多""大概"是失败信号——表里有就是表里那个值。

## 文件清单

| 文件 | 内容 | 精确到 |
|------|------|--------|
| `00-index.md` | 风格 → 文件路由;一表选风格 | — |
| `01-tokens-linear.md` | Linear design tokens 全集 | px / hex / ms / cubic-bezier |
| `02-tokens-stripe.md` | Stripe design tokens 全集 | px / hex |
| `03-tokens-notion.md` | Notion design tokens 全集 | px / hex |
| `04-tokens-material3.md` | Material 3 + Apple HIG tokens 全集 | dp / pt |
| `05-tokens-tailwind-shadcn.md` | Tailwind 默认 scale + shadcn/ui 尺寸链 | rem / px |
| `10-basic-button.md` | Button:6 风格 × 5 尺寸 × 8 状态 全矩阵 | px |
| `11-basic-input.md` | Input / Textarea / Select:6 状态 × 尺寸 | px |
| `12-basic-card.md` | Card:3 变体 × 内边距 × 边框 × 阴影 | px |
| `13-basic-table.md` | Table:行高/列宽/对齐/排序/空态/加载态 | px |
| `14-basic-modal-drawer-toast.md` | Modal / Drawer / Toast:触发/层级/尺寸/动效 | px / ms |
| `15-basic-badge-avatar.md` | Badge / Avatar / Chip:尺寸链/状态 | px |
| `20-complex-tabs-dropdown.md` | Tabs / Dropdown / Menu:激活态/键盘/对齐 | px |
| `21-complex-popover-tooltip.md` | Popover / Tooltip:触发延迟/箭头/边界 | px / ms |
| `22-complex-datepicker-combobox.md` | DatePicker / Combobox:键盘/范围/时区 | px |
| `23-complex-tree-pagination.md` | Tree / Pagination:层级/间距/当前页 | px |
| `30-pattern-list-detail.md` | 列表-详情 模式:三栏/分屏/抽屉 触发 | px |
| `31-pattern-form-wizard.md` | 表单向导:步骤/校验/草稿/提交 | px |
| `32-pattern-data-table-filter.md` | 数据表格+筛选:密度/筛选/批量/导出 | px |
| `33-pattern-kanban.md` | 看板:列宽/卡片/WIP/拖拽 | px |
| `34-pattern-settings.md` | 设置页:分组/开关/危险区/搜索 | px |
| `35-pattern-empty-loading-error.md` | 空三态 + 加载 + 错误恢复 模式 | px |
| `40-micro-button.md` | 按钮微交互:trigger/rule/feedback/loop 精确 | ms / transform |
| `41-micro-input.md` | 输入微交互:focus / 校验 / 自动填充 / 粘贴 | ms |
| `42-micro-drag.md` | 拖拽微交互:抬升 / 占位 / 落点 / 弹回 | ms / scale |
| `43-micro-toggle-upload-notify.md` | 开关 / 上传 / 通知 / 抽屉 微交互四件套 | ms |

## 调研来源(可追溯)

- Linear: designmd.cc/benchmarks/linear + Reseed + 多份 design-md
- Stripe: docs.stripe.com/stripe-apps/style + duply.ai/stripe + explainx.ai
- Notion: designmd.co/d/notion + styleextract.com/vault/notion + refero.styles
- Apple: developer.apple.com/design/tips + HIG buttons + ehmo/platform-design-skills/ios
- Material 3: developer.android.com + Material spec + hamen/material-3-skill
- shadcn/ui: ui.shadcn.com/docs/components/base/button + GitHub v4 button.tsx
- Radix: radix-ui.com/primitives/docs/guides/composition + Mintlify accessibility
- Motion: material-components Motion.md + aldefy/compose-skill material3-motion.md

所有数值已交叉验证;每张表头部标了来源,可回溯。
