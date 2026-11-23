import json
import logging
import os
from datetime import datetime

ARCHIVO_ANALYTICS = "data/analytics_events.json"

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def registrar_evento(nombre_evento, propiedades=None):
    if propiedades is None:
        propiedades = {}

    evento = {
        "evento": nombre_evento,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "propiedades": propiedades
    }

    try:
        os.makedirs("data", exist_ok=True)

        eventos = []

        if os.path.exists(ARCHIVO_ANALYTICS):
            with open(
                ARCHIVO_ANALYTICS,
                "r",
                encoding="utf-8"
            ) as archivo:
                eventos = json.load(archivo)

        eventos.append(evento)

        with open(
            ARCHIVO_ANALYTICS,
            "w",
            encoding="utf-8"
        ) as archivo:
            json.dump(
                eventos,
                archivo,
                ensure_ascii=False,
                indent=4
            )

    except (OSError, json.JSONDecodeError) as error:
        logging.error(
            "Error al registrar evento de analytics: %s",
            error
        )