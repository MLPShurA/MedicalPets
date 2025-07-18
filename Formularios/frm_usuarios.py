import streamlit as st
import mysql.connector
from db import get_connection
from Login.security import hash_password

# Función para generar la contraseña automática
def generar_contrasena(nombres, apellidos, cedula):
    parte_nombre = nombres[:3].lower()
    parte_apellido = apellidos[:3].lower()
    parte_cedula = cedula[-3:]
    return parte_nombre + parte_apellido + parte_cedula

# Formulario de nuevo usuario o edición
def formulario_nuevo_usuario(usuario_data=None):
    st.subheader("Registro de Usuarios")

    if 'usuario_registrado_exito' not in st.session_state:
        st.session_state['usuario_registrado_exito'] = False

    if st.session_state['usuario_registrado_exito']:
        st.success("")
        st.markdown('<div style="color:#111; font-size:1.1rem; font-weight:bold; margin-top:-2.5em; margin-bottom:1.5em;">Usuario registrado exitosamente</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Registrar otro usuario", key="registrar_otro_usuario_btn"):
                st.session_state['usuario_registrado_exito'] = False
                st.session_state['usuario_editar'] = None
                st.rerun()
        with col2:
            if st.button("Volver al listado", key="volver_listado_btn"):
                st.session_state['mostrar_formulario_usuario'] = False
                st.session_state['usuario_editar'] = None
                st.session_state['usuario_registrado_exito'] = False
                st.rerun()
    else:
        nombres = st.text_input("Nombres", value=usuario_data.get('nombres') if usuario_data else "")
        apellidos = st.text_input("Apellidos", value=usuario_data.get('apellidos') if usuario_data else "")
        cedula = st.text_input("Cédula", value=usuario_data.get('cedula') if usuario_data else "")
        telefono = st.text_input("Teléfono", value=usuario_data.get('telefono') if usuario_data else "")
        correo = st.text_input("Correo electrónico", value=usuario_data.get('correo_electronico') if usuario_data else "")
        direccion = st.text_input("Dirección", value=usuario_data.get('direccion') if usuario_data else "")
        rol = st.selectbox("Rol", ["paciente", "secretaria", "doctor", "veterinario"],
                           index=["paciente", "secretaria", "doctor", "veterinario"].index(usuario_data.get('rol')) if usuario_data else 0)

        if st.button("Guardar", key="guardar_usuario_btn"):
            if not nombres or not apellidos or not cedula or not correo:
                st.warning("")
                if usuario_data:
                    st.markdown('<div style="color:#111; font-size:1.1rem; font-weight:bold; margin-top:-2.5em; margin-bottom:1.5em;">Error al editar usuario</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="color:#111; font-size:1.1rem; font-weight:bold; margin-top:-2.5em; margin-bottom:1.5em;">Error al guardar usuario, revise los campos</div>', unsafe_allow_html=True)
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()

                if usuario_data:  # 📝 Modo edición
                    query_update_detalle = """
                        UPDATE usuarios_detalle 
                        SET nombres=%s, apellidos=%s, cedula=%s, telefono=%s, correo_electronico=%s, direccion=%s 
                        WHERE id=%s
                    """
                    values_detalle = (nombres, apellidos, cedula, telefono, correo, direccion, usuario_data['detalle_id'])
                    cursor.execute(query_update_detalle, values_detalle)

                    query_update_usuarios = "UPDATE usuarios SET rol=%s WHERE id=%s"
                    cursor.execute(query_update_usuarios, (rol, usuario_data['usuario_id']))

                    st.success("✅ Usuario actualizado exitosamente.")

                else:  # 🆕 Modo nuevo
                    contrasena = generar_contrasena(nombres, apellidos, cedula)
                    contrasena_hashed = hash_password(contrasena)

                    query_usuarios = """
                        INSERT INTO usuarios (nombre_usuario, contrasena, contrasena_hash, rol)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query_usuarios, (correo, contrasena, contrasena_hashed, rol))
                    usuario_id = cursor.lastrowid

                    query_detalle = """
                        INSERT INTO usuarios_detalle 
                        (nombres, apellidos, cedula, telefono, correo_electronico, direccion, usuario_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query_detalle, (nombres, apellidos, cedula, telefono, correo, direccion, usuario_id))

                    st.session_state['usuario_registrado_exito'] = True
                    st.success("")
                    st.markdown('<div style="color:#111; font-size:1.1rem; font-weight:bold; margin-top:-2.5em; margin-bottom:1.5em;">Usuario registrado exitosamente</div>', unsafe_allow_html=True)
                    # No cambiar mostrar_formulario_usuario ni hacer rerun aquí

                conn.commit()
                cursor.close()
                conn.close()

            except Exception as e:
                st.error(f"❌ Error: {e}")

        if st.button("Volver al listado", key="volver_listado_btn"):
            st.session_state['mostrar_formulario_usuario'] = False
            st.session_state['usuario_editar'] = None
            st.rerun()
