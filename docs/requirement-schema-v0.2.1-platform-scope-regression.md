# 咖啡机平台范围回归测试

## 测试输入

- 采购对象：咖啡饮料机。
- 用户指定必搜平台：Amazon、淘宝、1688、京东-中国、京东-德国。
- Agent补充范围：1—3个平台。
- 收货与使用：德国慕尼黑展会。

“Amazon”按履约目的地解释为 Amazon Germany；“京东-德国”经核验映射为 JD.com 在欧洲及德国运营的 Joybuy Germany，而不是虚构一个 `jd.de` 京东商城。

## 平台覆盖结果

| 平台 | 来源 | 状态 | 商品级候选 | 说明 |
| --- | --- | --- | ---: | --- |
| Amazon Germany | 用户指定 | 成功 | 1 | 找到德国商品页、价格和库存；电压字段需复核 |
| 淘宝 | 用户指定 | 访问受限 | 0 | 搜索页无法安全访问，未取得可核验商品结果 |
| 1688 | 用户指定 | 访问受限 | 0 | 搜索页无法安全访问，未取得可核验商品结果 |
| 京东-中国 | 用户指定 | 部分成功 | 0 | 能确认品类及商品名称，但逐项搜索跳转登录页，价格和详情不完整 |
| 京东-德国（Joybuy） | 用户指定 | 成功 | 1 | 已确认德国平台及咖啡机商品 |
| GGM Gastro Germany | Agent补充 | 成功 | 1 | 德国商用设备电商，补充展会型粉料机 |
| Automaten Hofmann | Agent补充 | 成功 | 1 | 德国专业设备商，补充高吞吐翻新机 |

Agent补充平台数为2，符合1—3个平台要求。

## 候选快照

| 商品 | 来源平台 | 页面价格 | 判断 |
| --- | --- | ---: | --- |
| [De'Longhi Magnifica S ECAM22.110.B](https://www.amazon.de/DeLonghi-ECAM-22-110-B-Kaffeevollautomat-Milchaufsch%C3%A4umd%C3%BCse/dp/B00400OMU0) | Amazon Germany | €294.90 | 条件候选：页面电压字段冲突，非咖啡饮料能力有限 |
| [De'Longhi Magnifica Evo ECAM290.61.SB](https://m.joybuy.de/dp/delonghi-magnifica-evo-ecam29061sb-kaffeevollautomat-silber/10364381) | Joybuy Germany | €339.99 | 条件候选：德国本地可买，非咖啡饮料能力待确认 |
| [GGM Gastro HAS2S](https://www.ggmgastro.com/de-de-eur/heissgetraenkeautomat-2-programme-digital-2-pulverbehaelter-schwarz-has2s) | GGM Gastro Germany | €297.49含税 | 当前综合匹配最好：咖啡＋热巧克力、桶装水、230V/50Hz |
| [Nescafé Alegria 6/30](https://automaten-hofmann.com/automaten/heissgetraenkeautomat-nescafe-alegria-6-30-gebraucht/) | Automaten Hofmann | €750未税＋运费 | 条件候选：吞吐较高，但为翻新机 |

## Schema结论

平台范围策略通过回归，但存在一个跨结构影响：Requirement Schema可以表达必搜平台和补充平台数量；最终输出仍需要逐平台记录来源、状态、候选数和失败原因。目前仅有 `channels_attempted` 与 `channels_succeeded`，无法完整表达“访问受限”和“部分成功”。

因此：

1. Requirement Schema v0.2.1候选可以进入审阅；
2. Procurement Output candidate.3不应立即冻结；
3. 下一修订应把 `platform_coverage[]` 加入最终输出，再用本案例复跑；
4. Query Planner以后负责把平台范围展开为关键词和执行计划，但不能改变用户指定的平台边界。

## 未完成事项

- 淘宝和1688商品级搜索未完成，原因是访问限制；
- 京东中国商品级价格和详情采集未完成，原因是登录限制；
- 中国平台到德国的运输、税费、合规和插头转换成本未计算；
- 当前价格不是2026年11月锁价或库存承诺。

