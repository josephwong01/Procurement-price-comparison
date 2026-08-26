# 平台 Adapter v0.1（冻结版）

## 状态

- 版本：`0.1`
- 状态：`FROZEN`
- 冻结日期：2026-08-26
- Schema：`schemas/platform-adapter-result-v0.1.schema.json`
- 校验器：`scripts/validate_adapter_results.py`

## 冻结规则

1. Adapter只负责来源数据到Candidate、Supplier和Evidence的映射，不负责匹配、去重、TCO或评分。
2. 每次运行记录Adapter版本、平台、访问方式、输入、采集时间、输出和字段级映射。
3. 观察、派生、估算、未知和冲突值必须区分。
4. 搜索展示价不能自动成为锁定SKU价格；产品、店铺和供应商评分不能混用。
5. 缺失字段保持未知，无法映射字段必须记录处置方式。
6. 成功、部分成功、失败和跳过状态必须如实表达。
7. 登录输入必须脱敏；Token、Cookie值和Authorization凭据不得进入产物或仓库。
8. Adapter成功不代表Candidate业务合格，输出仍需通过目标Schema及后续业务流程。
9. 访问受限时只报告失败并交由Query Planner选择允许的降级方式，不绕过访问控制。

## 验证基线

- 淘宝Apify API。
- 1688 Apify API。
- GGM公开网页。
- 京东登录浏览器脱敏记录。
- 公开网页访问失败负向Fixture。
- 5份记录通过正式Schema、引用完整性、脱敏和状态业务校验。

## 版本管理

冻结后只允许兼容性修复。改变输入输出合同或字段映射语义时，应建立后续候选版本。

