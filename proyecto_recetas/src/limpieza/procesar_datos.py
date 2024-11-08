import re

# Función para convertir la duración a minutos solo para el gráfico
def procesar_minutos(duracion):

    horas = re.search(r"(\d+)h", duracion)
    minutos = re.search(r"(\d+)m", duracion)
    total_minutos = 0
    if horas:
        total_minutos += int(horas.group(1)) * 60
    if minutos:
        total_minutos += int(minutos.group(1))
    return total_minutos


def Clasificar_Dificultad(df):
    nivel_map = {
        'muy baja': 'Muy Baja',
        'baja': 'Baja',
        'media': 'Media',
        'alta': 'Alta'
    }
    df['Dificultad'] = df['Dificultad'].map(nivel_map)
    
def procesar_datos(df):
    
    df['Duracion'] = df['Duracion'].apply(procesar_minutos)
    df['Valoracion'] = df['Valoracion'].str.replace('%', '').astype(float)

    # Eliminar filas duplicadas
    df = df.drop_duplicates()

    # Eliminar filas con valores nulos o vacíos
    df = df.dropna()

    # Filtrar duración en minutos: solo valores mayores a 0
    df = df[df['Duracion'] > 0]

    # Filtrar valoración: entre 0 y 100
    df = df[(df['Valoracion'] >= 0) & (df['Valoracion'] <= 100)]

    # Filtrar dificultad: solo valores válidos
    df = df[df['Dificultad'].isin(['alta', 'media', 'baja', 'muy baja'])]

    Clasificar_Dificultad(df)

