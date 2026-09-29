# Component: Input (text input, textarea, form field)

Where users suffer most. Article line 1292: *"用户填表,本质上是在替产品劳动. 你多问一句,他多付一点成本;你报错说不清,他多绕一圈;你提交失败还丢内容,他可能直接走人."*

## Spec table (pixel-exact)

| Token | Value | Notes |
| --- | --- | --- |
| height | 36px (`h-9`) | matches button height |
| padding-x | 12px (`px-3`) | Stripe uses 8px; 12px is the modern default |
| padding-y | 8px (`py-2`) | |
| radius | 8px (`rounded-md`) | matches button |
| font | 14px / 1.5 (`text-sm`) | |
| bg | `color.bg.canvas` (#FFFFFF) | |
| border default | 1px `color.border.default` (#E5E7EB or #D1D5DB) | |
| border hover | 1px `color.border.strong` (#9CA3AF) | subtle darken |
| border focus | 2px `color.border.focus` (#5E6AD2) + 2px ring outside | double-ring for clarity |
| border error | 2px `color.danger` (#DC2626) + inline message below | |
| text color | `color.text.primary` (#111827) | |
| placeholder | `color.text.secondary` (#6B7280) | never lighter — fails WCAG |
| label | 14px / 500, above input, 6px gap | always visible (no floating label unless space-constrained) |
| helper text | 12px / `color.text.secondary`, below input, 4px gap | shown BEFORE error, not only on error |
| error message | 12px / `color.danger`, below input (replaces helper), 4px gap | in-place, specific, recoverable |
| mobile font | ≥16px | iOS Safari auto-zooms below 16px — causes layout shift |
| min tap target | 44px height (with padding) | |

## States (per article line 11194-11222)

| State | Visual | Copy | Behavior |
| --- | --- | --- | --- |
| default | 1px border default, bg canvas, placeholder secondary | label + helper ("we'll never share your email") | editable |
| hover | 1px border darken slightly | same | cursor text |
| focus | **2px border focus + 2px ring outside** (4px total accent), no placeholder flicker | same | typing, keyboard reachable |
| filled | text primary, border default | same | editable |
| error | **2px border danger**, helper replaced by error message inline below | error: specific ("email missing @") + recovery ("check and retry") | editable, draft preserved |
| disabled | bg muted, opacity 0.6, cursor not-allowed | label + "disabled because..." | not editable |
| readonly | bg canvas, no border change, text primary | label + "(read-only)" badge | not editable, selectable |
| loading (with button) | input stays editable, paired button shows loading | — | draft preserved across async |

**Focus state is mandatory.** Article line 11194: *"聚焦态必须满足对比度"* — the 2px+2px double ring is the clearest focus affordance.

**Error is in-place.** Article line 11711: *"哪里出错,哪里解释"* — never a global toast for a field error.

## Prompt fragment (English)

```text
Input field spec (Stripe-inspired, pixel-exact):
- container: 36px tall, padding 12px horizontal 8px vertical, radius 8px
- border default: 1px solid #E5E7EB (gray-200)
- border hover: 1px solid #9CA3AF (gray-400) — subtle darken
- border focus: 2px solid #5E6AD2 (Linear violet) PLUS 2px ring of same color outside, offset 0
  → total 4px accent ring on focus; this is the clearest focus affordance
- border error: 2px solid #DC2626 (red-600); error message appears BELOW input (not above, not as toast)
- typography: 14px / 1.5 line-height, input text #111827 (gray-900)
- placeholder: #6B7280 (gray-500) — NEVER lighter, fails WCAG contrast
- label: 14px weight 500, positioned ABOVE input with 6px gap (always visible — no floating label unless mobile-constrained)
- helper text: 12px #6B7280, BELOW input with 4px gap, shown BEFORE error ("6-20 characters")
- error message: 12px #DC2626, replaces helper text position when error fires
- mobile: font-size ≥16px to prevent iOS Safari auto-zoom

validation behavior:
- validate on BLUR (not on every keystroke — that's naggy)
- once in error, re-validate on every keystroke (so user sees recovery live)
- on success: clear error, restore helper text, optional green checkmark icon RIGHT side

error wording (human, specific, recoverable):
- BAD: "invalid input", "request failed", "operation invalid"
- GOOD: "email missing @ — check and retry", "password needs 8+ chars", "file over 20MB — compress and re-upload"

NEVER:
- remove focus ring
- use placeholder as label (placeholder disappears on type)
- clear user input on error (draft must survive)
- show error as global toast at page top
- validate on every keystroke (naggy)
- use auto-zoom-triggering font (<16px) on mobile
```

## Prompt fragment (Chinese)

```text
输入框规格(Stripe 风格,精确到像素):
- 容器:高 36px,内边距 左右12px 上下8px,圆角 8px
- 默认边框:1px 实线 #E5E7EB(gray-200)
- hover 边框:1px 实线 #9CA3AF(gray-400)——轻微加深
- focus 边框:2px 实线 #5E6AD2(Linear 紫)外加 同色 2px 外环,offset 0
  → 聚焦时总共 4px 强调环;这是最清晰的聚焦反馈
- error 边框:2px 实线 #DC2626(red-600);错误信息出现在输入框下方(不是上方,不是 toast)
- 字体:14px / 行高 1.5,输入文字 #111827(gray-900)
- 占位符:#6B7280(gray-500)——绝不能更浅,否则 WCAG 对比度不过
- 标签:14px 字重 500,定位在输入框上方,间距 6px(始终可见——除非手机空间紧否则不用浮动标签)
- 辅助文字:12px #6B7280,在输入框下方,间距 4px,出错前就显示("6-20 个字符")
- 错误信息:12px #DC2626,出错时替换辅助文字的位置
- 手机端:字号 ≥16px,否则 iOS Safari 自动缩放

校验行为:
- 失焦时校验(不要每输入一个字符就校验——烦人)
- 一旦出错,之后每次输入都重新校验(让用户实时看到恢复)
- 校验通过:清掉错误,恢复辅助文字,右侧可选绿色对勾图标

错误文案(说人话、具体、可恢复):
- 错误:"无效输入"、"请求失败"、"操作无效"
- 正确:"邮箱缺少 @,请检查后重试"、"密码需要 8 位以上"、"文件超过 20MB,请压缩后上传"

绝对不要:
- 删掉 focus ring
- 用占位符当标签(一输入就消失)
- 出错时清空用户输入(草稿必须保留)
- 把错误显示成页面顶部的全局 toast
- 每输入一个字符就校验(烦)
- 手机端用 <16px 的字号(会触发自动缩放)
```

## Tailwind classes

```tsx
// text input
<input
  type="text"
  className="h-9 w-full rounded-md border border-[--color-border-default] bg-[--color-bg-canvas] px-3 py-2 text-sm text-[--color-text-primary] placeholder:text-[--color-text-secondary] transition-colors hover:border-[--color-border-strong] focus:border-[--color-border-focus] focus:outline-none focus:ring-2 focus:ring-[--color-border-focus] focus:ring-offset-0 aria-[invalid=true]:border-[--color-danger] aria-[invalid=true]:ring-2 aria-[invalid=true]:ring-[--color-danger]/20 disabled:bg-[--color-bg-muted] disabled:opacity-60"
  aria-invalid={!!error}
/>

// label + helper + error wrapper
<div className="space-y-1.5">
  <label className="text-sm font-medium text-[--color-text-primary]">Email</label>
  <input ... />
  {error ? (
    <p className="text-xs text-[--color-danger]">{error}</p>
  ) : (
    <p className="text-xs text-[--color-text-secondary]">We'll never share your email.</p>
  )}
</div>
```

## Reverse examples

| Aspect | Plastic | Human |
| --- | --- | --- |
| label | placeholder doubles as label (disappears on type) | always-visible label above |
| focus | 1px color change, hard to see | 2px border + 2px ring = 4px accent |
| error | global toast "operation failed" | inline below field, specific wording |
| validation | every keystroke, naggy | on blur, then live re-validate in error |
| draft on error | cleared | preserved |
| mobile font | 14px → iOS zooms | ≥16px |
| placeholder color | gray-300 (fails WCAG) | gray-500 |

## Composes with

- `button.md` — submit button (primary) below the form
- `table-row.md` — inline-edit inputs in rows
- `drawer.md` — form inside drawer; on close, draft preserved or warned
- `modal.md` — confirm before discarding unsaved form

## Failure modes

| Failure | Fix |
| --- | --- |
| placeholder as label | add always-visible label above |
| weak focus | 2px border + 2px ring outside |
| global error toast | inline error at field |
| clears input on error | preserve draft |
| validates per keystroke | validate on blur, re-validate in error |
| <16px mobile font | bump to 16px |
