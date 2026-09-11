class AutomationError(Exception):
    """Error esperado al cargar o ejecutar una automatización."""


class ValidationError(AutomationError):
    """La configuración no cumple el esquema soportado."""


class ConfirmationRequired(AutomationError):
    """La acción requiere confirmación explícita."""

