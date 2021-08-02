import asyncio
from typing import List

import discord
from discord.ext import commands

from utils import profiles


async def add_reactions(message: discord.Message, emojis: List[str]):
    for i in emojis:
        await message.add_reaction(i)


class Profile(commands.Cog):
    edit_menu = {
        'никнейм': '1️⃣',
        'uid': '2️⃣',
        'уровень талантов': '3️⃣',
        'описание': '4️⃣'
    }
    edit_emoji = '📝'

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def modify_embed_for_editing(self, embed: discord.Embed):
        fields = embed.fields
        if not fields:
            return

        new_embed = discord.Embed(title='Выберите поле для редактирования')

        for i in range(len(fields)):
            field = fields[i]
            emoji = self.edit_menu.get(field.name.lower())
            if not emoji:
                continue
            new_embed.add_field(name=f'{emoji} {field.name}', value=field.value)

        return new_embed

    async def proceed_profile_edit(self, ctx: commands.Context, embed_message: discord.Message):
        if not embed_message.embeds:
            return

        embed = embed_message.embeds[0]
        await embed_message.clear_reactions()
        embed = await self.modify_embed_for_editing(embed)
        await embed_message.edit(embed=embed)

        edit_emojis = list(self.edit_menu.values()).copy()
        await add_reactions(embed_message, edit_emojis)

        def check(react, user):
            return react.emoji in edit_emojis and user.id == ctx.author.id and react.message.id == embed_message.id

        try:
            reaction = await self.bot.wait_for('reaction_add', check=check, timeout=10)
            await ctx.send(str(reaction))
        except asyncio.TimeoutError:
            await embed_message.clear_reactions()

    @commands.group()
    async def profile(self, ctx: commands.Context):
        if ctx.invoked_subcommand:
            return

        embed = profiles.user_profile_embed(ctx.author.id)
        message = await ctx.send(embed=embed)

        await message.add_reaction(self.edit_emoji)

        def check(react, user):
            return str(react.emoji) == self.edit_emoji and user == ctx.author and react.message.id == message.id

        try:
            await self.bot.wait_for('reaction_add', check=check, timeout=600)
        except asyncio.TimeoutError:
            await message.clear_reactions()
        else:
            await self.proceed_profile_edit(ctx, message)

    @profile.command()
    async def create(self, ctx: commands.Context, uid: int = None, talent_lvl: int = None):
        if profiles.profile_exists(ctx.author.id):
            return await ctx.send('Вы уже зарегистрированы в системе')
        if not uid or not talent_lvl:
            return await ctx.send(
                'Передайте свой UID и уровень талантов в виде __**z!profile create <UID> <уровень>**__')
        if 50 < talent_lvl < 0:
            return await ctx.send('Введите корректный уровень талантов')
        if len(ctx.message.attachments) != 2:
            return await ctx.send('Прикрепите к сообщению скриншоты:\n\n'
                                  'Вашего игрового профиля с рассматриваемым UID\n'
                                  'Экрана талантов')


def setup(bot):
    bot.add_cog(Profile(bot))
