import os
from ..models import BookingRequest
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_google_calendar_service():
    creds = Credentials.from_service_account_file(
        os.getenv("GOOGLE_CREDENTIALS_JSON", "credentials.json"),
        scopes=SCOPES
    )
    service = build("calendar", "v3", credentials=creds)
    return service


def create_google_event(booking: BookingRequest):
    service = get_google_calendar_service()
    
    start_dt = datetime.fromisoformat(f"{booking.date}T{booking.time}")
    end_dt = start_dt + timedelta(minutes=30)

    event = {
        "summary": "Meeting 30 minutes",
        "start": {"dateTime": start_dt.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": "UTC"},
        "attendees": [{"email": booking.email}],
    }

    created_event = service.events().insert(
        calendarId="primary", body=event
    ).execute()

    return created_event