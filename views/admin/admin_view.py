from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from views.admin.barra_admin import PanelAdmin
from views.admin.sidebar import Sidebar


class Pendiente(MDScreen):
    """Pantalla provisoria para las secciones que aún no existen."""

    def __init__(self, titulo, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDLabel(text=f"{titulo}\n(en construcción)", halign="center"))


class AdminDashboardView(MDScreen):
    """Pantalla 'dashboard' de admin_pc.py: barra lateral + contenido (el calendario va primero)."""

    def __init__(self, repositorio, **kwargs):
        super().__init__(**kwargs)
        contenido = ScreenManager()
        contenido.add_widget(PanelAdmin(repositorio=repositorio, name="calendario"))  # primera = pantalla inicial
        contenido.add_widget(Pendiente("Lista de reservas", name="reservas"))
        contenido.add_widget(Pendiente("Perfil", name="perfil"))

        sidebar = Sidebar(contenido, [
            ("calendar-month", "Calendario", "calendario"),
            ("format-list-bulleted", "Reservas", "reservas"),
            ("account", "Perfil", "perfil"),
        ])

        raiz = MDBoxLayout(orientation="horizontal")
        raiz.add_widget(sidebar)
        raiz.add_widget(contenido)
        self.add_widget(raiz)