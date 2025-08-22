import unittest
from fastapi.testclient import TestClient
from fastapi import FastAPI

# importa tu router
from src.calendar_back.routes.api_routes import api_router
from src.calendar_back import __version__


# Creamos un FastAPI app solo para tests
app = FastAPI()
app.include_router(api_router)


class TestHealthEndpoint(unittest.TestCase):

    def test_health(self):
        client = TestClient(app)

        response = client.get("/health")

        # Validamos el status code
        self.assertEqual(response.status_code, 200)

        # Validamos que el contenido devuelto es correcto
        data = response.json()
        self.assertIn("version", data)
        self.assertEqual(data["version"], __version__)


if __name__ == "__main__":
    unittest.main()
