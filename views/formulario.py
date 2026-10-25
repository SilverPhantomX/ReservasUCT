from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, MDDialogSupportingText
from kivymd.uix.button import MDButtonIcon, MDButtonText
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.anchorlayout import MDAnchorLayout
from models.reserva_model import (SALAS, DIAS, HORAS, MOTIVOS, MAX_ACOMPANANTES)
from kivy.utils import get_color_from_hex
from models.reserva_model import Reserva

AZUL = get_color_from_hex("#01568e")
GUINDA = get_color_from_hex("#7B1D35")

class FormularioScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical")
        caja = MDBoxLayout(orientation="vertical")
        caja.add_widget(self.crear_titulo("FORMULARIO DE RESERVA"))
        
        formulario = MDBoxLayout(orientation="vertical", adaptive_height=True, padding=dp(20), spacing=dp(14))
        self.campo_nombre = MDTextField(MDTextFieldHintText(text="Nombre completo"), mode="outlined")
        self.campo_correo = MDTextField(MDTextFieldHintText(text="Correo (ej: jperez@uct.cl)"), mode="outlined")
        formulario.add_widget(self.campo_nombre)
        formulario.add_widget(self.campo_correo)
        
        formulario.add_widget(self.crear_boton_menu("sala", "Elegir sala", SALAS))
        formulario.add_widget(self.crear_boton_menu("dia", "Elegir día", DIAS))
        formulario.add_widget(self.crear_boton_menu("hora", "Elegir hora", HORAS))
        formulario.add_widget(self.crear_boton_menu("motivo", "Motivo de la reserva", MOTIVOS))
        formulario.add_widget(self.crear_boton_menu("acompanantes", "Acompañantes: 0", list(range(MAX_ACOMPANANTES + 1))))
        
        formulario.add_widget(self.crear_boton("CONFIRMAR RESERVA", GUINDA, self.confirmar_reserva))
        formulario.add_widget(self.crear_boton("VER MIS RESERVAS", AZUL, self.ir_a_reservas))
        
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
        scroll.add_widget(formulario)
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

    def confirmar_reserva(self, *args):
        app = MDApp.get_running_app()
        self.reserva_nueva = Reserva(
            self.campo_nombre.text, self.campo_correo.text, app.seleccion["sala"],
            app.seleccion["dia"], app.seleccion["hora"], app.seleccion["motivo"], app.seleccion["acompanantes"]
        )
        errores = self.reserva_nueva.validar()
        if errores:
            self.mostrar_dialogo("Revisa el formulario","\n".join(errores),[("ENTENDIDO",self.cerrar_dialog)])
        else:
            self.mostrar_dialogo("¿Confirmar reserva?", self.reserva_nueva.resumen(),
                                [("CANCELAR", self.cerrar_dialog), ("CONFIRMAR",self.guardar_reserva)])

    def guardar_reserva(self, *args):
        self.dialog.dismiss()
        app = MDApp.get_running_app()
        errores = app.gestor.agregar(self.reserva_nueva)
        if errores:
            self.mostrar_dialogo("No se pudo reservar", "\n".join(errores), [( "ENTENDIDO", self.cerrar_dialog)])
        else:
            self.ir_a_reservas()

    def ir_a_reservas(self, *args):    
        self.manager.current = "reservas"