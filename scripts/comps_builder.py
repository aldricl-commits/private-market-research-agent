#!/usr/bin/env python3
"""private-market-research skill · Comps 表构建与隐含估值计算器

用法：
    python scripts/comps_builder.py --input comps.json
    python scripts/comps_builder.py --demo

输入 JSON：target（含 metrics 与可选 proposed_valuation）、primary_comps（一级轮次）、
secondary_comps（二级锚：上市公司/流通 token）、discounts（折价组件，乘法叠加）。
输出：倍数分布、隐含估值区间、报价分位、文本版 football field。仅标准库。
"""

import argparse
import json
import statistics


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


def quartiles(vals):
    v = sorted(vals)
    n = len(v)
    med = statistics.median(v)
    q1 = statistics.median(v[: (n + 1) // 2]) if n >= 2 else v[0]
    q3 = statistics.median(v[n // 2:]) if n >= 2 else v[0]
    return v[0], q1, med, q3, v[-1]


def percentile_rank(vals, x):
    v = sorted(vals)
    below = sum(1 for e in v if e < x)
    equal = sum(1 for e in v if e == x)
    return (below + 0.5 * equal) / len(v)


def comp_table(comps, metric, title, extra_cols=()):
    lines = [f"\n## {title}（metric: {metric}）\n"]
    header = "| 名称 | " + " | ".join(extra_cols) + (" | " if extra_cols else "") + "估值 | metric 值 | 倍数 | 备注 |"
    sep = "|---|" + "---|" * len(extra_cols) + "---:|---:|---:|---|"
    lines += [header, sep]
    multiples = []
    for c in comps:
        mv = c.get("metrics", {}).get(metric)
        val = c.get("valuation")
        if mv and mv > 0 and val:
            mult = val / mv
            multiples.append(mult)
            mult_s = f"{mult:,.1f}x"
        else:
            mult_s = "n/a（缺 metric，不进统计）"
        extras = " | ".join(str(c.get(k.lower().replace(" ", "_"), c.get(k, ""))) for k in extra_cols)
        lines.append(f"| {c['name']} | " + (extras + " | " if extra_cols else "")
                     + f"${fmt(val)} | {fmt(mv)} | {mult_s} | {c.get('note', '')} |")
    return lines, multiples


def run(cfg):
    tgt = cfg["target"]
    metric = cfg.get("metric") or next(iter(tgt.get("metrics", {})), None)
    if not metric:
        raise SystemExit("target.metrics 为空且未指定 --metric")
    tval = tgt["metrics"].get(metric)
    proposed = tgt.get("proposed_valuation")

    out = [f"# Comps — {tgt['name']}（{tgt.get('stage', '')}）",
           f"\n- 对比 metric：**{metric}** = {fmt(tval)}",
           f"- 本轮报价：${fmt(proposed)}（{tgt.get('valuation_basis', '口径未注明')}）" if proposed else "- 本轮报价：未提供（仅输出隐含区间）"]

    sections = []
    prim = cfg.get("primary_comps", [])
    sec = cfg.get("secondary_comps", [])

    p_mult, s_mult = [], []
    if prim:
        lines, p_mult = comp_table(prim, metric, "一级轮次 comps", ("date", "round"))
        sections += lines
    if sec:
        lines, s_mult = comp_table(sec, metric, "二级锚 comps", ("kind",))
        sections += lines
    out += sections

    # 折价
    disc_parts = cfg.get("discounts", {}).get("components", [])
    combined = 1.0
    for d in disc_parts:
        combined *= (1 - d["pct"] / 100.0)
    total_disc = 1 - combined

    def implied_block(mult, label, discount=0.0):
        mn, q1, med, q3, mx = quartiles(mult)
        k = 1 - discount
        block = [f"\n### {label}",
                 f"- 倍数分布（n={len(mult)}）：min {mn:.1f}x ｜ Q1 {q1:.1f}x ｜ **中位 {med:.1f}x** ｜ Q3 {q3:.1f}x ｜ max {mx:.1f}x"]
        if discount > 0:
            disc_desc = "; ".join("{} {}%".format(d["name"], d["pct"]) for d in disc_parts)
            block.append(f"- 折价：{disc_desc} → 乘法叠加合计 **{total_disc*100:.0f}%**")
        if tval:
            lo, mid, hi = tval * q1 * k, tval * med * k, tval * q3 * k
            block.append(f"- 标的隐含估值区间：**${fmt(lo)} — ${fmt(mid)} — ${fmt(hi)}**（Q1—中位—Q3{'，折价后' if discount else ''}）")
            rng = (lo, hi, mid)
        else:
            rng = None
        if proposed and tval:
            implied_mult = proposed / tval / k if k > 0 else float("inf")
            pr = percentile_rank(mult, implied_mult)
            block.append(f"- 反向检验：报价 ${fmt(proposed)} → 隐含倍数 {proposed/tval:.1f}x"
                         + (f"（折价还原后对标 {implied_mult:.1f}x）" if discount else "")
                         + f"，位于该组第 **{pr*100:.0f} 分位**")
        return block, rng

    ranges = {}
    if p_mult:
        b, r = implied_block(p_mult, "一级轮次隐含区间")
        out += b
        if r:
            ranges["一级 comps"] = r
    if s_mult:
        b, r = implied_block(s_mult, "二级锚隐含区间（折价后）", total_disc)
        out += b
        if r:
            ranges["二级锚折价后"] = r

    # football field
    if ranges:
        all_lo = min(r[0] for r in ranges.values())
        all_hi = max(r[1] for r in ranges.values())
        if proposed:
            all_lo, all_hi = min(all_lo, proposed), max(all_hi, proposed)
        span = all_hi - all_lo or 1.0
        width = 44

        def bar(lo, hi):
            s = int((lo - all_lo) / span * width)
            e = max(s + 1, int((hi - all_lo) / span * width))
            return " " * s + "▓" * (e - s)

        out.append("\n## 估值对比图（football field）\n")
        out.append("```text")
        for name, (lo, hi, mid) in ranges.items():
            out.append(f"{name:<12} {bar(lo, hi)} {fmt(lo)}—{fmt(hi)}")
        if proposed:
            pos = int((proposed - all_lo) / span * width)
            out.append(f"{'本轮报价':<12} " + " " * pos + f"▼ {fmt(proposed)}")
        out.append("```")

    out.append("\n注：comps 的周期/阶段/口径调整依据 valuation-private.md 第 2–3 节；折价取值理由须在报告正文写明。")
    return "\n".join(out)


DEMO = {
    "target": {"name": "DemoProtocol", "stage": "Series A / pre-TGE",
               "metrics": {"annualized_fees": 12_000_000},
               "proposed_valuation": 300_000_000, "valuation_basis": "FDV, post-money"},
    "metric": "annualized_fees",
    "primary_comps": [
        {"name": "CompA", "date": "2025-11", "round": "A", "valuation": 250_000_000, "metrics": {"annualized_fees": 8_000_000}},
        {"name": "CompB", "date": "2026-02", "round": "A", "valuation": 400_000_000, "metrics": {"annualized_fees": 20_000_000}},
        {"name": "CompC", "date": "2025-07", "round": "B", "valuation": 600_000_000, "metrics": {"annualized_fees": 35_000_000}},
        {"name": "CompD", "date": "2026-05", "round": "A", "valuation": 180_000_000, "metrics": {"annualized_fees": 6_000_000}},
    ],
    "secondary_comps": [
        {"name": "ListedX", "kind": "token", "valuation": 1_200_000_000, "metrics": {"annualized_fees": 90_000_000}},
        {"name": "ListedY", "kind": "token", "valuation": 800_000_000, "metrics": {"annualized_fees": 45_000_000}},
        {"name": "ListedZ", "kind": "equity", "valuation": 5_000_000_000, "metrics": {"annualized_fees": 400_000_000}},
    ],
    "discounts": {"components": [{"name": "流动性", "pct": 25}, {"name": "阶段风险", "pct": 20}]},
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input")
    ap.add_argument("--metric")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    if args.demo:
        cfg = DEMO
    elif args.input:
        with open(args.input, encoding="utf-8") as f:
            cfg = json.load(f)
    else:
        ap.error("需要 --input 或 --demo")
    if args.metric:
        cfg["metric"] = args.metric
    print(run(cfg))


if __name__ == "__main__":
    main()
