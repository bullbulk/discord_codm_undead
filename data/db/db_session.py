import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

SqlAlchemyBase = declarative_base()
__factory: AsyncSession = None


async def init_db(name, username, password, host):
    global __factory

    engine = create_async_engine(
        f"postgresql+asyncpg://{username}:{password}@{host}/{name}",
    )
    __factory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)()

    from . import __all_models

    async with engine.begin() as conn:
        await conn.run_sync(SqlAlchemyBase.metadata.create_all)


def global_init(dbname, username, password, db_host):
    if __factory:
        return

    asyncio.get_event_loop().run_until_complete(init_db(dbname, username, password, db_host))


def get_session() -> AsyncSession:
    global __factory
    return __factory


def close_session():
    global __factory
    asyncio.run(__factory.close())
