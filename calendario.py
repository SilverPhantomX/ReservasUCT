from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.pickers import MDModalDatePicker
from kivymd.uix.screen import MDScreen


class MiApp(MDApp):

    def build(self):
        return MDScreen(
            MDButton(
                MDButtonText(
                    text="Seleccionar fecha"
                ),
                style="filled",
                pos_hint={
                    "center_x": 0.5,
                    "center_y": 0.5
                },
                on_release=self.abrir_calendario,
            )
        )

    def abrir_calendario(self, *args):
        calendario = MDModalDatePicker()
        calendario.bind(on_ok=self.guardar_fecha)
        calendario.open()

    def guardar_fecha(self, calendario):
        fecha = calendario.get_date()

        print("Fecha seleccionada:", fecha)

        calendario.dismiss()


MiApp().run()