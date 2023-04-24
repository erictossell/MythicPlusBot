##---------------Take a Lap Discord Bot-----------------
#Description: This file is used to create the database and tables for the bot. It is also used to query the database for information.
#Author: Eriim\
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Optional, List
from psycopg2 import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, joinedload
from dotenv import load_dotenv

from app.db.models.discord_guild_db import DiscordGuildDB
from app.db.models.character_db import CharacterDB
from app.db.models.character_history_db import CharacterHistoryDB
from app.db.models.dungeon_run_db import DungeonRunDB
from app.db.models.default_character_db import DefaultCharacterDB
from app.db.models.character_run_db import CharacterRunDB
from app.db.models.announcement_db import AnnouncementDB
from app.raiderIO.models.character import Character
from app.raiderIO.models.dungeon_run import DungeonRun

load_dotenv('configurations/main.env')
PASSWORD = os.getenv('RAILWAY_POSTGRES')

logging.basicConfig(filename='tal.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

async_engine = create_async_engine(
    'postgresql+asyncpg://postgres:'+PASSWORD+'@containers-us-west-142.railway.app:7486/railway',
    echo=False, logging_name='sqlalchemy.engine', echo_pool=True, pool_pre_ping=True
)

# Create a session factory for async sessions
AsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_= AsyncSession)

# Define an async context manager for session scope
@asynccontextmanager
async def async_session_scope():
    async_session = AsyncSessionLocal()
    try:
        yield async_session
        await async_session.commit()
        
    except IntegrityError as e:
        await async_session.rollback()
        print('Integrity Error')
        raise e
    except Exception as e:
        await async_session.rollback()
        raise e
    finally:
        await async_session.close()

#-----------------------Read Functions--------------------------------#

async def lookup_discord_guild(discord_guild_id: int) -> Optional[DiscordGuildDB]:
    """Look up a specific discord guild in the database.

    Args:
        discord_guild_id (integer): The discord guild id to look up.

    Returns:
        existing_guild: returns a guild object if found, otherwise returns None.
    """
    try:
        async with async_session_scope() as session:
            existing_guild_query = select(DiscordGuildDB).filter(DiscordGuildDB.id == discord_guild_id)
            result = await session.execute(existing_guild_query)
            existing_guild = result.scalar()
            if not existing_guild:
                return None
            else:
                return existing_guild
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def lookup_character(name: str, realm: str) -> Optional[CharacterDB]:
    """Look up a specific character in the database.

    Args:
        name (string): The name of the character to look up.
        realm (string): The realm of the character to look up.

    Returns:
        existing_character: returns a character object if found, otherwise returns None.
    """
    try:
        async with async_session_scope() as session:
            existing_character_query = select(CharacterDB).filter(CharacterDB.name == name, CharacterDB.realm == realm.lower())
            result = await session.execute(existing_character_query)
            existing_character = result.scalar()
            if existing_character is None:
                return None
            else:
                return existing_character
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def lookup_run(run_id: int) -> Optional[DungeonRunDB]:
    """Look up a specific run in the database.

    Args:
        run_id (integer): The run id to look up.

    Returns:
        existing_run: returns a run object if found, otherwise returns None.
    """
    try:
        async with async_session_scope() as session:
            run_query = select(DungeonRunDB).options(joinedload(DungeonRunDB.character_runs)).filter(DungeonRunDB.id == run_id)
            result = await session.execute(run_query)
            existing_run = result.scalar()
            return existing_run
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def lookup_character_run(character: CharacterDB, run: DungeonRunDB) -> CharacterRunDB:
    """Lookup a character run from the database.

    Args:
        character (CharacterDB): The CharacterDB.py object to lookup in the database.
        run (DungeonRunDB): The DungeonRunDB.py object to lookup in the database.

    Returns:
        CharacterRunDB: Returns a CharacterRunDB.py object if the character run exists, otherwise returns None.
    """
    print(f'Tal_DB : looking up character run: {character.name} for run: {run.name}')
    try:
        async with async_session_scope() as session:
            ec_query = select(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm)
            ec_result = await session.execute(ec_query)
            existing_character = ec_result.scalar()
            er_query = select(DungeonRunDB).filter(DungeonRunDB.id == run.id)
            er_result = await session.execute(er_query)
            existing_run = er_result.scalar()
            if existing_character is None:
                return None
            elif existing_run is None:
                return None
            else:
                ecr_query = select(CharacterRunDB).filter(CharacterRunDB.character_id == existing_character.id, CharacterRunDB.run_id == existing_run.id)
                ecr_result = await session.execute(ecr_query)
                existing_character_run = ecr_result.scalar()
                if existing_character_run is not None:
                    return existing_character_run
                else:
                    return None
    except SQLAlchemyError as error:
        print(error)
        return None

async def lookup_default_character(discord_guild_id, discord_user_id) -> DefaultCharacterDB:
    """Lookup a default character from the database.

    Returns:
        DefaultCharacterDB: Returns a DefaultCharacterDB.py object if the relationship exists, otherwise returns None.
    """
    
    try:
        async with async_session_scope() as session:
            default_character_query = select(DefaultCharacterDB).filter(DefaultCharacterDB.discord_guild_id == discord_guild_id, DefaultCharacterDB.discord_user_id == discord_user_id)
            result = await session.execute(default_character_query)
            default_character = result.scalar()
            if default_character is not None:   
                character_query = select(CharacterDB).filter(CharacterDB.id == default_character.character_id)
                characer_result = await session.execute(character_query)
                default_character.character = characer_result.scalar()               
                
                # Return the existing default_character object
                return default_character
            elif default_character is None:
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def lookup_next_announcement(discord_guild_id: int) -> AnnouncementDB:
    try:
        async with async_session_scope() as session:
            query = select(AnnouncementDB).filter(AnnouncementDB.discord_guild_id == discord_guild_id, AnnouncementDB.has_been_sent == False).order_by(AnnouncementDB.created_at.asc())
            result = await session.execute(query)
            existing_announcement = result.scalar()
            if existing_announcement is None:
                return None
            else:
                announcement = AnnouncementDB(id = existing_announcement.id,
                                              discord_guild_id = existing_announcement.discord_guild_id,
                                              announcement_channel_id = existing_announcement.announcement_channel_id,
                                              title = existing_announcement.title,
                                              content = existing_announcement.content,
                                              has_been_sent = existing_announcement.has_been_sent)
                existing_announcement.dungeon_run = (await session.execute(
                        select(DungeonRunDB).filter(DungeonRunDB.id == existing_announcement.dungeon_run_id)
                    )).scalar()
                if existing_announcement.dungeon_run is not None:
                    
                    dungeon_run = DungeonRunDB(id = existing_announcement.dungeon_run.id,
                                                    season = existing_announcement.dungeon_run.season,
                                                    name= existing_announcement.dungeon_run.name,
                                                    short_name= existing_announcement.dungeon_run.short_name,
                                                    mythic_level= existing_announcement.dungeon_run.mythic_level,
                                                    completed_at= existing_announcement.dungeon_run.completed_at,
                                                    clear_time_ms= existing_announcement.dungeon_run.clear_time_ms,
                                                    par_time_ms= existing_announcement.dungeon_run.par_time_ms,
                                                    num_keystone_upgrades= existing_announcement.dungeon_run.num_keystone_upgrades,
                                                    score= existing_announcement.dungeon_run.score,
                                                    url= existing_announcement.dungeon_run.url)
                    announcement.dungeon_run = dungeon_run
                return announcement
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None            

#-------------------------Create Functions------------------------------#

async def add_discord_guild(discord_guild : DiscordGuildDB) -> DiscordGuildDB:
    """Add a discord guild to the database.

    Args:
        discord_guild_id (int): The discord guild id to add to the database.

    Returns:
        DiscordGuildDB: Returns a DiscordGuildDB.py object if the guild was added to the database, otherwise returns None.
    """
    try:
        async with async_session_scope() as session:
            query = select(DiscordGuildDB).filter(DiscordGuildDB.id == discord_guild.id)
            result = await session.execute(query)
            existing_guild = result.scalar()
            if not existing_guild:
                discord_guild = DiscordGuildDB(id = discord_guild.id,
                                               discord_guild_name = discord_guild.discord_guild_name,
                                               wow_guild_name = discord_guild.wow_guild_name,
                                               wow_region = discord_guild.wow_region,
                                               wow_realm = discord_guild.wow_realm,
                                               announcement_channel_id = discord_guild.announcement_channel_id,
                                               modified_by = discord_guild.modified_by)
                session.add(discord_guild)
                await session.commit()
                return discord_guild
            else:
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def add_character(character: CharacterDB) -> CharacterDB:
    """Add a character to the database.

    Args:
        character (Character): The Character.py object to add to the database.

    Returns:
        bool: Returns True if the character was added to the database, otherwise returns False.
    """
    try:
        async with async_session_scope() as session:
            query = select(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm.lower()).first()
            result = await session.execute(query)
            existing_character = result.scalar()
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
                return character_db
            else:
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def add_character_history(character: CharacterDB) -> CharacterHistoryDB:
    """Add a history record for a character to the database.

    Args:
        character (CharacterDB): the CharacterDB.py object to add to the database.

    Returns:
        CharacterHistoryDB: The added CharacterHistoryDB.py object.
    """
    try:
        async with async_session_scope() as session:
            character_history = CharacterHistoryDB(character.discord_user_id,
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
            character_history.character = character
            session.add(character_history)
            return character_history
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def add_dungeon_run(dungeon_run: DungeonRun) -> bool:
    """Add a dungeon run to the database.

    Args:
        character (characterDB): The CharacterDB.py object for the character that completed the dungeon run.
        run (DungeonRun): The DungeonRun.py object to add to the database.

    Returns:
        bool: Returns True if the dungeon run was added to the database, otherwise returns False.
    """
    try:
        async with async_session_scope() as session:
            query = select(DungeonRunDB).filter(DungeonRunDB.id == int(dungeon_run.id))
            result = await session.execute(query)
            existing_dungeon_run = result.scalar()
            if existing_dungeon_run is None:
                dungeon_run = DungeonRunDB(int(dungeon_run.id),
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
                return False
            else:
                return False
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False

async def add_character_run(character_run: CharacterRunDB) -> Optional[CharacterRunDB]:
    try:
        async with async_session_scope() as session:
            ec_query = select(CharacterDB).filter(
                CharacterDB.name == character_run.character.name, CharacterDB.realm == character_run.character.realm)
            ec_result = await session.execute(ec_query)
            existing_character = ec_result.scalar()
            
            er_query = select(DungeonRunDB).filter(DungeonRunDB.id == character_run.dungeon_run.id)
            er_result = await session.execute(er_query)
            existing_run = er_result.scalar()

            if existing_character is None or existing_run is None:
                return None

            ecr_query = select(CharacterRunDB).filter(
                CharacterRunDB.character_id == existing_character.id,
                CharacterRunDB.dungeon_run_id == existing_run.id)
            ecr_result = await session.execute(ecr_query)
            existing_character_run = ecr_result.scalar()
            
            if existing_character_run is not None:
                return None

            character_run.character = existing_character
            character_run.dungeon_run = existing_run
            session.add(character_run)
            return character_run
    except SQLAlchemyError as error:
        print(error)
        return None

async def add_default_character(default_character: DefaultCharacterDB) -> bool:
    """Add a default character to the database.

    Returns:
        bool: Returns True if the character was added to the database, otherwise returns False.
    """
    try:
        async with async_session_scope() as session:
            er_query = select(DefaultCharacterDB).filter(DefaultCharacterDB.discord_guild_id == default_character.discord_guild_id,
                                                                             DefaultCharacterDB.discord_user_id == default_character.discord_user_id)
            er_result = await session.execute(er_query)
            existing_relationship = er_result.scalar()
            if existing_relationship is None:
                session.add(default_character)
                return True
            else:
                return False
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False

async def add_announcement(announcement: AnnouncementDB) -> bool:
    """Add an announcement to the database.

    Returns:
        bool: Returns True if the announcement was added to the database, otherwise returns False.
    """
    try:
        async with async_session_scope() as session:
            er_query = select(DungeonRunDB).filter(DungeonRunDB.id == announcement.dungeon_run_id)
            er_result = await session.execute(er_query)
            existing_dungeon_run = er_result.scalar()
            
            if existing_dungeon_run is None:
                return False            
            new_announcement = AnnouncementDB(discord_guild_id = announcement.discord_guild_id,
                                              announcement_channel_id=announcement.announcement_channel_id,
                                              title=announcement.title,
                                              content=announcement.content,
                                              dungeon_run_id=existing_dungeon_run.id)
            session.add(new_announcement)
            return new_announcement
            
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False

#-------------------------Update Functions------------------------------#

async def update_character(character: Character) -> CharacterDB:
    """Update an existing character in the database.

    Args:
        character (Character): The Character.py object to update in the database.

    Returns:
        bool: Returns True if the character was updated in the database, otherwise returns False.
    """
    try:
        async with async_session_scope() as session:
            existing_character_query = select(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm.lower())
            result = await session.execute(existing_character_query)
            existing_character = result.scalars().first()
            if existing_character is not None:                
                if has_any_character_field_changed(existing_character, character):
                    character_history = CharacterHistoryDB(existing_character.discord_user_id,
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
                    character_history.character = existing_character
                    session.add(character_history)
                
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
                #print('Tal_DB : updated character: ' + character.name + ' on realm: ' + character.realm)
                return existing_character
            else:
                #print('Tal_DB : character not found: ' + character.name + ' on realm: ' + character.realm)
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def update_character_reporting(character: Character) -> bool:
    """Update the reporting status of an existing character in the database.

    Args:
        character (Character): The Character.py object to update in the database.

    Returns:
        Bool: Returns True if the character was updated in the database, otherwise returns False.
    """
    
    print(f'Tal_DB : updating character reporting status: {character.name} on realm: {character.realm}')
    try:
        async with async_session_scope() as session:
            ec_query = select(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm.lower())
            ec_result = await session.execute(ec_query)
            existing_character = ec_result.scalar()
            if existing_character is not None:
                if existing_character.is_reporting is True:
                    existing_character.is_reporting = False
                else:
                    existing_character.is_reporting = True
                    character_history = CharacterHistoryDB(existing_character.discord_user_id,
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
                    character_history.character = existing_character
                    session.add(character_history)
                return True
            else:
                #print('Tal_DB : character not found: ' + character.name + ' on realm: ' + character.realm)
                return False
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False

async def update_dungeon_run(dungeon_run : DungeonRunDB) -> bool:
    """Update an existing dungeon run.

    Args:
        dungeon_run (DungeonRunDB): _description_
    """
    try:
        async with async_session_scope() as session:                
            er_query = select(DungeonRunDB).filter(DungeonRunDB.id == dungeon_run.id)
            er_result = await session.execute(er_query)
            existing_dungeon_run = er_result.scalar()
            if existing_dungeon_run is not None:
                existing_dungeon_run.is_guild_run = dungeon_run.is_guild_run
                existing_dungeon_run.is_crawled = True
                return True
            else:
                return False          
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False  

async def update_default_character(discord_user_id:int, discord_guild_id:int, character: CharacterDB) -> DefaultCharacterDB:
    """Update a default character in the database or create a new one if not exists.

    Args:
        default_character (DefaultCharacterDB): _description_

    Returns:
        Tuple[DefaultCharacterDB, bool]: Returns a tuple with the updated or created default character and a boolean indicating if the default character was updated (True) or created (False).
    """
    try: 
        async with async_session_scope() as session:
            
            er_query = select(DefaultCharacterDB).filter(DefaultCharacterDB.discord_guild_id == discord_guild_id,
                                                                             DefaultCharacterDB.discord_user_id == discord_user_id)
            er_result = await session.execute(er_query)
            existing_relationship = er_result.scalar()
            
            nc_query = select(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm.lower())
            nc_result = await session.execute(nc_query)
            new_character = nc_result.scalar()
            
            if new_character is None:
                return None
            
            if existing_relationship is not None:
                existing_relationship.character_id = new_character.id
                existing_relationship.version += 1
                character_name = new_character.name
                character_realm = new_character.realm
                return existing_relationship, character_name, character_realm
            
            else:
                default_character = DefaultCharacterDB(discord_user_id, discord_guild_id, character.id)
                session.add(default_character)
                character_name = new_character.name
                character_realm = new_character.realm
                return default_character, character_name, character_realm

    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None, False

async def update_announcement_has_been_sent(announcement_id: int) -> bool:
    """Update the announcement_has_been_sent field of an announcement.

    Args:
        announcement_id (int): The id of the announcement to update.

    Returns:
        Bool: Returns True if the announcement was updated in the database, otherwise returns False.
    """
    try:
        async with async_session_scope() as session:
            query = select(AnnouncementDB).filter(AnnouncementDB.id == announcement_id)
            result = await session.execute(query)
            existing_announcement = result.scalar()
            if existing_announcement is not None:
                existing_announcement.has_been_sent = True
                print('Tal_DB : updated announcement_has_been_sent for announcement: ' + str(announcement_id))
                return True
            else:
                print('Tal_DB : announcement not found: ' + str(announcement_id))
                return False
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False

async def set_guild_run(run: DungeonRun) -> bool:
    """Set a run as a guild run.

    Args:
        run (DungeonRun): The DungeonRun.py object to update in the database.

    Returns:
        Bool: Returns True if the run was updated in the database, otherwise returns False.
    """
    try:
        async with async_session_scope() as session:        
            query = select(DungeonRunDB).filter(DungeonRunDB.id == run.id)
            result = await session.execute(query)
            existing_run = result.scalar()
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

#-------------------------Delete Functions------------------------------#

async def remove_character(name, realm) -> bool:
    """Remove a character from the database.

    Args:
        name (string): The name of the character to remove.
        realm (string): The realm of the character to remove.

    Returns:
        bool: Returns True if the character was removed from the database, otherwise returns False.
    """
    try:
        async with async_session_scope() as session:
            query = select(CharacterDB).filter(CharacterDB.name == name, CharacterDB.realm == realm)
            result = await session.execute(query)
            existing_character = result.scalar()
            if existing_character is not None:
                session.delete(existing_character)
                return True
            else:            
                return False
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False

async def remove_default_character(default_character: DefaultCharacterDB) -> bool:
    """Remove a default character from the database.

    Returns:
        bool: Returns True if the character was removed from the database, otherwise returns False.
    """
    try:
        async with async_session_scope() as session:
            query = select(DefaultCharacterDB).filter(DefaultCharacterDB.discord_guild_id == default_character.discord_guild_id,
                                                                             DefaultCharacterDB.discord_user_id == default_character.discord_user_id)
            result = await session.execute(query)
            existing_relationship = result.scalar()
            if existing_relationship is not None:
                session.delete(existing_relationship)
                return True
            else:
                return False
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False 

#-------------------------Bulk Read Functions------------------------------#

async def get_all_characters() -> List[CharacterDB]:
    """Get all of the characters from the database.

    Returns:
        characters_list: a list of all of the characters in the database.
    """
    try:
        async with async_session_scope() as session:
            characters_query = (
                select(CharacterDB)
                .options(joinedload(CharacterDB.discord_guild))  # Load the relationship
                .join(CharacterDB.discord_guild)  # Join the tables using the relationship
            )
            result = await session.execute(characters_query)
            characters_list = result.scalars().unique().all()
            return characters_list
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_all_characters_active_in_last_30_days() -> List[CharacterDB]:
    """Get all of the characters from the database.

    Returns:
        characters_list: a list of all of the characters in the database.
    """
    try:
        async with async_session_scope() as session:
            characters_query = select(CharacterDB).filter(CharacterDB.last_crawled_at > datetime.now() - timedelta(days=30), CharacterDB.is_reporting == True)
            result = await session.execute(characters_query)
            characters = result.scalars().unique().all()
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
                                           character.is_reporting) for character in characters]
            return characters_list
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_all_characters_not_recently_crawled() -> List[CharacterDB]:
    """Get all of the characters from the database that have not been crawled recently.

    Returns:
        List[CharacterDB]: A list of all of the characters in the database that have not been crawled recently.
    """
    try:
        async with async_session_scope() as session: 
            characters_query = select(CharacterDB).filter(CharacterDB.last_crawled_at < datetime.now() - timedelta(days=1), CharacterDB.is_reporting == True)
            result = await session.execute(characters_query)
            characters = result.scalars().unique().all()
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
                                           character.is_reporting) for character in characters]
            return characters_list
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_all_runs() -> List[DungeonRunDB]:
    """Get all of the runs from the database.

    Returns:
        runs_list: A list of all of the runs in the database.
    """
    try:
        async with async_session_scope() as session:
            runs_query = select(DungeonRunDB)
            result = await session.execute(runs_query)
            runs = result.scalars().unique().all()
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
                                      run.url) for run in runs]
            return runs_list
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_all_runs_not_crawled() -> List[DungeonRunDB]:
    """Get all of the runs that have not been crawled.

    Returns:
        List[DungeonRunDB]: A list of all of the runs that have not been crawled.
    """
    try:
        async with async_session_scope() as session:
            runs_query = select(DungeonRunDB).filter(DungeonRunDB.is_crawled == False)
            result = await session.execute(runs_query)
            runs = result.scalars().unique().all()
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
                                      run.url) for run in runs]
            return runs_list
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_all_characters_for_run(run_id: int) -> List[CharacterRunDB]:
    """Get all characters for a run.

    Args:
        run (DungeonRunDB): The DungeonRunDB.py object to lookup in the database.

    Returns:
        List[CharacterRunDB]: Returns a list of CharacterRunDB.py objects if the character run exists, otherwise returns None.
    """
    try:
        async with async_session_scope() as session:
            query = select(DungeonRunDB).filter(DungeonRunDB.id == run_id)
            result = await session.execute(query)
            existing_run = result.scalar()
            if existing_run is None:
                return None
            else:
                existing_character_runs_query = select(CharacterRunDB).filter(CharacterRunDB.dungeon_run_id == existing_run.id)
                excresult = await session.execute(existing_character_runs_query)
                existing_character_runs = excresult.scalars().all()
                existing_characters = select(CharacterDB).filter(CharacterDB.id.in_([char.character_id for char in existing_character_runs]))
                ecresult = await session.execute(existing_characters)
                existing_characters = ecresult.scalars().unique().all()
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

async def get_all_runs_for_character(character: CharacterDB) -> List[CharacterRunDB]:
    """Get all runs for a character.

    Args:
        character (CharacterDB): The CharacterDB.py object to lookup in the database.

    Returns:
        List[CharacterRunDB]: Returns a list of CharacterRunDB.py objects if the character run exists, otherwise returns None.
    """
    try:
        async with async_session_scope() as session:
            query = select(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm)
            result = await session.execute(query)
            existing_character = result.scalar()
            if existing_character is None:
                return None
            else:
                existing_character_runs_query = select(CharacterRunDB)\
                                        .join(DungeonRunDB, CharacterRunDB.dungeon_run_id == DungeonRunDB.id)\
                                        .filter(CharacterRunDB.character_id == existing_character.id)\
                                        .order_by(DungeonRunDB.score.desc())\
                                        .limit(10)
                result = await session.execute(existing_character_runs_query)
                existing_character_runs = result.scalars().unique().all()
                if existing_character_runs is not None:
                    run_list = []
                    for character_run in existing_character_runs:
                        run_query = select(DungeonRunDB).filter(DungeonRunDB.id == character_run.dungeon_run_id)
                        run_result = await session.execute(run_query)
                        run = run_result.scalar()
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
                    return run_list
                else:
                    return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 

async def get_top10_character_by_achievement() -> List[CharacterDB]:
    """Get the top 10 characters by achievement points.

    Returns:
        List[CharacterDB]: Returns a list of the top 10 characters by achievement points.
    """
    try:
        async with async_session_scope() as session:
            query = select(CharacterDB).order_by(CharacterDB.achievement_points.desc()).limit(10)
            result = await session.execute(query)
            characters = result.scalars().unique().all()
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
                                            char.is_reporting) for char in characters]
            return top10_characters
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 

async def get_top10_character_by_mythic_plus() -> List[CharacterDB]:
    """Get the top 10 characters by mythic plus score.

    Returns:
        List[CharacterDB]: Returns a list of the top 10 characters by mythic plus score.
    """
    try:
        async with async_session_scope() as session:
            query = select(CharacterDB).order_by(CharacterDB.score.desc()).limit(10)
            result = await session.execute(query)
            characters = result.scalars().unique().all()
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
                                            char.is_reporting) for char in characters]
            return top10_characters
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 

async def get_top10_character_by_highest_item_level() -> List[CharacterDB]:
    """Get the top 10 characters by highest item level.

    Returns:
        List[CharacterDB]: Returns a list of the top 10 characters by highest item level.
    """
    try:
        async with async_session_scope() as session:
            
            query = select(CharacterDB).order_by(CharacterDB.item_level.desc()).limit(10)
            result = await session.execute(query)
            characters = result.scalars().unique().all()
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
                                            char.is_reporting) for char in characters]
            return top10_characters
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 

async def get_top10_guild_runs_this_week() -> List[DungeonRunDB]:
    try: 
        async with async_session_scope() as session:
            one_week_ago = datetime.now() - timedelta(weeks=1)
            query = select(DungeonRunDB).filter(DungeonRunDB.is_guild_run == True,
                                                                                DungeonRunDB.num_keystone_upgrades >= 1,
                                                                                DungeonRunDB.completed_at >= one_week_ago).order_by(DungeonRunDB.score.desc()).limit(10)
            result = await session.execute(query)
            runs = result.scalars().unique().all()
            
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
                                       run.url) for run in runs]
            return top10_runs
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_top10_guild_runs_all_time() -> List[DungeonRunDB]:
    try: 
        async with async_session_scope() as session:
            query = select(DungeonRunDB).filter(DungeonRunDB.is_guild_run == True,
                                                DungeonRunDB.num_keystone_upgrades >= 1).order_by(DungeonRunDB.score.desc()).limit(10)
            result = await session.execute(query)
            runs = result.scalars().unique().all()
            
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
                                       run.url) for run in runs] 
            return top10_runs
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

#-------------------------Comparison Functions------------------------------#

def has_any_character_field_changed(existing_character: CharacterDB, character: Character) -> bool:
    return (existing_character.guild_name != character.guild_name or
            existing_character.realm != character.realm.lower() or
            existing_character.faction != character.faction or
            existing_character.region != character.region or
            existing_character.role != character.role or
            existing_character.spec_name != character.spec_name or
            existing_character.class_name != character.class_name or
            existing_character.achievement_points != character.achievement_points or
            existing_character.item_level != character.item_level or
            existing_character.score != character.score or
            existing_character.rank != character.rank or
            existing_character.thumbnail_url != character.thumbnail_url or
            existing_character.url != character.url or
            existing_character.last_crawled_at != character.last_crawled_at or
            existing_character.is_reporting != character.is_reporting)
