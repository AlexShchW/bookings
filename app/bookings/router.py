from datetime import date
from fastapi import APIRouter, Depends, HTTPException

from app.bookings.dao import BookingDAO
from app.bookings.shemas import BookingSchema, BookingWithRoomInfoSchema
from app.exceptions import BookingCannotBeDeletedException, RoomCannotBeBookedException
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[BookingWithRoomInfoSchema]:
    return await BookingDAO.bookings_with_room_info(user_id=user.id)

@router.post("")
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBookedException
    

@router.delete("/{booking_id}")
async def delete_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),
):
    result = await BookingDAO.delete_booking(user.id, booking_id)
    if not result:
        raise BookingCannotBeDeletedException





  