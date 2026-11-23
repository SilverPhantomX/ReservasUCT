"""
Lógica de ReservasUCT (sin interfaz gráfica).
- Reserva: guarda los datos de UNA reserva y sabe validarse.
- GestorReservas: guarda la lista de reservas y evita choques de horario.
"""
from datetime import datetime

SALAS = ["Sala de piano", "Sala de teoria músical", "Auditorio", "Sala de percusión"]
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
HORAS = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
HORAS_INICIO = HORAS[:-1]
HORAS_TERMINO = HORAS[1:]
MOTIVOS = ["Estudio", "Ensayo"]
MAX_ACOMPANANTES = 3
ESTADOS = ["Pendiente", "Confirmada", "Cancelada", "Finalizada"]
ESTADOS_ACTIVOS = ["Pendiente", "Confirmada"]



#Clase reserva :)
class Reserva:
    #Una reserva de sala por un bloque de 1 hora
    
    #constructor de las reservas
    def __init__(self, nombre, correo, sala, dia, hora_inicio, hora_termino, motivo, acompanantes, codigo_acceso=None, estado="Pendiente", usuario_correo=None):
        self.nombre = nombre.strip()
        self.correo = correo.strip()
        self.sala = sala
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_termino = hora_termino
        self.motivo = motivo
        self.acompanantes = acompanantes
        self.codigo_acceso = codigo_acceso
        self.estado = estado
        self.fecha_registro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.usuario_correo = usuario_correo
        
        
    def to_dict(self):
        # Serializa los atributos en un diccionario para la persistencia
        return {
            "nombre": self.nombre,
            "correo": self.correo,
            "sala": self.sala,
            "dia": self.dia,
            "hora_inicio": self.hora_inicio,
            "hora_termino": self.hora_termino,
            "motivo": self.motivo,
            "acompanantes": self.acompanantes,
            "codigo_acceso": self.codigo_acceso,
            "fecha_registro": self.fecha_registro,
            "estado": self.estado,   
            "usuario_correo": self.usuario_correo
        }

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
        if self.hora_inicio is None:
            errores.append("Debe elegir una hora de inicio.")
        if self.hora_termino is None:
            errores.append("Debe elegir una hora de termino.")
        if self.motivo is None:
            errores.append("Debe elegir un motivo.")
        if self.acompanantes > MAX_ACOMPANANTES:
            errores.append(f"Máximo {MAX_ACOMPANANTES} acompañantes.")
        if (self.hora_inicio is not None and self.hora_termino is not None and self.hora_termino <= self.hora_inicio):
            errores.append("La hora de término debe ser posterior a la hora de inicio.")
        return errores

    #funcion para ver si una reserva choca con otra
    def choca_con(self, otra):
        if self.sala != otra.sala:
            return False
    
        if self.dia != otra.dia:
            return False
    
        if otra.estado == "Cancelada":
            return False
    
        return (
            self.hora_inicio < otra.hora_termino
            and self.hora_termino > otra.hora_inicio
        )
    
    
    #funcion para obtener el resumen del la reserva
    def resumen(self):
        return (f"Registrado el: {self.fecha_registro}\n"
                f"Sala: {self.sala}\n"
                f"Día: {self.dia}\n" 
                f"Horario: De {self.hora_inicio}hs a {self.hora_termino}hs\n"
                f"Motivo: {self.motivo}\n"
                f"Acompañantes: {self.acompanantes}\n"
                f"Codigo de acceso: {self.codigo_acceso}\n"
                f"Estado: {self.estado}\n")
        
    def esta_activa(self):
        return self.estado in ESTADOS_ACTIVOS
    
    def ocupa_bloque(self, hora):
        return self.hora_inicio <= hora < self.hora_termino