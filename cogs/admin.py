from discord.ext import commands

from stubs import ZombieBotStub
from utils import extensions


class Admin(commands.Cog):
    def __init__(self, bot: ZombieBotStub):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id == self.bot.owner_id

    @commands.group()
    async def ext(self, ctx):
        pass

    @ext.command()
    async def load(self, ctx, extension=None):
        try:
            if extension:
                extensions.load_ext(self.bot, name=extension)
            else:
                extensions.load_all_ext(self.bot)
            await ctx.send('Success')
        except commands.ExtensionNotFound:
            await ctx.send('Extension not found')
        except commands.ExtensionFailed:
            await ctx.send('Extension load error')
        except commands.ExtensionError:
            await ctx.send('Extension error')

    @ext.command()
    async def reload(self, ctx, extension=None):
        try:
            if extension:
                extensions.reload_ext(self.bot, name=extension)
            else:
                extensions.reload_all_ext(self.bot)
            await ctx.send('Success')
        except commands.ExtensionNotFound:
            await ctx.send('Extension not found')
        except commands.ExtensionNotLoaded:
            await ctx.send('Extension has not been loaded')
        except commands.ExtensionFailed:
            await ctx.send('Extension load error')
        except commands.ExtensionError:
            await ctx.send('Extension error')

    @ext.command()
    async def unload(self, ctx, extension=None):
        try:
            if extension:
                extensions.unload_ext(self.bot, name=extension)
            else:
                extensions.unload_all_ext(self.bot)
            await ctx.send('Success')
        except commands.ExtensionNotFound:
            await ctx.send('Extension not found')
        except commands.ExtensionNotLoaded:
            await ctx.send('Extension has not been loaded')


def setup(bot):
    bot.add_cog(Admin(bot))
