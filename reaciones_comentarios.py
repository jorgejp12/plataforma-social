import json
from datetime import datetime

# Datos iniciales (como ejemplo)
data = {
    "usuarios": {
        "gamerx@example.com": {
            "nombre": "GamerX",
            "amigos": ["player2@example.com"],
            "publicaciones": ["post1"]
        },
        "player2@example.com": {
            "nombre": "Player2",
            "amigos": ["gamerx@example.com"],
            "publicaciones": ["post2"]
        }
    },
    "publicaciones": {
        "post1": {
            "autor": "gamerx@example.com",
            "contenido": "¡Subí a Diamante en LoL!",
            "fecha": "2025-03-26 14:30",
            "reacciones": 5,
            "comentarios": [
                {
                    "autor": "player2@example.com",
                    "contenido": "¡Felicidades!",
                    "fecha": "2025-03-26 14:35"
                }
            ]
        },
        "post2": {
            "autor": "player2@example.com",
            "contenido": "Busco equipo para Valorant",
            "fecha": "2025-03-26 15:00",
            "reacciones": 3,
            "comentarios": []
        }
    }
}

# Función para agregar una reacción a una publicación
def agregar_reaccion(post_id):
    if post_id in data["publicaciones"]:
        data["publicaciones"][post_id]["reacciones"] += 1
        print(f"Reacción añadida a la publicación {post_id}. Total de reacciones: {data['publicaciones'][post_id]['reacciones']}")
    else:
        print(f"La publicación con ID {post_id} no existe.")

# Función para agregar un comentario a una publicación
def agregar_comentario(post_id, usuario_email, contenido_comentario):
    if post_id in data["publicaciones"]:
        comentario = {
            "autor": usuario_email,
            "contenido": contenido_comentario,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        data["publicaciones"][post_id]["comentarios"].append(comentario)
        print(f"Comentario añadido a la publicación {post_id}. Total de comentarios: {len(data['publicaciones'][post_id]['comentarios'])}")
    else:
        print(f"La publicación con ID {post_id} no existe.")

# Función para mostrar los comentarios de una publicación
def mostrar_comentarios(post_id):
    if post_id in data["publicaciones"]:
        print(f"Comentarios para la publicación {post_id}:")
        for comentario in data["publicaciones"][post_id]["comentarios"]:
            print(f"{comentario['autor']} dijo: {comentario['contenido']} (Fecha: {comentario['fecha']})")
    else:
        print(f"La publicación con ID {post_id} no existe.")

# Función para mostrar el menú y pedir la opción
def menu():
    while True:
        print("\n--- Menú de Opciones ---")
        print("1. Agregar una reacción a una publicación")
        print("2. Agregar un comentario a una publicación")
        print("3. Ver los comentarios de una publicación")
        print("4. Salir")
        
        opcion = input("Selecciona una opción (1/2/3/4): ")

        if opcion == "1":
            post_id = input("Ingresa el ID de la publicación (ej. post1, post2): ")
            agregar_reaccion(post_id)
        elif opcion == "2":
            post_id = input("Ingresa el ID de la publicación (ej. post1, post2): ")
            usuario_email = input("Ingresa tu correo (ej. gamerx@example.com): ")
            comentario = input("Escribe tu comentario: ")
            agregar_comentario(post_id, usuario_email, comentario)
        elif opcion == "3":
            post_id = input("Ingresa el ID de la publicación (ej. post1, post2): ")
            mostrar_comentarios(post_id)
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida, por favor elige de nuevo.")

# Ejecutar el menú
menu()