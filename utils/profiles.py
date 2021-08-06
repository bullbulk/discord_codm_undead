from typing import Union

import discord
import sqlalchemy.orm
from aiopg.sa.result import ResultProxy

from data.db import db_session
from data.db.models.profile import Profile


async def profile_exists(discord_user_id: int):
    session = db_session.get_session()

    res = await Profile.get(session, discord_user_id)
    return res is not None


async def create_profile(discord_id, nickname, uid, talents_lvl):
    if await profile_exists(discord_id):
        return

    session = db_session.get_session()

    profile = await Profile.create(session, id=discord_id, nickname=nickname, uid=uid, talents_lvl=talents_lvl)
    return profile


async def get_profile(user_id: int) -> Union[Profile, None]:
    session = db_session.get_session()
    res = await Profile.get(session, user_id)
    return res


async def get_user_profile_embed(user_id: int):
    profile = await get_profile(user_id)
    if not profile:
        return

    embed = discord.Embed(title='Профиль')
    embed.add_field(name='Никнейм', value=profile.nickname)
    embed.add_field(name='UID', value=str(profile.uid))
    embed.add_field(name='Всего матчей', value=str(profile.matches_count))

    if all([profile.matches_count, profile.wins_count]):
        embed.add_field(name='W/L',
                        value=str(round(profile.wins_count / profile.matches_count, 2)))

    embed.add_field(name='Уровень талантов', value=str(profile.talents_lvl))

    if profile.profile_description:
        embed.add_field(name='Описание', value=profile.profile_description)

    return embed
