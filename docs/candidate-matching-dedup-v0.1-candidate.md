# 商品匹配与去重 v0.1-candidate

## 状态与边界

- 状态：`DRAFT_FOR_HUMAN_REVIEW`
- Schema：`schemas/candidate-resolution-v0.1-candidate.schema.json`
- `MATCH_RECORD` 保存逐项需求匹配，可将摘要回写Product Candidate。
- `DUPLICATE_CLUSTER` 保存候选之间的同款、变体和重复刊登关系。

本阶段不删除原始候选、不覆盖平台原价、不把相似标题直接判定为同款。

## 匹配规则

1. 每个条件同时记录需求路径、候选路径、期望值、观察值、结果、置信度和证据。
2. 任一硬条件明确失败，则 `hard_failure=true`、总体结果为 `FAIL`，Candidate建议写回 `EXCLUDED`。
   自动排除仅适用于置信度为 `HIGH` 或 `MEDIUM` 的明确失败；低置信度信息必须转为 `UNKNOWN` 并人工复核。
3. 硬条件未知不等于失败；总体结果保持 `PARTIAL` 或 `UNKNOWN`，并进入缺失信息清单。
4. 偏好条件失败不会单独排除候选。
5. 语义匹配用于材料、工艺、服务范围等不能只做字符串相等的条件，但必须给出理由和证据。

## 去重规则

1. 优先使用GTIN、制造商料号、品牌+型号、已选SKU等强标识；标题相似只作为弱信号。
2. 同一型号在不同平台或供应商出售，标记 `SAME_MODEL_DIFFERENT_OFFER`，保留各自价格和供应商。
3. 同一商品不同颜色、容量或配置标记 `SAME_PRODUCT_DIFFERENT_VARIANT`，不得直接合并报价。
4. 同一供应商重复刊登且SKU一致时才考虑 `EXACT_DUPLICATE`。
5. 有冲突字段或证据不足时使用 `POSSIBLE_DUPLICATE` 与 `HUMAN_REVIEW`。
6. 规范候选只是比较展示入口，不会删除其余成员及证据。
7. 规范候选按已锁定SKU、价格完整度、证据质量与新鲜度、供应商清晰度、直达链接依次选择，并记录实际采用的依据。

## 人工审阅重点

- 是否接受硬条件失败自动建议排除、硬条件未知不自动排除。
- 是否接受跨平台同型号只建立关联而不合并报价。
- 是否接受颜色、容量、配置不同一律视为变体。
- 是否接受只有高置信度精确重复才允许合并。

