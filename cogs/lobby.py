from discord.ext import commands


class Lobby(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Lobby(bot))
