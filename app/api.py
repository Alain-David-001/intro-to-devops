from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.models import Fruit, FruitCreate, FruitUpdate
from app.store import store

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/fruits", response_model=list[Fruit])
def list_fruits(
    in_season: bool | None = None,
    limit: Annotated[int | None, Query(ge=1)] = None,
) -> list[Fruit]:
    return store.list(in_season=in_season, limit=limit)


@router.post("/fruits", response_model=Fruit, status_code=status.HTTP_201_CREATED)
def create_fruit(fruit: FruitCreate) -> Fruit:
    return store.create(fruit)


@router.get("/fruits/cheapest", response_model=Fruit)
def get_cheapest_fruit() -> Fruit:
    fruit = store.cheapest()
    if fruit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No fruits found")
    return fruit


@router.get("/fruits/{fruit_id}", response_model=Fruit)
def get_fruit(fruit_id: int) -> Fruit:
    fruit = store.get(fruit_id)
    if fruit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fruit not found")
    return fruit


@router.put("/fruits/{fruit_id}", response_model=Fruit)
def update_fruit(fruit_id: int, changes: FruitUpdate) -> Fruit:
    fruit = store.update(fruit_id, changes)
    if fruit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fruit not found")
    return fruit


@router.delete("/fruits/{fruit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fruit(fruit_id: int) -> Response:
    deleted = store.delete(fruit_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fruit not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

