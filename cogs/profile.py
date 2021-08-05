import asyncio
from typing import List

import discord
from discord.ext import commands

from stubs import ZombieBotStub
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

    def __init__(self, bot: ZombieBotStub):
        self.bot = bot
        self.text_data = bot.text_data['profile']

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
            # todo: edit profile
        except asyncio.TimeoutError:
            await embed_message.clear_reactions()

    @commands.group()
    async def profile(self, ctx: commands.Context):
        if ctx.invoked_subcommand:
            return
        f_text_data = self.text_data['profile']

        embed = await profiles.get_user_profile_embed(ctx.author.id)
        if not embed:
            return await ctx.send(f_text_data['to_create'])

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
    async def create(self, ctx: commands.Context, nickname=None, uid: int = None, talents_lvl: int = None):
        f_text_data = self.text_data['create']

        if await profiles.profile_exists(ctx.author.id):
            return await ctx.send(f_text_data['profile_already_exists'])
        if not all([uid, talents_lvl, nickname]):
            return await ctx.send(f_text_data['no_parameters_provided'])
        if talents_lvl < 0 or talents_lvl > 50:
            return await ctx.send(f_text_data['incorrect_talent_lvl'])
        await profiles.create_profile(ctx.author.id, nickname, uid, talents_lvl)

    @profile.command()
    async def verify(self, ctx: commands.Context):
        f_text_data = self.text_data['verify']

        if len(ctx.message.attachments) != 2:
            return await ctx.send(f_text_data['screenshot_info'])


def setup(bot):
    bot.add_cog(Profile(bot))
