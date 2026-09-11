import argparse
import logging
import sys
from pathlib import Path

from .config import load_config
from .engine import find_automation, run_automation
from .errors import AutomationError, ConfirmationRequired
from .logging_config import configure_logging
from .scheduler import run_scheduler


def _interactive_confirm(prompt: str) -> bool:
    answer = input(f"{prompt}. ¿Continuar? [y/N] ").strip().lower()
    return answer in {"y", "yes", "s", "si", "sí"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ejecutor seguro de automatizaciones declarativas.")
    parser.add_argument("--config", type=Path, default=Path("automatization.yaml"))
    parser.add_argument("--dry-run", action="store_true", help="Muestra acciones sin ejecutarlas.")
    parser.add_argument("--verbose", action="store_true")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="Lista automatizaciones disponibles.")
    run = subparsers.add_parser("run", help="Ejecuta una automatización.")
    run.add_argument("name")
    schedule = subparsers.add_parser("schedule", help="Activa el scheduler opcional.")
    schedule.add_argument("--interval", type=float, default=60)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging(args.verbose)
    try:
        config = load_config(args.config)
        if args.command == "list":
            for automation in config["automations"]:
                print(automation["name"])
            return 0
        if args.command == "run":
            run_automation(
                find_automation(config, args.name),
                dry_run=args.dry_run,
                confirm=_interactive_confirm,
            )
            return 0
        run_scheduler(config, dry_run=args.dry_run, confirm=_interactive_confirm, interval=args.interval)
        return 0
    except (AutomationError, OSError, ValueError) as exc:
        logging.getLogger(__name__).error("execution_error", extra={"error": str(exc)})
        if isinstance(exc, ConfirmationRequired):
            return 2
        return 1


if __name__ == "__main__":
    sys.exit(main())
