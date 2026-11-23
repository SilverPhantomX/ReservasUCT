import json
import logging

ARCHIVO_CONFIG = "data/remote_config.json"


def cargar_config():
    try:
        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    except (OSError, json.JSONDecodeError) as error:
        logging.error("Error cargando remote_config: %s", error)
        return {}


def obtener_texto_confirmacion():
    config = cargar_config()

    try:
        datos = config["boton_reserva"]

        if not datos["activo"]:
            return "CONFIRMAR RESERVA"

        variante = datos["variante"]

        return datos[variante]["texto_boton"]

    except KeyError:
        return "CONFIRMAR RESERVA"


def obtener_guia_reserva():
    config = cargar_config()

    try:
        datos = config["guia_reserva"]

        if not datos["activo"]:
            return {
                "mostrar_mensaje": False,
                "variante": "A"
            }

        variante = datos["variante"]
        opcion = datos[variante]

        return {
            "mostrar_mensaje": opcion.get("mostrar_mensaje", False),
            "mensaje": opcion.get("mensaje", ""),
            "variante": variante
        }

    except KeyError:
        return {
            "mostrar_mensaje": False,
            "mensaje": "",
            "variante": "A"
        }