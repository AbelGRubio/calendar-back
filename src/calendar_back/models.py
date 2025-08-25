from pydantic import BaseModel, Field
from typing import List, Optional


class BookingRequest(BaseModel):
    name: str
    email: str
    message: str
    date: str
    time: str


# Pydantic models
class Holiday(BaseModel):
    date: str = Field(..., example="2025-12-25")
    description: Optional[str] = Field("", example="Christmas")

class BulkHolidays(BaseModel):
    holidays: List[Holiday]
