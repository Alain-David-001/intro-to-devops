import os
from decimal import Decimal

import pymysql
from pymysql.cursors import DictCursor

from app.models import Fruit, FruitCreate, FruitUpdate, build_fruit_response


DEFAULT_FRUITS = [
    FruitCreate(name="Apple", price=1.25, in_season=True),
    FruitCreate(name="Banana", price=0.75, in_season=True),
    FruitCreate(name="Mango", price=2.5, in_season=False),
]


class FruitStore:
    def seed(self, fruits: list[FruitCreate]) -> None:
        raise NotImplementedError

    def list(self, in_season: bool | None = None, limit: int | None = None) -> list[Fruit]:
        raise NotImplementedError

    def create(self, fruit: FruitCreate) -> Fruit:
        raise NotImplementedError

    def get(self, fruit_id: int) -> Fruit | None:
        raise NotImplementedError

    def update(self, fruit_id: int, changes: FruitUpdate) -> Fruit | None:
        raise NotImplementedError

    def delete(self, fruit_id: int) -> bool:
        raise NotImplementedError

    def cheapest(self) -> Fruit | None:
        raise NotImplementedError


class InMemoryFruitStore(FruitStore):
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


class MySQLFruitStore(FruitStore):
    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
    ) -> None:
        self._connection_settings = {
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password,
            "autocommit": True,
            "cursorclass": DictCursor,
        }

    def _connect(self):
        return pymysql.connect(**self._connection_settings)

    def initialize(self) -> None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS fruits (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        price DECIMAL(10, 2) NOT NULL,
                        in_season BOOLEAN NOT NULL
                    )
                    """
                )

    def seed_if_empty(self, fruits: list[FruitCreate]) -> None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS count FROM fruits")
                if cursor.fetchone()["count"] == 0:
                    for fruit in fruits:
                        cursor.execute(
                            "INSERT INTO fruits (name, price, in_season) VALUES (%s, %s, %s)",
                            (fruit.name, fruit.price, fruit.in_season),
                        )

    def seed(self, fruits: list[FruitCreate]) -> None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM fruits")
                cursor.execute("ALTER TABLE fruits AUTO_INCREMENT = 1")
                for fruit in fruits:
                    cursor.execute(
                        "INSERT INTO fruits (name, price, in_season) VALUES (%s, %s, %s)",
                        (fruit.name, fruit.price, fruit.in_season),
                    )

    def list(self, in_season: bool | None = None, limit: int | None = None) -> list[Fruit]:
        query = "SELECT id, name, price, in_season FROM fruits"
        params: list[object] = []
        if in_season is not None:
            query += " WHERE in_season = %s"
            params.append(in_season)
        query += " ORDER BY id"
        if limit is not None:
            query += " LIMIT %s"
            params.append(limit)

        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return [self._row_to_fruit(row) for row in cursor.fetchall()]

    def create(self, fruit: FruitCreate) -> Fruit:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO fruits (name, price, in_season) VALUES (%s, %s, %s)",
                    (fruit.name, fruit.price, fruit.in_season),
                )
                fruit_id = cursor.lastrowid
        created = self.get(fruit_id)
        if created is None:
            raise RuntimeError("Created fruit could not be read from MySQL")
        return created

    def get(self, fruit_id: int) -> Fruit | None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, price, in_season FROM fruits WHERE id = %s",
                    (fruit_id,),
                )
                row = cursor.fetchone()
        if row is None:
            return None
        return self._row_to_fruit(row)

    def update(self, fruit_id: int, changes: FruitUpdate) -> Fruit | None:
        existing = self.get(fruit_id)
        if existing is None:
            return None

        changed_fields = changes.model_dump(exclude_unset=True)
        if changed_fields:
            assignments = ", ".join(f"{field} = %s" for field in changed_fields)
            values = list(changed_fields.values()) + [fruit_id]
            with self._connect() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"UPDATE fruits SET {assignments} WHERE id = %s", values)

        return self.get(fruit_id)

    def delete(self, fruit_id: int) -> bool:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM fruits WHERE id = %s", (fruit_id,))
                return cursor.rowcount > 0

    def cheapest(self) -> Fruit | None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, price, in_season FROM fruits ORDER BY price ASC, id ASC LIMIT 1"
                )
                row = cursor.fetchone()
        if row is None:
            return None
        return self._row_to_fruit(row)

    def _row_to_fruit(self, row: dict) -> Fruit:
        price = row["price"]
        if isinstance(price, Decimal):
            price = float(price)
        return Fruit(
            id=row["id"],
            name=row["name"],
            price=price,
            in_season=bool(row["in_season"]),
        )


def create_store() -> FruitStore:
    backend = os.getenv("FRUITAPI_STORE", "memory").lower()
    if backend == "mysql":
        mysql_store = MySQLFruitStore(
            host=os.environ["DB_HOST"],
            port=int(os.getenv("DB_PORT", "3306")),
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
        )
        mysql_store.initialize()
        if os.getenv("FRUITAPI_SEED_ON_START", "true").lower() == "true":
            mysql_store.seed_if_empty(DEFAULT_FRUITS)
        return mysql_store

    memory_store = InMemoryFruitStore()
    memory_store.seed(DEFAULT_FRUITS)
    return memory_store


store = create_store()
