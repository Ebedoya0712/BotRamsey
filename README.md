# BotRamsey: Un Bot de Recomendación de Recetas


![BotRamsey](https://github.com/Joanaa789/BotRamsey/blob/831939889c5856dae5dcdf53bcc1325326a0ccb8/DALL%C2%B7E%202024-10-31%2018.40.54%20-%20A%20highly%20detailed%20and%20realistic%20image%20of%20Gordon%20Ramsay%20with%20half%20of%20his%20face%20as%20a%20robot.%20The%20robotic%20half%20includes%20metallic%20features%2C%20LED%20lights%2C%20and%20.webp)

## Objetivo del Proyecto
El objetivo de este proyecto es crear un sistema que permita a los usuarios encontrar recetas de cocina que se puedan realizar en un tiempo específico. Las recetas estarán organizadas por ingredientes y dificultad, y se clasificarán según los tiempos parciales de preparación, cocción y armado, así como el tiempo total requerido.

## Características Principales
- **Búsqueda Personalizada:** Los usuarios pueden ingresar el tiempo disponible, tipo de cocina, nivel de dificultad y seleccionar ingredientes para encontrar recetas que se ajusten a sus necesidades.
- **Clasificación de Recetas:** Las recetas se agrupan en categorías según el tiempo total (15 minutos, 30 minutos, 1 hora, etc.) y dificultad (fácil, media, difícil).
- **Recomendaciones Inteligentes:** Un modelo de recomendación sugiere recetas basadas en los ingredientes que el usuario tiene disponibles y el tiempo que quiere invertir.
- **Visualización Interactiva:** Gráficos que muestran recetas agrupadas por tiempo y dificultad para facilitar la elección.

## Metodología y Fuentes de Datos
Para la recopilación de datos, se utilizará web scraping de sitios de recetas como AllRecipes, Epicurious y Tasty, asegurando el cumplimiento de sus políticas de uso. Los datos clave a extraer incluyen:
- Tiempos de preparación y cocción
- Listado de ingredientes y pasos detallados
- Dificultad de la receta
- Valoraciones y popularidad

## Pasos del Proyecto
1. **Recopilación de Datos:**
   - Realizar web scraping para extraer información clave de recetas.
   - Limpiar y normalizar los datos para unificar formatos.
   - Etiquetar recetas según tipos de cocina, ingredientes, dificultad y tiempo total.

2. **Análisis y Clasificación:**
   - Clasificar recetas por tiempo total y dificultad.
   - Agrupar recetas por ingredientes principales.

3. **Desarrollo de Modelos Predictivos:**
   - Predecir el tiempo total de preparación basado en ingredientes y pasos.
   - Implementar un sistema de recomendación.

4. **Visualización y Accesibilidad:**
   - Crear una interfaz de búsqueda intuitiva.
   - Desarrollar gráficos interactivos para la visualización de datos.

## Desafíos y Consideraciones
- Normalización de tiempos de recetas que pueden ser imprecisos.
- Compatibilidad de ingredientes y variaciones en recetas.
- Cumplimiento de políticas de scraping y manejo adecuado de solicitudes.

## Posibilidades de Expansión
- Integración de un asistente de voz o chatbot para guiar a los usuarios en las recetas.
- Funciones que ajusten los tiempos de cocción en tiempo real.

## Tecnologías y Herramientas Sugeridas
- **Web Scraping:** Beautiful Soup
- **Análisis de Datos:** Pandas
- **Machine Learning:** scikit-learn, TensorFlow
- **Visualización:** Plotly, Seaborn
- **Interfaz de Usuario:** Streamlit

## Conclusión
Este proyecto tiene el potencial de ofrecer una solución innovadora para personas con agendas ajustadas, facilitando la experiencia culinaria y reduciendo la barrera del tiempo en la cocina. ¡Esperamos que disfrutes usando el bot y descubras nuevas recetas que se adapten a tu estilo de vida!
