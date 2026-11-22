import json
import os

ARCHIVO_SESION = "data/sesion.json"


def guardar_sesion(usuario):
    datos = {
        "correo": usuario.correo
    }

    with open(ARCHIVO_SESION, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)


def cargar_sesion():
    if not os.path.exists(ARCHIVO_SESION):
        return None

    with open(ARCHIVO_SESION, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def cerrar_sesion():
    if os.path.exists(ARCHIVO_SESION):
        os.remove(ARCHIVO_SESION)