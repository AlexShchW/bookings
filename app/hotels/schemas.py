from typing import Any, Optional
from pydantic import BaseModel


class HotelsWithVacantRoomsSchema(BaseModel):
    id: int
    name: str
    location: str
    services: Any
    rooms_quantity: int
    image_id: Optional[int]
    rooms_left: int
    
    class Config:
        orm_mode = True
        

class HotelSchema(BaseModel):
    id: int
    name: str
    location: str
    services: Any
    rooms_quantity: int
    image_id: Optional[int]
    
    class Config:
        orm_mode = True

