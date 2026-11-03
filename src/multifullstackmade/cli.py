"""Read-only local CLI; no model, code-execution or GitHub-write command exists."""

import argparse
import json
import sys
from dataclasses import asdict
from importlib.metadata import version

from multifullstackmade.adapters.catalog import read_catalog
from multifullstackmade.adapters.environment import observe_environment
from multifullstackmade.application.inspection import inspect_contracts, inspect_environment
from multifullstackmade.domain.reports import CatalogUnavailable


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Development-team scaffold: local inspection only."
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {version('multifullstackmade')}"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("doctor", "Report prerequisites and unimplemented capabilities."),
        ("contracts", "List bundled design contracts and exact content digests."),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument(
            "--json", action="store_true", help="Emit a bounded structured report."
        )
    args = parser.parse_args(argv)
    if args.command == "doctor":
        report = inspect_environment(observe_environment)
        if args.json:
            print(json.dumps(asdict(report), ensure_ascii=True))
        else:
            print(f"Stage: {report.stage}; Python {report.python_version}")
            for check in report.checks:
                print(f"{check.name}: {check.state} - {check.detail}")
            print("Mission execution is not available in this scaffold.")
        return 1
    try:
        catalog = inspect_contracts(read_catalog)
    except CatalogUnavailable:
        print(
            "Bundled contracts are unavailable or invalid; reinstall the verified package.",
            file=sys.stderr,
        )
        return 1
    if args.json:
        print(json.dumps(asdict(catalog), ensure_ascii=True))
    else:
        print("Bundled design contracts; this is not runtime evidence.")
        for item in catalog.contracts:
            print(f"{item.name}\t{item.size_bytes}\t{item.sha256}")
    return 0
