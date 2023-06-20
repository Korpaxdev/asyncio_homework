import os

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from classes.models import Base, Characters


class Alchemy:
    DB = os.getenv("DATABASE", "sqlite+aiosqlite:///database/database.db")
    engine: AsyncEngine = None

    @classmethod
    def create_engine(cls):
        cls.engine = create_async_engine(cls.DB)
        return cls

    @classmethod
    def get_session(cls):
        session = async_sessionmaker(bind=cls.engine, class_=AsyncSession, expire_on_commit=False)
        return session()

    @classmethod
    async def engine_off(cls):
        return await cls.engine.dispose()

    @classmethod
    async def create_tables(cls):
        async with cls.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def insert_character_into_db(cls, character):
        async with cls.get_session() as session:
            if character:
                char = Characters(**character)
                session.add(char)
                await session.commit()
                print(f"Персонаж {char.name} успешно добавлен в бд")
                return char
