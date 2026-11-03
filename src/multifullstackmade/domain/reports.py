"""Read-only inspection results, separate from transport and host probes."""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class EnvironmentSnapshot:
    python_version: tuple[int, int, int]
    executables: frozenset[str]


@dataclass(frozen=True)
class Capability:
    name: str
    state: Literal["available", "missing", "unverified"]
    detail: str


@dataclass(frozen=True)
class DoctorReport:
    stage: str
    python_version: str
    mission_execution_available: bool
    checks: tuple[Capability, ...]


@dataclass(frozen=True)
class ContractFile:
    name: str
    sha256: str
    size_bytes: int


@dataclass(frozen=True)
class ContractReport:
    scope: str
    runtime_evidence: bool
    total_bytes: int
    contracts: tuple[ContractFile, ...]


class CatalogUnavailable(Exception):
    """The installed bundle cannot be safely or completely inspected."""
