# Supplier Schema v0.1-candidate

## 状态

- 版本：`0.1-candidate`
- 状态：`DRAFT_FOR_HUMAN_REVIEW`
- 本阶段不冻结、不替代 Product Candidate Schema v0.1。

人工字段审阅已于2026-08-26按推荐规则确认；当前进入真实案例回归，仍为候选状态。

## 记录边界

Supplier 是可跨商品复用的供应商主体记录。平台店铺是 `platform_profiles`，商品或报价仍属于 Product Candidate。若店铺和法律主体的关系没有证据，不得合并为已核实主体。

## 字段组

1. `identity`：法律主体、展示名称、类型、所在地及官网。
2. `platform_profiles`：一个或多个平台店铺、店铺评分及主体关系。
3. `business_signals`：销量、成交、经营年限、响应率等平台原始信号；原始值永久保留，标准化值可为空。
4. `capabilities`：支持的采购类型、生产/定制/服务能力、服务地区和交期宣称。
5. `qualifications`：营业执照、平台认证、证书、检测报告和作品集。
6. `assessment`：优缺点、风险及单一供应商总分。
7. `pending_confirmations`：当前未自动联系供应商时的人工询盘清单。
8. `evidence` 与 `provenance`：证据、采集时间、置信度和假设。

## 候选规则

1. `supplier_id` 是本系统ID，不把平台店铺ID直接当作跨平台主体ID。
2. 店铺评分必须包含指标代码、原始值、原始量表和采集时间；不能把产品评分写成店铺评分。
3. 销量、成交等信号必须记录平台原始口径和统计周期；不明确时写 `null`，不得猜测。
4. 资质名称出现不等于已核验，必须用 `verification_status` 区分。
5. `overall_score` 信息不足时必须为空，且 `score_status` 为 `NOT_SCORED`。
6. `EXCLUDED` 记录必须提供排除原因。
7. 库存和保修暂不设为核心字段；交期只保留供应商公开宣称，具体报价交期仍属于 Product Candidate。
8. 未询盘事项进入 `pending_confirmations`，不会被描述为已确认能力。

## 本轮人工审阅重点

- 是否接受“主体—多平台店铺”的一对多结构。
- 是否接受主体关系的五级状态，而不是自动认定同一家公司。
- 是否保留原始平台指标并允许标准化值为空。
- 供应商总分是否继续保持单一分数，信息不足时不评分。
- 是否接受将主动询盘留到后续阶段，仅生成待确认问题。

