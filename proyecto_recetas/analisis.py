# Importar librerías necesarias
import pandas as pd
import os
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import src.limpieza.procesar_datos as prd
import json

def graficar():
    clasificacion, df = cargar()

    prd.procesar_datos(df)
    
    st.title('Recetas y Valoración')

    st.sidebar.header('Filtros')
    df = filtros(clasificacion, df)

    # Mostrar la tabla de datos de las recetas 
    st.subheader('Datos de las recetas')
    st.dataframe(df[['Recetas', 'Duracion', 'Dificultad', 'Valoracion', "Tipo"]])

    estilo()

    st.title("Análisis de Recetas")

    DurvsDif(df)

    DifvsVal(df)

    DvsV(df)

    Barras(df)

def DurvsDif(df):
    st.subheader("Duración vs Dificultad")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=df, x='Duracion', y='Dificultad', ax=ax)
    ax.set_facecolor('black')
    plt.title("Duración vs Dificultad", fontsize=16, color='white')
    plt.xlabel("Duración (minutos)", fontsize=14, color='white')
    plt.ylabel("Dificultad", fontsize=14, color='white')
    st.pyplot(fig)

def DifvsVal(df):
    st.subheader("Dificultad vs Valoración")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=df, x='Dificultad', y='Valoracion', ax=ax)
    ax.set_facecolor('black')
    plt.title("Dificultad vs Valoración", fontsize=16, color='white')
    plt.xlabel("Dificultad", fontsize=14, color='white')
    plt.ylabel("Valoración (%)", fontsize=14, color='white')
    st.pyplot(fig)

def DvsV(df):
    st.subheader("Duración vs Valoración")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=df, x='Duracion', y='Valoracion', ax=ax)
    ax.set_facecolor('black')
    plt.title("Duración vs Valoración", fontsize=16, color='white')
    plt.xlabel("Duración (minutos)", fontsize=14, color='white')
    plt.ylabel("Valoración (%)", fontsize=14, color='white')
    st.pyplot(fig)

def Barras(df):
    # Gráfico de barras: comparación de niveles de dificultad
    st.subheader("Comparación de Niveles de Dificultad")
    fig, ax = plt.subplots(figsize=(10, 6))
    nivel_counts = df['Dificultad'].value_counts()
    nivel_counts.plot(kind='bar', ax=ax)
    ax.set_facecolor('black')
    plt.title("Comparación de Niveles de Dificultad", fontsize=16, color='white')
    plt.xlabel("Nivel de Dificultad", fontsize=14, color='white')
    plt.ylabel("Cantidad de Recetas", fontsize=14, color='white')
    st.pyplot(fig)

def filtros(clasificacion, df):
    dificultad = st.sidebar.selectbox('Selecciona la dificultad', ['todas', 'alta', 'media', 'baja', 'muy baja'])
    tipo = st.sidebar.selectbox('Selecciona Tipo', ['todas']+list(clasificacion.keys()))

    # Filtrar DataFrame por dificultad y tipo
    if dificultad != 'todas':
        df = df[df['Dificultad'] == dificultad]

    if tipo != 'todas':
        df = df[df['Tipo'].isin(clasificacion[tipo])]
    return df

def cargar():
    # cargar datos del csv y el json de clasificaciones
    with open('proyecto_recetas/data/clasificacion.json', 'r') as f:
        clasificacion = json.load(f)

    ruta_archivo = 'proyecto_recetas/data/recetas.csv' 
    if os.path.exists(ruta_archivo):
        df = pd.read_csv(ruta_archivo)
    else:
        st.subheader("No hay datos que analizar")
        df = None
    return clasificacion,df

def estilo():
# Aplicar el estilo a los graficos
    sns.set_style("darkgrid")
    sns.set_palette("bright")

    plt.rcParams['axes.facecolor'] = 'black'
    plt.rcParams['figure.facecolor'] = 'black'
    plt.rcParams['savefig.facecolor'] = 'black'
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
    plt.rcParams['legend.facecolor'] = 'black'