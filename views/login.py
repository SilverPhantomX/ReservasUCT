from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
from views.calendario import AZUL
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, MDDialogSupportingText
from kivy.utils import get_color_from_hex
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from services.persistencia_sesion import guardar_sesion
from services.analytics_service import registrar_evento

AZUL = get_color_from_hex("#01568e")
GUINDA = get_color_from_hex("#7B1D35")

class LoginScreen(Screen):
    def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.layout = MDBoxLayout(orientation='vertical')   
            principal = MDBoxLayout(orientation="vertical") #layout de la app
            
            
            #banner de la app
            banner = MDBoxLayout(size_hint_y=None, height=dp(70), md_bg_color= AZUL) 
            #titulo del banner Nombre, aliniacion, color y agregacion al banner
            titulo = MDLabel(text="ReservasUCT", halign="center", bold=True, theme_text_color="Custom", text_color=(1, 1, 1, 1))
            banner.add_widget(titulo)
             
            # Zona que permitirá desplazamiento vertical
            scroll = MDScrollView()
    
            # Contenedor donde irá el formulario
            contenido = MDBoxLayout(orientation="vertical", 
                                    adaptive_height=True,
                                    size_hint_x=0.9,
                                    spacing=dp(15),
                                    padding=dp(20)
                                    )
            
            contenido.add_widget(MDButtonIcon(icon="account-circle",
                                              theme_text_color="Custom",
                                              text_color=(0.25, 0.25, 0.25, 1),
                                              pos_hint={"center_x": 0.5},
                                              theme_icon_color="Custom",
                                              icon_color=(0.25, 0.25, 0.25, 1),
                                              theme_font_size="Custom",
                                              font_size=dp(70)))
            
            self.campo_correo = MDTextField(MDTextFieldHintText(text="Correo"), mode="outlined")
            self.campo_contrasena = MDTextField(MDTextFieldHintText(text="Contraseña"), mode="outlined")

            contenido.add_widget(self.campo_correo)
            contenido.add_widget(self.campo_contrasena)
            
            contenedor_centro = MDAnchorLayout(anchor_x="center",anchor_y="center")
            
            contenedor_centro.add_widget(contenido)
            scroll.add_widget(contenedor_centro)
            

    
    
            # Panel inferior de navegación tamaño
            navegacion = MDBoxLayout(size_hint_y=None, height=dp(70), md_bg_color=AZUL)
            
            # Contenedores que dividen la navegación en 3 partes iguales
            zona_iniciar_sesion = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")
            zona_registrarse = MDAnchorLayout(size_hint_x=1, anchor_x="center", anchor_y="center")

            
            btn_inicio_sesion = MDButton(
                MDButtonIcon(icon="home", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
                MDButtonText(text="iniciar sesion", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
                style="text", size_hint=(None, None),
                on_release=self.iniciar_sesion
            )
            btn_registrarse = MDButton(
                MDButtonIcon(icon="account-plus", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
                MDButtonText(text="Registrarse", theme_text_color="Custom", text_color=(1, 1, 1, 1)),
                style="text", size_hint=(None, None),
                on_release=lambda x: setattr(self.manager, 'current', 'registro')
            )
            
            
            # Agregamos los botones a sus respectivas zonas
            zona_iniciar_sesion.add_widget(btn_inicio_sesion)
            zona_registrarse.add_widget(btn_registrarse)
            
            navegacion.add_widget(zona_iniciar_sesion)
            navegacion.add_widget(zona_registrarse)
            
            #PINTAMOS LA PANTALLA de login
            
            principal.add_widget(banner)
            principal.add_widget(scroll)
            principal.add_widget(navegacion)
            
            self.add_widget(principal)
            
    def iniciar_sesion(self, *args):
        app = MDApp.get_running_app()
        
        

        correo = self.campo_correo.text.strip()
        contrasena = self.campo_contrasena.text

        for usuario in app.gestor_usuarios.usuarios:

            if (usuario.correo == correo and usuario.contrasena == contrasena):
                
                app.usuario_actual = usuario
                registrar_evento("login_exitoso", {"correo": usuario.correo, "rol": usuario.rol})
                
                guardar_sesion(usuario)

                print(f"Sesión iniciada: {usuario.nombre}")
                self.manager.current = "calendario"
                return
            
        registrar_evento( "login_fallido", {"correo": correo})
        self.mostrar_dialogo("Error", "Correo o contraseña incorrectos.")
        
    def mostrar_dialogo(self, titulo, texto):
        contenedor = MDDialogButtonContainer()

        contenedor.add_widget(MDButton(MDButtonText(text="ENTENDIDO"),
                                       style="text",
                                       on_release=self.cerrar_dialogo))

        self.dialog = MDDialog(MDDialogHeadlineText(text=titulo),
                               MDDialogSupportingText(text=texto),
                               contenedor)

        self.dialog.open()


    def cerrar_dialogo(self, *args):
        self.dialog.dismiss()