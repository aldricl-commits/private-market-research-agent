#!/usr/bin/env python3
"""private-market-research skill · 脚本回归测试

运行：python3 tests/test_scripts.py
覆盖：token_economics（token/equity demo）、comps_builder（demo）、
check_private_output（通过/拦截两个 fixture）。仅标准库。
"""

import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
FIXTURES = os.path.join(ROOT, "tests", "fixtures")
PY = sys.executable


def run(args):
    return subprocess.run([PY] + args, capture_output=True, text=True, cwd=ROOT)


class TokenEconomicsTest(unittest.TestCase):
    def test_token_demo(self):
        r = run([os.path.join(SCRIPTS, "token_economics.py"), "--demo-token"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("FDV $150.0M", r.stdout)
        self.assertIn("解锁与供给压力表", r.stdout)
        # 内部人 42% 应触发红旗
        self.assertIn("内部人（团队+投资人+顾问）份额 42.0% > 40%", r.stdout)
        # 投资人 MOIC：150M FDV / 30M cost = 5.0x
        self.assertIn("5.0x", r.stdout)

    def test_equity_demo(self):
        r = run([os.path.join(SCRIPTS, "token_economics.py"), "--demo-equity"])
        self.assertEqual(r.returncode, 0, r.stderr)
        # Series A 投 3M @ post 50M = 6%，经 B 轮 20%+5% 稀释 → 4.50%
        self.assertIn("4.50%", r.stdout)
        self.assertIn("MOIC", r.stdout)
        self.assertIn("清算优先权", r.stdout)  # 无 prefs 假设的显式注记


class CompsBuilderTest(unittest.TestCase):
    def test_demo(self):
        r = run([os.path.join(SCRIPTS, "comps_builder.py"), "--demo"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("中位 25.0x", r.stdout)          # 一级 comps 中位
        self.assertIn("乘法叠加合计 **40%**", r.stdout)  # (1-.25)(1-.20) → 40%
        self.assertIn("football field", r.stdout)
        self.assertIn("100 分位", r.stdout)             # 报价超出二级锚全组


class CheckerTest(unittest.TestCase):
    def test_pass_fixture(self):
        r = run([os.path.join(SCRIPTS, "check_private_output.py"),
                 "--report", os.path.join(FIXTURES, "deep_research_pass.md")])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("P0 × 0", r.stdout)

    def test_fail_fixture(self):
        r = run([os.path.join(SCRIPTS, "check_private_output.py"),
                 "--report", os.path.join(FIXTURES, "memo_fail.md"), "--mode", "memo"])
        self.assertEqual(r.returncode, 1)
        for code in ["AVAIL-GRADE", "MAP-MISSING", "VAL-METHODS", "PREMORTEM", "MEMO-TERMS",
                     "MEMO-SYNERGY", "MEMO-META", "MEMO-RECO"]:
            self.assertIn(code, r.stdout)

    def test_batch_fixture(self):
        # batch 模式：跳过单 deal 的 MAP/VAL/IND 检查，但声明框仍是 P0，且十节结构不足要报 BATCH-STRUCT
        r = run([os.path.join(SCRIPTS, "check_private_output.py"),
                 "--report", os.path.join(FIXTURES, "batch_fail.md")])
        self.assertEqual(r.returncode, 1)  # AVAIL-GRADE 仍为 P0
        self.assertIn("mode=batch", r.stdout)  # 自动识别 residency
        self.assertIn("BATCH-STRUCT", r.stdout)
        self.assertIn("BATCH-HEADER", r.stdout)
        self.assertNotIn("MAP-MISSING", r.stdout)
        self.assertNotIn("VAL-METHODS", r.stdout)


class SectionParsingTest(unittest.TestCase):
    """回归：章节内含下级小标题（### 6.1）时，section() 不得在小标题处截断。
    此前的实现会漏掉小标题之后的表格，对结构良好的报告误报 P0。"""

    def test_subheadings_do_not_truncate(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "chk", os.path.join(SCRIPTS, "check_private_output.py"))
        chk = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(chk)

        doc = (
            "## 六、风险与反方论证（Pre-mortem）\n\n本章要点：略。\n\n"
            "### 6.1 Pre-mortem\n\n"
            "| 失败情景 | 触发机制 |\n|---|---|\n| A | a |\n| B | b |\n| C | c |\n\n"
            "### 6.2 其他\n\n正文。\n\n"
            "## 七、结论\n\n结论正文。\n"
        )
        sec = chk.section(doc, ["pre-mortem", "反方论证"])
        self.assertIsNotNone(sec)
        self.assertEqual(chk.count_table_rows(sec), 3)      # 三条失败情景都在
        self.assertIn("6.2", sec)                            # 下级小标题不截断
        self.assertNotIn("七、结论", sec)                     # 同级标题正确终止


if __name__ == "__main__":
    unittest.main(verbosity=2)
