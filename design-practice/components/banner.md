# Component: Banner (persistent system status)

> 出处:原文行 620:"**保存成功,用 toast;权限不足,用 inline message 或 banner;删除危险,用确认弹窗;列表为空,用空状态;加载较久,用骨架屏或进度提示稳住心。**"
>
> Banner 是 toast 的对位组件。Toast 是**瞬时**反馈(4-6 秒消失);Banner 是**持久**反馈(置顶、不可自动消失、需要用户主动关闭或状态变更后消失)。

## 为什么需要单独一个组件(不是 toast 加个不消失参数)

AI 翻车点:权限不足、离线模式、只读模式、维护公告——这些是**产品级状态**,不是单次操作的结果。AI 把它们塞进 toast,4 秒后自动消失,用户没看清就没了,然后再次操作又被拒,死循环。

| 场景 | 错误容器 | 正确容器 | 为什么 |
|---|---|---|---|
| 权限不足(本页只读) | toast(消失) | **Banner 置顶** | 用户每次操作都会触发,toast 闪一下就没了,用户以为是 bug |
| 离线模式 | toast(消失) | **Banner 置顶** | 离线状态持续,用户需要随时知道"我现在是离线的" |
| 只读模式(管理员降权) | toast(消失) | **Banner 置顶** | 同上,持续状态 |
| 维护公告 / 密码过期强提醒 | toast(消失) | **Banner 置顶 + 关闭按钮** | 用户必须看见且主动处理 |
| 保存成功 | Banner(置顶)❌ | **Toast** ✓ | 单次结果,用 Banner 占顶部太重 |
| 字段校验错 | Banner(置顶)❌ | **Inline at field** ✓ | 字段级错误,与 Banner 无关 |

## Spec table (pixel-exact)

| Token | Value |
| --- | --- |
| width | 100% of container(不是固定宽度,贴顶/贴内容区) |
| min-height | 48px |
| bg | variant color at 10% opacity(如 danger 用 `#FEE2E2`) |
| border-left | 4px solid variant color(主信号) |
| border | 无其他边框(靠 4px 左条 + 浅底识别) |
| radius | 0(贴顶贴边,无圆角)或 8px(内嵌在内容区时) |
| padding | 12px 16px(`px-4 py-3`) |
| shadow | none(不漂浮,贴在页面/内容区顶部) |
| position | sticky top-0(主区顶部)或 sticky top-[--header-h](header 下方) |
| z-index | 40(sticky banner,低于 modal=60 / drawer=50 / toast=70) |
| close button | 右侧 ghost icon(可选——权限/离线 banner 不允许关闭,因为状态没变) |
| animation | 200ms slide-down + fade(进入);200ms slide-up + fade(退出) |

## Banner anatomy

```text
danger banner(权限不足,不可关闭):
┌────────────────────────────────────────────────────────────────┐
│ ▌  你没有编辑权限。本页为只读模式。如需修改,请联系管理员。       │
│ ↑ 4px 左条  ↑ icon 16px       ↑ message 14px/500               │
└────────────────────────────────────────────────────────────────┘

warning banner(离线,可关闭):
┌────────────────────────────────────────────────────────────────┐
│ ▌  ⚠ 当前离线。你的修改会暂存在本地,联网后自动同步。        [ × ] │
│ ↑ 4px 左条  ↑ icon   ↑ message                    ↑ close ghost │
└────────────────────────────────────────────────────────────────┘

info banner(维护公告,带操作):
┌────────────────────────────────────────────────────────────────┐
│ ▌  ℹ 系统将于今晚 22:00 维护 30 分钟。                  [ 查看 ] │
└────────────────────────────────────────────────────────────────┘
```

## Variants

| Variant | Left border color | Bg | Icon | Close | Example |
| --- | --- | --- | --- | --- | --- |
| **danger** | red #EF4444 | #FEE2E2 | ⛔ or ✕ | 不允许(状态没变) | 权限不足、账户冻结、删除失败需手动恢复 |
| **warning** | amber #F59E0B | #FEF3C7 | ⚠ | 允许(用户已知) | 离线、只读、磁盘满、订阅过期 |
| **info** | blue #3B82F6 | #DBEAFE | ℹ | 允许 | 维护公告、新功能提示 |
| **success** | green #10B981 | #D1FAE5 | ✓ | 允许(罕见用) | 全局同步完成、批量操作成功(少用,Banner 通常不是好事) |

## States

| State | Visual | Behavior |
| --- | --- | --- |
| entering | slide-down + fade 200ms | 进入视口 |
| visible | static,4px 左条 + 浅底 + icon + message | sticky 顶部 |
| with action | action button right-aligned(text button,ghost) | 点击触发动作 |
| closeable | close × icon right | 点击关闭(状态变更后自动消失) |
| persistent | 无 close × icon | 状态变更前一直在(如权限 banner) |
| exiting | slide-up + fade 200ms | 状态变更后退出 |

## 和 toast 的边界(决策表)

| 维度 | Toast | Banner |
| --- | --- | --- |
| 时长 | 瞬时(4-6s) | 持久(状态没变就在) |
| 范围 | 单次操作结果 | 产品级状态 |
| 关闭 | 自动消失 | 用户主动关 / 状态变更后消失 |
| 位置 | 右上角(桌面)/ 底部居中(移动) | 内容区顶部 sticky |
| 数量 | 可叠 3 个 | 同时只 1 个(多了用 notice center) |
| z-index | 70 | 40 |
| 例子 | "任务已保存"、"导出失败" | "权限不足"、"离线模式"、"维护公告" |

## Prompt fragment (English)

```text
Banner spec (persistent system status, pixel-exact):
- container: full-width, 100% of parent, min-height 48px
- background: variant color at 10% opacity (danger=#FEE2E2, warning=#FEF3C7, info=#DBEAFE, success=#D1FAE5)
- border-left: 4px solid variant color (danger=#EF4444, warning=#F59E0B, info=#3B82F6, success=#10B981)
- border (other): none
- radius: 0 (sticky top of page) OR 8px (embedded in content area)
- padding: 12px 16px
- position: sticky top-0 (below header) — stays visible while scrolling
- z-index: 40 (below modal/drawer/toast, above page content)
- enter: slide-down + fade, 200ms ease-out
- exit: slide-up + fade, 200ms ease-in

anatomy:
- left border 4px variant color (the main signal)
- icon 16px (left of message, after the 4px border): ⛔ danger, ⚠ warning, ℹ info, ✓ success
- message: 14px weight 500, color inherits (usually text-primary)
- action button (optional): text button right-aligned (ghost), inherits button.md focus-visible rule
- close button (optional): ghost icon × top-right, hidden if banner is persistent (state-locked)

variants:
- danger: 4px red left border, bg #FEE2E2, ⛔ icon, NO close button (state must change first)
- warning: 4px amber, bg #FEF3C7, ⚠ icon, optional close
- info: 4px blue, bg #DBEAFE, ℹ icon, optional close
- success: 4px green, bg #D1FAE5, ✓ icon, optional close (rarely used — banners are rarely good news)

WHEN TO USE BANNER VS TOAST:
- permission denied (page-level read-only) → BANNER (sticky, no close)
- offline mode → BANNER (sticky, no close, state-locked)
- read-only mode (admin downgraded) → BANNER
- maintenance announcement → BANNER (info, with action link)
- password expiring soon → BANNER (warning, with action "Change now")
- single save success → TOAST (not banner)
- single save failure → TOAST with retry OR inline error (not banner)

NEVER:
- use banner for single-operation results (use toast)
- auto-dismiss a banner (banners persist until state changes or user closes)
- close a danger/permission banner without fixing the state (user will just trigger it again)
- stack banners (only one banner visible at a time — multiple go into a notice center)
- use banner for field-level error (use inline below field)
```

## Prompt fragment (Chinese)

```text
Banner 规格(持久系统状态,精确到像素):
- 容器:宽度 100%(贴父容器),最小高度 48px
- 背景:变体色 10% 透明度(danger=#FEE2E2,warning=#FEF3C7,info=#DBEAFE,success=#D1FAE5)
- 左边框:4px 实线变体色(danger=#EF4444,warning=#F59E0B,info=#3B82F6,success=#10B981)
- 其他边框:无
- 圆角:0(贴顶贴边)或 8px(内嵌内容区)
- 内边距:12px 16px
- 位置:sticky top-0(header 下方)—— 滚动时保持可见
- z-index:40(低于 modal/drawer/toast,高于页面内容)
- 进入:200ms 下滑 + 淡入
- 退出:200ms 上滑 + 淡出

结构:
- 左侧 4px 变体色条(主信号)
- 图标 16px(4px 条右侧):⛔ danger、⚠ warning、ℹ info、✓ success
- 信息:14px 字重 500,色继承(通常 text-primary)
- 操作按钮(可选):右对齐文字按钮(ghost),继承 button.md focus-visible 规则
- 关闭按钮(可选):右上角 ghost × 图标,持久 banner(状态锁定)隐藏

变体:
- danger:4px 红左边框,底 #FEE2E2,⛔ 图标,无关闭按钮(状态必须先变)
- warning:4px 琥珀,底 #FEF3C7,⚠ 图标,可关闭
- info:4px 蓝,底 #DBEAFE,ℹ 图标,可关闭
- success:4px 绿,底 #D1FAE5,✓ 图标,可关闭(罕见用——Banner 通常不是好消息)

什么时候用 Banner 而不是 Toast:
- 页面级权限不足(只读)→ BANNER(sticky,不关闭)
- 离线模式 → BANNER(sticky,不关闭,状态锁)
- 管理员降权只读 → BANNER
- 维护公告 → BANNER(info,带操作链接)
- 密码即将过期 → BANNER(warning,带操作"立即修改")
- 单次保存成功 → TOAST(不要 Banner)
- 单次保存失败 → TOAST + 重试 或 就地错误(不要 Banner)

绝对不要:
- 用 Banner 报单次操作结果(用 Toast)
- 让 Banner 自动消失(Banner 持续到状态变更或用户关闭)
- 在状态没修复前关闭 danger/权限 Banner(用户会再触发)
- 叠 Banner(同时只 1 个——多了进消息中心)
- 用 Banner 报字段级错误(用字段下方就地错误)
```

## Tailwind classes

```tsx
// warning banner (offline, persistent)
<div
  role="alert"
  aria-live="polite"
  className="sticky top-0 z-40 flex w-full items-center gap-3 border-l-4 border-l-[--color-warning] bg-[--color-warning-bg] px-4 py-3"
>
  <span className="size-4 shrink-0 text-[--color-warning]">⚠</span>
  <p className="flex-1 text-sm font-medium text-[--color-text-primary]">
    当前离线。你的修改会暂存在本地,联网后自动同步。
  </p>
</div>

// danger banner (permission denied, no close)
<div
  role="alert"
  aria-live="assertive"
  className="sticky top-0 z-40 flex w-full items-center gap-3 border-l-4 border-l-[--color-danger] bg-[--color-danger-bg] px-4 py-3"
>
  <span className="size-4 shrink-0 text-[--color-danger]">⛔</span>
  <p className="flex-1 text-sm font-medium text-[--color-text-primary]">
    你没有编辑权限。本页为只读模式。如需修改,请联系管理员。
  </p>
</div>

// info banner (maintenance, with action, closeable)
<div role="status" aria-live="polite" className="... border-l-[--color-info] bg-[--color-info-bg] ...">
  <span className="size-4 text-[--color-info]">ℹ</span>
  <p className="flex-1 text-sm font-medium">系统将于今晚 22:00 维护 30 分钟。</p>
  <button className="text-sm font-medium text-[--color-info] hover:underline">查看详情</button>
  <IconButton aria-label="关闭" variant="ghost" onClick={dismiss}>×</IconButton>
</div>
```

## Reverse examples

| Aspect | Plastic | Human |
| --- | --- | --- |
| 持续状态容器 | 全塞进 toast 4 秒消失 | 权限/离线进 Banner,sticky |
| 边框 | 全 1px 边框,弱信号 | 4px 左条 + 浅底,强信号 |
| 关闭按钮 | 所有 banner 都给关闭 | danger/权限 banner 隐藏关闭(状态没变) |
| 位置 | absolute 漂浮 | sticky top-0,滚动时保持 |
| 数量 | 多个 banner 叠加 | 同时只 1 个,多了进 notice center |
| aria-live | 缺失 | role="alert"(danger)/ role="status"(info) |

## Composes with

- `button.md` — action button inside banner, close × icon
- `toast.md` — 边界对照(瞬时 vs 持久)
- `empty-state.md` — 权限空状态可以配套权限 banner

## Failure modes

| Failure | Fix |
| --- | --- |
| 持续状态塞 toast | 用 Banner |
| 单次结果塞 Banner | 用 Toast |
| 关闭按钮全给 | danger/权限 banner 隐藏关闭 |
| sticky 失效 | 用 sticky 而非 fixed,避免遮挡 |
| 多个 banner 叠 | 同时只 1 个,多余进 notice center |
| 字段错误用 Banner | 用 inline below field |
