import os

from dotenv import load_dotenv

from bot import ZombieBot

load_dotenv()

bot = ZombieBot('z!')
bot.run(token=os.getenv('DISCORD_BOT_TOKEN'))
