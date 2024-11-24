import streamlit as st
import analisis
import src.scraping.scraper as sp  # funciones de scraping de recetas
import data_usuario as du


def main():
    # Configurar la página de la aplicación con título y diseño centrado
    st.set_page_config(page_title="BotRamsey", layout="centered")
    st.title("Bienvenido a BotRamsey")

    # Inicialización de los estados en la sesión
    inicializar_estado()
    sp.guardar_archivos(st.session_state.Base)  # Guardar archivos actualizados

    if st.button("ver analisis") or st.session_state['analisis']:
        analisis.graficar()
        st.session_state['analisis'] = True
        st.button("Salir", key="salir")
    elif st.button("Ver Informacion de usuario") or st.session_state['informacion']:
        du.generar_ui_usuario()
        st.session_state['informacion'] = True
        st.button("Salir", key="salir")
    else:   
        cargar_historial(st.session_state.mensajes)  # Cargar historial de chat
        chat()

def inicializar_estado():
    ### Inicializa los valores de sesión al inicio o si es necesario reiniciar ### 
    defaults = {
        'mensajes': [],
        'paso': 0,
        'preparar': False,
        'siguiente': False,
        'analisis':False,
        'salir': False,
        'cronometro': False,
        'tiempo': 0,
        'informacion': False
    }
    if 'Base' not in st.session_state:
        st.session_state.Base = sp.cargar_datos()
        reproducir_audio("Hola, bienvenido al sistema de Recetas de BotRamsey")
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if st.session_state['salir']:
        st.session_state['paso'] = 0
        st.session_state['analisis'] = False
        st.session_state['informacion'] = False


def chat():
    ### Manejo del flujo de interacción con el usuario en el chat ### 
    if mensaje := st.chat_input("¿Qué vamos a cocinar hoy?"):
        manejar_mensaje_usuario(mensaje)
    elif st.session_state['cronometro']:
        # Iniciar el temporizador si está activo
        sp.temporizador(st.session_state.tiempo)
        st.session_state['siguiente'] = True
        st.session_state.paso += 1
    elif st.session_state['preparar'] or st.session_state['siguiente']:
        manejar_pasos_receta()


def manejar_mensaje_usuario(mensaje):
    ### Procesa y responde al mensaje del usuario ### 
    with st.chat_message("user"):
        st.markdown(mensaje)
        st.session_state.mensajes.append({"role": "user", "content": mensaje})

    with st.chat_message("assistant", avatar="proyecto_recetas/src/Media/Avatar.jpg"):
        respuesta = sp.buscar_receta(mensaje)
        st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
        if respuesta:
            st.button("Ver Preparación", key="preparar")

            


def manejar_pasos_receta():
    ### Muestra los pasos de preparación de la receta ### 
    if st.button("Siguiente paso", key="siguiente"):
        st.session_state.paso += 1

    with st.chat_message("assistant", avatar="proyecto_recetas/src/Media/Avatar.jpg"):
        sp.mostrar_pasos(st.session_state.mensajes[-1]["content"])

    if st.button("Salir", key="salir"):
        st.session_state['salir'] = True
        st.session_state['paso'] = 0


def cargar_historial(historial):
    ### Carga el historial de mensajes de la sesión ### 
    for mensaje in historial:
        with st.chat_message(mensaje["role"], avatar="proyecto_recetas/src/Media/Avatar.jpg" if mensaje["role"] == "assistant" else None):
            if mensaje["role"] == "user":
                st.markdown(mensaje["content"])
            else:
                sp.obtener_receta(mensaje["content"])


if __name__ == "__main__":
    main()
