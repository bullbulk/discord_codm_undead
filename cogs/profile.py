import discord
from discord.ext import commands

from utils import profiles


class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    async def profile(self, ctx: commands.Context):
        if ctx.invoked_subcommand:
            return

        await ctx.send(embed=profiles.user_profile_embed(ctx.author.id))

    @profile.command()
    async def create(self, ctx: commands.Context, uid: int = None, talent_lvl: int = None):
        if profiles.profile_exists(ctx.author.id):
            return await ctx.send('Вы уже зарегистрированы в системе')
        if not uid or not talent_lvl:
            return await ctx.send(
                'Передайте свой UID и уровень талантов в виде __**z!profile create <UID> <уровень>**__')
        if 50 < talent_lvl < 0:
            return await ctx.send('Введите корректный уровень талантов')
        ctx.message: discord.Message
        if len(ctx.message.attachments) != 2:
            return await ctx.send('Прикрепите к сообщению скриншоты:\n\n'
                                  'Вашего игрового профиля с рассматриваемым UID\n'
                                  'Экрана талантов')



def setup(bot):
    bot.add_cog(Profile(bot))
