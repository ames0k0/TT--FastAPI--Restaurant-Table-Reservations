import pytest
from pydantic import BaseModel
from pydantic import PositiveInt
from fastapi.testclient import TestClient

from main import app


CREATED_TABLES: list[PositiveInt] = []


class ValidationErrorDetail(BaseModel):
    type: str
    loc: list[str]
    msg: str
    input: int


class ErrorResponseJson(BaseModel):
    detail: list[ValidationErrorDetail]


client = TestClient(app=app)


@pytest.mark.skip
def test_get_tables_empty_response():
    # XXX (ames0k0): Fails for non empty Database
    response = client.get("/tables")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize(
    "name,seats,location,failed_to_validate",
    [
        (1, 2, 3, "name"),
        ("name", 0, 0, "seats"),
        ("name", 1, 0, "location"),
    ],
)
def test_create_table_validation_error(
    name,
    seats,
    location,
    failed_to_validate,
):
    response = client.post(
        "/tables",
        json={
            "name": name,
            "seats": seats,
            "location": location,
        },
    )
    assert response.status_code == 422

    json: ErrorResponseJson = ErrorResponseJson.model_validate(
        response.json(),
    )
    assert failed_to_validate in json.detail[0].loc


@pytest.mark.parametrize(
    "name,seats,location",
    [
        ("Table 1", 4, "Терраса"),
    ],
)
def test_create_table(name, seats, location):
    response = client.post(
        "/tables",
        json={
            "name": name,
            "seats": seats,
            "location": location,
        },
    )

    assert response.status_code == 200

    json: dict = response.json()
    assert json["id"] != 0
    assert json["name"] == name
    assert json["seats"] == seats
    assert json["location"] == location

    CREATED_TABLES.append(json["id"])


def test_get_tables_non_empty_response():
    response = client.get("/tables")
    assert response.status_code == 200
    assert response.json() != []


def test_delete_table_errors():
    id: int = 0
    response = client.delete(f"/tables/{id}")
    assert response.status_code == 422

    json: ErrorResponseJson = ErrorResponseJson.model_validate(response.json())
    assert "id" in json.detail[0].loc

    if CREATED_TABLES:
        id: int = CREATED_TABLES[0] + 9999
        response = client.delete(f"/tables/{id}")
        assert response.status_code == 404

        custom_exception: dict[str, str] = response.json()
        # Столик по id=`id` не найдено
        assert str(id) in custom_exception["detail"]


def test_delete_table():
    for table_id in CREATED_TABLES:
        response = client.delete(f"/tables/{table_id}")
        assert response.status_code == 200
