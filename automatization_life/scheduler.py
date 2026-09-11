import logging
import threading
from typing import Any

from .actions import Confirm
from .engine import run_automation

LOGGER = logging.getLogger(__name__)


def run_scheduler(
    config: dict[str, Any], *, dry_run: bool, confirm: Confirm | None, interval: float = 60
) -> None:
    """Ejecuta automatizaciones que declaren interval_seconds mientras el proceso siga activo."""
    LOGGER.info("scheduler_started", extra={"interval": interval})
    stop = threading.Event()
    try:
        while not stop.is_set():
            for automation in config["automations"]:
                seconds = automation.get("interval_seconds")
                if isinstance(seconds, (int, float)) and seconds > 0:
                    run_automation(automation, dry_run=dry_run, confirm=confirm)
            stop.wait(interval)
    except KeyboardInterrupt:
        LOGGER.info("scheduler_stopped")
    finally:
        stop.set()
