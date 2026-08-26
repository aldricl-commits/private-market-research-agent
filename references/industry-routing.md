# 行业附录选择与执行规则（一级市场版）

先定位标的的**主要价值来源与经济模型**，再选附录；不按叙事标签或赛道热词机械选择。crypto 项目尤其如此——"AI+DePIN+RWA"的项目按它实际靠什么收钱路由。

## 1. 选择协议

1. 按未来 3–5 年价值贡献选一个主附录；只有当次业务会改变 KPI 或估值方法时加载一个次附录。
2. **Crypto 按协议经济类型路由**：先问"这个协议的收入/价值捕获机制像什么"，再选 crypto-* 附录。发链的应用（appchain）按应用本体路由，链只是形态。
3. **混合标的**：AI×crypto → 看付费方买的是 AI 能力还是 token 经济（前者主 ai-native 次 crypto-*，后者反之）；biotech×AI 平台 → 主 biotech-private 次 ai-native。
4. **一级标的使用二级继承附录**（下表"继承"类）时：KPI 字典、价值驱动树、护城河判断直接用；**估值方法一律改走 `valuation-private.md`**（轮次 comps + 二级锚折价），附录内的 DCF/倍数仅作二级锚参照。
5. 无完全匹配时选经济模型最接近的附录，报告中写明适配与未覆盖项。
6. 报告头部声明 `行业附录: <slug>[, <slug>]`，slug 为文件名（如 `crypto-defi`）。

## 2. 路由矩阵 — 本技能原生附录（一级视角）

| 主附录 | 适用边界 | 主估值方法 | 必备 KPI | 常用次附录 |
|---|---|---|---|---|
| [crypto-infra](../industries/crypto-infra.md) | L1/L2、rollup、DA、跨链、节点/RPC、开发者中间件 | FDV/fees vs 二级锚、轮次 comps、生态期权 | 活跃地址、真实费用、TVL 生态、开发者数 | crypto-defi |
| [crypto-defi](../industries/crypto-defi.md) | DEX、借贷、perp、收益、衍生品协议 | FDV/fees、P/S(协议收入)、轮次 comps | TVL、fees vs 激励、take rate、留存 | crypto-infra、crypto-stablecoin-payments |
| [crypto-stablecoin-payments](../industries/crypto-stablecoin-payments.md) | 稳定币发行方、支付网络、出入金、汇款 | 储备收益模型、P/S、轮次 comps | 供应量、真实交易量、储备结构、牌照 | payments-fintech、crypto-defi |
| [crypto-cefi-exchange](../industries/crypto-cefi-exchange.md) | CEX、托管、prime broker、做市商 | P/S、P/E（有利润）、二级锚(COIN等)折价 | 交易量、take rate、牌照版图、资产留存 | capital-markets、crypto-stablecoin-payments |
| [crypto-consumer-gaming-depin](../industries/crypto-consumer-gaming-depin.md) | 链游、消费应用、社交、NFT、DePIN | 用户价值倍数、供给侧单位经济（DePIN）、轮次 comps | 真实 DAU/留存、付费转化、供给节点经济 | media-gaming、crypto-infra |
| [crypto-rwa-tokenization](../industries/crypto-rwa-tokenization.md) | RWA 发行/平台、代币化基金/国债/信贷、链上资管 | AUM 费率模型、P/S、二级锚(资管)折价 | 链上 AUM、费率、赎回机制、底层资产质量 | capital-markets、crypto-stablecoin-payments |
| [ai-native](../industries/ai-native.md) | 基础模型、AI infra/工具链、AI 应用与 agent 公司 | ARR 倍数 vs 二级软件折价、轮次 comps | ARR 增速、毛利率(推理成本)、留存、算力承诺 | saas、semiconductors |
| [biotech-private](../industries/biotech-private.md) | pre-IPO 创新药、平台型 biotech、诊断 | 逐资产 rNPV、licensing comps、IPO comps | 管线阶段、现金 runway、临床数据质量 | pharma、healthcare-services |

## 3. 路由矩阵 — 继承附录（二级视角，估值按第 1 节规则 4 调整）

| 主附录 | 适用边界（一级场景） | 二级锚示例用途 |
|---|---|---|
| [saas](../industries/saas.md) | 订阅/用量软件公司 | 上市 SaaS 倍数作锚，按阶段折价 |
| [internet-platform](../industries/internet-platform.md) | 平台/marketplace/电商 | GMV/take rate 框架直接用 |
| [payments-fintech](../industries/payments-fintech.md) | 支付、钱包、BNPL、跨境 | TPV/净 take rate 框架直接用 |
| [capital-markets](../industries/capital-markets.md) | 交易所、资管、经纪、市场基础设施 | 交易量/AUM 驱动模型直接用 |
| [semiconductors](../industries/semiconductors.md) | 芯片/算力硬件初创 | 需求周期与单位经济框架 |
| [hardware](../industries/hardware.md) | 设备/终端/机器人 | BOM 与量产良率框架 |
| [pharma](../industries/pharma.md) | 商业化阶段药企 | biotech-private 的后期补充 |
| [healthcare-services](../industries/healthcare-services.md) | 医疗服务/器械/CRO | 量/报销框架 |
| [consumer](../industries/consumer.md) | 品牌/零售/餐饮 | 量价 mix 框架 |
| [media-gaming](../industries/media-gaming.md) | 游戏/内容/IP | 用户付费框架（链游次附录常用） |
| [banks](../industries/banks.md) / [insurance](../industries/insurance.md) | 持牌金融初创 | 监管资本框架 |
| [energy](../industries/energy.md) / [utilities](../industries/utilities.md) | 能源/电力初创（含算力配套电力） | 资产收益框架 |
| [industrials](../industries/industrials.md) / [telecom](../industries/telecom.md) / [reits](../industries/reits.md) | 对应传统赛道 | 按需 |
| [autos-ev](../industries/autos-ev.md) / [metals-mining](../industries/metals-mining.md) / [transport](../industries/transport.md) | 整车/矿业（含 DePIN 硬件供给侧参照）/运输物流 | 按需 |

## 4. 一手数据入口（一级增补）

| 领域 | 入口 |
|---|---|
| Crypto 协议数据 | [DefiLlama](https://defillama.com) · [Token Terminal](https://tokenterminal.com) · [Dune](https://dune.com) · [Artemis](https://app.artemis.xyz) · 区块浏览器 |
| Crypto 融资/估值 | [RootData](https://rootdata.com) · [Messari](https://messari.io) · [DeFiLlama Raises](https://defillama.com/raises) · [CryptoRank unlock](https://cryptorank.io/token-unlock) |
| 私募申报 | [SEC EDGAR Form D](https://efts.sec.gov/LATEST/search-index?q=&dateRange=custom&forms=D) · [UK Companies House](https://find-and-update.company-information.service.gov.uk/) |
| 传统一级融资 | Crunchbase · PitchBook · Tracxn（按订阅可得性） |
| AI | Hugging Face · Google Scholar · GitHub |
| Biotech | [ClinicalTrials.gov](https://clinicaltrials.gov) · [FDA](https://www.fda.gov/drugs/drug-approvals-and-databases) · [Google Patents](https://patents.google.com) · PubMed |
| 团队 | LinkedIn · [Wayback Machine](https://web.archive.org) · 法院公开记录 · FINRA BrokerCheck |

引用记录 URL、发布日期、数据期间、抓取日期；二级锚数据（上市公司/流通 token 倍数）标注快照时间。

## 5. 行业附录待建清单

当前未覆盖、出现标的时按 saas.md 骨架 + 一级两节（token economics 若适用、一级红旗）新建：defense tech、space、climate/energy storage 一级视角、robotics。新建后在 `industry-rules-private.json` 注册 slug。
