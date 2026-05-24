import os

import httpx
import pytest


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
TIMEOUT = 5.0

pytestmark = pytest.mark.integration


def test_health_endpoint():
    response = httpx.get(f"{BASE_URL}/health", timeout=TIMEOUT)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_crud_lifecycle():
    create_response = httpx.post(
        f"{BASE_URL}/fruits",
        json={"name": "Kiwi", "price": 1.8, "in_season": True},
        timeout=TIMEOUT,
    )
    assert create_response.status_code == 201
    created = create_response.json()
    fruit_id = created["id"]

    get_response = httpx.get(f"{BASE_URL}/fruits/{fruit_id}", timeout=TIMEOUT)
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Kiwi"

    update_response = httpx.put(f"{BASE_URL}/fruits/{fruit_id}", json={"price": 2.0}, timeout=TIMEOUT)
    assert update_response.status_code == 200
    assert update_response.json()["price"] == 2.0

    delete_response = httpx.delete(f"{BASE_URL}/fruits/{fruit_id}", timeout=TIMEOUT)
    assert delete_response.status_code == 204

    missing_response = httpx.get(f"{BASE_URL}/fruits/{fruit_id}", timeout=TIMEOUT)
    assert missing_response.status_code == 404


def test_cheapest_matches_minimum_price_from_list():
    fruits_response = httpx.get(f"{BASE_URL}/fruits", timeout=TIMEOUT)
    cheapest_response = httpx.get(f"{BASE_URL}/fruits/cheapest", timeout=TIMEOUT)

    assert fruits_response.status_code == 200
    assert cheapest_response.status_code == 200

    fruits = fruits_response.json()
    cheapest = cheapest_response.json()
    assert cheapest["price"] == min(fruit["price"] for fruit in fruits)


def test_created_fruit_appears_in_list():
    create_response = httpx.post(
        f"{BASE_URL}/fruits",
        json={"name": "Plum", "price": 1.3, "in_season": False},
        timeout=TIMEOUT,
    )
    assert create_response.status_code == 201
    created = create_response.json()

    list_response = httpx.get(f"{BASE_URL}/fruits", timeout=TIMEOUT)
    assert list_response.status_code == 200
    assert created in list_response.json()

    httpx.delete(f"{BASE_URL}/fruits/{created['id']}", timeout=TIMEOUT)
