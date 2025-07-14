import streamlit as st

def main():
    st.title("Ventana del VETERINARIO")
    st.write("Bienvenido "f": {st.session_state['usuario']}")