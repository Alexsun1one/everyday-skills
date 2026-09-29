# 图标系统选型表 — 4 大主流图标库 + 混用反例

> 图标系统是反塑料的**第二关键**层(第一是字体)。一个界面如果同时出现 Lucide(2px stroke 几何)+ Phosphor Duotone(双层填色手绘感)+ Material Symbols(填充流线),就是业余军混搭——三种不同的 stroke 宽度、不同的网格、不同的视觉重量、不同的圆角哲学,在一屏内看起来就是"东拼西凑的塑料样"。
>
> 这一页冻结:每个图标库的气质、笔画、覆盖度、适用场景,以及与 4 个风格 DNA 的强制绑定。

## 黄金铁律

> **一个产品只用一个图标库。** 没有例外。
>
> 如果选定的库没有需要的图标,**自定 SVG 匹配那个库的风格**(24×24 viewBox、相同 stroke 宽度、相同 line-cap 风格),**不要**引入第二个库"救场"。

## 4 大图标库对照表

| 维度 | **Lucide** | **Heroicons** | **Phosphor** | **Tabler Icons** |
|---|---|---|---|---|
| **气质** | 几何精确、工程感、克制 | Tailwind 团队官方、clean、line-based | 手绘感、温暖、Duotone 独特 | 精细、庞大、几何 + 装饰平衡 |
| **笔画 stroke** | 2px | 1.5px(outline)/ solid | 多 weight(Thin/Light/Regular/Bold/Fill/Duotone)| 2px |
| **viewBox** | 24×24 | 24×24 | 24×24 | 24×24 |
| **line-cap** | round | round | round | round |
| **图标数** | 1500+(2026)| 292(outline + solid 各一半)| 9000+(6 weights 每个都有) | 5800+ |
| **License** | MIT | MIT | MIT | MIT |
| **维护活跃** | 极高(Feather 的 fork,持续更新)| 高(Tailwind 团队官方)| 极高 | 高 |
| **React/Vue 包** | lucide-react / lucide-vue-next | @heroicons/react | @phosphor-icons/react | @tabler/icons-react |
| **Tree-shake** | 优秀 | 优秀 | 优秀 | 优秀 |
| **填充变体** | 无(纯 outline)| outline + solid 两套 | Thin/Light/Regular/Bold/Fill/Duotone 六档 | 无(纯 outline)|

## 气质路由表(产品类型 → 图标库)

| 产品类型 / 风格 DNA | 推荐图标库 | 为什么 |
|---|---|---|
| **Linear 风**(深色工程工具、开发者)| **Lucide** | 2px stroke + 几何精确 + 工程感,完美匹配 Linear 的"严肃工具"气质 |
| **Stripe 风**(白底编辑式、金融)| **Heroicons** | 1.5px 更细更克制,匹配 Stripe 的 whisper-authority;深度绑定 Tailwind 生态 |
| **Notion 风**(温暖反流派、知识协作)| **Phosphor Duotone** | 双层填色手绘感,匹配 Notion 的纸感亲和;Regular 用于 nav |
| **Vercel 风**(极客纯黑)| **Lucide** | 2px stroke 几何精确,匹配 Vercel 的极客极致 |
| **Material You 产品**(安卓原生)| **Material Symbols** | Google 官方,如果产品明确是 Material 体系,用这个 |
| **企业后台 / 数据密集 dashboard** | **Lucide** | 工程感 + 大覆盖(1500+),最通用 |
| **iOS / Apple HIG 产品** | **SF Symbols** | Apple 官方,如果是原生 iOS App 用这个 |

## 为什么不混用 —— 视觉证据

### 同一按钮里混 Lucide + Phosphor(典型事故)

```text
按钮: [Lucide Settings icon 2px stroke] Settings
按钮: [Phosphor Duotone Plus icon] Add item
```

看起来是塑料,因为:
- Lucide 是 2px stroke、几何精确、空灵
- Phosphor Duotone 是双层填色、手绘感、有重量
- 同屏出现两种"视觉重量语言",眼睛瞬间识别为"东拼西凑"

### 同一 nav 里混 Lucide + Heroicons

```text
nav: [Lucide Home 2px] Home
nav: [Heroicons ChartPie 1.5px] Analytics
```

看起来是塑料,因为:
- 1.5px stroke 比 2px stroke 视觉上细 25%
- 同一 nav 高度内,有的 icon 看起来"重"、有的"轻"
- 视觉重心不齐 = 业余信号

## 如何自定 SVG 匹配库风格

当你的选定库缺一个图标,不要换库,自定 SVG:

### Lucide 风(2px stroke 几何)

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none"
     stroke="currentColor" stroke-width="2"
     stroke-linecap="round" stroke-linejoin="round">
  <!-- 你的 path -->
</svg>
```

### Heroicons 风(1.5px stroke outline)

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none"
     stroke="currentColor" stroke-width="1.5"
     stroke-linecap="round" stroke-linejoin="round">
  <!-- 你的 path -->
</svg>
```

### Phosphor 风(选一个 weight 后匹配)

```svg
<!-- Regular weight -->
<svg width="24" height="24" viewBox="0 0 256 256" fill="none"
     stroke="currentColor" stroke-width="16"
     stroke-linecap="round" stroke-linejoin="round">
  <!-- 你的 path -->
</svg>
```

> **注意 Phosphor 是 256 viewBox**(不是 24),stroke 是 16(不是 2)——这是它的坐标系。

## 图标尺寸规范(跨所有库)

| 场景 | 尺寸 | Tailwind | 用途 |
|---|---|---|---|
| button icon | 16px | `size-4` | 按钮内 icon |
| inline input icon | 16px | `size-4` | 输入框前后 icon |
| nav icon | 18-20px | `size-[18px]` / `size-5` | 侧栏 / 顶栏导航 |
| table row action | 16px | `size-4` | 表格行操作(行 hover 时淡入) |
| toolbar icon | 20px | `size-5` | 工具栏 |
| feature card icon | 24px | `size-6` | bento card / feature 区块 icon |
| hero / large | 32-48px | `size-8` / `size-12` | 大型 hero 装饰 |

## 图标颜色规范(跨所有库)

| 场景 | 颜色 |
|---|---|
| 默认 | `currentColor`(继承文字色) |
| primary CTA 内 | `#FFFFFF`(on accent fill) |
| secondary button 内 | `color.text.primary` |
| ghost icon button | `color.text.secondary`(hover → primary) |
| nav active | accent 色 |
| nav inactive | `color.text.tertiary` |
| danger action | `color.danger` |
| success state | `color.success` |

## 反塑料证据(图标层)

- [ ] **整页只有一个图标库**(grep import 检查)
- [ ] **stroke 宽度一致**(2px 全场,或 1.5px 全场,不混)
- [ ] **line-cap / line-join 都是 round**(检查 SVG attributes)
- [ ] **viewBox 一致**(24×24 全场,不混 24/256)
- [ ] **icon 尺寸阶梯**(只用 16/20/24,不用 14/17/22 离格值)
- [ ] **颜色用 currentColor**(不硬编码 fill)
- [ ] **没有 emoji 替代 icon**(除非 Notion 风的"页面 icon"特殊场景)
- [ ] **没有填充和描边混用**(Lucide 全描边,Phosphor 选定一个 weight 后一致)

## AI 验收员提示词(图标层检查)

```text
审查这个 UI 的图标系统。检查:

1. 是否只使用了一个图标库?(列出所有 import 的图标库)
2. stroke 宽度是否全场一致?(预期 2px 或 1.5px,不混)
3. line-cap 和 line-join 是否都是 round?
4. viewBox 是否全场一致?(24×24 或 256×256,不混)
5. icon 尺寸是否使用阶梯值?(16/20/24,不是 14/17/22)
6. 颜色是否用 currentColor?(不是硬编码 fill)
7. 是否有 emoji 替代功能 icon?(只在 Notion 风的"页面 icon"允许)
8. 是否有描边和填充混用?(同一界面 outline 和 solid 混)

每条都要打勾。任何一条失败都是塑料信号,需要修复。
```

## 权威信源

- **Lucide**:lucide.dev(官方)+ github.com/lucide-icons/lucide + pkgpulse 2026 评估
- **Heroicons**:heroicons.com + github.com/tailwindlabs/heroicons
- **Phosphor**:phosphoricons.com + github.com/phosphor-icons/web
- **Tabler Icons**:tabler.io/icons + github.com/tabler/tabler-icons
- **混用反例**:auditbuffet.com "icon consistency audit" + allsvgicons.com 比较文章
- **覆盖率比较**:pkgpulse.com "React icon library comparison 2026"
