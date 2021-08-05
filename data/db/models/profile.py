import datetime

import sqlalchemy as sa
from sqlalchemy import Table
from sqlalchemy import Column

Profile = Table(
    'profiles', sa.MetaData(),
    Column('discord_id', sa.BigInteger, unique=True),
    Column('nickname', sa.String),

    Column('uid', sa.BigInteger, unique=True),
    Column('talents_lvl', sa.Integer),
    Column('profile_description', sa.Text),
    Column('matches_count', sa.Integer),
    Column('wins_count', sa.Integer),
    Column('likes', sa.Integer),
    Column('dislikes', sa.Integer),
    Column('register_date', sa.DateTime, default=datetime.datetime.now),

)
