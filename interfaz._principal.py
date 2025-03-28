from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Static, Input, Label
from lista_gamers import lista_usuarios
from publicaciones import cargar_publicaciones

class PlataformaApp(App):
    CSS = """
    .columna {
        border: solid white;
        padding: 1;
        width: 20%;
    }
    .columna-60 {
        border: solid white;
        padding: 1;
        width: 60%;
    }
    .boton {
        width: 90%;
        text-align: left;
    }
    """

    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        super().__init__()  # Llamada correcta a la superclase


    def compose(self) -> ComposeResult:
        usuarios = lista_usuarios()
        publicaciones = cargar_publicaciones()

        with Horizontal():
            # Sección de Usuarios (Izquierda)
            with Vertical(classes="columna"):
                yield Static("🎮 Jugadores", classes="titulo")
                for user_id, (username, status) in usuarios.items():
                    est = "🟢" if status == 1 else "🔴"
                    texto = f"ID: {user_id}\n{username} {est}"
                    yield Button(texto, id=f"user_{user_id}", classes="boton")

            # Sección de Publicaciones (Centro)
            with Vertical(classes="columna-60"):
                yield Static("📢 Publicaciones", classes="titulo")
                yield Input(placeholder="Escribe tu publicación (300 chars max)", id="post-input")
                yield Button("Publicar", id="post-btn")
                yield Label("", id="feedback")
                
                for pub_id, (texto, reacciones , ids) in publicaciones.items():
                    emoji = "👍" if self.id_usuario in ids else "🤙"
                    texto_publicacion = f"{texto}\n{emoji} {reacciones}"
                    boton = Button(texto_publicacion, id=pub_id, classes="boton")
                    yield boton

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.log("hola")
        if event.button.id.startswith("pub_"):
            
            pub_id = event.button.id[4:]  # Remueve "pub_"
            publicaciones = cargar_publicaciones()  # Volvemos a cargar las publicaciones
            texto,reacciones, ids = publicaciones[event.button.id]
            if self.id_usuario not in ids:
                reacciones += -1
                event.button.label = f"{texto}\n 🤙 {reacciones}"

            else:
                reacciones += +1
                event.button.label = f"{texto}\n 🤙 {reacciones}"

        elif event.button.id == "post-btn":
            input_widget = self.query_one("#post-input", Input)
            contenido = input_widget.value
            if len(contenido)<=300:
                self.query_one("#feedback", Label).update(f"✅ Publicado: '{contenido[:20]}...'")
                input_widget.value = ""  # Limpiar el input
            else:
                self.query_one("#feedback", Label).update("❌ ¡Máximo 300 caracteres!")
        else:
            self.query_one(".titulo").update(f"¡Usuario {event.button.id} seleccionado!")

if __name__ == "__main__":
    PlataformaApp(2).run()
