import streamlit as st
from datetime import date, datetime
from decimal import Decimal
from db import get_connection

def formulario_nuevo_historial(historial_data=None):
    st.subheader("Registro de Historial Clínico")

    # Buscar lista de mascotas
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.id, m.nombre, m.raza, m.sexo, ud.nombres AS dueño_nombre
        FROM mascotas m
        JOIN usuarios_detalle ud ON m.id_dueño = ud.usuario_id
        ORDER BY m.nombre
    """)
    mascotas = cursor.fetchall()
    cursor.close()
    conn.close()

    if not mascotas:
        st.error("❌ No hay mascotas registradas. Debe registrar mascotas primero.")
        if st.button("Volver"):
            st.session_state['mostrar_formulario_historial'] = False
            st.rerun()
        return

    # Selección de mascota
    opciones_mascotas = {f"{m['nombre']} ({m['raza']}) - {m['dueño_nombre']}": m['id'] for m in mascotas}
    nombres_mascotas = list(opciones_mascotas.keys())

    search = st.text_input("Buscar mascota", "")
    filtrados = [n for n in nombres_mascotas if search.lower() in n.lower()]

    if not filtrados:
        st.warning("No se encontraron mascotas con ese nombre.")
        return

    mascota_seleccionada = st.selectbox("Seleccionar Mascota", filtrados)
    id_mascota = opciones_mascotas[mascota_seleccionada]

    # Información de la mascota seleccionada
    mascota_info = next(m for m in mascotas if m['id'] == id_mascota)
    st.info(f"📋 **Mascota seleccionada:** {mascota_info['nombre']} - {mascota_info['raza']} - {mascota_info['sexo']}")

    # Campos del historial
    fecha = st.date_input("Fecha de consulta", value=historial_data.get('fecha') if historial_data else date.today())
    
    motivo_consulta = st.text_area("Motivo de consulta", 
                                  value=historial_data.get('motivo_consulta') if historial_data else "",
                                  height=100)
    
    sintomas = st.text_area("Síntomas observados", 
                           value=historial_data.get('sintomas') if historial_data else "",
                           height=100)
    
    antecedentes = st.text_area("Antecedentes médicos", 
                               value=historial_data.get('antecedentes') if historial_data else "",
                               height=100)
    
    diagnostico = st.text_area("Diagnóstico", 
                              value=historial_data.get('diagnostico') if historial_data else "",
                              height=100)
    
    observaciones = st.text_area("Observaciones adicionales", 
                                value=historial_data.get('observaciones') if historial_data else "",
                                height=100)
    
    # Peso con validación
    peso_input = st.number_input("Peso (kg)", 
                                min_value=0.1, 
                                max_value=999.99, 
                                step=0.1,
                                value=float(historial_data.get('peso')) if historial_data and historial_data.get('peso') else None,
                                format="%.2f")

    # Sección de tratamientos
    st.subheader("Tratamientos")
    
    if 'tratamientos' not in st.session_state:
        st.session_state.tratamientos = []
    
    if historial_data and historial_data.get('tratamientos'):
        st.session_state.tratamientos = historial_data['tratamientos']

    # Estado para edición de tratamiento
    if 'tratamiento_editar_idx' not in st.session_state:
        st.session_state.tratamiento_editar_idx = None
    if 'tratamiento_editar_data' not in st.session_state:
        st.session_state.tratamiento_editar_data = None

    # Formulario para agregar o editar tratamiento
    if st.session_state.tratamiento_editar_idx is not None:
        idx = st.session_state.tratamiento_editar_idx
        data = st.session_state.tratamiento_editar_data or st.session_state.tratamientos[idx]
        with st.expander("✏️ Editar Tratamiento", expanded=True):
            with st.form("form_editar_tratamiento"):
                col1, col2 = st.columns(2)
                with col1:
                    nombre_tratamiento = st.text_input("Nombre del tratamiento", value=data.get('nombre_tratamiento', ''))
                    dosis = st.text_input("Dosis", value=data.get('dosis', ''))
                    fecha_inicio = st.date_input("Fecha de inicio", value=data.get('fecha_inicio', date.today()))
                with col2:
                    frecuencia = st.text_input("Frecuencia", value=data.get('frecuencia', ''))
                    duracion = st.text_input("Duración", value=data.get('duracion', ''))
                    fecha_fin = st.date_input("Fecha de fin", value=data.get('fecha_fin', date.today()))
                observaciones_tratamiento = st.text_area("Observaciones del tratamiento", value=data.get('observaciones', ''))
                if st.form_submit_button("Actualizar Tratamiento"):
                    if nombre_tratamiento.strip():
                        st.session_state.tratamientos[idx] = {
                            'nombre_tratamiento': nombre_tratamiento,
                            'dosis': dosis,
                            'frecuencia': frecuencia,
                            'duracion': duracion,
                            'observaciones': observaciones_tratamiento,
                            'fecha_inicio': fecha_inicio,
                            'fecha_fin': fecha_fin
                        }
                        st.session_state.tratamiento_editar_idx = None
                        st.session_state.tratamiento_editar_data = None
                        st.success("✅ Tratamiento actualizado")
                        st.rerun()
                    else:
                        st.session_state.tratamiento_editar_data = {
                            'nombre_tratamiento': nombre_tratamiento,
                            'dosis': dosis,
                            'frecuencia': frecuencia,
                            'duracion': duracion,
                            'observaciones': observaciones_tratamiento,
                            'fecha_inicio': fecha_inicio,
                            'fecha_fin': fecha_fin
                        }
                        st.error("❌ El nombre del tratamiento es obligatorio")
            if st.button("Cancelar edición de tratamiento"):
                st.session_state.tratamiento_editar_idx = None
                st.session_state.tratamiento_editar_data = None
                st.rerun()
    else:
        with st.expander("➕ Agregar Tratamiento", expanded=False):
            with st.form("form_tratamiento"):
                col1, col2 = st.columns(2)
                with col1:
                    nombre_tratamiento = st.text_input("Nombre del tratamiento")
                    dosis = st.text_input("Dosis")
                    fecha_inicio = st.date_input("Fecha de inicio", value=date.today())
                with col2:
                    frecuencia = st.text_input("Frecuencia")
                    duracion = st.text_input("Duración")
                    fecha_fin = st.date_input("Fecha de fin", value=date.today())
                observaciones_tratamiento = st.text_area("Observaciones del tratamiento")
                if st.form_submit_button("Agregar Tratamiento"):
                    if nombre_tratamiento.strip():
                        nuevo_tratamiento = {
                            'nombre_tratamiento': nombre_tratamiento,
                            'dosis': dosis,
                            'frecuencia': frecuencia,
                            'duracion': duracion,
                            'observaciones': observaciones_tratamiento,
                            'fecha_inicio': fecha_inicio,
                            'fecha_fin': fecha_fin
                        }
                        st.session_state.tratamientos.append(nuevo_tratamiento)
                        st.success("✅ Tratamiento agregado")
                        st.rerun()
                    else:
                        st.error("❌ El nombre del tratamiento es obligatorio")

    # Mostrar tratamientos agregados
    if st.session_state.tratamientos:
        st.write("**Tratamientos registrados:**")
        for i, tratamiento in enumerate(st.session_state.tratamientos):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{tratamiento['nombre_tratamiento']}** - {tratamiento['dosis']} - {tratamiento['frecuencia']}")
                st.write(f"*{tratamiento['observaciones']}*")
            with col2:
                if st.button("✏️", key=f"editar_trat_{i}"):
                    st.session_state.tratamiento_editar_idx = i
                    st.session_state.tratamiento_editar_data = None
                    st.rerun()
            with col3:
                if st.button("🗑️", key=f"eliminar_trat_{i}"):
                    st.session_state.tratamientos.pop(i)
                    st.rerun()
    else:
        st.info("No hay tratamientos registrados")

    # Botones de acción
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("💾 Guardar Historial"):
            if not motivo_consulta.strip():
                st.error("❌ El motivo de consulta es obligatorio")
                return
            
            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                if historial_data:  # Editar
                    # Actualizar historial clínico
                    query_historial = """
                        UPDATE historial_clinico 
                        SET id_mascota=%s, fecha=%s, motivo_consulta=%s, sintomas=%s, 
                            antecedentes=%s, diagnostico=%s, observaciones=%s, peso=%s
                        WHERE id=%s
                    """
                    cursor.execute(query_historial, (
                        id_mascota, fecha, motivo_consulta, sintomas, antecedentes,
                        diagnostico, observaciones, peso_input, historial_data['id']
                    ))
                    
                    # Eliminar tratamientos anteriores
                    cursor.execute("DELETE FROM tratamientos WHERE id_historial=%s", (historial_data['id'],))
                    
                    st.success("✅ Historial actualizado exitosamente.")
                    
                else:  # Nuevo
                    # Insertar historial clínico
                    query_historial = """
                        INSERT INTO historial_clinico 
                        (id_mascota, fecha, motivo_consulta, sintomas, antecedentes, diagnostico, observaciones, peso)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query_historial, (
                        id_mascota, fecha, motivo_consulta, sintomas, antecedentes,
                        diagnostico, observaciones, peso_input
                    ))
                    historial_id = cursor.lastrowid
                    
                    st.success("✅ Historial registrado exitosamente.")
                
                # Insertar tratamientos
                for tratamiento in st.session_state.tratamientos:
                    query_tratamiento = """
                        INSERT INTO tratamientos 
                        (id_historial, nombre_tratamiento, dosis, frecuencia, duracion, observaciones, fecha_inicio, fecha_fin)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query_tratamiento, (
                        historial_data['id'] if historial_data else historial_id,
                        tratamiento['nombre_tratamiento'],
                        tratamiento['dosis'],
                        tratamiento['frecuencia'],
                        tratamiento['duracion'],
                        tratamiento['observaciones'],
                        tratamiento['fecha_inicio'],
                        tratamiento['fecha_fin']
                    ))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                # Limpiar estado
                st.session_state['mostrar_formulario_historial'] = False
                st.session_state['historial_editar'] = None
                st.session_state.tratamientos = []
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error al guardar: {e}")
    
    with col2:
        if st.button("🔄 Limpiar"):
            st.session_state.tratamientos = []
            st.rerun()
    
    with col3:
        if st.button("⬅️ Volver al listado"):
            st.session_state['mostrar_formulario_historial'] = False
            st.session_state['historial_editar'] = None
            st.session_state.tratamientos = []
            st.rerun() 