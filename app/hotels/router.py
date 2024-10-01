import asyncio
from datetime import date
from fastapi import APIRouter

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import HotelSchema, HotelsWithVacantRoomsSchema

from fastapi_cache.decorator import cache

router = APIRouter(prefix="/hotels",
                   tags=["Отели"])


@router.get("/{location}")
@cache(expire=200)
async def get_hotels(location: str,
                     date_from: date,
                     date_to: date) -> list[HotelsWithVacantRoomsSchema]:
    hotels = await HotelsDAO.get_available_hotels(location, date_from, date_to)
    #await asyncio.sleep(4)
    return hotels


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> HotelSchema:
    res = await HotelsDAO.find_by_id(hotel_id)
    return res
    