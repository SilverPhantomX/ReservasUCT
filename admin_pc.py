from kivy.config import Config
Config.set("graphics", "width", "1150")
Config.set("graphics", "height", "680")

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from services.admin_repositorio import RepositorioAdminJSON
from views.admin.admin_view import AdminDashboardView


class AdminPCApp(MDApp):
    def build(self):
        self.title = "Reservas UCT - Dashboard Administrador"
        # Origen de datos del panel. Cuando exista SQL, solo se cambia esta línea.
        self.repositorio = RepositorioAdminJSON("datos_admin/reservas.json")

        sm = ScreenManager()
        sm.add_widget(AdminDashboardView(repositorio=self.repositorio, name="dashboard"))
        return sm


if __name__ == "__main__":
    AdminPCApp().run()