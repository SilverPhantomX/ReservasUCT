from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButtonText
from kivy.metrics import dp
from kivymd.uix.scrollview import MDScrollView
from views.componentes import (
    banner,
    tarjeta,
    fila_icono,
    chip,
    estado_vacio,
    boton_contorno,
    mostrar_dialogo
)

from views.estilos import (
    AZUL,
    AZUL_SUAVE,
    GRIS_SUAVE,
    GRIS_TEXTO,
    GUINDA,
    VERDE
)


COLOR_ESTADO = {
    "Pendiente": AZUL,
    "Confirmada": VERDE,
    "Cancelada": GUINDA,
    "Finalizada": GRIS_TEXTO
}

class ReservaScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        caja = MDBoxLayout(orientation="vertical")
        caja.add_widget(banner("MIS RESERVAS"))
        
        self.lista = MDBoxLayout(orientation="vertical", adaptive_height=True, padding=dp(20), spacing=dp(10))
        scroll = MDScrollView()
        scroll.add_widget(self.lista)
        
        volver = MDBoxLayout(adaptive_height=True, padding=dp(20))
        volver.add_widget(self.crear_boton("VOLVER AL FORMULARIO", AZUL, self.ir_a_formulario))
        
        caja.add_widget(scroll)
        caja.add_widget(volver)
        self.add_widget(caja)
        
    def on_enter(self, *args):
        app = MDApp.get_running_app()
    
        app.gestor.actualizar_estados()
        self.actualizar_lista()
    


    def crear_boton(self, texto, color, accion):
        return MDButton(
            MDButtonText(text=texto, theme_text_color="Custom",  text_color=(1, 1, 1, 1), pos_hint={"center_x": 0.5,"center_y": 0.5}),
            style="filled", theme_bg_color="Custom", md_bg_color=color, theme_width="Custom", size_hint_x=1, on_release=accion
        )
        
    def actualizar_lista(self):
        app = MDApp.get_running_app()
    
        self.lista.clear_widgets()
    
        activas, historial = app.gestor.separar_reservas(
            app.usuario_actual
        )
    
        if not activas and not historial:
            self.lista.add_widget(
                estado_vacio(
                    "calendar-blank-outline",
                    "Aún no tienes reservas",
                    "Crea una nueva reserva desde el calendario."
                )
            )
            return
    
        # Próximas reservas
        self.lista.add_widget(
            self.titulo_seccion(
                f"Próximas ({len(activas)})"
            )
        )
    
        if not activas:
            self.lista.add_widget(
                MDLabel(
                    text="No tienes reservas próximas.",
                    adaptive_height=True,
                    theme_text_color="Custom",
                    text_color=GRIS_TEXTO
                )
            )
    
        for reserva in activas:
            self.lista.add_widget(
                self.tarjeta_reserva(reserva)
            )
    
        # Historial
        if historial:
            self.lista.add_widget(
                self.titulo_seccion(
                    f"Historial ({len(historial)})"
                )
            )
    
            for reserva in historial:
                self.lista.add_widget(
                    self.tarjeta_reserva(reserva)
                )
    
              

    def preguntar_anular(self, reserva):
        self.reserva_a_anular = reserva
        mostrar_dialogo("¿Anular reserva?", reserva.resumen(), [("NO", None), ("SÍ, ANULAR",self.anular_reserva)])

    def anular_reserva(self, *args):
        app = MDApp.get_running_app()                   
        app.gestor.anular(self.reserva_a_anular)
        self.actualizar_lista()                  

    def ir_a_formulario(self, *args):    
        self.manager.current = "formulario"
        
    def titulo_seccion(self, texto):
        return MDLabel(
            text=texto,
            bold=True,
            adaptive_height=True,
            theme_text_color="Custom",
            text_color=AZUL
        )
        
    def tarjeta_reserva(self, reserva):
        activa = reserva.estado in ["Pendiente", "Confirmada"]

        cabecera = MDBoxLayout(
            adaptive_height=True,
            spacing=dp(8)
        )

        cabecera.add_widget(
            MDLabel(
                text=reserva.sala,
                bold=True,
                adaptive_height=True
            )
        )

        cabecera.add_widget(
            chip(
                reserva.estado,
                COLOR_ESTADO.get(
                    reserva.estado,
                    GRIS_TEXTO
                )
            )
        )

        partes = [
            cabecera,

            fila_icono(
                "calendar-outline",
                reserva.dia
            ),

            fila_icono(
                "clock-outline",
                f"{reserva.hora_inicio} - {reserva.hora_termino}"
            ),

            fila_icono(
                "music-note-outline",
                reserva.motivo
            )
        ]

        if activa:
            partes.append(
                fila_icono(
                    "key-outline",
                    f"Código de acceso: {reserva.codigo_acceso}"
                )
            )

            partes.append(
                boton_contorno(
                    "ANULAR",
                    GUINDA,
                    lambda x, r=reserva: self.preguntar_anular(r),
                    icono="close"
                )
            )

        return tarjeta(
            *partes,
            color=AZUL_SUAVE if activa else GRIS_SUAVE
        )