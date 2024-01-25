import datetime
from sqlalchemy import BigInteger, String, Boolean, Column, DateTime, Integer
from sqlalchemy.orm import relationship
from bot.db.base import Base


class DiscordGuildDB(Base):
    __tablename__ = "discord_guilds"

    id = Column(BigInteger, primary_key=True)
    discord_guild_name = Column(String)

    players_per_run = Column(Integer, default=4)
    announcement_channel_id = Column(BigInteger)
    is_announcing = Column(Boolean, default=False)
    modified_by = Column(BigInteger)
    modified_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    announcements = relationship("AnnouncementDB", back_populates="discord_guild")
    discord_game_guilds = relationship(
        "DiscordGameGuildDB", back_populates="discord_guild"
    )

    discord_guild_runs = relationship(
        "DiscordGuildRunDB", back_populates="discord_guild"
    )
    discord_guild_characters = relationship(
        "DiscordGuildCharacterDB", back_populates="discord_guild"
    )

    def __init__(
        self,
        id: int,
        discord_guild_name: str,
        announcement_channel_id: int = None,
        is_announcing: bool = False,
        modified_by: int = None,
        modified_at: datetime.datetime = None,
        created_at: datetime.datetime = None,
    ):
        self.id = id
        self.discord_guild_name = discord_guild_name
        self.announcement_channel_id = announcement_channel_id
        self.is_announcing = is_announcing
        self.modified_by = modified_by
        self.modified_at = modified_at
        self.created_at = created_at

    def __repr__(self):
        return f"DiscordGuild(id={self.id}, discord_guild_name={self.discord_guild_name}, wow_guild_name={self.wow_guild_name}, announcement_channel_id={self.announcement_channel_id}, is_announcing={self.is_announcing}, modified_by={self.modified_by}, modified_at={self.modified_at}, created_at={self.created_at})"
