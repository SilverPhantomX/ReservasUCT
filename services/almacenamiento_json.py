"""
Acceso a disco para TODA la app (sin Kivy).
Es el único módulo que abre archivos JSON: el resto de los servicios lo usa,
y las vistas nunca lo tocan directamente.

Programación defensiva: si un archivo no existe, está dañado o no se puede escribir,
se registra con `logging` y se devuelve un valor seguro en vez de cerrar la app.
"""
import json
import logging
import os

logger = logging.getLogger(__name__)

# Carpeta data/ en la raíz del proyecto (no depende de desde dónde se ejecute main.py)
RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRECTORIO_DATOS = os.path.join(RAIZ_PROYECTO, "data")


def ruta_datos(nombre_archivo):
    return os.path.join(DIRECTORIO_DATOS, nombre_archivo)


def leer_json(ruta, por_defecto=None):
    """Devuelve el contenido del archivo, o `por_defecto` si no existe o no se puede leer."""
    if not os.path.exists(ruta):
        return por_defecto

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except json.JSONDecodeError as error:
        logger.error("Archivo JSON dañado (%s): %s", ruta, error)
    except OSError as error:
        logger.error("No se pudo leer %s: %s", ruta, error)

    return por_defecto


def escribir_json(ruta, datos):
    """Guarda `datos` en el archivo. Devuelve True si se guardó, False si hubo un error."""
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        return True
    except (OSError, TypeError) as error:
        logger.error("No se pudo guardar %s: %s", ruta, error)
        return False


def eliminar_archivo(ruta):
    """Borra el archivo si existe. Devuelve True si quedó borrado."""
    try:
        if os.path.exists(ruta):
            os.remove(ruta)
        return True
    except OSError as error:
        logger.error("No se pudo eliminar %s: %s", ruta, error)
        return False
