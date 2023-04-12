#---------------Take a Lap Discord Bot-----------------
#Description: This file contains the CharacterDB class which is used to create the character table in the database.
#Author: Eriim

import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.base import Base


class CharacterDB(Base):
    """CharacterDB class which is used to create the character table in the database."""
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True)
    discord_user_id = Column(Integer)
    discord_guild_id = Column(Integer)    
    guild_name = Column(String)    
    name = Column(String)
    realm = Column(String)
    faction = Column(String)
    region = Column(String)
    role = Column(String)
    spec_name = Column(String)
    class_name = Column(String)
    achievement_points = Column(Integer)
    item_level = Column(Integer)
    score = Column(Integer)
    rank = Column(Integer)  
    thumbnail_url = Column(String)
    url = Column(String)
    last_crawled_at = Column(DateTime)
    is_reporting = Column(Boolean)
    character_runs = relationship("CharacterRunDB", back_populates="character")
    default_character = relationship("DefaultCharacterDB", back_populates="character")
    def __init__(self,
                 discord_user_id: int,
                 discord_guild_id: int,                 
                 guild_name: str,
                 name: str,
                 realm: str,
                 faction: str,
                 region: str,
                 role: str,
                 spec_name: str,
                 class_name: str,
                 achievement_points: int,
                 item_level: int,
                 score: int,
                 rank: int,
                 thumbnail_url: str,
                 url: str,
                 last_crawled_at: datetime,
                 is_reporting: bool):
        """CharacterDB constructor"""
        self.discord_user_id = discord_user_id
        self.discord_guild_id = discord_guild_id 
        self.guild_name = guild_name    
        self.name = name
        self.realm = realm
        self.faction = faction
        self.region = region
        self.role = role
        self.spec_name = spec_name        
        self.class_name = class_name
        self.achievement_points = achievement_points
        self.item_level = item_level
        self.score = score
        self.rank = rank
        self.thumbnail_url = thumbnail_url
        self.url = url
        self.last_crawled_at = last_crawled_at
        self.is_reporting = is_reporting
        self.character_runs = []
        
        
    def __repr__(self):
        return f"CharacterDB(discord_user_id={self.discord_user_id}, name={self.name}, realm={self.realm}, faction={self.faction}, region={self.region}, role={self.role}, spec_name={self.spec_name}, class_name={self.class_name}, achievement_points={self.achievement_points}, item_level={self.item_level}, score={self.score}, rank={self.rank}, thumbnail_url={self.thumbnail_url}, url={self.url}, last_crawled_at={self.last_crawled_at}, is_reporting={self.is_reporting}, dungeon_runs={self.character_runs})"