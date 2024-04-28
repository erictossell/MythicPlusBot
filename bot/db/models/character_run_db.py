import datetime
from sqlalchemy import BigInteger, Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from bot.db.base import Base
from bot.db.models.character_db import CharacterDB
from bot.db.models.dungeon_run_db import DungeonRunDB


class CharacterRunDB(Base):
    """Model representing the many-to-many relationship between characters and dungeon runs."""

    __tablename__ = "character_runs"
    id = Column(Integer, primary_key=True)
    spec_name = Column(String, nullable=True)
    role = Column(String, nullable=True)
    rank_world = Column(Integer, nullable=True)
    rank_region = Column(Integer, nullable=True)
    rank_realm = Column(Integer, nullable=True)
    rio_character_id = Column(BigInteger, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    character_id = Column(Integer, ForeignKey("characters.id"))
    character = relationship("CharacterDB", back_populates="character_runs")
    dungeon_run_id = Column(Integer, ForeignKey("dungeon_runs.id"))
    dungeon_run = relationship("DungeonRunDB", back_populates="character_runs")

    def __init__(
        self,
        character: CharacterDB,
        dungeon_run: DungeonRunDB,
        rio_character_id: int = None,
        spec_name: str = None,
        role: str = None,
        rank_world: int = None,
        rank_region: int = None,
        rank_realm: int = None,
    ):
        """
        CharacterRunDB constructor.

        Args:
            character (CharacterDB): The related CharacterDB instance.
            dungeon_run (DungeonRunDB): The related DungeonRunDB instance.
            is_personal_best (bool, optional): Whether this run is a personal best for the character. Defaults to False.
        """
        self.character = character
        self.dungeon_run = dungeon_run
        self.rio_character_id = rio_character_id
        self.spec_name = spec_name
        self.role = role
        self.rank_world = rank_world
        self.rank_region = rank_region
        self.rank_realm = rank_realm

    def __repr__(self):
        return (
            f"CharacterRunDB(id={self.id}, character={self.character}, dungeon_run={self.dungeon_run}, "
            f"is_personal_best={self.is_personal_best}, created_at={self.created_at}, modified_at={self.modified_at})"
        )
