# Importar librerías necesarias
import pandas as pd
import re
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Datos iniciales de las recetas con algunos valores duplicados y erróneos para probar
data = {
    "Recetas": [
        "Receta de Muffins de chocolate con pepitas de chocolate",
        "Receta de Romanescu con jamón",
        "Receta de Pizza porteña",
        "Receta de Chocotorta helada",
        "Receta de Caramelo para quesillo",
        "Receta de Pollo con panko",
        "Receta de Pollo con panko",  # Duplicado
        "Receta de Pasticho de plátano",
        "Receta de Torta napoleón",
        "Receta de Pasteles chilenitos",
        "Receta de Pasteles chilenitos",  # Duplicado
        "Receta de Tarta de caballa",
        "Receta de Tarta errónea"  # Entrada errónea para prueba
    ],
    "Duracion": ["30m", "30m", "1h 30m", "30m", "30m", "30m", "30m", "1h 30m", "2h 30m", "1h 30m", "1h 30m", "45m", "invalid"],  # Error en "invalid"
    "Dificultad": ["baja", "baja", "baja", "baja", "baja", "baja", "baja", "media", "media", "media", "media", "baja", "unknown"],  # Error en "unknown"
    "Valoracion": ["80.00%", "90.00%", "80.00%", "90.00%", "92.20%", "100.00%", "100.00%", "78.20%", "90.00%", "93.40%", "93.40%", "100.00%", "105%"]  # Error en "105%"
}

# Convertir datos a DataFrame
df = pd.DataFrame(data)

# Función para convertir y mostrar la duración en el formato adecuado
def format_duration(duration):
    hours = re.search(r"(\d+)h", duration)
    minutes = re.search(r"(\d+)m", duration)
    formatted_duration = ""
    if hours:
        formatted_duration += f"{hours.group(1)}h "
    if minutes:
        formatted_duration += f"{minutes.group(1)}m"
    return formatted_duration.strip()

# Función para convertir la duración a minutos solo para el gráfico
def convert_to_minutes(duration):
    hours = re.search(r"(\d+)h", duration)
    minutes = re.search(r"(\d+)m", duration)
    total_minutes = 0
    if hours:
        total_minutes += int(hours.group(1)) * 60
    if minutes:
        total_minutes += int(minutes.group(1))
    return total_minutes

# Crear columna de duración en minutos para el gráfico y renombrar la columna formateada a "Duracion"
df['Duracion'] = df['Duracion'].apply(format_duration)
df['DuracionMinutos'] = df['Duracion'].apply(convert_to_minutes)
df['Valoracion'] = df['Valoracion'].str.replace('%', '').astype(float)

# LIMPIEZA DE DATOS

# Eliminar filas duplicadas
df = df.drop_duplicates()

# Eliminar filas con valores nulos o vacíos
df = df.dropna()

# Filtrar duración en minutos: solo valores mayores a 0
df = df[df['DuracionMinutos'] > 0]

# Filtrar valoración: entre 0 y 100
df = df[(df['Valoracion'] >= 0) & (df['Valoracion'] <= 100)]

# Filtrar dificultad: solo valores válidos
df = df[df['Dificultad'].isin(['baja', 'media', 'alta'])]

# Configuración de la interfaz en Streamlit
st.title('Recetas y Valoración')

# Sidebar para los filtros
st.sidebar.header('Filtros')
dificultad = st.sidebar.selectbox('Selecciona la dificultad', ['todas', 'baja', 'media', 'alta'])

# Filtrar DataFrame por dificultad si se selecciona
if dificultad != 'todas':
    df = df[df['Dificultad'] == dificultad]

# Mostrar la tabla de datos de las recetas con la duración formateada sin la numeración
st.subheader('Datos de las recetas')
st.table(df[['Recetas', 'Duracion', 'Dificultad', 'Valoracion']])

# Gráfico de duración de las recetas usando la columna de duración en minutos
st.subheader('Gráfico de Duración de las Recetas')
fig, ax = plt.subplots()
sns.barplot(x='Recetas', y='DuracionMinutos', data=df, ax=ax, palette="viridis")
plt.xticks(rotation=90)
plt.ylabel('Duración (minutos)')
st.pyplot(fig)

# Gráfico de valoraciones
st.subheader('Gráfico de Valoración de las Recetas')
fig, ax = plt.subplots()
sns.barplot(x='Recetas', y='Valoracion', data=df, ax=ax, palette="coolwarm")
plt.xticks(rotation=90)
plt.ylabel('Valoración (%)')
st.pyplot(fig)
