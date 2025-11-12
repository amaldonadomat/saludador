"""
Alpyro Saludador - Un paquete de ejemplo para aprender a crear paquetes Python.
"""

# La versión se obtiene dinámicamente de Git tags vía setuptools-scm
try:
    from ._version import version as __version__
except ImportError:
    # Fallback si el archivo _version.py no existe (ej: desarrollo sin instalación)
    __version__ = "0.0.0.dev0+unknown"

from .saludador import saludar, saludar_personalizado, obtener_estadisticas_saludo

__all__ = ["saludar", "saludar_personalizado", "obtener_estadisticas_saludo"]
