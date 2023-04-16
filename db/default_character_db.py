import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.base import Base
from db.character_db import CharacterDB


class DefaultCharacterDB(Base):
    """Model representing a default character for a Discord user on a given server."""

    __tablename__ = 'default_characters'
    id = Column(Integer, primary_key=True)
    discord_user_id = Column(Integer)
    discord_guild_id = Column(Integer)
    is_default_character = Column(Boolean, default=True)
    version = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("CharacterDB", back_populates="default_character")

    def __init__(self, discord_user_id: int, discord_guild_id: int, character_id=None, character=None, version: int = 1):
        self.discord_user_id = discord_user_id
        self.discord_guild_id = discord_guild_id
        if character_id:
            self.character_id = character_id
        else:
            self.character = character
        self.version = version
        self.is_default_character = True

    def __repr__(self):
        return f"DefaultCharacterDB(id={self.id}, discord_user_id={self.discord_user_id}, discord_guild_id={self.discord_guild_id}, " \
               f"is_default_character={self.is_default_character}, version={self.version}, created_at={self.created_at}, character={self.character})"
