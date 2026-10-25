from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, MDDialogSupportingText
from kivymd.uix.button import MDButtonIcon, MDButtonText
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.anchorlayout import MDAnchorLayout

AZUL = get_color_from_hex("#01568e")
GUINDA = get_color_from_hex("#7B1D35")

class ReservaScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical")
        
        caja = MDBoxLayout(orientation="vertical")
        caja.add_widget(self.crear_titulo("MIS RESERVAS"))
        
        self.lista = MDBoxLayout(orientation="vertical", adaptive_height=True, padding=dp(20), spacing=dp(10))
        scroll = MDScrollView()
        scroll.add_widget(self.lista)
        
        volver = MDBoxLayout(adaptive_height=True, padding=dp(20))
        volver.add_widget(self.crear_boton("VOLVER AL FORMULARIO", AZUL, self.ir_a_formulario))
        
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
            on_release=lambda x: setattr(self.manager, 'current', 'perfil'),)
        
        zona_inicio.add_widget(btn_inicio)
        zona_reservas.add_widget(btn_reservas)
        zona_perfil.add_widget(btn_perfil)
        navegacion.add_widget(zona_inicio)
        navegacion.add_widget(zona_reservas)
        navegacion.add_widget(zona_perfil)
        
        caja.add_widget(scroll)
        caja.add_widget(volver)
        caja.add_widget(navegacion)
        self.add_widget(caja)
        
    def on_enter(self, *args):
        self.actualizar_lista()
    
    def crear_titulo(self, texto):
        barra = MDBoxLayout(size_hint_y=None, height=dp(70), md_bg_color=AZUL)
        barra.add_widget( MDLabel(text=texto, halign="center", bold=True, theme_text_color="Custom", text_color=(1, 1, 1, 1)))
        return barra

    def crear_boton(self, texto, color, accion):
        return MDButton(
            MDButtonText(text=texto, theme_text_color="Custom",  text_color=(1, 1, 1, 1), pos_hint={"center_x": 0.5,"center_y": 0.5}),
            style="filled", theme_bg_color="Custom", md_bg_color=color, theme_width="Custom", size_hint_x=1, on_release=accion
        )

    def actualizar_lista(self):
        app = MDApp.get_running_app()
        self.lista.clear_widgets()
        if not app.gestor.reservas:        
            self.lista.add_widget(MDLabel(text="Aún no tienes reservas.", adaptive_height=True))
            return
        for reserva in app.gestor.reservas:        
            self.lista.add_widget(MDLabel(text=reserva.resumen(), adaptive_height=True))
            self.lista.add_widget(self.crear_boton("ANULAR", GUINDA, lambda x, r=reserva: self.preguntar_anular(r)))
            
    def mostrar_dialogo(self, titulo, texto, botones):
        contenedor = MDDialogButtonContainer(spacing="8dp")
        for texto_boton, funcion in botones:
            contenedor.add_widget(MDButton(MDButtonText(text=texto_boton), style="text", on_release=funcion))
        self.dialog = MDDialog(MDDialogHeadlineText(text=titulo), MDDialogSupportingText(text=texto), contenedor)
        self.dialog.open()

    def cerrar_dialog(self, *args):
        self.dialog.dismiss()

    def preguntar_anular(self, reserva):
        self.reserva_a_anular = reserva
        self.mostrar_dialogo("¿Anular reserva?", reserva.resumen(), [("NO",self.cerrar_dialog), ("SÍ, ANULAR",self.anular_reserva)])

    def anular_reserva(self, *args):
        app = MDApp.get_running_app()
        self.dialog.dismiss()                    
        app.gestor.anular(self.reserva_a_anular)
        self.actualizar_lista()                  

    def ir_a_formulario(self, *args):    
        self.manager.current = "formulario"