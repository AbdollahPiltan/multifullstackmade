"""Gate offline scanner findings without printing potential secret values."""

import json
import subprocess
import sys

from verify_repository import ROOT, repository_files


def main() -> int:
    paths = [str(p.relative_to(ROOT)) for p in repository_files()]
    result = subprocess.run(
        ["detect-secrets", "scan", "--no-verify", "--", *paths],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    scan = json.loads(result.stdout)
    findings = [
        (path, item["type"], item["line_number"])
        for path, items in scan["results"].items()
        for item in items
    ]
    if findings:
        for path, kind, line in findings:
            print(f"Unreviewed scanner finding: {path}:{line} ({kind})", file=sys.stderr)
        return 1
    print(
        "PASS: offline secret scan; no unreviewed findings. No credential verification requests sent."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
