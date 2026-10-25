#Administra todas las reservas de la academia
class GestorReservas:

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