from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button

class MiApp(App):
    def build(self):
        Window.clearcolor = (200, 150, 100, 200) # color de fondo de toda la ventana
        boton = Button(text="Hola con color")
        return boton
    
MiApp().run()