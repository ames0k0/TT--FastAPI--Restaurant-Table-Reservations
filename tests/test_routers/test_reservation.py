"""
TODO (ames0k0)
    - Cannot create reservations without `customer_name`
    - Cannot create reservations with the same `reservation_time`
    - Cannot create reservations unless ended the previous reservation
        - new ReservationTime > `reservation_time` + `duration_minutes`
"""
import datetime

import pytest
from fastapi.testclient import TestClient

from main import app


FUTURE_DATETIME: str = str(
    datetime.datetime.now() + datetime.timedelta(days=1)
)


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
        ("", FUTURE_DATETIME, 0, 1, "Input should be greater than 0"),
        ("", FUTURE_DATETIME, 1, 0, "Input should be greater than 0"),
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
