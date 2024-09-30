from datetime import date
from app.base_dao.base_dao import BaseDAO
from app.database import async_session_maker
from sqlalchemy.orm import aliased


from sqlalchemy import delete, func, insert, select, and_, or_
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date
    ):
        """
        WITH booked_rooms AS (
        SELECT * FROM bookings
        WHERE room_id = 1 AND
        (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
        (date_from < '2023-05-15' AND date_to > '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
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
                )
            ).cte("booked_rooms")

            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
                ).select_from(Rooms).join(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                ).where(Rooms.id == room_id).group_by(
                    Rooms.quantity, booked_rooms.c.room_id
                )
            
            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price = price.scalar()
                
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

            else:
                return None

    @classmethod
    async def bookings_with_room_info(cls, user_id: int):
        async with async_session_maker() as session:

            query = (
                select(
                    Bookings.room_id,
                    Bookings.user_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_cost,
                    Bookings.total_days,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                    Rooms.image_id
                )
                .select_from(Bookings)
                .join(Rooms, Bookings.room_id == Rooms.id)
                .where(Bookings.user_id == user_id)
            )

            result = await session.execute(query)
            rows = result.fetchall()
            dict_result = [
                {
            "room_id": row[0],
            "user_id": row[1],
            "date_from": row[2],
            "date_to": row[3],
            "price": row[4],
            "total_cost": row[5],
            "total_days": row[6],
            "name": row[7],
            "description": row[8],
            "services": row[9],
            "image_id": row[10] if row[10] else None
                } for row in rows
            ]

            return dict_result
    
    @classmethod
    async def delete_booking(
        cls,
        user_id: int,
        booking_id: int):
        async with async_session_maker() as session:
            checking_query = select(Bookings).where(and_(Bookings.user_id == user_id, Bookings.id == booking_id))
            result = await session.execute(checking_query)
            booking_to_delete = result.scalar_one_or_none()
            
            if not booking_to_delete:
                return False
            
            query = delete(Bookings).where(
                and_(
                    Bookings.user_id == user_id,
                    Bookings.id == booking_id
                )
            )
            await session.execute(query)
            await session.commit()

            return True