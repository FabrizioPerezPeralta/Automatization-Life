from pathlib import Path

import pytest

from automatization_life.config import load_config, validate_config
from automatization_life.errors import ValidationError


def test_validate_config_rejects_unknown_action() -> None:
    with pytest.raises(ValidationError, match="Acción inválida"):
        validate_config({"automations": [{"name": "x", "tasks": [{"action": "format"}]}]})


def test_load_config(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text("automations:\n  - name: demo\n    tasks:\n      - action: mkdir\n        path: out\n", encoding="utf-8")
    assert load_config(path)["automations"][0]["name"] == "demo"
