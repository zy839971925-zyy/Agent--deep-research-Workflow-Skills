"""Synthetic local-only persistence adapter for workflow evaluation."""

class LocalScheduleStore:
    def __init__(self, database_path):
        self.database_path = database_path

    def save_schedule(self, schedule):
        """Persist one schedule locally; production I/O intentionally omitted."""
        return {"stored_at": self.database_path, "schedule": schedule}

    def load_schedule(self, schedule_id):
        """Placeholder for the fixture's existing local lookup."""
        return {"id": schedule_id, "source": "local"}
