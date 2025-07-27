import streamlit as st
from datetime import datetime, date
from Formularios.frm_citas import formulario_nueva_cita
from db import get_connection

def eliminar_cita(cita_id: int, mascota_nombre: str):
    """Elimina una cita"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM citas WHERE id=%s", (cita_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        st.success(f"✅ Cita de {mascota_nombre} eliminada exitosamente.")
        
    except Exception as e:
        st.error(f"❌ Error al eliminar: {e}")

def obtener_citas():
    """Obtiene todas las citas con información relacionada"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                c.id,
                c.fecha_hora,
                c.duracion_minutos,
                c.tipo,
                c.estado,
                c.motivo,
                c.observaciones,
                m.nombre AS mascota_nombre,
                m.raza AS mascota_raza,
                m.sexo AS mascota_sexo,
                CONCAT(u_vet.nombre_usuario, ' ', u_vet.apellidos) AS veterinario_nombre,
                CONCAT(u_dueño.nombre_usuario, ' ', u_dueño.apellidos) AS dueño_nombre
            FROM citas c
            JOIN mascotas m ON c.id_mascota = m.id
            JOIN usuarios u_vet ON c.id_veterinario = u_vet.id
            JOIN usuarios u_dueño ON c.id_dueño = u_dueño.id
            ORDER BY c.fecha_hora DESC, c.id DESC
        """
        cursor.execute(query)
        citas = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return citas
        
    except Exception as e:
        st.error(f"❌ Error al obtener citas: {e}")
        return []

def obtener_cita_completa(cita_id: int):
    """Obtiene una cita completa con información detallada"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                c.id,
                c.fecha_hora,
                c.duracion_minutos,
                c.tipo,
                c.estado,
                c.motivo,
                c.observaciones,
                m.nombre AS mascota_nombre,
                m.raza AS mascota_raza,
                m.sexo AS mascota_sexo,
                CONCAT(u_vet.nombre_usuario, ' ', u_vet.apellidos) AS veterinario_nombre,
                CONCAT(u_dueño.nombre_usuario, ' ', u_dueño.apellidos) AS dueño_nombre
            FROM citas c
            JOIN mascotas m ON c.id_mascota = m.id
            JOIN usuarios u_vet ON c.id_veterinario = u_vet.id
            JOIN usuarios u_dueño ON c.id_dueño = u_dueño.id
            WHERE c.id = %s
        """
        cursor.execute(query, (cita_id,))
        cita = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return cita
        
    except Exception as e:
        st.error(f"❌ Error al obtener cita: {e}")
        return None

def formatear_fecha_hora(fecha_hora):
    """Formatea la fecha y hora para mostrar"""
    if isinstance(fecha_hora, str):
        fecha_hora = datetime.fromisoformat(fecha_hora.replace('Z', '+00:00'))
    return fecha_hora.strftime("%d/%m/%Y %H:%M")

def formatear_tipo_cita(tipo):
    """Formatea el tipo de cita para mostrar"""
    tipos = {
        "consulta_general": "Consulta General",
        "vacunacion": "Vacunación",
        "esterilizacion": "Esterilización",
        "urgencia": "Urgencia",
        "revision": "Revisión",
        "cirugia": "Cirugía"
    }
    return tipos.get(tipo, tipo)

def formatear_estado_cita(estado):
    """Formatea el estado de la cita para mostrar"""
    estados = {
        "programada": "Programada",
        "confirmada": "Confirmada",
        "en_progreso": "En Progreso",
        "completada": "Completada",
        "cancelada": "Cancelada",
        "no_asistio": "No Asistió"
    }
    return estados.get(estado, estado)

def obtener_color_estado(estado):
    """Obtiene el color para el estado de la cita"""
    colores = {
        "programada": "#FFA500",  # Naranja
        "confirmada": "#008000",  # Verde
        "en_progreso": "#0000FF", # Azul
        "completada": "#006400",  # Verde oscuro
        "cancelada": "#FF0000",   # Rojo
        "no_asistio": "#808080"   # Gris
    }
    return colores.get(estado, "#000000")

def main():
    st.title("📅 Gestión de Citas")
    
    # Inicializar variables de sesión
    if 'mostrar_formulario_cita' not in st.session_state:
        st.session_state['mostrar_formulario_cita'] = False
    if 'cita_editar' not in st.session_state:
        st.session_state['cita_editar'] = None
    if 'cita_confirmar_eliminar' not in st.session_state:
        st.session_state['cita_confirmar_eliminar'] = None
    if 'cita_ver_detalle' not in st.session_state:
        st.session_state['cita_ver_detalle'] = None

    # Botón para nueva cita
    if not st.session_state['mostrar_formulario_cita']:
        if st.button("➕ Agendar Cita"):
            st.session_state['mostrar_formulario_cita'] = True
            st.session_state['cita_editar'] = None

    # Mostrar formulario si está activo
    if st.session_state['mostrar_formulario_cita']:
        formulario_nueva_cita(st.session_state['cita_editar'])

    # Confirmación de eliminación
    elif st.session_state['cita_confirmar_eliminar']:
        cita = st.session_state['cita_confirmar_eliminar']
        st.warning("")
        st.markdown(f'<div style="color:#111; font-size:1.15rem; font-weight:bold; margin-top:-2.5em; margin-bottom:1.5em;">¿Está seguro que desea eliminar la cita de <b>{cita["mascota_nombre"]}</b> del {formatear_fecha_hora(cita["fecha_hora"])}?</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Cancelar"):
                st.session_state['cita_confirmar_eliminar'] = None
                st.rerun()
        with col2:
            if st.button("✅ Eliminar"):
                eliminar_cita(cita['id'], cita['mascota_nombre'])
                st.session_state['cita_confirmar_eliminar'] = None
                st.rerun()

    # Ver detalle de cita
    elif st.session_state['cita_ver_detalle']:
        cita_id = st.session_state['cita_ver_detalle']
        cita = obtener_cita_completa(cita_id)
        
        if cita:
            st.subheader(f"📅 Detalle de la Cita - {cita['mascota_nombre']}")
            
            # Información general
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Fecha y Hora:** {formatear_fecha_hora(cita['fecha_hora'])}")
                st.write(f"**Mascota:** {cita['mascota_nombre']}")
                st.write(f"**Raza:** {cita['mascota_raza']}")
                st.write(f"**Sexo:** {cita['mascota_sexo']}")
            with col2:
                st.write(f"**Dueño:** {cita['dueño_nombre']}")
                st.write(f"**Veterinario:** {cita['veterinario_nombre']}")
                st.write(f"**Duración:** {cita['duracion_minutos']} minutos")
                st.write(f"**Tipo:** {formatear_tipo_cita(cita['tipo'])}")
            
            # Estado de la cita
            color_estado = obtener_color_estado(cita['estado'])
            st.markdown(f'<div style="background-color:{color_estado}; color:white; padding:10px; border-radius:5px; text-align:center; font-weight:bold;">Estado: {formatear_estado_cita(cita["estado"])}</div>', unsafe_allow_html=True)
            
            # Motivo de la consulta
            st.subheader("Motivo de la Consulta")
            st.write(cita['motivo'])
            
            # Observaciones
            if cita['observaciones']:
                st.subheader("Observaciones")
                st.write(cita['observaciones'])
            
            if st.button("⬅️ Volver al listado"):
                st.session_state['cita_ver_detalle'] = None
                st.rerun()
        else:
            st.error("❌ No se pudo cargar la cita")
            if st.button("⬅️ Volver al listado"):
                st.session_state['cita_ver_detalle'] = None
                st.rerun()

    # Listado de citas
    else:
        citas = obtener_citas()
        
        if citas:
            st.subheader("Citas Agendadas")
            
            # Filtros
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                filtro_mascota = st.text_input("🔍 Filtrar por mascota", "")
            with col2:
                filtro_veterinario = st.text_input("👨‍⚕️ Filtrar por veterinario", "")
            with col3:
                filtro_fecha = st.date_input("📅 Filtrar por fecha", value=None)
            with col4:
                filtro_estado = st.selectbox("📊 Filtrar por estado", 
                                           ["Todos"] + list(set([c['estado'] for c in citas])))
            
            # Aplicar filtros
            citas_filtradas = citas
            if filtro_mascota:
                citas_filtradas = [c for c in citas_filtradas if filtro_mascota.lower() in c['mascota_nombre'].lower()]
            if filtro_veterinario:
                citas_filtradas = [c for c in citas_filtradas if filtro_veterinario.lower() in c['veterinario_nombre'].lower()]
            if filtro_fecha:
                citas_filtradas = [c for c in citas_filtradas if c['fecha_hora'].date() == filtro_fecha]
            if filtro_estado and filtro_estado != "Todos":
                citas_filtradas = [c for c in citas_filtradas if c['estado'] == filtro_estado]
            
            # Mostrar citas
            if citas_filtradas:
                for cita in citas_filtradas:
                    with st.container():
                        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2, 1, 1, 1, 1, 1, 1, 1])
                        
                        with col1:
                            st.write(f"**{cita['mascota_nombre']}** ({cita['mascota_raza']})")
                            st.write(f"*{cita['motivo'][:50]}{'...' if len(cita['motivo']) > 50 else ''}*")
                        
                        with col2:
                            st.write(f"📅 {formatear_fecha_hora(cita['fecha_hora'])}")
                        
                        with col3:
                            st.write(f"👨‍⚕️ {cita['veterinario_nombre']}")
                        
                        with col4:
                            st.write(f"👤 {cita['dueño_nombre']}")
                        
                        with col5:
                            color_estado = obtener_color_estado(cita['estado'])
                            st.markdown(f'<div style="background-color:{color_estado}; color:white; padding:5px; border-radius:3px; text-align:center; font-size:0.8rem;">{formatear_estado_cita(cita["estado"])}</div>', unsafe_allow_html=True)
                        
                        with col6:
                            if st.button("👁️", key=f"ver_{cita['id']}"):
                                st.session_state['cita_ver_detalle'] = cita['id']
                                st.rerun()
                        
                        with col7:
                            if st.button("✏️", key=f"editar_{cita['id']}"):
                                # Preparar datos para edición
                                cita_editar = {
                                    'id': cita['id'],
                                    'fecha': cita['fecha_hora'].date(),
                                    'hora': cita['fecha_hora'].time(),
                                    'duracion_minutos': cita['duracion_minutos'],
                                    'tipo': cita['tipo'],
                                    'estado': cita['estado'],
                                    'motivo': cita['motivo'],
                                    'observaciones': cita['observaciones']
                                }
                                st.session_state['cita_editar'] = cita_editar
                                st.session_state['mostrar_formulario_cita'] = True
                                st.rerun()
                        
                        with col8:
                            if st.button("🗑️", key=f"eliminar_{cita['id']}"):
                                st.session_state['cita_confirmar_eliminar'] = cita
                                st.rerun()
                        
                        st.divider()
            else:
                st.info("No se encontraron citas con los filtros aplicados.")
        else:
            st.info("📅 No hay citas agendadas.")

if __name__ == "__main__":
    main()
