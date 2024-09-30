from datetime import date
from fastapi import APIRouter

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import RoomsOfHotelSchema


router = APIRouter(prefix="/hotels", tags=["Комнаты"])

@router.get("/{hotel_id}/room")
async def get_hotel_rooms_info(
    hotel_id: int,
    date_from: date,
    date_to: date
) -> list[RoomsOfHotelSchema]:
    res = await RoomsDAO.get_rooms_info_of_hotel(hotel_id, date_from, date_to)
    return res