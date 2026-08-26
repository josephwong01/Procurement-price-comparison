# Product Candidate Schema v0.1 candidate

## 定义

一个 Candidate 不是抽象产品型号，而是“某个平台、某个供应商、某个已选SKU或报价”的可比较采购方案。同一型号如果平台、供应商、SKU或报价不同，应生成不同 `candidate_id`。本阶段不按履约方案拆分 Candidate。

## 字段分组

1. `identity`：标题、品牌、型号、已选SKU、变体、商品状态和页面类型。
2. `source`：平台、商品链接、店铺链接、市场国家、观察时间和采集方式。
3. `supplier`：供应商主体、类型、地点、商家评分、资质和可核验信号。
4. `offer`：采购数量、MOQ、搜索展示价、已选SKU价、正式报价、成本组成、可比总成本、未知成本及报价商业条件。
5. `requirement_match`：逐条记录硬条件、软条件和信息项的通过情况。
6. `category_data`：标准品、设备、定制品和服务类的差异字段。
7. `assessment`：优缺点、风险、分项分数、单一总分、推荐角色和排除原因。
8. `evidence`：每个关键事实对应的网页、API、截图、报价、文档或计算证据。
9. `provenance`：生成时间、采集批次、总体可信度和假设。

## 本版关键规则

- 主表价格必须优先来自 `selected_sku_price` 或 `quoted_price`；`search_display_price` 仅用于发现和纠错。
- 运费、税费或清关费未知时列入 `unknown_costs`，不得按零处理。
- 本阶段不设置独立履约方案对象，也不因履约方式不同拆分 Candidate；已知运输费用仍记录在 `offer.cost_components`。
- 交期、交期起算点、售后、付款条件和报价有效期属于报价商业条件，记录在 `offer.commercial_terms`，但不构成独立履约方案。当前版本按人工审阅结论不设置库存和保修字段。
- `supplier.rating.subject` 必须区分 `SUPPLIER`、`STORE` 和 `PRODUCT`；产品评分不能冒充商家评分。
- 关键价格和关键规格通过 `evidence_refs` 指向证据；允许暂时未知，但必须降低可信度。
- `candidate_status=EXCLUDED` 时必须提供至少一个 `exclusion_reasons`。
- `procurement_type` 与 `category_data.kind` 必须一致。
- JSON Schema负责单条记录的结构约束；总分复算、权重合计、证据引用存在性、Candidate ID唯一性和跨记录去重由业务校验器负责。

## 类型扩展

| 类型 | 重点字段 |
|---|---|
| 标准品 | 通用属性、包装、Logo定制 |
| 设备 | 电压、供水、容量、尺寸、安装、耗材 |
| 定制品 | 材料、工艺、设计输入、打样、修改轮次、验收方式 |
| 服务 | 服务范围、交付物、里程碑、修改轮次、源文件、知识产权 |

## 暂定人工审阅项

1. 已确认：Candidate 按“平台 × 供应商 × 已选SKU/报价”拆分，暂不包含履约方案。
2. 已确认：搜索展示价永久保留，用于审计和价格纠错。
3. 已确认：产品评分可在详细表展示，但主表商家评分只读取 `STORE` 或 `SUPPLIER`。
4. 已确认：`overall_score` 在信息不足时允许为空，不把不完整候选强行排序。
5. 已确认：候选版允许 `content_hash=null`，后续冻结版本再评估是否强制。
