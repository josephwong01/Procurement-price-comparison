# 平台 Adapter v0.1-candidate 回归报告

## 覆盖范围

- 淘宝Apify API：搜索与详情映射到蓝牙音响Candidate和Supplier。
- 1688 Apify API：人偶服起始价、定制能力和未知字段的部分映射。
- GGM公开网页：价格、电源和公开供应商信息映射。
- 京东登录浏览器：只形成脱敏证据和部分映射，不伪造已锁定SKU。

## 关键断言

1. Adapter运行状态与警告、错误一致。
2. 字段映射必须引用真实输入和输出ID。
3. 输出文件存在，Candidate或Supplier ID及Schema版本一致。
4. 登录输入必须标记已脱敏。
5. Token、Cookie值和Authorization凭据不得进入产物。
6. 搜索展示价不会映射为锁定SKU价格。

## 验证结果

- Draft 2020-12元Schema检查：通过。
- 淘宝API、1688 API、公开网页、登录浏览器及访问失败Fixture：`5/5`通过，零错误。
- 输出文件、ID、Schema版本、脱敏和状态业务校验：通过。

## 当前状态

`FROZEN_V0.1`。记录已迁移至正式版本并完成冻结后复验。

