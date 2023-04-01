from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Character(Base):
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    realm = Column(String)
    faction = Column(String)
    class_ = Column(String)
    spec = Column(String)
    role = Column(String)
    thumbnail = Column(String)
    achievement_points = Column(Integer)
    last_crawled_at = Column(DateTime)
    score = Column(Integer)
    rank = Column(Integer)
    gear = Column(Integer)
    score_color = Column(String)
    profile_url = Column(String)
    dungeon_runs = relationship("DungeonRun", back_populates="character")
    
    def __init__(self,name,realm,faction,class_,spec,role,thumbnail,achievement_points,last_crawled_at,score,rank,gear,score_color,profile_url):
        self.name = name
        self.realm = realm
        self.faction = faction
        self.class_ = class_
        self.spec = spec
        self.role = role
        self.thumbnail = thumbnail
        self.achievement_points = achievement_points
        self.last_crawled_at = last_crawled_at
        self.score = score
        self.rank = rank
        self.gear = gear
        self.score_color = score_color
        self.profile_url = profile_url
        self.dungeon_runs = []