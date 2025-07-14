import streamlit as st
from db import get_connection
from Formularios.frm_mascotas import formulario_nueva_mascota

def eliminar_mascota(mascota_id, nombre):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mascotas WHERE id = %s", (mascota_id,))
        conn.commit()
        cursor.close()
        conn.close()
        st.success(f"✅ Mascota '{nombre}' eliminada exitosamente.")
    except Exception as e:
        st.error(f"❌ Error al eliminar mascota: {e}")

def main():
    st.title("Listado de Mascotas")

    if 'mostrar_formulario_mascota' not in st.session_state:
        st.session_state['mostrar_formulario_mascota'] = False
    if 'mascota_editar' not in st.session_state:
        st.session_state['mascota_editar'] = None
    if 'mascota_confirmar_eliminar' not in st.session_state:
        st.session_state['mascota_confirmar_eliminar'] = None

    if not st.session_state['mostrar_formulario_mascota']:
        if st.button("➕ Nueva Mascota"):
            st.session_state['mostrar_formulario_mascota'] = True
            st.session_state['mascota_editar'] = None

    if st.session_state['mostrar_formulario_mascota']:
        formulario_nueva_mascota(st.session_state['mascota_editar'])

    elif st.session_state['mascota_confirmar_eliminar']:
        mascota = st.session_state['mascota_confirmar_eliminar']
        st.warning(f"¿Estás seguro que deseas eliminar a la mascota **{mascota['nombre']}**?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Cancelar"):
                st.session_state['mascota_confirmar_eliminar'] = None
                st.rerun()
        with col2:
            if st.button("✅ Eliminar"):
                eliminar_mascota(mascota['id'], mascota['nombre'])
                st.session_state['mascota_confirmar_eliminar'] = None
                st.rerun()

    else:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT m.id, m.nombre, m.sexo, m.edad, m.raza, ud.nombres AS dueño
            FROM mascotas m
            JOIN usuarios_detalle ud ON m.id_dueño = ud.usuario_id
        """
        cursor.execute(query)
        mascotas = cursor.fetchall()
        cursor.close()
        conn.close()

        st.subheader("Mascotas registradas")

        if mascotas:
            col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 1, 2, 2, 1, 1])
            col1.write("**Nombre**")
            col2.write("**Sexo**")
            col3.write("**Edad**")
            col4.write("**Raza**")
            col5.write("**Dueño**")
            col6.write("**Editar**")
            col7.write("**Eliminar**")

            for mascota in mascotas:
                col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 1, 2, 2, 1, 1])
                col1.write(mascota['nombre'])
                col2.write(mascota['sexo'])
                col3.write(f"{mascota['edad'] // 12}")
                col4.write(mascota['raza'])
                col5.write(mascota['dueño'])

                if col6.button("✏️", key=f"editar_{mascota['id']}"):
                    st.session_state['mostrar_formulario_mascota'] = True
                    st.session_state['mascota_editar'] = mascota
                    st.rerun()

                if col7.button("🗑️", key=f"eliminar_{mascota['id']}"):
                    st.session_state['mascota_confirmar_eliminar'] = mascota
                    st.rerun()
        else:
            st.info("No hay mascotas registradas.")
