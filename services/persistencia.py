import json
import os

ARCHIVO_RESERVAS = "reserva/reservas.json"


def guardar_reservas(reservas):
    
    datos = [reserva.to_dict() for reserva in reservas]
    
    with open(ARCHIVO_RESERVAS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)


def cargar_reservas():
    
    if not os.path.exists(ARCHIVO_RESERVAS):
        return []
    
    with open(ARCHIVO_RESERVAS, "r", encoding="utf-8") as archivo:
        return json.load(archivo)