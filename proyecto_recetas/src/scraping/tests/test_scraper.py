from unittest import TestCase
from unittest.mock import patch, MagicMock
from scraping.scraper import obtener_contenido, guardar_datos

class TestScraper(TestCase):

    @patch('scraping.scraper.requests.get')
    def test_obtener_contenido(self, mock_get):
        # Simula una respuesta HTML ficticia
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Contenido de prueba</body></html>"
        mock_get.return_value = mock_response

        # Llamada a la función y verificación
        sopa = obtener_contenido("https://ficticia.com/receta")
        self.assertIsNotNone(sopa, "La función obtener_contenido debería devolver contenido HTML.")
        self.assertIn("Contenido de prueba", sopa.get_text(), "El contenido HTML simulado no coincide.")

    @patch('streamlit.session_state', new_callable=MagicMock)
    def test_guardar_datos(self, mock_session_state):
        # Simulación de valores de entrada
        mock_session_state.Base = {}  # Añade 'Base' al session_state simulado
        titulo = "Receta de Prueba"
        propiedades = ["10 minutos", "Dificultad fácil"]
        ingredientes = ["1 taza de harina", "2 huevos"]

        # Llamada a la función guardar_datos
        guardar_datos(titulo, propiedades, ingredientes)

        # Validación de los resultados esperados en session_state['Base']
        self.assertIn(titulo, mock_session_state.Base, "El título de la receta debería estar en el estado de la sesión.")
        
        # Validación de propiedades dinámicamente
        receta = mock_session_state.Base[titulo]
        self.assertEqual(receta["ingredientes"], [ingrediente.strip() for ingrediente in ingredientes], "Los ingredientes no coinciden.")

        # Verifica la duración y dificultad en las propiedades guardadas
        self.assertEqual(receta.get("Duracion"), "10 minutos", "La duración guardada no es correcta.")
        self.assertEqual(receta.get("Dificultad"), "fácil", "La dificultad guardada no es correcta.")

if __name__ == "__main__":
    import unittest
    unittest.main()
