"""
REST API endpoints for user management, message handling, and file uploads.

Includes:

- Add, update, list and delete users.
- Upload files.
- Get recent messages and delete them.
- Retrieve user configuration from request token.
- Track connected users via WebSocket manager.

"""


from fastapi import APIRouter


from ..configuration import LOGGER
from ..utils.functions import create_outlook_event
from ..models import BookingRequest

v1_router = APIRouter()


@v1_router.post("/book")
def create_booking(data: BookingRequest):
    LOGGER.info("Creating booking for ", data)
    event = create_outlook_event(data)
    return {"status": "success", "event_id": event["id"]}
