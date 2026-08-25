# Requirement Schema v0.2 Candidate.2

## 状态

本版本是第二轮候选版，不是冻结版。它落实了第一轮人工字段审阅结论。

## 主要变化

- 新增 `procurement_type`，区分标准品、定制品、设备和服务。
- 新增 `use_case`，结构化记录用途、环境、用户和项目。
- 将单一交付地址改为 `fulfillment_options`，支持多渠道、多目的地和各自成本边界。
- 交付支持月份或日期区间，并明确交期起算事件。
- 预算增加价格口径、包含费用和排除费用。
- 定制模式区分 `NONE`、`OPTIONAL`、`REQUIRED`。
- 定制增加输入资料、确认里程碑和验收标准。
- 服务增加范围、客户输入、交付物、里程碑、修改政策和知识产权。
- 恢复采购申请人及可选业务上下文。
- 履约路径增加选择规则和主路径、备选路径、兜底路径角色。
- 全局预算只保留上限与比较币种，具体价格口径和费用边界下沉至履约路径。
- 成本项目改用标准代码。
- 增加顶层通用验收标准。
- 搜索偏好改名为采购方明确的 `sourcing_preferences`，自动生成的查询仍属于后续Query Planner。
- 增加采购类型、就绪状态和约束操作符的条件校验。
- provenance至少保留1条。

## 兼容策略

v0.1文件保留不覆盖；候选文件通过Git历史保留第一轮版本。冻结前必须完成四例回归、标准验证器校验和最终人工确认。

## 顶层结构

`requester → business_context → subject → use_case → quantity → budget → fulfillment_policy → fulfillment_options → commercial → customization/service → acceptance_criteria → supplier_requirements → sourcing_preferences → readiness → provenance`

## 不属于本 Schema 的内容

“最低成本、较高配置、中间平衡方案各一个”属于后续 Search / Report Strategy，不进入 Requirement Schema。
