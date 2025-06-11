import streamlit as st
import groq

st.set_page_config(page_title="mi primera pagina web con python", page_icon="😎")

MODELOS = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]

def configurar_pagina():
    st.title("pagina chatbot")

def mostrar_sidebar():
    st.sidebar.title("elegi tu IA")
    modelo = st.sidebar.selectbox("tu favorito", MODELOS, index=0)
    st.write(f"elegiste la IA : {modelo}")
    return modelo

def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groq_api_key)

def configurar_modelo(cliente, modelo, mensajedeentrada):
    # Aquí deberías obtener la respuesta del modelo, no un stream
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajedeentrada}]
    )
    return respuesta.choices[0].message.content

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat:
        st.markdown("### Chat")
        st.chat_message("system", avatar="https://cdn-icons-png.flaticon.com/512/1946/1946429.png")
        st.markdown("Hola, soy tu asistente virtual. ¿En qué puedo ayudarte hoy?")
        mostrar_historial()

if __name__ == "__main__":
    configurar_pagina()
    elegituIA = mostrar_sidebar()
    clienteUsuario = crear_cliente_groq()
    inicializar_estado()
    area_chat()
    mensaje = st.chat_input("Escribí tu mensaje:")

    if mensaje:
        actualizar_historial("user", mensaje, None)
        chat_completo = configurar_modelo(clienteUsuario, elegituIA, mensaje)
        actualizar_historial("assistant", chat_completo, "https://cdn-icons-png.flaticon.com/512/1946/1946429.png")
        st.rerun()

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
    return respuesta_completa
