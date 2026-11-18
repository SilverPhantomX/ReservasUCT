from models.usuario_model import Usuario
from services.persistencia_usuarios import guardar_usuarios, cargar_usuarios


class GestorUsuarios:

    def __init__(self):
        self.usuarios = []
        self.cargar()


    def cargar(self):
        datos = cargar_usuarios()

        for dato in datos:
            usuario = Usuario(
                dato["nombre"],
                dato["correo"],
                dato["contrasena"],
                dato["rol"]
            )

            usuario.fecha_registro = dato["fecha_registro"]

            self.usuarios.append(usuario)


    def agregar(self, usuario):
        errores = usuario.validar()

        for existente in self.usuarios:
            if existente.correo == usuario.correo:
                errores.append("Ya existe un usuario con ese correo.")

        if not errores:
            self.usuarios.append(usuario)
            guardar_usuarios(self.usuarios)

        return errores