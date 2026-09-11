import logging
from typing import Any

from .actions import Confirm, execute_task
from .errors import AutomationError

LOGGER = logging.getLogger(__name__)


def run_automation(
    automation: dict[str, Any], *, dry_run: bool = False, confirm: Confirm | None = None
) -> int:
    name = automation["name"]
    LOGGER.info("automation_started", extra={"automation": name, "dry_run": dry_run})
    completed = 0
    try:
        for task in automation["tasks"]:
            execute_task(task, dry_run=dry_run, confirm=confirm)
            completed += 1
    except AutomationError:
        LOGGER.exception("automation_failed", extra={"automation": name, "task": completed + 1})
        raise
    LOGGER.info("automation_completed", extra={"automation": name, "tasks": completed})
    return completed


def find_automation(config: dict[str, Any], name: str) -> dict[str, Any]:
    for automation in config["automations"]:
        if automation["name"] == name:
            return automation
    raise AutomationError(f"No existe la automatización: {name}")
