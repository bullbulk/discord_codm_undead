import os

from dotenv import load_dotenv

from bot import ZombieBot
from data.db import db_session

load_dotenv()

db_session.global_init(
    os.getenv("POSTGRE_DBNAME"),
    os.getenv("POSTGRE_USERNAME"),
    os.getenv("POSTGRE_PASSWORD"),
    os.getenv("POSTGRE_DBHOST")
)

bot = ZombieBot('z!')
bot.run(os.getenv('DISCORD_BOT_TOKEN'))

db_session.close_session()
