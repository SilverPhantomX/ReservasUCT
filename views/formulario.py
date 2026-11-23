from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButtonText
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from models.reserva_model import (SALAS, HORAS, MOTIVOS, MAX_ACOMPANANTES)
from kivy.utils import get_color_from_hex
from models.reserva_model import Reserva
from services.analytics_service import registrar_evento
from services.remote_config import obtener_texto_confirmacion
from views.componentes import mostrar_dialogo

AZUL = get_color_from_hex("#01568e")
GUINDA = get_color_from_hex("#7B1D35")

class FormularioScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        caja = MDBoxLayout(orientation="vertical")
        caja.add_widget(self.crear_titulo("FORMULARIO DE RESERVA"))
        
        formulario = MDBoxLayout(orientation="vertical", adaptive_height=True, padding=dp(20), spacing=dp(14))
        self.campo_nombre = MDTextField(MDTextFieldHintText(text="Nombre completo"), mode="outlined")
        self.campo_correo = MDTextField(MDTextFieldHintText(text="Correo (ej: jperez@uct.cl)"), mode="outlined")
        formulario.add_widget(self.campo_nombre)
        formulario.add_widget(self.campo_correo)
        
        formulario.add_widget(self.crear_boton_menu("sala", "Elegir sala", SALAS))
        self.texto_fecha = MDButtonText(
            text="Fecha no seleccionada",
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.5
            }
        )
    
        self.boton_fecha = MDButton(
            self.texto_fecha,
            style="outlined",
            theme_width="Custom",
            size_hint_x=1,
            on_release = self.ir_a_calendario
        )

        formulario.add_widget(self.boton_fecha)
        formulario.add_widget(self.crear_boton_menu("hora_inicio", "Elegir hora de inicio", HORAS))
        formulario.add_widget(self.crear_boton_menu("hora_termino", "Elegir hora de termino", HORAS))
        formulario.add_widget(self.crear_boton_menu("motivo", "Motivo de la reserva", MOTIVOS))
        formulario.add_widget(self.crear_boton_menu("acompanantes", "Acompañantes: 0", list(range(MAX_ACOMPANANTES + 1))))
        
        formulario.add_widget(self.crear_boton(obtener_texto_confirmacion(), GUINDA,self.confirmar_reserva))
        formulario.add_widget(self.crear_boton("VER MIS RESERVAS", AZUL, self.ir_a_reservas))
        

        scroll = MDScrollView()
        scroll.add_widget(formulario)
        caja.add_widget(scroll)
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
        app = MDApp.get_running_app()

        # Si quiere elegir una hora, primero debe existir fecha y sala
        if campo in ["hora_inicio", "hora_termino"]:

            if app.seleccion["dia"] is None:
                mostrar_dialogo(
                    "Fecha requerida",
                    "Primero debes seleccionar una fecha."
                )
                return

            if app.seleccion["sala"] is None:
                mostrar_dialogo(
                    "Sala requerida",
                    "Primero debes seleccionar una sala."
                )
                return

            dia = app.seleccion["dia"]
            sala = app.seleccion["sala"]

            # Solo muestra horas de inicio libres
            if campo == "hora_inicio":
                opciones = app.gestor.obtener_horas_disponibles(
                    dia,
                    sala
                )

                if not opciones:
                    mostrar_dialogo(
                        "Sin disponibilidad",
                        "No quedan horas disponibles para esta sala."
                    )
                    return

            # La hora de término depende de la hora de inicio self.crear_boton
            elif campo == "hora_termino":
            
                if app.seleccion["hora_inicio"] is None:
                    mostrar_dialogo(
                        "Hora de inicio requerida",
                        "Primero debes elegir la hora de inicio."
                    )
                    return
    
                opciones = app.gestor.obtener_horas_termino(
                    dia,
                    sala,
                    app.seleccion["hora_inicio"]
                )
    
        items = [
            {
                "text": str(opcion),
                "on_release": lambda opcion=opcion:
                    self.elegir(campo, opcion)
            }
            for opcion in opciones
        ]
    
        self.menu = MDDropdownMenu(
            caller=boton,
            items=items
        )
    
        self.menu.open()

    def ir_a_calendario(self, *args):
            # No se limpia el formulario, para conservar lo que ya escribiste al volver
            self.manager.current = "calendario"
    
    def elegir(self, campo, opcion):
        
        app = MDApp.get_running_app()
        app.seleccion[campo] = opcion
        
        if campo == "sala":
            app.seleccion["hora_inicio"] = None
            app.seleccion["hora_termino"] = None
            
            app.textos_botones["hora_inicio"].text = "Elegir hora de inicio"
            app.textos_botones["hora_termino"].text = "Elegir hora de termino"
        
        if campo == "acompanantes":
            app.textos_botones[campo].text = f"Acompañantes: {opcion}"
        else:        
            app.textos_botones[campo].text = str(opcion)
        self.menu.dismiss()
        if campo == "hora_inicio":
            app.seleccion["hora_termino"] = None
            app.textos_botones["hora_termino"].text = "Elegir hora de termino"
            

    def confirmar_reserva(self, *args):
        app = MDApp.get_running_app()
        self.reserva_nueva = Reserva(
            self.campo_nombre.text, self.campo_correo.text, app.seleccion["sala"],
            app.seleccion["dia"], app.seleccion["hora_inicio"], app.seleccion["hora_termino"], app.seleccion["motivo"], app.seleccion["acompanantes"],
            None, "Pendiente", app.usuario_actual.correo
        )
        errores = self.reserva_nueva.validar()
        if errores:
            mostrar_dialogo("Revisa el formulario","\n".join(errores),[("ENTENDIDO",self.cerrar_dialog)])
        else:
            mostrar_dialogo("¿Confirmar reserva?", self.reserva_nueva.resumen(),
                                [("CANCELAR", self.cerrar_dialog), ("CONFIRMAR",self.guardar_reserva)])

    def guardar_reserva(self, *args):
        self.dialog.dismiss()
        app = MDApp.get_running_app()
        errores = app.gestor.agregar(self.reserva_nueva)
        if errores:
            mostrar_dialogo("No se pudo reservar", "\n".join(errores), [( "ENTENDIDO", self.cerrar_dialog)])
        else:
            registrar_evento("reserva_confirmada",
                    {
                    "sala": self.reserva_nueva.sala,
                    "dia": self.reserva_nueva.dia,
                    "hora_inicio": self.reserva_nueva.hora_inicio,
                    "hora_termino": self.reserva_nueva.hora_termino
                    })

            self.limpiar_formulario()
            self.ir_a_reservas()

    def ir_a_reservas(self, *args):    
        self.manager.current = "reservas"
        
        
    def recibir_fecha(self, fecha):

        # Guardamos también la fecha en la selección de la app
        app = MDApp.get_running_app()
        app.seleccion["dia"] = fecha

        # La mostramos en el formulario
        self.texto_fecha.text = f"Fecha: {fecha}"
        
    def limpiar_formulario(self):
        app = MDApp.get_running_app()

        # Limpiar campos de texto
        self.campo_nombre.text = ""
        self.campo_correo.text = ""

        # Reiniciar selección
        app.seleccion = {
                "sala": None,
                "dia": None,
                "hora_inicio": None,
                "hora_termino": None,
                "motivo": None,
                "acompanantes": 0
        }

        app.textos_botones["sala"].text = "Elegir sala"
        app.textos_botones["hora_inicio"].text = "Elegir hora de inicio"
        app.textos_botones["hora_termino"].text = "Elegir hora de termino"
        app.textos_botones["motivo"].text = "Motivo de la reserva"
        app.textos_botones["acompanantes"].text = "Acompañantes: 0"
        

        # Reiniciar fecha
        self.texto_fecha.text = "Fecha no seleccionada"
        