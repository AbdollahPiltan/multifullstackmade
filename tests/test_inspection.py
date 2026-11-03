import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from multifullstackmade.adapters import catalog
from multifullstackmade.application.inspection import inspect_contracts, inspect_environment
from multifullstackmade.cli import main
from multifullstackmade.domain.reports import CatalogUnavailable, EnvironmentSnapshot


def test_available_tools_do_not_claim_mission_readiness():
    report = inspect_environment(
        lambda: EnvironmentSnapshot((3, 12, 14), frozenset({"uv", "git", "gh", "docker"}))
    )
    assert not report.mission_execution_available
    assert next(c for c in report.checks if c.name == "mission_engine").state == "missing"
    assert next(c for c in report.checks if c.name == "sandbox_release").state == "unverified"


def test_missing_tools_and_unsupported_python_are_explicit():
    report = inspect_environment(lambda: EnvironmentSnapshot((3, 13, 0), frozenset()))
    states = {c.name: c.state for c in report.checks}
    assert states["python"] == states["docker"] == states["gh"] == "missing"


def test_catalog_hashes_exact_file_bytes(tmp_path):
    content = b'{"kind":"design"}\n'
    (tmp_path / "one.json").write_bytes(content)
    result = catalog.read_catalog(tmp_path)
    assert result[0].size_bytes == len(content)
    assert result[0].sha256 == hashlib.sha256(content).hexdigest()
    with pytest.raises(CatalogUnavailable):
        inspect_contracts(lambda: result)


def test_catalog_rejects_symlinks(tmp_path):
    (tmp_path / "outside").write_text("sensitive-placeholder")
    root = tmp_path / "catalog"
    root.mkdir()
    (root / "link.json").symlink_to(tmp_path / "outside")
    with pytest.raises(CatalogUnavailable):
        catalog.read_catalog(root)


def test_catalog_rejects_unknown_entries(tmp_path):
    (tmp_path / "private.txt").write_text("synthetic-content")
    with pytest.raises(CatalogUnavailable):
        catalog.read_catalog(tmp_path)


def test_catalog_rejects_unavailable_directory(tmp_path):
    with pytest.raises(CatalogUnavailable):
        catalog.read_catalog(tmp_path / "missing")


def test_catalog_enforces_total_byte_limit(tmp_path, monkeypatch):
    for name in ("one.json", "two.json"):
        (tmp_path / name).write_bytes(b"x" * 6)
    monkeypatch.setattr(catalog, "MAX_TOTAL_BYTES", 11)
    with pytest.raises(CatalogUnavailable):
        catalog.read_catalog(tmp_path)


def test_catalog_enforces_streaming_byte_limit(tmp_path, monkeypatch):
    (tmp_path / "large.json").write_bytes(b"x" * 10)
    monkeypatch.setattr(catalog, "MAX_FILE_BYTES", 9)
    with pytest.raises(CatalogUnavailable):
        catalog.read_catalog(tmp_path)


def test_catalog_enforces_count_limit(tmp_path, monkeypatch):
    for name in ("one.json", "two.json"):
        (tmp_path / name).write_text("{}")
    monkeypatch.setattr(catalog, "MAX_FILES", 1)
    with pytest.raises(CatalogUnavailable):
        catalog.read_catalog(tmp_path)


def test_installed_bundle_is_complete_and_not_runtime_evidence():
    report = inspect_contracts(catalog.read_catalog)
    assert len(report.contracts) == 15
    assert not report.runtime_evidence
    assert report.total_bytes > 0


def test_doctor_output_does_not_disclose_environment(capsys, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "synthetic-do-not-print")
    monkeypatch.setenv("GH_TOKEN", "synthetic-do-not-print")
    assert main(["doctor", "--json"]) == 1
    output = capsys.readouterr().out
    assert "synthetic-do-not-print" not in output
    assert not json.loads(output)["mission_execution_available"]


def test_missing_bundle_has_sanitized_error(capsys, monkeypatch):
    def fail():
        raise CatalogUnavailable("private-internal-path")

    monkeypatch.setattr("multifullstackmade.cli.read_catalog", fail)
    assert main(["contracts", "--json"]) == 1
    result = capsys.readouterr()
    assert result.out == ""
    assert "private-internal-path" not in result.err


def test_no_execution_command_is_exposed():
    with pytest.raises(SystemExit) as result:
        main(["run", "untrusted.py"])
    assert result.value.code == 2


def test_module_entrypoint_works_outside_checkout(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "multifullstackmade", "contracts", "--json"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert len(json.loads(result.stdout)["contracts"]) == 15


def test_console_version_does_not_require_docker(tmp_path):
    executable = Path(sys.executable).parent / "multifullstackmade"
    result = subprocess.run(
        [str(executable), "--version"],
        cwd=tmp_path,
        env={**os.environ, "PATH": ""},
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.stdout.strip() == "multifullstackmade 0.1.0a1"
