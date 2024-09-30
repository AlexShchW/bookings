from datetime import date
from app.base_dao.base_dao import BaseDAO
from app.database import async_session_maker
from sqlalchemy.orm import aliased


from sqlalchemy import delete, func, insert, select, and_, or_
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_available_hotels(
        cls,
        location: str,
        date_from: date,
        date_to: date
    ):
        async with async_session_maker() as session:
            booked_rooms_with_hotel_id = select(Bookings, Rooms.hotel_id).join(Rooms, Bookings.room_id == Rooms.id, isouter=True).where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to

                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from
                    )
                )
            ).cte("booked_rooms_with_hotel_id")

            hotels_ids_with_rooms_occupied = select(booked_rooms_with_hotel_id.c.hotel_id, func.count(booked_rooms_with_hotel_id.c.id).label("rooms_booked")
            ).group_by(
                    booked_rooms_with_hotel_id.c.hotel_id
            ).cte("hotels_ids_with_rooms_occupied")
            

            hotels_with_vacant_rooms = (
            select(
                Hotels,
                (Hotels.rooms_quantity - func.coalesce(hotels_ids_with_rooms_occupied.c.rooms_booked, 0)).label("rooms_left")
            )
            .outerjoin(
                hotels_ids_with_rooms_occupied,
                Hotels.id == hotels_ids_with_rooms_occupied.c.hotel_id
            )
            ).cte("hotels_with_vacant_rooms")

            res = select(hotels_with_vacant_rooms).where(and_(
                hotels_with_vacant_rooms.c.rooms_left > 0,
                hotels_with_vacant_rooms.c.location.ilike(f"%{location}%")))
            res = await session.execute(res)
            res = res.mappings().all()
            return res
                        
            
            
            

            