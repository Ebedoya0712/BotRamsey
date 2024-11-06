import streamlit as st
import src.scraping.scraper as sp #funciones de scraping de recetas


def main():
    # Configurar la página de la aplicación con título y diseño centrado
    st.set_page_config(page_title="BotRamsey", layout="centered")
    st.title("Bienvenido a BotRamsey")

    # Inicialización de los estados en la sesión
    if 'mensajes' not in st.session_state:
        st.session_state.mensajes = []
    if 'paso' not in st.session_state or st.session_state['salir']:
        st.session_state.paso = 0
    if 'preparar' not in st.session_state:
        st.session_state['preparar'] = False
    if 'siguiente' not in st.session_state:
        st.session_state['siguiente'] = False
        st.session_state['salir'] = False
    if 'cronometro' not in st.session_state:
        st.session_state['cronometro'] = False
        st.session_state.tiempo = 0
    if 'Base' not in st.session_state:
        st.session_state.Base = sp.cargar_datos()

    cargar_historial(st.session_state.mensajes)
    sp.guardar_archivos(st.session_state.Base)
    chat()

def chat():
    # Solicitar entrada del usuario sobre qué receta buscar
    if mensaje := st.chat_input("¿Qué vamos a cocinar hoy?"):
        with st.chat_message("user"):
            st.markdown(mensaje)
            st.session_state.mensajes.append({"role": "user", "content": mensaje})
        
            # Buscar la receta y mostrar la respuesta del asistente
        with st.chat_message("assistant", avatar="https://www.firecrackercommunications.com/site/wp-content/uploads/2012/01/Gordonramsay.jpg"):
            try:
                respuesta = sp.buscar_receta(mensaje)
                st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
                st.button("Ver Preparación", key="preparar")
            except AttributeError:
                st.subheader("Lamentablemente no dispongo de esa receta")

    elif st.session_state['cronometro']:
        # Iniciar el temporizador si está activo
        sp.temporizador(st.session_state.tiempo)
        st.session_state['siguiente'] = True
        st.session_state.paso += 1

    elif st.session_state['preparar'] or st.session_state['siguiente']:
        # Mostrar los pasos de la receta
        if st.button("Siguiente paso", key="siguiente"):
            st.session_state.paso += 1

        with st.chat_message("assistant", avatar="https://www.firecrackercommunications.com/site/wp-content/uploads/2012/01/Gordonramsay.jpg"):
            sp.mostrar_pasos(st.session_state.mensajes[-1]["content"])
        st.button("Salir", key="salir")


def cargar_historial(historial):
    # Cargar el historial de mensajes de la sesión
    for mensaje in historial:
        with st.chat_message(mensaje["role"]):
            if mensaje["role"] == "user":
                st.markdown(mensaje["content"])
            else:
                sp.obtener_receta(mensaje["content"])

if __name__ == "__main__":
    main()  