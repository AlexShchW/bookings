import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id,date_from,date_to,have_bookings,status_code",
    [
        *(
            (4, "2030-05-01", "2030-05-15", have_bookings, 200)
            for have_bookings in range(3, 11)
        ),
        (4, "2030-05-01", "2030-05-15", 10, 409),
        (4, "2030-05-01", "2030-05-15", 10, 409),
        (4, "2030-05-01", "2030-05-15", 10, 409),
    ],
)
async def test_add_and_get_booking(
    room_id,
    date_from,
    date_to,
    have_bookings,
    status_code,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "/bookings",
        params={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )

    assert response.status_code == status_code

    bookings_list = await authenticated_ac.get("/bookings")

    assert len(bookings_list.json()) == have_bookings
