import streamlit as st
from groq import Groq

# Configuración básica

# Le agregamos el nombre a la pestaña y un ícono. Esta configuración tiene que ser la primer linea de streamlit.
st.set_page_config(page_title="Mi chat de IA", page_icon="🤖", layout="centered")

# Título de la aplicación
st.title("Mi Primera Aplicación")

# Entrada de texto
nombre = st.text_input("¿Cuál es tu nombre?")

if st.button("Saludar"):
    st.write(f"¡Hola, {nombre}! Bienvenido/a, Gracias por venir a Talento Tech")

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768'] # Se modifica en Clase 7

def configurar_pagina():
    # Agregamos un título principal a nuestra página
    st.title("Mi chat de IA")
    st.sidebar.title("Configuración de la IA") # Creamos un sidebar con un título.
    elegirModelo =  st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, index=0)
    return elegirModelo

# modelo = configurar_pagina()

# Clase 7: Configuración del modelo y variables de estado
# Seguridad: Nunca subas tu archivo secrets.toml a un repositorio público.
# La gestión de secretos debe hacerse directamente a través de la interfaz de Streamlit Cloud.

# Ciente
def crear_usuario_groq():
    claveSecreta = st.secrets["clave_api"]
    return Groq(api_key=claveSecreta)


def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

# clienteUsuario = crear_usuario_groq()
# inicializar_estado() #Captura el mensaje del usuario

#Clase 08 - Actualizar historial, Mostrar historial, area del chat
#Actualizar historial.

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content":contenido, "avatar": avatar})

#Mostrar Historial
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]):
            st.markdown(mensaje["content"])


#area_chat
def area_chat():
    contenedorDelChat = st.container(height=300, border=True)
    with contenedorDelChat:
        mostrar_historial()

#Clase 9 - Funcion generar respuesta y Funcion Principal. Nos preparamos para el deploy
def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado() #Captura el mensaje del usuario
    area_chat()
    mensaje = st.chat_input("Escribí tu mensaje:")
    if mensaje:
        actualizar_historial("user",mensaje,"👦")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistent", respuesta_completa,"🤖")
        st.rerun()


if __name__ == "__main__":
    main()























































    





