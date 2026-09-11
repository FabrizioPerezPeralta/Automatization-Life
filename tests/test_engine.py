from pathlib import Path

from automatization_life.engine import run_automation
from automatization_life.errors import ConfirmationRequired


def test_dry_run_does_not_write(tmp_path: Path) -> None:
    target = tmp_path / "created.txt"
    automation = {
        "name": "demo",
        "tasks": [{"action": "write_text", "path": str(target), "content": "hola"}],
    }
    assert run_automation(automation, dry_run=True) == 1
    assert not target.exists()


def test_write_text_creates_file(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "created.txt"
    automation = {
        "name": "demo",
        "tasks": [{"action": "write_text", "path": str(target), "content": "hola"}],
    }
    run_automation(automation)
    assert target.read_text(encoding="utf-8") == "hola"


def test_delete_requires_confirmation(tmp_path: Path) -> None:
    target = tmp_path / "file.txt"
    target.write_text("x", encoding="utf-8")
    automation = {"name": "demo", "tasks": [{"action": "delete", "path": str(target)}]}
    try:
        run_automation(automation)
    except ConfirmationRequired:
        pass
    else:
        raise AssertionError("delete debe requerir confirmación")
    assert target.exists()
