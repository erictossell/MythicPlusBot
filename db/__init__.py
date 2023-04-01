from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
from db.characters import Character
from db.dungeonRun import DungeonRun

engine = create_engine('sqlite:///tal.db', echo=True)
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)