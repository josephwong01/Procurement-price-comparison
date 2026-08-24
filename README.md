# Procurement Price Comparison

面向企业采购经理的“采购询源与比价 Agent / Skill”。项目目标不是简单搜索最低价，而是形成可比、可追溯、可解释、可复核的候选供应商池和初步比价结论。

## 当前阶段

当前正在用真实采购案例验证 `Procurement Requirement Schema v0.1`。咖啡饮料机案例只完成了“设备类”验证；在标准品、定制品、设备和服务至少各验证 1 个案例并冻结 v0.2 前，不进入 Query Planner。

## 核心流程

```text
采购需求 → 需求补全 → 搜索策略 → 多平台检索 → 统一候选池
→ 去重 → 商品匹配 → 硬约束淘汰 → TCO 计算 → 供应商评估
→ 综合评分 → 比价表与证据 → 人工复核
```

## 目录

```text
.
├── SKILL.md
├── agents/openai.yaml
├── cases/
│   ├── coffee-beverage-machine-munich-2026/
│   │   ├── requirement.json
│   │   └── validation-notes.md
│   ├── bluetooth-speaker-giveaway/
│   │   ├── requirement.json
│   │   └── validation-notes.md
│   └── ip-mascot-costume/
│       ├── requirement.json
│       └── validation-notes.md
├── docs/
│   ├── project-roadmap.md
│   ├── schema-guide.md
│   ├── source-recovery.md
│   └── workflow.md
├── examples/
│   └── procurement-requirement.example.json
└── schemas/
    ├── common.schema.json
    └── procurement-requirement.schema.json
```

## 使用原则

- 网页展示价格不是最终采购价格；统一换算含税到手成本（TCO）。
- 产品匹配和供应商评估分开进行。
- `HARD` 约束不满足时不得进入正式比价。
- 无法确认的字段必须标记未知并生成待人工确认清单，不得编造。
- 输出保留 URL、采集时间、证据和可信度。

详见 [项目路线图](docs/project-roadmap.md)、[工作流](docs/workflow.md)和 [Schema 指南](docs/schema-guide.md)。

真实案例见 `cases/`。目前已覆盖设备类、定制品和标准品。
