import asyncio
from typing import Annotated, Optional

from sqlmodel import AsyncSession, Field, SQLModel, create_async_engine, select


class Hero(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True)]
    name: str
    secret_name: str
    age: Optional[int] = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

engine = create_async_engine(sqlite_url, echo=True)


async def create_db_and_tables() -> None:
    meta = SQLModel.metadata

    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)


async def create_heroes() -> None:
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    async with AsyncSession(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        await session.commit()


async def select_heroes() -> None:
    async with AsyncSession(engine) as session:
        statement = select(Hero)
        results = await session.exec(statement)
        heroes = results.all()
        print(heroes)


async def main() -> None:
    await create_db_and_tables()
    await create_heroes()
    await select_heroes()


if __name__ == "__main__":
    asyncio.run(main())
