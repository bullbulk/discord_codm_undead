import asyncio

from aiopg.sa import create_engine, SAConnection
from sqlalchemy.sql.ddl import CreateTable

__factory = None


async def execute_if_table_exists(conn, table_name, query):
    q = f"""SELECT *
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_NAME = '{table_name}'"""
    res = await conn.execute(q)

    if not await res.first():
        await conn.execute(query)


async def create_tables():
    from .__all_models import models

    conn = get_session()

    for model in models:
        await execute_if_table_exists(conn, model, CreateTable(model))


async def init_db(name, username, password, host):
    global __factory

    engine = await create_engine(host=host,
                                 database=name,
                                 user=username,
                                 password=password,
                                )
    __factory = await engine.acquire()

    await create_tables()


def global_init(dbname, username, password, db_host):
    if __factory:
        return

    asyncio.get_event_loop().run_until_complete(init_db(dbname, username, password, db_host))


def get_session() -> SAConnection:
    global __factory
    return __factory


__factory: SAConnection


async def close_session():
    global __factory
    await __factory.close()
