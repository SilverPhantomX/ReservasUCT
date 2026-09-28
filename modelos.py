"""
Lógica de ReservasUCT (sin interfaz gráfica).
- Reserva: guarda los datos de UNA reserva y sabe validarse.
- GestorReservas: guarda la lista de reservas y evita choques de horario.
"""
SALAS = ["Sala de piano", "Sala de teoria musical", "Auditorio", "Sala de percusión"]
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
HORAS = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
MOTIVOS = ["Estudio", "Ensayo"]
MAX_ACOMPANANTES = 3

#Clase reserva :)
class Reserva:
    #Una reserva de sala por un bloque de 1 hora
    
    #constructor de las reservas
    def __init__(self, nombre, correo, sala, dia, hora, motivo, acompanantes):
        self.nombre = nombre.strip()
        self.correo = correo.strip()
        self.sala = sala
        self.dia = dia
        self.hora = hora
        self.motivo = motivo
        self.acompanantes = acompanantes

    #Valida los datos del usuario
    def validar(self):
        #Devuelve una lista con los errores encontrados (vacía si está todo bien).
        errores = []
        #lista de posibles errores que el usario puede cometer
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

    #funcion para ver si una reserva choca con otra
    def choca_con(self, otra):
        #True si las dos reservas piden la misma sala, el mismo día y a la misma hora.
        return self.sala == otra.sala and self.dia == otra.dia and self.hora == otra.hora

    #funcion para obtener el resumen del la reserva
    def resumen(self):
        return (f"{self.nombre}\n{self.sala}\n{self.dia} a las {self.hora}\n"
                f"Motivo: {self.motivo} - Acompañantes: {self.acompanantes}")


#Administra todas las reservas de la academia
class GestorReservas:

    #constructor del gestor
    def __init__(self):
        self.reservas = []

    #funcion de agregar reserva
    def agregar(self, reserva):
        #Intenta guardar la reserva. Devuelve la lista de errores (si está vacía, la reserva se guardó)
        errores = reserva.validar()
        for existente in self.reservas:
            if reserva.choca_con(existente):
                errores.append(f"{reserva.sala} ya está reservada el {reserva.dia} a las {reserva.hora}.")
        if not errores:
            self.reservas.append(reserva)
        return errores

    #Funcion para eliminar reserva
    def anular(self, reserva):
        self.reservas.remove(reserva)