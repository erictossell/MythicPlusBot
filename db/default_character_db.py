import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.base import Base
from db.character_db import CharacterDB

class DefaultCharacterDB(Base):
    """Contains a default character for a discord user for a given server.

    Args:
        Base (base): _description_
    """
    __tablename__ = 'default_characters'   
    id = Column(Integer, primary_key=True)
    discord_user_id = Column(Integer)
    discord_guild_id = Column(Integer)
    is_default_character = Column(Boolean)
    version = Column(Integer)
    created_at = Column(DateTime)
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("CharacterDB", back_populates="default_character")
    def __init__(self,
                 discord_user_id: int,                
                 discord_guild_id: int,
                 is_default_character: bool,
                 version: int,
                 created_at: datetime,
                 character: CharacterDB):
        """DefaultCharacterDB constructor"""
        self.discord_user_id = discord_user_id
        self.discord_guild_id = discord_guild_id
        self.is_default_character = is_default_character
        self.version = version
        self.created_at = created_at
        self.character = character
    def __repr__(self):
        return f"DefaultCharacterDB(discord_user_id={self.discord_user_id}, guild_id={self.guild_id}, is_default_character={self.is_default_character}, version={self.version}, created_at={self.created_at}, character={self.character})"