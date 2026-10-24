"""Fault-injection tests for write reconciliation after a lost receipt.

The in-memory target is only a deterministic external-system fixture. Every action
passes through the real HarnessBridge authorization, durable status and replay gates.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from harness_bridge import (  # noqa: E402
    HarnessBridge,
    ReplayRequiresObservation,
    ToolGrant,
    ToolIntent,
)


class LostReceiptReconciliation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.bridge = HarnessBridge(Path(self.temp.name) / "run.sqlite")
        self.intent = ToolIntent(
            "write-42", "files.write", "reports/result.md", "create",
            {"content": "final report"}, "consequential",
        )
        self.profile = {"autonomy_class": "D"}
        self.grants = [ToolGrant("files.write", "reports/result.md", "create", "user-task-42")]

    def test_lost_receipt_reconciles_target_before_retry(self):
        # The first external write commits, then the response is lost before the
        # bridge receives a result/receipt. A current target read is the evidence
        # used to close the uncertain operation; retrying must never duplicate it.
        target = {}
        calls = []
        observations = []

        def execute(intent):
            calls.append(intent.operation_id)
            target[intent.target] = {"content": intent.arguments["content"], "version": 1}
            raise ConnectionError("commit succeeded; caller received no receipt")

        with self.assertRaisesRegex(ConnectionError, "no receipt"):
            self.bridge.call(self.intent, self.profile, self.grants, execute, receipt=lambda _: "write-receipt")
        self.assertEqual(self.bridge.status(self.intent.operation_id), "started")

        # Prove a retry cannot reach the executor before reconciliation.
        def forbidden_retry(intent):
            calls.append("UNEXPECTED_RETRY")
            return "duplicate"

        with self.assertRaises(ReplayRequiresObservation):
            self.bridge.call(self.intent, self.profile, self.grants, forbidden_retry, receipt=lambda _: "duplicate-receipt")
        self.assertEqual(calls, [self.intent.operation_id])

        # Simulate the host's authoritative read of the live target, not a stale
        # cache. The evidence reference is passed to the bridge's real recovery API.
        observations.append(dict(target.get(self.intent.target, {})))
        self.assertEqual(observations[0], {"content": "final report", "version": 1})
        self.bridge.confirm_succeeded(self.intent.operation_id, evidence_ref="live-target-read:reports/result.md:v1")

        with self.assertRaises(ReplayRequiresObservation):
            self.bridge.call(self.intent, self.profile, self.grants, forbidden_retry, receipt=lambda _: "duplicate-receipt")
        self.assertEqual(calls, [self.intent.operation_id])
        self.assertEqual(self.bridge.status(self.intent.operation_id), "completed")
        events = [event["event_type"] for event in self.bridge.events()]
        self.assertEqual(events.count("tool_started"), 1)
        self.assertEqual(events.count("external_success_confirmed"), 1)
        self.assertNotIn("tool_completed", events)  # caller never got a receipt

    def test_unknown_target_lookup_stays_unknown_and_blocks_retry(self):
        # The failed call may or may not have committed. If the current target
        # lookup itself supplies no evidence, do not turn uncertainty into either
        # success or absence, and do not permit a replay.
        target = {}
        calls = []
        lookup_calls = []

        def current_target_lookup():
            lookup_calls.append("reports/result.md")
            # The provider cannot resolve the request or prove absence.
            return {"status": "unknown", "evidence_ref": None}

        def execute(intent):
            calls.append(intent.operation_id)
            raise TimeoutError("outcome unknown")

        with self.assertRaisesRegex(TimeoutError, "unknown"):
            self.bridge.call(self.intent, self.profile, self.grants, execute, receipt=lambda _: "write-receipt")

        # Reconciliation actually consults the current target, but the provider
        # returns unknown rather than an authenticated present/absent observation.
        lookup_result = current_target_lookup()
        self.assertEqual(lookup_result, {"status": "unknown", "evidence_ref": None})
        with self.assertRaises(ReplayRequiresObservation):
            self.bridge.call(self.intent, self.profile, self.grants, execute, receipt=lambda _: "write-receipt")

        self.assertEqual(calls, [self.intent.operation_id])
        self.assertEqual(lookup_calls, ["reports/result.md"])
        self.assertEqual(self.bridge.status(self.intent.operation_id), "started")
        event_types = [event["event_type"] for event in self.bridge.events()]
        self.assertEqual(event_types.count("tool_outcome_uncertain"), 1)
        self.assertNotIn("external_success_confirmed", event_types)
        self.assertNotIn("external_nonexecution_confirmed", event_types)
        self.assertEqual(target, {})

    def test_retry_allowed_only_after_live_lookup_confirms_absence(self):
        target = {}
        calls = []
        lookups = []

        def first_attempt(intent):
            calls.append("first")
            raise ConnectionError("no receipt; commit state uncertain")

        with self.assertRaises(ConnectionError):
            self.bridge.call(self.intent, self.profile, self.grants, first_attempt, receipt=lambda _: "write-receipt")

        # The lookup is against the current target. Only its explicit absent result
        # is allowed to authorize the real bridge's retry transition.
        lookups.append(target.get(self.intent.target))
        self.assertIsNone(lookups[-1])
        self.bridge.confirm_not_run(self.intent.operation_id, evidence_ref="live-target-read:reports/result.md:absent")

        def retry(intent):
            calls.append("retry")
            target[intent.target] = {"content": intent.arguments["content"], "version": 1}
            return "committed"

        result = self.bridge.call(self.intent, self.profile, self.grants, retry, receipt=lambda value: "receipt:" + value)
        self.assertEqual(result, "committed")
        self.assertEqual(calls, ["first", "retry"])
        self.assertEqual(target[self.intent.target]["version"], 1)
        self.assertEqual(self.bridge.status(self.intent.operation_id), "completed")
        event_types = [event["event_type"] for event in self.bridge.events()]
        self.assertEqual(event_types.count("external_nonexecution_confirmed"), 1)
        self.assertEqual(event_types.count("tool_started"), 2)
        self.assertEqual(event_types.count("tool_completed"), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
