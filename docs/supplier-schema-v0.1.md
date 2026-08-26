# Supplier Schema v0.1（冻结版）

## 状态

- 版本：`0.1`
- 状态：`FROZEN`
- 冻结日期：2026-08-26
- Schema：`schemas/supplier-v0.1.schema.json`
- 业务校验器：`scripts/validate_suppliers.py`

候选版 `supplier-v0.1-candidate.schema.json` 与候选说明保留为历史审阅记录，新Supplier记录统一写入正式版。

## 记录边界

Supplier表示可跨商品复用的供应商主体，平台店铺记录在 `platform_profiles`，商品和报价仍属于Product Candidate。平台店铺与法律主体没有充分证据时不得自动认定为同一主体。

## 冻结规则

1. 一个供应商主体可以关联多个平台店铺。
2. 店铺评分必须保留指标代码、原始值、量表、采集时间和证据；产品评分不得写入供应商评分。
3. 销量、成交、经营年限等信号必须保留平台原始口径；统计周期不明时不得猜测。
4. 公开宣传的能力标记为 `CLAIMED`，不能当作已确认承诺。
5. 资质区分已核验、部分核验、未核验和过期。
6. 信息不足时 `overall_score` 必须为空，`score_status` 必须为 `NOT_SCORED`。
7. 未询盘事项进入 `pending_confirmations`；本版本不主动联系供应商。
8. 库存和保修不作为核心字段；供应商交期只记录公开宣称，报价交期仍属于Product Candidate。
9. `EXCLUDED` 记录必须提供排除原因。

## 验证基线

- 人工字段审阅：全部按推荐规则确认。
- Draft 2020-12元Schema验证：通过。
- 4份结构Fixture和4份真实/轻量真实记录：通过。
- 跨字段业务规则校验：通过。

## 版本管理

冻结后只允许兼容性修复。新增必填字段或改变现有字段语义时，应建立后续候选版本，不直接覆盖v0.1。

