"""Inspect only the installed contract bundle or this package's editable checkout."""

import hashlib
import re
from pathlib import Path

from multifullstackmade.domain.reports import CatalogUnavailable, ContractFile

MAX_FILES = 64
MAX_FILE_BYTES = 4 * 1024 * 1024
MAX_TOTAL_BYTES = 16 * 1024 * 1024


def bundled_directory() -> Path:
    package = Path(__file__).resolve().parents[1]
    installed = package / "contracts"
    if installed.is_dir():
        return installed
    # Hatch's editable import points at src; force-included wheel data stays in contracts/.
    if package.parent.name == "src":
        editable = package.parent.parent / "contracts"
        if editable.is_dir():
            return editable
    raise CatalogUnavailable


def read_catalog(directory: Path | None = None) -> tuple[ContractFile, ...]:
    """Hash a bounded bundle; the directory seam is for trusted tests, never CLI input."""
    try:
        root = bundled_directory() if directory is None else directory
        entries: list[Path] = []
        for path in root.iterdir():
            if len(entries) >= MAX_FILES:
                raise CatalogUnavailable
            if (
                path.is_symlink()
                or not path.is_file()
                or not re.fullmatch(r"[a-z][a-z0-9.-]{0,63}\.(json|sql)", path.name)
            ):
                raise CatalogUnavailable
            entries.append(path)
        result = []
        total = 0
        for path in sorted(entries):
            digest = hashlib.sha256()
            size = 0
            with path.open("rb") as stream:
                while chunk := stream.read(65536):
                    size += len(chunk)
                    total += len(chunk)
                    if size > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
                        raise CatalogUnavailable
                    digest.update(chunk)
            result.append(ContractFile(path.name, digest.hexdigest(), size))
        return tuple(result)
    except OSError:
        raise CatalogUnavailable from None
