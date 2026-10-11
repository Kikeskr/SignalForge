"""Command-line entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from signalforge import __version__
from signalforge.agent import run_research


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="signalforge",
        description="Research a question and produce a cited evidence report.",
    )
    parser.add_argument("--version", action="version", version=f"SignalForge {__version__}")
    subparsers = parser.add_subparsers(dest="command")
    run_parser = subparsers.add_parser("run", help="run a research task")
    run_parser.add_argument("question", help="research question")
    run_parser.add_argument("--max-sources", type=int, default=8)
    run_parser.add_argument("--output", default="reports")
    run_parser.add_argument("--url", action="append", default=[], help="fetch a specific public URL (repeatable)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command is None:
        build_parser().print_help()
        return 0
    if args.max_sources < 1 or args.max_sources > 12:
        print("--max-sources must be between 1 and 12", file=sys.stderr)
        return 2
    try:
        evidence, report, ledger = run_research(
            args.question, Path(args.output), args.max_sources, args.url
        )
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Research run failed ({type(exc).__name__}). Check search connectivity and try --url.", file=sys.stderr)
        return 1
    print(f"Sources captured: {len(evidence)}")
    print(f"Report: {report}")
    print(f"Evidence: {ledger}")
    return 0 if evidence else 1


if __name__ == "__main__":
    raise SystemExit(main())
