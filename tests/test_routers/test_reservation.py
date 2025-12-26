import datetime

import pytest
from pydantic import PositiveInt
from fastapi.testclient import TestClient

from main import app


FUTURE_DATETIME: datetime.datetime = (
    datetime.datetime.now() + datetime.timedelta(days=1)
)
FUTURE_DATETIME_STR: str = str(
    datetime.datetime.now() + datetime.timedelta(days=1)
)

CREATED_TABLES: list[PositiveInt] = []
CREATED_RESERVATIONS: list[PositiveInt] = []


client = TestClient(app=app)


@pytest.mark.skip
def test_get_reservations_empty_response():
    # XXX (ames0k0): Fails for non empty Database
    response = client.get("/reservations")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize(
    "customer_name,reservation_time,duration_minutes,table_id,error_msg",
    [
        ("", FUTURE_DATETIME_STR, 0, 1, "Input should be greater than 0"),
        ("", FUTURE_DATETIME_STR, 1, 0, "Input should be greater than 0"),
        ("", "2025-01-02", 1, 1, "Input should be in the future"),
    ],
)
def test_create_reservation_validation_error(
    customer_name,
    reservation_time,
    duration_minutes,
    table_id,
    error_msg,
):
    response = client.post(
        "/reservations",
        json={
            "customer_name": customer_name,
            "reservation_time": reservation_time,
            "duration_minutes": duration_minutes,
            "table_id": table_id,
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0].get("msg") == error_msg


def test_create_table_for_reservation():
    response = client.post(
        "/tables",
        json={
            "name": "Table 1",
            "seats": 4,
            "location": "Терраса",
        },
    )

    assert response.status_code == 200

    json: dict = response.json()
    table_id: PositiveInt = json["id"]
    assert table_id != 0

    CREATED_TABLES.append(table_id)


def test_create_reservation():
    response = client.post(
        "/reservations",
        json={
            "customer_name": "Alice",
            "reservation_time": FUTURE_DATETIME_STR,
            "duration_minutes": 30,
            "table_id": CREATED_TABLES[0],
        },
    )

    assert response.status_code == 200

    json: dict = response.json()
    reservation_id: PositiveInt = json["id"]
    assert reservation_id != 0

    CREATED_RESERVATIONS.append(reservation_id)


@pytest.mark.parametrize(
    "reservation_time,error_code",
    [
        (FUTURE_DATETIME_STR, 409),
        (str(FUTURE_DATETIME + datetime.timedelta(minutes=29)), 409),
    ],
)
def test_create_reservation_busy_table(reservation_time: str, error_code: int):
    response = client.post(
        "/reservations",
        json={
            "customer_name": f"Alice: {reservation_time}",
            "reservation_time": reservation_time,
            "duration_minutes": 30,
            "table_id": CREATED_TABLES[0],
        },
    )

    assert response.status_code == error_code


def test_delete_created_reservations_and_tables():
    for reservation_id in CREATED_RESERVATIONS:
        response = client.delete(f"/reservations/{reservation_id}")
        assert response.status_code == 200

    for table_id in CREATED_TABLES:
        response = client.delete(f"/tables/{table_id}")
        assert response.status_code == 200
