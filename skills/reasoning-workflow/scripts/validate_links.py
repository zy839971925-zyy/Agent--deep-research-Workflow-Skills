#!/usr/bin/env python3
"""Validate local Markdown navigation and reference reachability."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def local_links(path: Path) -> list[str]:
    out: list[str] = []
    for target in LINK_RE.findall(path.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0]
        if target:
            out.append(target)
    return out


def validate(skill_dir: Path) -> list[str]:
    skill_dir = skill_dir.resolve()
    errors: list[str] = []
    root = skill_dir / "SKILL.md"
    if not root.is_file():
        return ["missing SKILL.md"]

    all_md = [root] + sorted((skill_dir / "references").glob("*.md"))
    for md in all_md:
        for rel in local_links(md):
            target = (md.parent / rel).resolve()
            try:
                target.relative_to(skill_dir)
            except ValueError:
                errors.append(f"{md.relative_to(skill_dir)} links outside root: {rel}")
                continue
            if not target.exists():
                errors.append(f"broken link in {md.relative_to(skill_dir)}: {rel}")

    root_targets = {
        (root.parent / rel).resolve()
        for rel in local_links(root)
        if rel.startswith("references/")
    }
    for ref in sorted((skill_dir / "references").glob("*.md")):
        if ref.resolve() not in root_targets:
            errors.append(f"reference not directly linked from SKILL.md: {ref.name}")
        backlink_targets = {(ref.parent / rel).resolve() for rel in local_links(ref)}
        if root.resolve() not in backlink_targets:
            errors.append(f"reference missing backlink to SKILL.md: {ref.name}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_dir", nargs="?", default=".")
    args = ap.parse_args()
    errors = validate(Path(args.skill_dir))
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1
    print("OK: local links, direct reference routing, and backlinks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
