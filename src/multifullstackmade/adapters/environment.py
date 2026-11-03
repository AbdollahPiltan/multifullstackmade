"""Observe executable availability without invoking tools or reading credentials."""

import shutil
import sys

from multifullstackmade.domain.reports import EnvironmentSnapshot


def observe_environment() -> EnvironmentSnapshot:
    return EnvironmentSnapshot(
        python_version=(sys.version_info.major, sys.version_info.minor, sys.version_info.micro),
        executables=frozenset(name for name in ("uv", "git", "gh", "docker") if shutil.which(name)),
    )
