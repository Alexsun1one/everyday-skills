# 意图读心 — Intent Reading

> 在生成任何像素之前,先冻结用户的真实意图。**不做这一步,后面所有组件精度都白搭**——用户说"做个登录页",可能是 SaaS 后台登录、可能是消费者 App 登录、可能是营销活动的注册落地页,三者视觉决策完全不同。
>
> 这一页的职责:把模糊的"做个 X",翻译成精确的 Intent Brief——goal、audience、tone、风格 DNA 路由——再进 Stage 1 草稿生成。

## 三层意图模型

每次用户开口,要冻结三层:

```text
1. GOAL —— 这个页面/产品要达成什么业务目标?
2. AUDIENCE —— 给谁看?他们的语境、知识、情绪是什么?
3. TONE —— 要传达什么气质?(严肃/亲和/极客/温暖/... )
```

## 8 种 GOAL 分类

| Goal 类型 | 业务目标 | 典型页面 | 关键设计决策 |
|---|---|---|---|
| **转化 Acquisition** | 让用户做某个动作(注册/购买/订阅)| 营销落地页、Pricing、注册流 | 单 CTA、社会证据、稀缺性、friction 最小 |
| **激活 Activation** | 让新用户完成 onboarding 达到 aha moment | Welcome、引导流、空状态引导 | 进度条、skip 选项、空状态 CTA |
| **留存 Retention** | 让用户反复回来用核心功能 | Dashboard、Feed、Inbox、Home | 个性化、通知、新鲜感、流式内容 |
| **生产力 Productivity** | 让用户高效完成重复任务 | 项目管理、表格、编辑器、CRM | 密度高、键盘快捷键、批量操作、低延迟感 |
| **信息消费 Information** | 让用户高效阅读/查找内容 | 文档站、知识库、博客、搜索结果 | 可读性优先、目录、搜索、视觉层次 |
| **探索 Discovery** | 让用户发现新东西 | 推荐、Explore、Catalog、Marketplace | 卡片网格、视觉吸引、过滤器、个性化 |
| **支付 Transaction** | 让用户完成付款 | Checkout、订阅管理、发票 | 可信感、安全感、明确费用、错误防护 |
| **配置 Configuration** | 让管理员调整设置 | Settings、Admin、Permissions、Integrations | 表单清晰、即时反馈、destructive 防护 |

## 6 类 AUDIENCE 分类

| Audience 类型 | 知识水平 | 情绪 | 视觉决策 |
|---|---|---|---|
| **开发者 Developer** | 高(懂技术细节)| 理性、效率至上 | Linear/Vercel 风、深色、代码块、键盘提示 |
| **企业用户 Enterprise** | 中(懂业务流程)| 谨慎、看重可控 | Linear 风浅色、密集 dashboard、权限可见 |
| **SMB / 创业者** | 中(多任务一身)| 时间紧、看重效率 | Linear/Stripe 风、营销感+工具感平衡 |
| **消费者 Consumer** | 低(不懂技术)| 情绪化、易流失 | Notion 风温暖、大按钮、强引导、最少术语 |
| **专业用户 Pro(设计/写作/编辑)** | 高(懂审美)| 重美感、挑剔 | Notion 风、serif、留白、editorial |
| **管理员 Admin** | 高(懂系统)| 重精确、防错 | Linear 风密集、destructive 防护、即时反馈 |

## 5 类 TONE 分类

| Tone 类型 | 传达气质 | 视觉证据 |
|---|---|---|
| **严肃工程 Serious Engineering** | 精确、可靠、不浮夸 | Linear 风、深色、克制 accent、Inter/Geist、Lucide |
| **可信金融 Trustworthy Finance** | 安全、专业、有底蕴 | Stripe 风、白底、whisper-authority、sohne-var 300、Heroicons |
| **温暖亲和 Warm & Approachable** | 友好、不冰冷、像伙伴 | Notion 风、奶油、serif 标题、Phosphor Duotone、emoji |
| **极客前沿 Geek Frontier** | 前沿、高性能、为懂的人做 | Vercel 风、纯黑、bento、几何点纹、Lucide |
| **优雅奢华 Elegant Luxury** | 高端、克制、不讨好 | 大留白、serif、单色 + 金属 accent、极少元素 |

## 形容词 → 决策翻译表

用户常用模糊形容词,每个都要翻译成具体视觉决策:

| 用户形容词 | 翻译成 | 视觉决策 |
|---|---|---|
| "现代" | Linear/Vercel 风 | 深色、几何、克制 accent、Inter/Geist |
| "专业" | Stripe 风白底 | sohne-var 300、单紫 accent、平面无 shadow |
| "高端" | Elegant Luxury | 大留白、serif、单色 + 金属、最少元素 |
| "亲和" | Notion 风 | 奶油、Phosphor Duotone、emoji、温暖橙 |
| "极客" | Vercel 风 | 纯黑、bento、几何点纹、Lucide |
| "简洁" | 减法 | 单 accent、4px 网格、少元素、Linear 风 |
| "活泼" | 多 accent(克制)| 每屏一个饱和 accent、圆角、轻动效 |
| "高效" | Productivity goal | 密度高、键盘提示、批量操作、Linear 风 |
| "可信" | Stripe 风 + 证据 | logo strip、case study、testimonial、平面 |
| "未来感" | Vercel 风 + gradient | 几何点纹、蓝紫 gradient、bento、纯黑 |
| "温暖" | Notion 风 | 奶油、serif、Phosphor Duotone、暖色 accent |
| "奢华" | Elegant Luxury | 大留白、serif、金属 accent、最少 CTA |
| "数据密集" | Linear 浅色风 | 紧表格、密 row、键盘导航、minimal padding |

## Intent Brief 模板(必填)

每次开始 Stage 1 之前,先填这个表(可以问用户,也可以从他的描述推断,但要让他确认):

```markdown
## Intent Brief

### 1. GOAL(业务目标)
- 类型:[转化 / 激活 / 留存 / 生产力 / 信息消费 / 探索 / 支付 / 配置]
- 核心动作(用户要做什么):[一句话]
- 次要动作(可接受的备选):[一句话,或"无"]

### 2. AUDIENCE(受众)
- 类型:[开发者 / 企业用户 / SMB / 消费者 / 专业用户 / 管理员]
- 知识水平:[高 / 中 / 低]
- 进入页面的情绪:[理性 / 紧迫 / 情绪化 / 谨慎 / 挑剔]
- 母语 / i18n:[中文 / 英文 / 双语]

### 3. TONE(气质)
- 主气质:[严肃工程 / 可信金融 / 温暖亲和 / 极客前沿 / 优雅奢华]
- 关键词(用户用的形容词):[列出]
- 反向气质(不要的感觉):[列出]

### 4. 风格 DNA 路由
- 推荐:[style-linear / stripe / notion / vercel]
- 备选:[次选]
- 理由:[一句话]

### 5. 关键约束
- 暗色 / 亮色:[默认 / 必须]
- 移动端优先 / 桌面优先:[默认]
- 品牌色:[用户提供,或继承风格 DNA 默认]
- 字体限制:[用户提供,或继承风格 DNA 默认]

### 6. 反塑料锚点(让产物不像 AI)
- 这个产品的"人做的"信号是什么?[1-3 条]
- 例如:weight 510、focus 双环、progressive tracking、trailing arrow、block 流...
```

## 意图推断流程(从模糊到精确)

```text
Step 1. 解析用户的原始描述
   ├─ 提取名词(做什么)→ 候选 GOAL
   ├─ 提取形容词(什么感觉)→ 候选 TONE
   └─ 提取上下文(给谁、为什么)→ 候选 AUDIENCE

Step 2. 路由到风格 DNA
   ├─ 如果用户明确说"像 Linear/Stripe/Notion/Vercel",直接走那个
   ├─ 如果用户说形容词,查"形容词→决策翻译表"
   └─ 如果用户没说,默认 style-linear(它是 2026 SaaS 公约)

Step 3. 反向验证
   ├─ 用推断的 Intent Brief 反推用户描述
   ├─ 如果一致,直接进 Stage 1
   └─ 如果不一致或有歧义,把 Intent Brief 给用户确认

Step 4. 生成 Intent Brief
   ├─ 填上面 6 个字段
   ├─ 用户确认或调整
   └─ 进入 Stage 1 草稿生成
```

## 常见意图误读警示

| 用户说 | 错误推断 | 正确推断 |
|---|---|---|
| "做个登录页" | 通用登录表单 | 必须问:SaaS 后台?消费者 App?营销注册?——三者完全不同 |
| "做个 dashboard" | 通用图表 dashboard | 必须问:数据密集?营销 overview?管理员配置?——三者完全不同 |
| "简洁" | Linear 深色 | 可能是 Stripe 白底(也简洁)。必须问:深色还是浅色? |
| "活泼" | 多色 + emoji | 可能是 Vercel 的彩色 bento(也活泼)。必须问:给谁? |
| "高端" | 加金色 + 渐变 | 高端是减法,不是加法。用 Elegant Luxury:大留白 + serif + 单色 |

## 风格冲突解决规则(关键)

用户说的风格和 intent 推断的风格**冲突时**,按这张表解决:

| 用户说 | intent 推断 | 冲突 | 解决 |
|---|---|---|---|
| "Linear 风的支付页" | Linear(开发者)+ Stripe(支付)| Linear 暗色工程感 vs Stripe 白底可信感 | **优先 intent 的 goal**:支付场景 → Stripe 风白底,**保留** Linear 的某些克制(单 accent、几何感)做调和 |
| "Notion 风的 dashboard" | Notion(温暖)+ Linear(dashboard)| Notion block 流 vs Linear 表格密集 | **优先 intent 的 goal**:dashboard 数据密集 → Linear 表格风,**保留** Notion 的温暖色温(浅奶油色背景、圆角偏柔) |
| "Vercel 风的知识管理" | Vercel(极客)+ Notion(知识)| Vercel 纯黑 vs Notion 奶油 | **优先 audience**:知识管理常给非工程师 → Notion 奶油温暖,**保留** Vercel 的 bento 网格布局做现代感 |
| "Stripe 风的极客工具" | Stripe(可信)+ Vercel(极客)| Stripe 编辑式 vs Vercel 几何点纹 | **优先 audience**:极客给开发者 → Vercel 纯黑 bento,**保留** Stripe 的 gradient text headline 做签名 |
| "中文产品但想要 Linear 风" | 中文 SaaS + Linear | Linear 暗色工程 vs 中文本土亲切 | **优先 audience**:中文受众 → style-chinese-saas(亮色 + 微信绿/知乎蓝),**保留** Linear 的某些克制(单 accent、密集信息) |

**通用规则**:**audience 和 goal 优先于用户的形容词**。用户说"Linear 风"可能只是想要"专业感"——如果 audience 是消费者,应该用 Notion/中文 SaaS 温暖 + Linear 的某些克制(单 accent),而不是死套 Linear 暗色工程感。

**冲突时必须主动提示用户**:"你说 Linear 风的支付页,但支付场景适合 Stripe 白底可信感。我可以:(A) 用 Stripe 白底 + Linear 单紫 accent;(B) 用 Linear 深色但加 Stripe 式的 gradient text headline;(C) 你真的要 Linear 深色 + 支付?选哪个?"

## 完整 Intent Brief 示例(填法参考)

### 示例 1:任务管理页(开发者向)

```markdown
## Intent Brief

### 1. GOAL
- 类型:生产力(Productivity)
- 核心动作:用户创建/分配/跟踪任务,从 todo 到 done
- 次要动作:评论、附件、@通知

### 2. AUDIENCE
- 类型:开发者 + SMB
- 知识水平:高
- 进入情绪:理性、效率至上,讨厌多余装饰
- 母语:中文(双语界面)

### 3. TONE
- 主气质:严肃工程(Serious Engineering)
- 关键词:"高效"、"专业"、"键盘驱动"
- 反向气质:不要"营销感"、"卡通"、"花哨"

### 4. 风格 DNA 路由
- 推荐:style-linear(开发者 + 生产力 + 严肃工程 = Linear 默认)
- 备选:无(用户明确要高效专业)
- 理由:开发者向 + 生产力 = Linear 的舒适区

### 5. 关键约束
- 暗色 / 亮色:默认暗色(开发者偏好)
- 移动端优先 / 桌面优先:桌面优先(任务管理是桌面操作)
- 品牌色:用户未指定,继承 Linear violet #5E6AD2
- 字体限制:用户未指定,继承 Inter var + cv01 + ss03

### 6. 反塑料锚点
- weight 510(不是 500/600)
- focus 双层 box-shadow
- progressive tracking
- luminance stacking(暗色模式抬升靠提亮表面)
- pressed scale 0.98
```

### 示例 2:中文 SaaS 官网首页(消费者向)

```markdown
## Intent Brief

### 1. GOAL
- 类型:转化(Acquisition)+ 探索(Discovery)
- 核心动作:访客了解产品 → 注册试用
- 次要动作:看案例、查价格、联系销售

### 2. AUDIENCE
- 类型:SMB 创业者 + 企业用户
- 知识水平:中
- 进入情绪:时间紧、看重效率、要本土亲切感
- 母语:中文

### 3. TONE
- 主气质:温暖亲和 + 严肃工程混合(本土 SaaS 气质)
- 关键词:"专业"、"亲切"、"本土"、"高效"
- 反向气质:不要"海外翻译感"、"冰冷工程"、"花哨营销"

### 4. 风格 DNA 路由
- 推荐:**style-chinese-saas**(中文受众 = 本土亲切感必需)
- 备选:style-stripe(如果产品定位高端 B2B)
- 理由:中文 SMB 受众 → 西方风格(Linear/Stripe/Notion/Vercel)会显得"像海外的",失去本土亲切

### 5. 关键约束
- 暗色 / 亮色:亮色(中文 SaaS 主流亮色)
- 移动端优先 / 桌面优先:桌面 + 移动并重(中文用户大量移动端)
- 品牌色:微信绿 #07C160 或飞书青 #1456F0(用户选)
- 字体限制:PingFang SC 第一栈(绝不用 Inter 主导)

### 6. 反塑料锚点
- PingFang SC 第一栈(不是 Inter)
- line-height 1.7-1.8(不是 1.5)
- 中英混排加空格
- 圆角 8-12px(不是 6px)
- icon 带彩色背景圆(不是裸 Lucide)
- 品牌色饱和(不是 Linear 紫)
```

### 示例 3:空 Intent Brief(错误示范)

```markdown
## Intent Brief(空 — 错误示范)

### 1. GOAL
- 类型:??(没问是阅读还是写作)

### 2. AUDIENCE
- 类型:??(没问是个人用还是团队用)

### 3. TONE
- 主气质:??(只说"Notion 风")

### 4. 风格 DNA 路由
- 推荐:??(直接套 Notion 是错的 — 必须先问 audience)

→ 这个 Intent Brief 不合格,**必须回 Task Card 问清楚**:
  - 是个人笔记还是团队知识库?
  - 主要用来读还是写?
  - 给工程师还是给非工程师?
  - 然后**才能**定 style-notion
```

## 与 SKILL.md 的关系

SKILL.md 的"Stage 1 入口"必须先调用这一页做意图读心,**再**进 Anti-Plastic Test 和 Five-Layer Blade。否则后面 Five-Layer 推得再深,风格 DNA 选错,产出还是塑料。

## 与 variation-engine.md 的关系

Intent Brief 的"invariants(不可变)"部分就是 variation-engine 的语义不变量——无论生成几个变体,GOAL/AUDIENCE/TONE 不能变,变的只是视觉 surface。

## 权威信源

- lego-town/SKILL.md 的 "Intent Reading" 章节(用户旗舰 skill 标准)
- "Designing for the User's Task" — Don Norman《设计心理学》
- "Goal-Directed Design" — Alan Cooper《About Face》
- "Jobs to Be Done" — Clayton Christensen
