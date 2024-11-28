import streamlit as st
import pandas as pd
import json
import src.limpieza.procesar_datos as prd

# Funciones para cargar y procesar datos
def cargar_datos():
    df = pd.read_csv('proyecto_recetas/data/recetas.csv')
    prd.procesar_datos(df)
    return df

def calcular_promedios():
    df = cargar_datos()
    promedio_duracion = int(df['Duracion'].mean())
    dificultad_promedio = df['Dificultad'].value_counts().idxmax()
    return promedio_duracion, dificultad_promedio

def receta_favorita():
    df = cargar_datos()
    with open('proyecto_recetas/data/clasificacion.json', 'r') as f:
        clasificacion = json.load(f)

    mayor = 0
    recetafav = None
    for tipo in clasificacion.keys():
        aux = len((df[df['Tipo'].isin(clasificacion[tipo])]))
        if mayor < aux:
            mayor = aux
            recetafav = tipo
    return mayor, recetafav

def generar_ui_usuario():

    st.title("Perfil del Usuario")

    st.header("📊 Estadísticas Generales")
    promedio_duracion, dificultad_promedio = calcular_promedios()
    st.metric("Duración Promedio de Recetas", f"{promedio_duracion} minutos")
    st.metric("Dificultad más Común", dificultad_promedio)

    st.header("💖 Receta Favorita")
    mayor, recetafav = receta_favorita()
    st.subheader("Tipo de Receta Favorita")
    st.write(f"**{recetafav}** con un total de **{mayor} recetas**.")
    st.markdown("---")
    st.header("📄 Resumen de Recetas")
    df = cargar_datos()
    st.dataframe(df)



