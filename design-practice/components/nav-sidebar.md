# Component: Navigation (sidebar + top bar)

The app skeleton. Article line 1493: navigation is where AI shows its "skin without skeleton" problem — pretty icons, but no active state discipline, no keyboard support, no collapse behavior, no breadcrumbs.

## The 3-zone shell (Linear / Notion / Slack consensus)

```text
┌─top-bar (56px)──────────────────────────────────────────┐
│ [☰]  [breadcrumb / page title]            [⌘K] [🔔] [👤] │
├──────────┬───────────────────────────────────────────────┤
│ sidebar  │                                                │
│ (240px)  │                                                │
│          │              main content                      │
│ ┌──────┐ │                                                │
│ │🏠Home│ │                                                │
│ │📋Task│◀│ active item: bg primary/8, left 2px primary    │
│ │📁Proj│ │                                                │
│ │⚙ Set │ │                                                │
│ └──────┘ │                                                │
│          │                                                │
│ [+ New]  │                                                │
└──────────┴───────────────────────────────────────────────┘
```

## Top bar spec

| Token | Value |
| --- | --- |
| height | 56px (`h-14`) — Linear/Notion consensus |
| bg | `color.bg.surface` (#FFFFFF) |
| border-bottom | 1px `color.border.default` |
| padding-x | 16px (`px-4`) first/last, 8px between groups |
| sticky | `sticky top-0 z-30` |
| left zone | mobile menu toggle (hidden desktop) + breadcrumb or page title |
| center zone | (optional) global search / ⌘K command bar |
| right zone | notifications bell, help, user avatar menu |
| gap between right items | 8px |

## Sidebar spec

| Token | Value |
| --- | --- |
| width | 240px expanded (`w-60`), 64px collapsed (`w-16`) |
| bg | `color.bg.canvas` (#FFFFFF) or `color.bg.muted` (#F9FAFB) for tinted |
| border-right | 1px `color.border.default` |
| padding | 12px (`p-3`) |
| nav item height | 36px (`h-9`) — matches button height |
| nav item padding-x | 12px (`px-3`) |
| nav item radius | 8px (`rounded-md`) |
| nav item gap | 2px (`gap-0.5`) between items |
| section label | 11px / 500 uppercase, `color.text.secondary`, 16px above first item |
| icon | 18px (`size-[18px]`), 12px gap right of label |
| active item | bg primary at 8% (`bg-primary/8`), text primary, **left 2px primary border OR primary-tinted icon** |
| hover item | bg muted (`bg-muted`), 100ms |
| focus item | 2px primary ring outside, offset 0 |
| collapse toggle | chevron icon at bottom or top, persists icon-only when collapsed |
| footer | user mini-profile (24px avatar + name) OR primary CTA ("+ New") |

## Nav item states

| State | Visual | Behavior |
| --- | --- | --- |
| default | transparent bg, secondary text + icon | cursor pointer |
| hover | bg muted, text darken | 100ms |
| active (current page) | bg primary at 8%, text primary, icon primary-tinted | persists, aria-current="page" |
| focus | 2px primary ring outside | keyboard reachable (Tab) |
| disabled | opacity 0.5, cursor not-allowed | — |
| collapsed (icon-only) | icon centered, label as tooltip on hover | preserve width 64px |
| badge (count) | right-aligned, 16px min-width, matches `badge.md` | e.g. unread count |

## ⌘K command palette (the modern nav)

Article line 1501: Linear normalized ⌘K. For any productivity tool, ⌘K opens a unified search + action surface.

| Token | Value |
| --- | --- |
| trigger | ⌘K (Mac) / Ctrl+K (Win/Linux) — always |
| position | centered, top 25% of viewport |
| width | 576px (`max-w-xl`) |
| input | 48px height (`h-12`), no label, placeholder "Search or type a command…" |
| results | 40px row height, icon + label + optional shortcut hint |
| grouping | sections by type (Pages, Actions, Recent) with 11px uppercase labels |
| keyboard nav | ↑↓ to move, Enter to select, ESC to close |
| footer | ↑↓ navigate, ↵ select, ESC dismiss |

## Breadcrumb spec

| Token | Value |
| --- | --- |
| height | inherits top bar (56px) |
| separator | `/` or chevron `›`, 12px, `color.text.secondary`, 8px gap |
| current page | 14px / 500, `color.text.primary`, NOT a link |
| ancestors | 14px / 400, `color.text.secondary`, hover underline + primary color |
| truncate | long names truncate middle with ellipsis |

```text
Projects / Acme Inc / Tasks / Task #4831
         ↑           ↑
       link       current (no link, bold)
```

## Prompt fragment (English)

```text
App navigation spec (sidebar + top bar, Linear/Notion-inspired, pixel-exact):

TOP BAR:
- height 56px, sticky top-0 z-30
- bg #FFFFFF, 1px #E5E7EB bottom border
- padding 16px horizontal
- LEFT zone: mobile menu toggle (hidden on desktop, hamburger 24px) + breadcrumb OR page title (16px weight 500)
- CENTER zone (optional): global search / ⌘K trigger (input styled, 320px wide, placeholder "Search or type a command…")
- RIGHT zone: notifications bell (24px, badge dot if unread), help icon (24px), user avatar (32px, opens menu)
- gap between right items: 8px

SIDEBAR:
- width 240px expanded (64px collapsed)
- bg #FFFFFF (or #F9FAFB tinted), 1px #E5E7EB right border
- padding 12px
- nav item: 36px tall, 12px padding-x, radius 8px, gap 2px between items
- nav item content: 18px icon + 12px gap + 14px label
- section label: 11px weight 500 UPPERCASE #6B7280, 16px above first item in section
- active item: bg primary at 8% opacity, text primary, icon primary-tinted, aria-current="page"
- hover item: bg #F9FAFB (muted), 100ms transition
- focus item: 2px primary ring outside
- collapse: chevron toggle, icon-only mode at 64px width, label as tooltip on hover
- footer: user mini-profile (24px avatar + name) OR primary CTA "+ New"

⌘K COMMAND PALETTE (for productivity tools):
- trigger: ⌘K (Mac) / Ctrl+K (Win/Linux) — globally bound
- container: 576px wide, centered, top 25% of viewport, shadow-2xl
- input: 48px height, no label, placeholder "Search or type a command…"
- results: 40px row height, icon + label + optional shortcut hint right-aligned
- grouping: sections by type (Pages, Actions, Recent) with 11px UPPERCASE labels
- keyboard nav: ↑↓ to move selection, Enter to select, ESC to close
- footer: "↑↓ navigate  ↵ select  ESC dismiss" in 12px secondary

BREADCRUMB (in top bar):
- separator: "/" or "›" chevron, 12px #6B7280, 8px gap each side
- ancestors: 14px weight 400 #6B7280, hover underline + primary color
- current page: 14px weight 500 #111827, NOT a link
- truncate: long names truncate with ellipsis

NEVER:
- make the active nav item a different color than primary tint (consistency)
- forget aria-current="page" on active (screen readers)
- skip keyboard nav on ⌘K palette (it's the whole point)
- make the sidebar non-collapsible on tablet widths (cramped content)
- use hamburger on desktop (only mobile)
- forget the breadcrumb "you are here" signal
```

## Prompt fragment (Chinese)

```text
应用导航规格(侧边栏 + 顶栏,Linear/Notion 风格,精确到像素):

顶栏:
- 高 56px,sticky top-0 z-30
- 背景 #FFFFFF,1px #E5E7EB 下边框
- 内边距 左右16px
- 左区:移动端菜单切换(桌面端隐藏,汉堡 24px)+ 面包屑 或 页面标题(16px 字重 500)
- 中区(可选):全局搜索 / ⌘K 触发器(输入框样式,宽 320px,占位符"搜索或输入命令…")
- 右区:通知铃铛(24px,未读有红点)、帮助图标(24px)、用户头像(32px,点开菜单)
- 右区间距:8px

侧边栏:
- 宽 240px 展开(64px 折叠)
- 背景 #FFFFFF(或 #F9FAFB 浅底),1px #E5E7EB 右边框
- 内边距 12px
- 导航项:高 36px,左右内边距 12px,圆角 8px,项间距 2px
- 导航项内容:18px 图标 + 12px 间距 + 14px 标签
- 分组标签:11px 字重 500 大写 #6B7280,距组内首项 16px
- 激活项:背景 主色 8% 透明度,文字 primary,图标主色调,aria-current="page"
- hover 项:背景 #F9FAFB(muted),100ms 过渡
- focus 项:外侧 2px 主色环
- 折叠:箭头切换,64px 宽仅图标模式,标签 hover 时 tooltip
- 底部:用户迷你资料(24px 头像 + 名字)或 主 CTA "+ 新建"

⌘K 命令面板(生产力工具必备):
- 触发:⌘K(Mac)/ Ctrl+K(Win/Linux)——全局绑定
- 容器:宽 576px,居中,距顶 25% 视口高,shadow-2xl
- 输入:高 48px,无标签,占位符"搜索或输入命令…"
- 结果:行高 40px,图标 + 标签 + 可选快捷键提示右对齐
- 分组:按类型分节(页面、操作、最近),11px 大写标签
- 键盘导航:↑↓ 移动选择,Enter 选中,ESC 关闭
- 底部:"↑↓ 导航  ↵ 选择  ESC 关闭" 12px secondary

面包屑(顶栏内):
- 分隔符:"/" 或 "›" 箭头,12px #6B7280,两侧各 8px 间距
- 祖先项:14px 字重 400 #6B7280,hover 下划线 + 主色
- 当前页:14px 字重 500 #111827,不是链接
- 截断:长名用省略号截断

绝对不要:
- 激活导航项用非主色调的颜色(要一致)
- 忘了激活项的 aria-current="page"(屏幕阅读器)
- ⌘K 面板跳过键盘导航(那是它的核心)
- 平板宽度还不让侧边栏折叠(内容挤)
- 桌面端用汉堡(只移动端)
- 忘了面包屑"你在哪"的信号
```

## Tailwind classes

```tsx
// app shell
<div className="flex h-screen flex-col">
  {/* top bar */}
  <header className="sticky top-0 z-30 flex h-14 items-center justify-between border-b border-[--color-border-default] bg-[--color-bg-surface] px-4">
    <div className="flex items-center gap-2">
      <Button variant="ghost" size="icon" className="md:hidden" aria-label="Menu">☰</Button>
      <Breadcrumb />
    </div>
    <div className="flex items-center gap-2">
      <Button variant="ghost" size="icon" aria-label="Notifications"><Bell /><span className="size-2 rounded-full bg-[--color-danger]" /></Button>
      <Avatar size={32} src={user.avatar} />
    </div>
  </header>

  <div className="flex flex-1 overflow-hidden">
    {/* sidebar */}
    <aside className="w-60 shrink-0 border-r border-[--color-border-default] bg-[--color-bg-surface] p-3">
      <nav className="flex flex-col gap-0.5">
        <span className="px-3 pb-1 pt-4 text-[11px] font-medium uppercase tracking-wide text-[--color-text-secondary]">Workspace</span>
        <a href="#" aria-current="page" className="flex h-9 items-center gap-3 rounded-md bg-[--color-state-primary]/8 px-3 text-sm font-medium text-[--color-text-primary]">
          <HomeIcon className="size-[18px] text-[--color-state-primary]" /> Home
        </a>
        <a href="#" className="flex h-9 items-center gap-3 rounded-md px-3 text-sm text-[--color-text-secondary] transition-colors hover:bg-[--color-bg-muted] hover:text-[--color-text-primary]">
          <TasksIcon className="size-[18px]" /> Tasks
        </a>
      </nav>
    </aside>

    {/* main */}
    <main className="flex-1 overflow-y-auto bg-[--color-bg-canvas]">{children}</main>
  </div>
</div>
```

## Reverse examples

| Aspect | Plastic | Human |
| --- | --- | --- |
| active state | different colors per item | consistent primary tint |
| aria-current | missing | "page" on active |
| ⌘K | missing or mouse-only | global trigger + full keyboard nav |
| collapse | never | icon-only at <1024px |
| breadcrumb | page title only | full path with links |
| top bar height | arbitrary (44px, 64px) | 56px consensus |

## Composes with

- `avatar.md` — user menu trigger (32px in top bar, 24px in sidebar footer)
- `badge.md` — unread count on nav items, notification dot
- `button.md` — "+ New" primary CTA in sidebar footer, ghost icons in top bar
- `modal.md` / `drawer.md` — user menu opens one

## Failure modes

| Failure | Fix |
| --- | --- |
| inconsistent active color | standardize to primary tint |
| no aria-current | add aria-current="page" |
| no ⌘K | add global trigger + keyboard nav |
| no collapse on tablet | collapse to 64px below 1024px |
| hamburger on desktop | hide below md breakpoint |
| title-only "where am I" | add breadcrumb |
