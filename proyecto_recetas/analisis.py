# Importar librerías necesarias
import pandas as pd
import os
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import src.limpieza.procesar_datos as prd
import json



def graficar():
    clasificacion, df = cargar()

    prd.procesar_datos(df)

# Configuración de la interfaz en Streamlit
    st.title('Recetas y Valoración')

# Sidebar para los filtros
    st.sidebar.header('Filtros')
    df = filtros(clasificacion, df)

# Mostrar la tabla de datos de las recetas con la duración formateada
    st.subheader('Datos de las recetas')
    st.dataframe(df[['Recetas', 'Duracion', 'Dificultad', 'Valoracion', "Tipo"]])

    estilo()

    st.title("Análisis de Recetas")

    DuracionVsDificultad(df)

    DificultadVsValoracion(df)

    DuracionVsValoracion(df)

    barrasDificultad(df)



def formato_tiempo(ax):
    ax.xaxis.set_major_locator(ticker.MultipleLocator(120))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x // 60)}h {int(x % 60)}m' if (x >= 60) else f'{int(x)}m'))



def DificultadVsValoracion(df):
    st.subheader("Dificultad vs Valoración")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=df, x='Dificultad', y='Valoracion', ax=ax)
    ax.set_facecolor('black')
    plt.title("Dificultad vs Valoración", fontsize=16, color='white')
    plt.xlabel("Dificultad", fontsize=14, color='white')
    plt.ylabel("Valoración (%)", fontsize=14, color='white')
    st.pyplot(fig)



def DuracionVsDificultad(df):
    st.subheader(f"Duración vs Dificultad")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=df, x='Duracion', y="Dificultad", ax=ax)
    ax.set_facecolor('black')
    formato_tiempo(ax)
    plt.title(f"Duración vs Dificultad", fontsize=16, color='white')
    plt.xlabel("Duración", fontsize=14, color='white')
    plt.ylabel("Dificultad", fontsize=14, color='white')
    ax.invert_yaxis()
    st.pyplot(fig)

def DuracionVsValoracion(df):
    st.subheader(f"Duración vs Valoracion")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=df, x='Duracion', y="Valoracion", ax=ax)
    ax.set_facecolor('black')
    formato_tiempo(ax)
    plt.title(f"Duración vs Valoracion", fontsize=16, color='white')
    plt.xlabel("Duración", fontsize=14, color='white')
    plt.ylabel("Valoracion", fontsize=14, color='white')
    st.pyplot(fig)



def barrasDificultad(df):
    st.subheader("Comparación de Niveles de Dificultad")
    fig, ax = plt.subplots(figsize=(10, 6))
    nivel_counts = df["Dificultad"].value_counts(sort= False)
    sns.barplot(data=nivel_counts, ax=ax)
    ax.set_facecolor('black')
    plt.title("Comparación de Niveles de Dificultad", fontsize=16, color='white')
    plt.xlabel("Nivel de Dificultad", fontsize=14, color='white')
    plt.ylabel("Cantidad de Recetas", fontsize=14, color='white')
    st.pyplot(fig)



def filtros(clasificacion, df):
    dificultad = st.sidebar.selectbox('Selecciona la dificultad', ['todas', 'alta', 'media', 'baja', 'muy baja'])
    tipo = st.sidebar.selectbox('Selecciona Tipo', ['todas']+list(clasificacion.keys()))

    if dificultad != 'todas':
        df = df[df['Dificultad'] == dificultad]

    if tipo != 'todas':
        df = df[df['Tipo'].isin(clasificacion[tipo])]

    return df



def cargar():
    # datos del formato de clasificacion en json
    with open('proyecto_recetas/data/clasificacion.json', 'r') as f:
        clasificacion = json.load(f)

    # datos del historial de recetas en csv
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
    plt.rcParams.update({
        'axes.facecolor': 'black',
        'figure.facecolor': 'black',
        'savefig.facecolor': 'black',
        'text.color': 'white',
        'axes.labelcolor': 'white',
        'xtick.color': 'white',
        'ytick.color': 'white',
        'legend.facecolor': 'black'
    })
