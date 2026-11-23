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
    
    def buscar_por_correo(self, correo):
        #Devuelve el usuario con ese correo, o None si no existe.
        correo = correo.strip().lower()

        for usuario in self.usuarios:
            if usuario.correo == correo:
                return usuario

        return None


    def agregar(self, usuario):
        errores = usuario.validar()

        for existente in self.usuarios:
            if existente.correo == usuario.correo:
                errores.append("Ya existe un usuario con ese correo.")

        if not errores:
            self.usuarios.append(usuario)
            guardar_usuarios(self.usuarios)

        return errores

    def autenticar(self, correo, contrasena):
        #Devuelve (usuario, errores). Si hay errores, usuario es None.
        if correo.strip() == "" or contrasena == "":
            return None, ["Debe ingresar su correo y contraseña."]

        usuario = self.buscar_por_correo(correo)

        if usuario is None or not usuario.verificar_contrasena(contrasena):
            return None, ["Correo o contraseña incorrectos."]

        return usuario, []
