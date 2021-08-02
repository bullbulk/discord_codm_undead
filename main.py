import os

from dotenv import load_dotenv

from bot import ZombieBot

load_dotenv()

bot = ZombieBot('z!')
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
