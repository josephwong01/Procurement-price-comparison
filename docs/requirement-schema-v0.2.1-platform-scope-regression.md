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
| 京东-中国 | 用户指定 | 成功 | 3 | 已登录Chrome采集低、中、高三个价格层级，含价格、店铺、销量和好评率 |
| 京东-德国（Joybuy） | 用户指定 | 成功 | 1 | 已确认德国平台及咖啡机商品 |
| GGM Gastro Germany | Agent补充 | 成功 | 1 | 德国商用设备电商，补充展会型粉料机 |
| Automaten Hofmann | Agent补充 | 成功 | 1 | 德国专业设备商，补充高吞吐翻新机 |

Agent补充平台数为2，符合1—3个平台要求。

## 访问限制复核

GitHub上存在淘宝、1688和京东的浏览器自动化项目，但不能直接作为当前可用的“绕过方案”：

| 平台 | 参考项目 | 技术路线 | 最近代码推送 | 结论 |
| --- | --- | --- | --- | --- |
| 淘宝 | [Python3WebSpider/TaobaoProduct](https://github.com/Python3WebSpider/TaobaoProduct) | Selenium | 2020-05-02 | 仅供思路参考，页面结构和验证机制已可能变化 |
| 1688 | [resphinas/1688-selenium-spider](https://github.com/resphinas/1688-selenium-spider) | Selenium | 2023-04-20 | 需要真实浏览器环境，不能绕过当前安全限制 |
| 京东中国 | [chisdiva/JdSpider](https://github.com/chisdiva/JdSpider) | Scrapy＋Selenium | 2022-05-06 | 当前商品详情仍跳转登录页，旧采集逻辑不能直接采用 |

可视浏览器复核显示：完成Chrome登录后，京东搜索页可以取得商品价格、店铺、销量、好评率和商品ID，并已截取搜索结果证据。淘宝与1688搜索页仍被浏览器安全策略明确禁止，不能通过脚本、备用浏览器、CDP或间接请求规避。

安全可行的后续方案是：用户在自己的浏览器登录相应平台并打开搜索结果，再由Agent读取当前可见页面和截图留证；不读取、导出或复用Cookie。

## 候选快照

| 商品 | 来源平台 | 页面价格 | 判断 |
| --- | --- | ---: | --- |
| [De'Longhi Magnifica S ECAM22.110.B](https://www.amazon.de/DeLonghi-ECAM-22-110-B-Kaffeevollautomat-Milchaufsch%C3%A4umd%C3%BCse/dp/B00400OMU0) | Amazon Germany | €294.90 | 条件候选：页面电压字段冲突，非咖啡饮料能力有限 |
| [De'Longhi Magnifica Evo ECAM290.61.SB](https://m.joybuy.de/dp/delonghi-magnifica-evo-ecam29061sb-kaffeevollautomat-silber/10364381) | Joybuy Germany | €339.99 | 条件候选：德国本地可买，非咖啡饮料能力待确认 |
| [GGM Gastro HAS2S](https://www.ggmgastro.com/de-de-eur/heissgetraenkeautomat-2-programme-digital-2-pulverbehaelter-schwarz-has2s) | GGM Gastro Germany | €297.49含税 | 当前综合匹配最好：咖啡＋热巧克力、桶装水、230V/50Hz |
| [Nescafé Alegria 6/30](https://automaten-hofmann.com/automaten/heissgetraenkeautomat-nescafe-alegria-6-30-gebraucht/) | Automaten Hofmann | €750未税＋运费 | 条件候选：吞吐较高，但为翻新机 |

### 京东中国低、中、高价格层级

| 商品 | 商品价 | 加3,000元运输规划值 | 店铺信号 | 判断 |
| --- | ---: | ---: | --- | --- |
| [维纳仕商用速溶咖啡机上置式台式](https://item.jd.com/10038826907073.html) | ¥860 | 约¥3,860 | 已售6000+、100%好评、旗舰店 | 最低价；饮品数、供水、电压和CE待确认 |
| [妙雀2冷2热＋冷热水台式咖啡奶茶饮料机](https://item.jd.com/10125691765315.html) | ¥1,480 | 约¥4,480 | 已售900+、100%好评、官方旗舰店 | 中间档；冷热与花式饮品更匹配展会 |
| [西堤岛6冷6热涡轮防堵台式一体机](https://item.jd.com/10096651005504.html) | ¥2,980 | 约¥5,980 | 已售1000+、99%好评 | 高配档；饮品覆盖最好，但合规仍待确认 |

## 中国至慕尼黑运输规划值

对中国平台候选，暂按一台包装后35—60kg、0.20—0.35m³估算：

- 运输规划值：人民币3,000元/台；
- 合理区间：人民币2,000—5,000元/台；
- 包含：中国提货、国际运输、德国末端派送的粗略缓冲；
- 不包含：德国进口增值税、可能的关税、展馆进馆物流、特殊木箱和保险。

公开线路参考中，2026年中国至德国普通空运约6美元/公斤，铁路拼箱约148—210美元/立方米；单台货物还会受到最低收费、报关、两端操作和末端派送影响，所以不能直接用重量或体积单价相乘。本回归统一用3,000元作为可比价的占位成本。

## Schema结论

平台范围策略通过回归，但存在一个跨结构影响：Requirement Schema可以表达必搜平台和补充平台数量；最终输出仍需要逐平台记录来源、状态、候选数和失败原因。目前仅有 `channels_attempted` 与 `channels_succeeded`，无法完整表达“访问受限”和“部分成功”。

因此：

1. Requirement Schema v0.2.1候选可以进入审阅；
2. Procurement Output candidate.3不应立即冻结；
3. 下一修订应把 `platform_coverage[]` 加入最终输出，再用本案例复跑；
4. Query Planner以后负责把平台范围展开为关键词和执行计划，但不能改变用户指定的平台边界。

## 未完成事项

- 淘宝和1688商品级搜索未完成，原因是访问限制；
- 京东中国价格和商家信号已采集，但供水、电压、CE、包装与售后尚未核验；
- 中国平台到德国运输已加入3,000元规划值，但税费、合规和插头转换成本仍未计算；
- 当前价格不是2026年11月锁价或库存承诺。

