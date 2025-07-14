import streamlit as st
from db import get_connection
import pandas as pd

def obtener_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE estado = 'activo'")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado

def actualizar_usuario(id_usuario, nuevo_usuario, nuevo_rol):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE usuarios SET nombre_usuario = %s, rol = %s WHERE id = %s"
    cursor.execute(query, (nuevo_usuario, nuevo_rol, id_usuario))
    conn.commit()
    cursor.close()
    conn.close()

def main():
    st.title("Gestión de Usuarios")

    usuarios = obtener_usuarios()

    for user in usuarios:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        with col1:
            seleccionado = st.checkbox(f"{user['nombre_usuario']} ({user['rol']})", key=f"check_{user['id']}")
        with col2:
            st.write("ID:", user['id'])

        if seleccionado:
            with col3:
                if st.button("✏️ Editar", key=f"edit_{user['id']}"):
                    with st.form(f"edit_form_{user['id']}", clear_on_submit=False):
                        nuevo_usuario = st.text_input("Nuevo nombre de usuario", value=user['nombre_usuario'], key=f"nombre_{user['id']}")
                        nuevo_rol = st.selectbox("Nuevo rol", ['paciente', 'secretaria', 'asistente', 'doctor', 'admin'], index=['paciente', 'secretaria', 'asistente', 'doctor', 'admin'].index(user['rol']), key=f"rol_{user['id']}")
                        submitted = st.form_submit_button("Guardar cambios")
                        if submitted:
                            actualizar_usuario(user['id'], nuevo_usuario, nuevo_rol)
                            st.success("Usuario actualizado correctamente.")
                            st.rerun()
