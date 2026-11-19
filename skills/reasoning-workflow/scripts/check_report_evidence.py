#!/usr/bin/env python3
"""Check quote locations and declared origins in a local research packet."""
import argparse
import json
from pathlib import Path


def required_text(record, key):
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Expected nonempty text for {key}")
    return value


def records(packet, key):
    rows = packet.get(key)
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"Expected an array of objects for {key}")
    return rows


def unique_index(rows):
    result = {}
    for row in rows:
        identifier = required_text(row, "id")
        if identifier in result:
            raise ValueError(f"Duplicate ID: {identifier}")
        result[identifier] = row
    return result


def check(packet, directory):
    if not isinstance(packet, dict):
        raise ValueError("Expected a packet object")
    sources = unique_index(records(packet, "sources"))
    claims = unique_index(records(packet, "claims"))
    if not claims:
        raise ValueError("Supply at least one claim")
    root = directory.resolve()
    documents = {}
    for identifier, source in sources.items():
        relative = Path(required_text(source, "file"))
        path = (root / relative).resolve()
        if relative.is_absolute() or not path.is_relative_to(root):
            raise ValueError(f"{identifier}: source must be inside the packet directory")
        required_text(source, "origin")
        documents[identifier] = path.read_text(encoding="utf-8")

    results = []
    for identifier, claim in claims.items():
        required_text(claim, "text")
        status = required_text(claim, "status")
        if status not in {"observed", "inferred", "contested", "unknown"}:
            raise ValueError(f"{identifier}: invalid status")
        origins = set()
        sides = set()
        evidence = records(claim, "evidence")
        for item in evidence:
            source_id = required_text(item, "source")
            if source_id not in sources:
                raise ValueError(f"{identifier}: unknown source {source_id}")
            quote = required_text(item, "quote")
            side = required_text(item, "role")
            if side not in {"support", "counter"}:
                raise ValueError(f"{identifier}: invalid evidence role")
            if quote not in documents[source_id]:
                raise ValueError(f"{identifier}: quote missing in {source_id}")
            sides.add(side)
            origins.add(sources[source_id]["origin"])
        if status != "unknown" and "support" not in sides:
            raise ValueError(f"{identifier}: missing supporting passage")
        if status == "contested" and "counter" not in sides:
            raise ValueError(f"{identifier}: missing counterevidence passage")
        results.append({"claim": identifier, "passages": len(evidence),
                        "declared_origins": sorted(origins)})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    try:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        claims = check(packet, args.packet.parent)
    except (ValueError, OSError) as error:
        print(json.dumps({"passed": False, "error": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps({"passed": True, "claims": claims,
                      "checks": "local quote presence and declared links only"},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
