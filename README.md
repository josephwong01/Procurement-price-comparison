# Procurement Price Comparison

面向企业采购场景的“采购询源与比价 Agent / Skill”。它把采购需求转成可追溯的多平台候选池、统一成本与综合评分，并输出供人工初筛和确认的采购比价结果。

## 当前状态

MVP v0.1 已完成：需求 Schema、最终输出、候选商品、供应商、Query Planner、匹配去重、TCO 评分、平台 Adapter 和 Skill 端到端组装均已冻结或完成回归。设备、标准品、定制品和服务类案例均已覆盖；最新盲测为“智能手环客户礼品”。

本版本止于候选比价和采购建议，不会自动联系商家、发送询价、下单、发起审批或写入 ERP。

## 核心流程

```text
采购需求 → 补全与确认 → 查询计划 → 多平台采集 → 候选与供应商归一化
→ 匹配与去重 → TCO 与综合评分 → 主表/详细表 → 人工确认
```

## 快速使用

Skill 入口位于 `skills/procurement-sourcing/SKILL.md`。输入采购品类、数量、预算、用途、收货地和到货要求；信息不完整时，Skill 会区分硬约束、偏好、假设和待确认项，并保留证据与未知项。

## 校验

安装校验依赖后运行：

```powershell
python -m pip install -r requirements-validation.txt
python scripts/validate_mvp.py
```

统一校验会检查全部 JSON 文件、端到端清单、底层 Schema/业务校验器、Skill 包结构、敏感信息和发布必需文件。

## 目录

- `skills/procurement-sourcing/`：可复用 Skill、工作流合同和 RFQ 准备边界
- `schemas/`：各阶段正式 Schema
- `examples/`：四类结构示例与校验样本
- `cases/`：真实、轻量真实与端到端回归案例
- `scripts/`：Schema、业务规则和 MVP 统一校验器
- `docs/`：路线图、冻结记录、回归报告和发布清单

## 使用原则

- 原始平台价格和人民币比较价同时保留，汇率可用有时间戳的大致参考值。
- 产品适配度与供应商可靠度分开评估，再合并为可解释的单一总分。
- 不满足硬约束的候选不得伪装成合格项；排除原因必须展示。
- 库存、运费、税费、交期等不能确认时必须标记未知或待询价，不得编造。
- 搜索执行成功不等于产生有效候选；原始结果与有效候选数量分别记录。

Apify 连接与浏览器 Console 排查见 [Apify 连接常见问题](docs/apify-browser-console-faq.md)。

详见 [项目路线图](docs/project-roadmap.md) 和 [MVP 发布检查清单](docs/mvp-release-checklist-v0.1.md)。
