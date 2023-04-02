from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
from db.characterDB import CharacterDB
from db.dungeonRunDB import DungeonRunDB


engine = create_engine('sqlite:///tal.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)