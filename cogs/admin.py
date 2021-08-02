from discord.ext import commands

from utils import extensions


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id == self.bot.owner_id

    @commands.group()
    async def cogs(self, ctx):
        pass

    @cogs.command()
    async def load(self, ctx, cog=None):
        cog = f'cogs.{cog}'
        try:
            if cog:
                extensions.load_ext(self.bot, name=cog)
            else:
                extensions.load_all_ext(self.bot)
            await ctx.send('Success')
        except commands.ExtensionNotFound:
            await ctx.send('Extension not found')
        except commands.ExtensionFailed:
            await ctx.send('Extension load error')
        except commands.ExtensionError:
            await ctx.send('Extension error')

    @cogs.command()
    async def reload(self, ctx, cog=None):
        cog = f'cogs.{cog}'
        try:
            if cog:
                extensions.reload_ext(self.bot, name=cog)
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

    @cogs.command()
    async def unload(self, ctx, cog=None):
        cog = f'cogs.{cog}'
        try:
            if cog:
                extensions.unload_ext(self.bot, name=cog)
            else:
                extensions.unload_all_ext(self.bot)
            await ctx.send('Success')
        except commands.ExtensionNotFound:
            await ctx.send('Extension not found')
        except commands.ExtensionNotLoaded:
            await ctx.send('Extension has not been loaded')


def setup(bot):
    bot.add_cog(Admin(bot))
