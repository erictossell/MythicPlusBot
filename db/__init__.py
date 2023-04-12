##---------------Take a Lap Discord Bot-----------------
#Description: This file is used to create the database and tables for the bot. It is also used to query the database for information.
#Author: Eriim\
    
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base

from db.character_db import CharacterDB
from db.dungeon_run_db import DungeonRunDB
from db.default_character_db import DefaultCharacterDB
from raiderIO.character import Character
from raiderIO.dungeonRun import DungeonRun


engine = create_engine('sqlite:///tal.db', echo=True)
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
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == name and CharacterDB.realm == realm).first()
        if existing_character is None:
            print('DB: character not found: ' + name + ' on realm: ' + realm)
        elif str(existing_character.realm).capitalize() == str(realm).capitalize() and str(existing_character.name).capitalize() == str(name).capitalize():
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
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name and CharacterDB.realm == character.realm).first()
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
                
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name and CharacterDB.realm == character.realm).first()
        
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
        
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name and CharacterDB.realm == character.realm).first()
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
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == name and CharacterDB.realm == realm).first()
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
def add_dungeon_run(character: Character, run: DungeonRun) -> bool:
    """Add a dungeon run to the database.

    Args:
        character (characterDB): The CharacterDB.py object for the character that completed the dungeon run.
        run (DungeonRun): The DungeonRun.py object to add to the database.

    Returns:
        bool: Returns True if the dungeon run was added to the database, otherwise returns False.
    """
    session = Session()
    try:
        existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name and CharacterDB.realm == character.realm).first()
        if existing_character is not None:
            dungeon_run = DungeonRunDB(run.id,
                                       run.season,
                                       run.name,
                                       run.short_name,
                                       run.mythic_level,
                                       run.completed_at,
                                       run.clear_time_ms,
                                       run.par_time_ms,
                                       run.num_keystone_upgrades,
                                       run.score,
                                       run.url,
                                       existing_character)
            session.add(dungeon_run)
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
        existing_relationship = session.query(DefaultCharacterDB).filter((DefaultCharacterDB.discord_guild_id == default_character.discord_guild_id) and (DefaultCharacterDB.discord_user_id == default_character.discord_user_id)).first()
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
        existing_relationship = session.query(DefaultCharacterDB).filter((DefaultCharacterDB.discord_guild_id == default_character.discord_guild_id) and (DefaultCharacterDB.discord_user_id == default_character.discord_user_id)).first()
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
        default_character = session.query(DefaultCharacterDB).filter(DefaultCharacterDB.discord_guild_id == discord_guild_id and DefaultCharacterDB.discord_user_id == discord_user_id).first()
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