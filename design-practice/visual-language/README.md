# Visual Language — 风格 DNA 层(皮肤 + 手感 + 气质)

> 这是 skill 从"骨架"升级到"骨架+皮肤+手感+气质"的层。`components/` 冻结了组件尺寸(骨架),`visual-language/` 冻结了**视觉决策**(配色策略、阴影阶梯、字体配对、字重、tracking、动效曲线、图标体系)。
>
> 没有这一层,生成出来还是塑料——光知道按钮 36px 高,不知道什么时候用 luminance stacking(Linear 深色)、什么时候用 mesh gradient hero(Stripe 营销)、什么时候用 cream 背景(Notion 温暖反流派)。视觉语言层回答:**这个产品该长什么样、摸起来什么手感、传达什么气质**。

## 通用配色铁律(所有风格共享,先于风格选择生效)

> 出处:原文第二编第一章(行 336-352)。这条铁律**先于**风格路由——无论最终选 Linear / Stripe / Notion / Vercel,这条都成立。它是 AI 最容易翻车的"满屏 accent 滥用 / 五颜六色彩虹页 / 状态色错位"的根因。

一句话总纲(原文行 352):
> **大面积中性灰托底,小面积主色点睛,状态色各司其职,一切走语义令牌,所有文字守对比度。**

五条章法:

1. **一套中性灰托底**——界面高级感七成来自灰阶稳定。canvas / surface / surface-2 / border / text-primary / text-secondary / text-tertiary 必须形成稳定的明度阶梯。Stripe 文档页是教科书:大面积白灰黑中性色,主色只在链接/重点/关键行动上(原文行 306)。
2. **一个主色点睛**——主色要省着用,只用在三个地方:**主按钮 / 当前选中态 / 链接**。满屏主色 = 没主色。Linear 是教科书:大量灰阶暗色 + 弱边框,主色用得很省(原文行 308)。
3. **一组状态色守规矩**——成功用绿、警告用黄、危险用红、信息用蓝。**不要把删除做成绿色,不要把成功做成红色**。状态色不参与"好看",只参与"说话"。
4. **强色小面积用**——强色像辣椒,少放提味,多放毁菜。高饱和色(包括主色的高饱和变体、品牌渐变)只能小面积点缀(图标、徽章、高亮、重点描边),**绝不铺满主区域**。
5. **渐变要有理由**——渐变不是装饰,是引导。只在两种情况下用:(a) 品牌核心叙事区(Stripe hero、Vercel logo wall);(b) 需要建立视觉焦点(主 CTA 的微渐变、状态指示)。**正文区、列表区、表格区不得有渐变**。

### 违反这条铁律的塑料信号(AI 产物最常翻车点)

| 塑料信号 | 违反了哪一条 | 修正 |
|---|---|---|
| 整页所有 accent 都是 violet(或任何单一高饱和色) | 2 主色点睛(变成了"主色铺满") | 主色只保留在主按钮/选中/链接,其余降级为中性灰 |
| 删除按钮是绿色、成功 toast 是红色 | 3 状态色守规矩 | 删除=danger 红、成功=success 绿,不可错位 |
| 卡片背景、表单背景、导航背景都有渐变 | 5 渐变要有理由 | 渐变只留给 hero/品牌叙事区 |
| 五六级灰阶明度差 < 5%,看着像只有两档 | 1 中性灰托底 | 拉开明度差,每档至少差 8-10% |
| 配色没有语义层,全是 primitive 原色值 | 总纲"走语义令牌" | 必须有 semantic layer(border.default / text.secondary...) |

### 这条铁律和各风格文件的关系

各 `style-*.md` 冻结的是**这个风格如何执行这五条**(Linear 用 luminance stacking 托底、Stripe 用白底 + 单紫点睛、Notion 用 cream 托底 + 黑色 CTA、Vercel 用纯黑托底 + 单饱和 accent)。**先读本节铁律,再读风格文件**——风格文件是铁律的具体实例,不是替代品。


## 为什么需要这一层

Sun 第四轮命门(2026-06-27):"你调研的那些优秀网站的事例,还有那些优秀的设计网站,然后等等这些。而且你网站不光是组件啊,还有图呢,还有视觉方面的东西呢。你这些到底是怎么约束的呢?如果你不这样做,你怎么给用户生成组件的图呢和建议呢?"

——只给组件尺寸,不给视觉语言,等于给了一把砖头不给图纸。这一层就是图纸。

## 怎么用

1. 用户说"做个 X",先读 `references/intent-reading.md` 推断 goal/audience/tone。
2. 用下面的**风格 DNA 选择器**,把 intent 路由到一个风格家族。
3. 打开对应 `style-*.md` 文件,把里面的完整 token 集(配色/阴影/字体/动效/图标库)冻结进提示词。
4. 把 `components/` 的组件规格套上这套视觉 token,生成出来的就是"那个风格的、有手感的、人做的"界面,而不是塑料。

## 风格 DNA 选择器(意图 → 风格路由表)

| 用户意图 / 产品类型 | 推荐风格 | 为什么 | 绑定图标库 |
|---|---|---|---|
| **开发者工具 / 项目管理 / 高效生产力**(Linear、Vercel、Raycast 系) | `style-linear.md` | 深色优先、近黑画布、单色 accent、Inter var 510、luminance stacking——传达"严肃工程工具"气质 | Lucide |
| **支付 / 金融 / SaaS 营销落地页**(Stripe 系) | `style-stripe.md` | 白底 + sohne-var 300 字重 + 单紫 accent + 渐变 mesh hero——传达"可信金融科技 + 编辑式高级感" | Heroicons |
| **知识管理 / 协作 / 教育 / 消费者**(Notion、Anthropic、PostHog 系) | `style-notion.md` | 奶油底 + serif 标题 + 手绘插画 + 暖色调——温暖反流派,传达"亲和 + 人味 + 不冰冷" | Phosphor Duotone |
| **极客 / hosting / 开发平台营销**(Vercel、Supabase 系) | `style-vercel.md` | 纯黑 #000 + 几何点纹 + bento grid + 一个饱和 accent——传达"前沿 + 极客 + 高对比" | Lucide 或自定 |
| **企业后台 / 数据密集 / 仪表盘**(无特定品牌诉求) | `style-linear.md` 的浅色变体 | 数据密度优先,中性灰 + 克制语义色,避免营销气质 | Lucide |

**当用户没指定风格时,默认 `style-linear.md`**——它是 2026 年事实上的 SaaS 视觉公约(70% 新 B2B SaaS 采用),也是 skill 最深冻结的一家。

## 风格 DNA 是什么(每个 style-*.md 都冻结这 9 层)

每个风格文件按统一结构冻结 9 层视觉决策:

```text
1. 配色策略(canvas / surface ladder / accent / 语义色 / 中性色阶)
2. 字体系统(family / weight / progressive tracking / mono 配对)
3. 圆角阶梯(每家不一样,Linear 是 6/12,Stripe 是 4,Notion 是 4/8)
4. 阴影 / elevation 哲学(Linear 是 luminance stacking,Stripe 是多层款,Vercel 是几乎无)
5. 间距气质(4px 网格但每个风格用得不一样——Linear 紧、Notion 松)
6. 动效曲线(duration 阶梯 + easing 函数 + 禁用曲线)
7. 图标体系(绑定一个图标库,严禁混用)
8. 反塑料证据(这个风格的"人做的"信号是什么)
9. 反派警示(这个风格最容易塌成什么塑料样)
```

## 4px 网格(所有风格共享的通用常量)

不论选哪个风格,这条铁律不变——所有尺寸是 4 的倍数(半步 4/8/12/16/20/24/32/40/48/64/80/96...)。这是 Tailwind v4 默认、Linear 基础、Material 3 基础。**离格值(13px、17px、22px)是失败信号**。

```text
spacing scale:
  1 = 4px    2 = 8px    3 = 12px   4 = 16px   5 = 20px
  6 = 24px   8 = 32px   10 = 40px  12 = 48px  16 = 64px
  20 = 80px  24 = 96px  32 = 128px
```

## Z-index 公约(所有风格共享)

```text
  z-base      = 0     默认内容
  z-raised    = 1     抬升卡片
  z-dropdown  = 10    下拉、右键菜单
  z-sticky    = 50    sticky nav、表头
  z-overlay   = 60    模态遮罩
  z-modal     = 70    模态内容
  z-popover   = 80    popover、tooltip
  z-toast     = 90    toast 通知
  z-top       = 100   skip-to-content、关键覆盖层
```

## 反塑料的视觉证据(跨所有风格)

不论选哪个风格,这些"人做的"信号都成立:

- **6 级 elevation** 而不是一层 box-shadow 打天下
- **focus ring 双层 box-shadow**(不是单层 outline)
- **pressed scale**(0.97-0.98 按下手感)
- **progressive tracking**(大字紧、小字松,不是统一 0)
- **图标单一库**(不是 Lucide + Heroicons 混用)
- **动效有曲线**(不是 ease 或 linear 蛮力)

## 文件清单

| 文件 | 风格 | 何时用 |
|---|---|---|
| `style-linear.md` | Linear 风(深色优先) | 开发者工具、项目管理、高效生产力——**默认** |
| `style-stripe.md` | Stripe 风(白底编辑式) | 支付、金融、SaaS 营销落地页 |
| `style-notion.md` | Notion 风(温暖反流派) | 知识管理、协作、教育、消费者 |
| `style-vercel.md` | Vercel 风(极客纯黑) | 开发平台、hosting、极客营销 |
| `icon-systems.md` | 图标库选型 + 混用反例 | 所有风格都绑一个图标库 |

## 权威信源(每家风格文件标注来源)

- **Linear**:designmd.cc/benchmarks/linear + soulcore-dev/soul-design-md(line 1122 行完整 DESIGN.md)+ styles.refero.design + designlang.app
- **Stripe**:designmd.cc/benchmarks/stripe + duply.ai/stripe + stripe.design + styles.refero.design
- **Notion**:designmd.cc + styleextract.com + refero.styles(待补深采)
- **Vercel**:welovedaily.net Vercel aesthetic + brainy.ink 同质化分析
- **图标库**:Lucide/Heroicons/Phosphor/Tabler 官方 + pkgpulse.com + allsvgicons.com + auditbuffet.com(混用反例)
- **趋势 2026**:brainy.ink 同质化警告 + toimi.pro SaaS 设计趋势 + ui-ux-suite 趋势表
