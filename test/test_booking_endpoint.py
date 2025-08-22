import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# importa tu router real
from src.calendar_back.routes.v1_routes import v1_router


# Creamos un FastAPI app solo para tests
from fastapi import FastAPI
app = FastAPI()
app.include_router(v1_router)


class TestBookingEndpoint(unittest.TestCase):

    @patch("src.calendar_back.routes.v1_routes.create_google_event")
    def test_create_booking(self, mock_create_event):
        # Preparamos el mock
        mock_create_event.return_value = {"id": "abc123"}

        client = TestClient(app)

        # Datos simulados de la request
        payload = {
            "date": "2025-08-22",
            "time": "10:00:00",
            "email": "test@example.com",
            "name": "John",
            "message": "eee"
        }

        response = client.post("/book", json=payload)

        # Validamos respuesta
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["event_id"], "abc123")

        # Aseguramos que create_google_event fue llamado correctamente
        mock_create_event.assert_called_once()
        args, kwargs = mock_create_event.call_args
        booking_arg = args[0]
        self.assertEqual(booking_arg.date, payload["date"])
        self.assertEqual(booking_arg.time, payload["time"])
        self.assertEqual(booking_arg.email, payload["email"])


if __name__ == "__main__":
    unittest.main()
