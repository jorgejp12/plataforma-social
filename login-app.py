from textual.app import App, ComposeResult 
from textual.containers import Vertical, Container, Horizontal
from textual.widgets import Input, Button, Label, TabbedContent, TabPane
from textual.screen import Screen
import re 
from conexiones import *   # Predefined credentials 
from plataforma_app import *


class LoginRegistrationScreen(App):
    CSS = """
    Screen {
    align: center middle;
    }

    #main_container {
        width: 50;
        height: 35;
        border: heavy white;
        background: black;
        padding: 2;
        align: center middle;
        content-align: center middle;
    }

    .input {
        width: 100%;
        margin-bottom: 1;
    }

    .button {
        width: 100%;
        margin-bottom: 1;
    }

    .message {
        color: yellow;
        text-align: center;
    }

    .tab-title {
        color: white;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():  # Contenedor principal en horizontal
            yield Container()  # Contenedor vacío a la izquierda (espaciador)

            with Container(id="main_container"):
                with TabbedContent():
                    with TabPane("Login", id="login_tab", classes="tab-title"):
                        yield Vertical(
                            Input(placeholder="Usuario", id="username_login", classes="input"),
                            Input(placeholder="Contraseña", password=True, id="password_login", classes="input"),
                            Button("Iniciar Sesión", id="login_btn", classes="button"),
                            Label("", id="login_message", classes="message")
                        )
                    
                    with TabPane("Registro", id="register_tab", classes="tab-title"):
                        yield Vertical(
                            Input(placeholder="Correo", id="email_register", classes="input"),
                            Input(placeholder="Nombre completo", id="fullname_register", classes="input"),
                            Input(placeholder="Contraseña", password=True, id="password_register", classes="input"),
                            Button("Registrar", id="register_btn", classes="button"),
                            Label("", id="register_message", classes="message")
                        )

            yield Container()  # Contenedor vacío a la derecha (espaciador)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "login_btn":
            usuario = self.query_one("#username_login", Input).value
            password = self.query_one("#password_login", Input).value
            login_message = self.query_one("#login_message", Label)
            
            if vericacion_users(usuario, password):
                cambiar_estado(usuario)
                login_message.update("✔️ Login exitoso")
                
                # Cerrar la pantalla actual de login
                self.push_screen(PlataformaApp(usuario,usuario, self.interfaz_visitar_perfil, self.cerra_sesion))
                # Iniciar la plataforma social
       
            else:
                login_message.update("❌ Usuario o contraseña incorrectos")

        elif event.button.id == "register_btn":
            email = self.query_one("#email_register", Input).value
            fullname = self.query_one("#fullname_register", Input).value
            password = self.query_one("#password_register", Input).value
            register_message = self.query_one("#register_message", Label)

            # Validar correo
            if not self.validar_correo(email):
                register_message.update("❌ Correo electrónico inválido")
                return

            # Intentar guardar usuario
            if save_usuarios(email, fullname, password):
                register_message.update(f"✔️ Registro exitoso: {email.split('@')[0]}")
            else:
                register_message.update("❌ Correo ya registrado")

    def validar_correo(self, email):
        """Verifica si el correo tiene un formato válido"""
        patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(patron, email))

   
    def interfaz_visitar_perfil(self, perfil, autor):
        self.pop_screen()
        self.push_screen(PlataformaApp(perfil,autor, self.interfaz_visitar_perfil, self.cerra_sesion))
    
    def cerra_sesion(self, usuario):
        cambiar_estado(usuario)

        self.pop_screen()

        self.query_one("#login_message", Label).update("✔️ Cerrado de sesión exitoso")

            
        
if __name__ == "__main__":
    LoginRegistrationScreen().run()