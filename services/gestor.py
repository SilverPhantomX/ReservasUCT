from services.persistencia import guardar_reservas
from models.reserva_model import Reserva
from services.persistencia import cargar_reservas
from models.reserva_model import HORAS
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
                    f"el {reserva.dia} a las {reserva.hora}.")
                
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
                dato["hora"],
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
            
    def obtener_horas_disponibles(self, dia, sala):
        horas_ocupadas = []

        for reserva in self.reservas:
            if (reserva.dia == dia and reserva.sala == sala and reserva.estado != "Cancelada"
                ):
                horas_ocupadas.append(reserva.hora)

        return [
            hora for hora in HORAS
            if hora not in horas_ocupadas
        ]
        