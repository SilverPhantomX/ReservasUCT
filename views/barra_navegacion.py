from kivy.metrics import dp
from kivy.app import App
from kivy.utils import get_color_from_hex
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText

AZUL = get_color_from_hex("#01568e")
ACTIVO = (1, 1, 1, 1)
INACTIVO = (1, 1, 1, 0.6)

# Qué pestaña se marca según la pantalla en que estés
PESTANA_DE = {"calendario": "calendario", "formulario": "calendario",
              "reservas": "reservas", "perfil": "perfil"}


class BarraNavegacion(MDBoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(size_hint_y=None, height=dp(70), md_bg_color=AZUL, **kwargs)
        self.sm = screen_manager
        self.items = {}  # destino -> (icono, texto), para poder cambiarles el color

        for icono, texto, destino in (("home", "Inicio", "calendario"),
                                      ("calendar", "Reservas", "reservas"),
                                      ("account", "Perfil", "perfil")):
            w_icono = MDButtonIcon(icon=icono, theme_text_color="Custom", text_color=ACTIVO)
            w_texto = MDButtonText(text=texto, theme_text_color="Custom", text_color=ACTIVO)
            boton = MDButton(w_icono, w_texto, style="text", size_hint=(None, None),
                             on_release=lambda x, d=destino: setattr(self.sm, "current", d))
            zona = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")
            zona.add_widget(boton)
            self.add_widget(zona)
            self.items[destino] = (w_icono, w_texto)

        self.sm.bind(current=self.marcar)  # se actualiza sola al cambiar de pantalla
        self.marcar()

    def marcar(self, *args):
            app = App.get_running_app()
            hay_sesion = getattr(app, "usuario_actual", None) is not None
    
            # Sin sesión, la barra se oculta y no se puede tocar
            self.opacity = 1 if hay_sesion else 0
            self.disabled = not hay_sesion
            self.height = dp(70) if hay_sesion else 0
    
            activa = PESTANA_DE.get(self.sm.current)
            for destino, (w_icono, w_texto) in self.items.items():
                color = ACTIVO if destino == activa else INACTIVO
                w_icono.text_color = color
                w_texto.text_color = color