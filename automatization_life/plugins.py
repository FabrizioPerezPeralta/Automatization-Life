"""Registro pequeño y explícito para extender acciones sin cargar código remoto."""

from collections.abc import Callable
from typing import Any

PluginAction = Callable[[dict[str, Any], bool], None]
_actions: dict[str, PluginAction] = {}


def register_action(name: str, handler: PluginAction) -> None:
    if not name or name in {"mkdir", "copy", "move", "delete", "write_text", "launch", "shell"}:
        raise ValueError("El nombre del plugin no es válido o está reservado.")
    _actions[name] = handler


def get_action(name: str) -> PluginAction | None:
    return _actions.get(name)


def action_names() -> set[str]:
    return set(_actions)

