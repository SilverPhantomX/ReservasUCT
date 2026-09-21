from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer)
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window

class MiApp(MDApp):
    
    def build(self):
        
        Window.clearcolor = (200, 150, 100, 200) # color de fondo de toda la ventana

        pantalla = MDScreen()
        
        boton = MDButton(
        MDButtonText(text="¿Desea reservar una sala?"), 
        style="filled",
        pos_hint={"center_x": 0.5, "center_y": 0.5},)
        
        self.boton2 = MDButton(
        MDButtonText(text="Opciones"),
        style="filled",
        pos_hint={"center_x": 0.5, "center_y": 0.4},)
        
        self.boton2.bind(on_release=self.abrir_menu)
        
        pantalla.add_widget(self.boton2)
        
        boton.bind(on_release=self.mostrar_confirmacion)
        
        pantalla.add_widget(boton)
        
        return pantalla
    
    def abrir_menu(self, instance):
        opciones = [
        {"text": "Anular reserva", "on_release": lambda: self.elegir("Anular reserva")},
        {"text": "Volver a la pantalla principal", "on_release": lambda: self.elegir("Volver a la pantalla principal")},
        ]
        self.menu = MDDropdownMenu(caller=instance, items=opciones)
        self.menu.open()
    def elegir(self, texto):
        print("Elegiste:", texto)
        self.menu.dismiss()
        
    def mostrar_confirmacion(self, instance):
        self.dialog = MDDialog(
        MDDialogHeadlineText(text="Confirmación"),
        MDDialogSupportingText(text="¿Está seguro de que desea reservar una sala?"),
        MDDialogButtonContainer(
        MDButton(
        MDButtonText(text="CANCELAR"),
        style="text",
        on_release=self.cerrar_dialog,
        ),
        MDButton(
        MDButtonText(text="CONFIRMAR"),
        style="text",
        on_release=self.confirmar,
        ),
        spacing="8dp",
        ),
        )
        self.dialog.open()
        
    def cerrar_dialog(self, instance):
        self.dialog.dismiss()
        
    def confirmar(self, instance):
        print("Reserva confirmada") 
        self.dialog.dismiss()

MiApp().run()