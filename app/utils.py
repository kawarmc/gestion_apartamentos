import re

def validar_contraseña(contraseña):
    """
    Verifica si una contraseña cumple con los requisitos de seguridad.
    """
    if len(contraseña) < 8:
        return "La contraseña debe tener al menos 8 caracteres."
    if not any(char.isupper() for char in contraseña):
        return "La contraseña debe contener al menos una letra mayúscula."
    if not any(char.islower() for char in contraseña):
        return "La contraseña debe contener al menos una letra minúscula."
    if not any(char.isdigit() for char in contraseña):
        return "La contraseña debe contener al menos un número."
    if not any(char in "!@#$%^&*()-_=+[]{};:,.<>?/|`~" for char in contraseña):
        return "La contraseña debe contener al menos un carácter especial."
    return None
