from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screenmanager import MDScreenManager
from services.gestor import GestorReservas
from kivymd.uix.boxlayout import MDBoxLayout
from services.analytics_service import registrar_evento
from views.barra_navegacion import BarraNavegacion
from views.calendario import Calendario
from views.formulario import FormularioScreen
from views.reserva_view import ReservaScreen
from views.perfil_view import PerfilView
from services.gestor_usuarios import GestorUsuarios
from views.login import LoginScreen
from views.registro import RegistroScreen
from services.persistencia_sesion import cargar_sesion

Window.size = (400, 600)

class MiApp(MDApp):
    def build(self):
        
        registrar_evento("app_abierta")
        Window.clearcolor = (1, 1, 1, 1)
        self.gestor = GestorReservas()
        self.gestor_usuarios = GestorUsuarios()
        self.usuario_actual = None
        sesion = cargar_sesion()
        if sesion is not None:
            for usuario in self.gestor_usuarios.usuarios:
                if usuario.correo == sesion["correo"]:
                    self.usuario_actual = usuario
                break
        
        self.seleccion = {"sala": None, "dia": None, "hora_inicio": None, "hora_termino": None, "motivo": None, "acompanantes": 0}
        self.textos_botones = {}   

        #administra las pantallas
        sm = MDScreenManager()
        sm.add_widget(Calendario(name="calendario"))
        sm.add_widget(FormularioScreen(name="formulario"))
        sm.add_widget(ReservaScreen(name="reservas"))
        sm.add_widget(PerfilView(name="perfil"))

        raiz = MDBoxLayout(orientation="vertical")
        raiz.add_widget(sm)                      # las pantallas arriba
        raiz.add_widget(BarraNavegacion(sm))     # la barra, una sola vez, abajo
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegistroScreen(name="registro"))
        if self.usuario_actual is not None:
            sm.current = "calendario"
        else:
            sm.current = "login"
            
        return raiz

if __name__ == "__main__":
    MiApp().run()