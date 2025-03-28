from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Button, Static, Input, Label
from textual.screen import Screen
from conexiones import *
from collections.abc import Generator
from post_widget1 import *
from textual.timer import Timer


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
        border: none;
        background: $surface;
    }

    #post-input:focus {
        border: none;
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

    PublicacionWidget {

        border: solid $accent;
        height: 80vh;
        overflow-y: auto;
    }
    .comments-box {
        height: 30vh;
        overflow-y: auto;      /* Scroll vertical si el contenido excede */
    }
    """

    def __init__(self, id_usuario, id_usuario_v):

        self.id_usuario = id_usuario
        self.id_usuario_v = id_usuario_v
        self.timer_actualizar: Timer | None = None  # Inicializa el temporizador
        super().__init__()

    def compose(self) -> ComposeResult:
        """Configura el temporizador para actualizar publicaciones cada 10 segundos"""
        self.timer_actualizar = self.set_interval(5.0, self._actualizar_publicaciones)  # Ejecutar cada 10s

        usuarios = listar_gamers()
        self.publicaciones = cargar_publicaciones(self.id_usuario)

        with Horizontal():
            # Sección de Usuarios (Columna Izquierda)
            with Vertical(classes="columna"):
                yield Static("🎮 Jugadores Conectados", classes="titulo")
                yield from self._crear_lista_usuarios(usuarios)

            # Sección de Publicaciones (Columna Central)
            with Vertical(classes="columna-60", id="contenedor-publicaciones"):
                yield Static("📢 Últimas Publicaciones", classes="titulo")
                yield from self._crear_seccion_publicacion()
   
                yield from self._crear_lista_publicaciones(self.publicaciones)
    async def _actualizar_publicaciones(self) -> None:
        """Agrega solo las publicaciones nuevas sin borrar las existentes."""
        nuevas_publicaciones = cargar_publicaciones(self.id_usuario)
        contenedor = self.query_one("#contenedor-publicaciones")

        # Comparar publicaciones anteriores con las nuevas
        for pub_id, post in sorted(nuevas_publicaciones.items(), key=lambda x: x[1].get('fecha', ''), reverse=True):
            if pub_id not in self.publicaciones:  # Solo agregar si es nueva
                publicacion = PublicacionWidget(
                    pub_id=pub_id,
                    autor=post['autor'],
                    contenido=post['contenido'],
                    fecha=post['fecha'],
                    likes=post.get('likes', 0),
                    comentarios=post.get('comentarios', 0),
                    reacciones=post.get('reacciones', []),
                    id_usuario=self.id_usuario
                )
                contenedor.mount(publicacion, before=contenedor.children[4] if contenedor.children else None)

        # Actualizar el estado de publicaciones almacenadas
        self.publicaciones = nuevas_publicaciones

    def _crear_lista_usuarios(self, usuarios: dict) -> Generator:
        """Genera la lista de usuarios conectados"""
        for user_id, status in usuarios.items():
            if user_id != self.id_usuario:
                estado = "🟢" if status == 1 else "🔴"
                texto = f"👤 {user_id} {estado}"
                yield Button(texto, id=f"user_{user_id}", classes="boton")

    def _crear_seccion_publicacion(self) -> Generator:
        """Crea la sección para escribir nuevas publicaciones"""
        yield Input(
            placeholder="✏️ Escribe tu publicación (máx 300 caracteres)", 
            id="post-input"
        )
        yield Button("📤 Publicar", id="post-btn", classes="boton")
        yield Label("", id="feedback")

    def _crear_lista_publicaciones(self, publicaciones: dict) -> Generator:
        """Genera la lista de publicaciones existentes"""
        if not publicaciones:
            yield Static("📭 No hay publicaciones aún. ¡Sé el primero en publicar!", 
                        classes="mensaje-vacio")
            return
            
        for pub_id, post in sorted(publicaciones.items(), 
                                key=lambda x: x[1].get('fecha', ''), 
                                reverse=True):
            # Verificar si los campos esenciales existen
            if not all(key in post for key in ['autor', 'contenido', 'fecha']):
                continue
             
            publicacion = PublicacionWidget(
                pub_id=pub_id,
                autor=post['autor'],
                contenido=post['contenido'],
                fecha=post['fecha'],
                likes=post.get('likes', 0),
                comentarios=post.get('comentarios', 0),
                reacciones=post.get('reacciones', []),
                id_usuario=self.id_usuario
            )
            yield publicacion
     

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja los eventos de los botones"""
        if event.button.id == "post-btn":
            self._manejar_publicacion()
        elif event.button.id.startswith("user_"):
            user_id = event.button.id[5:]
            self.notify(f"Usuario seleccionado: {user_id}")

    def _manejar_publicacion(self):
        """Maneja la creación de nuevas publicaciones"""
        input_widget = self.query_one("#post-input", Input)
        contenido = input_widget.value.strip()

        if not contenido:
            self.query_one("#feedback", Label).update("❌ ¡El mensaje no puede estar vacío!")
            return

        if len(contenido) > 300:
            self.query_one("#feedback", Label).update("❌ ¡Máximo 300 caracteres!")
            return

        # Guardar publicación
        nueva_publicacion,id_post = guardar_publicacion(self.id_usuario, contenido, self.id_usuario_v)
        
        if nueva_publicacion:
            self.query_one("#feedback", Label).update(f"✅ Publicado: '{contenido[:20]}...'")
            input_widget.value = ""
            
            # Añadir la nueva publicación al inicio
            contenedor = self.query_one("#contenedor-publicaciones")
            contenedor.mount(
                PublicacionWidget(
                    pub_id=id_post,
                    autor=self.id_usuario_v,
                    contenido=contenido,
                    fecha=nueva_publicacion["fecha"],
                    likes=0,
                    comentarios=[],
                    reacciones=[],
                    id_usuario=self.id_usuario
                ),
                before=contenedor.children[4] if contenedor.children else None
            )
            self.publicaciones = cargar_publicaciones(self.id_usuario)

    
class MiAplicacion(App):
    """App principal que maneja las pantallas"""

    def on_mount(self):
        self.push_screen(PlataformaApp("leon_123l", "jfleong6"))

if __name__ == "__main__":
    MiAplicacion().run()