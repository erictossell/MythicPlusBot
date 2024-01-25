import datetime
from sqlalchemy import BigInteger, Boolean, ForeignKey, Column, DateTime, Integer
from sqlalchemy.orm import relationship
from bot.db.base import Base
from bot.db.models.discord_guild_db import DiscordGuildDB

class DiscordGuildCharacterDB(Base):
    
    __tablename__ = 'discord_guild_characters'
    
    id = Column(Integer, primary_key=True)
    
    guild_character_score = Column(Integer, nullable=True)
    
    
    discord_guild_id = Column(BigInteger, ForeignKey('discord_guilds.id'))
    discord_guild = relationship("DiscordGuildDB", back_populates="discord_guild_characters")
    
    character_id = Column(BigInteger, ForeignKey('characters.id'))
    character = relationship("CharacterDB", back_populates="discord_guild_characters")
    
    is_reporting = Column(Boolean, nullable=False, default=True)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __init__(self,
                 is_reporting: bool = True,
                 discord_guild_id: int = None,
                 discord_guild : DiscordGuildDB = None,
                 character_id: int = None,
                 character = None):
        
        self.is_reporting = is_reporting
        if discord_guild_id:
            self.discord_guild_id = discord_guild_id
        else:
            self.discord_guild = discord_guild
        
        if character_id:
            self.character_id = character_id
        else:
            self.character = character
            
    def __repr__(self):
        return f'DiscordGuildCharacter(id={self.id}, discord_guild_id={self.discord_guild_id}, character_id={self.character_id}, modified_at={self.modified_at}, created_at={self.created_at})'
    
