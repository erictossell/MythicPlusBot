import datetime
from sqlalchemy import DateTime, Column, Integer, String
from sqlalchemy.orm import relationship
from bot.db.base import Base
from bot.db.models.game_guild_db import GameGuildDB


class GameDB(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    modified_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    game_guilds = relationship("GameGuildDB", back_populates="game")

    def __init__(self, name: str = "World of Warcraft"):
        self.name = name

