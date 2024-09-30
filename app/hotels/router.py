from datetime import date
from fastapi import APIRouter

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import HotelSchema, HotelsWithVacantRoomsSchema


router = APIRouter(prefix="/hotels",
                   tags=["Отели"])


@router.get("/{location}")
async def get_hotels(location: str,
                     date_from: date,
                     date_to: date) -> list[HotelsWithVacantRoomsSchema]:
    res = await HotelsDAO.get_available_hotels(location, date_from, date_to)
    return res


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> HotelSchema:
    res = await HotelsDAO.find_by_id(hotel_id)
    return res
    