#!/usr/bin/env python3
"""Verify the exported CiteSage demo manifest, hashes, and allowlist."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEMO = ROOT / "demo"
MANIFEST = DEMO / "bundle-manifest.json"
ALLOWED_UNMANAGED = {"README.md"}
EXPECTED_ARTIFACTS = {
    "cluster_map.html",
    "demo_static.html",
    "flow_dossier.html",
    "knowledge_flow.html",
    "knowledge_sankey.html",
    "research_timeline.html",
    "theme_alluvial.html",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="allow a local preview exported from uncommitted canonical changes",
    )
    args = parser.parse_args()
    failures: list[str] = []

    if not MANIFEST.is_file():
        print("PUBLIC_DEMO_BUNDLE=FAIL\n- missing demo/bundle-manifest.json")
        return 1
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("contract") != "citesage-artifact-v1":
        failures.append("artifact contract version mismatch")
    if manifest.get("lineage_contract") != "citesage-public-lineage-v1":
        failures.append("lineage contract version mismatch")
    commit = manifest.get("canonical_commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        failures.append("canonical_commit is not a full Git SHA")
    worktree = manifest.get("canonical_worktree")
    if worktree not in {"CLEAN", "DIRTY"}:
        failures.append("canonical_worktree must be CLEAN or DIRTY")
    elif worktree != "CLEAN" and not args.allow_dirty:
        failures.append("release manifest was exported from a dirty canonical worktree")

    files = manifest.get("files", {})
    for relative, expected in files.items():
        path = DEMO / relative
        if not path.is_file():
            failures.append(f"missing manifest file: {relative}")
        elif sha256(path) != expected:
            failures.append(f"hash mismatch: {relative}")
    expected_files = set(files) | ALLOWED_UNMANAGED | {"bundle-manifest.json"}
    actual_files = {
        str(path.relative_to(DEMO))
        for path in DEMO.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    for relative in sorted(actual_files - expected_files):
        failures.append(f"unexpected stale file: {relative}")

    artifacts = manifest.get("artifacts", {})
    if set(artifacts) != EXPECTED_ARTIFACTS:
        failures.append("lineage must cover exactly the seven public artifacts")
    for name, lineage in artifacts.items():
        if f"artifacts/{name}" not in files:
            failures.append(f"{name}: artifact hash is absent from files")
        if not lineage.get("builder") or not re.fullmatch(
            r"[0-9a-f]{64}", lineage.get("builder_sha256", "")
        ):
            failures.append(f"{name}: invalid builder lineage")
        inputs = lineage.get("inputs", {})
        if not inputs or any(not re.fullmatch(r"[0-9a-f]{64}", value) for value in inputs.values()):
            failures.append(f"{name}: invalid input lineage")

    if failures:
        print("PUBLIC_DEMO_BUNDLE=FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(
        "PUBLIC_DEMO_BUNDLE=PASS "
        f"files={len(files)} artifacts={len(artifacts)} canonical={commit[:12]} "
        f"worktree={worktree}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
