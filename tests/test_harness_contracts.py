"""Public, synthetic regressions for the installable workflow contracts."""

from __future__ import annotations

import copy
import json
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "skills" / "reasoning-workflow"
sys.path.insert(0, str(ROOT / "scripts"))

from learning_core import retrieve  # noqa: E402
from route_resources import select  # noqa: E402
from routing_core import recheck_profile, route_is_stale, route_task  # noqa: E402
from runtime_core import compute_node_contract_hash, validate_schedule  # noqa: E402
from validate_delivery import validate as validate_delivery  # noqa: E402
from validate_dual_verification import validate as validate_review  # noqa: E402


def profile(**changes):
    result = {
        "profile_version": 1,
        "lane": "question",
        "depth_class": "ultra",
        "autonomy_class": "A",
        "reasoning_breadth": "deep",
        "evidence_depth": "deep",
        "challenge_depth": "deep",
        "verification_depth": "deep",
        "governance_depth": "standard",
        "routing_confidence": "high",
        "task_modes": ["research"],
    }
    result.update(changes)
    return result


def node(node_id, *, depends_on=(), resource_locks=()):
    result = {
        "node_id": node_id,
        "objective": node_id,
        "depends_on": list(depends_on),
        "output_contract": {},
        "completion_contract": {},
        "verification_contract": {},
        "parallel_policy": "allowed",
        "resource_locks": list(resource_locks),
    }
    result["node_contract_hash"] = compute_node_contract_hash(result)
    return result


def assignment(n, **changes):
    result = {
        "node_id": n["node_id"],
        "node_contract_hash": n["node_contract_hash"],
        "executor_id": "manager",
        "executor_kind": "manager",
        "attempt_id": n["node_id"] + "-1",
    }
    result.update(changes)
    return result


def schedule(nodes, assignments, *, completed=(), mode="parallel"):
    plan = {"schema_version": "1.1", "plan_id": "p", "plan_version": 1, "objective": "example", "nodes": nodes}
    sched = {
        "schema_version": "1.1", "schedule_id": "s", "schedule_version": 1,
        "plan_id": "p", "based_on_plan_version": 1, "mode": mode, "scope": "wave",
        "assignments": assignments, "completed_prerequisite_refs": list(completed), "deferred_nodes": [],
    }
    return plan, sched


def codes(findings):
    return {f.code if hasattr(f, "code") else f["code"] for f in findings}


class ScheduleContracts(unittest.TestCase):
    def test_shared_resource_lock_conflicts_even_in_different_workspaces(self):
        a, b = node("a", resource_locks=["external-api"]), node("b", resource_locks=["external-api"])
        plan, sched = schedule([a, b], [
            assignment(a, concurrency_group="g", isolation_mode="isolated_workspace", workspace_ref="one"),
            assignment(b, concurrency_group="g", isolation_mode="isolated_workspace", workspace_ref="two"),
        ])
        self.assertIn("PARALLEL_STATE_CONFLICT", codes(validate_schedule(plan, sched, ROOT)))

    def test_disjoint_locks_are_parallel_safe(self):
        a, b = node("a", resource_locks=["api-1"]), node("b", resource_locks=["api-2"])
        plan, sched = schedule([a, b], [assignment(a, concurrency_group="g"), assignment(b, concurrency_group="g")])
        self.assertNotIn("PARALLEL_STATE_CONFLICT", codes(validate_schedule(plan, sched, ROOT)))

    def test_completed_prerequisite_needs_a_verified_ledger(self):
        a, b = node("a"), node("b", depends_on=["a"])
        plan, sched = schedule([a, b], [assignment(b)], completed=["a"])
        self.assertIn("SCHEDULE_PREREQUISITE_NOT_VERIFIED", codes(validate_schedule(plan, sched, ROOT)))
        verified = {"schema_version": "1.0", "plan_id": "p", "plan_version": 1, "state_version": 1, "nodes": [
            {"node_id": "a", "node_contract_hash": a["node_contract_hash"], "effective_status": "verified_complete", "updated_at": "2026-09-26"},
        ]}
        self.assertNotIn("SCHEDULE_PREREQUISITE_NOT_VERIFIED", codes(validate_schedule(plan, sched, ROOT, verified)))
        verified["nodes"][0]["node_contract_hash"] = "sha256:" + "0" * 64
        self.assertIn("NODE_LEDGER_STALE_CONTRACT", codes(validate_schedule(plan, sched, ROOT, verified)))

    def test_malformed_ledger_is_a_finding_not_a_crash(self):
        a, b = node("a"), node("b", depends_on=["a"])
        plan, sched = schedule([a, b], [assignment(b)], completed=["a"])
        self.assertIn("SCHEMA", codes(validate_schedule(plan, sched, ROOT, {"nodes": "invalid"})))


class DeliveryContracts(unittest.TestCase):
    def setUp(self):
        self.state = {
            "schema_version": "2.0", "work_id": "w", "state_version": 1,
            "lane": "action", "declared_status": "closed", "objective": "deliver", "updated_at": "2026-09-26",
            "artifacts": [{"id": "artifact", "record_type": "artifact", "materiality": "material", "declared_status": "current"}],
        }
        self.manifest = {
            "schema_version": "2.0", "work_id": "w", "state_version": 1, "generated_at": "2026-09-26",
            "requirements": [], "acceptance_criteria": [],
            "artifacts": [{"id": "artifact", "role": "deliverable", "declared_current": True}],
            "declared_delivery_ready": True,
        }

    def test_material_current_artifact_requires_a_path(self):
        for root in (None, Path(".")):
            with self.subTest(root=root):
                findings, computed = validate_delivery(self.state, self.manifest, root)
                self.assertIn("ART_PATH_REQUIRED", codes(findings))
                self.assertFalse(computed["computed_delivery_ready"])

    def test_current_artifact_cannot_hide_behind_false_flag(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["artifacts"][0]["declared_current"] = False
        findings, computed = validate_delivery(self.state, manifest)
        self.assertIn("ART_NOT_CURRENT", codes(findings))
        self.assertFalse(computed["computed_delivery_ready"])

    def test_existing_current_artifact_can_be_delivered(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "report.txt").write_text("result")
            self.manifest["artifacts"][0]["path"] = "report.txt"
            findings, computed = validate_delivery(self.state, self.manifest, Path(directory))
            self.assertNotIn("ART_FILE_MISSING", codes(findings))
            self.assertTrue(computed["computed_delivery_ready"])


class ReviewContracts(unittest.TestCase):
    def record(self, layer2_verdict, reconciliation="not_required"):
        return {
            "verification_id": "v", "mode": "dual", "solver_id": "solver", "solver_context_id": "c1",
            "layer1": {"verdict": "pass", "verification_refs": ["l1"]},
            "layer2": {
                "reviewer_id": "reviewer", "reviewer_context_id": "c2", "solver_transcript_included": False,
                "independence_basis": ["fresh_context"], "verdict": layer2_verdict,
            },
            "reconciliation_status": reconciliation,
        }

    def test_second_layer_failure_cannot_close_as_not_required(self):
        self.assertIn("REVIEW_CONFLICT_UNRESOLVED", codes(validate_review(self.record("fail"), ROOT)))

    def test_reconciliation_without_evidence_cannot_close(self):
        self.assertIn("RECONCILIATION_EVIDENCE_REQUIRED", codes(validate_review(self.record("fail", "reconciled"), ROOT)))

    def test_consistent_pass_needs_no_reconciliation(self):
        self.assertEqual(validate_review(self.record("pass"), ROOT), [])


class RoutingContracts(unittest.TestCase):
    def test_changing_profile_content_invalidates_route_without_version_bump(self):
        before = profile()
        route = route_task(before)
        after = profile(autonomy_class="D")
        self.assertTrue(route_is_stale(route, after))

    def test_index_change_invalidates_route(self):
        p = profile()
        route = route_task(p)
        self.assertTrue(route_is_stale(route, p, index_fingerprint="sha256:" + "0" * 64))

    def test_changed_resource_index_is_rejected(self):
        p = profile()
        route = route_task(p)
        index = json.loads((ROOT / "routing-index.json").read_text())
        index["references"][0]["default_priority"] += 1
        with self.assertRaisesRegex(ValueError, "STALE_ROUTE"):
            select(index, route, p, [])

    def test_tampered_route_cannot_skip_references(self):
        p = profile()
        route = route_task(p)
        route["reference_phase_limit"] = 0
        with self.assertRaisesRegex(ValueError, "STALE_ROUTE"):
            select(json.loads((ROOT / "routing-index.json").read_text()), route, p, [])

    def test_ultra_explicit_request_loads_overlay_with_multiple_gaps(self):
        p = profile(active_gap_tags=["framing", "deep-research", "evidence", "ultra", "verification"])
        selected = select(json.loads((ROOT / "routing-index.json").read_text()), route_task(p), p, [])
        self.assertIn("ultra-research", [item["reference_id"] for item in selected])
        self.assertLessEqual(len(selected), route_task(p)["reference_phase_limit"])

    def test_information_target_gap_routes_to_navigation_without_crowding_ultra(self):
        index = json.loads((ROOT / "routing-index.json").read_text())
        for depth in ("deep", "ultra"):
            with self.subTest(depth=depth):
                p = profile(depth_class=depth, active_gap_tags=["information-target"])
                selected = select(index, route_task(p), p, [])
                ids = [item["reference_id"] for item in selected]
                self.assertIn("information-target-navigation", ids)
                self.assertTrue((ROOT / "references/information-target-navigation.md").is_file())
                if depth == "ultra":
                    self.assertIn("ultra-research", ids)
                self.assertLessEqual(len(ids), route_task(p)["reference_phase_limit"])

    def test_custom_index_missing_ultra_overlay_explains_failure(self):
        p = profile()
        index = json.loads((ROOT / "routing-index.json").read_text())
        index["references"] = [e for e in index["references"] if e["id"] != "ultra-research"]
        with self.assertRaisesRegex(ValueError, "ULTRA_REFERENCE_MISSING"):
            select(index, route_task(p, index), p, [])

    def test_explicit_ultra_signal_escalates_from_deep(self):
        self.assertEqual(recheck_profile(profile(depth_class="deep"), ["ultra_requested"])["depth_class"], "ultra")


class LearningContracts(unittest.TestCase):
    def test_ordinary_retrieval_is_limited_to_tier_one(self):
        records = [
            {"learning_id": "one", "tier": 1, "status": "validated", "task_signature": ["research"]},
            {"learning_id": "two", "tier": 2, "status": "validated", "task_signature": ["research"]},
        ]
        selected = retrieve(records, ["research"], [], limit=3)
        self.assertEqual([item["learning_id"] for item in selected], ["one"])


class CliContracts(unittest.TestCase):
    def test_route_and_resource_cli_work_from_repository_root(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / "profile.json").write_text(json.dumps(profile()), encoding="utf-8")
            first = subprocess.run(
                [sys.executable, str(ROOT / "scripts/route_task.py"), str(path / "profile.json")],
                cwd=ROOT.parents[1], capture_output=True, text=True,
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            (path / "route.json").write_text(json.dumps(json.loads(first.stdout)["route"]), encoding="utf-8")
            second = subprocess.run(
                [sys.executable, str(ROOT / "scripts/route_resources.py"), str(path / "profile.json"), str(path / "route.json")],
                cwd=ROOT.parents[1], capture_output=True, text=True,
            )
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)

    def test_custom_index_can_be_used_by_both_cli_commands(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / "profile.json").write_text(json.dumps(profile()), encoding="utf-8")
            index = json.loads((ROOT / "routing-index.json").read_text())
            index["references"][0]["default_priority"] += 1
            (path / "index.json").write_text(json.dumps(index), encoding="utf-8")
            first = subprocess.run(
                [sys.executable, str(ROOT / "scripts/route_task.py"), str(path / "profile.json"), "--index", str(path / "index.json")],
                capture_output=True, text=True,
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            (path / "route.json").write_text(json.dumps(json.loads(first.stdout)["route"]), encoding="utf-8")
            second = subprocess.run(
                [sys.executable, str(ROOT / "scripts/route_resources.py"), str(path / "profile.json"), str(path / "route.json"), "--index", str(path / "index.json")],
                capture_output=True, text=True,
            )
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)


if __name__ == "__main__":
    unittest.main()
