---
type: demo-stage0
created: 2026-06-27
demo: demo-crm-v2.html
source: 严格走 design-judgment/01-05 + patterns/01-list-detail
---

# CRM Demo v2 — Stage 0 五张判断卡 + list-detail 模式卡

> 这张卡是 v2 的设计依据。每条判断都直接对应到 v2 的具体设计决策。**v1 翻车的根因 = 这张卡没填。**

## Intent Brief

```text
- GOAL: 生产力（销售团队高速处理客户）
- AUDIENCE: 企业用户（销售经理 + 销售员,桌面端为主,每天 8 小时用）
- TONE: 严肃工程（不是营销页,不是消费 App,是 Linear/Vercel 系生产力工具）
- 风格 DNA 路由: style-linear（深色优先 + luminance stacking + 单色 accent）
- 反向气质: 不要营销感、不要喜庆、不要装饰渐变、不要五颜六色
- 反塑料锚点:
  1. 关闭详情抽屉后,列表滚动位置必须保留（坐标感核心）
  2. 销售阶段（Lead/Qualified/Proposal/Won/Lost）各有专属状态色,不混用 violet
  3. 销售看的是数字（金额、转化率）,关键数字大且字重 700,辅助信息小且浅灰
```

## Anti-Plastic Test

```text
- user: 销售经理（张磊式人物）,桌面端,在月底冲业绩,心情急,要快速找出该跟的客户
- core task: 看客户列表 → 筛选该跟的 → 打开详情 → 改阶段/记活动/设下次跟进 → 关闭回列表
- success criteria:
  · 5 秒内知道本页是"客户列表"
  · 一次点击进入详情,关闭后列表不动
  · 改阶段不丢活动记录
  · 失败重试不丢内容
- non-goals: 本轮不做报表/预测/AI 摘要/邮件营销/合同生成
- states that can break:
  · loading: 列表骨架（行骨架匹配行结构）
  · empty-initial: 新销售,还没有客户
  · empty-filter: 筛选无匹配（如筛选 Lost 但没有）
  · empty-permission: viewer 看不到别人客户
  · error: 网络断,改阶段没生效
  · offline: 顶部 banner,修改暂存
  · repeat-click: 改阶段防重复
- one primary action per screen: yes（列表页主按钮 = "新建客户";详情页主按钮 = "保存"）
- data objects & lifecycle: 客户（lead→qualified→proposal→won/lost→archived）
- permission roles: viewer（只看自己）/ editor（改自己客户）/ admin（改所有人+删）
- what breaks if AI just generates a pretty screenshot:
  · viewer 会看到"新建客户"按钮,点了 403
  · 网络断改阶段没生效,但 UI 显示成功
  · 关闭详情后列表回顶部,销售找不到刚看的位置
  · Lost 客户用绿色 badge（状态色错位）
- forbidden drift: 不要装饰渐变、不要所有 badge 都 violet、不要列表项和卡片同时可点
```

## Card 0 — 任务场（design-judgment/01）

```text
□ 用户主任务（动词开头）: 跟进客户（看-筛-改-记-设下次）
□ 用户第一秒应该感知到:
  · 这是"全部客户"列表（标题 + count + 总金额）
  · 哪些客户"该跟"（本周到期、未联系超 7 天的视觉提醒）
  · 我能从哪开始（⌘K / 搜索框 / 主按钮"新建客户"）
□ 用户路径图:
  进入列表 → 第一眼看到"128 客户 / 总价值" → 扫表找到该跟的 →
  点行打开右侧抽屉 → 改阶段/记活动 → 保存 → 抽屉关闭 →
  列表还在原位 → 继续下一个客户
□ 出口: 完成本轮跟进（关 tab）/ 切到具体客户深度处理（点客户名进独立详情页）
```

## Card 1 — 复杂度归谁（design-judgment/02）

```text
□ 复杂度归系统:
  · 阶段切换（自动记录活动,不让销售手填活动日志）
  · 时区/货币（系统统一,不让销售选）
  · 重复检测（系统提示,不让销售手动查）
□ 复杂度归用户:
  · 跟进策略（哪些客户优先,销售判断）
  · 沟通内容（具体话术,销售写）
□ 复杂度归团队:
  · 阶段定义（团队统一定义 Lead/Qualified/Proposal/Won/Lost 标准）
  · 权限模型（viewer/editor/admin 边界）
□ 复杂度归 AI（不本轮）:
  · 智能跟进建议（next round）
  · 客户健康度评分（next round）
□ 默认值清单:
  · 阶段默认 Lead（新建客户）
  · 负责人默认当前用户
  · 货币默认 CNY
  · 下次跟进默认 +3 天
```

## Card 2 — 真简 vs 空简（design-judgment/03）

```text
□ 这是真简还是空简: 真简
  · 表面简:一屏一个主按钮、列表密度高、灰阶托底
  · 背后全:8 态按钮 + 5 态数据 + 权限矩阵 + 协作 cursor + 历史活动时间轴
□ 5 个异常都想全了吗:
  · 网络断:顶部 banner 持续 + 修改暂存
  · 权限不足:viewer 看不到别人客户 + "新建客户" disabled + tooltip
  · 删除二次确认:Lost 不是真删,真删进归档（软删 30 天恢复）
  · 长客户名:截断 + tooltip 全名（不换行）
  · 重复客户:系统检测 + 提示"已存在类似客户,是否合并"
```

## Card 3 — 视觉层级（design-judgment/04，★ demo v1 翻车主因）

```text
□ 层级三问:
  · 第一眼看什么: 标题"全部客户" + count（最大、字重 700、深色）
  · 第二眼看什么: 列表里的客户名（中等、字重 500、深色）+ 阶段 badge（彩色,信息性）
  · 可以不看什么: 元数据（邮箱、电话、地址,小、浅灰）

□ 视觉权重 5-3-2 分配:
  · 权重 5（第一眼,1 个）: 标题 + 总金额数字
    - 字号 28px,字重 700（不是 v1 的 590）
    - 金额用 tabular-nums,数字突出
  · 权重 3（第二眼,3-5 个）: 客户名、阶段 badge、负责人 avatar、本周到期标记
    - 客户名 14px 字重 500
    - 阶段 badge 各状态色（不是全 violet）
    - 本周到期 = 左侧 4px warning 色条（不是 badge）
  · 权重 2（背景,其余）: 表头、邮箱、地址、操作时间
    - 12-13px 字重 400 浅灰

□ v1 翻车对比:
  · v1: 所有标题 590 / 所有 accent violet / 没有 700 强对比层 → 一屋子人喊话
  · v2: 标题 700 / accent 只在主按钮和选中态 / 阶段色各司其职 → 有主次

□ 7 杠杆应用:
  · 大小:标题 28 > 客户名 14 > 元数据 12
  · 字重:标题 700 / 客户名 500 / 元数据 400（三档强对比）
  · 颜色:中性灰托底（80% 面积）+ 主色 violet 只在主按钮/选中（< 5% 面积）+ 阶段色只在 badge
  · 位置:主按钮右上、搜索顶部、列表中部、详情右抽屉
  · 留白:行间距 12px、表头 16px、区块间 24px
  · 分组:搜索+筛选 chip 一组 / 列表一组 / 详情抽屉独立
  · 对齐:表头/表格/搜索框左边界全部对齐（v1 没强调,v2 强制）
```

## Card 4 — 任务网络（CRM 不是单页,是网络）

```text
□ 3 个主任务:
  1. 跟进客户（列表→详情→改阶段）← 本 demo 主体
  2. 创建客户（主按钮→抽屉表单）
  3. 查看团队进度（sidebar 切到团队视图）
□ 任务网络图:
  入口:sidebar "全部客户" / ⌘K "搜索客户" / 顶部"新建客户"
  → 列表（默认状态）
    → 筛选（chip）→ 列表（filtered）
    → 点行 → 详情抽屉（不开新页）
      → 改阶段 → 自动记活动 → 抽屉保持
      → 保存 → toast → 抽屉关闭 → 列表（位置保留）★
    → 主按钮 → 新建抽屉
  出口:关闭 tab / 切其他 sidebar 项
□ 入口出口纪律:
  · 详情必须用抽屉,不用新页（保持列表上下文）
  · 关闭抽屉后列表 scrollTop 必须保留（反塑料锚点 #1）
  · 改阶段是高频,用 inline 切换,不开模态
```

## 模式卡 — list-detail（patterns/01）

```text
□ 主模式: list-detail
  · 列表（左/中）+ 详情（右抽屉,不开新页）
  · 列表项点击 → 详情打开,列表保持
  · 详情保存 → 列表更新该行（不重排,保持位置）
□ 列表密度: 高密度表格行（48px 行高,一屏 15-20 行）
□ 详情容器: 右侧抽屉 480px（不是全屏,不是模态）
  · 原因:CRM 详情是辅助,主任务在列表;抽屉保持列表可见
□ 坐标感 5 件套（反塑料锚点）:
  · 面包屑:不必要（两层结构,sidebar active 高亮足够）
  · 当前导航高亮:sidebar "全部客户" active
  · 清晰标题:抽屉顶部显示客户名（不是"客户详情"）
  · 返回逻辑:ESC / 点击遮罩 / 关闭 × → 回列表
  · ★ 列表滚动位置保留:关闭抽屉后,列表 scrollTop 不变（v1 没有,v2 必须）
□ 反模式自查:
  · 详情不开新页 ✓
  · 列表项整行可点 + 行内无 primary 按钮 ✓（只有 ghost icon）
  · 关闭抽屉后列表位置保留 ✓
  · 改阶段 inline,不开模态 ✓
```

## v2 设计决策（基于以上判断卡）

1. **字阶改成三档强对比**:标题 700/28px、客户名 500/14px、元数据 400/12px（v1 只有 590 一档,差）
2. **accent 严控面积**:violet 只用在 ① 主按钮"新建客户" ② 选中行 2px 左条 ③ focus ring。**阶段 badge 各状态色,不混 violet**（v1 全 violet）
3. **阶段状态色守规矩**:Lead=灰、Qualified=蓝、Proposal=琥珀、Won=绿、Lost=红（v1 用了 violet 给 Qualified,违反"状态色各司其职"）
4. **列表滚动位置保留**:点行开抽屉前记录 scrollTop,关闭后恢复（v1 没有）
5. **关键数字突出**:总金额用 tabular-nums + 700 字重,辅助文字（"总价值"标签）字重 400 浅灰（v1 都是 590）
6. **整张卡片可点规则**:列表行整行可点（开抽屉）+ 行内只允许 ghost icon（操作 ⋯）,无 primary 按钮（v1 隐含违反）
7. **持久状态用 Banner 不用 Toast**:viewer 权限不足、离线模式用 Banner 置顶（v1 把权限错误塞 toast）
8. **空状态三分类**:initial/filter/permission 各有专属文案 + CTA（v1 只有 initial）
9. **8 态按钮全覆盖**:loading 用 spinner + "保存中…"、disabled 防 re-click、error shake + 重试（v1 部分）
10. **错误文案说人话**:"网络断了,客户阶段还没改,你可以重试"（v1 是"操作失败"）
