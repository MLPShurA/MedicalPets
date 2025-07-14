import streamlit as st

def main():
    st.title("Ventana del PACIENTE")
    st.write("Bienvenido "f": {st.session_state['usuario']}")