# SaaS 行业深度研究附录

适用范围：订阅制软件、云原生应用软件、平台型 B2B 软件、垂直 SaaS、消费订阅软件，以及以订阅收入为核心的混合软件公司。若公司同时有硬件、服务、广告、交易抽佣或云基础设施业务，先拆分收入和毛利，再只对订阅/软件部分使用本附录。

## 目录

1. 使用原则
2. 信息来源与公允机制
3. SaaS 价值驱动树
4. 核心 KPI 字典
5. 财务模型结构
6. 估值方法
7. 护城河与竞争判断

## 1. 使用原则

- 先确定公司是否真是 SaaS：收入必须以可续约订阅、用量订阅或长期软件合约为主。一次性 license、咨询实施、硬件打包收入不能直接套 SaaS 倍数。
- 不要只看收入增速。SaaS 研究的核心是“增长质量”：留存、扩张、获客效率、毛利率、现金流、SBC 稀释和竞争强度共同决定价值。
- 区分企业级、SMB、开发者工具、垂直 SaaS、消费订阅和平台型 SaaS。不同客群的 churn、销售周期、毛利率、S&M 效率和估值中枢不同。
- 所有公司自定义 KPI 必须回到披露原文定义，不得把不同公司口径强行横比。
- 把 reported growth 拆成 organic growth、并购、汇率、价格、seat expansion、usage expansion 和 churn 的贡献。
- 对高估值 SaaS，估值章节优先用反向 DCF 说明现价隐含的 ARR、FCF margin、Rule of 40 和终局市场份额。

## 2. 信息来源与公允机制

### 来源优先级

1. **监管申报**：10-K/10-Q/20-F/S-1/F-1/年报。用于确认收入确认、RPO、deferred revenue、客户集中度、风险因素、SBC、并购和分部口径。
2. **公司财报材料**：earnings release、shareholder letter、investor presentation、supplemental metrics。用于获取 ARR、NRR、RPO、客户数、ACV、guidance 和管理层口径。
3. **电话会文字稿**：用于跟踪管理层对 demand、pipeline、seat expansion、AI monetization、pricing、churn、macro headwind 的措辞变化。
4. **同业公司披露**：用于建立 peer set 和 KPI 合理区间。优先选择相同客群、销售模式、产品类别和增长阶段的公司。
5. **第三方与卖方研究**：只能作为补充观点，不得替代一手披露。引用时标明日期和口径。

### 公允机制

- **定义优先**：每个 KPI 首次出现时写明公司定义。若公司没有披露定义，写“未获取到公司定义”，不要用行业习惯定义代替事实。
- **同业可比前先调口径**：横比 NRR、ARR、RPO、billings、FCF margin 前，说明口径差异和不可比项。
- **增长与质量并列**：任何“高速增长”结论必须同时给出留存、获客效率、毛利率、FCF 或 SBC 稀释的质量约束。
- **反证优先写入**：每个看多论点必须给出可推翻证据。例如“AI 驱动扩张”必须绑定 AI attach rate、ARPU、gross retention 或 usage 增长，而不是只引用管理层描述。
- **避免幸存者偏差**：选择可比公司时同时纳入优质、高增长、成熟和受压公司，不能只选高倍数同业。
- **区分周期与结构**：预算冻结、销售周期拉长、seat contraction 可能是宏观周期，也可能是产品竞争力下降。必须用续约、扩张、pipeline conversion 和客户 cohort 证据判断。

## 3. SaaS 价值驱动树

SaaS 内在价值可以拆成：

```text
企业价值 =
  可服务市场规模
  × 长期可获取份额
  × 定价能力 / ARPU
  × 留存与扩张质量
  × 稳态毛利率
  × 稳态销售与营销效率
  × 研发和管理费用杠杆
  × 税后 FCF 转换率
  ÷ 风险折现率
  − 稀释与资本配置损耗
```

报告中至少回答：

- 增长来自新客户、老客户扩张、价格、用量、模块 attach，还是并购？
- 增长是否需要持续高 S&M 投入才能维持？
- 客户留存是否足以证明产品是 workflow system of record，而非可替换工具？
- 毛利率和 FCF margin 是否已经接近成熟软件公司水平，还是仍被基础设施、支持、服务或 AI 推理成本压制？
- SBC 和股本稀释是否吞掉了自由现金流价值？

## 4. 核心 KPI 字典

| KPI | 计算/定义 | 研究用途 | 常见陷阱 |
|---|---|---|---|
| ARR | 年化经常性收入；以公司定义为准 | 订阅收入基准和 forward revenue 先行指标 | 有的公司用 ending ARR，有的用 run-rate revenue；并购 ARR 需剔除 |
| Revenue growth | reported / organic / constant currency | 顶线增长速度 | 并购、汇率、价格、一次性迁移收入会污染 |
| NRR / DBNRR | 期初客户群在期末的收入留存和扩张 | 老客户扩张与产品粘性 | 是否包含 churn、降级、价格、并购客户、超大客户扩张要查定义 |
| Gross retention | 剔除 expansion 后的收入留存 | 产品不可替代性 | 只披露 NRR 不披露 gross retention 时，可能用 upsell 掩盖 churn |
| Churn | 客户或收入流失率 | 需求韧性和竞争压力 | logo churn 与 revenue churn 含义不同 |
| RPO / cRPO | 剩余履约义务及 12 个月内可确认部分 | 已签合同和收入可见度 | 多年大单、合同期限变化、消费型合约会扭曲 |
| Billings | revenue + deferred revenue change | 订单/收款趋势 | 年付/月付变化、合同期限、预付款会影响 |
| Customer count | 付费客户数，常分 ACV 档 | 客户获取和上行空间 | 低价值客户增长不等于高质量 ARR |
| ACV / ARPA | 年合同价值 / 每账户收入 | 客户质量与上行空间 | 企业客户 mix 变化会推高但降低客户数增速 |
| Net new ARR | 新增 ARR | 增长动能 | 季节性强，需看 4Q rolling |
| CAC payback | 获客成本回收月数 | S&M 效率 | 用 gross margin-adjusted ARR 更保守 |
| Magic number | 净新增 ARR × 4 × gross margin / 上季 S&M | 销售效率 | 对季节性、企业大单和价格调整敏感 |
| Rule of 40 | 收入增长率 + FCF margin 或 operating margin | 增长和利润平衡 | 口径必须统一，不要混用 non-GAAP operating margin 和 unlevered FCF |
| Gross margin | gross profit / revenue | 软件经济性 | Professional services、hosting、AI inference cost 会压低 |
| S&M / Revenue | 销售营销费用率 | 增长投入强度 | 高增长阶段高费用率不一定坏，需结合新增 ARR |
| R&D / Revenue | 研发费用率 | 产品再投资 | 资本化软件、SBC 和平台迁移要单列 |
| SBC / Revenue | 股权激励 / revenue | 股东稀释 | Non-GAAP 利润常排除 SBC，但估值不能忽略 |
| FCF margin | FCF / revenue | 现金生成能力 | 年付预收款、裁员、capex、租赁和收款周期会扰动 |

必须优先披露的 8 个指标：ARR 或订阅收入、revenue growth、NRR 或 gross retention、RPO/cRPO、gross margin、S&M efficiency、FCF margin、SBC/revenue。

## 5. 财务模型结构

### 收入模型

按可得数据从高到低选择驱动：

1. `ARR beginning + new ARR + expansion ARR - churned ARR = ARR ending`
2. `客户数 × ARPA`
3. `seat 数 × price per seat × attach rate`
4. `usage volume × price per unit`
5. 披露不足时用订阅收入与服务收入分开预测，不得只做总收入 CAGR。

最低预测要求：

- 至少 3 年历史、8 个季度历史。
- 未来 5 年显性预测，收入增速逐年向成熟水平衰减。
- 单列订阅收入、专业服务/实施收入、硬件或其他非订阅收入。
- 单列 organic growth 与并购影响；若无法拆分，写“未获取到拆分”，并降低结论置信度。

### 成本与利润率模型

- Gross margin：订阅毛利率和服务毛利率分开。若 AI 推理、云托管、支付通道或第三方数据成本显著，单独讨论稳态压力。
- S&M：用销售效率驱动，不要机械按收入比例下降。企业级 SaaS 需考虑销售周期和 quota capacity。
- R&D：高增长公司不能过早假设成熟利润率。若平台重构或 AI 产品投入期，研发杠杆应更慢释放。
- G&A：可随规模下降，但上市公司合规成本、并购整合、国际化会设下限。
- SBC：同时进入 diluted shares 和真实经济成本讨论；Non-GAAP margin 不能替代 FCF。
- FCF：从经营现金流、capex、capitalized software、租赁和 deferred revenue 变化解释，不只贴一个 margin。AI 推理、模型训练、数据中心或平台迁移导致 capex/资本化软件上升时，必须拆分维护性 capex 与成长性 capex；维护性 FCF 和成长投入回报路径分开判断。

### 稳态假设边界

- 成熟优质 SaaS 可拥有高毛利率和高 FCF margin，但必须由 retention、pricing power、低 churn 和费用杠杆支持。
- 若 NRR 下降、gross retention 低、CAC payback 拉长，不能同时给高增速、高稳态 margin 和低折现率。
- 若 SBC/revenue 长期高且回购只抵消稀释，应下调权益价值或显性增加股本稀释。

## 6. 估值方法

### scenario analysis可参考的参数
估值假设表

| 假设 | Bear | Base | Bull | 依据 |
|---|---:|---:|---:|---|
| 5 年收入 CAGR | | | | |
| 稳态 FCF margin | | | | |
| 年化股本稀释 | | | | |
| 终局 EV/FCF 或退出倍数 | | | | |
| 情景概率 | | | | |

1. **相对估值**：EV/Revenue、EV/ARR、EV/FCF 或 P/FCF。高增长亏损期可用 EV/Revenue，但必须用 Rule of 40 和增长质量校正。
2. **Unit economics 估值**：披露足够时，用 LTV/CAC、gross retention、CAC payback 交叉验证长期 FCF margin。

### Peer set 规则

选择 5-10 家可比公司，并标注选择理由：

- 产品类别：CRM、ERP、security、observability、data、collaboration、vertical SaaS 等。
- 客群：enterprise、mid-market、SMB、developer、consumer。
- 销售模式：sales-led、PLG、channel-led、marketplace-led。
- 增长阶段：高增长亏损、Rule of 40 平衡、成熟现金牛、转型受压。
- 地理与汇率：美国、欧洲、中国、全球化收入占比。

剔除项必须说明：若某公司看似同业但商业模式、毛利结构、客户群或增长阶段明显不同，不应强行放入同一倍数表。

## 7. 护城河与竞争判断

SaaS 护城河不能只写“切换成本高”。至少从以下维度打分：

| 维度 | 强证据 | 弱证据/反证 |
|---|---|---|
| Workflow depth | 成为核心业务流程系统，停用会影响收入、合规或生产 | 只是 dashboard、插件或可替代工具 |
| Data moat | 客户数据、历史工作流、模型反馈形成累积优势 | 数据可轻易导出，竞品迁移成本低 |
| Ecosystem | API、marketplace、partner、developer 形成生态 | 生态收入弱，集成只是销售话术 |
| Multi-product expansion | 多模块 attach 推高 NRR 和 ARPA | 只靠单一爆款，cross-sell 证据不足 |
| Scale efficiency | S&M 效率随规模改善，gross retention 稳定 | 增长完全靠销售堆出来 |
| Pricing power | 多年提价后 churn 仍低，NRR 稳定 | 提价导致降级、seat contraction 或 logo churn |
| AI defensibility | AI 功能提升留存、ARPU、效率或数据壁垒 | AI 只是功能平权，压低价格或提高推理成本 |

定性护城河必须与财务证据交叉：若声称“强护城河”，但 gross retention 低、NRR 下降、CAC payback 拉长、SBC 高企，必须解释矛盾。
