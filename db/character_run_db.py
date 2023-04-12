import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.base import Base
from db.character_db import CharacterDB
from db.dungeon_run_db import DungeonRunDB

class CharacterRunDB(Base):
    """Contains the many to many relationship between characters and dungeon runs.

    Args:
        Base (base): _description_
    """
    __tablename__ = 'character_runs'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("CharacterDB", back_populates="character_runs")
    dungeon_run_id = Column(Integer, ForeignKey('dungeon_runs.id'))
    dungeon_run = relationship("DungeonRunDB", back_populates="character_runs")
    is_personal_best = Column(Boolean)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)
    
    
    def __init__(self,
                 character: CharacterDB,
                 dungeon_run: DungeonRunDB,
                 created_at: datetime,
                 modified_at: datetime):
        """CharacterRunDB constructor"""
        self.character = character
        self.dungeon_run = dungeon_run
        self.created_at = created_at
        self.modified_at = modified_at
    def __repr__(self):
        return f"CharacterRunDB(character={self.character}, dungeon_run={self.dungeon_run}, created_at={self.created_at}, modified_at={self.modified_at})"