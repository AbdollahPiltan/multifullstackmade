"""Coordinate bounded local inspection without mission or external effects."""

from collections.abc import Callable

from multifullstackmade.domain.reports import (
    Capability,
    CatalogUnavailable,
    ContractFile,
    ContractReport,
    DoctorReport,
    EnvironmentSnapshot,
)

REQUIRED_CONTRACTS = frozenset(
    {
        "protocol.schema.json",
        "protocol.examples.json",
        "notes.openapi.json",
        "notes.examples.json",
        "workflow.graph.json",
        "domain-storage.sql",
        "execution-limits.json",
        "execution-limits.schema.json",
        "execution-limits.examples.json",
        "sandbox-profiles.json",
        "sandbox-profiles.schema.json",
        "sandbox-profiles.examples.json",
        "github-delivery.json",
        "github-delivery.schema.json",
        "github-delivery.examples.json",
    }
)


def inspect_environment(observe: Callable[[], EnvironmentSnapshot]) -> DoctorReport:
    snapshot = observe()
    supported = (3, 12, 14) <= snapshot.python_version < (3, 13, 0)
    checks = [
        Capability(
            "python",
            "available" if supported else "missing",
            "Python 3.12.14+ within 3.12 required.",
        )
    ]
    checks.extend(
        Capability(
            name,
            "available" if name in snapshot.executables else "missing",
            "Executable availability only; version, daemon and authentication not checked.",
        )
        for name in ("uv", "git", "gh", "docker")
    )
    checks.extend(
        (
            Capability(
                "mission_engine", "missing", "Mission execution is not implemented in stage nine."
            ),
            Capability(
                "sandbox_release", "unverified", "No qualified image/host release is registered."
            ),
            Capability(
                "publication_binding",
                "unverified",
                "No runtime publication consent or CI manifest is configured.",
            ),
        )
    )
    return DoctorReport(
        "scaffold", ".".join(map(str, snapshot.python_version)), False, tuple(checks)
    )


def inspect_contracts(load: Callable[[], tuple[ContractFile, ...]]) -> ContractReport:
    contracts = load()
    names = [item.name for item in contracts]
    if len(set(names)) != len(names) or set(names) != REQUIRED_CONTRACTS:
        raise CatalogUnavailable
    return ContractReport(
        "bundled design contracts", False, sum(item.size_bytes for item in contracts), contracts
    )
