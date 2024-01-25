import datetime
from sqlalchemy import BigInteger, Boolean, ForeignKey, Column, DateTime, Integer
from sqlalchemy.orm import relationship
from bot.db.base import Base
from bot.db.models.discord_guild_db import DiscordGuildDB
from bot.db.models.game_guild_db import GameGuildDB

class DiscordGameGuildDB(Base):
    
    __tablename__ = 'discord_game_guilds'
    id = Column(Integer, primary_key=True)
    
    discord_guild_id = Column(BigInteger, ForeignKey('discord_guilds.id'))
    discord_guild = relationship("DiscordGuildDB", back_populates="discord_game_guilds")
    
    game_guild_id = Column(BigInteger, ForeignKey('game_guilds.id'))
    game_guild = relationship("GameGuildDB", back_populates="discord_game_guilds")
    
    
    is_crawlable = Column(Boolean, default=False)  
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __init__(self,
                 is_crawlable : bool = False,
                 discord_guild_id: int = None,
                 discord_guild : DiscordGuildDB = None,
                 game_guild_id: int = None,
                 game_guild : GameGuildDB = None):
        
        self.is_crawlable = is_crawlable
        if discord_guild_id:
            self.discord_guild_id = discord_guild_id
        else: 
            self.discord_guild = discord_guild
        if game_guild_id:
            self.game_guild_id = game_guild_id
        else:
            self.game_guild = game_guild
            
    def __repr__(self):
        return f'DiscordGameGuildDB(id={self.id}, discord_guild_id={self.discord_guild_id}, game_guild_id={self.game_guild_id}, modified_at={self.modified_at}, created_at={self.created_at})'
        
        
    
