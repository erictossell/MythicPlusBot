import datetime
from sqlalchemy import BigInteger, Boolean, ForeignKey, Column, DateTime, Integer
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.models.discord_guild_db import DiscordGuildDB

class DiscordGuildRunDB(Base):
    
    __tablename__ = 'discord_guild_runs'
    id = Column(Integer, primary_key=True)
    
    discord_guild_id = Column(BigInteger, ForeignKey('discord_guilds.id'))
    discord_guild = relationship("DiscordGuildDB", back_populates="discord_guild_runs")
    
    dungeon_run_id = Column(Integer, ForeignKey('dungeon_runs.id'))
    dungeon_run = relationship("DungeonRunDB", back_populates="discord_guild_runs")
    
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __init__(self,
                 discord_guild_id: int = None,
                 discord_guild : DiscordGuildDB = None,
                 dungeon_run_id: int = None,
                 dungeon_run = None):
        
        if discord_guild_id:
            self.discord_guild_id = discord_guild_id
        else:
            self.discord_guild = discord_guild
        if dungeon_run_id:
            self.dungeon_run_id = dungeon_run_id
        else:
            self.dungeon_run = dungeon_run
            
    def __repr__(self):
        return f'DiscordGuildRun(id={self.id}, discord_guild_id={self.discord_guild_id}, dungeon_run_id={self.dungeon_run_id}, modified_at={self.modified_at}, created_at={self.created_at})'