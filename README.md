# Automatization-Life

Primera versión funcional y open source de un ejecutor local de automatizaciones declarativas, con prioridad en Windows y controles explícitos para acciones potencialmente destructivas.

## Arquitectura

El CLI (`automatization_life/cli.py`) carga YAML mediante `config.py`, valida su esquema y delega cada tarea al motor (`engine.py`). Las operaciones están aisladas en `actions.py`; `scheduler.py` ofrece un modo opcional basado en intervalos. El logging se emite como JSON para facilitar diagnóstico y automatización.

Acciones soportadas: `mkdir`, `copy`, `move`, `delete`, `write_text`, `launch` y `shell`. `delete`, `move` y `shell` solicitan confirmación interactiva; `--dry-run` nunca modifica el sistema. No hay control remoto y no se permite ejecutar comandos shell sin confirmación.

## Instalación

Requiere Python 3.11 o superior:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Uso

```powershell
Copy-Item automatization.example.yaml automatization.yaml
automatization-life list
automatization-life --config automatization.yaml --dry-run run preparar-proyecto
automatization-life --config automatization.yaml run preparar-proyecto
automatization-life --config automatization.yaml schedule --interval 60
```

Las rutas aceptan variables de entorno de Windows como `%USERPROFILE%`. Revisa siempre el YAML antes de ejecutar y concede únicamente las confirmaciones esperadas.

### Plugins

Un plugin local puede registrar una acción con `register_action("mi_accion", handler)`. El handler recibe `(task, dry_run)` y debe respetar `dry_run`; los plugins se cargan desde código instalado por el usuario, nunca desde la configuración YAML ni desde la red.

## Contribución

1. Crea un entorno virtual e instala `.[dev]`.
2. Añade o modifica código con pruebas unitarias.
3. Ejecuta `pytest`, `ruff check .` y `mypy automatization_life`.
4. Abre un pull request describiendo el riesgo y el comportamiento de seguridad.

El proyecto usa licencia MIT. Las contribuciones deben mantener la ejecución local, la validación estricta y la confirmación explícita de acciones sensibles.
