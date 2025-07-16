import streamlit as st
from db import get_connection

def formulario_nueva_mascota(mascota_data=None):
    st.subheader("Registro de Mascotas")

    if 'paciente_registrado_exito' not in st.session_state:
        st.session_state['paciente_registrado_exito'] = False
    if 'paciente_editado_exito' not in st.session_state:
        st.session_state['paciente_editado_exito'] = False

    if st.session_state['paciente_registrado_exito']:
        st.success("")
        st.markdown('<div style="color:#111; font-size:1.1rem; font-weight:bold; margin-top:-2.5em; margin-bottom:1.5em;">Paciente registrado exitosamente</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Registrar otro paciente", key="registrar_otro_paciente_btn"):
                st.session_state['paciente_registrado_exito'] = False
                st.session_state['mascota_editar'] = None
                st.rerun()
        with col2:
            if st.button("Volver al listado", key="volver_listado_paciente_btn"):
                st.session_state['mostrar_formulario_mascota'] = False
                st.session_state['mascota_editar'] = None
                st.session_state['paciente_registrado_exito'] = False
                st.rerun()
    elif st.session_state['paciente_editado_exito']:
        st.success("")
        st.markdown('<div style="color:#111; font-size:1.1rem; font-weight:bold; margin-top:-2.5em; margin-bottom:1.5em;">Paciente actualizado exitosamente</div>', unsafe_allow_html=True)
        if st.button("Volver al listado", key="volver_listado_editado_btn"):
            st.session_state['mostrar_formulario_mascota'] = False
            st.session_state['mascota_editar'] = None
            st.session_state['paciente_editado_exito'] = False
            st.rerun()
    else:
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

        if st.button("Guardar", key="guardar_paciente_btn"):
            if not nombre or not raza or not id_dueño:
                st.warning("")
                if mascota_data:
                    st.markdown('<div style="color:#111; font-size:1.1rem; font-weight:bold; margin-top:-2.5em; margin-bottom:1.5em;">Error al editar paciente</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="color:#111; font-size:1.1rem; font-weight:bold; margin-top:-2.5em; margin-bottom:1.5em;">Error al registrar paciente</div>', unsafe_allow_html=True)
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()

                if mascota_data:  # Editar
                    query = "UPDATE mascotas SET nombre=%s, sexo=%s, edad=%s, raza=%s, id_dueño=%s WHERE id=%s"
                    cursor.execute(query, (nombre, sexo, edad, raza, id_dueño, mascota_data['id']))
                    st.session_state['paciente_editado_exito'] = True
                    st.success("")
                    st.markdown('<div style="color:#111; font-size:1.1rem; font-weight:bold; margin-top:-2.5em; margin-bottom:1.5em;">Paciente actualizado exitosamente</div>', unsafe_allow_html=True)
                else:  # Nuevo
                    query = "INSERT INTO mascotas (nombre, sexo, edad, raza, id_dueño) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(query, (nombre, sexo, edad, raza, id_dueño))
                    st.session_state['paciente_registrado_exito'] = True
                    st.success("")
                    st.markdown('<div style="color:#111; font-size:1.1rem; font-weight:bold; margin-top:-2.5em; margin-bottom:1.5em;">Paciente registrado exitosamente</div>', unsafe_allow_html=True)

                conn.commit()
                cursor.close()
                conn.close()

            except Exception as e:
                st.error(f"❌ Error al guardar: {e}")

        if st.button("Volver al listado", key="volver_listado_paciente_btn2"):
            st.session_state['mostrar_formulario_mascota'] = False
            st.session_state['mascota_editar'] = None
            st.session_state['paciente_registrado_exito'] = False
            st.session_state['paciente_editado_exito'] = False
            st.rerun()
