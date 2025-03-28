from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Button, Static, Input, Label
from textual.screen import Screen
from conexiones import *
from collections.abc import Generator
from post_widget import *

class PlataformaApp(Screen):
    CSS = """
    Screen {
        background: rgb(20, 20, 40);
        color: white;
    }

    .columna {
        border: tall $surface-lighten-2;
        background: $surface-darken-1;
        padding: 1;
        width: 20%;
        height: 100%;
        overflow-y: auto;
    }

    .columna-60 {
        border: tall $surface-lighten-2;
        background: $surface-darken-1;
        padding: 1;
        width: 60%;
        height: 100%;
        overflow-y: auto;
    }

    .titulo {
        text-align: center;
        color: $text-muted;
        text-style: bold underline;
        margin-bottom: 1;
    }

    .boton {
        width: 100%;
        text-align: left;
        margin-bottom: 1;
        padding: 1;
        background: $surface;
        border: none;
    }

    .boton:hover {
        background: $surface-lighten-1;
    }

    #post-input {
        margin-bottom: 1;
        width: 100%;
        border: none;           /* Asegura que el Input no tenga bordes extraños */
        background: $surface;   /* Fondo consistente */
    }

    #post-input:focus {
        border: none;           /* Elimina el borde al enfocar */
    }

    #post-btn {
        width: 100%;
        text-align: center;
        background: $success;
        color: $text;
    }

    #post-btn:hover {
        background: $success-darken-1;
    }

    #feedback {
        text-align: center;
        margin-top: 1;
    }
    """

    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        super().__init__()

    def compose(self) -> ComposeResult:
        usuarios = listar_gamers()
        publicaciones = cargar_publicaciones(self.id_usuario)

        with Horizontal():
            # Sección de Usuarios (Columna Izquierda)
            with Vertical(classes="columna"):
                yield Static("🎮 Jugadores Conectados")
                yield from self._crear_lista_usuarios(usuarios)

            # Sección de Publicaciones (Columna Central)
            with Vertical(classes="columna-60"):
                yield Static("📢 Últimas Publicaciones")
                yield from self._crear_seccion_publicacion()
                with Container():  
                    with Vertical():
                        yield from self._crear_lista_publicaciones(publicaciones)

    def _crear_lista_usuarios(self, usuarios: dict) -> Generator:
        for user_id, status in usuarios.items():
            if user_id != self.id_usuario:
                estado = "🟢" if status == 1 else "🔴"
                texto = f"👤 {user_id} {estado}"
                yield Button(texto, id=f"user_{user_id}")

    def _crear_seccion_publicacion(self) -> Generator:
        yield Input(
            placeholder="✏️ Escribe tu publicación (máx 300 caracteres)", 
            id="post-input",
            max_length=300  # Limita automáticamente a 300 caracteres
        )
        yield Button("📤 Publicar", id="post-btn")
        yield Label("", id="feedback")

    def _crear_lista_publicaciones(self, publicaciones: dict) -> Generator:
        for pub_id, post in publicaciones.items():
            publicacion = PublicacionWidget(
                pub_id=pub_id,
                autor=post.get("autor", "Anónimo"),
                contenido=post.get("contenido", "Sin contenido"),
                fecha=post.get("fecha", "Fecha desconocida"),
                likes=len(post.get("reacciones", [])),
                comentarios=len(post.get("comentarios", [])),
                reacciones=post.get("reacciones", []),
                id_usuario=self.id_usuario
            )
            yield publicacion

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "post-btn":
            input_widget = self.query_one("#post-input", Input)
            contenido = input_widget.value.strip()

            if not contenido:
                self.query_one("#feedback", Label).update("❌ ¡El mensaje no puede estar vacío!")
                return

            if len(contenido) > 300:
                self.query_one("#feedback", Label).update("❌ ¡Máximo 300 caracteres!")
                return

            nueva_publicacion = guardar_publicacion(self.id_usuario, contenido)
            if nueva_publicacion:
                self.query_one("#feedback", Label).update(f"✅ Publicado: '{contenido[:20]}...'")
                input_widget.value = ""  # Limpiar el input

class MiAplicacion(App):
    def on_mount(self):
        self.push_screen(PlataformaApp("leon_123"))

if __name__ == "__main__":
    MiAplicacion().run()