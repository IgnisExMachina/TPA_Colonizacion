"""Punto de entrada del programa. Ejecutar con:  python src/main.py"""
import sys
from pathlib import Path

# Añadimos la carpeta 'src' a las rutas de búsqueda para que funcionen los imports del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Lo que se imprime se ve tambien en el panel de registro de la interfaz.
# Va antes de importar Interfaz para que el logging de GestorPersistencia use ya la salida redirigida.
from interfaz.Registro import instalar_redireccion
instalar_redireccion()

from interfaz.Interfaz import Interfaz


def main():
    app = Interfaz()
    app.start()


if __name__ == "__main__":
    main()
