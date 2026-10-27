from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
from views.calendario import AZUL
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, MDDialogSupportingText
from kivy.utils import get_color_from_hex

AZUL = get_color_from_hex("#01568e")
GUINDA = get_color_from_hex("#7B1D35")

class PerfilView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(
            MDLabel(
                text="Vista de Perfil en construcción\n :p",
                halign="center"
            )
        )
        caja = MDBoxLayout(orientation="vertical")    
            
        navegacion = MDBoxLayout(size_hint_y=None, height=dp(70), md_bg_color=AZUL)
        zona_inicio = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")
        zona_reservas = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")
        zona_perfil = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")
        
        btn_inicio = MDButton(
            MDButtonIcon(icon="home", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
            MDButtonText(text="Inicio", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
            style="text", size_hint=(None, None),
            on_release=lambda x: setattr(self.manager, 'current', 'calendario')
        )
        btn_reservas = MDButton(
            MDButtonIcon(icon="calendar", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
            MDButtonText(text="Reservas", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
            style="text", size_hint=(None, None),
            on_release=lambda x: setattr(self.manager, 'current', 'reservas')
        )
        # Botón Perfil
        btn_perfil = MDButton(
            MDButtonIcon(icon="account", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
            MDButtonText(text="Perfil",theme_text_color="Custom",text_color=(1, 1, 1, 1)),
            style="text", size_hint=(None, None),
            on_release=lambda x: setattr(self.manager, 'current', 'perfil'))
        
        zona_inicio.add_widget(btn_inicio)
        zona_reservas.add_widget(btn_reservas)
        zona_perfil.add_widget(btn_perfil)
        navegacion.add_widget(zona_inicio)
        navegacion.add_widget(zona_reservas)
        navegacion.add_widget(zona_perfil)

        scroll = MDScrollView()
        caja.add_widget(scroll)
        caja.add_widget(navegacion)
        self.add_widget(caja)

    def crear_titulo(self, texto):
        barra = MDBoxLayout(size_hint_y=None, height=dp(70), md_bg_color=AZUL)
        barra.add_widget(MDLabel(text=texto, halign="center", bold=True, theme_text_color="Custom", text_color=(1, 1, 1, 1)))
        return barra

    def crear_boton(self, texto, color, accion):
        return MDButton(
            MDButtonText(text=texto, theme_text_color="Custom", text_color=(1, 1, 1, 1), pos_hint={"center_x": 0.5,"center_y": 0.5}),
            style="filled", theme_bg_color="Custom", md_bg_color=color, theme_width="Custom", size_hint_x=1, on_release=accion
        )

    def crear_boton_menu(self, campo, texto, opciones):
        texto_boton = MDButtonText(text=texto, pos_hint={"center_x": 0.5,"center_y": 0.5})
        MDApp.get_running_app().textos_botones[campo] = texto_boton
        boton = MDButton(texto_boton, style="outlined", theme_width="Custom", size_hint_x=1)
        boton.bind(on_release=lambda x: self.abrir_menu(x, campo, opciones))
        return boton

    def abrir_menu(self, boton, campo, opciones):
        items = [{"text": str(opcion), "on_release": lambda opcion=opcion: self.elegir(campo, opcion)} for opcion in opciones]
        self.menu = MDDropdownMenu(caller=boton, items=items)
        self.menu.open()

    def elegir(self, campo, opcion):
        app = MDApp.get_running_app()
        app.seleccion[campo] = opcion
        if campo == "acompanantes":
            app.textos_botones[campo].text = f"Acompañantes: {opcion}"
        else:        
            app.textos_botones[campo].text = str(opcion)
        self.menu.dismiss()
            
    def mostrar_dialogo(self, titulo, texto, botones):
        contenedor = MDDialogButtonContainer(spacing="8dp")
        for texto_boton, funcion in botones:
            contenedor.add_widget(MDButton(MDButtonText(text=texto_boton), style="text", on_release=funcion))
        self.dialog = MDDialog(MDDialogHeadlineText(text=titulo), MDDialogSupportingText(text=texto), contenedor)
        self.dialog.open()

    def cerrar_dialog(self, *args):
        self.dialog.dismiss()