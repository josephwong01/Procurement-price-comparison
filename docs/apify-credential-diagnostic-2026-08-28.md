# Apify凭证与淘宝Actor排障记录（2026-08-28）

## 结论

本次API Key没有过期、撤销或被替换。使用项目`.env.local`中的Token请求Apify官方`GET /v2/users/me`返回HTTP 200。此前将PowerShell的“Authentication failed”表述为凭证失效属于误判。

实际存在两个独立问题：

1. Token最初只存在于被忽略的`.env.local`，Windows Process/User/Machine环境变量均为空；不同执行入口读取不同来源，造成“有时存在、有时不存在”。
2. Token恢复验证后，淘宝搜索Actor主查询成功，但店铺定向运行返回`free_tier_exhausted`。这是社区Actor免费运行次数上限，不是Token认证失败。

## 已采取修订

- 仓库Skill新增[Apify凭证与额度预检](../skills/procurement-sourcing/references/apify-credential-preflight.md)。
- 凭证来源固定为：Process → Windows User → 已被`.gitignore`排除的`.env.local`。
- 每次Actor运行前必须调用`users/me`；HTTP 200才表示Token有效。
- HTTP 401、403、无HTTP状态码和`free_tier_exhausted`分别报告，不再合并为“凭证失效”。
- PowerShell诊断须兼容Windows PowerShell 5.1，不使用`SHA256.HashData`或`Convert.ToHexString`。
- Actor技术状态与采购可用性分开记录；Dataset只包含错误对象时不能计为成功采集。

## 本次复测

- Token预检：HTTP 200。
- 关键词：`咖啡饮料机`。
- 主搜索：成功，10条原始记录。
- 商品详情：唐雀TQ400、西堤岛X-41SCW和妙雀目标SKU成功锁定。
- 未完成：松崎京选、斯麦龙定向商品详情，原因是Actor免费运行次数耗尽。

详细运行ID、Dataset ID和归一化字段见：

`cases/coffee-beverage-machine-skill-acceptance-2026-08-27/taobao-refresh-2026-08-28.json`

本记录不包含Token、Cookie或Authorization header。
