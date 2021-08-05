from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select


class DeclarativeBaseMixin:
    @classmethod
    async def create(cls, async_db_session: AsyncSession, **kwargs):
        instance = cls(**kwargs)
        async_db_session.add(instance)
        await async_db_session.commit()
        return instance

    @classmethod
    async def update(cls, async_db_session: AsyncSession, id_, **kwargs):
        query = update(cls).where(cls.id == id_).values(**kwargs)

        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get(cls, async_db_session: AsyncSession, id_):
        query = select(cls).where(cls.id == id_)

        results = await async_db_session.execute(query)

        res = results.first()

        if not res:
            return

        (res,) = res
        return res
