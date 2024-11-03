from bs4 import BeautifulSoup
import requests
import streamlit as st
import time


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

    cargar_historial(st.session_state.mensajes)
    chat()


def chat():
    # Solicitar entrada del usuario sobre qué receta buscar
    if mensaje := st.chat_input("¿Qué vamos a cocinar hoy?"):
        with st.chat_message("user"):
            st.markdown(mensaje)
            st.session_state.mensajes.append({"role": "user", "content": mensaje})
        try:
            # Buscar la receta y mostrar la respuesta del asistente
            with st.chat_message("assistant", avatar="https://www.firecrackercommunications.com/site/wp-content/uploads/2012/01/Gordonramsay.jpg"):
                respuesta = buscar_receta(mensaje)
                st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
                st.button("Ver Preparación", key="preparar")
        except:
            st.subheader("Lamentablemente no dispongo de esa receta")

    elif st.session_state['cronometro']:
        # Iniciar el temporizador si está activo
        temporizador(st.session_state.tiempo)
        st.session_state['siguiente'] = True
        st.session_state.paso += 1

    elif st.session_state['preparar'] or st.session_state['siguiente']:
        # Mostrar los pasos de la receta
        if st.button("Siguiente paso", key="siguiente"):
            st.session_state.paso += 1

        with st.chat_message("assistant", avatar="https://www.firecrackercommunications.com/site/wp-content/uploads/2012/01/Gordonramsay.jpg"):
            mostrar_pasos(st.session_state.mensajes[-1]["content"])
        st.button("Salir", key="salir")


def cargar_historial(historial):
    # Cargar el historial de mensajes de la sesión
    for mensaje in historial:
        with st.chat_message(mensaje["role"]):
            if mensaje["role"] == "user":
                st.markdown(mensaje["content"])
            else:
                obtener_receta(mensaje["content"])


def obtener_receta(enlace):
    # Extraer información de la receta de la página web
    sopa = obtener_contenido(enlace)
    titulo = sopa.find('h1', class_='titulo titulo--articulo')
    propiedades = [prop.get_text() for prop in sopa.find('div', class_='properties').find_all('span')]
    ingredientes = [ing.get_text() for ing in sopa.find('div', class_='ingredientes').find_all('label')]

    st.subheader(titulo.get_text())
    st.write("\n\n".join(propiedades))

    st.subheader("Lista De Ingredientes")
    st.write("\n\n".join(ingredientes))


def obtener_contenido(enlace):
    # Realizar una solicitud HTTP para obtener el contenido HTML de la página
    respuesta = requests.get(enlace)
    contenido = respuesta.text
    sopa = BeautifulSoup(contenido, 'lxml')
    return sopa


def mostrar_pasos(enlace):
    # Extraer y mostrar los pasos de preparación de la receta
    sopa = obtener_contenido(enlace)
    pasos = list(map(lambda x: x.get_text(), sopa.find_all("div", class_="apartado")))

    if st.session_state.paso < len(pasos):
        st.subheader("Pasos de preparación:")
        st.write(pasos[st.session_state.paso] + "\n\n")

        # Si hay una referencia a "minuto", iniciar el cronómetro
        if "minuto" in pasos[st.session_state.paso]:
            indice = pasos[st.session_state.paso].index("minuto") - 2
            tiempo = pasos[st.session_state.paso][indice]     
            while pasos[st.session_state.paso][indice - 1].isdigit():
                tiempo = pasos[st.session_state.paso][indice - 1] + tiempo
                indice -= 1 
            st.session_state.tiempo = int(tiempo)
            st.button("Iniciar cronómetro", key="cronometro")


def buscar_receta(busqueda):
    # Buscar recetas en la web y obtener el primer enlace
    busqueda = busqueda.replace(" ", "+")
    enlace_web = f"https://www.recetasgratis.net/busqueda?q={busqueda}"
    sopa = obtener_contenido(enlace_web)
    resultado = sopa.find('div', class_='resultado link')
    enlace = resultado.find('a')
    obtener_receta(enlace.get('href'))

    return enlace.get('href')


def temporizador(minutos):
    # Temporizador que cuenta hacia atrás
    marcador = st.empty()
    st.button("Siguiente paso", key="siguiente")

    for i in range(minutos, 0, -1):
        for j in range(60, 0, -1):
            with marcador:
                st.write(f"\rTiempo restante: {i-1} minutos : {j-1} segundos")
            time.sleep(1)

    st.write("\n¡Tiempo finalizado!")


if __name__ == "__main__":
    main()  