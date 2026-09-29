# Component: Avatar (with status dot)

User representation. Article line 1456: avatars are everywhere, but AI gets the sizes, the fallbacks, and the presence indicators wrong.

## Spec table (pixel-exact)

| Size | Value | Use |
| --- | --- | --- |
| xs | 16px (`size-4`) | inline in dense text, mentions |
| sm | 24px (`size-6`) | table rows, list items, comments |
| md | 32px (`size-8`) | default, nav bar, headers |
| lg | 40px (`size-10`) | profile cards, comment authors |
| xl | 64px (`size-16`) | profile pages |
| 2xl | 96px (`size-24`) | large profile, onboarding |

| Token | Value |
| --- | --- |
| radius | 9999px (`rounded-full`) — always circle for people |
| border | 2px `color.bg.surface` (creates separation when stacked) |
| bg fallback | `color.bg.muted` (when no image) |
| text fallback | initials, 14px / 500, `color.text.secondary`, centered |
| status dot (presence) | xs/sm: 8px, md: 10px, lg+: 12px |
| status dot position | bottom-right, 2px inside, 2px border in bg color |
| status dot colors | green=online, gray=offline, amber=away, red=busy/do-not-disturb |

## Avatar group (stacked)

```text
[AB][CD][EF][+3]   ← overlapping avatars with count overflow
```

| Token | Value |
| --- | --- |
| overlap | -8px margin-left on each after first (`-space-x-2`) |
| max visible | 4; rest shown as "+N" pill |
| overflow pill | same height as avatars, bg muted, text secondary |
| border | 2px `color.bg.surface` on every avatar (creates separation) |
| z-index | first on top, decreasing |

## States

| State | Visual |
| --- | --- |
| loaded | image fills circle (object-cover) |
| loading | skeleton pulse (gray-200 bg) |
| error (image failed) | initials fallback |
| no image set | initials fallback |
| hover (in avatar group) | bring to front (z-index raise) + tooltip with name |

## Prompt fragment (English)

```text
Avatar spec (with status dot, pixel-exact):
sizes (always circle for people, radius 9999px):
- xs 16px: inline in dense text, @mentions
- sm 24px: table rows, list items, comments
- md 32px: default, nav bar, headers
- lg 40px: profile cards, comment authors
- xl 64px: profile pages
- 2xl 96px: large profile, onboarding

fallbacks:
- bg #F3F4F6 (muted) when no image
- initials: 14px weight 500 #6B7280, centered, capitalize
- border 2px #FFFFFF (or page bg) for separation when stacked

status dot (presence indicator):
- size: 8px for xs/sm, 10px for md, 12px for lg+
- position: bottom-right, 2px inside the circle, 2px border in #FFFFFF
- colors: green=online, gray=offline, amber=away, red=do-not-disturb
- omit if presence is unknown (don't show gray by default — ambiguous)

avatar group (stacked):
- overlap: -8px margin-left each (Tailwind -space-x-2)
- max 4 visible; rest as "+N" pill (same height, bg muted, text secondary)
- border 2px #FFFFFF on every avatar
- first avatar highest z-index, decreasing
- hover: bring to front + tooltip with full name

loading:
- skeleton pulse: bg gray-200 with pulse animation, same size as final
- error (image 404): fall back to initials silently (no broken image icon)

NEVER:
- use square avatars for people (squares are for objects/brands)
- use a placeholder face emoji (👤) — use initials
- omit the status dot border (it disappears into the avatar)
- show "+N" without a number (just "+" is meaningless)
- let broken image icons appear (fall back to initials)
```

## Prompt fragment (Chinese)

```text`
头像规格(带状态点,精确到像素):
尺寸(人物永远圆形,圆角 9999px):
- xs 16px:密集文字内联,@提及
- sm 24px:表格行、列表项、评论
- md 32px:默认,导航栏,头部
- lg 40px:个人卡片,评论作者
- xl 64px:个人页
- 2xl 96px:大头像,引导页

兜底:
- 无图时背景 #F3F4F6(muted)
- 首字母:14px 字重 500 #6B7280,居中,大写
- 堆叠时 2px #FFFFFF(或页面底色)边框分隔

状态点(在线指示):
- 尺寸:xs/sm 8px,md 10px,lg+ 12px
- 位置:右下角,圆内 2px,2px #FFFFFF 边框
- 颜色:绿=在线,灰=离线,琥珀=离开,红=勿扰
- 未知状态就不显示(别默认灰——歧义)

头像组(堆叠):
- 重叠:每个左侧 -8px 外边距(Tailwind -space-x-2)
- 最多 4 个可见;其余显示成"+N"胶囊(同高,背景 muted,文字 secondary)
- 每个头像 2px #FFFFFF 边框
- 第一个 z-index 最高,递减
- hover:提到最前 + tooltip 显示全名

加载:
- 骨架脉冲:背景 gray-200 + 脉冲动画,尺寸同最终
- 错误(图 404):静默回退到首字母(不要破图图标)

绝对不要:
- 人物用方形头像(方形是物体/品牌用)
- 用占位脸 emoji(👤)——用首字母
- 省略状态点边框(会消失进头像)
- "+N" 不带数字(光一个 "+" 没意义)
- 让破图图标出现(回退到首字母)
```

## Tailwind classes

```tsx
// avatar with status dot
<div className="relative inline-block size-8">
  <img src={user.avatar} alt={user.name} className="size-8 rounded-full object-cover ring-2 ring-[--color-bg-surface]" />
  {user.online && (
    <span className="absolute bottom-0 right-0 size-2.5 rounded-full bg-[--color-success] ring-2 ring-[--color-bg-surface]" />
  )}
</div>

// initials fallback
<div className="flex size-8 items-center justify-center rounded-full bg-[--color-bg-muted] text-sm font-medium text-[--color-text-secondary]">
  {initials}
</div>

// avatar group
<div className="flex -space-x-2">
  {visible.map(u => <img key={u.id} src={u.avatar} className="size-8 rounded-full object-cover ring-2 ring-[--color-bg-surface]" />)}
  {overflow > 0 && (
    <div className="flex size-8 items-center justify-center rounded-full bg-[--color-bg-muted] text-xs font-medium text-[--color-text-secondary] ring-2 ring-[--color-bg-surface]">
      +{overflow}
    </div>
  )}
</div>
```

## Reverse examples

| Aspect | Plastic | Human |
| --- | --- | --- |
| shape | square or inconsistent | always circle for people |
| no image | broken icon or 👤 emoji | initials fallback |
| status dot | missing or borderless | sized + 2px bg border |
| group overflow | shows all (cluttered) | max 4 + "+N" pill |
| group border | none (merge together) | 2px bg border on each |
| loading | bare spinner | skeleton pulse matching shape |

## Composes with

- `badge.md` — status dot reuses badge colors
- `table-row.md` — assignee column (24px sm)
- `nav-sidebar.md` — user menu trigger (32px md)

## Failure modes

| Failure | Fix |
| --- | --- |
| square avatars | rounded-full |
| broken image icon | initials fallback |
| borderless status dot | 2px ring in bg color |
| cluttered group | cap at 4 + "+N" |
| merged group | 2px ring on each |
