import streamlit as st
import pandas as pd

# Título y descripción de la aplicación
st.title("BotRamsey: Encuentra tu receta ideal")
st.write("Encuentra recetas según los ingredientes que tienes y el tiempo disponible.")

# Barra lateral para los filtros
st.sidebar.header("Filtrar búsqueda")
ingredientes = st.sidebar.text_input("Ingredientes (separados por comas)")
tiempo_maximo = st.sidebar.slider("Tiempo máximo disponible (minutos)", 5, 120, 30)
dificultad = st.sidebar.selectbox("Nivel de dificultad", ["Fácil", "Media", "Difícil"])

# Botón para buscar recetas
if st.sidebar.button("Buscar recetas"):
    # Generación de resultados ficticios
    recetas = [
        {"Receta": "Pasta al pesto", "Tiempo (min)": 25, "Dificultad": "Fácil"},
        {"Receta": "Pollo al horno", "Tiempo (min)": 45, "Dificultad": "Media"},
        {"Receta": "Ensalada César", "Tiempo (min)": 15, "Dificultad": "Fácil"}
    ]
    df_recetas = pd.DataFrame(recetas)

    # Filtrar recetas según los parámetros seleccionados (simulado)
    recetas_filtradas = df_recetas[
        (df_recetas["Tiempo (min)"] <= tiempo_maximo) &
        (df_recetas["Dificultad"] == dificultad)
    ]
    
    # Mostrar resultados
    st.subheader("Resultados de Búsqueda")
    if len(recetas_filtradas) > 0:
        st.table(recetas_filtradas)
    else:
        st.write("No se encontraron recetas con los criterios seleccionados.")

# Sección de gráficos (demostración)
st.subheader("Gráfico de Tiempo vs Dificultad")
st.write("Aquí puedes ver cómo se agrupan las recetas según el tiempo y dificultad.")

# Datos de ejemplo para el gráfico
df_grafico = pd.DataFrame({
    "Receta": ["Pasta al pesto", "Pollo al horno", "Ensalada César"],
    "Tiempo (min)": [25, 45, 15],
    "Dificultad": ["Fácil", "Media", "Fácil"]
})
st.bar_chart(df_grafico.set_index("Receta")["Tiempo (min)"])
