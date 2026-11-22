from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
from views.calendario import AZUL
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, MDDialogSupportingText
from kivy.utils import get_color_from_hex
from kivymd.uix.anchorlayout import MDAnchorLayout


AZUL = get_color_from_hex("#01568e")
GUINDA = get_color_from_hex("#7B1D35")

class PerfilView(Screen):
    def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.layout = MDBoxLayout(orientation='vertical')   
            principal = MDBoxLayout(orientation="vertical") #layout de la app
            
            
            #banner de la app
            banner = MDBoxLayout(size_hint_y=None, height=dp(70), md_bg_color= AZUL) 
            #titulo del banner Nombre, aliniacion, color y agregacion al banner
            titulo = MDLabel(text="Academia de Artes Musicales", halign="center", bold=True, theme_text_color="Custom", text_color=(1, 1, 1, 1))
            banner.add_widget(titulo)
             
            # Zona que permitirá desplazamiento vertical
            scroll = MDScrollView()
    
            #PINTAMOS LA PANTALLA de inicio
    
            principal.add_widget(banner)
            principal.add_widget(scroll)
            
            self.add_widget(principal)