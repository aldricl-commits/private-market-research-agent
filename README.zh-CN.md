# 一级市场投研 Agent（Private Market Research Agent）

*[English](README.md) · [中文](README.zh-CN.md)*

一个 [Claude Code](https://claude.com/claude-code) 技能：把"帮我看看这个项目"变成一份**结构完整、来源可溯、可验证性透明**的机构级**深度研究报告**或 **IC memo**，覆盖 **crypto、AI、biotech** 的一级市场投资。

做这件事的出发点很简单：一级市场的问题不是信息太多，而是**信息太少、且被创始人叙事包装过**。所以这个 agent 的价值不在"浓缩信息"，而在**结构化、交叉验证、拉齐质量底线**。

---

## 产出什么

| 模式 | 产出 | 适用场景 |
|---|---|---|
| **Deep Research**（默认） | 七章报告：业务描述 → 行业成长前景 → 产业地图 → 团队背调 → 估值对比 → 反方论证 → 结论与监控 | 研究驱动，没有 deal 也能跑 |
| **IC Memo** | 按 house 结构的投决材料：元数据 → 投资论点 → 条款 → 产品 → 商业模式 → traction → 市场与竞争 → 团队 → cap table → 估值 → 风险 → 生态协同 → 建议 | 有在谈的 deal 与条款 |
| **批量评审** | 每个项目十节精简格式 | Residency / 孵化批次评审 |

---

## 五条设计原则

这五条是它区别于"帮我写份研究报告"这类通用 prompt 的地方。每一条都由**自动检查器强制执行**，不是建议而是门槛。

**1. 数据可得性必须前置声明，并且它封顶结论的强度。**
每份报告开头是一个等级——**A/B/C/D**——加一行来源结构占比（链上可审计 / 申报审计 / 公司一手 / 第三方 / 未验证，合计 100%），再加一份关键缺口清单。**D 级报告不允许给出投资观点。**这让读者第一眼就知道"这份报告能信到什么程度"，而不用自己逆向推断。

**2. 产业地图的每一层都必须写出它的二级估值锚。**
产业地图章节是一张分层表，其中"二级锚"列是硬性要求：每一层要回答有没有上市公司或流通 token 为它定价、倍数是多少；没有就明确写"无二级锚"并说明估值从最近的锚如何传导。这是把一级估值接到真实定价上的那根线。

**3. 公司口径的声称永远不会被洗成事实。**
关键数字都带来源标签——`[链上]` `[申报/审计]` `[公司]` `[第三方]` `[未验证]`。无法验证的声称原样引用为声称（"公司称 ARR $10M `[公司]`，未能独立验证"），绝不改写成客观陈述语气。缺失的数据写"未获取到"，**绝不用记忆或估算填充**。

**4. 估值一律脚本计算，且每个结论都要绑定退出。**
至少两种方法交叉验证（轮次 comps / 二级锚折价 / token economics / rNPV / 情景退出）。所有计算跑内置 Python 脚本、假设留存为 JSON——**禁止心算**。每个估值结论必须给出退出路径与隐含 IRR/MOIC。

**5. 默认自我攻击。**
必做 pre-mortem（"三年后这笔投资失败了，最可能的原因是什么"），其中至少一条要直击报告自己的核心论点。未验证的声称要做反转检验：**如果它是假的，结论会不会翻转？** crypto 标的的任何增长数字在使用前必须先过刷量与激励净化那一关。

---

## 覆盖范围

**原生行业附录（一级视角）**——为这个 agent 专门写的：

- `crypto-infra` — L1/L2、rollup、DA、跨链、中间件
- `crypto-defi` — DEX、借贷、永续、收益协议
- `crypto-stablecoin-payments` — 稳定币发行方、支付网络、出入金
- `crypto-cefi-exchange` — 中心化交易所、托管、prime broker
- `crypto-consumer-gaming-depin` — 链游、消费应用、DePIN
- `crypto-rwa-tokenization` — RWA 发行、代币化基金、链上资管
- `ai-native` — 基础模型、AI infra、AI 应用
- `biotech-private` — pre-IPO 创新药、平台型 biotech

每个附录都含 KPI 字典、价值驱动树、（适用时的）token economics 剖析、估值方法、护城河判断和**一级尽调红旗清单**。

**继承行业附录**——20 个传统赛道（SaaS、半导体、银行、保险、消费、能源、工业、支付、互联网平台、医疗、REIT、电信、汽车/EV、金属矿业、运输、游戏媒体、公用事业、资本市场、医药、硬件）。KPI 框架可直接使用，估值一律改走一级方法矩阵。

---

## 目录结构

```
SKILL.md                        # 入口：角色纪律 + 六步工作流
references/
  deep-research-template.md     # 七章结构模板
  ic-memo-template.md           # IC memo（模式 A 单 deal / 模式 B 批量）
  memo-rubric.md                # 1-10 评分标尺、过会特征、弱 memo 红旗、尽调动作清单
  output-format.md              # 声明框、来源标签、文风纪律、数字规范
  data-sources-private.md       # 来源分级、可得性等级定义、刷量识别
  valuation-private.md          # 阶段 x 赛道方法矩阵、折价纪律、退出与回报框架
  team-diligence.md             # 核查表、红旗清单、合规边界
  industry-routing.md           # 28 类行业路由矩阵 + 一手数据入口
  industry-rules-private.json   # 检查器读取的 slug 与必备 KPI 规则
industries/                     # 28 个行业附录
scripts/
  comps_builder.py              # comps 表、隐含估值区间、分位反查、football field 图
  token_economics.py            # token 解锁/稀释 + 股权 cap table 与退出 IRR/MOIC
  check_private_output.py       # 报告完整性与纪律检查器（P0/P1/P2）
tests/                          # 7 个回归测试
```

---

## 开始使用

**作为 Claude Code 技能安装：**

```bash
cp -r "Private market research agent" ~/.claude/skills/private-market-research
```

之后在 Claude Code 里直接说："帮我研究一下 <公司名>" 或 "给 <项目> 写一份 IC memo"——技能会自动触发，不需要斜杠命令。

**单独运行脚本**（Python 3，仅用标准库，无依赖）：

```bash
python3 scripts/comps_builder.py --demo
python3 scripts/token_economics.py --demo-token
python3 scripts/token_economics.py --demo-equity
python3 scripts/check_private_output.py --report 你的报告.md
python3 tests/test_scripts.py
```

检查器在存在 P0 问题时返回非零退出码，因此可以直接接入评审流程做门禁。

---

## 关于范围与保密

本仓库**只包含方法论**——模板、rubric、行业框架和脚本。**不含任何 deal 数据、公司具体结论或可归属的内部观点。**

IC memo 模板与 rubric 是对照真实历史投决 memo 校准出来的。那次校准提炼的是**结构与纪律**（章节顺序、验证文化、评分标尺）；所有项目名、人名、条款和数字在设计上就被排除在外。

使用时请注意：pitch deck、data room、内部 memo 属敏感材料。在本地处理，不要把机密数字贴进联网检索，也不要让工作文件混进对外产出。

---

**非投资建议。** 这套工具辅助分析，不做决策。产出的质量上限由它背后的来源决定——这正是每份报告都必须先声明来源的原因。
