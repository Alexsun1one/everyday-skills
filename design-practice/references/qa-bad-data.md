# 坏数据清单 — Bad Data Acceptance

> AI 生成 UI 第四常见失败模式:**默认数据好看,真实数据塌**。AI 总是给"John Doe"、"test@example.com"、"Lorem ipsum"——真实世界的超长姓名、空字段、负数、极端值、emoji 用户名、不同 i18n,会让脆弱的布局瞬间塌掉。
>
> 这一页冻结:6 类坏数据边界 case,每个生成完都要用这套数据压力测试。

## 6 类坏数据

### 1. 超长 Long Content

**测试数据:**
- 用户名:`Alexander Wellington-Humperdinck the Third`(超长英文名)
- 中文用户名:`欧阳龙飞凤舞李察德森史密斯`(超长中文名)
- 邮箱:`extremely.long.email.address.that.goes.on.forever@very-long-subdomain.example-corporation.com`
- URL:`https://www.example.com/very/long/path/that/keeps/going/and/going/and/going`
- 单词:`Pneumonoultramicroscopicsilicovolcanoconiosis`(45 字符)
- 表格备注:`这是一段非常非常非常非常非常非常非常非常非常非常长的备注文字,完全没有换行符,考验 UI 的 word-break 能力`
- emoji 名:`🚀🦄🌈✨不可能的超长 emoji 用户名🎉🎊💫`

**塌的地方:**
- avatar 旁边的名字撑爆容器
- 表格列宽被撑爆,挤压其他列
- 按钮文字撑爆按钮宽度
- breadcrumb 撑爆顶栏
- 链接 URL 撑爆侧栏

**修复:**
```css
.username {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.url {
  word-break: break-all;       /* URL 强制断 */
  overflow-wrap: break-word;
}

.long-content {
  overflow-wrap: break-word;   /* 长单词允许断 */
  word-break: break-word;
}
```

表格列:`max-width` + `text-overflow: ellipsis` + hover 显示 tooltip 全文。

### 2. 空内容 Empty Content

**测试数据:**
- 名字:`(空)` / 单空格 / 多空格
- 简介:`null` / `undefined` / `""` / `"   "`
- 头像:`null` / 缺失
- 数字:`0`(看起来像空)/ `null`(看起来像 0)
- 日期:`null` / `0000-00-00` / `1970-01-01`

**塌的地方:**
- 空字段显示 `null` / `undefined` 字面字符串
- 缺头像显示 broken image icon
- 数字 0 显示成"—"或空白(用户以为没数据)
- 空日期显示 `Invalid Date`

**修复:**
- 空字段显示 fallback:`—` 或 `(未填写)` 或 `(暂无)`
- 缺头像用 initials fallback(`A` for `Alexander`)
- 数字 0 必须显示 `0`(不是空白或 `—`)
- 空日期显示 `(未设置)` 或 `(待定)`
- 用 `??`(空值合并)而不是 `||`(避免 0 被吞):
```js
const value = data.count ?? '—';   // 0 显示 0
const value = data.count || '—';   // 0 显示 —(错!)
```

### 3. 极端值 Extreme Numbers

**测试数据:**
- 价格:`$0.01`(超小)/ `$9,999,999,999.99`(超大)
- 百分比:`-100%`(负)/ `0.00001%`(超小)/ `1000000%`(超大)
- 数量:`0` / `-1`(负)/ `999,999,999`(超大)
- 时间:`1ms`(超快)/ `9999h 59m`(超大)
- 距离:`0.1m` / `99999km`

**塌的地方:**
- `$9,999,999,999.99` 撑爆价格列
- `1000000%` 进度条撑爆 100%
- `-100%` 负数显示成 `NaN%`
- `999,999,999` 不带千分位难读

**修复:**
- 千分位逗号:`(999999999).toLocaleString()` → `999,999,999`
- 智能单位:`1024` → `1K`,`1500000` → `1.5M`,`999999999` → `999.99M` 或 `1B`
- 进度条 clamp:`width: ${Math.min(100, Math.max(0, value))}%`
- 负数保护:`value >= 0 ? value : 0`
- 货币符号本地化:` Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY' })`

### 4. 权限 Permission Boundary

**测试数据:**
- 普通用户访问管理员页面 → 应该 403,不是显示管理员内容
- 只读用户访问编辑页 → 编辑按钮应该 disabled 或隐藏
- 没付费用户访问高级功能 → 应该 upsell,不是显示 disabled 按钮
- 跨组织访问别的组织数据 → 应该 404,不是显示数据
- token 过期 → 应该重新登录,不是显示错误状态

**塌的地方:**
- 前端隐藏了按钮但 API 没鉴权(用户手动调用 API 还能改)
- 没权限显示成空状态(误导,用户以为没数据)
- token 过期显示"网络错误"(误导)
- 跨组织数据 404 显示成"服务器错误"

**修复:**
- 前端 + API 双重鉴权(前端隐藏只是 UX,API 必须验证)
- 没权限明确显示:"你没有访问此页面的权限,联系管理员 [姓名] 请求权限"
- token 过期自动跳转登录页
- 跨组织数据返回 404,前端显示"未找到"

### 5. 网络 Network Failure

**测试数据:**
- 网络完全断 → 所有 API 失败
- 网络慢 → 30 秒才返回(应该 timeout)
- 间歇性失败 → 第一次成功第二次失败
- 502 / 503 / 504 → 服务不可用
- CORS 错误 → 跨域被拒
- DNS 解析失败

**塌的地方:**
- 网络断显示白屏
- 网络慢一直 loading 不返回
- 502 显示 stack trace
- CORS 错误显示控制台错误但 UI 无反馈

**修复:**
- 网络断全局监听 `offline` 事件,显示 banner:"网络连接已断开,显示的是缓存数据"
- API timeout 10-30s,超时显示"请求超时,请重试"
- 502/503/504 统一显示:"服务暂时不可用,我们的团队已收到通知。30 秒后自动重试,或[手动重试]。"
- CORS 等浏览器级错误统一显示:"请求失败,请检查网络后重试"
- 加 retry 机制(指数退避):1s → 2s → 4s → 放弃

### 6. i18n 国际化 Internationalization

**测试数据:**
- 中文姓名 + 英文 UI(汉字宽度不同)
- 阿拉伯文 / 希伯来文(RTL 阅读方向)
- 德文(单词比英文长 30%)
- 日文(汉字 + 假名 + 罗马字混排)
- 韩文(圆角字符)
- 泰文(无空格分隔)
- 印地文(复杂字素)
- 俄文(西里尔字母 + 不同字宽)
- emoji(双字节宽度)
- 货币:`¥100` / `$100` / `100€` / `100₹`(符号位置不同)
- 日期:`2026-01-15` / `15/01/2026` / `15.01.2026` / `令和8年1月15日`
- 数字:`1,000.00`(美)/ `1.000,00`(欧)/ `1 000,00`(法)

**塌的地方:**
- 英文 UI 装不下德文翻译(button "Submit" → "Absenden" 30% 长)
- 没处理 RTL(阿拉伯文整个布局反向)
- 货币符号硬编码在前面(`¥100` vs `100€`)
- 日期格式硬编码美式
- 数字千分位硬编码逗号
- 字体不支持 CJK / 阿拉伯文

**修复:**
- 所有文字用 i18n 库(`react-i18next` / `next-intl`),不硬编码
- 容器宽度给 30% 余量(德文)
- RTL 支持:`<html dir="rtl">` + CSS logical properties(`margin-inline-start` 而不是 `margin-left`)
- 货币、日期、数字用 `Intl.NumberFormat` `Intl.DateTimeFormat`
- 字体 fallback:`font-family: Inter, "PingFang SC", "Hiragino Sans", "Microsoft YaHei", sans-serif`

## 验收清单

```text
页面 URL:_____________

□ 1. 超长
  □ 用 "Alexander Wellington-Humperdinck the Third" 测试用户名
  □ 用 50 字符 URL 测试链接显示
  □ 用超长无空格单词测试 word-break
  □ 用 emoji 用户名测试宽度
  □ 验证:text-overflow: ellipsis / word-break

□ 2. 空
  □ 用 null/undefined/""/  "   " 测试所有字段
  □ 用缺失头像测试 fallback(initials)
  □ 用 0 vs null 测试显示(0 ≠ 空)
  □ 验证:fallback 文字 / initials avatar

□ 3. 极端
  □ 用 $9,999,999,999.99 测试价格列
  □ 用 1000000% 测试进度条
  □ 用 -1 测试负数显示
  □ 验证:千分位 / 智能单位 / clamp

□ 4. 权限
  □ 普通用户访问管理员页面
  □ 只读用户看编辑按钮(应 disabled 或隐藏)
  □ 跨组织访问数据(应 404)
  □ 验证:前端 + API 双重鉴权

□ 5. 网络
  □ 关网络再访问
  □ 模拟 502 / 503 / 504
  □ 模拟 30s 慢响应
  □ 验证:offline banner / timeout / retry

□ 6. i18n
  □ 用德文 UI 测试(单词长 30%)
  □ 用阿拉伯文测试 RTL
  □ 用中文姓名 + 英文 UI 测试宽度
  □ 测试不同货币符号位置
  □ 测试不同日期格式
  □ 测试不同数字千分位
```

## AI 验收员提示词

```text
你是一个严格的坏数据验收员。审查下面这个页面/组件对真实世界数据的鲁棒性。

页面 / 组件:[提供]

按 6 类坏数据测试:

1. 超长:用 "Alexander Wellington-Humperdinck the Third"、50 字符 URL、超长无空格单词、emoji 用户名测试。
   - 容器是否会撑爆?
   - 是否有 text-overflow: ellipsis?
   - 是否有 word-break: break-word?

2. 空:用 null/undefined/""/多空格/缺失头像测试。
   - 是否显示 null/undefined 字面字符串?
   - 是否有 fallback 文字(— / 未填写)?
   - 缺头像是否有 initials fallback?
   - 0 是否显示成 0(不是空白或 —)?

3. 极端:用 $9,999,999,999.99、1000000%、-1 测试。
   - 数字是否带千分位?
   - 进度条是否 clamp 在 0-100%?
   - 负数是否保护?

4. 权限:
   - 前端隐藏了按钮,API 是否也鉴权?
   - 没权限是否明确显示(不是空状态)?
   - 跨组织访问是否 404?

5. 网络:
   - 网络断是否显示 banner?
   - 是否有 timeout 和 retry?
   - 502/503/504 是否有用户友好提示?

6. i18n:
   - 是否用 i18n 库(不硬编码文字)?
   - 容器宽度是否给 30% 余量(德文)?
   - 是否支持 RTL?
   - 货币/日期/数字是否本地化?

每类打勾或打叉,失败的具体指出修复点。
```

## 与 SKILL.md 的关系

SKILL.md 的 "Three-Gate QA" 的 Product Gate(或 Engineering Gate)必须包含这一页。任何页面生成完,都要用这套坏数据压力测试。

## 权威信源

- "Designing for the Unexpected" — Smashing Magazine
- "Defensive CSS" — Ahmad Shadeed 文章系列
- "Internationalization Handbook" — W3C
- "Real World Data" —testing 库 best practice
