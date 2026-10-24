"""Synthetic existing user-controlled export surface."""

import json


def export_schedule(schedule, path):
    with open(path, "w", encoding="utf-8") as stream:
        json.dump(schedule, stream, ensure_ascii=False, sort_keys=True)
    return path
