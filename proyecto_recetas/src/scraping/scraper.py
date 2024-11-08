#En este archivo se van a manejar el codigo para poder realizar web scrapin a las recetas de las siguientes paginas:
#www.recetasgratis.net

from bs4 import BeautifulSoup
import requests
import streamlit as st
import time
import json
import pandas as pd
import os

def obtener_contenido(enlace):
    ### Realiza una solicitud HTTP y devuelve el contenido en formato BeautifulSoup ### 
    try:
        respuesta = requests.get(enlace)
        respuesta.raise_for_status()
        return BeautifulSoup(respuesta.text, 'html.parser')
    except requests.RequestException:
        st.subheader("Lamentablemente no dispongo de esa receta")
        return None



def obtener_receta(enlace):
    ### Extrae información de la receta de la página y la muestra ### 
    sopa = obtener_contenido(enlace)
    if not sopa:
        return

    titulo = sopa.find('h1', class_='titulo titulo--articulo').get_text(strip=True)
    tipo = sopa.find('a', class_='post-categoria-link').get_text(strip=True)
    valoracion = sopa.find('div', class_='valoracion').get('style', '').split(':')[-1].strip()
    propiedades = [prop.get_text(strip=True) for prop in sopa.select('div.properties span')]
    ingredientes = [ing.get_text(strip=True) for ing in sopa.select('div.ingredientes label')]

    guardar_datos(titulo, propiedades, ingredientes, valoracion, tipo)

    st.subheader(titulo)
    st.write("\n\n".join(propiedades))
    st.write(f"Al {valoracion} de los usuarios les gusta esta receta")
    st.subheader("Lista De Ingredientes")
    st.write("\n\n".join(ingredientes))



def mostrar_pasos(enlace):
    ### Extrae y muestra los pasos de preparación de la receta ### 
    sopa = obtener_contenido(enlace)
    if not sopa:
        return

    pasos = [p.get_text() for p in sopa.select("div.apartado")]

    if st.session_state.paso < len(pasos):
        st.subheader("Pasos de preparación:")
        paso_actual = pasos[st.session_state.paso]
        st.write(paso_actual + "\n")

        if "minuto" in paso_actual:
            tiempo = extraer_minutos(paso_actual)
            if tiempo:
                st.session_state.tiempo = int(tiempo)
                st.button("Iniciar cronómetro", key="cronometro")



def extraer_minutos(texto):
    ### Extrae los minutos de un texto si se menciona la palabra 'minuto' ### 
    index = texto.find("minuto")
    if index != -1:
        tiempo_str = ''.join(filter(str.isdigit, texto[max(0, index - 3):index]))
        return tiempo_str if tiempo_str.isdigit() else None
    return None



def buscar_receta(busqueda):
    ### Busca recetas y obtiene el primer enlace ### 
    enlace_web = f"https://www.recetasgratis.net/busqueda?q={busqueda.replace(' ', '+')}"
    sopa = obtener_contenido(enlace_web)
    if not sopa:
        return None

    enlace = sopa.select_one('div.resultado.link a')
    if enlace:
        href = enlace.get('href')
        obtener_receta(href)
        return href
    return None



def temporizador(minutos):
    ### Temporizador que cuenta hacia atrás ### 
    marcador = st.empty()
    st.button("Siguiente paso", key="siguiente")

    for i in range(minutos * 60, 0, -1):
        with marcador:
            minutos_restantes, segundos_restantes = divmod(i, 60)
            st.write(f"Tiempo restante: {minutos_restantes} minutos : {segundos_restantes} segundos")
        time.sleep(1)

    st.write("\n¡Tiempo finalizado!")

# Funciones de Datos

def guardar_datos(titulo, propiedades, ingredientes, valoracion, tipo):
    ### Guarda la receta en la base de datos de sesión ### 
    if titulo not in st.session_state.Base:
        receta = {
            "ingredientes": [ingrediente.strip() for ingrediente in ingredientes],
            "Valoracion": valoracion,
            "Duracion": propiedades[1] if len(propiedades) > 1 else "Desconocido",
            "Dificultad": next((p.split()[-1] for p in propiedades if "Dificultad" in p), "Desconocida"),
            "Tipo": tipo
        }
        st.session_state.Base[titulo] = receta



def guardar_archivos(Base):
    ### Guarda la base de datos en archivos JSON y CSV ### 
    if Base:
        # Guardar JSON
        with open('proyecto_recetas/data/recetas.json', 'w', encoding='utf-8') as f:
            json.dump(Base, f, indent=4, ensure_ascii=False)

        # Guardar CSV
        data = {
            "Recetas": list(Base.keys()),
            "Duracion": [receta['Duracion'] for receta in Base.values()],
            "Dificultad": [receta['Dificultad'] for receta in Base.values()],
            "Valoracion": [receta['Valoracion'] for receta in Base.values()],
            "Tipo": [receta['Tipo'] for receta in Base.values()]
        }
        pd.DataFrame(data).to_csv('proyecto_recetas/data/recetas.csv', index=False, encoding='utf-8')



def cargar_datos():
    ### Carga los datos desde el archivo JSON si existe ### 
    path = 'proyecto_recetas/data/recetas.json'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}
