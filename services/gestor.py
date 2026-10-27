from services.persistencia import guardar_reservas
from models.reserva_model import Reserva
from services.persistencia import cargar_reservas
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
            if reserva.choca_con(existente):
                errores.append(f"{reserva.sala} ya está reservada el {reserva.dia} a las {reserva.hora}.")
                
        if not errores:
            reserva.codigo_acceso = self.generar_codigo_acceso()
            self.reservas.append(reserva)
            
        guardar_reservas(self.reservas)
        
        return errores

    #Funcion para eliminar reserva
    def anular(self, reserva):
        self.reservas.remove(reserva)
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
                dato["codigo_acceso"]
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