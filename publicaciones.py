from textual.app import App, ComposeResult
from textual.widgets import Button, Static

# Nueva función con IDs corregidos
def cargar_publicaciones():
    return {
        "101": ["Hoy es un gran día para programar!", 9, [1,2,3,5]],
        "102": ["Python es increíble para desarrollo rápido.",9, [1]],
        "103": ["¿Cuál es tu lenguaje de programación favorito?",9, [1,5]],
        "104": ["Textual facilita la creación de interfaces en terminal.",9, [5]],
        "105": ["Estoy aprendiendo a usar IA en mis proyectos.",9, [2,3]]
    }

class PublicacionesApp(App):
    CSS = """
    .boton {
        margin: 1;
        width: 30%;
        text-align: left;
    }
    """

    def compose(self) -> ComposeResult:
        self.publicaciones = cargar_publicaciones()

        yield Static("📢 Publicaciones 📢", classes="titulo")

        for pub_id, (texto, emoji, reacciones) in self.publicaciones.items():
            texto_publicacion = f"{texto}\n{emoji} {reacciones}"
            print(texto)
            boton = Button(texto_publicacion, id=pub_id)
            boton.add_class("boton")  # Aplicar clase CSS
            yield boton

    def on_button_pressed(self, event: Button.Pressed) -> None:
        pub_id = event.button.id
        self.publicaciones[pub_id][2] += 1  # Incrementar contador de reacciones
        texto, emoji, reacciones = self.publicaciones[pub_id]
        event.button.label = f"{texto}\n{emoji} {reacciones}"

if __name__ == "__main__":
    PublicacionesApp().run()
