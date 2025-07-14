#AQUI SE CONECTA EL FORMULARIO DEL REGISTRO DEL HISTORIAL CLINICO CON LA BDD
import streamlit as st
from Formularios.frm_historial import formulario_nuevo_historial
from db import get_connection

def eliminar_historial(historial_id: int, mascota_nombre: str):
    """Elimina un historial clínico"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Eliminar tratamientos primero (por la FK)
        cursor.execute("DELETE FROM tratamientos WHERE id_historial=%s", (historial_id,))
        
        # Eliminar historial
        cursor.execute("DELETE FROM historial_clinico WHERE id=%s", (historial_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        st.success(f"✅ Historial de {mascota_nombre} eliminado exitosamente.")
        
    except Exception as e:
        st.error(f"❌ Error al eliminar: {e}")

def obtener_historiales():
    """Obtiene todos los historiales clínicos con información relacionada"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                hc.id,
                hc.fecha,
                hc.motivo_consulta,
                hc.sintomas,
                hc.antecedentes,
                hc.diagnostico,
                hc.observaciones,
                hc.peso,
                m.nombre AS mascota_nombre,
                m.raza AS mascota_raza,
                m.sexo AS mascota_sexo,
                ud.nombres AS dueño_nombre,
                COUNT(t.id) AS num_tratamientos
            FROM historial_clinico hc
            JOIN mascotas m ON hc.id_mascota = m.id
            JOIN usuarios_detalle ud ON m.id_dueño = ud.usuario_id
            LEFT JOIN tratamientos t ON hc.id = t.id_historial
            GROUP BY hc.id, hc.fecha, hc.motivo_consulta, hc.sintomas, hc.antecedentes, 
                     hc.diagnostico, hc.observaciones, hc.peso, m.nombre, m.raza, m.sexo, ud.nombres
            ORDER BY hc.fecha DESC, hc.id DESC
        """
        cursor.execute(query)
        historiales = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return historiales
        
    except Exception as e:
        st.error(f"❌ Error al obtener historiales: {e}")
        return []

def obtener_historial_completo(historial_id: int):
    """Obtiene un historial completo con sus tratamientos"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Obtener historial
        query_historial = """
            SELECT 
                hc.id,
                hc.fecha,
                hc.motivo_consulta,
                hc.sintomas,
                hc.antecedentes,
                hc.diagnostico,
                hc.observaciones,
                hc.peso,
                m.nombre AS mascota_nombre,
                m.raza AS mascota_raza,
                m.sexo AS mascota_sexo,
                ud.nombres AS dueño_nombre
            FROM historial_clinico hc
            JOIN mascotas m ON hc.id_mascota = m.id
            JOIN usuarios_detalle ud ON m.id_dueño = ud.usuario_id
            WHERE hc.id = %s
        """
        cursor.execute(query_historial, (historial_id,))
        historial = cursor.fetchone()
        
        if not historial:
            return None
        
        # Obtener tratamientos
        query_tratamientos = """
            SELECT id, nombre_tratamiento, dosis, frecuencia, duracion, observaciones, fecha_inicio, fecha_fin
            FROM tratamientos
            WHERE id_historial = %s
            ORDER BY fecha_inicio
        """
        cursor.execute(query_tratamientos, (historial_id,))
        tratamientos = cursor.fetchall()
        
        historial['tratamientos'] = tratamientos
        cursor.close()
        conn.close()
        
        return historial
        
    except Exception as e:
        st.error(f"❌ Error al obtener historial: {e}")
        return None

def main():
    st.title("📋 Historial Clínico")
    
    # Inicializar variables de sesión
    if 'mostrar_formulario_historial' not in st.session_state:
        st.session_state['mostrar_formulario_historial'] = False
    if 'historial_editar' not in st.session_state:
        st.session_state['historial_editar'] = None
    if 'historial_confirmar_eliminar' not in st.session_state:
        st.session_state['historial_confirmar_eliminar'] = None
    if 'historial_ver_detalle' not in st.session_state:
        st.session_state['historial_ver_detalle'] = None

    # Botón para nuevo historial
    if not st.session_state['mostrar_formulario_historial']:
        if st.button("➕ Nuevo Historial Clínico"):
            st.session_state['mostrar_formulario_historial'] = True
            st.session_state['historial_editar'] = None

    # Mostrar formulario si está activo
    if st.session_state['mostrar_formulario_historial']:
        formulario_nuevo_historial(st.session_state['historial_editar'])

    # Confirmación de eliminación
    elif st.session_state['historial_confirmar_eliminar']:
        historial = st.session_state['historial_confirmar_eliminar']
        st.warning(f"¿Estás seguro que deseas eliminar el historial de **{historial['mascota_nombre']}** del {historial['fecha']}?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Cancelar"):
                st.session_state['historial_confirmar_eliminar'] = None
                st.rerun()
        with col2:
            if st.button("✅ Eliminar"):
                eliminar_historial(historial['id'], historial['mascota_nombre'])
                st.session_state['historial_confirmar_eliminar'] = None
                st.rerun()

    # Ver detalle de historial
    elif st.session_state['historial_ver_detalle']:
        historial_id = st.session_state['historial_ver_detalle']
        historial = obtener_historial_completo(historial_id)
        
        if historial:
            st.subheader(f"📋 Detalle del Historial - {historial['mascota_nombre']}")
            
            # Información general
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Fecha:** {historial['fecha']}")
                st.write(f"**Mascota:** {historial['mascota_nombre']}")
                st.write(f"**Raza:** {historial['mascota_raza']}")
                st.write(f"**Sexo:** {historial['mascota_sexo']}")
            with col2:
                st.write(f"**Dueño:** {historial['dueño_nombre']}")
                st.write(f"**Peso:** {historial['peso']} kg" if historial['peso'] else "**Peso:** No registrado")
                st.write(f"**Tratamientos:** {len(historial['tratamientos'])}")
            
            # Motivo de consulta
            st.subheader("Motivo de Consulta")
            st.write(historial['motivo_consulta'])
            
            # Síntomas
            if historial['sintomas']:
                st.subheader("Síntomas")
                st.write(historial['sintomas'])
            
            # Antecedentes
            if historial['antecedentes']:
                st.subheader("Antecedentes")
                st.write(historial['antecedentes'])
            
            # Diagnóstico
            if historial['diagnostico']:
                st.subheader("Diagnóstico")
                st.write(historial['diagnostico'])
            
            # Observaciones
            if historial['observaciones']:
                st.subheader("Observaciones")
                st.write(historial['observaciones'])
            
            # Tratamientos
            if historial['tratamientos']:
                st.subheader("Tratamientos")
                for i, tratamiento in enumerate(historial['tratamientos'], 1):
                    with st.expander(f"Tratamiento {i}: {tratamiento['nombre_tratamiento']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Dosis:** {tratamiento['dosis']}")
                            st.write(f"**Frecuencia:** {tratamiento['frecuencia']}")
                            st.write(f"**Duración:** {tratamiento['duracion']}")
                        with col2:
                            st.write(f"**Inicio:** {tratamiento['fecha_inicio']}")
                            st.write(f"**Fin:** {tratamiento['fecha_fin']}")
                        if tratamiento['observaciones']:
                            st.write(f"**Observaciones:** {tratamiento['observaciones']}")
            
            if st.button("⬅️ Volver al listado"):
                st.session_state['historial_ver_detalle'] = None
                st.rerun()
        else:
            st.error("❌ No se pudo cargar el historial")
            if st.button("⬅️ Volver al listado"):
                st.session_state['historial_ver_detalle'] = None
                st.rerun()

    # Listado de historiales
    else:
        historiales = obtener_historiales()
        
        if historiales:
            st.subheader("Historiales Clínicos Registrados")
            
            # Filtros
            col1, col2, col3 = st.columns(3)
            with col1:
                filtro_mascota = st.text_input("🔍 Filtrar por mascota", "")
            with col2:
                filtro_fecha = st.date_input("📅 Filtrar por fecha", value=None)
            with col3:
                mostrar_solo_con_tratamientos = st.checkbox("💊 Solo con tratamientos")
            
            # Aplicar filtros
            historiales_filtrados = historiales
            if filtro_mascota:
                historiales_filtrados = [h for h in historiales_filtrados if filtro_mascota.lower() in h['mascota_nombre'].lower()]
            if filtro_fecha:
                historiales_filtrados = [h for h in historiales_filtrados if h['fecha'] == filtro_fecha]
            if mostrar_solo_con_tratamientos:
                historiales_filtrados = [h for h in historiales_filtrados if h['num_tratamientos'] > 0]
            
            # Mostrar historiales
            if historiales_filtrados:
                for historial in historiales_filtrados:
                    with st.container():
                        col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 2, 1, 1, 1])
                        
                        with col1:
                            st.write(f"**{historial['mascota_nombre']}** ({historial['mascota_raza']})")
                            st.write(f"*{historial['motivo_consulta'][:50]}{'...' if len(historial['motivo_consulta']) > 50 else ''}*")
                        
                        with col2:
                            st.write(f"📅 {historial['fecha']}")
                        
                        with col3:
                            st.write(f"👤 {historial['dueño_nombre']}")
                            if historial['peso']:
                                st.write(f"⚖️ {historial['peso']} kg")
                        
                        with col4:
                            if historial['num_tratamientos'] > 0:
                                st.write(f"💊 {historial['num_tratamientos']}")
                            else:
                                st.write("❌ Sin tratamientos")
                        
                        with col5:
                            if st.button("👁️", key=f"ver_{historial['id']}"):
                                st.session_state['historial_ver_detalle'] = historial['id']
                                st.rerun()
                        
                        with col6:
                            if st.button("🗑️", key=f"eliminar_{historial['id']}"):
                                st.session_state['historial_confirmar_eliminar'] = historial
                                st.rerun()
                        
                        st.divider()
            else:
                st.info("No se encontraron historiales con los filtros aplicados.")
        else:
            st.info("📋 No hay historiales clínicos registrados.")

if __name__ == "__main__":
    main()
