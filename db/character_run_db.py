import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from db.base import Base
from db.character_db import CharacterDB
from db.dungeon_run_db import DungeonRunDB


class CharacterRunDB(Base):
    """Model representing the many-to-many relationship between characters and dungeon runs."""
    __tablename__ = 'character_runs'
    id = Column(Integer, primary_key=True)
    is_personal_best = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("CharacterDB", back_populates="character_runs")
    dungeon_run_id = Column(Integer, ForeignKey('dungeon_runs.id'))
    dungeon_run = relationship("DungeonRunDB", back_populates="character_runs")

    def __init__(self, character: CharacterDB, dungeon_run: DungeonRunDB, is_personal_best: bool = False):
        """
        CharacterRunDB constructor.

        Args:
            character (CharacterDB): The related CharacterDB instance.
            dungeon_run (DungeonRunDB): The related DungeonRunDB instance.
            is_personal_best (bool, optional): Whether this run is a personal best for the character. Defaults to False.
        """
        self.character = character
        self.dungeon_run = dungeon_run
        self.is_personal_best = is_personal_best

    def __repr__(self):
        return f"CharacterRunDB(id={self.id}, character={self.character}, dungeon_run={self.dungeon_run}, " \
               f"is_personal_best={self.is_personal_best}, created_at={self.created_at}, modified_at={self.modified_at})"
