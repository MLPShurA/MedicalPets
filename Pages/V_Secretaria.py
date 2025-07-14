import streamlit as st

def main():
    st.title("Ventana de la SECRETARIA")
    st.write("Bienvenido "f": {st.session_state['usuario']}")