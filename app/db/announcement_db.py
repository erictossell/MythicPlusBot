import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.dungeon_run_db import DungeonRunDB

class AnnouncementDB(Base):
    """Stores information about announcements."""
    __tablename__ = 'announcements'
    
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    discord_guild_id = Column(Integer, nullable=False)
    guild_name = Column(String, nullable=False)
    announcement_channel_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)    
    message = Column(String, nullable=False)
    has_been_sent = Column(Boolean, nullable=False, default=False)
    dungeon_run_id = Column(Integer, ForeignKey('dungeon_runs.id'))
    dungeon_run = relationship("DungeonRunDB", back_populates="announcements")
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    modified_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    
    def __init__(self,
                 discord_guild_id: int,
                 guild_name: str,
                 announcement_channel_id: int,
                 title: str,
                 description: str,
                 message: str,
                 dungeon_run: DungeonRunDB = None,
                 has_been_sent: bool = False):
        """AnnouncementDB constructor"""
        self.discord_guild_id = discord_guild_id
        self.guild_name = guild_name
        self.announcement_channel_id = announcement_channel_id
        self.title = title
        self.description = description
        self.message = message
        self.dungeon_run = dungeon_run
        self.has_been_sent = has_been_sent
        
    def __repr__(self):
        return f"AnnouncementDB(id={self.id}, discord_guild_id={self.discord_guild_id}, guild_name={self.guild_name}, announcement_channel_id={self.announcement_channel_id}, title={self.title}, description={self.description}, message={self.message}, created_at={self.created_at}, modified_at={self.modified_at}, has_been_sent={self.has_been_sent})"
