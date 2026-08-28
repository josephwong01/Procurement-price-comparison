# 平台 Adapter v0.1-candidate

## 状态与责任边界

- 状态：`DRAFT_FOR_HUMAN_REVIEW`
- Adapter负责把来源数据映射为Product Candidate、Supplier和Evidence。
- Adapter不负责需求匹配、去重、TCO、综合评分或供应商联系。

## Adapter家族

1. `APIFY_MARKETPLACE`：淘宝和1688的搜索、详情、SKU与店铺数据。
2. `PUBLIC_WEB`：Amazon、Joybuy、品牌官网和供应商网站。
3. `AUTHENTICATED_BROWSER`：需要用户登录态的京东、淘宝等浏览器采集。
4. `SCREENSHOT_MANUAL`：截图或人工抄录的降级输入。
5. `GENERIC_API`：未来其他结构化接口。

Apify渠道运行前必须执行凭证和额度预检，规则见`skills/procurement-sourcing/references/apify-credential-preflight.md`。`users/me`的HTTP 200证明Token有效；`free_tier_exhausted`属于Actor额度不足，不能记录为凭证失效。Actor返回`SUCCEEDED`但Dataset只有错误对象时，技术执行与采购可用性必须分别记录。

## 核心规则

1. 每次运行必须记录Adapter版本、平台、访问方式、输入记录和采集时间。
2. 原始输入不直接进入主表；必须输出字段级映射和证据引用。
3. 观察值、派生值、估算值、未知值和冲突值必须区分。
4. 搜索展示价只能映射到 `search_display_price`，不得自动成为锁定SKU价格。
5. 产品评分、店铺评分和供应商评分必须按主体映射，不能混用。
6. 缺失字段保持未知；不得用空字符串、0或默认枚举伪装已知。
7. 无法映射的字段必须说明忽略、保留原始值、待新增映射或敏感信息已脱敏。
8. `FAILED`、`PARTIAL`、`SKIPPED` 必须如实记录错误或警告，不得描述为成功。
9. API Token、Cookie、账号和其他凭据不得进入Adapter结果或Git仓库。
10. Adapter输出必须继续通过目标Schema校验，Adapter成功不代表Candidate业务合格。

## 首版退出条件

- 淘宝与1688 API各通过1例。
- 公开网页通过1例。
- 登录浏览器或截图降级通过1例。
- 输出引用现有Product Candidate与Supplier正式Schema。
- 失败、部分成功、未知字段和敏感脱敏规则通过业务校验。
