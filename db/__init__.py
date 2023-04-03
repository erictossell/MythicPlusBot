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
def addCharacter(character):
    session = Session()
    existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name and CharacterDB.realm == character.realm).first()
    if existing_character == None:
        characterDB = CharacterDB(character.discord_user_id, character.name, character.realm, character.faction, character.region, character.role, character.spec_name, character.class_name, character.achievement_points, character.item_level, character.score, character.rank, character.thumbnail_url, character.url, character.last_crawled_at, character.active, character.raid_progression)
        session.add(characterDB)
        session.commit()
        session.close()
        return True
    else:
        return False
def updateCharacter(character):
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
        existing_character.active = character.active
        existing_character.raid_progression = character.raid_progression
        session.commit()
        session.close()
        return True
    else:
        return False
    
                
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
    
def addDungeonRun(character, dungeon_run):
    session = Session()
    existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name and CharacterDB.realm == character.realm).first()
    if existing_character != None:
        dungeon_Run = DungeonRunDB(dungeon_run.season, dungeon_run.dungeon, dungeon_run.level, dungeon_run.num_keystone_upgrades, dungeon_run.final_level, dungeon_run.num_chests, dungeon_run.num_affixes, dungeon_run.time, dungeon_run.completed_at, dungeon_run.url, dungeon_run.mythic_plus_highest_level_runs, dungeon_run.mythic_plus_recent_runs, dungeon_run.mythic_plus_best_runs)
        session.commit(dungeon_Run)
        session.close()
        return True
    else:
        return False