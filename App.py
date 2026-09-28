from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.anchorlayout import MDAnchorLayout
import calendar
from datetime import datetime
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import (MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer)
from modelos import (Reserva, GestorReservas, SALAS, DIAS, HORAS, MOTIVOS, MAX_ACOMPANANTES)


Window.size = (400, 600)

AZUL = get_color_from_hex("#01568e")
GUINDA = get_color_from_hex("#7B1D35")


class MiApp(MDApp):

    def build(self):
        
        Window.clearcolor = (1, 1, 1, 1)
        
        # Gestor que almacenará las reservas
        self.gestor = GestorReservas()

        # Opciones seleccionadas en el formulario
        self.seleccion = {
            "sala": None,
            "dia": None,
            "hora": None,
            "motivo": None,
            "acompanantes": 0
        }

        # Guarda los textos de los botones desplegables
        self.textos_botones = {}
        
        
        self.pantallas = MDScreenManager()
        # Pantalla donde estará el calendario
        pantalla_calendario = MDScreen(name="calendario")
        
        # --------------------------------------------------
        # Pantalla de reserva temporal
        # --------------------------------------------------
        
        principal = MDBoxLayout(orientation="vertical") #layout de la app
        
        #banner de la app
        banner = MDBoxLayout(size_hint_y=None, height=dp(70), md_bg_color=AZUL)
        
        #titulos o foto nose
        titulo = MDLabel(
            text="Academia de Artes Musicales",
            halign="center",
            bold=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1))
        banner.add_widget(titulo)
        
        # --------------------------------------------------
        # Barra para seleccionar el mes del calendario seleccionar_fecha()
        # --------------------------------------------------
        
        # Guardamos el mes y año actuales
        hoy = datetime.now()

        self.mes_actual = hoy.month
        self.anio_actual = hoy.year

        selector_mes = MDBoxLayout(
            size_hint_y=None,
            height=dp(55),
            padding=dp(10)
        )

        # Flecha para ir al mes anterior
        btn_mes_anterior = MDButton(
            MDButtonIcon(
                icon="chevron-left",
                theme_text_color="Custom",
                text_color=AZUL
            ),
            style="text",
            size_hint=(None, None)
        )

        # Nombre del mes actual
        self.lbl_mes = MDLabel(
            text="",
            halign="center",
            bold=True,
            theme_text_color="Custom",
            text_color=AZUL
        )

        # Flecha para ir al mes siguiente
        btn_mes_siguiente = MDButton(
            MDButtonIcon(
                icon="chevron-right",
                theme_text_color="Custom",
                text_color=AZUL
            ),
            style="text",
            size_hint=(None, None)
        )
        # Al presionar las flechas cambiamos de mes
        btn_mes_anterior.bind(on_release=self.mes_anterior)
        btn_mes_siguiente.bind(on_release=self.mes_siguiente)

        # Agregamos los elementos a la barra
        selector_mes.add_widget(btn_mes_anterior)
        selector_mes.add_widget(self.lbl_mes)
        selector_mes.add_widget(btn_mes_siguiente)
        
        
        # Zona que permitirá desplazamiento vertical
        scroll = MDScrollView()

        # Contenedor donde irá el formulario
        contenido = MDBoxLayout(
        orientation="vertical",
        adaptive_height=True)
        
        # --------------------------------------------------
        # Calendario
        # --------------------------------------------------

        # Cuadrícula de 7 columnas, una para cada día de la semana
        self.calendario = MDGridLayout(
            cols=7,
            adaptive_height=True,
            spacing=dp(2),
            padding=dp(5)
        )

        # Agregamos el calendario al contenido principal
        contenido.add_widget(self.calendario)

        # Metemos el contenido dentro del scroll
        scroll.add_widget(contenido)
        



        # Panel inferior de navegación tamaño
        navegacion = MDBoxLayout(size_hint_y=None, height=dp(70), md_bg_color=AZUL)
        
        # Contenedores que dividen la navegación en 3 partes iguales
        zona_inicio = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")
        zona_reservas = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")
        zona_perfil = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")
        
        
        btn_inicio = MDButton(
        MDButtonIcon(icon="home", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
        MDButtonText(text="Inicio", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
        style="text",
        size_hint=(None, None),)

        # Botón Reservas etiqueta_dia
        btn_reservas = MDButton(
            MDButtonIcon(icon="calendar", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
            MDButtonText(text="Reservas", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
            style="text",
            size_hint=(None, None),)


        # Botón Perfil
        btn_perfil = MDButton(
            MDButtonIcon(icon="account", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
            MDButtonText(text="Perfil",theme_text_color="Custom",text_color=(1, 1, 1, 1)),
            style="text",
            size_hint=(None, None),)
        
        
        # Agregamos los botones a sus respectivas zonas
        zona_inicio.add_widget(btn_inicio)
        zona_reservas.add_widget(btn_reservas)
        zona_perfil.add_widget(btn_perfil)

        
       
        navegacion.add_widget(zona_inicio)
        navegacion.add_widget(zona_reservas)
        navegacion.add_widget(zona_perfil)

        # --------------------------------------------------
        # Armamos la pantalla del calendario
        # --------------------------------------------------

        principal.add_widget(banner)
        principal.add_widget(selector_mes)
        principal.add_widget(scroll)
        principal.add_widget(navegacion)

        # Metemos todo el layout dentro de la pantalla calendario
        pantalla_calendario.add_widget(principal)

        # Agregamos la pantalla al administrador
        self.pantallas.add_widget(pantalla_calendario)
        
        # Pantalla con el formulario real
        self.pantallas.add_widget(
        self.crear_pantalla_formulario())
         
        # Pantalla donde se mostrarán las reservas
        self.pantallas.add_widget(
        self.crear_pantalla_reservas())
        self.actualizar_mes()

        # Ahora la aplicación devuelve el administrador de pantallas
        return self.pantallas

        # --------------------------------------------------
        # Cambiar al mes anterior
        # --------------------------------------------------
    def mes_anterior(self, *args):

        self.mes_actual -= 1

        # Si retrocedemos desde enero, pasamos a diciembre
        # del año anterior
        if self.mes_actual == 0:
            self.mes_actual = 12
            self.anio_actual -= 1

        self.actualizar_mes()


    # --------------------------------------------------
    # Cambiar al mes siguiente
    # --------------------------------------------------
    def mes_siguiente(self, *args):

        self.mes_actual += 1

        # Si avanzamos desde diciembre, pasamos a enero
        # del año siguiente
        if self.mes_actual == 13:
            self.mes_actual = 1
            self.anio_actual += 1

        self.actualizar_mes()


    # --------------------------------------------------
    # Actualizar el texto del mes
    # --------------------------------------------------
    def actualizar_mes(self):

        meses = [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre"
        ]

        self.lbl_mes.text = f"{meses[self.mes_actual - 1]} {self.anio_actual}"
        self.actualizar_calendario()
        
    # --------------------------------------------------
    # Dibujar el calendario
    # --------------------------------------------------

    def actualizar_calendario(self):

        # Eliminamos los elementos del mes anterior
        self.calendario.clear_widgets()

        # Nombres de los días de la semana
        dias_semana = [
            "Lun",
            "Mar",
            "Mié",
            "Jue",
            "Vie",
            "Sáb",
            "Dom"
        ]
        hoy = datetime.now().date()

        # Agregamos los nombres de los días
        for dia_semana in dias_semana:

            etiqueta = MDLabel(
                text=dia_semana,
                halign="center",
                bold=True,
                size_hint_y=None,
                height=dp(40)
            )

            self.calendario.add_widget(etiqueta)

        # Obtenemos las semanas del mes actual
        semanas = calendar.monthcalendar(
            self.anio_actual,
            self.mes_actual
        )

        # Recorremos cada semana
        for semana in semanas:

            # Recorremos los 7 días de cada semana
            for dia in semana:

                # Si vale 0, ese espacio no pertenece al mes actual
                if dia == 0:

                    espacio = MDLabel(
                        text="",
                        size_hint_y=None,
                        height=dp(45)
                    )

                    self.calendario.add_widget(espacio)

                else:
                    
                    fecha_dia = datetime(self.anio_actual, self.mes_actual, dia).date()

                    # Creamos un botón para cada día real
                    boton_dia = MDButton(
                        MDButtonText(text=str(dia)),
                        style="text",
                        
                        theme_width="Custom",
                        size_hint_x = 1,
                        
                        size_hint_y=None,
                        height=dp(45),
                        disabled=fecha_dia < hoy or fecha_dia.weekday() >= 5
                        
                    )

                    # Guardamos el número de ese día al presionarlo
                    boton_dia.bind(
                        on_release=lambda boton, d=dia: self.seleccionar_fecha(d)
                    )

                    self.calendario.add_widget(boton_dia)


    # --------------------------------------------------
    # Seleccionar una fecha
    # --------------------------------------------------

    def seleccionar_fecha(self, dia):

        # Guardamos la fecha seleccionada
        self.dia_seleccionado = dia
        self.mes_seleccionado = self.mes_actual
        self.anio_seleccionado = self.anio_actual

        # La mostramos en consola por ahora self.calendario
        print(
            f"Fecha seleccionada: "
            f"{self.dia_seleccionado}/"
            f"{self.mes_seleccionado}/"
            f"{self.anio_seleccionado}"
        )
        self.pantallas.current = "formulario"
        
        # --------------------------------------------------
        # Pantalla del formulario de reserva
        # --------------------------------------------------

    def crear_pantalla_formulario(self):
    
        # Creamos la pantalla
        pantalla = MDScreen(
            name="formulario"
        )
        # Contenedor principal
        caja = MDBoxLayout(
            orientation="vertical"
        )
        # Título
        caja.add_widget(
            self.crear_titulo("FORMULARIO DE RESERVA")
        )
        # Contenedor de los campos del formulario
        formulario = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            padding=dp(20),
            spacing=dp(14)
        )
        # Campo nombre
        self.campo_nombre = MDTextField(
            MDTextFieldHintText(
                text="Nombre completo"
            ),
            mode="outlined"
        )
        # Campo correo
        self.campo_correo = MDTextField(
            MDTextFieldHintText(
                text="Correo (ej: jperez@uct.cl)"
            ),
            mode="outlined"
        )
        formulario.add_widget(self.campo_nombre)
        formulario.add_widget(self.campo_correo)
        # Menús desplegables
        formulario.add_widget(
            self.crear_boton_menu(
                "sala",
                "Elegir sala",
                SALAS
            )
        )
        formulario.add_widget(
            self.crear_boton_menu(
                "dia",
                "Elegir día",
                DIAS
            )
        )
        formulario.add_widget(
            self.crear_boton_menu(
                "hora",
                "Elegir hora",
                HORAS
            )
        )
        formulario.add_widget(
            self.crear_boton_menu(
                "motivo",
                "Motivo de la reserva",
                MOTIVOS
            )
        )
        formulario.add_widget(
            self.crear_boton_menu(
                "acompanantes",
                "Acompañantes: 0",
                list(range(MAX_ACOMPANANTES + 1))
            )
        )
        # Botón confirmar
        formulario.add_widget(
            self.crear_boton(
                "CONFIRMAR RESERVA",
                GUINDA,
                self.confirmar_reserva
            )
        )
        # Botón ver reservas
        formulario.add_widget(
            self.crear_boton(
                "VER MIS RESERVAS",
                AZUL,
                self.ir_a_reservas
            )
        )
        
        # Panel inferior de navegación tamaño
        navegacion = MDBoxLayout(size_hint_y=None, height=dp(70), md_bg_color=AZUL)
        
        # Contenedores que dividen la navegación en 3 partes iguales
        zona_inicio = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")
        zona_reservas = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")
        zona_perfil = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")
        
        # Botón inicio etiqueta_dia
        btn_inicio = MDButton(
        MDButtonIcon(icon="home", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
        MDButtonText(text="Inicio", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
        style="text",
        size_hint=(None, None),)
        

        # Botón Reservas etiqueta_dia
        btn_reservas = MDButton(
            MDButtonIcon(icon="calendar", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
            MDButtonText(text="Reservas", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
            style="text",
            size_hint=(None, None),)


        # Botón Perfil
        btn_perfil = MDButton(
            MDButtonIcon(icon="account", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
            MDButtonText(text="Perfil",theme_text_color="Custom",text_color=(1, 1, 1, 1)),
            style="text",
            size_hint=(None, None),)
        
        
        # Agregamos los botones a sus respectivas zonas
        zona_inicio.add_widget(btn_inicio)
        zona_reservas.add_widget(btn_reservas)
        zona_perfil.add_widget(btn_perfil)

        
        
        navegacion.add_widget(zona_inicio)
        navegacion.add_widget(zona_reservas)
        navegacion.add_widget(zona_perfil)
        
        
        # Hacemos el formulario scrolleable
        scroll = MDScrollView()
        scroll.add_widget(formulario)
        caja.add_widget(scroll)
        pantalla.add_widget(caja)
        caja.add_widget(navegacion)
        
        return pantalla
    
    # --------------------------------------------------
    # Pantalla donde se muestran las reservas
    # --------------------------------------------------
    def crear_pantalla_reservas(self):
    
        pantalla = MDScreen(
            name="reservas"
        )
        caja = MDBoxLayout(
            orientation="vertical"
        )
        caja.add_widget(
            self.crear_titulo("MIS RESERVAS")
        )
        # Contenedor de la lista
        self.lista = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            padding=dp(20),
            spacing=dp(10)
        )
        scroll = MDScrollView()
        scroll.add_widget(self.lista)
        caja.add_widget(scroll)
        # Zona del botón volver
        volver = MDBoxLayout(
            adaptive_height=True,
            padding=dp(20)
        )
        volver.add_widget(
            self.crear_boton(
                "VOLVER AL FORMULARIO",
                AZUL,
                self.ir_a_formulario
            )
        )
        
        # Panel inferior de navegación tamaño
        navegacion = MDBoxLayout(size_hint_y=None, height=dp(70), md_bg_color=AZUL)
        
        # Contenedores que dividen la navegación en 3 partes iguales
        zona_inicio = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")
        zona_reservas = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")
        zona_perfil = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")
        
        # Botón inicio etiqueta_dia
        btn_inicio = MDButton(
        MDButtonIcon(icon="home", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
        MDButtonText(text="Inicio", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
        style="text",
        size_hint=(None, None),)

        # Botón Reservas etiqueta_dia
        btn_reservas = MDButton(
            MDButtonIcon(icon="calendar", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
            MDButtonText(text="Reservas", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
            style="text",
            size_hint=(None, None),)


        # Botón Perfil
        btn_perfil = MDButton(
            MDButtonIcon(icon="account", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
            MDButtonText(text="Perfil",theme_text_color="Custom",text_color=(1, 1, 1, 1)),
            style="text",
            size_hint=(None, None),)
        
        
        # Agregamos los botones a sus respectivas zonas
        zona_inicio.add_widget(btn_inicio)
        zona_reservas.add_widget(btn_reservas)
        zona_perfil.add_widget(btn_perfil)

        
        
        navegacion.add_widget(zona_inicio)
        navegacion.add_widget(zona_reservas)
        navegacion.add_widget(zona_perfil)
        
        caja.add_widget(volver)
        pantalla.add_widget(caja)
        caja.add_widget(navegacion)
        return pantalla
    
    # --------------------------------------------------
    # Crear barra de título
    # --------------------------------------------------

    def crear_titulo(self, texto):

        # Creamos una barra azul
        barra = MDBoxLayout(
            size_hint_y=None,
            height=dp(70),
            md_bg_color=AZUL
        )

        # Agregamos el texto dentro de la barra
        barra.add_widget(
            MDLabel(
                text=texto,
                halign="center",
                bold=True,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
        )

        return barra


    # --------------------------------------------------
    # Crear botón normal
    # --------------------------------------------------

    def crear_boton(self, texto, color, accion):

        # Creamos un botón reutilizable
        return MDButton(

            MDButtonText(
                text=texto,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                pos_hint={
                    "center_x": 0.5,
                    "center_y": 0.5
                }
            ),

            style="filled",

            # Permitimos utilizar nuestro propio color
            theme_bg_color="Custom",
            md_bg_color=color,

            # Hace que el botón ocupe el ancho disponible
            theme_width="Custom",
            size_hint_x=1,

            # Función que ejecutará al presionarse
            on_release=accion
        )


    # --------------------------------------------------
    # Crear botón con menú desplegable
    # --------------------------------------------------

    def crear_boton_menu(self, campo, texto, opciones):

        # Texto que aparecerá dentro del botón
        texto_boton = MDButtonText(
            text=texto,
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.5
            }
        )

        # Guardamos el texto para poder cambiarlo después
        self.textos_botones[campo] = texto_boton

        # Creamos el botón
        boton = MDButton(
            texto_boton,
            style="outlined",
            theme_width="Custom",
            size_hint_x=1
        )

        # Cuando se presione abre el menú correspondiente
        boton.bind(
            on_release=lambda x:
            self.abrir_menu(x, campo, opciones)
        )

        return boton
    
    # --------------------------------------------------
    # Abrir menú desplegable
    # --------------------------------------------------
    def abrir_menu(self, boton, campo, opciones):
    
        items = [
            {
                "text": str(opcion),
                "on_release":
                    lambda opcion=opcion:
                    self.elegir(campo, opcion)
            }
            for opcion in opciones
        ]
        self.menu = MDDropdownMenu(
            caller=boton,
            items=items
        )
        self.menu.open()
    # --------------------------------------------------
    # Guardar opción seleccionada
    # --------------------------------------------------
    def elegir(self, campo, opcion):
    
        self.seleccion[campo] = opcion
        if campo == "acompanantes":
        
            self.textos_botones[campo].text = (
                f"Acompañantes: {opcion}"
            )
        else:
        
            self.textos_botones[campo].text = str(opcion)
        self.menu.dismiss()
            
    # --------------------------------------------------
    # Mostrar diálogo
    # --------------------------------------------------

    def mostrar_dialogo(self, titulo, texto, botones):

        contenedor = MDDialogButtonContainer(
            spacing="8dp"
        )

        for texto_boton, funcion in botones:

            contenedor.add_widget(MDButton(
                    MDButtonText(
                        text=texto_boton
                    ),
                    style="text",
                    on_release=funcion
                )
            )

        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text=titulo
            ),

            MDDialogSupportingText(
                text=texto
            ),

            contenedor
        )

        self.dialog.open()


    def cerrar_dialog(self, *args):

        self.dialog.dismiss()
        
    # --------------------------------------------------
    # Confirmar reserva
    # --------------------------------------------------

    def confirmar_reserva(self, *args):

        self.reserva_nueva = Reserva(
            self.campo_nombre.text,
            self.campo_correo.text,
            self.seleccion["sala"],
            self.seleccion["dia"],
            self.seleccion["hora"],
            self.seleccion["motivo"],
            self.seleccion["acompanantes"]
        )

        errores = self.reserva_nueva.validar()

        if errores:

            self.mostrar_dialogo(
                "Revisa el formulario",
                "\n".join(errores),
                [
                    (
                        "ENTENDIDO",
                        self.cerrar_dialog
                    )
                ]
            )

        else:

            self.mostrar_dialogo(
                "¿Confirmar reserva?",
                self.reserva_nueva.resumen(),
                [
                    (
                        "CANCELAR",
                        self.cerrar_dialog
                    ),
                    (
                        "CONFIRMAR",
                        self.guardar_reserva
                    )
                ]
            )


    # --------------------------------------------------
    # Guardar reserva
    # --------------------------------------------------

    def guardar_reserva(self, *args):

        self.dialog.dismiss()

        errores = self.gestor.agregar(
            self.reserva_nueva
        )

        if errores:

            self.mostrar_dialogo(
                "No se pudo reservar",
                "\n".join(errores),
                [
                    (
                        "ENTENDIDO",
                        self.cerrar_dialog
                    )
                ]
            )

        else:

            print(
                "Reserva confirmada:",
                self.reserva_nueva.sala,
                self.reserva_nueva.dia,
                self.reserva_nueva.hora
            )

            self.ir_a_reservas()
            
    # --------------------------------------------------
    # Actualizar lista de reservas
    # --------------------------------------------------
    
    def actualizar_lista(self):
    
        self.lista.clear_widgets()
    
        if not self.gestor.reservas:
        
            self.lista.add_widget(
                MDLabel(
                    text="Aún no tienes reservas.",
                    adaptive_height=True
                )
            )
    
            return
    
        for reserva in self.gestor.reservas:
        
            self.lista.add_widget(
                MDLabel(
                    text=reserva.resumen(),
                    adaptive_height=True
                )
            )
    
            self.lista.add_widget(
                self.crear_boton(
                    "ANULAR",
                    GUINDA,
                    lambda x, r=reserva:
                        self.preguntar_anular(r)
                )
            )
    
    
    # --------------------------------------------------
    # Preguntar antes de anular crear_titulo
    # --------------------------------------------------
    
    def preguntar_anular(self, reserva):
    
        self.reserva_a_anular = reserva
    
        self.mostrar_dialogo(
            "¿Anular reserva?",
            reserva.resumen(),
            [
                (
                    "NO",
                    self.cerrar_dialog
                ),
                (
                    "SÍ, ANULAR",
                    self.anular_reserva
                )
            ]
        )
    
    
    # --------------------------------------------------
    # Anular reserva
    # --------------------------------------------------
    
    def anular_reserva(self, *args):
    
        self.dialog.dismiss()
    
        self.gestor.anular(
            self.reserva_a_anular
        )
    
        self.actualizar_lista()
    
    
    # --------------------------------------------------
    # Cambiar de pantalla crear_pantalla_reservas()
    # --------------------------------------------------
    
    def ir_a_reservas(self, *args):
    
        self.actualizar_lista()
    
        self.pantallas.current = "reservas"
    
    
    def ir_a_formulario(self, *args):
    
        self.pantallas.current = "formulario"
        
    def ir_a_calendario(self, *args):
        
            self.pantallas.current = "principal"
            
        

MiApp().run() 