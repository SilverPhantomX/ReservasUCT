"""
Lógica de la agenda semanal (sin interfaz gráfica, sin Kivy).
La vista solo dibuja lo que estas funciones devuelven.
"""
from datetime import datetime, timedelta

from models.reserva_model import HORAS

FORMATOS_FECHA = ("%Y-%m-%d", "%d/%m/%Y")  # la app móvil guarda d/m/aaaa en Reserva.dia
DIAS_HABILES = 5  # Lunes a Viernes


def fecha_de(reserva):
    """Devuelve la fecha (date) de una reserva (dict), o None si no tiene una fecha válida."""
    texto = reserva.get("fecha") or reserva.get("dia") or ""
    for formato in FORMATOS_FECHA:
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            pass
    return None  # por ejemplo reservas antiguas que solo decían "Lunes"


def lunes_de(fecha):
    return fecha - timedelta(days=fecha.weekday())


def dias_de_semana(lunes):
    return [lunes + timedelta(days=i) for i in range(DIAS_HABILES)]


def reservas_por_celda(reservas, lunes):
    """{(date, 'HH:MM'): [reservas]} solo para los días de la semana que empieza en `lunes`."""
    dias = set(dias_de_semana(lunes))
    celdas = {}
    for r in reservas:
        f = fecha_de(r)
        if f in dias and r.get("hora") in HORAS:
            celdas.setdefault((f, r["hora"]), []).append(r)
    return celdas


def total(celdas):
    return sum(len(v) for v in celdas.values())