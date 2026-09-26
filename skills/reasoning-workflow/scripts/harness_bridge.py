"""Optional host adapter for tool authorization and replay-safe side effects.

The host must derive ToolIntent from a trusted tool registry and supply grants
from its own authorization channel. Model text and retrieved content cannot
create grants or downgrade a tool's side-effect classification.
"""

from __future__ import annotations

from dataclasses import dataclass
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from typing import Callable, TypeVar


T = TypeVar("T")
SIDE_EFFECTS = {"none", "reversible", "consequential", "irreversible"}
STAGES = {"skill_activated", "task_profile_committed", "skill_route_selected", "reference_loaded",
          "checkpoint_saved", "verification_recorded", "closure_computed"}


def _valid_ref(value) -> bool:
    return isinstance(value, str) and 0 < len(value) <= 256 and not any(ord(ch) < 32 for ch in value)


class ActionDenied(PermissionError):
    """The host has no matching user authorization for this action."""


class ReplayRequiresObservation(RuntimeError):
    """The operation may already have happened; observe before retrying."""


@dataclass(frozen=True)
class ToolIntent:
    operation_id: str
    tool_id: str
    target: str
    action: str
    arguments: dict
    side_effect_class: str

    def __post_init__(self):
        if not all((self.operation_id, self.tool_id, self.target, self.action)):
            raise ValueError("operation, tool, target and action must be nonempty")
        if self.side_effect_class not in SIDE_EFFECTS:
            raise ValueError("invalid side effect class")

    def fingerprint(self) -> str:
        payload = json.dumps(self.__dict__, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ToolGrant:
    tool_id: str
    target: str
    action: str
    authorization_ref: str

    def matches(self, intent: ToolIntent) -> bool:
        return _valid_ref(self.authorization_ref) and (self.tool_id, self.target, self.action) == (
            intent.tool_id, intent.target, intent.action,
        )


def wrap_untrusted(content: str, source_ref: str) -> dict:
    """Preserve source provenance; the host must keep this in a data/tool role."""
    if not source_ref:
        raise ValueError("untrusted data needs a source reference")
    return {"trust_level": "untrusted", "source_ref": source_ref, "content": content}


class HarnessBridge:
    def __init__(self, database: Path):
        self.database = Path(database)
        self.database.parent.mkdir(parents=True, exist_ok=True)
        with self._connection() as db:
            db.execute("CREATE TABLE IF NOT EXISTS operations (operation_id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, status TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY, event_type TEXT NOT NULL, operation_id TEXT NOT NULL, fingerprint TEXT, evidence_ref TEXT, occurred_at TEXT NOT NULL)")

    @contextmanager
    def _connection(self):
        db = sqlite3.connect(self.database, timeout=15)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    @staticmethod
    def _event(db, event_type: str, operation_id: str, fingerprint: str | None = None, evidence_ref: str | None = None):
        db.execute("INSERT INTO events (event_type, operation_id, fingerprint, evidence_ref, occurred_at) VALUES (?, ?, ?, ?, ?)",
                   (event_type, operation_id, fingerprint, evidence_ref, datetime.now(timezone.utc).isoformat()))

    def status(self, operation_id: str) -> str | None:
        with self._connection() as db:
            row = db.execute("SELECT status FROM operations WHERE operation_id = ?", (operation_id,)).fetchone()
            return row["status"] if row else None

    def events(self) -> list[dict]:
        with self._connection() as db:
            return [dict(row) for row in db.execute("SELECT * FROM events ORDER BY seq")]

    def record_stage(self, run_id: str, event_type: str, content_fingerprint: str):
        """Host-observed lifecycle stage. This does not validate the host's claim."""
        if not run_id or event_type not in STAGES or not re.fullmatch(r"sha256:[0-9a-f]{64}", content_fingerprint):
            raise ValueError("stage needs a run ID, known type and SHA-256 fingerprint")
        with self._connection() as db:
            self._event(db, event_type, run_id, content_fingerprint)

    def call(self, intent: ToolIntent, profile: dict, grants: list[ToolGrant], execute: Callable[[ToolIntent], T],
             receipt: Callable[[T], str] | None = None) -> T:
        """Call a trusted host callback only after the authorization and replay gates."""
        if profile.get("autonomy_class") not in ("A", "B", "C", "D"):
            raise ValueError("a validated Task Profile autonomy class is required")
        fingerprint = intent.fingerprint()
        # A/B/C permit autonomous work within existing user scope; they do
        # not turn an unscoped external side effect into an authorized one.
        requires_grant = intent.side_effect_class != "none"
        if requires_grant and not any(grant.matches(intent) for grant in grants):
            with self._connection() as db:
                self._event(db, "tool_denied", intent.operation_id, fingerprint)
            raise ActionDenied(f"no matching authorization for {intent.tool_id} on {intent.target}")
        authorization_ref = next((grant.authorization_ref for grant in grants if grant.matches(intent)), None)
        if intent.side_effect_class in ("consequential", "irreversible") and receipt is None:
            raise ValueError("consequential tool calls require a host-supplied external receipt function")

        if intent.side_effect_class != "none":
            with self._connection() as db:
                db.execute("BEGIN IMMEDIATE")
                row = db.execute("SELECT fingerprint, status FROM operations WHERE operation_id = ?", (intent.operation_id,)).fetchone()
                if row and (row["fingerprint"] != fingerprint or row["status"] != "confirmed_not_run"):
                    raise ReplayRequiresObservation(f"{intent.operation_id}: observe the external state before retry")
                if row:
                    db.execute("UPDATE operations SET status = 'started' WHERE operation_id = ?", (intent.operation_id,))
                else:
                    db.execute("INSERT INTO operations VALUES (?, ?, 'started')", (intent.operation_id, fingerprint))
                self._event(db, "tool_started", intent.operation_id, fingerprint, authorization_ref)
        try:
            result = execute(intent)
            evidence_ref = receipt(result) if receipt else None
            if receipt and not _valid_ref(evidence_ref):
                raise ValueError("tool executed but external receipt is invalid; re-observe before retry")
        except Exception:
            if intent.side_effect_class != "none":
                with self._connection() as db:
                    self._event(db, "tool_outcome_uncertain", intent.operation_id, fingerprint)
            raise
        if intent.side_effect_class != "none":
            with self._connection() as db:
                db.execute("UPDATE operations SET status = 'completed' WHERE operation_id = ?", (intent.operation_id,))
                self._event(db, "tool_completed", intent.operation_id, fingerprint, evidence_ref)
        return result

    def confirm_not_run(self, operation_id: str, evidence_ref: str):
        """Host-only recovery decision after independently observing external state."""
        if not _valid_ref(evidence_ref):
            raise ValueError("a concrete external observation reference is required")
        with self._connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT fingerprint, status FROM operations WHERE operation_id = ?", (operation_id,)).fetchone()
            if not row or row["status"] != "started":
                raise ReplayRequiresObservation("only an interrupted or uncertain operation can be retried")
            db.execute("UPDATE operations SET status = 'confirmed_not_run' WHERE operation_id = ?", (operation_id,))
            self._event(db, "external_nonexecution_confirmed", operation_id, row["fingerprint"], evidence_ref)

    def confirm_succeeded(self, operation_id: str, evidence_ref: str):
        """Host-only close after the target system shows that the action committed."""
        if not _valid_ref(evidence_ref):
            raise ValueError("a concrete external observation reference is required")
        with self._connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT fingerprint, status FROM operations WHERE operation_id = ?", (operation_id,)).fetchone()
            if not row or row["status"] != "started":
                raise ReplayRequiresObservation("only an interrupted or uncertain operation can be reconciled")
            db.execute("UPDATE operations SET status = 'completed' WHERE operation_id = ?", (operation_id,))
            self._event(db, "external_success_confirmed", operation_id, row["fingerprint"], evidence_ref)
