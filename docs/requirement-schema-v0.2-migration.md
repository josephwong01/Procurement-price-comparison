# v0.1到v0.2迁移说明

## 文件策略

- v0.1 Schema归档为 `schemas/procurement-requirement-v0.1.schema.json`。
- 默认Schema路径 `schemas/procurement-requirement.schema.json` 指向冻结的v0.2内容。
- 四个原始 `requirement.json`继续作为v0.1历史实例保留。
- 每个案例新增 `requirement-v0.2.json`。

## 主要映射

| v0.1 | v0.2 |
|---|---|
| `product` | `subject` |
| 描述中的用途 | `use_case` |
| `delivery` | `fulfillment_policy + fulfillment_options` |
| 预算备注中的费用边界 | 全局预算＋路径成本代码 |
| `customization.required` | `customization.mode` |
| `search_preferences` | `sourcing_preferences` |
| 定制或服务备注 | 输入、里程碑、交付物、验收、修改和知识产权 |

## 兼容说明

v0.2不保证与v0.1逐字段兼容。历史实例不自动覆盖；迁移必须生成新文件并保留来源记录。
