from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Label

class InputApp(App):
    """App básica con un input y botón para capturar texto"""
    
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Escribe tu publicación (300 chars max)", id="post-input")
        yield Button("Publicar", id="post-btn")
        yield Label("", id="feedback")

    def on_button_publicar(self, event: Button.Pressed) -> None:
        if event.button.id == "post-btn":
            input_widget = self.query_one("#post-input", Input)
            contenido = input_widget.value
            
            if len(contenido) > 300:
                self.query_one("#feedback", Label).update("❌ ¡Máximo 300 caracteres!")
            else:
                self.query_one("#feedback", Label).update(f"✅ Publicado: '{contenido[:20]}...'")
                input_widget.value = ""  # Limpiar el input

if __name__ == "__main__":
    app = InputApp()
    app.run()
