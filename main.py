import streamlit as st
import base64
from Login.login import login
from Pages import (
    V_Veterianario, V_Doctor, V_Secretaria, V_Paciente,
    V_Admin, Citas, Historial_Medico, Notas, Paciente,
    Prediccion_IA, Tratamientos, Usuarios
)
from streamlit_option_menu import option_menu

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

st.set_page_config(
    page_title="Medical Pets",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- BLOQUE CSS GLOBAL PARA FORMULARIOS ----------
st.markdown("""
<style>
/* Estilo general para todos los inputs y selects */
input[type="text"], input[type="password"], input[type="email"], textarea, select, input[type="number"] {
    background-color: #E0FCFC !important;
    border: 2px solid #00C2C2 !important;
    color: #222 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding-left: 10px !important;
}
input[type="number"] {
    /* Asegura que el fondo de number input sea igual */
    background-color: #E0FCFC !important;
    color: #222 !important;
}
/* Color y tamaño para los botones de aumentar/disminuir */
input[type="number"]::-webkit-inner-spin-button, 
input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    background: #00C2C2 !important;
    border-radius: 4px !important;
    width: 18px;
    height: 28px;
    margin: 1px;
}
input[type="number"]:hover::-webkit-inner-spin-button,
input[type="number"]:hover::-webkit-outer-spin-button {
    background: #34CACA !important;
}
input[type="number"]::-webkit-inner-spin-button:active,
input[type="number"]::-webkit-outer-spin-button:active {
    background: #009999 !important;
}
input::placeholder, textarea::placeholder {
    color: #00A3A3 !important;
    opacity: 1 !important;
    font-weight: 500 !important;
}
/* Firefox (ocultar flechas si quieres un look limpio)
input[type="number"]::-moz-number-spin-box,
input[type="number"]::-moz-number-spin-up,
input[type="number"]::-moz-number-spin-down {
    background: #00C2C2 !important;
    border-radius: 4px !important;
} */
label, .stSelectbox label, .stTextInput label, .stTextArea label {
    color: #004D4D !important;
    font-weight: bold !important;
}
/* Menú desplegable de selectbox */
.stSelectbox [data-baseweb="select"]>div {
    background-color: #E0FCFC !important;
    color: #222 !important;
}
</style>
""", unsafe_allow_html=True)

# --- CSS para ocultar la barra automática y dejar solo tu menú + colores de botones ---
st.markdown("""
    <style>
    /* Oculta el selector de páginas streamlit-multipage */
    section[data-testid="stSidebarNav"] { display: none !important; }
    /* Oculta el bloque completo del primer menú lateral */
    div[class^="st-emotion-cache-79elbk"] { display: none !important; }
    /* Oculta barrita superior Streamlit */
    header, #MainMenu, footer { visibility: hidden; height: 0; padding: 0; }
    body, .main, .block-container { background-color: #C9F7F7 !important; color: #000; }
    [data-testid="stSidebar"] > div:first-child {
        background-color: #34CACA !important;
        padding-top: 0px !important;
    }
    /* BOTONES TURQUESA GLOBALES */
    .stButton>button, .icon-button, .edit-btn, .delete-btn {
        background-color: #34CACA !important;
        color: #fff !important;
        font-weight: bold;
        border: none !important;
        border-radius: 10px !important;
        transition: background-color 0.3s;
        box-shadow: none !important;
    }
    .stButton>button:hover, .icon-button:hover, .edit-btn:hover, .delete-btn:hover {
        background-color: #00C2C2 !important;
        color: #fff !important;
    }
    </style>
""", unsafe_allow_html=True)

if 'usuario' not in st.session_state:
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)
    login()
    st.stop()

col1, col2 = st.columns([0.9, 0.1])
with col2:
    if st.button("Cerrar sesión", key="logout_btn", type="primary"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.success("Sesión cerrada correctamente")
        st.rerun()

with st.sidebar:
    st.markdown(
        f"<div style='text-align:center; font-weight:bold; color:white; padding:20px 0;'>"
        f"Usuario: {st.session_state['usuario'].capitalize()}"
        "</div>",
        unsafe_allow_html=True
    )
    PAGINAS_POR_ROL = {
        'admin':       ['Inicio','Citas','Historial Medico','Notas','Paciente','Prediccion IA','Tratamientos','Usuarios','V Admin'],
        'veterinario': ['Inicio','Citas','Historial Medico','Notas','Paciente','Prediccion IA','Tratamientos','Usuarios','V Veterinario'],
        'doctor':      ['Inicio','Citas','Historial Medico','Notas','Paciente','Prediccion IA','Tratamientos','Usuarios','V Doctor'],
        'paciente':    ['Inicio','Paciente','Citas','Tratamientos','V Paciente','Notas'],
        'secretaria':  ['Inicio','Usuarios','Paciente','Citas','V Secretaria']
    }
    rol_actual = st.session_state['rol']
    paginas_visibles = PAGINAS_POR_ROL.get(rol_actual, [])

    seleccion = option_menu(
        menu_title=None,
        options=paginas_visibles,
        icons=[
            "house", "calendar-check", "journal-medical", "file-text",
            "person", "activity", "clipboard-check", "people",
            "shield-person"
        ][:len(paginas_visibles)],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0", "background-color": "#34CACA"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px", "text-align": "left",
                "margin": "0px", "color": "white",
                "--hover-color": "#00A3A3"
            },
            "nav-link-selected": {"background-color": "#00C2C2", "color": "white"},
        }
    )

image_path = "Recursos/logo.png"
image_b64 = image_to_base64(image_path)

if seleccion == 'Inicio':
    st.markdown(f"""
        <div style="text-align:center; margin-top:50px;">
            <h1 style="color:#004D4D;">
                ¡Bienvenido/a <span style='color:#00C2C2;'>{st.session_state['usuario'].capitalize()}</span>!
            </h1>
            <img src="data:image/png;base64,{image_b64}" width="620" style="border-radius:16px;"/>
            <h2 style="color:#004D4D;">Medical <span style='color:#00C2C2;'>Pets</span></h2>
        </div>
    """, unsafe_allow_html=True)

elif seleccion == 'V Admin':
    V_Admin.main()
elif seleccion == 'V Doctor':
    V_Doctor.main()
elif seleccion == 'V Paciente':
    V_Paciente.main()
elif seleccion == 'V Secretaria':
    V_Secretaria.main()
elif seleccion == 'V Veterinario':
    V_Veterianario.main()
elif seleccion == 'Citas':
    Citas.main()
elif seleccion == 'Historial Medico':
    Historial_Medico.main()
elif seleccion == 'Notas':
    Notas.main()
elif seleccion == 'Paciente':
    Paciente.main()
elif seleccion == 'Prediccion IA':
    Prediccion_IA.main()
elif seleccion == 'Tratamientos':
    Tratamientos.main()
elif seleccion == 'Usuarios':
    Usuarios.main()
