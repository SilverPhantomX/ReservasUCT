from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.label import MDLabel

AZUL = get_color_from_hex("#01568e")
BLANCO = (1, 1, 1, 1)
ACTIVO = (1, 1, 1, 0.20)  # fondo translúcido del ítem seleccionado


class Sidebar(MDBoxLayout):
    """Barra lateral izquierda. Cambia la pantalla del ScreenManager que recibe.

    expandida=False -> solo íconos (72dp), deja más espacio a la grilla.
    expandida=True  -> íconos + texto (200dp).
    """

    def __init__(self, screen_manager, items, expandida=False, **kwargs):
        """items: lista de (icono, texto, nombre_de_pantalla)."""
        super().__init__(orientation="vertical", size_hint_x=None, width=dp(200 if expandida else 72),
                         md_bg_color=AZUL, padding=dp(8), spacing=dp(4), **kwargs)
        self.sm = screen_manager
        self.cajas = {}

        if expandida:
            self.add_widget(MDLabel(text="Panel admin", bold=True, halign="center", size_hint_y=None,
                                    height=dp(56), theme_text_color="Custom", text_color=BLANCO))
        else:
            self.add_widget(MDBoxLayout(size_hint_y=None, height=dp(56)))  # alinea con el banner

        for icono, texto, nombre in items:
            caja = MDBoxLayout(size_hint_y=None, height=dp(48), radius=[dp(8)] * 4, md_bg_color=(0, 0, 0, 0))
            hijos = [MDButtonIcon(icon=icono, theme_text_color="Custom", text_color=BLANCO)]
            if expandida:
                hijos.append(MDButtonText(text=texto, theme_text_color="Custom", text_color=BLANCO))
            caja.add_widget(MDButton(*hijos, style="text", theme_width="Custom", size_hint_x=1,
                                     on_release=lambda x, n=nombre: self.ir(n)))
            self.cajas[nombre] = caja
            self.add_widget(caja)

        self.add_widget(MDBoxLayout())  # relleno: empuja todo hacia arriba (aquí irá "Cerrar sesión")
        self.marcar(self.sm.current)

    def ir(self, nombre):
        self.sm.current = nombre
        self.marcar(nombre)

    def marcar(self, nombre):
        for n, caja in self.cajas.items():
            caja.md_bg_color = ACTIVO if n == nombre else (0, 0, 0, 0)