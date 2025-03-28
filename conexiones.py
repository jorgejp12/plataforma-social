from conn_base import FirebaseDB
import logging
from uuid import uuid4
from checkpass import *
from datetime import datetime
path ="plataforma-social-247bc-firebase-adminsdk-fbsvc-ca73a47640.json"
url ="https://plataforma-social-247bc-default-rtdb.firebaseio.com/"

fb_db = FirebaseDB(path,url)

def save_usuarios(correo, nombre, password):
  usuario = correo.split("@")[0]
  if not fb_db.read_record(f'/users/{usuario}'):
    password = save_password(password)
    data_to_write ={
      "correo": correo,
      "nombre": nombre,
      "password": password,
      "estado":0
    }
    fb_db.write_record(f'/users/{usuario}', data_to_write)
    return True
  else:
    return False

def listar_gamers():
  jugadores = fb_db.read_record(f'/users')

  # Verificar si hay datos
  lista = {}
  if jugadores:
      for usuario, datos in jugadores.items():
          estado = datos.get("estado") # Obtener estado o mostrar "Desconocido" si no existe
          lista[usuario] = estado
      return lista
  else:
      return {}

def vericacion_users(usuario,password):
  result = fb_db.read_record(f'/users/{usuario}')
  return result and check_password(password, result["password"])

def cambiar_estado(usuario):
    """ Cambia el estado del usuario de 0 a 1 o de 1 a 0 """
    user_path = f"users/{usuario}/estado"
    estado_actual = fb_db.read_record(user_path)

    if estado_actual is None:
        print(f"Error: No se encontró el usuario '{usuario}' o el campo 'estado'.")
        return

    # Negar el estado (0 → 1, 1 → 0)
    nuevo_estado = 1 if estado_actual == 0 else 0

    # Actualizar el estado en Firebase
    fb_db.update_record(f"users/{usuario}", {"estado": nuevo_estado})

    print(f"Estado de '{usuario}' cambiado a {nuevo_estado}")
   
def cargar_publicaciones(id_user):
    publicaciones = fb_db.read_record("publicaciones") or {}  # Evita None si no hay datos
    usuarios = fb_db.read_record(f"users/{id_user}/post") or {}  # Evita None si no hay datos

    if not publicaciones:
        print("⚠️ No hay publicaciones disponibles.")
        return {}

    publicaciones_con_megusta = {}

    for post in usuarios:
        # Obtener lista de usuarios que han dado "me gusta"

        print(publicaciones[post].get("fecha", "Fecha no disponible"))
        if post in publicaciones:
          # Guardar datos en el diccionario
          publicaciones_con_megusta[post] = {
              "autor": publicaciones[post].get("autor", "Desconocido"),
              "contenido": publicaciones[post].get("contenido", "Sin contenido"),
              "fecha": publicaciones[post].get("fecha", "Fecha no disponible"),
              "likes":publicaciones[post].get("likes", 0),
              "reacciones": publicaciones[post].get("reacciones", []),  # Usuarios que dieron "me gusta"
              "comentarios": publicaciones[post].get("comentarios", [])
          }

    return publicaciones_con_megusta

def guardar_publicacion(id_usuario, contenido,autor):
    try:
        publicaciones = fb_db.read_record("publicaciones") or {}
        usuarios = fb_db.read_record("users") or {}  # Cargar usuarios

        # Generar un nuevo ID único para la publicación
        nuevo_post_id = f"post{len(publicaciones) + 1}"

        # Crear la nueva publicación
        publicaciones[nuevo_post_id] = {
            "autor": autor,
            "contenido": contenido,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "reacciones": [],
            "likes": 0,
            "comentarios": []
        }

        print(f"📌 Publicaciones antes de actualizar: {publicaciones}")  # Depuración

        # Guardar en la base de datos de publicaciones
        fb_db.update_record("publicaciones", publicaciones)

        # 🔹 Agregar el post al usuario correspondiente
        if id_usuario in usuarios:
            if "post" not in usuarios[id_usuario]:
                usuarios[id_usuario]["post"] = []
            usuarios[id_usuario]["post"].append(nuevo_post_id)
        else:
            usuarios[id_usuario] = {"post": [nuevo_post_id]}

        print(f"✅ Publicación guardada: {publicaciones[nuevo_post_id]}")  # Depuración

        # Guardar la actualización en la base de datos de usuarios
        fb_db.update_record("users", usuarios)

        return publicaciones[nuevo_post_id],nuevo_post_id  # Devuelve el post si se guardó correctamente
    except Exception as e:
        print(f"❌ Error al guardar publicación: {e}")
        return None  # Retorna None si hay un error

def actualizar_likes(pub_id,reacciones,likes):
    fb_db.update_record(f"publicaciones/{pub_id}", {
            "reacciones": reacciones,
            "likes": likes
    })

def guardar_comentario(pub_id: str, usuario_id: str, texto: str):
    """Guarda un comentario en la base de datos"""
    nuevo_comentario = {
        'autor': usuario_id,
        'texto': texto,
        'fecha': datetime.now().isoformat()
    }

    # Actualiza la base de datos con el nuevo comentario
    fb_db.update_record(f'publicaciones/{pub_id}/comentarios', nuevo_comentario)



"""
# Write data to the database
data_to_write = {
'name': 'jj',
'age': 27,
'email': 'jj@gmail.com'
}
fb_db.write_record('/users/jj', data_to_write)

# Read data from the database
result = fb_db.read_record('/users/toni')
print("Read Data:", result)

# Update data in the database
data_to_update = {
'age': 31
}
fb_db.update_record('/users/toni', data_to_update)

# Delete data from the database
fb_db.delete_record('/users/john_doe')

# Delete data from the database
fb_db.delete_record('/users/toni')

# to save a record with an unique id
ref = db.reference('users')
new_email_ref = ref.push()
new_email_ref.set({
    'name': 'Juan',
    'email': 'Juan@hotmail.com'
})

"""
