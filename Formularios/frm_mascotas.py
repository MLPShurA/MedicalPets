import streamlit as st
from db import get_connection

def formulario_nueva_mascota(mascota_data=None):
    st.subheader("Registro de Mascotas")

    nombre = st.text_input("Nombre", value=mascota_data.get('nombre') if mascota_data else "")
    sexo = st.selectbox("Sexo", ["Macho", "Hembra"], index=["Macho", "Hembra"].index(mascota_data.get('sexo')) if mascota_data else 0)
    col1, col2 = st.columns(2)
    with col1:
        edad_anos = st.number_input("Edad (años)", min_value=0, value=mascota_data['edad'] // 12 if mascota_data else 0)
    with col2:
        edad_meses = st.number_input("Edad (meses)", min_value=0, max_value=11,
                                     value=mascota_data['edad'] % 12 if mascota_data else 0)

    edad = edad_anos * 12 + edad_meses
    raza = st.text_input("Raza", value=mascota_data.get('raza') if mascota_data else "")

    # Buscar lista de dueños
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT usuario_id, nombres FROM usuarios_detalle")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()

    opciones_dueños = {u['nombres']: u['usuario_id'] for u in usuarios}
    nombres_usuarios = list(opciones_dueños.keys())

    search = st.text_input("Buscar dueño", "")
    filtrados = [n for n in nombres_usuarios if search.lower() in n.lower()]

    dueño_nombre = st.selectbox("Dueño", filtrados)
    id_dueño = opciones_dueños[dueño_nombre]

    if st.button("Guardar Mascota"):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            if mascota_data:  # Editar
                query = "UPDATE mascotas SET nombre=%s, sexo=%s, edad=%s, raza=%s, id_dueño=%s WHERE id=%s"
                cursor.execute(query, (nombre, sexo, edad, raza, id_dueño, mascota_data['id']))
                st.success("✅ Mascota actualizada exitosamente.")
            else:  # Nuevo
                query = "INSERT INTO mascotas (nombre, sexo, edad, raza, id_dueño) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (nombre, sexo, edad, raza, id_dueño))
                st.success("✅ Mascota registrada exitosamente.")

            conn.commit()
            cursor.close()
            conn.close()

            st.session_state['mostrar_formulario_mascota'] = False
            st.session_state['mascota_editar'] = None
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error al guardar: {e}")

    if st.button("Volver al listado"):
        st.session_state['mostrar_formulario_mascota'] = False
        st.session_state['mascota_editar'] = None
        st.rerun()
