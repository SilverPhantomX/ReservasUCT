"""
Widgets reutilizables de la interfaz (solo presentación, sin lógica de negocio).
Así cada pantalla arma su vista con las mismas piezas y el estilo queda en un solo lugar.
"""
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, MDDialogSupportingText
from kivymd.uix.label import MDLabel, MDIcon

from views.estilos import AZUL, AZUL_SUAVE, BLANCO, GRIS_ICONO, GRIS_TEXTO, ALTO_BARRA


# ---------- estructura ----------

def banner(texto):
    """Barra superior azul con el título de la pantalla."""
    barra = MDBoxLayout(size_hint_y=None, height=ALTO_BARRA, md_bg_color=AZUL)
    barra.add_widget(MDLabel(text=texto, halign="center", bold=True,
                             theme_text_color="Custom", text_color=BLANCO))
    return barra



def icono_grande(icono, tamano=70):
    return MDButtonIcon(icon=icono, pos_hint={"center_x": 0.5},
                        theme_icon_color="Custom", icon_color=GRIS_ICONO,
                        theme_font_size="Custom", font_size=dp(tamano))


def tarjeta(*widgets, color=AZUL_SUAVE):
    """Recuadro con fondo suave y bordes redondeados. Es un MDBoxLayout (no un MDCard)
    para que no reaccione al hacer clic: solo muestra información."""
    card = MDBoxLayout(orientation="vertical", adaptive_height=True, padding=dp(16), spacing=dp(8),
                       md_bg_color=color, radius=[dp(14)])
    for widget in widgets:
        card.add_widget(widget)
    return card


def fila_dato(icono, titulo, valor_label):
    """Fila 'icono  Título / valor'. `valor_label` es un MDLabel que la vista actualiza."""
    fila = MDBoxLayout(adaptive_height=True, spacing=dp(12))
    fila.add_widget(MDIcon(icon=icono, theme_text_color="Custom", text_color=AZUL,
                           pos_hint={"center_y": 0.5}))
    textos = MDBoxLayout(orientation="vertical", adaptive_height=True)
    textos.add_widget(MDLabel(text=titulo, adaptive_height=True, font_style="Label", role="medium",
                              theme_text_color="Custom", text_color=GRIS_TEXTO))
    textos.add_widget(valor_label)
    fila.add_widget(textos)
    return fila


def fila_icono(icono, texto, color=AZUL):
    """Fila simple 'icono  texto' de una sola línea."""
    fila = MDBoxLayout(adaptive_height=True, spacing=dp(10))
    fila.add_widget(MDIcon(icon=icono, theme_text_color="Custom", text_color=color,
                           theme_font_size="Custom", font_size=dp(18), pos_hint={"center_y": 0.5}))
    fila.add_widget(MDLabel(text=texto, adaptive_height=True, font_style="Body", role="medium",
                            pos_hint={"center_y": 0.5}))
    return fila


def chip(texto, color):
    """Etiqueta pequeña con fondo de color (por ejemplo, el estado de una reserva)."""
    caja = MDBoxLayout(adaptive_size=True, padding=(dp(10), dp(4)), md_bg_color=color,
                       radius=[dp(10)], pos_hint={"center_y": 0.5})
    caja.add_widget(MDLabel(text=texto, adaptive_size=True, font_style="Label", role="medium",
                            bold=True, theme_text_color="Custom", text_color=BLANCO))
    return caja


def estado_vacio(icono, titulo, texto):
    """Mensaje centrado para cuando una lista no tiene elementos."""
    caja = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=dp(8),
                       padding=(0, dp(60), 0, 0))
    caja.add_widget(icono_grande(icono, tamano=64))
    caja.add_widget(MDLabel(text=titulo, halign="center", bold=True, adaptive_height=True))
    caja.add_widget(MDLabel(text=texto, halign="center", adaptive_height=True,
                            font_style="Body", role="medium",
                            theme_text_color="Custom", text_color=GRIS_TEXTO))
    return caja


def indicador(icono, color, numero_label, texto):
    """Columna 'icono / número / texto' para resúmenes. `numero_label` lo actualiza la vista."""
    columna = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=dp(2))
    columna.add_widget(MDIcon(icon=icono, theme_text_color="Custom", text_color=color,
                              pos_hint={"center_x": 0.5}))
    columna.add_widget(numero_label)
    columna.add_widget(MDLabel(text=texto, halign="center", adaptive_height=True,
                               font_style="Label", role="small",
                               theme_text_color="Custom", text_color=GRIS_TEXTO))
    return columna


# ---------- botones ----------

def boton_contorno(texto, color, accion, icono=None):
    """Botón de ancho completo solo con borde (acción secundaria)."""
    partes = []
    if icono:
        partes.append(MDButtonIcon(icon=icono, theme_icon_color="Custom", icon_color=color))
    partes.append(MDButtonText(text=texto, theme_text_color="Custom", text_color=color,
                               pos_hint={"center_x": 0.5, "center_y": 0.5}))
    return MDButton(*partes, style="outlined", theme_width="Custom", size_hint_x=1,
                    theme_line_color="Custom", line_color=color, on_release=accion)


def boton_enlace(texto, accion):
    """Botón de solo texto, para enlaces como '¿No tienes cuenta? Regístrate'."""
    return MDButton(MDButtonText(text=texto, theme_text_color="Custom", text_color=AZUL),
                    style="text", pos_hint={"center_x": 0.5}, on_release=accion)


# ---------- diálogos ----------

def mostrar_dialogo(titulo, texto, botones=None):
    """
    Abre un MDDialog. `botones` es una lista de (texto, accion); cada botón cierra
    el diálogo y luego ejecuta su accion (o solo cierra si accion es None).
    Por defecto muestra un único botón "ENTENDIDO".
    """
    botones = botones or [("ENTENDIDO", None)]
    referencia = {}  # el diálogo se crea después de los botones

    def crear_al_presionar(accion):
        def al_presionar(*args):
            referencia["dialogo"].dismiss()
            if accion is not None:
                accion()
        return al_presionar

    contenedor = MDDialogButtonContainer(spacing="8dp")
    for texto_boton, accion in botones:
        contenedor.add_widget(MDButton(MDButtonText(text=texto_boton), style="text",
                                       on_release=crear_al_presionar(accion)))

    dialogo = MDDialog(MDDialogHeadlineText(text=titulo),
                       MDDialogSupportingText(text=texto),
                       contenedor)
    referencia["dialogo"] = dialogo
    dialogo.open()
    return dialogo
