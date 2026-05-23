from app.models import Fruit, FruitCreate, FruitUpdate, build_fruit_response


class FruitStore:
    def __init__(self) -> None:
        self._fruits: dict[int, Fruit] = {}
        self._next_id = 1

    def seed(self, fruits: list[FruitCreate]) -> None:
        self._fruits = {}
        self._next_id = 1
        for fruit in fruits:
            self.create(fruit)

    def list(self, in_season: bool | None = None, limit: int | None = None) -> list[Fruit]:
        fruits = list(self._fruits.values())
        if in_season is not None:
            fruits = [fruit for fruit in fruits if fruit.in_season is in_season]
        if limit is not None:
            fruits = fruits[:limit]
        return fruits

    def create(self, fruit: FruitCreate) -> Fruit:
        fruit_id = self._next_id
        self._next_id += 1
        created = build_fruit_response(fruit_id, fruit)
        self._fruits[fruit_id] = created
        return created

    def get(self, fruit_id: int) -> Fruit | None:
        return self._fruits.get(fruit_id)

    def update(self, fruit_id: int, changes: FruitUpdate) -> Fruit | None:
        existing = self.get(fruit_id)
        if existing is None:
            return None

        updated_data = existing.model_dump()
        updated_data.update(changes.model_dump(exclude_unset=True))
        updated = Fruit(**updated_data)
        self._fruits[fruit_id] = updated
        return updated

    def delete(self, fruit_id: int) -> bool:
        if fruit_id not in self._fruits:
            return False
        del self._fruits[fruit_id]
        return True

    def cheapest(self) -> Fruit | None:
        if not self._fruits:
            return None
        return min(self._fruits.values(), key=lambda fruit: fruit.price)


store = FruitStore()
store.seed(
    [
        FruitCreate(name="Apple", price=1.25, in_season=True),
        FruitCreate(name="Banana", price=0.75, in_season=True),
        FruitCreate(name="Mango", price=2.5, in_season=False),
    ]
)

