import json
import os

ARCHIVO_USUARIOS = "data/usuarios.json"


def guardar_usuarios(usuarios):
    datos = [usuario.to_dict() for usuario in usuarios]

    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)


def cargar_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS):
        return []

    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
        return json.load(archivo)