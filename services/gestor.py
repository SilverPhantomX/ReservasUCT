from services.persistencia import guardar_reservas
from services.persistencia import cargar_reservas
from models.reserva_model import Reserva ,HORAS, ESTADOS
import random

#Administra todas las reservas de la academia
class GestorReservas:

    def __init__(self):
        self.reservas = []
        self.cargar()
        


    #funcion de agregar reserva
    def agregar(self, reserva):
        
        #Intenta guardar la reserva. Devuelve la lista de errores (si está vacía, la reserva se guardó)
        errores = reserva.validar()
        
        for existente in self.reservas:
            if (reserva.choca_con(existente) and existente.estado != "Cancelada"):
                errores.append(
                    f"{reserva.sala} ya está reservada "
                    f"el {reserva.dia} a las {reserva.hora_inicio}.")
                
        if not errores:
            reserva.codigo_acceso = self.generar_codigo_acceso()
            self.reservas.append(reserva)     
            guardar_reservas(self.reservas)
        
        return errores

    #Funcion para eliminar reserva
    def anular(self, reserva):
        reserva.estado = "Cancelada"
        guardar_reservas(self.reservas)
        
    def cargar(self):
        datos = cargar_reservas()
    
        for dato in datos:
            reserva = Reserva(
                dato["nombre"],
                dato["correo"],
                dato["sala"],
                dato["dia"],
                dato["hora_inicio"],
                dato["hora_termino"],
                dato["motivo"],
                dato["acompanantes"],
                dato["codigo_acceso"],
                dato["estado"],
                dato["usuario_correo"]
            )
    
            reserva.fecha_registro = dato["fecha_registro"]
    
            self.reservas.append(reserva)
            
    def generar_codigo_acceso(self):
        while True:
            codigo = random.randint(100000, 999999)

            repetido = any(
                reserva.codigo_acceso == codigo
                for reserva in self.reservas
            )

            if not repetido:
                return codigo  
            
    def horas_ocupadas(self, dia, sala):
        # Todas las horas (bloques de 1 h) ya tomadas ese día en esa sala
        ocupadas = set()
        for r in self.reservas:
            if r.dia == dia and r.sala == sala and r.estado != "Cancelada":
                ocupadas.update(h for h in HORAS if r.hora_inicio <= h < r.hora_termino)
        return ocupadas
            
    def obtener_horas_disponibles(self, dia, sala):
        # Horas en que se puede EMPEZAR. La última de HORAS (21:00) es solo el cierre.
        ocupadas = self.horas_ocupadas(dia, sala)
        
        return [h for h in HORAS[:-1] if h not in ocupadas]
        
    def obtener_horas_termino(self, dia, sala, hora_inicio):
        # Horas de término posibles: hasta la siguiente reserva (pegadas se permiten)
        ocupadas = self.horas_ocupadas(dia, sala)
        opciones = []
        for h in HORAS:
            if h <= hora_inicio:
                continue
            opciones.append(h)
            if h in ocupadas:      # desde aquí ya hay otra reserva: no se puede pasar
                break
        return opciones
    
    def reservas_activas(self):
        return [reserva for reserva in self.reservas
            if reserva.esta_activa()
        ]
        
    def reservas_de(self, usuario):

        if usuario is None:
            return []

        if usuario.es_administrador():
            return self.reservas

        return [
            reserva
            for reserva in self.reservas
            if reserva.usuario_correo == usuario.correo
        ]
        
    def resumen_de(self, usuario):
        
        reservas = self.reservas_de(usuario)
        resumen = {
            "total": len(reservas)
        }
        for estado in ESTADOS:
            resumen[estado] = sum(
                1 for reserva in reservas
                if reserva.estado == estado
            )
        return resumen