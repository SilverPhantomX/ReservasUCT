import calendar
from datetime import date

from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, MDDialogSupportingText
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.screen import MDScreen

from models.reserva_model import HORAS  # 09:00 ... 21:00 (mismo listado que la app móvil)
from services import agenda
from services import agenda  # lógica de la semana (sin Kivy)

AZUL = get_color_from_hex("#01568e")
AZUL_CLARO = get_color_from_hex("#cfe3f2")
GUINDA = get_color_from_hex("#7B1D35")
GRIS = get_color_from_hex("#f2f2f2")
OCUPADO = get_color_from_hex("#f6dde3")
BLANCO = (1, 1, 1, 1)

MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
         "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
DIAS_CORTOS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
DIAS_LARGOS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
ANCHO_HORA = dp(64)


class Celda(ButtonBehavior, MDBoxLayout):
    """Celda de la grilla (un día + una hora). Se puede presionar para ver el detalle."""


class PanelAdmin(MDScreen):
    def __init__(self, repositorio=None, **kwargs):
        super().__init__(**kwargs)
        self.repositorio = repositorio  # origen de datos (ver services/admin_repositorio.py)
        self.reservas = repositorio.listar() if repositorio else []  # lista de diccionarios
        hoy = date.today()
        self.mes, self.anio = hoy.month, hoy.year
        self.semana_inicio = agenda.lunes_de(hoy)  # lunes de la semana actual

        raiz = MDBoxLayout(orientation="vertical")

        # Banner
        banner = MDBoxLayout(size_hint_y=None, height=dp(70), md_bg_color=AZUL)
        banner.add_widget(MDLabel(text="Academia de Artes Musicales - Panel de administración",
                                  halign="center", bold=True, theme_text_color="Custom", text_color=BLANCO))
        raiz.add_widget(banner)

        cuerpo = MDBoxLayout(orientation="horizontal", padding=dp(10), spacing=dp(10))

        # ---------- Columna izquierda: calendario ----------
        izquierda = MDBoxLayout(orientation="vertical", size_hint_x=None, width=dp(300), spacing=dp(6))

        selector = MDBoxLayout(size_hint_y=None, height=dp(48))
        selector.add_widget(MDButton(MDButtonIcon(icon="chevron-left"), style="text",
                                     on_release=self.mes_anterior))
        self.lbl_mes = MDLabel(text="", halign="center", bold=True)
        selector.add_widget(self.lbl_mes)
        selector.add_widget(MDButton(MDButtonIcon(icon="chevron-right"), style="text",
                                     on_release=self.mes_siguiente))
        izquierda.add_widget(selector)

        self.cal = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=dp(2))
        izquierda.add_widget(self.cal)
        izquierda.add_widget(MDLabel(text="Toca cualquier día para ver la semana completa.",
                                     size_hint_y=None, height=dp(40), theme_text_color="Secondary"))
        izquierda.add_widget(MDBoxLayout())  # relleno: empuja el calendario hacia arriba

        # ---------- Columna derecha: semana ----------
        derecha = MDBoxLayout(orientation="vertical", spacing=dp(6))
        self.lbl_semana = MDLabel(text="", bold=True, size_hint_y=None, height=dp(40))
        derecha.add_widget(self.lbl_semana)

        self.grid = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=dp(2))
        scroll = MDScrollView()
        scroll.add_widget(self.grid)
        derecha.add_widget(scroll)

        cuerpo.add_widget(izquierda)
        cuerpo.add_widget(derecha)
        raiz.add_widget(cuerpo)
        self.add_widget(raiz)

        self.actualizar_todo()
        # Revisa cada 10 s si hay reservas nuevas en el origen de datos
        Clock.schedule_interval(lambda dt: self.refrescar(), 10)

    # ------------------------------------------------------------------
    # Datos
    # ------------------------------------------------------------------
    def on_enter(self, *args):
        self.refrescar()

    def refrescar(self):
        """Vuelve a consultar el origen de datos y redibuja solo si algo cambió."""
        if not self.repositorio:
            return
        nuevas = self.repositorio.listar()
        if nuevas != self.reservas:
            self.cargar_reservas(nuevas)

    def cargar_reservas(self, reservas):
        """Recibe una lista de dicts: dia (d/m/aaaa), hora, sala, nombre..."""
        self.reservas = reservas
        self.dibujar_semana()

    # ------------------------------------------------------------------
    # Calendario mensual (con selección de fila = semana)
    # ------------------------------------------------------------------
    def mes_anterior(self, *args):
        self.mes -= 1
        if self.mes == 0:
            self.mes, self.anio = 12, self.anio - 1
        self.actualizar_todo()

    def mes_siguiente(self, *args):
        self.mes += 1
        if self.mes == 13:
            self.mes, self.anio = 1, self.anio + 1
        self.actualizar_todo()

    def seleccionar_semana(self, lunes):
        self.semana_inicio = lunes
        self.actualizar_todo()

    def actualizar_todo(self):
        self.lbl_mes.text = f"{MESES[self.mes - 1]} {self.anio}"
        self.dibujar_calendario()
        self.dibujar_semana()

    def dibujar_calendario(self):
        self.cal.clear_widgets()

        cabecera = MDBoxLayout(size_hint_y=None, height=dp(30))
        for nombre in DIAS_CORTOS:
            cabecera.add_widget(MDLabel(text=nombre, halign="center", bold=True))
        self.cal.add_widget(cabecera)

        for semana in calendar.Calendar(firstweekday=0).monthdatescalendar(self.anio, self.mes):
            lunes = semana[0]
            seleccionada = lunes == self.semana_inicio
            fila = MDBoxLayout(size_hint_y=None, height=dp(40), spacing=dp(2), padding=dp(2),
                               md_bg_color=AZUL_CLARO if seleccionada else (0, 0, 0, 0))
            for f in semana:
                fuera_del_mes = f.month != self.mes
                color = (0.6, 0.6, 0.6, 1) if fuera_del_mes else (0.1, 0.1, 0.1, 1)
                fila.add_widget(MDButton(
                    MDButtonText(text=str(f.day), theme_text_color="Custom", text_color=color),
                    style="text", theme_width="Custom", size_hint_x=1,
                    on_release=lambda x, l=lunes: self.seleccionar_semana(l)))
            self.cal.add_widget(fila)

    # ------------------------------------------------------------------
    # Grilla semanal: filas = horas, columnas = días (Lun-Vie)
    # ------------------------------------------------------------------
    def dibujar_semana(self):
        self.grid.clear_widgets()
        dias = agenda.dias_de_semana(self.semana_inicio)
        fin = dias[-1]
        por_celda = agenda.reservas_por_celda(self.reservas, self.semana_inicio)  # {(fecha, hora): [reservas]}
        total = agenda.total(por_celda)

        self.lbl_semana.text = (f"Semana del {self.semana_inicio.day} de {MESES[self.semana_inicio.month - 1].lower()} "
                                f"al {fin.day} de {MESES[fin.month - 1].lower()} de {fin.year}  -  {total} reserva(s)")

        # Cabecera con los días
        cabecera = MDBoxLayout(size_hint_y=None, height=dp(48), spacing=dp(2))
        cabecera.add_widget(MDLabel(text="", size_hint_x=None, width=ANCHO_HORA))
        for d in dias:
            caja = MDBoxLayout(md_bg_color=AZUL)
            caja.add_widget(MDLabel(text=f"{DIAS_LARGOS[d.weekday()]} {d.day}", halign="center", bold=True,
                                    theme_text_color="Custom", text_color=BLANCO))
            cabecera.add_widget(caja)
        self.grid.add_widget(cabecera)

        # Una fila por cada hora
        for hora in HORAS:
            contenido = [por_celda.get((d, hora), []) for d in dias]
            mas_alta = max([len(c) for c in contenido] + [1])
            fila = MDBoxLayout(size_hint_y=None, height=max(dp(44), dp(12) + dp(20) * mas_alta), spacing=dp(2))
            fila.add_widget(MDLabel(text=hora, halign="center", bold=True, size_hint_x=None, width=ANCHO_HORA))

            for d, items in zip(dias, contenido):
                celda = Celda(orientation="vertical", padding=dp(4), spacing=dp(2),
                              md_bg_color=OCUPADO if items else GRIS)
                for r in items:
                    celda.add_widget(MDLabel(text=f"{self.sala_corta(r['sala'])}: {r['nombre']}",
                                             size_hint_y=None, height=dp(20)))
                if items:
                    celda.bind(on_release=lambda x, d=d, h=hora, it=items: self.ver_detalle(d, h, it))
                fila.add_widget(celda)
            self.grid.add_widget(fila)

    @staticmethod
    def sala_corta(sala):
        corta = sala.replace("Sala de ", "")
        return corta[:1].upper() + corta[1:]

    # ------------------------------------------------------------------
    # Detalle al presionar una celda
    # ------------------------------------------------------------------
    def ver_detalle(self, dia, hora, items):
        lineas = []
        for r in items:
            lineas.append(f"{r['sala']}\n{r['nombre']} ({r.get('correo', '-')})\n"
                          f"Motivo: {r.get('motivo', '-')} - Acompañantes: {r.get('acompanantes', 0)}\n"
                          f"Código de acceso: {r.get('codigo_acceso', '-')}")
        botones = MDDialogButtonContainer(spacing="8dp")
        botones.add_widget(MDButton(MDButtonText(text="CERRAR"), style="text",
                                    on_release=lambda *a: self.dialog.dismiss()))
        self.dialog = MDDialog(
            MDDialogHeadlineText(text=f"{DIAS_LARGOS[dia.weekday()]} {dia.day} - {hora}"),
            MDDialogSupportingText(text="\n\n".join(lineas)),
            botones)
        self.dialog.open()