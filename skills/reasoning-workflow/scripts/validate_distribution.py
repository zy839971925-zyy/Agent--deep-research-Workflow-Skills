#!/usr/bin/env python3
"""Validate archive structure and every shared semantic payload without extraction."""
from pathlib import PurePosixPath
import argparse
import hashlib
import json
import zipfile

FAMILIES = {"reasoning-core", "deep-research", "decision-analysis",
            "execution-control", "audit-verification", "workflow-learning"}


def archive(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if len(names) != len(set(names)):
            raise ValueError("duplicate archive entries")
        for name in names:
            if name.startswith("/") or ".." in PurePosixPath(name).parts or "\\" in name:
                raise ValueError("unsafe archive path")
        if z.testzip() is not None:
            raise ValueError("ZIP integrity failure")
        return {n: z.read(n) for n in names if not n.endswith("/")}


def check(portable, modular):
    p, m = archive(portable), archive(modular)
    pr, mr = "reasoning-workflow/", "reasoning-workflow-modular/"
    manifest = json.loads(p[pr + "SEMANTIC_MANIFEST.json"])
    hashes = manifest["canonical_hashes"]
    if not isinstance(hashes, dict) or not hashes:
        raise ValueError("empty semantic manifest")
    expected = {n[len(pr):] for n in p if n.startswith((pr + "scripts/", pr + "schemas/"))}
    expected.add("routing-index.json")
    if set(hashes) != expected:
        raise ValueError("incomplete semantic manifest")
    if json.loads(m[mr + "SEMANTIC_MANIFEST.json"]) != manifest:
        raise ValueError("modular root manifest mismatch")
    prefix = mr + "skills/"
    actual = {n[len(prefix):].split("/")[0] for n in m if n.startswith(prefix)}
    if actual != FAMILIES:
        raise ValueError("modular distribution must contain exactly six Family Skills")
    roots = [(p, pr)] + [(m, prefix + family + "/") for family in sorted(FAMILIES)]
    for data, root in roots:
        if root + "SKILL.md" not in data:
            raise ValueError("missing Skill entrypoint: " + root)
        if json.loads(data[root + "SEMANTIC_MANIFEST.json"]) != manifest:
            raise ValueError("Skill manifest mismatch: " + root)
        shared = {n[len(root):] for n in data if n.startswith((root + "scripts/", root + "schemas/"))}
        if shared != expected - {"routing-index.json"}:
            raise ValueError("shared file set mismatch: " + root)
        for rel, digest in hashes.items():
            if hashlib.sha256(data[root + rel]).hexdigest() != digest:
                raise ValueError("semantic payload mismatch: " + root + rel)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("portable")
    ap.add_argument("modular")
    args = ap.parse_args()
    try:
        check(args.portable, args.modular)
    except (ValueError, KeyError, TypeError, OSError, zipfile.BadZipFile) as error:
        print("ERROR:", error)
        return 1
    print("OK: six Family Skills, complete manifests, ZIP integrity and shared semantic hashes are consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
