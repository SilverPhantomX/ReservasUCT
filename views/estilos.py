"""Colores y medidas comunes de la app: se cambian aquí y se aplican en todas las vistas."""
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

AZUL = get_color_from_hex("#01568e")
GUINDA = get_color_from_hex("#7B1D35")
BLANCO = (1, 1, 1, 1)
GRIS_ICONO = (0.25, 0.25, 0.25, 1)
GRIS_TEXTO = (0.45, 0.45, 0.45, 1)
AZUL_SUAVE = get_color_from_hex("#e8f1f8")   # fondo claro para tarjetas
GRIS_SUAVE = get_color_from_hex("#f2f2f2")   # fondo de tarjetas inactivas (historial)
VERDE = get_color_from_hex("#2e7d32")

ALTO_BARRA = dp(70)
