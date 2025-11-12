"""
Tests para el módulo saludador.
"""

import pytest
from alpyro_saludador import saludar, saludar_personalizado, obtener_estadisticas_saludo


class TestSaludar:
    """Tests para la función saludar básica."""

    def test_saludar_sin_nombre(self):
        """Test de saludo sin nombre (usa el default)."""
        resultado = saludar()
        assert resultado == "¡Hola, Mundo!"

    def test_saludar_con_nombre(self):
        """Test de saludo con nombre específico."""
        resultado = saludar("Juan")
        assert resultado == "¡Hola, Juan!"

    def test_saludar_con_nombre_complejo(self):
        """Test de saludo con nombre complejo."""
        resultado = saludar("María García")
        assert resultado == "¡Hola, María García!"


class TestSaludarPersonalizado:
    """Tests para la función saludar_personalizado."""

    def test_saludo_espanol_basico(self):
        """Test de saludo en español."""
        resultado = saludar_personalizado("Ana", idioma="es")
        assert resultado == "¡Hola, Ana! ¿Cómo estás?"

    def test_saludo_ingles(self):
        """Test de saludo en inglés."""
        resultado = saludar_personalizado("John", idioma="en")
        assert resultado == "Hello, John! How are you?"

    def test_saludo_frances(self):
        """Test de saludo en francés."""
        resultado = saludar_personalizado("Pierre", idioma="fr")
        assert resultado == "Bonjour, Pierre! Comment allez-vous?"

    def test_saludo_idioma_invalido(self):
        """Test de saludo con idioma inválido (debe usar español por defecto)."""
        resultado = saludar_personalizado("Ana", idioma="de")
        assert resultado == "¡Hola, Ana! ¿Cómo estás?"

    def test_saludo_con_hora(self):
        """Test de saludo que incluye la hora."""
        resultado = saludar_personalizado("Ana", idioma="es", incluir_hora=True)
        assert "¡Hola, Ana! ¿Cómo estás?" in resultado
        assert "Hora actual:" in resultado

    def test_saludo_sin_hora(self):
        """Test de saludo sin hora."""
        resultado = saludar_personalizado("Ana", idioma="es", incluir_hora=False)
        assert "Hora actual:" not in resultado


class TestEstadisticas:
    """Tests para la función obtener_estadisticas_saludo."""

    def test_estadisticas_basicas(self):
        """Test de estadísticas básicas."""
        resultado = obtener_estadisticas_saludo("¡Hola Mundo!")
        assert resultado["caracteres"] == 12
        assert resultado["palabras"] == 2
        assert resultado["tiene_exclamacion"] is True
        assert resultado["tiene_interrogacion"] is False

    def test_estadisticas_con_interrogacion(self):
        """Test de estadísticas con interrogación."""
        resultado = obtener_estadisticas_saludo("¿Cómo estás?")
        assert resultado["tiene_interrogacion"] is True
        assert resultado["tiene_exclamacion"] is False

    def test_estadisticas_texto_vacio(self):
        """Test de estadísticas con texto vacío."""
        resultado = obtener_estadisticas_saludo("")
        assert resultado["caracteres"] == 0
        assert resultado["palabras"] == 0  # split() en string vacío devuelve []

    def test_estadisticas_texto_largo(self):
        """Test de estadísticas con texto largo."""
        texto = "Este es un texto mucho más largo para probar las estadísticas"
        resultado = obtener_estadisticas_saludo(texto)
        assert resultado["caracteres"] == len(texto)
        assert resultado["palabras"] == 11
        assert resultado["tiene_exclamacion"] is False
        assert resultado["tiene_interrogacion"] is False


class TestIntegracion:
    """Tests de integración."""

    def test_flujo_completo_espanol(self):
        """Test del flujo completo en español."""
        nombre = "Pedro"
        saludo = saludar_personalizado(nombre, idioma="es")
        stats = obtener_estadisticas_saludo(saludo)

        assert nombre in saludo
        assert stats["caracteres"] > 0
        assert stats["palabras"] > 0

    def test_flujo_completo_ingles(self):
        """Test del flujo completo en inglés."""
        nombre = "Alice"
        saludo = saludar_personalizado(nombre, idioma="en")
        stats = obtener_estadisticas_saludo(saludo)

        assert nombre in saludo
        assert "Hello" in saludo
        assert stats["tiene_interrogacion"] is True


# Tests parametrizados
@pytest.mark.parametrize("nombre,esperado", [
    ("Juan", "¡Hola, Juan!"),
    ("María", "¡Hola, María!"),
    ("", "¡Hola, !"),
    ("123", "¡Hola, 123!"),
])
def test_saludar_parametrizado(nombre, esperado):
    """Test parametrizado para diferentes nombres."""
    assert saludar(nombre) == esperado


@pytest.mark.parametrize("idioma,palabra_clave", [
    ("es", "Hola"),
    ("en", "Hello"),
    ("fr", "Bonjour"),
])
def test_idiomas_parametrizado(idioma, palabra_clave):
    """Test parametrizado para diferentes idiomas."""
    resultado = saludar_personalizado("Test", idioma=idioma)
    assert palabra_clave in resultado
