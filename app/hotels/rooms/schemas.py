from typing import Any, Optional

from pydantic import BaseModel


class RoomsOfHotelSchema(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    price: int
    services: Any
    quantity: int
    image_id: Optional[int]
    total_cost: int
    rooms_left: int

    class Config:
        orm_mode = True
