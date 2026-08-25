# 咖啡饮料机 candidate.3 回归报告

## 结论

candidate.3 已解决上一轮发现的主表链接、平台显示、评分语义和评分明细问题。同一咖啡饮料机案例通过 JSON Schema、权重、总分复算、ID唯一性、引用完整性和状态门槛校验。

报告仍为 `READY_FOR_REVIEW`，不是可直接下单文件：预计杯量、展位功率与尺寸、具体送货地址、最终运费及合规文件仍未确认。

## 最终主表展示样例

| 排名 | 商品（点击打开商品页） | 来源平台 | 供应商 | 对比总价 | 主要优点 | 主要缺点 | 商家评分/信号 | 综合分 | 推荐角色 |
| ---: | --- | --- | --- | ---: | --- | --- | --- | ---: | --- |
| 1 | [HAS2S 双粉料热饮机](https://www.ggmgastro.com/de-de-eur/heissgetraenkeautomat-2-programme-digital-2-pulverbehaelter-schwarz-has2s) | GGM Gastro Germany | GGM Gastro | 约 ¥2,332.74 | 咖啡＋热巧克力；桶装水；230V/50Hz；连续出杯 | 仅两个程序；依赖粉料 | TÜV客户满意度“sehr gut”，非数字评分 | 84.25 | 综合平衡 |
| 2 | [TASSIMO HAPPY TAS107E](https://www.bosch-home.com/de/de/product/kaffeemaschinen/tassimo-kapselmaschinen/tassimo-happy/TAS107E) | Bosch Germany official store | Bosch Hausgeräte | €39.99＋未确认运费 | 价格最低；饮品多；紧凑易操作 | 高峰吞吐弱；胶囊成本未知 | 页面4.8/5为产品评分，非商家评分 | 82.25 | 最低成本 |
| 3 | [Nescafé Alegria 6/30 翻新机](https://automaten-hofmann.com/automaten/heissgetraenkeautomat-nescafe-alegria-6-30-gebraucht/) | Automaten Hofmann | Automaten Hofmann GmbH | 约 ¥7,642.31 | 六种饮品；80—180杯/小时；水箱；230V/50Hz | 翻新机；保修待确认 | 暂无可核验数字商家评分 | 72.25 | 较高配置 |

## 排除候选

| 商品（点击打开商品页） | 来源平台 | 排除原因 |
| --- | --- | --- |
| [Sielaff Siamonie TS IN](https://www.flavura.de/katalog/produkt/sielaff-siamonie-ts-in-01-ihr-premium-heissgetraenkeautomat/) | Flavura Germany | 约 ¥82,115且运费另计，显著超过1万元硬预算 |

## 回归结果

| 检查项 | 结果 |
| --- | --- |
| 主表商品超链接 | 通过 |
| 来源平台独立列 | 通过 |
| 商家评分与产品评分区分 | 通过 |
| 五维明细与单一总分复算 | 通过 |
| 权重合计100% | 通过 |
| candidate/detail/evidence/risk引用完整 | 通过 |
| 开放阻断项禁止进入审批 | 通过 |
| 审批状态要求可比较总价 | 通过 |

## 冻结判断

结构问题已修复，candidate.3 可以进入人工冻结审阅。采购案例自身的未确认事项继续保留为阻断项，不应被误判为Schema失败。

