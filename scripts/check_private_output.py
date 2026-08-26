#!/usr/bin/env python3
"""private-market-research skill · 报告完整性与纪律检查器

用法：
    python scripts/check_private_output.py --report report.md [--industry crypto-defi] [--mode deep|memo]

不传 --industry 时从报告头部的 `行业附录: <slug>` 声明解析。
P0 = 必须修正；P1 = 修正或在报告中显式解释；P2 = 建议。存在 P0 时退出码为 1。
仅使用 Python 标准库。
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import List

RULES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "industry-rules-private.json")

SOURCE_TAGS = ["[链上]", "[申报/审计]", "[公司]", "[第三方]", "[未验证]",
               "[on-chain]", "[filings/audited]", "[company]", "[third-party]", "[unverified]"]
MISSING_MARKERS = ["未获取到", "not obtained", "not available", "未验证", "待补"]
METHOD_MARKERS = {
    "轮次 comps": ["轮次 comps", "轮次comps", "round comps", "一级 comps", "一级comps"],
    "二级锚折价": ["二级锚", "secondary anchor", "折价后隐含", "liquidity discount"],
    "token economics": ["token economics", "解锁", "unlock", "fdv/流通", "供给压力"],
    "rNPV": ["rnpv", "成功概率加权", "risk-adjusted npv"],
    "情景/退出": ["退出情景", "exit scenario", "情景表", "scenario table", "irr", "moic"],
    "用户/收入倍数": ["用户价值倍数", "fdv/fees", "fdv/revenue", "ev/arr", "p/s", "ev/收入", "licensing comps"],
}


@dataclass
class Issue:
    severity: str
    code: str
    message: str
    detail: str = ""


@dataclass
class Report:
    issues: List[Issue] = field(default_factory=list)

    def add(self, severity, code, message, detail=""):
        self.issues.append(Issue(severity, code, message, detail))


def load_rules():
    try:
        with open(RULES_PATH, encoding="utf-8") as f:
            return json.load(f)["industries"]
    except Exception as e:
        print(f"警告：无法读取行业规则 {RULES_PATH}: {e}", file=sys.stderr)
        return {}


def section(text, markers, stop=None):
    """截取从任一 marker 所在章节标题起到「同级或更高级标题」的文本。

    章节常含下级小标题（### 6.1 ...），若在下级标题处截断会漏掉正文表格并误报，
    因此这里按匹配到的标题级别决定终止条件：只在 # 数量 <= 匹配级别的标题处结束。
    stop 显式传入时沿用旧行为（保留给调用方覆盖）。无标题匹配时退回全文首次出现。"""
    lines = text.splitlines(keepends=True)
    low_markers = [m.lower() for m in markers]
    pos = 0
    heading_hit = None
    level = 3
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("#") and any(m in line.lower() for m in low_markers):
            heading_hit = pos
            level = len(stripped) - len(stripped.lstrip("#"))
            break
        pos += len(line)
    if heading_hit is None:
        low = text.lower()
        hits = [low.find(m) for m in low_markers if low.find(m) >= 0]
        if not hits:
            return None
        heading_hit = min(hits)
        level = 3  # 非标题命中：沿用旧的“遇任意 1-3 级标题即止”
    rest = text[heading_hit:]
    pattern = stop or (r"\n#{1," + str(max(1, level)) + r"} ")
    nxt = re.search(pattern, rest[10:])
    return rest[: 10 + nxt.start()] if nxt else rest


def count_table_rows(chunk):
    rows = [l for l in chunk.splitlines() if l.strip().startswith("|")]
    # 去掉表头与分隔行
    return max(0, len([r for r in rows if not re.match(r"^\|[\s:\-|]+\|?$", r.strip())]) - 1)


def check(text, industries, rules, mode, rep):
    low = text.lower()

    # ---------- P0：数据可得性声明框 ----------
    m = re.search(r"(数据可得性等级|data availability grade)\s*[:：]?\s*\**([ABCD])\**", text, re.I)
    if not m:
        rep.add("P0", "AVAIL-GRADE", "缺少数据可得性等级声明（报告头部必须有 A/B/C/D 等级）")
        grade = None
    else:
        grade = m.group(2).upper()

    mix = re.search(r"(来源结构|source mix)[:：]?(.{0,220})", text, re.I)
    if not mix:
        rep.add("P0", "AVAIL-MIX", "缺少来源结构占比行（链上/申报/公司/第三方/未验证 五类占比）")
    else:
        nums = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*%", mix.group(2))]
        if len(nums) < 3:
            rep.add("P0", "AVAIL-MIX", "来源结构占比不完整（至少应有三类占比数字）", mix.group(2).strip()[:120])
        elif not (95 <= sum(nums) <= 105):
            rep.add("P0", "AVAIL-MIX-SUM", f"来源结构占比合计 {sum(nums):.0f}%，应约等于 100%")

    if not re.search(r"关键缺口|key gaps", text, re.I):
        rep.add("P1", "AVAIL-GAPS", "声明框缺少关键缺口清单（未获取到的关键数据及影响）")

    # 等级与结论强度
    if grade == "D" and re.search(r"投资观点[:：]\s*\**\s*(attractive|invest\b)", low):
        rep.add("P0", "GRADE-OVERREACH", "数据等级 D 但给出了明确投资观点——D 级只能输出 preliminary screen")

    # ---------- P0：行业附录声明（batch 模式跨行业，跳过） ----------
    if mode != "batch":
        if not industries:
            rep.add("P0", "IND-DECL", "缺少 `行业附录: <slug>` 声明或无法解析")
        else:
            for slug in industries:
                if rules and slug not in rules:
                    rep.add("P0", "IND-SLUG", f"行业 slug `{slug}` 不在 industry-rules-private.json 注册表中")

    # ---------- P0：Industry mapping 与二级锚（batch 模式跳过） ----------
    if mode != "batch":
        map_sec = section(text, ["industry mapping", "产业地图", "行业地图", "价值链分层"])
        if map_sec is None:
            rep.add("P0", "MAP-MISSING", "缺少 Industry Mapping（产业地图）章节")
        else:
            if not re.search(r"二级锚|secondary anchor", map_sec, re.I):
                rep.add("P0", "MAP-ANCHOR", "产业地图分层表缺少「二级锚」列（每层必须回答有无上市公司/流通 token 锚）")
            if count_table_rows(map_sec) < 2:
                rep.add("P1", "MAP-LAYERS", "产业地图分层表行数过少（应覆盖价值链多层）")

    # ---------- P0：估值多方法（batch 模式跳过） ----------
    if mode != "batch":
        found_methods = [name for name, pats in METHOD_MARKERS.items() if any(p in low for p in pats)]
        if len(found_methods) < 2:
            rep.add("P0", "VAL-METHODS", f"估值方法标记不足两种（检测到：{found_methods or '无'}）",
                    "至少两法交叉：轮次 comps / 二级锚折价 / token economics / rNPV / 情景退出")
        if not re.search(r"irr|moic", low):
            rep.add("P0", "VAL-RETURN", "估值章缺少隐含 IRR/MOIC——每个估值结论必须绑定退出路径与回报")
        if not re.search(r"退出|exit", low):
            rep.add("P1", "VAL-EXIT", "未检测到退出路径讨论（下轮/TGE/IPO/M&A）")

    # ---------- P0：风险/反方论证 ----------
    # deep 模式要求 Pre-mortem；memo 模式对齐 house 结构用 Risks / Open Questions（rubric 第 3 节：少于 3 条为弱 memo）
    risk_markers = (["risks", "open questions", "风险", "pre-mortem", "反方论证"] if mode == "memo"
                    else ["pre-mortem", "反方论证", "失败情景"])
    pm = section(text, risk_markers) if mode != "batch" else "SKIP"
    if pm == "SKIP":
        pass
    elif pm is None:
        rep.add("P0", "PREMORTEM", "缺少风险章节（deep 模式为 Pre-mortem/反方论证；memo 模式为 Risks / Open Questions）")
    else:
        n = count_table_rows(pm)
        if n < 3:
            n_list = len(re.findall(r"^\s*(?:[-*•]|\d+[.、])\s+", pm, re.M))
            if max(n, n_list) < 3:
                rep.add("P0", "PREMORTEM-N", f"风险/失败情景不足 3 条（表格行 {n} / 列表项 {n_list}）")

    # ---------- P1 ----------
    tag_count = sum(text.count(t) for t in SOURCE_TAGS)
    if tag_count < 8:
        rep.add("P1", "SOURCE-TAGS", f"来源标签使用过少（{tag_count} 处，建议 ≥8）——关键数字应带 [链上]/[公司] 等标签")

    if mode != "batch":
        team = section(text, ["团队", "team diligence", "## 四"])
        if team is None or not re.search(r"核查|verification|红旗|red flag|全职|full.?time", team or "", re.I):
            rep.add("P1", "TEAM", "团队章节缺少核查表/红旗清单/全职状态（team-diligence.md + rubric 第 4 节）")

    if mode == "deep":
        kt = len(re.findall(r"本章要点|key takeaways", text, re.I))
        if kt < 5:
            rep.add("P1", "TAKEAWAYS", f"「本章要点」出现 {kt} 次（deep 模式建议 ≥5）")

    if mode != "batch" and not re.search(r"投资观点|investment view|建议动作|recommended action|recommendation|invest / pass / track", text, re.I):
        rep.add("P1", "CONCLUSION-BOX", "缺少结论框（投资观点/建议动作/Recommendation）")

    if not re.search(r"来源与时间戳|sources and timestamps", text, re.I):
        rep.add("P1", "SOURCES-APPENDIX", "缺少来源与时间戳清单附录")

    if mode == "deep" and not re.search(r"置信度自评|综合置信度|confidence self|overall confidence", text, re.I):
        rep.add("P1", "CONFIDENCE", "缺少置信度自评表")

    if mode == "deep" and not re.search(r"监控清单|monitoring", text, re.I):
        rep.add("P1", "MONITORING", "缺少监控清单（3–5 项带阈值与验证日期）")
    if mode == "memo" and not re.search(r"验证点|监控|monitoring|watch|move to \d", text, re.I):
        rep.add("P1", "MONITORING", "缺少投后验证点（memo 第 15 节：投后 6/12 个月验证点与否决信号）")

    if not any(mk in low for mk in [m.lower() for m in MISSING_MARKERS]):
        rep.add("P1", "NO-MISSING", "全文没有任何「未获取到/待补」标注——一级研究数据全齐备极不寻常，请核实是否隐瞒了缺口")

    # 行业必备 KPI 组
    for slug in industries:
        rule = rules.get(slug)
        if not rule:
            continue
        for grp in rule.get("required_groups", []):
            if not any(t.lower() in low for t in grp["terms"]):
                sev = "P1" if rule.get("tier") == "native" else "P2"
                rep.add(sev, "IND-KPI", f"[{slug}] 缺少必备 KPI 组「{grp['label']}」", f"期望词之一：{', '.join(grp['terms'][:6])}")

    # ---------- P2 ----------
    if any(s.startswith("crypto-") for s in industries) and "fdv" not in low:
        rep.add("P2", "FDV", "crypto 标的未见 FDV 口径——倍数应用 FDV 计算并与流通市值并列")
    if text.count("**") < 6:
        rep.add("P2", "STYLE-BOLD", "加粗结论过少——每章先结论后论据，关键论点句应加粗")

    # ---------- memo 模式附加（v1：对齐 ic-memo-template.md 模式 A + memo-rubric.md） ----------
    if mode == "memo":
        if not re.search(r"条款|deal terms|deal structure", text, re.I):
            rep.add("P0", "MEMO-TERMS", "IC memo 缺少条款表（金额/equity 与 token 双轨估值口径/占比/特殊结构），条款未知时应列「待补条款」")
        meta_hits = sum(1 for kw in ["sector", "stage", "geography", "deal team", "source"] if kw in low)
        if meta_hits < 3:
            rep.add("P1", "MEMO-META", "缺少头部元数据行（Sector/Thesis/Geography/Chain/Deal Team/Source/Stage）")
        if not re.search(r"协同|synergy|strategic fit|ecosystem fit", text, re.I):
            rep.add("P1", "MEMO-SYNERGY", "缺少生态协同分析（house 一等公民：与链/交易所/组合的协同形态与条件）")
        if not re.search(r"为什么能拿到|adverse selection", text, re.I):
            rep.add("P1", "MEMO-ADVSEL", "缺少 adverse selection 检验（我们为什么能拿到这个 deal）")
        if not re.search(r"use of proceeds|资金用途|runway|burn", text, re.I):
            rep.add("P1", "MEMO-PROCEEDS", "缺少 runway/burn 核算")
        if not re.search(r"team feedback|ic feedback|recommendation|建议动作|评分标尺", text, re.I):
            rep.add("P1", "MEMO-RECO", "缺少 Recommendation 或 IC/Team Feedback 骨架区（评分标尺见 memo-rubric.md；不得虚构评分）")
        if len(re.findall(r"已验证|已确认|直接确认|未能独立验证|未验证|verified|confirmed with|not verified", text, re.I)) < 2:
            rep.add("P2", "MEMO-VERIFY", "验证状态标注过少——关键声称应显式写明「已验证/未能验证」（rubric 第 2 节）")
        if not re.search(r"circular|循环需求|独立需求|关联方", text, re.I):
            rep.add("P2", "MEMO-CIRCULAR", "未见循环需求检验——committed 资金/量中来自战投或关联生态的部分应单独拆出")

    # ---------- batch 模式（批量评审，ic-memo-template.md 模式 B）：轻量结构检查 ----------
    if mode == "batch":
        for kw, label in [("product / solution", "Product / Solution"), ("investment thesis", "Investment Thesis"),
                          ("investment terms", "Investment Terms"), ("risks", "Risks / Open Questions")]:
            cnt = low.count(kw)
            if cnt < 2:
                rep.add("P1", "BATCH-STRUCT", f"批量评审中「{label}」仅出现 {cnt} 次——每个项目应有完整十节")
        if not re.search(r"标准条款|standard terms|评分标尺|log scale", text, re.I):
            rep.add("P1", "BATCH-HEADER", "批次头部缺少标准条款与评分标尺声明")


def parse_industries(text):
    m = re.search(r"(?:行业附录|industry appendix)\s*[:：]\s*([a-z0-9\-,\s]+)", text, re.I)
    if not m:
        return []
    return [s.strip().lower() for s in m.group(1).split(",") if s.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--industry", action="append", default=[])
    ap.add_argument("--mode", choices=["deep", "memo", "batch"], default=None,
                    help="deep=深度研究；memo=单 deal IC memo；batch=批量评审（residency/孵化批次）")
    ap.add_argument("--language", choices=["zh", "en"], default=None, help="预留：当前检查中英标记均接受")
    args = ap.parse_args()

    with open(args.report, encoding="utf-8") as f:
        text = f.read()

    head = text[:400]
    if args.mode:
        mode = args.mode
    elif re.search(r"residency|批量评审|batch review", head, re.I):
        mode = "batch"
    elif re.search(r"ic\s*memo", head, re.I):
        mode = "memo"
    else:
        mode = "deep"
    industries = [s.lower() for s in args.industry] or parse_industries(text)
    rules = load_rules()

    rep = Report()
    check(text, industries, rules, mode, rep)

    order = {"P0": 0, "P1": 1, "P2": 2}
    rep.issues.sort(key=lambda i: order[i.severity])
    p0 = sum(1 for i in rep.issues if i.severity == "P0")
    p1 = sum(1 for i in rep.issues if i.severity == "P1")

    print(f"检查报告：{os.path.basename(args.report)}（mode={mode}，行业={industries or '未声明'}）")
    print(f"结果：P0 × {p0} ｜ P1 × {p1} ｜ P2 × {sum(1 for i in rep.issues if i.severity == 'P2')}\n")
    for i in rep.issues:
        line = f"[{i.severity}] {i.code}: {i.message}"
        if i.detail:
            line += f"\n    {i.detail}"
        print(line)
    if not rep.issues:
        print("全部检查通过。")
    sys.exit(1 if p0 else 0)


if __name__ == "__main__":
    main()
