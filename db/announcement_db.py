import datetime
import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from db.base import Base
from db.dungeon_run_db import DungeonRunDB

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
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    modified_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    has_been_sent = Column(Boolean, nullable=False, default=False)
    dungeon_run_id = Column(Integer, ForeignKey('dungeon_runs.id'))
    dungeon_run = relationship("DungeonRunDB", back_populates="announcements")
    
    def __init__(self,                 
                 discord_guild_id: int,
                 guild_name: str,
                 announcement_channel_id: int,
                 title: str,
                 description: str,
                 message: str,
                 id : int = None,
                 modified_at: datetime = datetime.datetime.utcnow(),
                 dungeon_run_id: int = None,
                 dungeon_run: DungeonRunDB = None,
                 created_at: datetime = datetime.datetime.utcnow(),
                 has_been_sent: bool = False                 
                 ):
        """AnnouncementDB constructor"""
        if id is None:
            id = uuid.uuid4()
        self.id = id    
        self.discord_guild_id = discord_guild_id
        self.guild_name = guild_name
        self.announcement_channel_id = announcement_channel_id
        self.title = title
        self.description = description
        self.message = message
        self.modified_at = modified_at
        self.dungeon_run_id = dungeon_run_id
        self.dungeon_run = dungeon_run
        self.created_at = created_at
        self.has_been_sent = has_been_sent
    def __repr__(self):
        return f"AnnouncementDB(id={self.id}, discord_guild_id={self.discord_guild_id}, guild_name={self.guild_name}, announcement_channel_id={self.announcement_channel_id}, title={self.title}, description={self.description}, message={self.message}, created_at={self.created_at}, modified_at={self.modified_at}, has_been_sent={self.has_been_sent})"
    