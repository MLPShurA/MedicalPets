import streamlit as st
from db import get_connection
from Login.security import verify_password
import base64

def verificar_usuario(usuario, contraseña):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    if resultado:
        if resultado.get('contrasena_hash'):
            if verify_password(contraseña, resultado['contrasena_hash']):
                return resultado
        elif contraseña == resultado.get('contrasena'):
            return resultado
    return None

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def login():
    st.markdown("""
    <style>
      html, body, .main, .block-container {
        background-color: #C9F7F7 !important;
        padding-top: 5px !important;
      }

      header, header > div {
        background-color: #C9F7F7 !important;
        border-bottom: none !important;
      }

      #MainMenu, footer {visibility: hidden;}

      div[data-testid="stForm"] {
        background-color: #FFFFFF;
        padding: 20px 30px;
        border-radius: 25px;
        max-width: 470px;
        margin: 5px auto 20px auto;
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        text-align: center;
      }

      div[data-testid="stForm"] .stImage > img {
        display: block;
        margin: 0 auto 20px auto;
        width: 130px;
        border-radius: 18px;
        box-shadow: 0 0 15px rgba(0,0,0,0.1);
      }

      div[data-testid="stForm"] h2.title {
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 30px;
        background: linear-gradient(90deg, #00C2C2, #34CACA);
        -webkit-background-clip: text;
        color: transparent;
      }

      input[type="text"], input[type="password"] {
        background-color: #E0FCFC !important;
        border: 2px solid #00C2C2 !important;
        padding-left: 10px !important;
        height: 45px !important;
        border-radius: 8px !important;
        color: #1C1C1C !important;
        font-weight: bold;
      }

      input::placeholder {
        color: #00A3A3 !important;
        font-weight: bold;
      }

      /* ✅ Estilo exclusivo del botón “Iniciar sesión” */
      div[data-testid="stFormSubmitButton"] button {
        background-color: #00C2C2 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        height: 45px !important;
        width: 100% !important;
        border: none !important;
        margin-top: 20px !important;
        transition: background-color 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
      }

      div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #34CACA !important;
      }
    </style>
    """, unsafe_allow_html=True)

    if 'logueado' not in st.session_state:
        st.session_state['logueado'] = False

    if not st.session_state['logueado']:
        col1, col2, col3 = st.columns([1, 2.5, 1])
        with col2:
            image_base64 = image_to_base64("Recursos/logo.png")

            with st.form(key="login_form"):
                st.image(f"data:image/png;base64,{image_base64}")
                st.markdown('<h2 class="title">MEDICAL PETS</h2>', unsafe_allow_html=True)

                usuario = st.text_input("", placeholder="👤 Usuario", label_visibility="collapsed")
                contraseña = st.text_input("", placeholder="🔒 Contraseña", type="password", label_visibility="collapsed")
                login_boton = st.form_submit_button("Iniciar sesión")

                if login_boton:
                    user_data = verificar_usuario(usuario, contraseña)
                    if user_data:
                        st.session_state['usuario'] = user_data['nombre_usuario']
                        st.session_state['rol'] = user_data['rol']
                        st.session_state['logueado'] = True
                        st.success("✅ Inicio de sesión correcto")
                        st.rerun()
                    else:
                        st.error("❌ Usuario o contraseña incorrectos")
    else:
        st.success(f"Bienvenido, {st.session_state['usuario']}")
