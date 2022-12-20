import asyncio
from typing import Annotated, Optional

from sqlmodel import Field, SQLModel, create_async_engine


class Team(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True)]
    name: Annotated[str, Field(index=True)]
    headquarters: str


class Hero(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True)]
    name: Annotated[str, Field(index=True)]
    secret_name: str
    age: Annotated[Optional[int], Field(default_factory=lambda: None, index=True)]

    team_id: Annotated[
        Optional[int], Field(default_factory=lambda: None, foreign_key="team.id")
    ]


sqlite_file_name = "database.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

engine = create_async_engine(sqlite_url, echo=True)


async def create_db_and_tables() -> None:
    meta = SQLModel.metadata

    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)


async def main() -> None:
    await create_db_and_tables()


if __name__ == "__main__":
    asyncio.run(main())
