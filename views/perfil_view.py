from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
from views.calendario import AZUL
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, MDDialogSupportingText
from kivy.utils import get_color_from_hex
from kivymd.uix.anchorlayout import MDAnchorLayout
from services.persistencia_sesion import cerrar_sesion
from views.componentes import (banner, icono_grande, tarjeta, fila_dato, indicador, boton_contorno, boton_enlace, mostrar_dialogo)
from views.estilos import AZUL, GUINDA, GRIS_TEXTO, BLANCO


AZUL = get_color_from_hex("#01568e")
GUINDA = get_color_from_hex("#7B1D35")
ESTADOS_PERFIL = [
    ("Pendiente", "Pendientes", "clock-outline", AZUL),
    ("Confirmada", "Confirmadas", "check-circle-outline", AZUL),
    ("Cancelada", "Canceladas", "close-circle-outline", GUINDA),
    ("Finalizada", "Finalizadas", "flag-checkered", GRIS_TEXTO)
]

def label(texto="", **kwargs):
    return MDLabel(text=texto, adaptive_height=True, **kwargs)

class PerfilView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Labels que se rellenan en on_enter con los datos del usuario actual
        self.lbl_nombre = label(halign="center", bold=True, font_style="Title", role="large")
        self.lbl_correo = label(halign="center", theme_text_color="Custom", text_color=GRIS_TEXTO)
        self.lbl_rol = label()
        self.lbl_registro = label()
        self.lbl_total = label(font_style="Label", role="medium",
                               theme_text_color="Custom", text_color=GRIS_TEXTO)
        self.lbl_estados = {}

        # Cabecera: avatar, nombre y correo
        cabecera = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=dp(4))
        cabecera.add_widget(icono_grande("account-circle", tamano=80))
        cabecera.add_widget(self.lbl_nombre)
        cabecera.add_widget(self.lbl_correo)

        # Resumen de reservas: título con el total y una franja con cada estado
        titulo_resumen = MDBoxLayout(adaptive_height=True)
        titulo_resumen.add_widget(label("Mis reservas", bold=True))
        self.lbl_total.halign = "right"
        titulo_resumen.add_widget(self.lbl_total)

        franja = MDBoxLayout(adaptive_height=True, padding=(dp(4), dp(12)),
                             md_bg_color=BLANCO, radius=[dp(12)])
        for estado, texto, icono, color in ESTADOS_PERFIL:
            numero = label("0", halign="center", bold=True, font_style="Title", role="large")
            self.lbl_estados[estado] = numero
            franja.add_widget(indicador(icono, color, numero, texto))

        resumen = tarjeta(titulo_resumen, franja,
                          boton_enlace("Ver mis reservas", self.ir_a_reservas))

        # Datos de la cuenta
        cuenta = tarjeta(
            label("Datos de la cuenta", bold=True),
            fila_dato("shield-account-outline", "Rol", self.lbl_rol),
            fila_dato("calendar-clock-outline", "Miembro desde", self.lbl_registro),
        )

        contenido = MDBoxLayout(orientation="vertical", adaptive_height=True,
                                padding=dp(20), spacing=dp(16))
        contenido.add_widget(cabecera)
        contenido.add_widget(resumen)
        contenido.add_widget(cuenta)
        contenido.add_widget(boton_contorno("CERRAR SESIÓN", GUINDA, self.preguntar_cerrar_sesion,
                                            icono="logout"))

        scroll = MDScrollView()
        scroll.add_widget(contenido)

        principal = MDBoxLayout(orientation="vertical")
        principal.add_widget(banner("MI PERFIL"))
        principal.add_widget(scroll)
        self.add_widget(principal)
        
    def on_enter(self, *args):
        self.actualizar()
        
    def actualizar(self):
        app = MDApp.get_running_app()

        usuario = app.usuario_actual

        if usuario is None:
            self.manager.current = "login"
            return

        resumen = app.gestor.resumen_de(usuario)

        self.lbl_nombre.text = usuario.nombre
        self.lbl_correo.text = usuario.correo
        self.lbl_rol.text = usuario.rol
        self.lbl_registro.text = usuario.fecha_registro

        self.lbl_total.text = f"{resumen['total']} en total"

        for estado, numero in self.lbl_estados.items():
            numero.text = str(resumen[estado])
            
    def ir_a_reservas(self, *args):
        self.manager.current = "reservas"
        
    def preguntar_cerrar_sesion(self, *args):
        mostrar_dialogo(
            "¿Cerrar sesión?",
            "Tendrás que volver a ingresar tu correo y contraseña.",
            [
                ("CANCELAR", None),
                ("CERRAR SESIÓN", self.cerrar_sesion)
            ]
        )
        
    def cerrar_sesion(self):
        app = MDApp.get_running_app()
    
        cerrar_sesion()
    
        app.usuario_actual = None
    
        self.manager.current = "login"