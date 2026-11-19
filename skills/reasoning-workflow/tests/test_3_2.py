"""Runtime regressions for optional evidence and task preparation."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from check_report_evidence import check
from prepare_task import prepare

ROOT = Path(__file__).resolve().parents[1]


class InfrastructureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "study.txt").write_text("Eight positive. Two negative.", encoding="utf-8")
        self.packet = {
            "sources": [{"id": k, "file": "study.txt", "origin": "register"} for k in ("A", "B")],
            "claims": [{"id": "result", "text": "Results vary.", "status": "contested",
                        "evidence": [{"source": "A", "quote": "Eight positive.", "role": "support"},
                                     {"source": "B", "quote": "Two negative.", "role": "counter"}]}]
        }
        self.profile = json.loads((ROOT / "tests/fixtures/standard_profile.json").read_text())

    def test_evidence_same_origin(self):
        self.assertEqual(check(self.packet, self.root)[0]["declared_origins"], ["register"])

    def test_evidence_changed_snapshot(self):
        (self.root / "study.txt").write_text("Two negative.")
        with self.assertRaisesRegex(ValueError, "quote missing"):
            check(self.packet, self.root)

    def test_unknown_and_contested_claims(self):
        claim = self.packet["claims"][0]
        claim["evidence"].pop()
        with self.assertRaisesRegex(ValueError, "counterevidence"):
            check(self.packet, self.root)
        claim.update(status="unknown", evidence=[])
        self.assertEqual(check(self.packet, self.root)[0]["passages"], 0)

    def test_missing_and_duplicate_sources(self):
        self.packet["claims"][0]["evidence"][0]["source"] = "absent"
        with self.assertRaisesRegex(ValueError, "unknown source"):
            check(self.packet, self.root)
        self.packet["sources"].append(self.packet["sources"][0])
        with self.assertRaisesRegex(ValueError, "Duplicate ID"):
            check(self.packet, self.root)

    def test_source_must_stay_with_packet(self):
        self.packet["sources"][0]["file"] = "../study.txt"
        with self.assertRaisesRegex(ValueError, "directory"):
            check(self.packet, self.root)

    def test_both_signal_entry_points(self):
        profile = ROOT / "tests/fixtures/standard_profile.json"
        for script, option in (("prepare_task.py", "--signal"), ("route_task.py", "--signals")):
            for signal, expected in (("ultra_requested", 0), ("ultra_requsted", 1)):
                out = subprocess.run([sys.executable, ROOT / "scripts" / script, profile,
                                      option, signal], capture_output=True, text=True)
                self.assertEqual(out.returncode, expected)
                result = json.loads(out.stdout)
                if expected:
                    self.assertIn("UNKNOWN_SIGNAL", result["errors"])
                else:
                    self.assertEqual(result["task_profile"]["depth_class"], "ultra")

    def test_on_demand_routes(self):
        for gap, ref in (("costly-ambiguity", "clarification-gate"),
                         ("design-reference", "specialist-resources"),
                         ("editing-voice", "writing-for-the-reader"),
                         ("claim-support", "research-to-report"),
                         ("release-install", "engineering-delivery")):
            for configured in (True, False):
                profile = dict(self.profile, active_gap_tags=[gap] if configured else [])
                result = prepare(profile, gap_tags=[] if configured else [gap])
                self.assertTrue(result["passed"], result)
                self.assertIn(ref, [r["reference_id"] for r in result["selected_references"]])
                self.assertFalse(result["authority_granted"])
        result = prepare(dict(self.profile, task_modes=[], depth_class="light"))
        self.assertEqual(result["selected_references"], [])
