import pytest
from fastapi.testclient import TestClient

from app.models import FruitCreate, build_fruit_response
from app.store import store
from main import app


FIXTURE_FRUITS = [
    FruitCreate(name="Apple", price=1.25, in_season=True),
    FruitCreate(name="Banana", price=0.75, in_season=True),
    FruitCreate(name="Mango", price=2.50, in_season=False),
]


@pytest.fixture(autouse=True)
def reset_store():
    store.seed(FIXTURE_FRUITS)
    yield
    store.seed(FIXTURE_FRUITS)


@pytest.fixture
def client():
    return TestClient(app)


def test_build_fruit_response_returns_expected_structure():
    fruit = FruitCreate(name="Pear", price=1.10, in_season=True)

    response = build_fruit_response(42, fruit)

    assert response.model_dump() == {
        "id": 42,
        "name": "Pear",
        "price": 1.10,
        "in_season": True,
    }


def test_list_fruits_returns_fixture_data(client):
    response = client.get("/fruits")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Apple", "price": 1.25, "in_season": True},
        {"id": 2, "name": "Banana", "price": 0.75, "in_season": True},
        {"id": 3, "name": "Mango", "price": 2.5, "in_season": False},
    ]


def test_cheapest_fruit_returns_lowest_price(client):
    response = client.get("/fruits/cheapest")

    assert response.status_code == 200
    assert response.json() == {"id": 2, "name": "Banana", "price": 0.75, "in_season": True}


def test_filter_fruits_by_in_season_true(client):
    response = client.get("/fruits?in_season=true")

    assert response.status_code == 200
    assert [fruit["name"] for fruit in response.json()] == ["Apple", "Banana"]


def test_filter_fruits_by_in_season_false(client):
    response = client.get("/fruits?in_season=false")

    assert response.status_code == 200
    assert response.json() == [{"id": 3, "name": "Mango", "price": 2.5, "in_season": False}]


def test_limit_fruits(client):
    response = client.get("/fruits?limit=2")

    assert response.status_code == 200
    assert [fruit["name"] for fruit in response.json()] == ["Apple", "Banana"]


def test_get_unknown_fruit_returns_404(client):
    response = client.get("/fruits/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Fruit not found"}


def test_create_fruit_with_invalid_body_returns_422(client):
    response = client.post("/fruits", json={"price": "free"})

    assert response.status_code == 422


def test_update_unknown_fruit_returns_404(client):
    response = client.put("/fruits/999", json={"price": 1.99})

    assert response.status_code == 404
    assert response.json() == {"detail": "Fruit not found"}


def test_delete_unknown_fruit_returns_404(client):
    response = client.delete("/fruits/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Fruit not found"}


def test_cheapest_fruit_when_store_empty_returns_404(client):
    store.seed([])

    response = client.get("/fruits/cheapest")

    assert response.status_code == 404
    assert response.json() == {"detail": "No fruits found"}
