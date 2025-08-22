from pydantic import BaseModel


class BookingRequest(BaseModel):
    name: str
    email: str
    message: str
    date: str
    time: str
