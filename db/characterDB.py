from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.base import Base
from db.dungeonRunDB import DungeonRunDB


class CharacterDB(Base):
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True) 
    discord_user_id = Column(Integer)   
    
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
    
    dungeon_runs = relationship("DungeonRunDB", back_populates="character")  
    
    def __init__(self, discord_user_id, name, realm, faction, region, role, spec_name, class_name, achievement_points, item_level, score, rank, thumbnail_url, url, last_crawled_at, is_reporting, dungeon_runs):
        self.discord_user_id = discord_user_id
        
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
        
        self.dungeon_runs = dungeon_runs
        
    def __repr__(self):
        return f"CharacterDB(discord_user_id={self.discord_user_id}, name={self.name}, realm={self.realm}, faction={self.faction}, region={self.region}, role={self.role}, spec_name={self.spec_name}, class_name={self.class_name}, achievement_points={self.achievement_points}, item_level={self.item_level}, score={self.score}, rank={self.rank}, thumbnail_url={self.thumbnail_url}, url={self.url}, last_crawled_at={self.last_crawled_at}, is_reporting={self.is_reporting}, dungeon_runs={self.dungeon_runs})"