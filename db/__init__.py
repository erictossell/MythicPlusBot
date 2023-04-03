from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
from db.characterDB import CharacterDB
from db.dungeonRunDB import DungeonRunDB

engine = create_engine('sqlite:///tal.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def lookupCharacter(name, realm):
        session = Session()
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == name and CharacterDB.realm == realm).first()
        if existing_character != None:
            return existing_character
        else:
            return None
def lookupRun(id):
        session = Session()
        existing_run = session.query(DungeonRunDB).filter(DungeonRunDB.id == id).first()
        if existing_run != None:
            return existing_run
        else:
            return None
def addCharacter(character):
    try:
        session = Session()
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name and CharacterDB.realm == character.realm).first()
        if existing_character == None:
            characterDB = CharacterDB(character.discord_user_id, character.name, character.realm, character.faction, character.region, character.role, character.spec_name, character.class_name, character.achievement_points, character.item_level, character.score, character.rank, character.thumbnail_url, character.url, character.last_crawled_at, character.is_reporting, character.dungeon_runs)
            session.add(characterDB)
            session.commit()
            session.close()
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return
def updateCharacter(character):
    try:
        session = Session()
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name and CharacterDB.realm == character.realm).first()
        if existing_character != None:
            existing_character.discord_user_id = character.discord_user_id
            existing_character.name = character.name
            existing_character.realm = character.realm
            existing_character.faction = character.faction
            existing_character.region = character.region
            existing_character.role = character.role
            existing_character.spec_name = character.spec_name
            existing_character.class_name = character.class_name
            existing_character.achievement_points = character.achievement_points
            existing_character.item_level = character.item_level
            existing_character.score = character.score
            existing_character.rank = character.rank
            existing_character.thumbnail_url = character.thumbnail_url
            existing_character.url = character.url
            existing_character.last_crawled_at = character.last_crawled_at
            existing_character.is_reporting = character.is_reporting
            existing_character.dungeon_runs = character.dungeon_runs
            
            session.commit()
            session.close()
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return
def updateCharacterReporting(character):
    try:
        session = Session()
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name and CharacterDB.realm == character.realm).first()
        if existing_character != None:
            if existing_character.is_reporting == True:
                existing_character.is_reporting = False
            else:
                existing_character.is_reporting = True
            
            session.commit()
            session.close()
            return True
    except Exception as e:
        print(e)
        return
def removeCharacter(name, realm):
    session = Session()
    existing_character = session.query(CharacterDB).filter(CharacterDB.name == name and CharacterDB.realm == realm).first()
    if existing_character != None:
        session.delete(existing_character)
        session.commit()
        session.close()
        return True
    else:
        return False
def addDungeonRun(character, run):
    try: 
        session = Session()
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name and CharacterDB.realm == character.realm).first()
        if existing_character != None:
            dungeon_Run = DungeonRunDB(run.id, run.season, run.name, run.short_name, run.mythic_level, run.completed_at, run.clear_time_ms, run.par_time_ms, run.num_keystone_upgrades, run.score, run.url, existing_character)
            session.add(dungeon_Run)
            session.commit()
            session.close()
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return None
def getAllCharacters():
    try:
        session = Session()
        characters = session.query(CharacterDB).all()
        session.close()
        return characters
    except Exception as e:
        print(e)
        return None

            