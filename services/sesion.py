"""
Manejo de la sesión del usuario (sin Kivy).
Las vistas solo llaman a iniciar(), cerrar() y leen `usuario`;
no saben cómo se valida la contraseña ni dónde se guarda la sesión.
"""
from services.persistencia_sesion import guardar_sesion, cargar_sesion, cerrar_sesion


class Sesion:

    def __init__(self, gestor_usuarios):
        self.gestor_usuarios = gestor_usuarios
        self.usuario = None

    def esta_activa(self):
        return self.usuario is not None

    def restaurar(self):
        """Recupera la sesión guardada en disco (si existe y el usuario sigue registrado)."""
        datos = cargar_sesion()
        if datos is None:
            return False

        usuario = self.gestor_usuarios.buscar_por_correo(datos.get("correo", ""))
        if usuario is None:
            cerrar_sesion()  # la sesión apunta a un usuario que ya no existe
            return False

        self.usuario = usuario
        return True

    def iniciar(self, correo, contrasena):
        """Intenta iniciar sesión. Devuelve la lista de errores (vacía si entró)."""
        usuario, errores = self.gestor_usuarios.autenticar(correo, contrasena)
        if errores:
            return errores

        self.usuario = usuario
        guardar_sesion(usuario)
        return []

    def cerrar(self):
        self.usuario = None
        cerrar_sesion()
