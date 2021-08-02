import discord


def profile_exists(user_id: int):
    return False


def user_profile_embed(user_id: int):
    embed = discord.Embed(title='Профиль')
    embed.add_field(name='Никнейм', value='Value')
    embed.add_field(name='UID', value='23424')
    embed.add_field(name='Уровень талантов', value='23')
    embed.add_field(name='Описание', value='ifeksfmf')
    return embed
