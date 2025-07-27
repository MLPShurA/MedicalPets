import streamlit as st
from datetime import datetime, date, time
from db import get_connection

def formulario_nueva_cita(cita_data=None):
    st.subheader("📅 Agendar Nueva Cita")

    if 'cita_registrada_exito' not in st.session_state:
        st.session_state['cita_registrada_exito'] = False

    # Buscar lista de veterinarios
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.id, u.nombre_usuario, u.rol, u.apellidos
        FROM usuarios u
        WHERE u.rol IN ('veterinario', 'doctor')
        ORDER BY u.nombre_usuario, u.apellidos
    """)
    veterinarios = cursor.fetchall()
    cursor.close()
    conn.close()

    # Procesar los datos de veterinarios para mostrar información más amigable
    for veterinario in veterinarios:
        # Si el nombre_usuario es un correo, extraer solo la parte antes del @
        if veterinario['nombre_usuario'] and '@' in str(veterinario['nombre_usuario']):
            veterinario['nombre_usuario'] = str(veterinario['nombre_usuario']).split('@')[0]
        
        # Si no hay apellidos, usar un valor por defecto
        if not veterinario['apellidos']:
            veterinario['apellidos'] = ""

    if not veterinarios:
        st.error("❌ No hay veterinarios registrados. Debe registrar veterinarios primero.")
        if st.button("Volver"):
            st.session_state['mostrar_formulario_cita'] = False
            st.rerun()
        return

    # Buscar lista de mascotas con dueños
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.id, m.nombre, m.raza, m.sexo, 
               u.nombre_usuario AS dueño_nombre, u.apellidos AS dueño_apellidos,
               m.id_dueño
        FROM mascotas m
        JOIN usuarios u ON m.id_dueño = u.id
        ORDER BY m.nombre
    """)
    mascotas = cursor.fetchall()
    cursor.close()
    conn.close()

    # Procesar los datos para mostrar información más amigable
    for mascota in mascotas:
        # Si el nombre_usuario es un correo, extraer solo la parte antes del @
        if mascota['dueño_nombre'] and '@' in mascota['dueño_nombre']:
            mascota['dueño_nombre'] = mascota['dueño_nombre'].split('@')[0]
        
        # Si no hay apellidos, usar un valor por defecto
        if not mascota['dueño_apellidos']:
            mascota['dueño_apellidos'] = ""

    if not mascotas:
        st.error("❌ No hay mascotas registradas. Debe registrar mascotas primero.")
        if st.button("Volver"):
            st.session_state['mostrar_formulario_cita'] = False
            st.rerun()
        return

    # Selección de veterinario
    opciones_veterinarios = {f"Dr. {v['nombre_usuario']} {v['apellidos']}": v['id'] for v in veterinarios}
    nombres_veterinarios = list(opciones_veterinarios.keys())

    st.write("**Seleccionar Veterinario:**")
    
    # Determinar el índice correcto para edición
    index_veterinario = 0
    if cita_data and cita_data.get('id_veterinario'):
        # Buscar el veterinario correspondiente a la cita
        for i, vet in enumerate(veterinarios):
            if vet['id'] == cita_data['id_veterinario']:
                index_veterinario = i
                break
    
    veterinario_seleccionado = st.selectbox("Veterinario", nombres_veterinarios, 
                                           index=index_veterinario)
    id_veterinario = opciones_veterinarios[veterinario_seleccionado]

    # Información del veterinario seleccionado
    veterinario_info = next(v for v in veterinarios if v['id'] == id_veterinario)
    st.markdown(f'''<div style="background:#e7f3fe; border-left:6px solid #2196F3; padding:12px 18px; border-radius:8px; margin-bottom:10px;">
        <span style="color:#111; font-size:1.1rem; font-weight:bold;">👨‍⚕️ Veterinario seleccionado: Dr. {veterinario_info["nombre_usuario"]} {veterinario_info["apellidos"]}</span>
    </div>''', unsafe_allow_html=True)

    # Selección de mascota con filtro de búsqueda
    opciones_mascotas = {f"{m['nombre']} ({m['raza']})": m for m in mascotas}
    nombres_mascotas = list(opciones_mascotas.keys())

    st.write("**Seleccionar Mascota:**")
    search = st.text_input("🔍 Buscar por nombre de mascota", "")
    filtrados = [n for n in nombres_mascotas if search.lower() in n.lower()]

    if not filtrados:
        st.warning("No se encontraron mascotas con ese nombre.")
        return

    # Determinar el índice correcto para edición de mascota
    index_mascota = 0
    if cita_data and cita_data.get('id_mascota'):
        # Buscar la mascota correspondiente a la cita
        for i, mascota in enumerate(mascotas):
            if mascota['id'] == cita_data['id_mascota']:
                # Encontrar el índice en la lista filtrada
                mascota_key = f"{mascota['nombre']} ({mascota['raza']})"
                if mascota_key in filtrados:
                    index_mascota = filtrados.index(mascota_key)
                break
    
    mascota_seleccionada = st.selectbox("Mascota", filtrados, 
                                       index=index_mascota)
    mascota_info = opciones_mascotas[mascota_seleccionada]

    # Información de la mascota seleccionada
    st.markdown(f'''<div style="background:#e7f3fe; border-left:6px solid #2196F3; padding:12px 18px; border-radius:8px; margin-bottom:10px;">
        <span style="color:#111; font-size:1.1rem; font-weight:bold;">🐾 Mascota seleccionada: {mascota_info["nombre"]} - {mascota_info["raza"]} - {mascota_info["sexo"]}</span><br>
        <span style="color:#666; font-size:0.9rem;">👤 Dueño: {mascota_info["dueño_nombre"]} {mascota_info["dueño_apellidos"]}</span>
    </div>''', unsafe_allow_html=True)

    # Campos de la cita
    col1, col2 = st.columns(2)
    
    with col1:
        fecha = st.date_input("📅 Fecha de la cita", 
                             value=cita_data.get('fecha') if cita_data else date.today())
    
    with col2:
        # Generar opciones de hora
        opciones_hora = []
        for h in range(8, 20):  # De 8:00 AM a 7:00 PM
            for m in [0, 15, 30, 45]:  # Cada 15 minutos
                hora_obj = time(h, m)
                opciones_hora.append((hora_obj, f"{h:02d}:{m:02d}"))
        
        # Encontrar el índice de la hora actual o por defecto
        hora_default = cita_data.get('hora') if cita_data else time(9, 0)
        hora_index = 0
        for i, (hora_obj, _) in enumerate(opciones_hora):
            if hora_obj == hora_default:
                hora_index = i
                break
        
        hora_seleccionada = st.selectbox("🕐 Hora de la cita", 
                                        options=[op[1] for op in opciones_hora],
                                        index=hora_index)
        
        # Convertir de vuelta a objeto time
        hora = time(int(hora_seleccionada.split(':')[0]), int(hora_seleccionada.split(':')[1]))

    # Combinar fecha y hora
    fecha_hora = datetime.combine(fecha, hora)

    col1, col2 = st.columns(2)
    
    with col1:
        duracion = st.selectbox("⏱️ Duración (minutos)", 
                               options=[15, 30, 45, 60, 90, 120],
                               index=1 if not cita_data else None)  # 30 minutos por defecto
    
    with col2:
        tipo_cita = st.selectbox("🏥 Tipo de cita",
                                options=[
                                    "consulta_general",
                                    "vacunacion", 
                                    "esterilizacion",
                                    "urgencia",
                                    "revision",
                                    "cirugia"
                                ],
                                format_func=lambda x: {
                                    "consulta_general": "Consulta General",
                                    "vacunacion": "Vacunación",
                                    "esterilizacion": "Esterilización",
                                    "urgencia": "Urgencia",
                                    "revision": "Revisión",
                                    "cirugia": "Cirugía"
                                }[x],
                                index=0 if not cita_data else None)

    motivo = st.text_area("📝 Motivo de la consulta", 
                         value=cita_data.get('motivo') if cita_data else "",
                         height=100)
    
    observaciones = st.text_area("📋 Observaciones adicionales", 
                                value=cita_data.get('observaciones') if cita_data else "",
                                height=100)

    # Estado de la cita (solo para edición)
    if cita_data:
        estado = st.selectbox("📊 Estado de la cita",
                             options=[
                                 "programada",
                                 "confirmada", 
                                 "en_progreso",
                                 "completada",
                                 "cancelada",
                                 "no_asistio"
                             ],
                             format_func=lambda x: {
                                 "programada": "Programada",
                                 "confirmada": "Confirmada",
                                 "en_progreso": "En Progreso",
                                 "completada": "Completada",
                                 "cancelada": "Cancelada",
                                 "no_asistio": "No Asistió"
                             }[x],
                             index=0 if not cita_data.get('estado') else None)
    else:
        estado = "programada"

    # Botones de acción
    col1, col2, col3 = st.columns([1, 1, 1])

    if st.session_state['cita_registrada_exito']:
        # Mensaje de éxito personalizado que simula el div de alerta
        st.markdown("""
        <div role="alert" data-baseweb="notification" data-testid="stAlertContainer" 
             style="background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 8px; padding: 1rem; margin: 1rem 0; display: flex; align-items: center; justify-content: center; text-align: center; min-height: 60px;">
            <div style="width: 100%; color: #155724; font-size: 1.1rem; font-weight: bold;">
                ✅ Cita agendada exitosamente
            </div>
        </div>
        """, unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Agendar otra cita", key="agendar_otra_cita_btn"):
                st.session_state['cita_registrada_exito'] = False
                st.session_state['cita_editar'] = None
                st.rerun()
        with col_b:
            if st.button("Volver al listado", key="volver_listado_cita_btn"):
                st.session_state['mostrar_formulario_cita'] = False
                st.session_state['cita_editar'] = None
                st.session_state['cita_registrada_exito'] = False
                st.rerun()
    else:
        with col1:
            if st.button("💾 Guardar"):
                if not motivo.strip():
                    if cita_data:
                        st.markdown('''<div style="background:#fff3cd; border-left:6px solid #ffecb5; padding:12px 18px; border-radius:8px; margin-bottom:10px;">
                            <span style="color:#111; font-size:1.1rem; font-weight:bold;">Error al editar cita</span>
                        </div>''', unsafe_allow_html=True)
                    else:
                        st.markdown('''<div style="background:#fff3cd; border-left:6px solid #ffecb5; padding:12px 18px; border-radius:8px; margin-bottom:10px;">
                            <span style="color:#111; font-size:1.1rem; font-weight:bold;">No se puede agendar cita</span>
                        </div>''', unsafe_allow_html=True)
                    return
                
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    
                    if cita_data:  # Editar
                        query = """
                            UPDATE citas 
                            SET fecha_hora=%s, duracion_minutos=%s, tipo=%s, estado=%s, 
                                motivo=%s, observaciones=%s, id_mascota=%s, id_veterinario=%s, id_dueño=%s
                            WHERE id=%s
                        """
                        cursor.execute(query, (
                            fecha_hora, duracion, tipo_cita, estado, motivo, observaciones,
                            mascota_info['id'], id_veterinario, mascota_info['id_dueño'], cita_data['id']
                        ))
                        # Mensaje de éxito personalizado que simula el div de alerta
                        st.markdown("""
                        <div role="alert" data-baseweb="notification" data-testid="stAlertContainer" 
                             style="background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 8px; padding: 1rem; margin: 1rem 0; display: flex; align-items: center; justify-content: center; text-align: center; min-height: 60px;">
                            <div style="width: 100%; color: #155724; font-size: 1.1rem; font-weight: bold;">
                                ✅ Cita actualizada exitosamente
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:  # Nueva
                        query = """
                            INSERT INTO citas 
                            (fecha_hora, duracion_minutos, tipo, estado, motivo, observaciones, 
                             id_mascota, id_veterinario, id_dueño)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(query, (
                            fecha_hora, duracion, tipo_cita, estado, motivo, observaciones,
                            mascota_info['id'], id_veterinario, mascota_info['id_dueño']
                        ))
                        st.session_state['cita_registrada_exito'] = True
                    
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                except Exception as e:
                    st.error(f"❌ Error al guardar: {e}")
        
        with col2:
            if st.button("🔄 Limpiar"):
                st.rerun()
        
        with col3:
            if st.button("⬅️ Volver al listado"):
                st.session_state['mostrar_formulario_cita'] = False
                st.session_state['cita_editar'] = None
                st.rerun()
