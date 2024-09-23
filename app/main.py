from fastapi import FastAPI, Query
from typing import Optional
from datetime import date
from pydantic import BaseModel

app = FastAPI()


@app.get("/hotels")
def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
    has_spa: Optional[bool] = None,
    stars: Optional[int] = Query(None, ge=1, le=5)
):
    return "Ok"


class BookingSchema(BaseModel):
    room_id: int 
    date_from: date
    dat_to: date

@app.post("/bookings")
def add_booking(booking_data: BookingSchema):
    return "Ok Ok"

