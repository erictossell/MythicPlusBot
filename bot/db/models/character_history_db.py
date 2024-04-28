import datetime
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Boolean,
)
from sqlalchemy.orm import relationship
from bot.db.base import Base


class CharacterHistoryDB(Base):
    """CharacterDB class which is used to create the character table in the database."""

    __tablename__ = "character_history"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    realm = Column(String, nullable=False)
    faction = Column(String, nullable=True)
    region = Column(String, nullable=True)
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

    character_id = Column(Integer, ForeignKey("characters.id"))
    character = relationship("CharacterDB", back_populates="character_history")
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    modified_at = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )

    def __init__(
        self,
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
    ):
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

    def __repr__(self):
        return f"<CharacterDB(id={self.id}, discord_user_id={self.discord_user_id}, name={self.name}, realm={self.realm}, faction={self.faction}, region={self.region}, role={self.role}, spec_name={self.spec_name}, class_name={self.class_name}, achievement_points={self.achievement_points}, item_level={self.item_level}, score={self.score}, rank={self.rank}, thumbnail_url={self.thumbnail_url}, url={self.url}, last_crawled_at={self.last_crawled_at}, is_reporting={self.is_reporting})>"
