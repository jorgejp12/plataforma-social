from textual.widgets import Button, Static
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical,Container
from textual.style import Style
from conexiones import *
from comentario_widget import CommentBox

class PublicacionWidget(Container):
    def __init__(self, pub_id: str, autor: str, contenido: str, fecha: str, 
                 likes: int = 0, comentarios: int = 0, 
                 reacciones: list = None, id_usuario: str = None):
        self.pub_id = pub_id
        self.autor = autor
        self.contenido = contenido
        self.fecha = fecha
        self.likes = likes
        self.comentarios = comentarios
        self.reacciones = reacciones
        self.id_usuario = id_usuario
        super().__init__(id=f"pub_{pub_id}")

    def compose(self) -> ComposeResult:
        # Encabezado con autor y fecha
        with Container():

            yield Static(f"Autor: {self.autor.ljust(50, " ")}{self.fecha}")
            yield Static()

            # Contenido de la publicación
            yield Static(self.contenido)

            # Acciones (me gusta, comentarios)
            with Horizontal():
                if self.id_usuario in self.reacciones:
                    ml = " Me gusta"
                else:
                    ml= ""
                like_btn = Button(
                    f"{self.likes}👍{ml}", 
                    id=f"btn-megusta", 
                )
                yield like_btn

                # Botón de comentarios
                comment_btn = Button(
                    f"💬 {self.comentarios}", 
                    id=f"btn-comentar_{self.pub_id}", 
                )
                yield comment_btn


    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn-megusta":
            # Verificar si el usuario actual ya dio like
            if self.id_usuario in self.reacciones:
                # Si ya dio like, remover like
                self.reacciones.remove(self.id_usuario)
                self.likes -= 1
                event.button.label = f" {self.likes} 👍"
            else:
                # Si no había dado like, agregar like
                self.reacciones.append(self.id_usuario)
                self.likes += 1
                event.button.label = f" {self.likes} 👍 Me gusta"
            
            # Aquí deberías actualizar la base de datos
            self._actualizar_megusta()
        
        elif event.button.id == f"btn-comentar_{self.pub_id}":
            # Lógica para comentarios
            print("Abrir comentarios")
            self.toggle_class()
    
    def toggle_comments(self):
        """Muestra/oculta la caja de comentarios."""
        if self.showing_comments:
            # Ocultar comentarios
            comments_box = self.query_one("#comments-box", None)
            if comments_box:
                comments_box.remove()
            self.showing_comments = False
        else:
            # Mostrar comentarios
            comments_box = CommentBox(
                pub_id=self.pub_id,
                comments=self.comentarios_data,
                user_id=self.id_usuario,
                id="comments-box"
            )
            self.mount(comments_box)
            self.showing_comments = True

    def _actualizar_megusta(self):
        """
        Método para actualizar el estado de 'Me gusta' en la base de datos
        """        
        # Actualizar en Firebase
        actualizar_likes(self.pub_id,self.reacciones,self.likes)
if __name__ == "__main__":
    from textual.app import App
    from textual.containers import Vertical

    class TestApp(App):
        def compose(self):
            # Crear instancias de PublicacionWidget con diferentes datos de prueba
            pub1 = PublicacionWidget(pub_id="1", autor="Alice", contenido="Hola, mundo!", fecha="2025-03-28", likes=3, comentarios=2, reacciones=["user1"], id_usuario="user2")
            pub2 = PublicacionWidget(pub_id="2", autor="Bob", contenido="Texto de prueba", fecha="2025-03-28", likes=5, comentarios=1, reacciones=["user2"], id_usuario="user2")
            
            with Vertical():
                yield pub1
                yield pub2

    TestApp().run()