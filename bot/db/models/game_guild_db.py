import datetime
from sqlalchemy import BigInteger, ForeignKey, String, Column, DateTime, Integer
from sqlalchemy.orm import relationship
from bot.db.base import Base


class GameGuildDB(Base):
    __tablename__ = "game_guilds"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    region = Column(String)
    realm = Column(String)

    modified_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    game_id = Column(Integer, ForeignKey("games.id"))
    game = relationship("GameDB", back_populates="game_guilds")

    characters = relationship("CharacterDB", back_populates="game_guild")
    discord_game_guilds = relationship(
        "DiscordGameGuildDB", back_populates="game_guild"
    )

    def __init__(
        self, name: str = "Default", realm: str = None, region="us", game_id: int = 1
    ):
        self.name = name
        self.realm = realm
        self.region = region
        self.game_id = game_id

    def __repr__(self):
        return f"GameGuild(id={self.id}, name={self.name}, region={self.region}, realm={self.realm}, modified_at={self.modified_at}, created_at={self.created_at})"
