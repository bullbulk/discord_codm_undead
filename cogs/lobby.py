from discord.ext import commands

from stubs import ZombieBotStub


class Lobby(commands.Cog):
    def __init__(self, bot: ZombieBotStub):
        self.bot = bot

    @commands.group()
    async def lobby(self, ctx):
        pass

    @lobby.command()
    async def create(self, ctx):
        pass

    @lobby.command()
    async def list(self, ctx):
        pass

    @lobby.command()
    async def join(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Lobby(bot))
