from datetime import datetime
from textual.app import App, ComposeResult
from post_widget import PublicacionWidget

class SocialMediaApp(App):
    """Aplicación de ejemplo con el sistema de comentarios."""
    
    def compose(self) -> ComposeResult:
        # Datos de usuario actual
        current_user = {
            'id': 'user_123',
            'name': 'Juan Pérez'
        }
        
        # Comentarios de ejemplo
        comentarios_ejemplo = [
            {
                'author': 'user_456',
                'author_name': 'María García',
                'text': '¡Interesante publicación!',
                'date': datetime.now().strftime("%Y-%m-%d %H:%M")
            },
            {
                'author': 'user_789',
                'author_name': 'Carlos López',
                'text': 'Estoy de acuerdo con tu punto de vista.',
                'date': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        ]
        
        # Crear publicación de ejemplo
        yield PublicacionWidget(
            pub_id="post_001",
            autor="Ana Martínez",
            contenido="Este es el contenido de mi publicación sobre el nuevo sistema de comentarios.",
            fecha=datetime.now().strftime("%Y-%m-%d"),
            current_user=current_user,
            likes=5,
            reacciones=['user_456', 'user_789'],
            comentarios=comentarios_ejemplo
        )

if __name__ == "__main__":
    app = SocialMediaApp()
    app.run()