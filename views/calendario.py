from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.gridlayout import MDGridLayout
from kivy.metrics import dp
from datetime import datetime
import calendar
from kivy.utils import get_color_from_hex
from kivymd.uix.anchorlayout import MDAnchorLayout

AZUL = get_color_from_hex("#01568e")
GUINDA = get_color_from_hex("#7B1D35")


# --------------------------------------------------
# Pantalla de Calendario
# --------------------------------------------------

class Calendario(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical')
                
        principal = MDBoxLayout(orientation="vertical") #layout de la app
        
        #banner de la app
        banner = MDBoxLayout(size_hint_y=None, height=dp(70), md_bg_color= AZUL)     
        #titulo del banner Nombre, aliniacion, color y agregacion al banner
        titulo = MDLabel(text="Academia de Artes Musicales", halign="center", bold=True, theme_text_color="Custom", text_color=(1, 1, 1, 1))
        banner.add_widget(titulo)
        
        # Barra para seleccionar el mes del calendario seleccionar_fecha() 
        # Guardamos el mes y año actuales
        hoy = datetime.now()

        self.mes_actual = hoy.month #Mes actual
        self.anio_actual = hoy.year #Año actual
        
        #barra de selecion de mes
        selector_mes = MDBoxLayout(size_hint_y=None, height=dp(55), padding=dp(10))

        # Flecha para ir al mes anterior, color, icono, estilo y tamaño
        btn_mes_anterior = MDButton(
            MDButtonIcon(icon="chevron-left", theme_text_color="Custom", text_color=AZUL),
            style="text",
            size_hint=(None, None))

        #label del nombre del mes actual
        self.lbl_mes = MDLabel(text="", halign="center", bold=True, theme_text_color="Custom", text_color=AZUL)

        # Flecha para ir al mes siguiente, color, icono, estilo y tamaño
        btn_mes_siguiente = MDButton(
            MDButtonIcon(icon="chevron-right", theme_text_color="Custom", text_color=AZUL),
            style="text",
            size_hint=(None, None))
        
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
        contenido = MDBoxLayout(orientation="vertical", adaptive_height=True)

        # Cuadrícula de 7 columnas, una para cada día de la semana
        self.calendario = MDGridLayout(cols=7, adaptive_height=True, spacing=dp(2), padding=dp(5))

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
            style="text",
            size_hint=(None, None),
            on_release=lambda x: setattr(self.manager, 'current', 'perfil'))
        
        
        # Agregamos los botones a sus respectivas zonas
        zona_inicio.add_widget(btn_inicio)
        zona_reservas.add_widget(btn_reservas)
        zona_perfil.add_widget(btn_perfil)
        
        navegacion.add_widget(zona_inicio)
        navegacion.add_widget(zona_reservas)
        navegacion.add_widget(zona_perfil)

        #PINTAMOS LA PANTALLA CALENDARIO

        principal.add_widget(banner)
        principal.add_widget(selector_mes)
        principal.add_widget(scroll)
        principal.add_widget(navegacion)
        
        self.add_widget(principal)
        self.actualizar_mes()
        
    # Cambiar al mes anterior
    def mes_anterior(self, *args):
        #se le resta 1 al mes actual
        self.mes_actual -= 1

        # si el numero del mes actual es 0 se cambia a 12 y se le resta 1 al año actual
        if self.mes_actual == 0:
            self.mes_actual = 12
            self.anio_actual -= 1

        self.actualizar_mes()

    # Cambiar al mes siguiente
    def mes_siguiente(self, *args):
        #se le suma 1 al mes actual
        self.mes_actual += 1

        # si el numero del mes actual es 13 se cambia a 1 y se le suma 1 al año actual
        if self.mes_actual == 13:
            self.mes_actual = 1
            self.anio_actual += 1

        self.actualizar_mes()

    # Actualizar el texto del mes
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
        #aqui se maneja los meses y se agrega el año actual
        self.lbl_mes.text = f"{meses[self.mes_actual - 1]} {self.anio_actual}"
        self.actualizar_calendario()

    # Dibujar el calendario
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
            "Dom"]
        #variable del dia de hoy para que no se puedan elegir dias anteriores
        hoy = datetime.now().date()

        # Se recorren y se agregan los nombres de los días
        for dia_semana in dias_semana:
            etiqueta = MDLabel(text=dia_semana, halign="center", bold=True, size_hint_y=None, height=dp(40))#etiqueta de los dias
            self.calendario.add_widget(etiqueta)    #se agrega la etiqueta

        # Obtenemos las semanas del mes actual
        semanas = calendar.monthcalendar(self.anio_actual, self.mes_actual)

        # Recorremos cada semana
        for semana in semanas:
            # Recorremos los 7 días de cada semana
            for dia in semana:
                # Si vale 0, ese espacio no pertenece al mes actual calendar.monthcalendar() usa 0 para rellenar espacios vacíos.
                if dia == 0:
                    espacio = MDLabel(text="", size_hint_y=None, height=dp(45))#se deja vacio porque no pertenece al mes
                    self.calendario.add_widget(espacio)#se deja vacio porque no pertenece al mes
                #en cambio si el dia existe se crea la fecha completa    
                else:   
                    fecha_dia = datetime(self.anio_actual, self.mes_actual, dia).date()
                    
                    # Creamos un botón para cada día real
                    boton_dia = MDButton(MDButtonText(text=str(dia)), style="text", 
                        theme_width="Custom", size_hint_x = 1, size_hint_y=None, height=dp(45),
                        disabled=fecha_dia < hoy or fecha_dia.weekday() >= 5)#se desahibila si es dia de fin de semana o antes de la fecha hoy
                    
                    #Guardamos el número de ese día al presionarlo
                    boton_dia.bind(on_release=lambda boton, d=dia: self.seleccionar_fecha(d))
                    self.calendario.add_widget(boton_dia)

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
        self.manager.current = "formulario" 