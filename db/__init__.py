##---------------Take a Lap Discord Bot-----------------
#Description: This file is used to create the database and tables for the bot. It is also used to query the database for information.
#Author: Eriim\
    
import logging
from datetime import datetime
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base

from db.character_db import CharacterDB
from db.dungeon_run_db import DungeonRunDB
from db.default_character_db import DefaultCharacterDB
from db.character_run_db import CharacterRunDB
from raiderIO.character import Character
from raiderIO.dungeonRun import DungeonRun

logging.basicConfig(filename='tal.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

engine = create_engine('sqlite:///tal.db', echo=True,
                       logging_name='sqlalchemy.engine',
                       echo_pool=True, pool_pre_ping=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def lookup_character(name: str, realm: str) -> Optional[CharacterDB]:
    """Look up a specific character in the database.

    Args:
        name (string): The name of the character to look up.
        realm (string): The realm of the character to look up.

    Returns:
        existing_character: returns a character object if found, otherwise returns None.
    """
    print('DB: looking up character: ' + name + ' on realm: ' + realm)
    session = Session()
    try:
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == name, CharacterDB.realm == realm).first()
        if existing_character is None:
            print('DB: character not found: ' + name + ' on realm: ' + realm)
        elif existing_character is not None:
            print('DB: found character: ' + existing_character.name + ' on realm: ' + existing_character.realm)
            return existing_character
        else:
            return None
    except Exception as exception:
        print(exception)
        session.rollback()
        return None
    finally:
        session.close()
def lookup_run(run_id: int) -> Optional[DungeonRunDB]:
    """Look up a specific run in the database.

    Args:
        run_id (integer): The run id to look up.

    Returns:
        existing_run: returns a run object if found, otherwise returns None.
    """
    session = Session()
    try:
        existing_run = session.query(DungeonRunDB).filter(DungeonRunDB.id == run_id).first()
        if existing_run is not None:
            return existing_run
        else:
            return None
    except Exception as exception:
        print(exception)
        session.rollback()
        return None
    finally:
        session.close()
def add_character(character: CharacterDB) -> bool:
    """Add a character to the database.

    Args:
        character (Character): The Character.py object to add to the database.

    Returns:
        bool: Returns True if the character was added to the database, otherwise returns False.
    """
    session = Session()
    try:
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm).first()
        if existing_character.realm.capitalize() != character.realm.capitalize() or existing_character.name.capitalize() != character.name.capitalize():
            character_db = CharacterDB(
                character.discord_user_id,
                character.discord_guild_id,
                character.guild_name,
                character.name,
                character.realm,
                character.faction,
                character.region,
                character.role,
                character.spec_name,
                character.class_name,
                character.achievement_points,
                character.item_level,
                character.score,
                character.rank,
                character.thumbnail_url,
                character.url,
                character.last_crawled_at,
                character.is_reporting,
                character.dungeon_runs)
            session.add(character_db)
            session.commit()            
            return True
        else:            
            return False
    except Exception as exception:
        print(exception)
        session.rollback()
        return
    finally:
        session.close()
def update_character(character: Character) -> bool:
    """Update an existing character in the database.

    Args:
        character (Character): The Character.py object to update in the database.

    Returns:
        bool: Returns True if the character was updated in the database, otherwise returns False.
    """
    session = Session()
    try:
                
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm).first()
        
        if existing_character is not None:
            existing_character.discord_user_id = character.discord_user_id
            existing_character.discord_guild_id = character.discord_guild_id
            existing_character.guild_name = character.guild_name
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
            
            session.commit()
            return True
        else:
            return False
    except Exception as exception:
        session.rollback()
        print(exception)
        return
    finally:
        session.close()
def update_character_reporting(character: Character) -> bool:
    """Update the reporting status of an existing character in the database.

    Args:
        character (Character): The Character.py object to update in the database.

    Returns:
        Bool: Returns True if the character was updated in the database, otherwise returns False.
    """
    session = Session()
    try:
        
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm).first()
        if existing_character is not None:
            if existing_character.is_reporting is True:
                existing_character.is_reporting = False
            else:
                existing_character.is_reporting = True
            session.commit()
            return True
        else:
            return False
    except Exception as exception:
        print(exception)
        return
    finally:
        session.close()
def set_guild_run(run: DungeonRun) -> bool:
    """Set a run as a guild run.

    Args:
        run (DungeonRun): The DungeonRun.py object to update in the database.

    Returns:
        Bool: Returns True if the run was updated in the database, otherwise returns False.
    """
    session = Session()
    try:        
        existing_run = session.query(DungeonRunDB).filter(DungeonRunDB.id == run.id).first()
        if existing_run is not None:
            existing_run.is_guild_run = True
            session.commit()
            return True
        else:
            return False
    except Exception as exception:
        session.rollback()
        print(exception)
        return
    finally:
        session.close()
def remove_character(name, realm) -> bool:
    """Remove a character from the database.

    Args:
        name (string): The name of the character to remove.
        realm (string): The realm of the character to remove.

    Returns:
        bool: Returns True if the character was removed from the database, otherwise returns False.
    """
    session = Session()
    try:
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == name, CharacterDB.realm == realm).first()
        if existing_character is not None:
            session.delete(existing_character)
            session.commit()
            return True
        else:            
            return False
    except Exception as exception:
        session.rollback()
        print(exception)
        return None
    finally:
        session.close()
def add_dungeon_run(dungeon_run: DungeonRun) -> bool:
    """Add a dungeon run to the database.

    Args:
        character (characterDB): The CharacterDB.py object for the character that completed the dungeon run.
        run (DungeonRun): The DungeonRun.py object to add to the database.

    Returns:
        bool: Returns True if the dungeon run was added to the database, otherwise returns False.
    """
    session = Session()
    try:
        existing_dungeon_run = session.query(DungeonRunDB).filter(DungeonRunDB.id == dungeon_run.id).first()
        if existing_dungeon_run is None:
            print('Run already exists in the database.')
            dungeon_run = DungeonRunDB(dungeon_run.id,
                                    dungeon_run.season,
                                    dungeon_run.name,
                                    dungeon_run.short_name,
                                    dungeon_run.mythic_level,
                                    dungeon_run.completed_at,
                                    dungeon_run.clear_time_ms,
                                    dungeon_run.par_time_ms,
                                    dungeon_run.num_keystone_upgrades,
                                    dungeon_run.score,
                                    dungeon_run.url)
            session.add(dungeon_run)
            session.commit()
            return True
        elif existing_dungeon_run.id == dungeon_run.id:
            print('Run already exists in the database.')
            return False
        else:
            print('Something went wrong.')
            return False
        
    except Exception as exception:
        session.rollback()
        print(exception)
        return None
    finally:
        session.close()
def update_dungeon_run(dungeon_run : DungeonRunDB) -> bool:
    """Update an existing dungeon run.

    Args:
        dungeon_run (DungeonRunDB): _description_
    """
    session = Session()
    try: 
        existing_dungeon_run = session.query(DungeonRunDB).filter(DungeonRunDB.id == dungeon_run.id).first()
        if existing_dungeon_run is not None:
            existing_dungeon_run.is_guild_run = dungeon_run.is_guild_run
            existing_dungeon_run.is_crawled = True
            session.commit() 
            return True
        else:
            return False          
    except Exception as exception:
        print(exception)
        session.rollback()
    finally: 
        session.close()
        
def get_all_characters() -> List[CharacterDB]:
    """Get all of the characters from the database.

    Returns:
        characters_list: a list of all of the characters in the database.
    """
    session = Session()
    try:        
        characters_list = session.query(CharacterDB).all()
        return characters_list
    except Exception as exception:
        print(exception)
        session.rollback()
        return None
    finally:
        session.close()
def get_all_runs() -> List[DungeonRunDB]:
    """Get all of the runs from the database.

    Returns:
        runs_list: A list of all of the runs in the database.
    """
    session = Session()
    try:
        runs_list = session.query(DungeonRunDB).all()
        return runs_list
    except Exception as exception:
        session.rollback()
        print(exception)
        return None
    finally:
        session.close()
def add_default_character(default_character: DefaultCharacterDB) -> bool:
    """Add a default character to the database.

    Returns:
        bool: Returns True if the character was added to the database, otherwise returns False.
    """
    session = Session()
    try:
        existing_relationship = session.query(DefaultCharacterDB).filter(DefaultCharacterDB.discord_guild_id == default_character.discord_guild_id, DefaultCharacterDB.discord_user_id == default_character.discord_user_id).first()
        if existing_relationship is None:
            session.add(default_character)
            session.commit()
            return True
        else:
            return False
    except Exception as exception:
        print(exception)
        session.rollback()
        return None
    finally:       
        session.close()
def remove_default_character(default_character: DefaultCharacterDB) -> bool:
    """Remove a default character from the database.

    Returns:
        bool: Returns True if the character was removed from the database, otherwise returns False.
    """
    session = Session()
    try:
        existing_relationship = session.query(DefaultCharacterDB).filter(DefaultCharacterDB.discord_guild_id == default_character.discord_guild_id, DefaultCharacterDB.discord_user_id == default_character.discord_user_id).first()
        if existing_relationship is not None:
            
            session.delete(existing_relationship)
            session.commit()
            return True
        else:
            return False
    except Exception as exception:
        print(exception)
        session.rollback()
        return None
    finally:
        session.close()
def lookup_default_character(discord_guild_id, discord_user_id) -> Character:
    """Lookup a default character from the database.

    Returns:
        DefaultCharacterDB: Returns a DefaultCharacterDB.py object if the relationship exists, otherwise returns None.
    """
    session = Session()
    try:
        default_character = session.query(DefaultCharacterDB).filter(DefaultCharacterDB.discord_guild_id == discord_guild_id, DefaultCharacterDB.discord_user_id == discord_user_id).first()
        if default_character is not None:
            character = session.query(CharacterDB).filter(CharacterDB.id == default_character.character.id).first()
            return character
        elif default_character is None:
            return None
    except Exception as exception:
        print(exception)
        session.rollback()
        return None
    finally:
        session.close()
def get_top10_character_by_achievement() -> List[CharacterDB]:
    """Get the top 10 characters by achievement points.

    Returns:
        List[CharacterDB]: Returns a list of the top 10 characters by achievement points.
    """
    session = Session()
    try:
        top10_characters = session.query(CharacterDB).order_by(CharacterDB.achievement_points.desc()).limit(10).all()
        return top10_characters
    except Exception as exception:
        print(exception)
        session.rollback()
        return None
    finally:
        session.close()
def get_top10_character_by_mythic_plus() -> List[CharacterDB]:
    """Get the top 10 characters by mythic plus score.

    Returns:
        List[CharacterDB]: Returns a list of the top 10 characters by mythic plus score.
    """
    session = Session()
    try:
        top10_characters = session.query(CharacterDB).order_by(CharacterDB.score.desc()).limit(10).all()
        return top10_characters
    except Exception as exception:
        print(exception)
        session.rollback()
        return None
    finally:
        session.close()
def get_top10_character_by_highest_item_level() -> List[CharacterDB]:
    """Get the top 10 characters by highest item level.

    Returns:
        List[CharacterDB]: Returns a list of the top 10 characters by highest item level.
    """
    session = Session()
    try:
        top10_characters = session.query(CharacterDB).order_by(CharacterDB.item_level.desc()).limit(10).all()
        return top10_characters
    except Exception as exception:
        print(exception)
        session.rollback()
        return None
    finally:
        session.close()
def add_character_run(character: CharacterDB, run_id: int) -> bool:
    """Add a character run to the database.

    Args:
        character (CharacterDB): The CharacterDB.py object to add to the database.
        run (DungeonRunDB): The DungeonRunDB.py object to add to the database.

    Returns:
        bool: Returns True if the character run was added to the database, otherwise returns False.
    """
    session = Session()
    try:
        print('Trying to add character run')
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm).first()
        existing_run = session.query(DungeonRunDB).filter(DungeonRunDB.id == run_id).first()
        if existing_character is None:
            print('------------------------------No character found-----------------------------')
            return False
        elif existing_run is None:
            print('------------------------------No run found-----------------------------')
            return False
        else:
            existing_character_run = session.query(CharacterRunDB).filter(CharacterRunDB.character_id == existing_character.id, CharacterRunDB.dungeon_run_id == existing_run.id).first()
            if existing_character_run is not None:
                print(f'------------------------------Character run already exists for {existing_character_run.dungeon_run.name} {existing_character_run.character.name}-----------------------------')
                print(existing_character_run)
                return False
            elif existing_character_run is None:
                new_character_run = CharacterRunDB(existing_character,
                                                existing_run,
                                                datetime.now(),
                                                datetime.now())
                print('Adding character run')
                session.add(new_character_run)                
                session.commit()
                return True
    except Exception as exception:
        session.rollback()
        print(exception)
        return None
    finally:
        session.close()
def lookup_character_run(character: CharacterDB, run: DungeonRunDB) -> CharacterRunDB:
    """Lookup a character run from the database.

    Args:
        character (CharacterDB): The CharacterDB.py object to lookup in the database.
        run (DungeonRunDB): The DungeonRunDB.py object to lookup in the database.

    Returns:
        CharacterRunDB: Returns a CharacterRunDB.py object if the character run exists, otherwise returns None.
    """
    session = Session()
    try:
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm).first()
        existing_run = session.query(DungeonRunDB).filter(DungeonRunDB.id == run.id).first()
        if existing_character is None:
            return None
        elif existing_run is None:
            return None
        else:
            existing_character_run = session.query(CharacterRunDB).filter(CharacterRunDB.character_id == existing_character.id, CharacterRunDB.run_id == existing_run.id).one()
            if existing_character_run is not None:
                return existing_character_run
            else:
                return None
    except Exception as exception:
        session.rollback()
        print(exception)
        return None
    finally:
        session.close()
        