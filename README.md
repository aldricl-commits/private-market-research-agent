# Private Market Research Agent

*[English](README.md) · [中文](README.zh-CN.md)*

A [Claude Code](https://claude.com/claude-code) skill that turns *"look into this company/project"* into a structured, source-tagged, institutional-grade **deep research report** or **IC memo** — for venture and growth-stage investing in **crypto, AI, and biotech**.

Built for a simple reason: in private markets the problem is not too much information, it's **too little — wrapped in founder narrative**. This agent's value is not summarizing. It's structuring, cross-verifying, and holding a quality floor.

---

## What it produces

| Mode | Output | When |
|---|---|---|
| **Deep Research** (default) | 7-chapter report: business description → growth drivers → industry mapping → team diligence → valuation → pre-mortem → conclusion & monitoring | Research-driven; runs with no live deal |
| **IC Memo** | House-structured investment committee memo: metadata → thesis → deal terms → product → business model → traction → market & competition → team → cap table → valuation → risks → ecosystem fit → recommendation | A live deal with terms |
| **Batch Review** | Condensed 10-section format per project | Residency / incubation cohorts |

---

## Five design principles

These are what separate this from a generic "write me a research report" prompt. Each one is **enforced by an automated checker**, not just suggested.

**1. Data availability is declared up front, and it caps how strong the conclusion may be.**
Every report opens with a grade — **A/B/C/D** — plus a source mix (on-chain / filings / company-provided / third-party / unverified, summing to 100%) and a list of the key gaps. A `D`-grade report is *not allowed* to state an investment view. This makes "how much should I trust this?" the first thing a reader learns, not something they have to reverse-engineer.

**2. Every industry-map layer must name its public-market anchor.**
The industry mapping chapter is a layered table, and the "secondary anchor" column is mandatory: for each layer, which listed company or liquid token prices it, at what multiple — or explicitly "no public anchor" plus how value transmits from the nearest one. This is what connects private valuation to something real.

**3. Company claims are never laundered into facts.**
Key numbers carry a source tag — `[on-chain]` `[filings/audited]` `[company]` `[third-party]` `[unverified]`. An unverifiable claim is quoted as a claim ("the company states ARR of $10M `[company]`, not independently verified"), never restated in an objective voice. Missing data is written as "not obtained" — never filled from memory or estimate.

**4. Valuation is computed by scripts, and every conclusion is tied to an exit.**
At least two methods must cross-check (round comps / public-anchor discount / token economics / rNPV / scenario-exit). All arithmetic runs through the bundled Python scripts with assumptions saved as JSON — no mental math. Every valuation conclusion must carry an exit path and an implied IRR/MOIC.

**5. Adversarial by default.**
A pre-mortem ("three years out, this failed — why?") with at least one scenario attacking the report's own core thesis. Unverified claims get a reversal test: *if this turns out false, does the conclusion flip?* Crypto targets get a mandatory wash-trading / incentive-farming purification pass before any growth number is used.

---

## Coverage

**Native appendices (private-market lens)** — built for this agent:

- `crypto-infra` — L1/L2, rollups, DA, bridges, middleware
- `crypto-defi` — DEX, lending, perps, yield
- `crypto-stablecoin-payments` — issuers, payment rails, on/off-ramps
- `crypto-cefi-exchange` — CEX, custody, prime brokerage
- `crypto-consumer-gaming-depin` — games, consumer apps, DePIN
- `crypto-rwa-tokenization` — RWA issuance, tokenized funds, on-chain asset management
- `ai-native` — foundation models, AI infra, AI applications
- `biotech-private` — pre-IPO drug developers, platform biotech

Each carries a KPI dictionary, a value-driver tree, token-economics analysis where relevant, valuation methods, moat tests, and a **red-flag checklist**.

**Inherited appendices** — 20 traditional sectors (SaaS, semiconductors, banks, insurance, consumer, energy, industrials, payments, internet platforms, healthcare, REITs, telecom, autos/EV, metals & mining, transport, media & gaming, utilities, capital markets, pharma, hardware). KPI frameworks apply directly; valuation always routes through the private-market method matrix.

---

## Repository layout

```
SKILL.md                        # Entry point: role discipline + 6-step workflow
references/
  deep-research-template.md     # 7-chapter structure
  ic-memo-template.md           # IC memo (Mode A single deal / Mode B batch)
  memo-rubric.md                # 1-10 scoring scale, strong/weak memo markers, diligence checklist
  output-format.md              # Declaration box, source tags, writing discipline, number conventions
  data-sources-private.md       # Source tiering, availability grades, wash-trading detection
  valuation-private.md          # Stage x sector method matrix, discount discipline, exit framework
  team-diligence.md             # Verification table, red flags, compliance boundaries
  industry-routing.md           # 28-sector routing matrix + primary-source entry points
  industry-rules-private.json   # Machine-readable slugs and required KPI groups
industries/                     # 28 sector appendices
scripts/
  comps_builder.py              # Comps tables, implied ranges, percentile check, football field
  token_economics.py            # Token unlock/dilution + equity cap-table & exit IRR/MOIC
  check_private_output.py       # Report completeness & discipline checker (P0/P1/P2)
tests/                          # 7 regression tests
```

---

## Getting started

**Install as a Claude Code skill:**

```bash
cp -r "Private market research agent" ~/.claude/skills/private-market-research
```

Then simply ask in Claude Code: *"Do a deep research on <company>"* or *"Write an IC memo for <project>"* — the skill triggers on the request, no slash command needed.

**Run the scripts standalone** (Python 3, standard library only — no dependencies):

```bash
python3 scripts/comps_builder.py --demo
python3 scripts/token_economics.py --demo-token
python3 scripts/token_economics.py --demo-equity
python3 scripts/check_private_output.py --report your_report.md
python3 tests/test_scripts.py
```

The checker exits non-zero when a P0 is present, so it can gate a review workflow.

---

## A note on scope and confidentiality

This repository contains **methodology only** — templates, rubrics, sector frameworks, and scripts. It contains no deal data, no company-specific findings, and no attributable internal views.

The IC memo template and rubric were calibrated against real historical investment committee memos. That calibration produced *structure and discipline* (section order, verification culture, scoring scale); all deal names, people, terms, and figures were excluded by design.

When using this agent: pitch decks, data rooms, and internal memos are sensitive material. Process them locally, never paste confidential figures into web searches, and keep working files out of any published output.

---

**Not investment advice.** This tooling supports analysis; it does not make decisions. Outputs are only as good as the sources behind them — which is exactly why every report has to declare them.
