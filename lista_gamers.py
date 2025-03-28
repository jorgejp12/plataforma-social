from textual.app import App, ComposeResult
from textual.widgets import Button, Static

def lista_usuarios():
    return {
        "12": ["jfleong6", 1],
        "1": ["jfleg6", 0],
    }

class ButtonApp(App):
    def compose(self) -> ComposeResult:
        usuarios = lista_usuarios()
        self.label = Static("Usuarios", id="info_label")
        yield self.label

        for user_id, (username, status) in usuarios.items():
            est = "🟢" if status == 1 else "🔴"
            texto = f"ID: {user_id} \n {username} {est}"
            yield Button(texto, id=f"user_{user_id}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.label.update(f"¡Botón {event.button.id} presionado!")

if __name__ == "__main__":
    ButtonApp().run()
