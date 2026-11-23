from datetime import datetime

ROLES = ["Estudiante", "Administrador"]

class Usuario:

    def __init__(
        self,
        nombre,
        correo,
        contrasena,
        rol="Estudiante"
    ):
        self.nombre = nombre.strip()
        self.correo = correo.strip().lower()
        self.contrasena = contrasena
        self.rol = rol
        self.fecha_registro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        @classmethod
        def desde_dict(cls, datos):
            # Inverso de to_dict(): reconstruye el usuario guardado en el JSON
            usuario = cls(datos["nombre"], datos["correo"], datos["contrasena"], datos.get("rol", "Estudiante"))
            usuario.fecha_registro = datos.get("fecha_registro", usuario.fecha_registro)
            return usuario
        
        def verificar_contrasena(self, contrasena):
            return self.contrasena == contrasena
        
        def es_administrador(self):
            return self.rol == "Administrador"
    
    def validar(self):
        errores = []

        if self.nombre == "":
            errores.append("Debe ingresar un nombre.")

        if "@" not in self.correo or "." not in self.correo:
            errores.append("Debe ingresar un correo válido.")

        if len(self.contrasena) < 6:
            errores.append(
                "La contraseña debe tener al menos 6 caracteres."
            )

        if self.rol not in ["Estudiante", "Administrador"]:
            errores.append("Rol de usuario no válido.")

        return errores

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "correo": self.correo,
            "contrasena": self.contrasena,
            "rol": self.rol,
            "fecha_registro": self.fecha_registro
        }
        
    def es_administrador(self):
        return self.rol == "Administrador"