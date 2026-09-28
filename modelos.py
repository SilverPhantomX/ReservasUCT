"""
Lógica de ReservasUCT (sin interfaz gráfica).

- Reserva: guarda los datos de UNA reserva y sabe validarse.
- GestorReservas: guarda la lista de reservas y evita choques de horario.
"""

SALAS = ["Sala de Piano", "Sala de Ensayo", "Cabina Individual", "Sala de Percusión"]
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
HORAS = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
MOTIVOS = ["Estudio", "Ensayo", "Clases"]
MAX_ACOMPANANTES = 3


class Reserva:
    """Una reserva de sala por un bloque de 1 hora."""

    def __init__(self, nombre, correo, sala, dia, hora, motivo, acompanantes):
        self.nombre = nombre.strip()
        self.correo = correo.strip()
        self.sala = sala
        self.dia = dia
        self.hora = hora
        self.motivo = motivo
        self.acompanantes = acompanantes

    def validar(self):
        """Devuelve una lista con los errores encontrados (vacía si está todo bien)."""
        errores = []
        if self.nombre == "":
            errores.append("Debe ingresar su nombre.")
        if "@" not in self.correo or "." not in self.correo:
            errores.append("Debe ingresar un correo válido.")
        if self.sala is None:
            errores.append("Debe elegir una sala.")
        if self.dia is None:
            errores.append("Debe elegir un día.")
        if self.hora is None:
            errores.append("Debe elegir una hora.")
        if self.motivo is None:
            errores.append("Debe elegir un motivo.")
        if self.acompanantes > MAX_ACOMPANANTES:
            errores.append(f"Máximo {MAX_ACOMPANANTES} acompañantes.")
        return errores

    def choca_con(self, otra):
        """True si las dos reservas piden la misma sala, el mismo día y a la misma hora."""
        return self.sala == otra.sala and self.dia == otra.dia and self.hora == otra.hora

    def resumen(self):
        return (f"{self.nombre}\n{self.sala}\n{self.dia} a las {self.hora}\n"
                f"Motivo: {self.motivo} - Acompañantes: {self.acompanantes}")


class GestorReservas:
    """Administra todas las reservas de la academia."""

    def __init__(self):
        self.reservas = []

    def agregar(self, reserva):
        """Intenta guardar la reserva. Devuelve la lista de errores
        (si está vacía, la reserva se guardó)."""
        errores = reserva.validar()
        for existente in self.reservas:
            if reserva.choca_con(existente):
                errores.append(f"{reserva.sala} ya está reservada el {reserva.dia} a las {reserva.hora}.")
        if not errores:
            self.reservas.append(reserva)
        return errores

    def anular(self, reserva):
        self.reservas.remove(reserva)
