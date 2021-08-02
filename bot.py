import os
import traceback
from datetime import datetime
from typing import Dict

import discord
from discord.ext import commands
from dotenv import dotenv_values

# from discord_slash import SlashCommand
from utils import extensions


class ZombieBot(commands.Bot):
    last_message: str
    owner: discord.User

    ignoring_exceptions = [
        commands.CommandNotFound,
        commands.CheckFailure
    ]

    def __init__(self, command_prefix, **options):
        intents = discord.Intents.all()
        super().__init__(command_prefix, intents=intents, **options)

        self.owner_id = int(os.getenv('DISCORD_OWNER_ID'))
        # self.slash = SlashCommand(self, sync_commands=True, sync_on_cog_reload=True)

    async def on_ready(self):
        self.owner = await self.fetch_user(self.owner_id)
        extensions.load_all_ext(self)

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        self.last_message = message.content
        await self.process_commands(message)

    async def on_command_error(self, ctx, exception):
        if type(exception) in self.ignoring_exceptions:
            return
        tb = \
            f'{"-" * 15}{datetime.now()}{"-" * 15}\n' \
            f'Command: {self.last_message}\n' \
            f'{"".join(traceback.format_exception(type(exception), exception, exception.__traceback__))}'

        await self.owner.send(tb)

    async def on_error(self, *args, **kwargs):
        tb = \
            f'{"-" * 15}{datetime.now()}{"-" * 15}\n' \
            f'{traceback.format_exc()}'

        await self.owner.send(tb)
