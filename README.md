# Alpyro Saludador

Un paquete de ejemplo para aprender a crear paquetes Python con las mejores prácticas modernas.

## Características

- Comando CLI simple para saludar
- Soporte para múltiples idiomas (español, inglés, francés)
- Estadísticas de texto
- Estructura moderna con `pyproject.toml`
- Tests incluidos

## Instalación

### Instalación en modo desarrollo

Para trabajar en el paquete y probarlo localmente:

```bash
cd alpyro-saludador
pip install -e .
```

### Instalación con dependencias de desarrollo

```bash
pip install -e ".[dev]"
```

### Instalación normal

```bash
pip install .
```

## Uso

### Como comando CLI

Después de instalar el paquete, tendrás acceso al comando `saludar`:

```bash
# Saludo básico
saludar

# Saludar a alguien específico
saludar Juan

# Saludo en inglés
saludar María --idioma en

# Saludo en francés con hora
saludar Pedro --idioma fr --incluir-hora

# Ver estadísticas del saludo
saludar "Mundo" --stats

# Ver versión
saludar --version

# Ver ayuda
saludar --help
```

### Como librería Python

También puedes usar las funciones directamente en tu código:

```python
from alpyro_saludador import saludar, saludar_personalizado, obtener_estadisticas_saludo

# Saludo simple
mensaje = saludar("Juan")
print(mensaje)  # ¡Hola, Juan!

# Saludo personalizado
mensaje = saludar_personalizado("María", idioma="en", incluir_hora=True)
print(mensaje)  # Hello, María! How are you? (Hora actual: 15:30)

# Obtener estadísticas
stats = obtener_estadisticas_saludo("¡Hola Mundo!")
print(stats)
# {'caracteres': 12, 'palabras': 2, 'tiene_exclamacion': True, 'tiene_interrogacion': False}
```

## Desarrollo

### Ejecutar tests

```bash
pytest
```

### Ejecutar tests con cobertura

```bash
pytest --cov=alpyro_saludador --cov-report=html
```

### Formatear código

```bash
black src/ tests/
```

### Linting

```bash
ruff check src/ tests/
```

## Estructura del proyecto

```
alpyro-saludador/
├── pyproject.toml              # Configuración del proyecto
├── README.md                   # Este archivo
├── .gitignore                  # Archivos ignorados por git
├── src/
│   └── alpyro_saludador/       # Paquete principal
│       ├── __init__.py         # Inicialización del paquete
│       ├── saludador.py        # Módulo con funciones de saludo
│       └── cli.py              # Interfaz de línea de comandos
└── tests/
    ├── __init__.py
    └── test_saludador.py       # Tests del módulo
```

## Construir el paquete

Para construir distribuciones del paquete:

```bash
# Instalar build si no lo tienes
pip install build

# Construir
python -m build
```

Esto generará archivos en `dist/`:
- `alpyro_saludador-0.1.0-py3-none-any.whl` (wheel)
- `alpyro-saludador-0.1.0.tar.gz` (source distribution)

## Publicar en PyPI

```bash
# Instalar twine si no lo tienes
pip install twine

# Subir a TestPyPI (para pruebas)
twine upload --repository testpypi dist/*

# Subir a PyPI (producción)
twine upload dist/*
```

## Licencia

MIT

## Autor

Tu Nombre <tu@email.com>
