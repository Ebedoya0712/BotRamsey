#En este archivo se van a manejar el codigo para poder realizar web scrapin a las recetas de las siguientes paginas:
#www.recetasgratis.net
from bs4 import BeautifulSoup
import requests
import streamlit as st
import time
import json
import pandas as pd
import os


def obtener_receta(enlace):
    # Extraer información de la receta de la página web
    sopa = obtener_contenido(enlace)
    titulo = sopa.find('h1', class_='titulo titulo--articulo').get_text()
    propiedades = [prop.get_text() for prop in sopa.find('div', class_='properties').find_all('span')]
    ingredientes = [ing.get_text() for ing in sopa.find('div', class_='ingredientes').find_all('label')]

    guardar_datos(titulo, propiedades, ingredientes)

    st.subheader(titulo)
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

def guardar_datos(titulo, propiedades, ingredientes):
    if titulo in st.session_state.Base.keys():
        return 0
    else:
        Receta = {"ingredientes" : [ingrediente.strip() for ingrediente in ingredientes], "Duracion": propiedades[1]}

        for i in propiedades:
            if "Dificultad" in i:
                Receta["Dificultad"] = " ".join(i.split()[1:])

        st.session_state.Base[titulo] = Receta

def guardar_archivos(Base):
    if len(Base) != 0:
        with open('proyecto_recetas/data/recetas.json', 'w') as f:
            json.dump(Base, f, indent=4)
        
        data = {
            "Recetas" : list(Base.keys()),
            "Duracion" : [Base[i]['Duracion'] for i in Base],
            "Dificultad" : [Base[i]['Dificultad'] for i in Base],
        }

        df = pd.DataFrame(data)
        df.to_csv('proyecto_recetas/data/recetas.csv', index=False)



def cargar_datos():
    if os.path.exists('proyecto_recetas/data/recetas.json'):
        with open('proyecto_recetas/data/recetas.json', 'r') as f:
            return json.load(f)
    else:
        return {}