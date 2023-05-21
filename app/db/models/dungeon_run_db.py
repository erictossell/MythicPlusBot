#---------------Take a Lap Discord Bot-----------------
# Description: This file contains the DungeonRunDB class which is used to create the dungeon_runs table in the database.
# Author: Eriim
import datetime
from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class DungeonRunDB(Base):
    """Model representing a dungeon run in the database."""

    __tablename__ = 'dungeon_runs'

    id = Column(Integer, primary_key=True)
    dungeon_id = Column(BigInteger)
    season = Column(String)
    name = Column(String)
    short_name = Column(String)
    mythic_level = Column(Integer)
    completed_at = Column(DateTime)
    clear_time_ms = Column(BigInteger)
    par_time_ms = Column(BigInteger)
    num_keystone_upgrades = Column(Integer)
    score = Column(Integer)
    url = Column(String)
    is_guild_run = Column(Boolean, default=False)
    is_crawled = Column(Boolean, default=False)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    character_runs = relationship("CharacterRunDB", back_populates="dungeon_run")
    announcements = relationship("AnnouncementDB", back_populates="dungeon_run")
    discord_guild_runs = relationship("DiscordGuildRunDB", back_populates="dungeon_run")

    def __init__(self, dungeon_id, season, name, short_name, mythic_level, completed_at, clear_time_ms, par_time_ms, num_keystone_upgrades, score, url):
        """
        DungeonRunDB constructor.

        Args:
            id (int): The unique ID of the dungeon run.
            season (str): The season in which the dungeon run took place.
            name (str): The name of the dungeon.
            short_name (str): The short name of the dungeon.
            mythic_level (int): The Mythic level of the dungeon run.
            completed_at (datetime): The completion time of the dungeon run.
            clear_time_ms (int): The clear time of the dungeon run in milliseconds.
            par_time_ms (int): The par time of the dungeon run in milliseconds.
            num_keystone_upgrades (int): The number of Keystone upgrades obtained during the dungeon run.
            score (int): The score obtained during the dungeon run.
            url (str): The URL related to the dungeon run.
        """
        self.dungeon_id = dungeon_id
        self.season = season
        self.name = name
        self.short_name = short_name
        self.mythic_level = mythic_level
        self.completed_at = completed_at
        self.clear_time_ms = clear_time_ms
        self.par_time_ms = par_time_ms
        self.num_keystone_upgrades = num_keystone_upgrades
        self.score = score
        self.url = url

    def __repr__(self):
        """
        Returns a readable representation of the DungeonRunDB object.

        Returns:
            str: Readable format of the DungeonRunDB object.
        """
        return f"DungeonRunDB(id={self.id}, season={self.season}, name={self.name}, short_name={self.short_name}, " \
               f"mythic_level={self.mythic_level}, completed_at={self.completed_at}, clear_time_ms={self.clear_time_ms}, " \
               f"par_time_ms={self.par_time_ms}, num_keystone_upgrades={self.num_keystone_upgrades}, score={self.score}, url={self.url})"
