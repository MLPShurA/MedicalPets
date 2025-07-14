import streamlit_authenticator as stauth
from db import get_connection  # Asegúrate de tener este archivo implementado correctamente

def cargar_usuarios_desde_db():
    # Conectar a la base de datos
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener usuarios con contraseña definida
    cursor.execute("SELECT * FROM usuarios WHERE contrasena_hash IS NOT NULL")
    usuarios = cursor.fetchall()

    # Cerrar conexión
    cursor.close()
    conn.close()

    # Construir el diccionario requerido por streamlit_authenticator
    usuarios_dict = {
        'usernames': {}
    }

    for user in usuarios:
        username = user['nombre_usuario']
        usuarios_dict['usernames'][username] = {
            'name': username,
            'password': user['contrasena_hash'],  # Se asume que ya está hasheada
            'email': user['nombre_usuario'],      # Si no tienes email, puedes usar el nombre de usuario
            'rol': user['rol']
        }

    # Configuración sin el parámetro deprecated
    config = {
        'credentials': usuarios_dict,
        'cookie': {
            'name': 'furryfriends_cookie',
            'key': 'clave_secreta123456',  # Cambia por una clave segura
            'expiry_days': 30
        }
    }

    return config
