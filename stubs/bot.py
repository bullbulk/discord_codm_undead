from typing import Dict, List

import discord
from discord.ext import commands


class ZombieBotStub(commands.Bot):
    text_data: Dict[str, Dict[str, Dict[str, str]]]
    last_message: str
    owner: discord.User
    ignoring_exceptions: List[Exception]
