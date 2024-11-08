import pandas as pd
import os
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import src.limpieza.procesar_datos as prd
import json

def graficar():
    clasificacion, df = cargar_datos()

    if df is None:
        st.subheader("No hay datos que analizar")
        return

    prd.procesar_datos(df)

    # Configurar estilos
    estilo()

    # Mostrar título y filtros
    st.title('Recetas y Valoración')
    st.sidebar.header('Filtros')
    df_filtrado = aplicar_filtros(clasificacion, df)

    # Mostrar tabla de datos
    st.subheader('Datos de las recetas')
    st.dataframe(df_filtrado[['Recetas', 'Duracion', 'Dificultad', 'Valoracion', 'Tipo']])

    st.title("Análisis de Recetas")
    
    # Mostrar gráficos
    graficar_linea(df_filtrado, 'Duracion', 'Dificultad', "Duración vs Dificultad")
    graficar_linea(df_filtrado, 'Dificultad', 'Valoracion', "Dificultad vs Valoración")
    graficar_linea(df_filtrado, 'Duracion', 'Valoracion', "Duración vs Valoración")
    graficar_barras(df_filtrado, 'Dificultad', "Comparación de Niveles de Dificultad")


def cargar_datos():
    ### Cargar datos desde archivos CSV y JSON ###
    try:
        with open('proyecto_recetas/data/clasificacion.json', 'r') as f:
            clasificacion = json.load(f)
    except FileNotFoundError:
        st.error("Archivo de clasificación no encontrado.")
        return None, None

    ruta_csv = 'proyecto_recetas/data/recetas.csv'
    if not os.path.exists(ruta_csv):
        st.error("Archivo de recetas no encontrado.")
        return clasificacion, None

    df = pd.read_csv(ruta_csv)
    return clasificacion, df


def aplicar_filtros(clasificacion, df):
    ### Aplicar filtros de dificultad y tipo ###
    dificultad = st.sidebar.selectbox('Selecciona la dificultad', ['todas', 'alta', 'media', 'baja', 'muy baja'])
    tipo = st.sidebar.selectbox('Selecciona Tipo', ['todas'] + list(clasificacion.keys()))

    if dificultad != 'todas':
        df = df[df['Dificultad'] == dificultad]

    if tipo != 'todas':
        df = df[df['Tipo'].isin(clasificacion[tipo])]
    return df


def graficar_linea(df, x_col, y_col, titulo):
    ### gráficos de líneas ###
    if df.empty:
        st.warning(f"No hay datos suficientes para el gráfico: {titulo}")
        return

    st.subheader(titulo)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
    ax.set_facecolor('black')
    plt.title(titulo, fontsize=16, color='white')
    plt.xlabel(x_col, fontsize=14, color='white')
    plt.ylabel(y_col, fontsize=14, color='white')
    st.pyplot(fig)


def graficar_barras(df, col, titulo):
    ### Gráfico de barras para comparación de niveles ###
    if df.empty:
        st.warning("No hay datos suficientes para el gráfico de barras")
        return

    st.subheader(titulo)
    fig, ax = plt.subplots(figsize=(10, 6))
    nivel_counts = df[col].value_counts()
    nivel_counts.plot(kind='bar', ax=ax)
    ax.set_facecolor('black')
    plt.title(titulo, fontsize=16, color='white')
    plt.xlabel(col, fontsize=14, color='white')
    plt.ylabel("Cantidad", fontsize=14, color='white')
    st.pyplot(fig)


def estilo():
    ### Configurar estilos para gráficos ###
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

