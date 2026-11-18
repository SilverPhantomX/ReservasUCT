from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.dialog import (MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, MDDialogSupportingText)
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from models.usuario_model import Usuario

AZUL = get_color_from_hex("#01568e")
GUINDA = get_color_from_hex("#7B1D35")

class RegistroScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        principal = MDBoxLayout(orientation="vertical")

        # Banner
        banner = MDBoxLayout(
            size_hint_y=None,
            height=dp(70),
            md_bg_color=AZUL
        )

        titulo = MDLabel(
            text="ReservasUCT",
            halign="center",
            bold=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )

        banner.add_widget(titulo)

        # Scroll
        scroll = MDScrollView()

        # Contenido
        contenido = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            size_hint_x=0.9,
            spacing=dp(15),
            padding=dp(20)
        )

        # Icono
        contenido.add_widget(
            MDButtonIcon(
                icon="account-plus",
                theme_text_color="Custom",
                text_color=(0.25, 0.25, 0.25, 1),
                theme_font_size="Custom",
                font_size=dp(70),
                pos_hint={"center_x": 0.5}
            )
        )

        # Nombre
        self.campo_nombre = MDTextField(
            MDTextFieldHintText(text="Nombre completo"),
            mode="outlined"
        )

        # Correo
        self.campo_correo = MDTextField(
            MDTextFieldHintText(text="Correo"),
            mode="outlined"
        )

        # Contraseña
        self.campo_contrasena = MDTextField(
            MDTextFieldHintText(text="Contraseña"),
            mode="outlined"
        )

        contenido.add_widget(self.campo_nombre)
        contenido.add_widget(self.campo_correo)
        contenido.add_widget(self.campo_contrasena)

        # Centrar contenido
        contenedor_centro = MDAnchorLayout(
            anchor_x="center",
            anchor_y="center"
        )

        contenedor_centro.add_widget(contenido)
        scroll.add_widget(contenedor_centro)

        # Footer
        navegacion = MDBoxLayout(
            size_hint_y=None,
            height=dp(70),
            md_bg_color=AZUL
        )

        zona_login = MDAnchorLayout(
            size_hint_x=1,
            anchor_x="center",
            anchor_y="center"
        )

        zona_registro = MDAnchorLayout(
            size_hint_x=1,
            anchor_x="center",
            anchor_y="center"
        )

        btn_login = MDButton(
            MDButtonIcon(
                icon="login",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            ),
            MDButtonText(
                text="Iniciar sesión",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            ),
            style="text",
            size_hint=(None, None),
            on_release=lambda x: setattr(
                self.manager,
                "current",
                "login"
            )
        )

        btn_registrarse = MDButton(
            MDButtonIcon(
                icon="account-plus",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            ),
            MDButtonText(
                text="Registrarse",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            ),
            style="text",
            size_hint=(None, None),
            on_release=self.crear_cuenta
        )

        zona_login.add_widget(btn_login)
        zona_registro.add_widget(btn_registrarse)

        navegacion.add_widget(zona_login)
        navegacion.add_widget(zona_registro)

        principal.add_widget(banner)
        principal.add_widget(scroll)
        principal.add_widget(navegacion)

        self.add_widget(principal)
        
    def crear_cuenta(self, *args):
        app = MDApp.get_running_app()

        usuario = Usuario(
            self.campo_nombre.text,
            self.campo_correo.text,
            self.campo_contrasena.text,
            "Estudiante"
        )

        errores = app.gestor_usuarios.agregar(usuario)

        if errores:
            self.mostrar_dialogo(
                "No se pudo crear la cuenta",
                "\n".join(errores)
            )
            return

        self.mostrar_dialogo(
            "Cuenta creada",
            "Usuario registrado correctamente."
        )

        self.campo_nombre.text = ""
        self.campo_correo.text = ""
        self.campo_contrasena.text = ""
        
    def mostrar_dialogo(self, titulo, texto):
        contenedor = MDDialogButtonContainer()

        contenedor.add_widget(
            MDButton(
                MDButtonText(text="ENTENDIDO"),
                style="text",
                on_release=self.cerrar_dialogo
            )
        )

        self.dialog = MDDialog(
            MDDialogHeadlineText(text=titulo),
            MDDialogSupportingText(text=texto),
            contenedor
        )

        self.dialog.open()


    def cerrar_dialogo(self, *args):
        self.dialog.dismiss()