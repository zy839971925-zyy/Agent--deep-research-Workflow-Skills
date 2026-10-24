# Synthetic architecture fixture (not a production project)

This small fictional app is offline-first. Users manually enter a timetable and local reminders. There is no account, backend, cloud provider, or existing sync protocol. `src/storage.py` owns local records; `src/export.py` creates a user-controlled JSON export. The tests cover current local behavior only.

Task under evaluation: research a recommendation for optional backup and cross-device restore before coding. The desired product outcome is known; whether cloud sync is a must-have or merely optional is intentionally unresolved.
