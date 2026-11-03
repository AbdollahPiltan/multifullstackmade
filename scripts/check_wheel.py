"""Check that the build preserves the authoritative contract bytes in the wheel."""

import hashlib
import zipfile
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    wheels = list((root / "dist").glob("*.whl"))
    if len(wheels) != 1:
        raise ValueError("Expected one wheel in dist/")
    with zipfile.ZipFile(wheels[0]) as wheel:
        for path in sorted((root / "contracts").iterdir()):
            data = wheel.read("multifullstackmade/contracts/" + path.name)
            if hashlib.sha256(data).digest() != hashlib.sha256(path.read_bytes()).digest():
                raise ValueError("Wheel contract differs from source")
        if not any(p.endswith("entry_points.txt") for p in wheel.namelist()):
            raise ValueError("Console entrypoint missing from wheel")
    print("PASS: wheel entrypoint and exact contract payloads.")


if __name__ == "__main__":
    main()
