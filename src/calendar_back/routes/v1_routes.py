"""
REST API endpoints for user management, message handling, and file uploads.

Includes:

- Add, update, list and delete users.
- Upload files.
- Get recent messages and delete them.
- Retrieve user configuration from request token.
- Track connected users via WebSocket manager.

"""


from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime

from ..configuration import LOGGER, HOLIDAYS
from ..utils.functions import create_google_event
from ..models import BookingRequest, Holiday, BulkHolidays

v1_router = APIRouter()


@v1_router.post("/book")
def create_booking(data: BookingRequest):
    LOGGER.info("Creating booking for ", data)
    event = create_google_event(data)
    return {"status": "success", "event_id": event["id"]}


# Helper function to validate date format
def validate_date(date_str: str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

# Endpoints

@v1_router.post("/holidays", response_model=Holiday)
def add_holiday(holiday: Holiday):
    validate_date(holiday.date)
    # Check for duplicates
    for h in HOLIDAYS:
        if h["date"] == holiday.date:
            raise HTTPException(status_code=400, detail="Holiday already exists.")
    HOLIDAYS.append({"date": holiday.date, "description": holiday.description})
    return holiday

@v1_router.post("/holidays/bulk", response_model=List[Holiday])
def add_holidays_bulk(data: BulkHolidays):
    added_holidays = []
    for holiday in data.holidays:
        try:
            validate_date(holiday.date)
            if any(h["date"] == holiday.date for h in holidays):
                continue  # Skip duplicates
            HOLIDAYS.append({"date": holiday.date, "description": holiday.description})
            added_holidays.append(holiday)
        except HTTPException:
            continue
    return added_holidays

@v1_router.delete("/holidays/{date}", response_model=dict)
def remove_holiday(date: str):
    validate_date(date)
    for h in HOLIDAYS:
        if h["date"] == date:
            HOLIDAYS.remove(h)
            return {"message": f"Holiday {date} removed."}
    raise HTTPException(status_code=404, detail="Holiday not found.")


@v1_router.get("/holidays", response_model=List[Holiday])
def list_holidays():
    return HOLIDAYS
