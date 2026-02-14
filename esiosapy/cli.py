from __future__ import annotations

import argparse
import sys

from esiosapy import ESIOSAPYClient
from esiosapy import __version__


def main() -> None:
    """Main entry point for the esiosapy CLI."""
    parser = argparse.ArgumentParser(
        prog="esiosapy",
        description="Unofficial ESIOS API Python library CLI",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"esiosapy {__version__}",
    )
    parser.add_argument(
        "--token",
        required=True,
        help="ESIOS API token",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser(
        "indicators",
        help="List all available indicators",
    )

    subparsers.add_parser(
        "archives",
        help="List available archives",
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    try:
        client = ESIOSAPYClient(
            token=args.token,
            timeout=args.timeout,
        )

        if args.command == "indicators":
            indicators = client.indicators.list_all()
            print(f"Found {len(indicators)} indicators:")
            for ind in indicators:
                print(f"  [{ind.id}] {ind.name} ({ind.short_name})")

        elif args.command == "archives":
            archives = client.archives.list_all()
            print(f"Found {len(archives)} archives:")
            for arc in archives:
                print(f"  [{arc.archive_type}] {arc.name}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
