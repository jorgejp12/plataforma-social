import hashlib
import os

# Salt fijo (debería ser único por usuario en un sistema real)
FIXED_SALT = b"\xa9\xd3\x0f\x8b\x12\xcd\xab\xf7\x98\x7e\x21\x94\x3c\xf5\xaa\xbb\xcc\xdd\xee\xff\x11\x22\x33\x44\x55\x66\x77\x88"

def save_password(password):
    """Hashea la contraseña con PBKDF2 y devuelve el hash en formato hexadecimal"""
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), FIXED_SALT, 100000)
    return password_hash.hex()  # Convertir a hexadecimal para fácil almacenamiento

def check_password(password, password_guardada):
    """Verifica si la contraseña ingresada coincide con el hash almacenado"""
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), FIXED_SALT, 100000)
    return password_hash.hex() == password_guardada  # Comparar los hashes en formato hex


