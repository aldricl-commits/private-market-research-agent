# IC Memo 模板（v1 — 已用 I2025–I2026 历史 memo 语料校准）

> **版本状态：v1。**结构、章节顺序、评审文化与评分标尺提炼自 7 份历史 IC memo（覆盖 RWA 基础设施、机构级公链、DeFi 交易终端、消费 DApp、biotech、机器人行业研究、以及孵化批量评审）。本文件只含结构与纪律，不含任何 deal 细节。评分与评审语言标准见 `references/memo-rubric.md`。

## 0. 两种模式（先判定）

- **模式 A · 单 deal IC memo**（默认）：一个标的一份 memo，完整结构见第 2 节。
- **模式 B · 批量评审 memo**（residency/incubation 每期多项目）：每个项目用第 3 节的精简十节格式，批次头部写一次标准条款与评分标尺。

篇幅纪律：模式 A 全文 1,500–4,000 词（技术复杂的基础设施类可上浮）；模式 B 每项目 300–800 词。**篇幅跟着分歧走**：无争议的节 1–3 句，辩论核心给足。

## 1. House 评审纪律（语料提炼，贯穿两种模式）

1. **验证文化（最高优先）**：
   - 关键合作/客户/committed capital 声称，尽力独立验证并在 memo 中**显式写明验证状态**（"已与 X、Y 直接确认" / "未能独立验证"）。
   - **产品能测必测**：注册试用、与头部竞品做同场景对比（速度/功能/体验差距具体化），测不了写明原因。
   - 创始人尽量见面或视频，写明接触方式（met in person / call）。
   - 数据诚实标注：连"项目方自己都没验证过用户真实性"这类信息也要如实写出——这是语料中过会 memo 的共同特征。
2. **循环需求识别（必做）**：committed capital / TVL / 交易量 / 预存款中，来自战投、关联方、自家生态的部分单独拆出并标注"circular, not independent demand"。
3. **时间承诺核查**：每位联创的全职状态是标准尽调项；兼职/缺席面试/在运营其他项目的，写明并列为 open question。
4. **生态协同是一等公民**：每个 deal 必答"与我们生态（链、交易所、组合公司）的协同是什么、我们能提供什么独特价值"——这直接影响能否拿到 deal 与投后回报路径。
5. **估值直言**：认为贵就写"估值偏高，建议谈判"；对比我们通常的 entry level 写明差距。
6. **Referral 来源记录**：deal 来源写具体（inbound / outbound / 谁引荐）。
7. **数据可得性声明框**（本技能硬性设计）与**产业地图二级锚**（第 2 节第 9 节）继续适用。

## 2. 模式 A · 单 deal memo 结构（顺序对齐 house 惯例）

### 头部（三件）

1. **元数据行**：`项目名` + 材料链接（Deck | Docs | Dataroom | Demo | Dashboard）

   | Sector | Thesis | Geography | Chain(s) | Deal Team（DO/DC） | Source | Stage |
   |---|---|---|---|---|---|---|

   DO = Deal Owner，DC = Deal Co-owner；Source 写明引荐人或渠道。

2. **数据可得性声明框**（`output-format.md` 1.1，硬性）

3. **IC Feedback 区（骨架）**：

   | 姓名/角色 | 评分（1–10）或 Y/N | 评论 |
   |---|---|---|

   评分标尺见 `memo-rubric.md`。**Agent 生成 memo 时此区留空骨架 + 预填"建议 IC 重点讨论的 2–3 个问题"，绝不虚构任何人的评分或评论**；最终决策人意见单列一行。

### 正文（顺序固定）

4. **Summary & Investment Thesis**：一段业务概括（8Q overview 风格：类比锚定 + 量化）+ bullet 式 investment highlights（每条带数字，验证状态显式标注）+ bullet 式 key risks 预览。
5. **Deal Terms / Structure**：

   | 条款 | 内容 |
   |---|---|
   | 投资额与轮次 | |
   | **Equity 估值（pre/post）** | |
   | **Token 估值（FDV）与 equity:token 映射** | 双轨标的两行都填；映射比例写明 |
   | 我们的股/币占比 | |
   | Vesting / 解锁 | |
   | 特殊结构 | blended valuation / advisory equity / call option / volume trigger / 分 tranche 等，逐项写触发条件 |
   | 本轮其他投资人 | 谁领投、谁定价 |

   条款不全列**"待补条款"清单**；估值对比上轮与同类 entry level，贵就直说。
6. **Product / Solution**：问题—方案结构；**产品实测记录**（与竞品的同场景对比，具体到功能与速度差距）；技术架构只写到"影响投资判断"的深度。
7. **Business Model**：收费方式层面（fee 结构、take rate、分层定价）+ 钱流走查；token 在钱流中的角色（无角色写无）。
8. **Traction / User Base**：真实性净化后的数据（`data-sources-private.md` 第 6 节）+ **循环需求拆分** + 留存/复购证据；runway 与 burn。
9. **Market & Competition**：TAM 算术（自己算，不抄 deck，deck 数字可列作对照）；竞品对比表（行=维度：定位/规模/费率/融资/估值/我们标的的差异化，列=竞品）；**产业地图分层表含二级锚列（硬性，`deep-research-template.md` 3.1）**。
10. **Team**：核查表（声称 vs 验证 vs 来源，`team-diligence.md`）+ 红旗 + **全职状态逐人标注** + refer 来源；亮点（连续创业退出、上一周期经历）如实列。
11. **Tokenomics / Cap Table**：token 分配比例与 vesting（`token_economics.py` 跑红旗）；cap table 主要股东与投资人列表；上轮融资历史（金额/估值/领投）。
12. **估值与回报**（本技能增强节，house 语料中较弱、按 `valuation-private.md` 补强）：轮次 comps + 二级锚折价 + 退出情景 IRR/MOIC（脚本计算）+ 反向检验一句（"本轮价格隐含……"）。
13. **Risks / Open Questions**：按类分（采用/监管/竞争/技术/财务与代币/市场/执行——按适用取舍），**最关键的 underwriting question 单独点名**（"本案成立与否最终取决于 X"）。
14. **生态协同与 Adverse Selection**：我们的独特价值（分发/流动性/品牌/牌照/组合协同）；协同的具体形态（部署承诺、volume 引导、集成路径）；**"我们为什么能拿到这个 deal"**必答。
15. **Recommendation**：评分（1–10，标尺见 rubric）+ 动作（Invest / Pass / Track + 条件）+ 投后 6/12 个月验证点 + 否决信号。

### 附录
来源与时间戳清单（含标签）、估值假设摘要、团队核查表全文、检查器结果摘要。

## 3. 模式 B · 批量评审格式（每项目十节，顺序固定）

批次头部：本期申请/面试漏斗数据、标准条款（引用内部条款单，偏离标准的项目单独写）、评分标尺声明。

每个项目：

```text
N. 项目名 —— 一句话定位
Product / Solution        （问题-方案-核心机制；实测记录）
Profit / Revenue          （模式+现值；pre-revenue 写清收入路径）
User Base / Traction      （净化后数据+循环需求拆分）
Team                      （核查结论+全职状态+refer 来源）
Market                    （TAM 算术一行）
Competitor                （2–4 个，每个一句差异化）
Risks / Open Questions    （2–4 条，最关键的 underwriting question 点名）
Investment Thesis         （3–5 条 bullet，生态协同必含一条）
Investment Terms          （标准/偏离标准写明结构）
Team Feedback             （骨架留空+建议讨论问题；不虚构评分）
```

## 4. 语言与风格

- House memo 惯用英文撰写；输出语言默认跟随用户指定，未指定时与语料一致用英文。
- Bullet 浓缩、每条带数字；验证状态显式；判断直言（"valuation too high" 式）；对标锚定（可比公司的规模/估值/结局）。
- 8Q 文风纪律（`output-format.md` 第 3 节）适用于叙述段落。

## 5. 与 deep research 的关系

已有同标的 deep research 报告时：第 4/6/7/8/9/12 节直接引用其结论（注明版本日期），memo 只做浓缩与 deal 层增量；没有时按本模板独立成文，深度对齐第 1 节纪律。
