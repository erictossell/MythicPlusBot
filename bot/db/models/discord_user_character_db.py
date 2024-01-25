import datetime
from sqlalchemy import BigInteger, Column, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from bot.db.base import Base


class DiscordUserCharacterDB(Base):
    """Model representing a default character for a Discord user on a given server."""

    __tablename__ = "discord_user_characters"
    id = Column(Integer, primary_key=True)

    discord_user_id = Column(BigInteger)

    version = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    character_id = Column(Integer, ForeignKey("characters.id"))
    character = relationship("CharacterDB", back_populates="discord_user_characters")

    def __init__(
        self, discord_user_id: int, character_id=None, character=None, version: int = 1
    ):
        self.discord_user_id = discord_user_id

        if character_id:
            self.character_id = character_id
        else:
            self.character = character
        self.version = version

    def __repr__(self):
        return (
            f"DiscordUserCharacter(id={self.id}, discord_user_id={self.discord_user_id}, discord_guild_id={self.discord_guild_id}, "
            f"is_default_character={self.is_default_character}, version={self.version}, created_at={self.created_at}, character={self.character})"
        )
