import datetime

from sqlalchemy import BigInteger, String, Integer, Text, DateTime
from sqlalchemy import Column

from data.db.db_session import SqlAlchemyBase
from data.db.models.mixin import DeclarativeBaseMixin


class Profile(SqlAlchemyBase, DeclarativeBaseMixin):
    __tablename__ = 'profiles'

    id = Column(BigInteger, primary_key=True)
    nickname = Column(String)
    uid = Column(BigInteger, unique=True)
    talents_lvl = Column(Integer)
    profile_description = Column(Text)
    matches_count = Column(Integer, default=0)
    wins_count = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    register_date = Column(DateTime, default=datetime.datetime.now)
