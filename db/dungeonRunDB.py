from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.base import Base


class DungeonRunDB(Base):
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
    is_personal_best = Column(Boolean)
    is_crawled = Column(Boolean)
    
    character_id = Column(Integer, ForeignKey('characters.id'))   
    character = relationship("CharacterDB", back_populates="dungeon_runs")
    
    
    def __init__(self,id, season, name, short_name, mythic_level, completed_at, clear_time_ms, par_time_ms, num_keystone_upgrades, score, url, character):
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
        self.is_personal_best = False
        self.is_crawled = False
        
        self.character = character
    
    
          
        
        
        