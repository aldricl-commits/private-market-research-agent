#!/usr/bin/env python3
"""private-market-research skill · Token/Equity 稀释与回报计算器

用法：
    python scripts/token_economics.py --input assumptions.json [--horizon 24]
    python scripts/token_economics.py --demo-token
    python scripts/token_economics.py --demo-equity

输入 JSON 的 mode 字段决定模式：
  "token"  — token 解锁表、供给压力、投资人成本 MOIC、结构红旗
  "equity" — cap table 逐轮稀释、我们的占比路径、退出情景 MOIC/IRR

仅使用 Python 标准库；输出 Markdown。所有假设由 JSON 留档，禁止心算。
"""

import argparse
import json
import sys

INSIDER_KEYWORDS = ("team", "founder", "advisor", "investor", "seed", "private", "strategic",
                    "团队", "创始", "顾问", "投资")


def fmt(x, nd=1):
    if x is None:
        return "n/a"
    if abs(x) >= 1e9:
        return f"{x/1e9:,.{nd}f}B"
    if abs(x) >= 1e6:
        return f"{x/1e6:,.{nd}f}M"
    if abs(x) >= 1e3:
        return f"{x/1e3:,.{nd}f}K"
    return f"{x:,.{nd}f}"


def pct(x, nd=1):
    return f"{x*100:.{nd}f}%"


# ---------------------------------------------------------------- token mode

def unlocked_fraction(alloc, m):
    """m 个月时该 allocation 的已解锁比例（TGE=第 0 月）。"""
    if m < 0:
        return 0.0
    tge = alloc.get("tge_unlock_pct", 0.0) / 100.0
    cliff = alloc.get("cliff_months", 0)
    vest = alloc.get("vesting_months", 0)
    if m < cliff:
        return tge
    if vest <= 0:
        return 1.0  # cliff 到期一次性解锁（或无 vesting）
    linear = (m - cliff) / vest
    return min(1.0, tge + (1.0 - tge) * min(1.0, linear))


def is_insider(alloc):
    if "category" in alloc:
        return alloc["category"] in ("team", "investor", "advisor")
    name = alloc.get("name", "").lower()
    return any(k in name for k in INSIDER_KEYWORDS)


def run_token(cfg, horizon):
    total = float(cfg["total_supply"])
    allocs = cfg["allocations"]
    pct_sum = sum(a.get("pct", 0.0) for a in allocs)
    price = cfg.get("current_price")
    if price is None and cfg.get("reference_fdv"):
        price = float(cfg["reference_fdv"]) / total
    fdv = price * total if price else None
    m_now = int(cfg.get("months_since_tge", 0))

    out = []
    out.append(f"# Token Economics — {cfg.get('project', 'Unnamed')}")
    out.append("")
    out.append(f"- 总供应量：{fmt(total, 0)}；分配占比合计：{pct_sum:.1f}%"
               + ("　⚠️ 未到 100%，缺口视为未披露" if abs(pct_sum - 100) > 0.5 else ""))
    if price:
        out.append(f"- 参考价格：${price:,.6g} → **FDV ${fmt(fdv)}**")
    out.append(f"- 时点：TGE 后第 {m_now} 个月" if m_now >= 0 else "- 时点：**pre-TGE**（下表为 TGE 起点推演）")
    base_m = max(m_now, 0)

    # 分配结构表
    out.append("\n## 分配结构\n")
    out.append("| 分配 | 占比 | TGE 解锁 | Cliff | Vesting | 内部人 | 成本 FDV | 现价 MOIC |")
    out.append("|---|---:|---:|---:|---:|:-:|---:|---:|")
    insider_pct = 0.0
    team_vest_flags = []
    for a in allocs:
        ins = is_insider(a)
        if ins:
            insider_pct += a.get("pct", 0.0)
        moic = ""
        if a.get("cost_basis_fdv") and fdv:
            moic = f"{fdv / float(a['cost_basis_fdv']):.1f}x"
        cost = f"${fmt(float(a['cost_basis_fdv']))}" if a.get("cost_basis_fdv") else ""
        name_l = a.get("name", "").lower()
        if ("team" in name_l or "团队" in name_l or a.get("category") == "team"):
            tv = a.get("cliff_months", 0) + a.get("vesting_months", 0)
            team_vest_flags.append((a.get("name"), tv))
        out.append(f"| {a['name']} | {a.get('pct', 0):.1f}% | {a.get('tge_unlock_pct', 0):.0f}% "
                   f"| {a.get('cliff_months', 0)}m | {a.get('vesting_months', 0)}m | {'✓' if ins else ''} | {cost} | {moic} |")

    # 解锁表
    out.append(f"\n## 解锁与供给压力表（自第 {base_m} 月起 {horizon} 个月）\n")
    out.append("| 月 | 新增解锁 | 累计流通 | 流通比 | 月新增/流通 | 新增价值@现价 |")
    out.append("|---:|---:|---:|---:|---:|---:|")

    def circ(m):
        return sum(total * a.get("pct", 0.0) / 100.0 * unlocked_fraction(a, m) for a in allocs)

    prev = circ(base_m)
    circ_start = prev if prev > 0 else None
    rows = []
    for m in range(base_m, base_m + horizon + 1):
        c = circ(m)
        new = c - prev if m > base_m else (c if base_m == 0 else 0.0)
        pressure = (new / prev) if (m > base_m and prev > 0) else 0.0
        val = f"${fmt(new * price)}" if price else "n/a"
        rows.append((m, new, c, c / total, pressure, val))
        prev = c
    for m, new, c, cr, pr, val in rows:
        out.append(f"| {m} | {fmt(new, 0)} | {fmt(c, 0)} | {pct(cr)} | {pct(pr)} | {val} |")

    # 汇总指标
    c0, c12 = circ(base_m), circ(base_m + 12)
    c24 = circ(base_m + 24)
    g12 = (c12 / c0 - 1) if c0 > 0 else float("inf")
    g24 = (c24 / c0 - 1) if c0 > 0 else float("inf")
    tge_float = circ(0) / total
    out.append("\n## 汇总与红旗\n")
    out.append(f"- 当前流通比：{pct(c0/total)}；TGE float：{pct(tge_float)}")
    out.append(f"- 未来 12 个月供给增长：**{pct(g12) if c0 > 0 else 'inf'}**；24 个月：{pct(g24) if c0 > 0 else 'inf'}")
    if price:
        out.append(f"- 流通市值：${fmt(c0*price)} vs FDV ${fmt(fdv)}（倍数一律用 FDV 口径，报告中两者并列披露）")

    flags = []
    if insider_pct > 40:
        flags.append(f"内部人（团队+投资人+顾问）份额 {insider_pct:.1f}% > 40%")
    if tge_float < 0.05 and any(a.get("tge_unlock_pct", 0) > 0 for a in allocs):
        flags.append(f"TGE float {pct(tge_float)} < 5%（低流通高 FDV，价格发现失真）")
    if c0 > 0 and g12 > 1.0:
        flags.append(f"12 个月供给增长 {pct(g12)} > 100%（重度解锁悬顶）")
    for name, tv in team_vest_flags:
        if tv < 24:
            flags.append(f"团队分配 [{name}] cliff+vesting 共 {tv} 个月 < 24 个月")
    if flags:
        out.append("\n**红旗（对照 valuation-private.md 第 4 节阈值）：**")
        for f in flags:
            out.append(f"- ⚠️ {f}")
    else:
        out.append("\n结构红旗：未命中阈值（阈值见 valuation-private.md 第 4 节）。")
    return "\n".join(out)


# --------------------------------------------------------------- equity mode

def run_equity(cfg):
    rounds = list(cfg.get("rounds", [])) + list(cfg.get("future_rounds", []))
    n_hist = len(cfg.get("rounds", []))
    our = cfg.get("our_investment", {})
    out = []
    out.append(f"# Cap Table 稀释与回报 — {cfg.get('project', 'Unnamed')}")
    out.append("\n## 逐轮稀释\n")
    out.append("| 轮次 | Pre-money | 融资额 | Post-money | 本轮新股占比 | ESOP 扩池 | 创始团队累计 | 我们的占比 |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|")

    founders = 1.0
    ours = 0.0
    our_amount = float(our.get("amount", 0.0)) if our else 0.0
    for i, r in enumerate(rounds):
        pre = float(r["pre_money"])
        raised = float(r["raised"])
        post = pre + raised
        new_share = raised / post
        esop = r.get("esop_added_pct", 0.0) / 100.0
        dilution = 1.0 - new_share - esop
        founders *= dilution
        ours *= dilution
        if our and r.get("name") == our.get("round"):
            ours += our_amount / post
        tag = "" if i < n_hist else "（未来轮模拟）"
        out.append(f"| {r['name']}{tag} | ${fmt(pre)} | ${fmt(raised)} | ${fmt(post)} "
                   f"| {pct(new_share)} | {pct(esop)} | {pct(founders)} | {pct(ours, 2)} |")

    if our and ours > 0:
        out.append(f"\n我们的投资：${fmt(our_amount)} @ {our.get('round')} → 全部轮次稀释后占比 **{pct(ours, 2)}**")
        scen = cfg.get("exit_scenarios", [])
        if scen:
            out.append("\n## 退出情景（无清算优先权假设，条款确认后修正）\n")
            out.append("| 情景 | 退出估值 | 年限 | 我们的回收 | MOIC | 隐含 IRR |")
            out.append("|---|---:|---:|---:|---:|---:|")
            for s in scen:
                ev = float(s["exit_value"])
                yrs = float(s.get("years", 5))
                proceeds = ours * ev
                moic = proceeds / our_amount if our_amount > 0 else 0
                irr = moic ** (1 / yrs) - 1 if moic > 0 and yrs > 0 else 0
                out.append(f"| {s['name']} | ${fmt(ev)} | {yrs:.0f} | ${fmt(proceeds)} | {moic:.2f}x | {pct(irr)} |")
            out.append("\n注：未建模清算优先权/participation/反稀释；若本轮或后续轮含 >1x preference，低估值情景的实际回收将低于上表。")
    return "\n".join(out)


# ----------------------------------------------------------------- demo data

DEMO_TOKEN = {
    "mode": "token", "project": "DemoProtocol", "total_supply": 1_000_000_000,
    "current_price": 0.15, "months_since_tge": 0,
    "allocations": [
        {"name": "Team", "category": "team", "pct": 20, "tge_unlock_pct": 0, "cliff_months": 12, "vesting_months": 24},
        {"name": "Investors-Seed", "category": "investor", "pct": 12, "tge_unlock_pct": 0, "cliff_months": 12, "vesting_months": 18, "cost_basis_fdv": 30_000_000},
        {"name": "Investors-A", "category": "investor", "pct": 10, "tge_unlock_pct": 0, "cliff_months": 12, "vesting_months": 18, "cost_basis_fdv": 80_000_000},
        {"name": "Ecosystem", "category": "ecosystem", "pct": 25, "tge_unlock_pct": 8, "cliff_months": 0, "vesting_months": 48},
        {"name": "Community Airdrop", "category": "community", "pct": 8, "tge_unlock_pct": 100},
        {"name": "Treasury", "category": "treasury", "pct": 25, "tge_unlock_pct": 4, "cliff_months": 0, "vesting_months": 60},
    ],
}

DEMO_EQUITY = {
    "mode": "equity", "project": "DemoCo",
    "rounds": [
        {"name": "Seed", "pre_money": 8_000_000, "raised": 2_000_000, "esop_added_pct": 10},
        {"name": "Series A", "pre_money": 40_000_000, "raised": 10_000_000},
    ],
    "our_investment": {"round": "Series A", "amount": 3_000_000},
    "future_rounds": [
        {"name": "Series B", "pre_money": 120_000_000, "raised": 30_000_000, "esop_added_pct": 5},
    ],
    "exit_scenarios": [
        {"name": "bear", "exit_value": 150_000_000, "years": 5},
        {"name": "base", "exit_value": 500_000_000, "years": 5},
        {"name": "bull", "exit_value": 1_500_000_000, "years": 6},
    ],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", help="假设 JSON 文件路径")
    ap.add_argument("--horizon", type=int, default=24, help="token 模式解锁表月数")
    ap.add_argument("--demo-token", action="store_true")
    ap.add_argument("--demo-equity", action="store_true")
    args = ap.parse_args()

    if args.demo_token:
        cfg = DEMO_TOKEN
    elif args.demo_equity:
        cfg = DEMO_EQUITY
    elif args.input:
        with open(args.input, encoding="utf-8") as f:
            cfg = json.load(f)
    else:
        ap.error("需要 --input 或 --demo-token / --demo-equity")

    mode = cfg.get("mode", "token")
    if mode == "token":
        print(run_token(cfg, args.horizon))
    elif mode == "equity":
        print(run_equity(cfg))
    else:
        sys.exit(f"未知 mode: {mode}")


if __name__ == "__main__":
    main()
