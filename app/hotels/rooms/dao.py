from datetime import date

from sqlalchemy import and_, func, or_, select

from app.base_dao.base_dao import BaseDAO
from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_rooms_info_of_hotel(
        cls, hotel_id: int, date_from: date, date_to: date
    ):
        days_total = abs((date_to - date_from).days)
        async with async_session_maker() as session:

            booked_rooms_with_hotel_id = (
                select(Bookings, Rooms.hotel_id)
                .join(Rooms, Bookings.room_id == Rooms.id, isouter=True)
                .where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from,
                        ),
                    )
                )
                .cte("booked_rooms_with_hotel_id")
            )

            booked_rooms = (
                select(
                    booked_rooms_with_hotel_id.c.room_id,
                    func.count(booked_rooms_with_hotel_id.c.id).label("booked_amount"),
                )
                .where(
                    and_(
                        or_(
                            and_(
                                booked_rooms_with_hotel_id.c.date_from >= date_from,
                                booked_rooms_with_hotel_id.c.date_from <= date_to,
                            ),
                            and_(
                                booked_rooms_with_hotel_id.c.date_from <= date_from,
                                booked_rooms_with_hotel_id.c.date_to > date_from,
                            ),
                        ),
                        booked_rooms_with_hotel_id.c.hotel_id == hotel_id,
                    )
                )
                .group_by(booked_rooms_with_hotel_id.c.room_id)
                .cte("booked_rooms")
            )

            rooms_with_needed_info = (
                select(
                    Rooms,
                    (Rooms.price * days_total).label("total_cost"),
                    (
                        Rooms.quantity - func.coalesce(booked_rooms.c.booked_amount, 0)
                    ).label("rooms_left"),
                )
                .outerjoin(booked_rooms, Rooms.id == booked_rooms.c.room_id)
                .cte("rooms_with_needed_info")
            )

            res = select(rooms_with_needed_info)
            res = await session.execute(res)
            res = res.mappings().all()

            # print(res)
            return res
