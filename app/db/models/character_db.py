#---------------Take a Lap Discord Bot-----------------
#Description: This file contains the CharacterDB class which is used to create the character table in the database.
#Author: Eriim

import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

from app.db.models.game_guild_db import GameGuildDB


class CharacterDB(Base):
    """CharacterDB class which is used to create the character table in the database."""
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True)       
    name = Column(String, nullable=False)
    realm = Column(String, nullable=False)
    faction = Column(String, nullable=False)
    region = Column(String, nullable=False)
    role = Column(String, nullable=True)
    spec_name = Column(String, nullable=True)
    class_name = Column(String, nullable=False)
    achievement_points = Column(Integer, nullable=False)
    item_level = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    rank = Column(Integer, nullable=False)  
    thumbnail_url = Column(String, nullable=False)
    url = Column(String, nullable=False)
    last_crawled_at = Column(DateTime, nullable=False)
    
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    game_guild_id = Column(BigInteger, ForeignKey('game_guilds.id'), nullable=True)
    game_guild = relationship("GameGuildDB", back_populates="characters")
    
    character_runs = relationship("CharacterRunDB",
                                  back_populates="character",
                                  cascade="all, delete-orphan")
    discord_user_characters = relationship("DiscordUserCharacterDB",
                                     back_populates="character",
                                     uselist=False,
                                     cascade="all, delete-orphan")
    character_history = relationship("CharacterHistoryDB",
                                     back_populates="character",
                                     cascade="all, delete-orphan")
    
    discord_guild_characters = relationship("DiscordGuildCharacterDB",
                                     back_populates="character",
                                     cascade="all, delete-orphan")
    

    def __init__(self,                                 
                 
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
                 game_guild_id: int = None,
                 game_guild: GameGuildDB = None,
                 id = None):
        """CharacterDB constructor"""   
        
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
        self.id = id
        
        if game_guild_id:
            self.game_guild_id = game_guild_id
        elif game_guild:
            self.game_guild = game_guild
        
    def __repr__(self):
        return f"<CharacterDB(id={self.id}, discord_user_id={self.discord_user_id}, name={self.name}, realm={self.realm}, faction={self.faction}, region={self.region}, role={self.role}, spec_name={self.spec_name}, class_name={self.class_name}, achievement_points={self.achievement_points}, item_level={self.item_level}, score={self.score}, rank={self.rank}, thumbnail_url={self.thumbnail_url}, url={self.url}, last_crawled_at={self.last_crawled_at}, is_reporting={self.is_reporting})>"
