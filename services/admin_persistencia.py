"""
Origen de datos del PANEL DE ADMINISTRADOR (independiente de la app móvil).

El panel solo conoce `listar()`. Hoy lee un JSON propio del panel (datos_admin/reservas.json);
cuando exista la base SQL se crea RepositorioAdminSQL con el mismo método y se cambia
UNA línea en admin_pc.py. Nada de la app móvil se usa ni se modifica.

Cada reserva es un dict con el mismo formato que Reserva.to_dict():
nombre, correo, sala, dia (d/m/aaaa), hora, motivo, acompanantes, codigo_acceso, fecha_registro
"""
import json
import os


class RepositorioAdmin:
    """Contrato: cualquier origen de datos (JSON, SQL, API) debe ofrecer listar()."""

    def listar(self):
        """Devuelve la lista de reservas como diccionarios."""
        raise NotImplementedError


class RepositorioAdminJSON(RepositorioAdmin):
    def __init__(self, ruta="datos_admin/reservas.json"):
        self.ruta = ruta

    def listar(self):
        if not os.path.exists(self.ruta):
            return []
        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []  # archivo vacío o a medio escribir