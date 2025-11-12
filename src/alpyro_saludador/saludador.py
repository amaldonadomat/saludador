"""
Módulo principal con funciones de saludo.
"""

from typing import Optional
from datetime import datetime


def saludar(nombre: str = "Mundo") -> str:
    """
    Genera un saludo simple.

    Args:
        nombre: El nombre a saludar. Por defecto "Mundo".

    Returns:
        Un mensaje de saludo.

    Examples:
        >>> saludar("Juan")
        '¡Hola, Juan!'
        >>> saludar()
        '¡Hola, Mundo!'
    """
    return f"¡Hola, {nombre}!"


def saludar_personalizado(
    nombre: str,
    idioma: str = "es",
    incluir_hora: bool = False
) -> str:
    """
    Genera un saludo personalizado en diferentes idiomas.

    Args:
        nombre: El nombre a saludar.
        idioma: Código del idioma ('es', 'en', 'fr'). Por defecto 'es'.
        incluir_hora: Si se debe incluir la hora actual. Por defecto False.

    Returns:
        Un mensaje de saludo personalizado.

    Examples:
        >>> saludar_personalizado("María", idioma="es")
        '¡Hola, María! ¿Cómo estás?'
        >>> saludar_personalizado("John", idioma="en")
        'Hello, John! How are you?'
    """
    saludos = {
        "es": f"¡Hola, {nombre}! ¿Cómo estás?",
        "en": f"Hello, {nombre}! How are you?",
        "fr": f"Bonjour, {nombre}! Comment allez-vous?",
    }

    saludo = saludos.get(idioma, saludos["es"])

    if incluir_hora:
        hora_actual = datetime.now().strftime("%H:%M")
        saludo += f" (Hora actual: {hora_actual})"

    return saludo


def obtener_estadisticas_saludo(texto: str) -> dict:
    """
    Obtiene estadísticas básicas de un texto de saludo.

    Args:
        texto: El texto a analizar.

    Returns:
        Un diccionario con estadísticas del texto.

    Examples:
        >>> stats = obtener_estadisticas_saludo("¡Hola Mundo!")
        >>> stats['caracteres']
        12
    """
    return {
        "caracteres": len(texto),
        "palabras": len(texto.split()),
        "tiene_exclamacion": "!" in texto,
        "tiene_interrogacion": "?" in texto,
    }
