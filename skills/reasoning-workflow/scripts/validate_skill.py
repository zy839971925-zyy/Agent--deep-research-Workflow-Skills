#!/usr/bin/env python3
"""Deterministic structural validator for the reasoning-workflow skill.

Checks package shape and metadata only. It does not validate semantic quality.
Uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}
    out: dict[str, str] = {}
    i = 1
    while i < end:
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, value = m.group(1), m.group(2).strip()
        if value in {">", ">-", "|", "|-"}:
            block: list[str] = []
            i += 1
            while i < end and (lines[i].startswith("  ") or not lines[i].strip()):
                if lines[i].strip():
                    block.append(lines[i].strip())
                i += 1
            out[key] = " ".join(block)
            continue
        out[key] = value.strip('"\'')
        i += 1
    return out


def parse_openai_interface(path: Path) -> dict[str, str]:
    """Parse the simple scalar interface fields used by this package."""
    out: dict[str, str] = {}
    in_interface = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip() == "interface:":
            in_interface = True
            continue
        if in_interface and raw and not raw.startswith((" ", "\t")):
            break
        if not in_interface:
            continue
        m = re.match(r"^\s{2}([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"\'')
    return out


def validate(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_dir = skill_dir.resolve()
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        fail(errors, "missing SKILL.md")
        return errors

    fm = parse_frontmatter(skill_md)
    name = fm.get("name", "")
    desc = fm.get("description", "")
    if not name:
        fail(errors, "SKILL.md frontmatter missing name")
    else:
        if len(name) > 64:
            fail(errors, f"skill name exceeds 64 chars: {len(name)}")
        if not NAME_RE.match(name):
            fail(errors, f"invalid skill name: {name!r}")
        if skill_dir.name != name:
            fail(errors, f"folder name {skill_dir.name!r} does not match skill name {name!r}")
    if not desc.strip():
        fail(errors, "SKILL.md frontmatter missing description")

    if len(skill_md.read_text(encoding="utf-8").splitlines()) > 500:
        fail(errors, "SKILL.md exceeds 500 lines")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.is_file():
        fail(errors, "missing agents/openai.yaml")
    else:
        interface = parse_openai_interface(openai_yaml)
        for required in ("display_name", "short_description", "default_prompt"):
            if not interface.get(required):
                fail(errors, f"openai.yaml missing interface.{required}")
        short = interface.get("short_description", "")
        if short and not (25 <= len(short) <= 64):
            fail(errors, f"short_description must be 25-64 chars, got {len(short)}")
        for icon_key in ("icon_small", "icon_large"):
            val = interface.get(icon_key)
            if val:
                target = (skill_dir / val).resolve()
                try:
                    target.relative_to(skill_dir)
                except ValueError:
                    fail(errors, f"{icon_key} points outside skill root: {val}")
                else:
                    if not target.is_file():
                        fail(errors, f"{icon_key} target does not exist: {val}")

    # Basic expected package pieces for this specific workflow release.
    expected_dirs = ["references", "schemas", "scripts", "tests"]
    for d in expected_dirs:
        if not (skill_dir / d).is_dir():
            fail(errors, f"missing expected directory: {d}/")

    # Ensure Markdown is UTF-8 readable.
    for md in skill_dir.rglob("*.md"):
        try:
            md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            fail(errors, f"not valid UTF-8: {md.relative_to(skill_dir)}")

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
    print("OK: skill structure and metadata passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
