from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.models.dungeon_run_db import DungeonRunDB

class AnnouncementDB(Base):
    """Model representing an announcement in the database."""

    __tablename__ = 'announcements'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    discord_guild_id = Column(Integer)
    announcement_channel_id = Column(Integer)
    has_been_sent = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    dungeon_run_id = Column(Integer, ForeignKey('dungeon_runs.id'))
    dungeon_run = relationship("DungeonRunDB", back_populates="announcements")

    def __init__(self,
                 title: str,
                 content: str,
                 discord_guild_id :int,
                 announcement_channel_id:int,
                 has_been_sent : bool = False ,
                 id: int = None,
                 dungeon_run_id: int = None,
                 dunegon_run: DungeonRunDB = None):
        """
        AnnouncementDB constructor.

        Args:
            id (int): The unique ID of the announcement.
            title (str): The title of the announcement.
            content (str): The content of the announcement.
            dungeon_run_id (int): The ID of the related dungeon run.
        """
        self.id = id
        self.title = title
        self.content = content
        self.discord_guild_id = discord_guild_id
        self.announcement_channel_id = announcement_channel_id
        self.has_been_sent = has_been_sent
        if dungeon_run_id:
            self.dungeon_run_id = dungeon_run_id
        else:
            self.dungeon_run = dunegon_run
