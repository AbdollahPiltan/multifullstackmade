"""Offline documentation/provenance checks for this trusted controller repository."""

import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
# Fingerprints of the 75 normative lines and MIT tail in upstream blob
# 0a503ff22f8d7d8a52397107f8d39d5f4e53642b, adopted at commit 0754e297.
RULE_DIGEST = (
    "7303b3c60ac442231b2fd06be835b4a84a7ebd35f0ca416176b5c605dba7d2e5"  # pragma: allowlist secret
)
NOTICE_DIGEST = (
    "a44153155c848869e82008b94540dce079ed9e0286568cad9f35d3e3e56e4e80"  # pragma: allowlist secret
)


def repository_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        timeout=10,
    )
    paths = [ROOT / name.decode() for name in result.stdout.split(b"\0") if name]
    if len(paths) > 4096 or any(not p.resolve().is_relative_to(ROOT) for p in paths):
        raise ValueError("Invalid repository inventory")
    return paths


def main() -> None:
    paths = repository_files()
    links = 0
    for path in paths:
        raw = path.read_bytes()
        if len(raw) > 4 * 1024 * 1024 or not raw.endswith(b"\n"):
            raise ValueError(f"File bound/final newline: {path.relative_to(ROOT)}")
        content = raw.decode()
        if any(line != line.rstrip() for line in content.splitlines()):
            raise ValueError(f"Trailing whitespace: {path.relative_to(ROOT)}")
        if path.suffix == ".json":
            json.loads(content)
        if path.suffix == ".py":
            ast.parse(content, filename=str(path.relative_to(ROOT)))
        if path.suffix != ".md":
            continue
        for reference in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            reference = reference.strip("<>")
            if urlsplit(reference).scheme or reference.startswith("#"):
                continue
            target = (path.parent / unquote(reference.split("#", 1)[0])).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                raise ValueError(f"Broken/escaping link in {path.relative_to(ROOT)}")
            links += 1
    policy = (ROOT / "AGENTS.md").read_text()
    rules = re.findall(r"^- \*\*[A-Z]+-\d+[^\n]*", policy, re.M)
    if len(rules) != 75 or hashlib.sha256("\n".join(rules).encode()).hexdigest() != RULE_DIGEST:
        raise ValueError("Pinned normative policy changed")
    if hashlib.sha256(policy.split("MIT License", 1)[1].encode()).hexdigest() != NOTICE_DIGEST:
        raise ValueError("Upstream MIT notice changed")
    task_ids = re.findall(r"^\| (T-\d+) \|", (ROOT / "TASKS.md").read_text(), re.M)
    if len(task_ids) != len(set(task_ids)) or len(task_ids) != 37:
        raise ValueError("Task identity drift")
    if len((ROOT / "MEMORY.md").read_text().splitlines()) >= 120:
        raise ValueError("Compact memory needs maintenance")
    print(
        f"PASS: {len(paths)} files, {links} local links, syntax/whitespace, 37 task IDs and pinned policy/MIT."
    )


if __name__ == "__main__":
    main()
