from textual.widgets import Button, Static, Input
from textual.containers import Vertical, Horizontal, Container
from textual.app import ComposeResult
from conexiones import *
class CommentBox(Container):
    """Widget para mostrar y agregar comentarios a una publicación."""
    
    def __init__(self, pub_id: str, comments: list, user_id: str, autor: str, id: str = None):  # Agregamos id como parámetro opcional
        self.pub_id = pub_id
        self.comments_data = comments or []
        self.user_id = user_id
        self.autor = autor
        super().__init__(id=id, classes="comments-box_")  # Pasamos el id al padre
    
    def compose(self) -> ComposeResult:
        # Área para mostrar comentarios existentes
        with Vertical(id="comments-list"):
            for comment in self.comments_data:
                yield Static(f"{comment['autor']}: {comment['texto']}")
        
        # Área para agregar nuevo comentario

        yield Input(
            placeholder="Escribe tu comentario...",
            id="comment-input"
        )
        yield Button("💬 Comentar", id="comment-btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "comment-btn":
            input_widget = self.query_one("#comment-input", Input)
            comment_text = input_widget.value.strip()
            
            if not comment_text:
                return
            
            # Guardar en la base de datos
            guardar_comentario(self.pub_id, self.autor, comment_text)
            
            # Agregar el comentario a la lista de comentarios visualmente
            new_comment = Static(f"Usuario {self.user_id}: {comment_text}")
            comments_list = self.query_one("#comments-list", Vertical)
            comments_list.mount(new_comment)  # Agrega el comentario al contenedor
            
            # Limpiar el input después de comentar
            input_widget.value = ""