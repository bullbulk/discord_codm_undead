import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool


SqlAlchemyBase = declarative_base()
__factory: AsyncSession = None
__engine = None


async def init_db(name, username, password, host):
    global __factory, __engine

    # if poolclass=NullPool is not provided, running AsyncEngine.dispose() in other loop will raise RuntimeError
    # discord.Bot.run() in the end closes the running loop, which AsyncEngine uses, and we can't open it
    __engine = create_async_engine(
        f"postgresql+asyncpg://{username}:{password}@{host}/{name}", poolclass=NullPool
    )
    __factory = sessionmaker(__engine, expire_on_commit=False, class_=AsyncSession)()

    from . import __all_models

    async with __engine.begin() as conn:
        await conn.run_sync(SqlAlchemyBase.metadata.create_all)


def global_init(dbname, username, password, db_host):
    if __factory:
        return

    asyncio.get_event_loop().run_until_complete(init_db(dbname, username, password, db_host))


def get_session() -> AsyncSession:
    global __factory
    return __factory


def close_session():
    global __engine
    asyncio.run(__engine.dispose())
