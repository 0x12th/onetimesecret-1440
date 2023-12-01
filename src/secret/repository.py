from typing import Any

from sqlalchemy import RowMapping, delete, insert, select

from src.db import async_session_maker
from src.secret.models import Secret


class SecretRepository:
    model = Secret

    @classmethod
    async def get_one_or_none(cls, **params: Any | None) -> Any | None:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**params)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, **params: Any | None) -> Any | list[Any]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**params)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data: Any | None) -> RowMapping | None:
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().one_or_none()

    @classmethod
    async def delete(cls, **params: Any | None) -> None:
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**params)
            await session.execute(query)
            await session.commit()
