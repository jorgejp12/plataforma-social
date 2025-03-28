import bcrypt

# Función para hashear una contraseña
def hash_password(password):
    salt = bcrypt.gensalt()  # Genera una sal aleatoria
    hashed_password = bcrypt.hashpw(password.encode(), salt)  # Hashea la contraseña
    return hashed_password

# Función para verificar la contraseña
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password)

# Ejemplo de uso
password = "MiContraseñaSegura123"
hashed_pw = hash_password(password)
print(f"Contraseña hasheada: {hashed_pw}")

# Verificación
print("¿La contraseña es correcta?", check_password("MiContraseñaSegura123", hashed_pw))
print("¿La contraseña es incorrecta?", check_password("OtraContraseña", hashed_pw))
