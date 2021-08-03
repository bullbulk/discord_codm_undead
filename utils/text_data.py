import os
from typing import Dict

import yaml
from discord.ext import commands

from stubs import ZombieBotStub


def setup(bot: ZombieBotStub):
    data: Dict[str, Dict[str, Dict[str, str]]] = {}
    base_path = 'data/text/'
    for i in os.listdir(base_path):
        with open(f'{base_path}{i}') as f:
            data[i.split('.')[0]] = yaml.safe_load(f)
    bot.text_data = data
