import json
import os
from datetime import datetime
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogContentContainer,
    MDDialogHeadlineText,
    MDDialogSupportingText,
)
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText

AZUL = get_color_from_hex("#01568e")
AZUL_CLARO = get_color_from_hex("#cfe3f2")
GUINDA = get_color_from_hex("#7B1D35")
GRIS = get_color_from_hex("#f2f2f2")
GRIS_BORDE = get_color_from_hex("#e0e0e0")
ROJO = get_color_from_hex("#b71c1c")
VERDE = get_color_from_hex("#1b5e20")
BLANCO = (1, 1, 1, 1)


class ReservasAdminView(MDScreen):
    """Vista de administración con listado detallado, buscador, edición y eliminación de reservas."""

    def __init__(self, repositorio=None, **kwargs):
        super().__init__(**kwargs)
        self.repositorio = repositorio
        self.reservas = repositorio.listar() if repositorio else []
        self.filtro_texto = ""
        self.dialog = None

        raiz = MDBoxLayout(orientation="vertical")

        # ---------- Banner superior ----------
        banner = MDBoxLayout(size_hint_y=None, height=dp(70), md_bg_color=AZUL, padding=[dp(16), 0])
        banner.add_widget(
            MDLabel(
                text="Academia de Artes Musicales - Gestión de Reservas",
                halign="center",
                bold=True,
                theme_text_color="Custom",
                text_color=BLANCO,
            )
        )
        raiz.add_widget(banner)

        # ---------- Barra de herramientas (Buscador + Contador + Nueva Reserva + Refrescar) ----------
        barra = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(68),
            padding=[dp(16), dp(10)],
            spacing=dp(12),
            md_bg_color=GRIS,
        )

        self.txt_buscar = MDTextField(
            MDTextFieldHintText(text="Buscar por nombre, correo, sala, fecha (d/m/aaaa) o código..."),
            mode="outlined",
            size_hint_x=0.55,
        )
        self.txt_buscar.bind(text=self.al_buscar)
        barra.add_widget(self.txt_buscar)

        self.lbl_contador = MDLabel(
            text="0 reserva(s)",
            bold=True,
            size_hint_x=0.20,
            halign="center",
        )
        barra.add_widget(self.lbl_contador)

        btn_nueva = MDButton(
            MDButtonIcon(icon="plus", theme_text_color="Custom", text_color=BLANCO),
            MDButtonText(text="Nueva reserva", theme_text_color="Custom", text_color=BLANCO),
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=AZUL,
            on_release=lambda *a: self.abrir_formulario_edicion(reserva=None),
        )
        barra.add_widget(btn_nueva)

        btn_refrescar = MDButton(
            MDButtonIcon(icon="refresh"),
            MDButtonText(text="Actualizar"),
            style="tonal",
            on_release=lambda *a: self.refrescar(forzar=True),
        )
        barra.add_widget(btn_refrescar)

        raiz.add_widget(barra)

        # ---------- Cabecera de la tabla ----------
        cabecera = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(44),
            padding=[dp(16), dp(4)],
            spacing=dp(8),
            md_bg_color=AZUL_CLARO,
        )
        columnas = [
            ("Fecha y Hora", 0.16),
            ("Sala", 0.16),
            ("Solicitante / Correo", 0.24),
            ("Motivo / Acomp.", 0.20),
            ("Código", 0.10),
            ("Acciones", 0.14),
        ]
        for titulo, peso in columnas:
            cabecera.add_widget(
                MDLabel(
                    text=titulo,
                    bold=True,
                    size_hint_x=peso,
                    halign="left" if titulo != "Acciones" else "center",
                )
            )
        raiz.add_widget(cabecera)

        # ---------- Lista desplazable de reservas ----------
        self.contenedor_lista = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=dp(6),
            padding=[dp(12), dp(10)],
        )
        scroll = MDScrollView()
        scroll.add_widget(self.contenedor_lista)
        raiz.add_widget(scroll)

        self.add_widget(raiz)

        self.dibujar_lista()
        Clock.schedule_interval(lambda dt: self.refrescar(), 10)

    # ------------------------------------------------------------------
    # Sincronización y Persistencia con el Repositorio
    # ------------------------------------------------------------------
    def on_enter(self, *args):
        self.refrescar(forzar=True)

    def refrescar(self, forzar=False):
        if not self.repositorio:
            return
        nuevas = self.repositorio.listar()
        if forzar or nuevas != self.reservas:
            self.reservas = nuevas
            self.dibujar_lista()

    def _persistir_cambios(self):
        """Guarda la lista actualizada en self.repositorio usando sus métodos o su ruta JSON."""
        if not self.repositorio:
            return

        # 1. Si el repositorio implementa un método guardar_todas / guardar_lista / actualizar_todas
        for metodo in ("guardar_todas", "guardar_lista", "actualizar_todas", "escribir"):
            if hasattr(self.repositorio, metodo) and callable(getattr(self.repositorio, metodo)):
                getattr(self.repositorio, metodo)(self.reservas)
                return

        # 2. Si el repositorio tiene un atributo de ruta al archivo JSON (ej. ruta, archivo, path, filepath)
        for attr in ("ruta", "archivo", "path", "filepath", "ruta_json"):
            ruta = getattr(self.repositorio, attr, None)
            if isinstance(ruta, str) and ruta:
                os.makedirs(os.path.dirname(ruta) or ".", exist_ok=True)
                with open(ruta, "w", encoding="utf-8") as f:
                    json.dump(self.reservas, f, ensure_ascii=False, indent=2)
                return

        # 3. Fallback a la ruta configurada en admin_pc.py
        ruta_defecto = "datos_admin/reservas.json"
        os.makedirs(os.path.dirname(ruta_defecto), exist_ok=True)
        with open(ruta_defecto, "w", encoding="utf-8") as f:
            json.dump(self.reservas, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # Búsqueda y Ordenamiento
    # ------------------------------------------------------------------
    def al_buscar(self, instancia, texto):
        self.filtro_texto = (texto or "").strip().lower()
        self.dibujar_lista()

    @staticmethod
    def _clave_orden(r):
        """Ordena por fecha (d/m/aaaa) y hora."""
        try:
            fecha = datetime.strptime(r.get("dia", "01/01/2000"), "%d/%m/%Y")
        except ValueError:
            fecha = datetime(2000, 1, 1)
        return (fecha, r.get("hora", ""))

    def _coincide_filtro(self, r):
        if not self.filtro_texto:
            return True
        campos = [
            str(r.get("dia", "")),
            str(r.get("hora", "")),
            str(r.get("sala", "")),
            str(r.get("nombre", "")),
            str(r.get("correo", "")),
            str(r.get("motivo", "")),
            str(r.get("codigo_acceso", "")),
        ]
        texto_completo = " ".join(campos).lower()
        return self.filtro_texto in texto_completo

    # ------------------------------------------------------------------
    # Renderizado de la Lista
    # ------------------------------------------------------------------
    def dibujar_lista(self):
        self.contenedor_lista.clear_widgets()

        filtradas = [r for r in self.reservas if self._coincide_filtro(r)]
        filtradas.sort(key=self._clave_orden, reverse=True)

        self.lbl_contador.text = f"{len(filtradas)} de {len(self.reservas)} reserva(s)"

        if not filtradas:
            vacio = MDBoxLayout(size_hint_y=None, height=dp(120), padding=dp(20))
            vacio.add_widget(
                MDLabel(
                    text="No se encontraron reservas con los criterios actuales.",
                    halign="center",
                    theme_text_color="Secondary",
                )
            )
            self.contenedor_lista.add_widget(vacio)
            return

        for idx, r in enumerate(filtradas):
            color_fila = BLANCO if idx % 2 == 0 else GRIS
            fila = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(68),
                padding=[dp(12), dp(6)],
                spacing=dp(8),
                md_bg_color=color_fila,
                radius=[dp(6)] * 4,
            )

            # 1. Fecha y Hora
            fila.add_widget(
                MDLabel(
                    text=f"{r.get('dia', '-')}\n{r.get('hora', '-')}",
                    bold=True,
                    size_hint_x=0.16,
                )
            )

            # 2. Sala
            fila.add_widget(
                MDLabel(
                    text=str(r.get("sala", "-")),
                    size_hint_x=0.16,
                )
            )

            # 3. Solicitante y Correo
            fila.add_widget(
                MDLabel(
                    text=f"{r.get('nombre', '-')}\n{r.get('correo', '-')}",
                    size_hint_x=0.24,
                )
            )

            # 4. Motivo y Acompañantes
            fila.add_widget(
                MDLabel(
                    text=f"{r.get('motivo', '-')}\nAcompañantes: {r.get('acompanantes', 0)}",
                    size_hint_x=0.20,
                )
            )

            # 5. Código de acceso
            fila.add_widget(
                MDLabel(
                    text=str(r.get("codigo_acceso", "-")),
                    bold=True,
                    theme_text_color="Custom",
                    text_color=GUINDA,
                    size_hint_x=0.10,
                )
            )

            # 6. Acciones (Ver / Editar / Eliminar)
            acciones = MDBoxLayout(
                orientation="horizontal",
                size_hint_x=0.14,
                spacing=dp(4),
                pos_hint={"center_y": 0.5},
            )

            btn_editar = MDButton(
                MDButtonIcon(icon="pencil", theme_text_color="Custom", text_color=AZUL),
                style="text",
                on_release=lambda x, res=r: self.abrir_formulario_edicion(res),
            )
            btn_eliminar = MDButton(
                MDButtonIcon(icon="delete", theme_text_color="Custom", text_color=ROJO),
                style="text",
                on_release=lambda x, res=r: self.confirmar_eliminacion(res),
            )

            acciones.add_widget(btn_editar)
            acciones.add_widget(btn_eliminar)
            fila.add_widget(acciones)

            self.contenedor_lista.add_widget(fila)

    # ------------------------------------------------------------------
    # Crear / Modificar Reserva (Diálogo con formulario)
    # ------------------------------------------------------------------
    def abrir_formulario_edicion(self, reserva=None):
        es_nueva = reserva is None
        datos = reserva or {
            "dia": datetime.today().strftime("%d/%m/%Y"),
            "hora": "09:00",
            "sala": "Sala de Piano",
            "nombre": "",
            "correo": "",
            "motivo": "Práctica individual",
            "acompanantes": 0,
            "codigo_acceso": "",
        }

        self.in_dia = MDTextField(
            MDTextFieldHintText(text="Fecha (dd/mm/aaaa)"),
            text=str(datos.get("dia", "")),
            mode="outlined",
        )
        self.in_hora = MDTextField(
            MDTextFieldHintText(text="Hora (ej. 09:00)"),
            text=str(datos.get("hora", "")),
            mode="outlined",
        )
        self.in_sala = MDTextField(
            MDTextFieldHintText(text="Sala (ej. Sala de Piano)"),
            text=str(datos.get("sala", "")),
            mode="outlined",
        )
        self.in_nombre = MDTextField(
            MDTextFieldHintText(text="Nombre del solicitante"),
            text=str(datos.get("nombre", "")),
            mode="outlined",
        )
        self.in_correo = MDTextField(
            MDTextFieldHintText(text="Correo electrónico"),
            text=str(datos.get("correo", "")),
            mode="outlined",
        )
        self.in_motivo = MDTextField(
            MDTextFieldHintText(text="Motivo de la reserva"),
            text=str(datos.get("motivo", "")),
            mode="outlined",
        )
        self.in_acomp = MDTextField(
            MDTextFieldHintText(text="Número de acompañantes"),
            text=str(datos.get("acompanantes", 0)),
            mode="outlined",
        )
        self.in_codigo = MDTextField(
            MDTextFieldHintText(text="Código de acceso"),
            text=str(datos.get("codigo_acceso", "")),
            mode="outlined",
        )

        contenedor_campos = MDDialogContentContainer(
            orientation="vertical",
            spacing=dp(10),
        )
        for campo in (
            self.in_dia,
            self.in_hora,
            self.in_sala,
            self.in_nombre,
            self.in_correo,
            self.in_motivo,
            self.in_acomp,
            self.in_codigo,
        ):
            contenedor_campos.add_widget(campo)

        botones = MDDialogButtonContainer(spacing=dp(8))
        botones.add_widget(
            MDButton(
                MDButtonText(text="CANCELAR"),
                style="text",
                on_release=lambda *a: self.dialog.dismiss(),
            )
        )
        botones.add_widget(
            MDButton(
                MDButtonText(text="GUARDAR", theme_text_color="Custom", text_color=BLANCO),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=AZUL,
                on_release=lambda *a: self.guardar_edicion(reserva_original=reserva),
            )
        )

        titulo = "Nueva reserva" if es_nueva else "Modificar reserva"
        self.dialog = MDDialog(
            MDDialogHeadlineText(text=titulo),
            contenedor_campos,
            botones,
        )
        self.dialog.open()

    def guardar_edicion(self, reserva_original=None):
        try:
            acompanantes_val = int(self.in_acomp.text.strip() or "0")
        except ValueError:
            acompanantes_val = 0

        nueva_data = {
            "dia": self.in_dia.text.strip(),
            "hora": self.in_hora.text.strip(),
            "sala": self.in_sala.text.strip(),
            "nombre": self.in_nombre.text.strip(),
            "correo": self.in_correo.text.strip(),
            "motivo": self.in_motivo.text.strip(),
            "acompanantes": acompanantes_val,
            "codigo_acceso": self.in_codigo.text.strip() or "S/C",
        }

        if reserva_original is None:
            # Crear nueva
            self.reservas.append(nueva_data)
        else:
            # Actualizar en sitio el diccionario original para reflejar cambios en todas las vistas
            if reserva_original in self.reservas:
                idx = self.reservas.index(reserva_original)
                self.reservas[idx].update(nueva_data)

        self._persistir_cambios()
        if self.dialog:
            self.dialog.dismiss()
        self.dibujar_lista()

    # ------------------------------------------------------------------
    # Eliminar Reserva (Diálogo de confirmación)
    # ------------------------------------------------------------------
    def confirmar_eliminacion(self, reserva):
        detalle = (
            f"¿Estás seguro de que deseas eliminar esta reserva?\n\n"
            f"• Fecha y hora: {reserva.get('dia', '-')} a las {reserva.get('hora', '-')}\n"
            f"• Sala: {reserva.get('sala', '-')}\n"
            f"• Solicitante: {reserva.get('nombre', '-')} ({reserva.get('correo', '-')})"
        )

        botones = MDDialogButtonContainer(spacing=dp(8))
        botones.add_widget(
            MDButton(
                MDButtonText(text="CANCELAR"),
                style="text",
                on_release=lambda *a: self.dialog.dismiss(),
            )
        )
        botones.add_widget(
            MDButton(
                MDButtonText(text="ELIMINAR", theme_text_color="Custom", text_color=BLANCO),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=ROJO,
                on_release=lambda *a: self.eliminar_reserva(reserva),
            )
        )

        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Confirmar eliminación"),
            MDDialogSupportingText(text=detalle),
            botones,
        )
        self.dialog.open()

    def eliminar_reserva(self, reserva):
        if reserva in self.reservas:
            self.reservas.remove(reserva)
            self._persistir_cambios()
        if self.dialog:
            self.dialog.dismiss()
        self.dibujar_lista()