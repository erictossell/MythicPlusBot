##---------------Take a Lap Discord Bot-----------------
#Description: This file is used to create the database and tables for the bot. It is also used to query the database for information.
#Author: Eriim\
from contextlib import contextmanager
import logging
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, joinedload
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

engine = create_engine('sqlite:///tal.db', echo=False,
                       logging_name='sqlalchemy.engine',
                       echo_pool=True, pool_pre_ping=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        
def lookup_character(name: str, realm: str) -> Optional[CharacterDB]:
    """Look up a specific character in the database.

    Args:
        name (string): The name of the character to look up.
        realm (string): The realm of the character to look up.

    Returns:
        existing_character: returns a character object if found, otherwise returns None.
    """
    print(f'Tal_DB : looking up character: {name} on realm: {realm}')
    try:
        with session_scope() as session:
            existing_character = session.query(CharacterDB).options(joinedload('*')).filter(CharacterDB.name == name, CharacterDB.realm == realm.lower()).first()
            
            if existing_character is None:
                print(f'Tal_DB : character not found: {name} on realm: {realm}')
            else:
                print(f'Tal_DB : found character: {existing_character.name} on realm: {existing_character.realm}')
                existing_character = CharacterDB(existing_character.discord_user_id,
                                             existing_character.discord_guild_id,
                                             existing_character.guild_name,
                                             existing_character.name,
                                             existing_character.realm,
                                             existing_character.faction,
                                             existing_character.region,
                                             existing_character.role,
                                             existing_character.spec_name,
                                             existing_character.class_name,
                                             existing_character.achievement_points,
                                             existing_character.item_level,
                                             existing_character.score,
                                             existing_character.rank,
                                             existing_character.thumbnail_url,
                                             existing_character.url,
                                             existing_character.last_crawled_at,
                                             existing_character.is_reporting)

        return existing_character
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None
def lookup_run(run_id: int) -> Optional[DungeonRunDB]:
    """Look up a specific run in the database.

    Args:
        run_id (integer): The run id to look up.

    Returns:
        existing_run: returns a run object if found, otherwise returns None.
    """
    print(f'DB: looking up run: {run_id}')
    try:
        with session_scope() as session:
            existing_run = session.query(DungeonRunDB).options(joinedload('*')).filter(DungeonRunDB.id == run_id).first()

            if existing_run is None:
                print(f'Tal_DB : run not found: {run_id}')
            else:
                print(f'Tal_DB : found run: {existing_run.id}')
        return existing_run
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None  
def lookup_character_run(character: CharacterDB, run: DungeonRunDB) -> CharacterRunDB:
    """Lookup a character run from the database.

    Args:
        character (CharacterDB): The CharacterDB.py object to lookup in the database.
        run (DungeonRunDB): The DungeonRunDB.py object to lookup in the database.

    Returns:
        CharacterRunDB: Returns a CharacterRunDB.py object if the character run exists, otherwise returns None.
    """
    print(f'Tal_DB : looking up character run: {character.name} for run: {run.name}')
    try:
        with session_scope() as session:
            existing_character = session.query(CharacterDB).options(joinedload('*')).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm).first()
            existing_run = session.query(DungeonRunDB).options(joinedload('*')).filter(DungeonRunDB.id == run.id).first()
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
    except SQLAlchemyError as error:
        print(error)
        return None
def lookup_default_character(discord_guild_id, discord_user_id) -> DefaultCharacterDB:
    """Lookup a default character from the database.

    Returns:
        DefaultCharacterDB: Returns a DefaultCharacterDB.py object if the relationship exists, otherwise returns None.
    """
    session = Session()
    try:
        default_character = session.query(DefaultCharacterDB).filter(DefaultCharacterDB.discord_guild_id == discord_guild_id, DefaultCharacterDB.discord_user_id == discord_user_id).first()
        if default_character is not None:   
            default_character = DefaultCharacterDB(default_character.discord_user_id,
                                                   default_character.discord_guild_id,
                                                   default_character.character,
                                                   default_character.version,
                                                   default_character.is_default_character)
            return default_character
        elif default_character is None:
            return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 
    
def add_character(character: CharacterDB) -> CharacterDB:
    """Add a character to the database.

    Args:
        character (Character): The Character.py object to add to the database.

    Returns:
        bool: Returns True if the character was added to the database, otherwise returns False.
    """
    print('Tal_DB : adding character: ' + character.name + ' on realm: ' + character.realm)
    try:
        with session_scope() as session:
            existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm.lower()).first()
            if existing_character is None:
                character_db = CharacterDB(
                    character.discord_user_id,
                    character.discord_guild_id,
                    character.guild_name,
                    character.name,
                    character.realm.lower(),
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
                    character.is_reporting)
                session.add(character_db)
                print('Tal_DB : added character: ' + character.name + ' on realm: ' + character.realm)
                return character_db
            else:
                print('Tal_DB : character already exists: ' + character.name + ' on realm: ' + character.realm)
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None
def add_dungeon_run(dungeon_run: DungeonRun) -> bool:
    """Add a dungeon run to the database.

    Args:
        character (characterDB): The CharacterDB.py object for the character that completed the dungeon run.
        run (DungeonRun): The DungeonRun.py object to add to the database.

    Returns:
        bool: Returns True if the dungeon run was added to the database, otherwise returns False.
    """
    print(f'Tal_DB : adding dungeon run: {dungeon_run.id}')
    try:
        with session_scope() as session:
            existing_dungeon_run = session.query(DungeonRunDB).filter(DungeonRunDB.id == dungeon_run.id).first()
            if existing_dungeon_run is None:
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
                return True
            elif existing_dungeon_run.id == dungeon_run.id:
                print('Run already exists in the database.')
                return False
            else:
                print('Something went wrong.')
                return False
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False
def add_character_run(character: CharacterDB, run: int) -> Optional[CharacterDB]:
    """Add a character run to the database.

    Args:
        character (CharacterDB): The CharacterDB object to add to the database.
        run (DungeonRunDB): The DungeonRunDB object to add to the database.

    Returns:
        Optional[CharacterDB]: Returns the CharacterDB object if the character run was added to the database, otherwise returns None.
    """
    try:
        with session_scope() as session:
            existing_character = session.query(CharacterDB).filter(
                CharacterDB.name == character.name, CharacterDB.realm == character.realm).first()
            existing_run = session.query(DungeonRunDB).filter(DungeonRunDB.id == run).first()

            if existing_character is None or existing_run is None:
                return None

            existing_character_run = session.query(CharacterRunDB).filter(
                CharacterRunDB.character_id == existing_character.id,
                CharacterRunDB.dungeon_run_id == existing_run.id).first()

            if existing_character_run is not None:
                return None

            new_character_run = CharacterRunDB(existing_character,
                                               existing_run
)
            session.add(new_character_run)

            return new_character_run
    except SQLAlchemyError as error:
        print(error)
        return None
def add_default_character(default_character: DefaultCharacterDB) -> bool:
    """Add a default character to the database.

    Returns:
        bool: Returns True if the character was added to the database, otherwise returns False.
    """
    print(f'Tal_DB : adding default character: {default_character.discord_user_id} for guild: {default_character.discord_guild_id}')
    try:
        with session_scope() as session:
            existing_relationship = session.query(DefaultCharacterDB).filter(DefaultCharacterDB.discord_guild_id == default_character.discord_guild_id,
                                                                             DefaultCharacterDB.discord_user_id == default_character.discord_user_id).first()
            if existing_relationship is None:
                session.add(default_character)
                return True
            else:
                return False
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False 
    
def update_character(character: Character) -> CharacterDB:
    """Update an existing character in the database.

    Args:
        character (Character): The Character.py object to update in the database.

    Returns:
        bool: Returns True if the character was updated in the database, otherwise returns False.
    """
    print('Tal_DB : updating character: ' + character.name + ' on realm: ' + character.realm)
    try:
        with session_scope() as session:
            existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name,
                                                                   CharacterDB.realm == character.realm.lower()).first()
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
                print('Tal_DB : updated character: ' + character.name + ' on realm: ' + character.realm)
                return existing_character
            else:
                print('Tal_DB : character not found: ' + character.name + ' on realm: ' + character.realm)
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None
def update_character_reporting(character: Character) -> bool:
    """Update the reporting status of an existing character in the database.

    Args:
        character (Character): The Character.py object to update in the database.

    Returns:
        Bool: Returns True if the character was updated in the database, otherwise returns False.
    """
    
    print(f'Tal_DB : updating character reporting status: {character.name} on realm: {character.realm}')
    try:
        with session_scope() as session:
            existing_character = session.query(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm.lower()).first()
            if existing_character is not None:
                if existing_character.is_reporting is True:
                    existing_character.is_reporting = False
                else:
                    existing_character.is_reporting = True
                print('Tal_DB : updated character reporting status: ' + character.name + ' on realm: ' + character.realm)
                return True
            else:
                print('Tal_DB : character not found: ' + character.name + ' on realm: ' + character.realm)
                return False
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False
def update_dungeon_run(dungeon_run : DungeonRunDB) -> bool:
    """Update an existing dungeon run.

    Args:
        dungeon_run (DungeonRunDB): _description_
    """
    print(f'Tal_DB : updating dungeon run: {dungeon_run.id}')
    try:
        with session_scope() as session:                
            existing_dungeon_run = session.query(DungeonRunDB).filter(DungeonRunDB.id == dungeon_run.id).first()
            if existing_dungeon_run is not None:
                existing_dungeon_run.is_guild_run = dungeon_run.is_guild_run
                existing_dungeon_run.is_crawled = True
                return True
            else:
                return False          
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False  
def update_default_character(discord_user_id:int, discord_guild_id:int, character: CharacterDB) -> DefaultCharacterDB:
    """Update a default character in the database or create a new one if not exists.

    Args:
        default_character (DefaultCharacterDB): _description_

    Returns:
        Tuple[DefaultCharacterDB, bool]: Returns a tuple with the updated or created default character and a boolean indicating if the default character was updated (True) or created (False).
    """
    print('Tal_DB : updating default character')
    
    try: 
        with session_scope() as session:
            existing_relationship = session.query(DefaultCharacterDB).filter(DefaultCharacterDB.discord_guild_id == discord_guild_id,
                                                                             DefaultCharacterDB.discord_user_id == discord_user_id).first()
            new_character = session.query(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm.lower()).first()
            if new_character is None:
                print('Tal_DB : Character not found in the database.')
                return None
            if existing_relationship is not None:
                print('Tal_DB : Main character updated')
                existing_relationship.character_id = new_character.id
                existing_relationship.version += 1
                character_name = new_character.name
                character_realm = new_character.realm
                return existing_relationship, character_name, character_realm
            else:
                print('Tal_DB : Main character created')
                default_character = DefaultCharacterDB(discord_user_id, discord_guild_id, character.id)
                session.add(default_character)
                character_name = new_character.name
                character_realm = new_character.realm
                return default_character, character_name, character_realm

    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None, False
    
def set_guild_run(run: DungeonRun) -> bool:
    """Set a run as a guild run.

    Args:
        run (DungeonRun): The DungeonRun.py object to update in the database.

    Returns:
        Bool: Returns True if the run was updated in the database, otherwise returns False.
    """
    
    try:
        with session_scope() as session:        
            existing_run = session.query(DungeonRunDB).filter(DungeonRunDB.id == run.id).first()
            if existing_run is not None:
                existing_run.is_guild_run = True
                print('Tal_DB : set run as guild run: ' + str(run.id))
                return True
            else:
                print('Tal_DB : run not found: ' + str(run.id))
                return False
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False
    
def remove_character(name, realm) -> bool:
    """Remove a character from the database.

    Args:
        name (string): The name of the character to remove.
        realm (string): The realm of the character to remove.

    Returns:
        bool: Returns True if the character was removed from the database, otherwise returns False.
    """
    print(f'Tal_DB : removing character: {name} on realm: {realm}')
    try:
        with session_scope() as session:
            existing_character = session.query(CharacterDB).filter(CharacterDB.name == name, CharacterDB.realm == realm).first()
            if existing_character is not None:
                session.delete(existing_character)
                return True
            else:            
                return False
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False
def remove_default_character(default_character: DefaultCharacterDB) -> bool:
    """Remove a default character from the database.

    Returns:
        bool: Returns True if the character was removed from the database, otherwise returns False.
    """
    print(f'Tal_DB : removing default character: {default_character.discord_user_id} for guild: {default_character.discord_guild_id}')
    try:
        with session_scope() as session:
            existing_relationship = session.query(DefaultCharacterDB).filter(DefaultCharacterDB.discord_guild_id == default_character.discord_guild_id,
                                                                             DefaultCharacterDB.discord_user_id == default_character.discord_user_id).first()
            if existing_relationship is not None:
                session.delete(existing_relationship)
                return True
            else:
                return False
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False 
   
def get_all_characters() -> List[CharacterDB]:
    """Get all of the characters from the database.

    Returns:
        characters_list: a list of all of the characters in the database.
    """
    print ('Tal_DB : getting all characters')
    try:
        with session_scope() as session:
            characters_query = session.query(CharacterDB).options(joinedload('*')).all()
            characters_list = [CharacterDB(character.discord_user_id,
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
                                           character.is_reporting) for character in characters_query]
            return characters_list
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 
def get_all_runs() -> List[DungeonRunDB]:
    """Get all of the runs from the database.

    Returns:
        runs_list: A list of all of the runs in the database.
    """
    print(f'Tal_DB : getting all runs')
    try:
        with session_scope() as session:
            runs_query = session.query(DungeonRunDB).options(joinedload('*')).all()
            runs_list = [DungeonRunDB(run.id,
                                      run.season,
                                      run.name,
                                      run.short_name,
                                      run.mythic_level,
                                      run.completed_at,
                                      run.clear_time_ms,
                                      run.par_time_ms,
                                      run.num_keystone_upgrades,
                                      run.score,
                                      run.url) for run in runs_query]
            return runs_list
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 
def get_all_characters_for_run(run_id: int) -> List[CharacterRunDB]:
    """Get all characters for a run.

    Args:
        run (DungeonRunDB): The DungeonRunDB.py object to lookup in the database.

    Returns:
        List[CharacterRunDB]: Returns a list of CharacterRunDB.py objects if the character run exists, otherwise returns None.
    """
    print(f'Getting all characters for run {run_id}')
    try:
        with session_scope() as session:
            existing_run = session.query(DungeonRunDB).options(joinedload('*')).filter(DungeonRunDB.id == run_id).first()
            if existing_run is None:
                print(f'No run found for id {run_id}')
                return None
            else:
                existing_character_runs = session.query(CharacterRunDB).filter(CharacterRunDB.dungeon_run_id == existing_run.id).all()
                existing_characters = session.query(CharacterDB).filter(CharacterDB.id.in_([char.character_id for char in existing_character_runs])).all()
                character_list = [CharacterDB(char.discord_user_id,
                                                char.discord_guild_id,
                                                char.guild_name,
                                                char.name,
                                                char.realm,
                                                char.faction,
                                                char.region,
                                                char.role,                                                
                                                char.spec_name,
                                                char.class_name,
                                                char.achievement_points,
                                                char.item_level,
                                                char.score,
                                                char.rank,
                                                char.thumbnail_url,
                                                char.url,
                                                char.last_crawled_at,
                                                char.is_reporting) for char in existing_characters]
                print(f'Found {len(character_list)} characters for run {run_id}')
                return character_list
                
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 
def get_all_runs_for_character(character: CharacterDB) -> List[CharacterRunDB]:
    """Get all runs for a character.

    Args:
        character (CharacterDB): The CharacterDB.py object to lookup in the database.

    Returns:
        List[CharacterRunDB]: Returns a list of CharacterRunDB.py objects if the character run exists, otherwise returns None.
    """
    print(f'Getting all runs for character {character.name} {character.realm}')
    try:
        with session_scope() as session:
            existing_character = session.query(CharacterDB).options(joinedload('*')).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm).first()
            if existing_character is None:
                print (f'No character found for {character.name} {character.realm}')
                return None
            else:
                existing_character_runs = session.query(CharacterRunDB)\
                                        .join(DungeonRunDB, CharacterRunDB.dungeon_run_id == DungeonRunDB.id)\
                                        .options(joinedload('*'))\
                                        .filter(CharacterRunDB.character_id == existing_character.id)\
                                        .order_by(DungeonRunDB.score.desc())\
                                        .limit(15)\
                                        .all()
                print(f'Existing character runs (before filtering): {len(existing_character_runs)}')
                if existing_character_runs is not None:
                    run_list = []
                    for character_run in existing_character_runs:
                        run = session.query(DungeonRunDB).options(joinedload('*')).filter(DungeonRunDB.id == character_run.dungeon_run_id).first()
                        run = DungeonRunDB(run.id,
                                       run.season,
                                       run.name,
                                       run.short_name,
                                       run.mythic_level,
                                       run.completed_at,
                                       run.clear_time_ms,
                                       run.par_time_ms,
                                       run.num_keystone_upgrades,
                                       run.score,
                                       run.url)
                        run_list.append(run)
                    print(f'Found {len(run_list)} runs for character {character.name} {character.realm}')
                    return run_list
                else:
                    print(f'No runs found for character {character.name} {character.realm}')
                    return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 

def get_top10_character_by_achievement() -> List[CharacterDB]:
    """Get the top 10 characters by achievement points.

    Returns:
        List[CharacterDB]: Returns a list of the top 10 characters by achievement points.
    """
    print('Tal_DB : getting top 10 characters by achievement points')
    try:
        with session_scope() as session:
            query = session.query(CharacterDB).options(joinedload('*')).order_by(CharacterDB.achievement_points.desc()).limit(10).all()
            top10_characters = [CharacterDB(char.discord_user_id,
                                            char.discord_guild_id,
                                            char.guild_name,
                                            char.name,
                                            char.realm,
                                            char.faction,
                                            char.region,
                                            char.role,
                                            char.spec_name,
                                            char.class_name,
                                            char.achievement_points,
                                            char.item_level,
                                            char.score,
                                            char.rank,
                                            char.thumbnail_url,
                                            char.url,
                                            char.last_crawled_at,
                                            char.is_reporting) for char in query]
            return top10_characters
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 
def get_top10_character_by_mythic_plus() -> List[CharacterDB]:
    """Get the top 10 characters by mythic plus score.

    Returns:
        List[CharacterDB]: Returns a list of the top 10 characters by mythic plus score.
    """
    print('Tal_DB : getting top 10 characters by mythic plus score')
    try:
        with session_scope() as session:
            query = session.query(CharacterDB).options(joinedload('*')).order_by(CharacterDB.score.desc()).limit(10).all()
            top10_characters = [CharacterDB(char.discord_user_id,
                                            char.discord_guild_id,
                                            char.guild_name,
                                            char.name,
                                            char.realm,
                                            char.faction,
                                            char.region,
                                            char.role,
                                            char.spec_name,
                                            char.class_name,
                                            char.achievement_points,
                                            char.item_level,
                                            char.score,
                                            char.rank,
                                            char.thumbnail_url,
                                            char.url,
                                            char.last_crawled_at,
                                            char.is_reporting) for char in query]
            return top10_characters
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 
def get_top10_character_by_highest_item_level() -> List[CharacterDB]:
    """Get the top 10 characters by highest item level.

    Returns:
        List[CharacterDB]: Returns a list of the top 10 characters by highest item level.
    """
    print('Tal_DB : getting top 10 characters by highest item level')
    try:
        with session_scope() as session:
            query = session.query(CharacterDB).options(joinedload('*')).order_by(CharacterDB.item_level.desc()).limit(10).all()
            top10_characters = [CharacterDB(char.discord_user_id,
                                            char.discord_guild_id,
                                            char.guild_name,
                                            char.name,
                                            char.realm,
                                            char.faction,
                                            char.region,
                                            char.role,
                                            char.spec_name,
                                            char.class_name,
                                            char.achievement_points,
                                            char.item_level,
                                            char.score,
                                            char.rank,
                                            char.thumbnail_url,
                                            char.url,
                                            char.last_crawled_at,
                                            char.is_reporting) for char in query]
            return top10_characters
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 
def get_top10_guild_runs() -> List[DungeonRunDB]:
    print('Tal_DB : getting top 10 guild runs')
    try: 
        with session_scope() as session:
            query = session.query(DungeonRunDB).options(joinedload('*')).filter(DungeonRunDB.is_guild_run == True).order_by(DungeonRunDB.score.desc()).limit(10).all()
            
            top10_runs = [DungeonRunDB(run.id,
                                       run.season,
                                       run.name,
                                       run.short_name,
                                       run.mythic_level,
                                       run.completed_at,
                                       run.clear_time_ms,
                                       run.par_time_ms,
                                       run.num_keystone_upgrades,
                                       run.score,
                                       run.url) for run in query]
            return top10_runs
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None        
        