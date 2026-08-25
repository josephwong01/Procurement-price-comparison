# Procurement Requirement Schema v0.2 指南

## 适用范围

v0.2用于标准品、定制品、设备和服务类采购需求。先确定 `procurement_type`，再填写通用字段及对应类型模块。

## 约束等级

- `HARD`：不满足即淘汰。
- `PREFERENCE`：影响排序，不直接淘汰。
- `INFORMATION`：用于理解、展示或后续确认。

## 就绪状态

- `DRAFT`：尚未完成初步评估。
- `NEEDS_CLARIFICATION`：至少有一个阻断问题。
- `SEARCH_READY`：阻断问题为零，可开始初步搜索。
- `COMPARISON_READY`：候选信息足够正式比价。
- `RFQ_READY`：可以形成统一询价内容。

`SEARCH_READY`不代表可以直接购买、签约或提交审批。

## 履约路径与预算

全局预算保存单价、总价和比较币种。每条履约路径单独记录目的地、渠道、价格口径、费用包含项和排除项。多条路径通过 `ANY_ONE`、`ALL`或`PRIMARY_WITH_FALLBACK`表达关系。

未知成本不得按零处理；无法归类的费用使用 `OTHER`并在说明中解释。

## 类型模块

- 标准品可使用 `customization.mode=OPTIONAL`表达轻定制。
- 定制品必须使用 `customization.mode=REQUIRED`，记录输入、确认节点和验收。
- 设备可在通用验收中表达安装环境、规格和合规要求。
- 服务类必须填写范围、客户输入、交付物、里程碑、修改政策和知识产权。

## 来源与补问

每份需求至少保留一条 `provenance`。推导值必须记录依据及可信度。每轮最多提出三个阻断问题，不得静默假设数量、交期、税率、替代品牌或定制工艺。

## 与Query Planner的边界

`sourcing_preferences`只保存采购方明确指定的平台、区域、语言及候选数量。自动扩展平台、关键词和筛选条件属于后续Query Planner。
