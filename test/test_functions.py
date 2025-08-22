import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from src.calendar_back.models import BookingRequest
from src.calendar_back.utils import functions  # ajusta según tu proyecto


class TestGoogleCalendarService(unittest.TestCase):

    @patch("src.calendar_back.utils.functions.build")
    @patch("src.calendar_back.utils.functions.Credentials")
    def test_get_google_calendar_service(self, mock_credentials, mock_build):
        # Mock del servicio de Google
        fake_service = MagicMock()
        mock_build.return_value = fake_service

        # Llamamos a la función
        service = functions.get_google_calendar_service()

        # Validamos que se creó la credencial y el servicio
        mock_credentials.from_service_account_file.assert_called_once()
        mock_build.assert_called_once_with(
            "calendar",
            "v3",
            credentials=mock_credentials.from_service_account_file.return_value
        )
        self.assertEqual(service, fake_service)


    @patch("src.calendar_back.utils.functions.get_google_calendar_service")
    def test_create_google_event(self, mock_get_service):
        # Mock del servicio
        fake_service = MagicMock()
        fake_service.events.return_value.insert.return_value.execute.return_value = {
            "id": "123"}
        mock_get_service.return_value = fake_service

        # Booking de ejemplo
        booking = BookingRequest(
            date="2025-08-22", time="10:00:00", email="test@example.com",
            name="John", message="message"
        )

        created_event = functions.create_google_event(booking)

        # Validamos el resultado
        self.assertEqual(created_event["id"], "123")

        # Validamos que el servicio se llamó correctamente
        mock_get_service.assert_called_once()
        insert_call = fake_service.events.return_value.insert.call_args[1]['body']
        start_dt = datetime.fromisoformat(f"{booking.date}T{booking.time}")
        end_dt = start_dt + timedelta(minutes=30)
        self.assertEqual(insert_call["attendees"][0]["email"], booking.email)
        self.assertEqual(insert_call["start"]["dateTime"], start_dt.isoformat())
        self.assertEqual(insert_call["end"]["dateTime"], end_dt.isoformat())


if __name__ == "__main__":
    unittest.main()