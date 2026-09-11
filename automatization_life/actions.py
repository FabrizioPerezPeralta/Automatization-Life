import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Callable

from .errors import ConfirmationRequired, AutomationError
from .plugins import get_action

LOGGER = logging.getLogger(__name__)
Confirm = Callable[[str], bool]


def _path(value: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(value)))


def _confirm(prompt: str, confirm: Confirm | None) -> None:
    if confirm is None or not confirm(prompt):
        raise ConfirmationRequired(prompt)


def execute_task(task: dict[str, Any], *, dry_run: bool, confirm: Confirm | None) -> None:
    action = task["action"]
    plugin = get_action(action)
    if plugin is not None:
        plugin(task, dry_run)
        return
    if action in {"delete", "shell"}:
        _confirm(f"Confirmación requerida para '{action}'", confirm)
    if action == "mkdir":
        path = _path(task["path"])
        LOGGER.info("mkdir", extra={"path": str(path), "dry_run": dry_run})
        if not dry_run:
            path.mkdir(parents=True, exist_ok=True)
    elif action == "copy":
        source, destination = _path(task["source"]), _path(task["destination"])
        LOGGER.info("copy", extra={"source": str(source), "destination": str(destination), "dry_run": dry_run})
        if not dry_run:
            if not source.exists():
                raise AutomationError(f"No existe el origen: {source}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    elif action == "move":
        source, destination = _path(task["source"]), _path(task["destination"])
        LOGGER.info("move", extra={"source": str(source), "destination": str(destination), "dry_run": dry_run})
        if not dry_run:
            if not source.exists():
                raise AutomationError(f"No existe el origen: {source}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
    elif action == "delete":
        path = _path(task["path"])
        LOGGER.info("delete", extra={"path": str(path), "dry_run": dry_run})
        if not dry_run and path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    elif action == "write_text":
        path = _path(task["path"])
        LOGGER.info("write_text", extra={"path": str(path), "dry_run": dry_run})
        if not dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(task["content"], encoding="utf-8")
    elif action == "launch":
        path = str(_path(task["path"]))
        LOGGER.info("launch", extra={"path": path, "dry_run": dry_run})
        if not dry_run:
            os.startfile(path)  # type: ignore[attr-defined]
    elif action == "shell":
        command = task["command"]
        LOGGER.info("shell", extra={"command": command, "dry_run": dry_run})
        if not dry_run:
            subprocess.run(command, shell=True, check=True)
