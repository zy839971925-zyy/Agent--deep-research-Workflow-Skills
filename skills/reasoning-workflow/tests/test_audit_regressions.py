import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from route_resources import select
from routing_core import route_task
from test_workflow import BASE_PROFILE


class RoutingBoundaries(unittest.TestCase):
    def setUp(self):
        self.index = json.loads((ROOT / "routing-index.json").read_text())
        self.profile = dict(BASE_PROFILE, depth_class="standard")
        self.route = route_task(self.profile)

    def test_zero_budget_loads_nothing(self):
        self.route["reference_phase_limit"] = 0
        self.assertEqual(select(self.index, self.route, self.profile, ["decomposition"]), [])

    def test_stale_route_rejected_by_library(self):
        self.route["profile_version"] = 0
        with self.assertRaises(ValueError):
            select(self.index, self.route, self.profile, [])

    def test_deep_routes_include_verification_family(self):
        self.assertIn("audit-verification", route_task(dict(BASE_PROFILE, depth_class="deep"))["required_families"])

    def test_future_evidence_need_cannot_authorize_prior_retrieval(self):
        from evaluate_run import validate
        run = {"events": [{"event": "evidence_retrieval"},
                          {"event": "problem_model_created", "problem_model_ref": "P"},
                          {"event": "evidence_need_created", "evidence_need_ref": "E"}]}
        codes = {f["code"] for f in validate({}, run)}
        self.assertIn("EVIDENCE_RETRIEVAL_WITHOUT_NEED", codes)
        self.assertIn("EVIDENCE_NEED_WITHOUT_MODEL", codes)

    def test_explicit_empty_capability_routes_block_readiness(self):
        from runtime_core import compute_ready_nodes
        self.assertEqual(compute_ready_nodes({"nodes": [{"node_id": "N"}]}, {}, {}), [])

    def test_invalid_schedule_returns_findings(self):
        from runtime_core import validate_schedule
        self.assertTrue(validate_schedule({"nodes": []}, {"assignments": [None]}, ROOT))

    def test_optional_family_is_allowed(self):
        from evaluate_run import validate
        run = {"route": {"required_families": [], "optional_families": ["deep-research"]},
               "events": [{"event": "reference_loaded", "family": "deep-research"}]}
        self.assertNotIn("UNROUTED_FAMILY_REFERENCE", {f["code"] for f in validate({}, run)})

    def test_canonical_learning_requires_offline_evaluation(self):
        from learning_core import validate_learning_semantics
        record = {"tier": 3, "status": "promoted", "regression_refs": ["R"],
                  "baseline_comparison_ref": "B", "dual_review_ref": "D", "rollback_ref": "RB"}
        self.assertTrue(validate_learning_semantics(record))

    def test_unknown_requirement_representation_returns_finding(self):
        from test_validators import base_question
        from validate_delivery import validate
        state = base_question()
        state["requirements"] = [{"id": "REQ", "record_type": "requirement", "declared_status": "satisfied"}]
        manifest = {"requirements": [{"id": "REQ", "represents": ["missing"]}]}
        findings, _ = validate(state, manifest)
        self.assertIn("REQ_REPRESENTS_REF", {f.code for f in findings})


class DistributionBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.temp.name)
        subprocess.run([sys.executable, str(ROOT / "scripts/build_distributions.py"),
                        "--source", str(ROOT), "--out-dir", str(cls.out)], check=True, stdout=subprocess.DEVNULL)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def validate(self, modular):
        return subprocess.run([sys.executable, str(ROOT / "scripts/validate_distribution.py"),
                               str(self.out / "reasoning-workflow-portable.zip"), str(modular)],
                              capture_output=True, text=True)

    def rewrite(self, predicate, replacement=None):
        target = self.out / "modified.zip"
        with zipfile.ZipFile(self.out / "reasoning-workflow-modular.zip") as src, zipfile.ZipFile(target, "w") as dst:
            for item in src.infolist():
                if predicate(item.filename):
                    dst.writestr(item, replacement if replacement is not None and item.filename.endswith("SEMANTIC_MANIFEST.json") else src.read(item))
        return target

    def test_valid_distribution(self):
        self.assertEqual(self.validate(self.out / "reasoning-workflow-modular.zip").returncode, 0)

    def test_missing_family_rejected(self):
        target = self.rewrite(lambda n: "/skills/deep-research/" not in n)
        self.assertNotEqual(self.validate(target).returncode, 0)

    def test_mismatched_modular_manifest_rejected(self):
        self.assertNotEqual(self.validate(self.rewrite(lambda n: True, b'{"canonical_hashes":{}}')).returncode, 0)

    def test_reproducible_zip_metadata(self):
        with zipfile.ZipFile(self.out / "reasoning-workflow-portable.zip") as z:
            self.assertTrue(all(i.date_time == (1980, 1, 1, 0, 0, 0) for i in z.infolist()))

    def test_source_manifest_is_current(self):
        import hashlib
        manifest = json.loads((ROOT / "SEMANTIC_MANIFEST.json").read_text())["canonical_hashes"]
        for rel, digest in manifest.items():
            self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), digest, rel)
