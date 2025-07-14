import streamlit as st
from db import get_connection
from Formularios.frm_usuarios import formulario_nuevo_usuario

def eliminar_usuario(usuario_id, detalle_id, nombre):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM usuarios_detalle WHERE id = %s", (detalle_id,))
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
        conn.commit()

        cursor.close()
        conn.close()

        st.success(f"✅ Usuario '{nombre}' eliminado exitosamente.")
    except Exception as e:
        st.error(f"Error al eliminar usuario: {e}")

def main():
    st.title("Listado de Usuarios")

    if 'mostrar_formulario_usuario' not in st.session_state:
        st.session_state['mostrar_formulario_usuario'] = False
    if 'usuario_editar' not in st.session_state:
        st.session_state['usuario_editar'] = None
    if 'usuario_confirmar_eliminar' not in st.session_state:
        st.session_state['usuario_confirmar_eliminar'] = None

    if not st.session_state['mostrar_formulario_usuario']:
        if st.button("➕ Nuevo"):
            st.session_state['mostrar_formulario_usuario'] = True
            st.session_state['usuario_editar'] = None

    if st.session_state['mostrar_formulario_usuario']:
        formulario_nuevo_usuario(st.session_state['usuario_editar'])

    elif st.session_state['usuario_confirmar_eliminar']:
        usuario = st.session_state['usuario_confirmar_eliminar']
        st.warning(f"¿Estás seguro que deseas eliminar al usuario **{usuario['nombres']}**?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Cancelar"):
                st.session_state['usuario_confirmar_eliminar'] = None
                st.rerun()
        with col2:
            if st.button("✅ Eliminar"):
                eliminar_usuario(usuario['usuario_id'], usuario['detalle_id'], usuario['nombres'])
                st.session_state['usuario_confirmar_eliminar'] = None
                st.rerun()

    else:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                ud.id AS detalle_id,
                ud.nombres,
                ud.apellidos,
                ud.cedula,
                ud.telefono,
                ud.correo_electronico,
                ud.direccion,
                ud.usuario_id,
                u.rol,
                u.nombre_usuario,
                (
                    SELECT m.nombre 
                    FROM mascotas m 
                    WHERE m.id_dueño = u.id 
                    ORDER BY m.id ASC 
                    LIMIT 1
                ) AS mascota
            FROM usuarios_detalle ud
            JOIN usuarios u ON ud.usuario_id = u.id
        """
        cursor.execute(query)
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()

        st.subheader("Usuarios registrados")

        if usuarios:
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 1, 1])
            col1.write("**Nombre**")
            col2.write("**Cédula**")
            col3.write("**Teléfono**")
            col4.write("**Mascota**")
            col5.write("**Editar**")
            col6.write("**Eliminar**")

            for usuario in usuarios:
                col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 1, 1])
                col1.write(usuario['nombres'])
                col2.write(usuario['cedula'])
                col3.write(usuario['telefono'])
                col4.write(usuario['mascota'])

                if col5.button("✏️", key=f"editar_{usuario['detalle_id']}"):
                    st.session_state['mostrar_formulario_usuario'] = True
                    st.session_state['usuario_editar'] = usuario
                    st.rerun()

                if col6.button("🗑️", key=f"eliminar_{usuario['detalle_id']}"):
                    st.session_state['usuario_confirmar_eliminar'] = usuario
                    st.rerun()
        else:
            st.info("No hay usuarios registrados.")
