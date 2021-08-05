import discord
import sqlalchemy.orm
from aiopg.sa.result import ResultProxy

from data.db import db_session
from data.db.models.profile import Profile


async def profile_exists(discord_user_id: int):
    session = db_session.get_session()

    res = await Profile.get(session, discord_user_id)
    print(res)
    return res is not None


async def create_profile(discord_id, nickname, uid, talents_lvl):
    if await profile_exists(discord_id):
        return

    session = db_session.get_session()

    profile = await Profile.create(session, id=discord_id, nickname=nickname, uid=uid, talents_lvl=talents_lvl)


async def get_user_profile_embed(user_id: int):
    if not await profile_exists(user_id):
        return
    embed = discord.Embed(title='Профиль')
    embed.add_field(name='Никнейм', value='Value')
    embed.add_field(name='UID', value='23424')
    embed.add_field(name='Уровень талантов', value='23')
    embed.add_field(name='Описание', value='ifeksfmf')
    return embed
