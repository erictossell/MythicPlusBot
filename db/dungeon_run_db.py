#---------------Take a Lap Discord Bot-----------------
# Description: This file contains the DungeonRunDB class which is used to create the dungeon_runs table in the database.
# Author: Eriim
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.base import Base

class DungeonRunDB(Base):
    """DungeonRunDB class is used to create the dungeon_runs table in the database.

    Args:
        Base (Base): The base type for the DB.

    Returns:
        DungeonRunDB: Holds the dungeon_runs table in the database.
    """
    __tablename__ = 'dungeon_runs'

    id = Column(Integer, primary_key=True)
    season = Column(String)
    name = Column(String)
    short_name = Column(String)
    mythic_level = Column(Integer)    
    completed_at = Column(DateTime)
    clear_time_ms = Column(Integer)
    par_time_ms = Column(Integer)
    num_keystone_upgrades = Column(Integer)
    score = Column(Integer)
    url = Column(String)
    is_guild_run = Column(Boolean)
    is_crawled = Column(Boolean)
    character_runs = relationship("CharacterRunDB", back_populates="dungeon_run")

    def __init__(self,
                 id,
                 season,
                 name,
                 short_name,
                 mythic_level,
                 completed_at,
                 clear_time_ms,
                 par_time_ms,
                 num_keystone_upgrades,
                 score,
                 url):
        """DungeonRunDB constructor"""
        self.id = id
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
        self.is_guild_run = False
        self.is_crawled = False
                
    def __repr__(self):
        """This method is used to print the DungeonRunDB object in a readable format.

        Returns:
            string: Readable format of the DungeonRunDB object.
        """
        return f"DungeonRunDB(id={self.id}, season={self.season}, name={self.name}, short_name={self.short_name}, mythic_level={self.mythic_level}, completed_at={self.completed_at}, clear_time_ms={self.clear_time_ms}, par_time_ms={self.par_time_ms}, num_keystone_upgrades={self.num_keystone_upgrades}, score={self.score}, url={self.url})" 
    
          
        
        
        