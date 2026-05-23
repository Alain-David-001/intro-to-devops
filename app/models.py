from pydantic import BaseModel, Field


class FruitBase(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    in_season: bool = True


class FruitCreate(FruitBase):
    pass


class FruitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    price: float | None = Field(default=None, gt=0)
    in_season: bool | None = None


class Fruit(FruitBase):
    id: int


def build_fruit_response(fruit_id: int, fruit: FruitBase) -> Fruit:
    return Fruit(id=fruit_id, **fruit.model_dump())

