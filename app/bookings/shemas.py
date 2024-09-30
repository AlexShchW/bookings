from datetime import date
from typing import Any, Optional
from pydantic import BaseModel


class BookingSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    class Config:
        orm_mode = True


class BookingWithRoomInfoSchema(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    name: str
    description: str
    services: Any
    image_id: Optional[int]

    class Config:
        orm_mode = True