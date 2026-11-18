from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screenmanager import MDScreenManager
from services.gestor import GestorReservas
from kivymd.uix.boxlayout import MDBoxLayout

from views.barra_navegacion import BarraNavegacion
from views.calendario import Calendario
from views.formulario import FormularioScreen
from views.reserva_view import ReservaScreen
from views.perfil_view import PerfilView

Window.size = (400, 600)

class MiApp(MDApp):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.gestor = GestorReservas()
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
        return raiz

if __name__ == "__main__":
    MiApp().run()