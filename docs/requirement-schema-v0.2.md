# Procurement Requirement Schema v0.2

## 状态

v0.2已冻结，作为Requirement Schema当前默认版本。v0.1归档保留。

## 设计原则

- 覆盖标准品、定制品、设备和服务。
- 区分硬约束、偏好和信息项。
- 每轮最多三个阻断问题。
- `SEARCH_READY`仅表示可以开始初步搜索，不表示可以购买或审批。
- 多履约路径可以是主路径、备选或兜底，并明确选择规则。
- 预算上限与每条履约路径的价格口径、费用包含项分开表达。
- 未知费用不得按零计算。
- 每份需求至少保留一条来源记录。
- Requirement Schema只记录采购方明确的渠道偏好，不生成搜索策略。

## 顶层结构

`requester → business_context → subject → use_case → quantity → budget → fulfillment_policy → fulfillment_options → commercial → customization/service → acceptance_criteria → supplier_requirements → sourcing_preferences → readiness → provenance`

## 冻结依据

Schema通过Draft 2020-12元Schema检查、四类真实案例验证、负面规则测试和主履约路径引用检查。详见验证报告。
