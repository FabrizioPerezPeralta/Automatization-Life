from pathlib import Path
from typing import Any

import yaml

from .errors import ValidationError

ALLOWED_ACTIONS = {"mkdir", "copy", "move", "delete", "write_text", "launch", "shell"}


def load_config(path: Path) -> dict[str, Any]:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"No existe el archivo de configuración: {path}") from exc
    except yaml.YAMLError as exc:
        raise ValidationError(f"YAML inválido: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValidationError("La raíz de la configuración debe ser un objeto YAML.")
    validate_config(raw)
    return raw


def validate_config(config: dict[str, Any]) -> None:
    automations = config.get("automations")
    if not isinstance(automations, list) or not automations:
        raise ValidationError("'automations' debe ser una lista no vacía.")
    names: set[str] = set()
    for automation in automations:
        if not isinstance(automation, dict):
            raise ValidationError("Cada automatización debe ser un objeto.")
        name = automation.get("name")
        tasks = automation.get("tasks")
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("Cada automatización necesita un 'name' válido.")
        if name in names:
            raise ValidationError(f"Nombre de automatización duplicado: {name}")
        names.add(name)
        if not isinstance(tasks, list) or not tasks:
            raise ValidationError(f"La automatización '{name}' necesita tareas.")
        for index, task in enumerate(tasks, start=1):
            if not isinstance(task, dict):
                raise ValidationError(f"Tarea {index} de '{name}' debe ser un objeto.")
            action = task.get("action")
            from .plugins import action_names

            if action not in ALLOWED_ACTIONS | action_names():
                allowed = ", ".join(sorted(ALLOWED_ACTIONS | action_names()))
                raise ValidationError(f"Acción inválida '{action}'. Permitidas: {allowed}.")
            if action == "shell" and not isinstance(task.get("command"), str):
                raise ValidationError(f"La tarea shell {index} necesita 'command'.")
            if action in {"mkdir", "delete", "launch"} and not isinstance(task.get("path"), str):
                raise ValidationError(f"La tarea {action} {index} necesita 'path'.")
            if action in {"copy", "move"} and not all(
                isinstance(task.get(key), str) for key in ("source", "destination")
            ):
                raise ValidationError(f"La tarea {action} {index} necesita source y destination.")
            if action == "write_text" and not all(
                isinstance(task.get(key), str) for key in ("path", "content")
            ):
                raise ValidationError(f"La tarea write_text {index} necesita path y content.")
