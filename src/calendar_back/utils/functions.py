import os
from ..models import BookingRequest
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
import pytz


SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_service():
    token_data = json.loads(os.environ["GOOGLE_TOKEN_JSON"])  # guardado como variable de entorno
    creds = Credentials.from_authorized_user_info(token_data, SCOPES)
    return build("calendar", "v3", credentials=creds)


def create_google_event(booking: BookingRequest):
    service = get_service()
    
    start_dt = datetime.fromisoformat(f"{booking.date}T{booking.time}")
    end_dt = start_dt + timedelta(minutes=30)

    event = {
        "summary": f"Meeting 30 minutes with {booking.name}",
        "description": f"<b>{booking.message}</b><br><br>If you want another time, check <a href='https://agrubio.dev/calendar/'>my availability</a>.",
        "start": {"dateTime": start_dt.isoformat(), "timeZone": "Europe/Madrid"},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": "Europe/Madrid"},
        "attendees": [{"email": booking.email},  {"email": os.environ["DEV_HOTMAIL"]}],
    }

    created = service.events().insert(
        calendarId="primary",
        body=event,
        conferenceDataVersion=1
    ).execute()

    return created


def generate_slots(date: datetime, start_hours: list, end_hours: list):
    slots = []
    tz = pytz.timezone("Europe/Madrid")
    for start, end in zip(start_hours, end_hours):
        current = date.replace(hour=start, minute=0, second=0, microsecond=0)
        end_time = date.replace(hour=end, minute=0, second=0, microsecond=0)
        while current < end_time:
            slot_end = current + timedelta(minutes=30)
            slots.append((current.astimezone(tz), slot_end.astimezone(tz)))
            current = slot_end
    return slots


def available_slots(date: str):
    service = get_service()
    tz = pytz.timezone("Europe/Madrid")

    # Fecha a consultar
    day_start = tz.localize(datetime.strptime(date, "%Y-%m-%d"))
    day_end = day_start + timedelta(days=1)

    # Obtener eventos del calendario para ese día
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=day_start.isoformat(),
            timeMax=day_end.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    busy_times = []
    for event in events_result.get("items", []):
        start = event["start"].get("dateTime")
        end = event["end"].get("dateTime")
        if start and end:
            busy_times.append(
                (datetime.fromisoformat(start), datetime.fromisoformat(end))
            )

    # Generar todos los posibles slots
    possible_slots = generate_slots(day_start, [11, 15], [14, 18])

    # Hora actual + 2h
    now_plus_2h = datetime.now(tz) + timedelta(hours=2)

    # Filtrar slots que no chocan con eventos existentes y que estén después de now+2h si es hoy
    available = []
    for start_slot, end_slot in possible_slots:
        conflict = any(bs < end_slot and be > start_slot for bs, be in busy_times)
        if not conflict:
            if day_start.date() == now_plus_2h.date():
                if start_slot > now_plus_2h:
                    available.append(start_slot.strftime("%H:%M"))
            else:
                available.append(start_slot.strftime("%H:%M"))
    return available
