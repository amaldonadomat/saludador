"""
Interfaz de línea de comandos para alpyro-saludador.
"""

import argparse
import sys
from . import __version__
from .saludador import saludar, saludar_personalizado, obtener_estadisticas_saludo


def main():
    """
    Punto de entrada principal del comando CLI.
    """
    parser = argparse.ArgumentParser(
        prog="saludar",
        description="Un comando CLI de ejemplo para saludar",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  saludar Juan
  saludar María --idioma en
  saludar Pedro --idioma fr --incluir-hora
  saludar Luigi --idioma it
  saludar João --idioma pt
  saludar Anna --idioma pl
  saludar --stats "Hola Mundo"
        """
    )

    parser.add_argument(
        "nombre",
        nargs="?",
        default="Mundo",
        help="Nombre a saludar (por defecto: Mundo)"
    )

    parser.add_argument(
        "-i", "--idioma",
        choices=["es", "en", "fr", "it", "pt", "pl"],
        default="es",
        help="Idioma del saludo (es, en, fr, it, pt, pl)"
    )

    parser.add_argument(
        "--incluir-hora",
        action="store_true",
        help="Incluir la hora actual en el saludo"
    )

    parser.add_argument(
        "-s", "--stats",
        action="store_true",
        help="Mostrar estadísticas del saludo generado"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    # Generar el saludo
    if args.idioma == "es" and not args.incluir_hora:
        mensaje = saludar(args.nombre)
    else:
        mensaje = saludar_personalizado(
            args.nombre,
            idioma=args.idioma,
            incluir_hora=args.incluir_hora
        )

    # Mostrar el saludo
    print(mensaje)

    # Mostrar estadísticas si se solicita
    if args.stats:
        stats = obtener_estadisticas_saludo(mensaje)
        print("\nEstadísticas del saludo:")
        print(f"  - Caracteres: {stats['caracteres']}")
        print(f"  - Palabras: {stats['palabras']}")
        print(f"  - Tiene exclamación: {'Sí' if stats['tiene_exclamacion'] else 'No'}")
        print(f"  - Tiene interrogación: {'Sí' if stats['tiene_interrogacion'] else 'No'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
