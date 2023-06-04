##---------------Take a Lap Discord Bot-----------------
#Description: This file is used to create the database and tables for the bot. It is also used to query the database for information.
#Author: Eriim\

import os
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Optional, List, DefaultDict
from psycopg2 import IntegrityError
from sqlalchemy import desc, select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, joinedload
from dotenv import load_dotenv
from app.db.base import Base

from app.db.models.game_db import GameDB
from app.db.models.game_guild_db import GameGuildDB
from app.db.models.discord_guild_db import DiscordGuildDB
from app.db.models.discord_game_guilds_db import DiscordGameGuildDB

from app.db.models.discord_guild_run_db import DiscordGuildRunDB
from app.db.models.discord_user_character_db import DiscordUserCharacterDB
from app.db.models.discord_guild_character_db import DiscordGuildCharacterDB

from app.db.models.character_db import CharacterDB
from app.db.models.character_history_db import CharacterHistoryDB

from app.db.models.dungeon_run_db import DungeonRunDB
from app.db.models.character_run_db import CharacterRunDB

from app.db.models.announcement_db import AnnouncementDB

from app.raiderIO.models.character import Character
from app.raiderIO.models.dungeon_run import DungeonRun


load_dotenv('configurations/main.env')

DEV_RAILWAY = os.getenv('DEV_RAILWAY')

async_engine = create_async_engine(
    DEV_RAILWAY,
    echo=False,
    logging_name='sqlalchemy.engine',
    echo_pool=True,
    pool_pre_ping=True
)

async def create_schema():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

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

async def get_discord_game_guild_by_guild_ids(discord_guild_id: int, game_guild_id: int) -> Optional[DiscordGameGuildDB]:
    try:
        async with async_session_scope() as session:
            query = select(DiscordGameGuildDB).filter(DiscordGameGuildDB.discord_guild_id == discord_guild_id, DiscordGameGuildDB.game_guild_id == game_guild_id)
            result = await session.execute(query)
            existing_discord_game_guild = result.scalar()
            
            if existing_discord_game_guild:
                return existing_discord_game_guild
            else:
                return None
            
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_discord_guild_character_by_name(discord_guild_id: int, name :str) -> Optional[DiscordGuildCharacterDB]:
    try:
        async with async_session_scope() as session:
            query = (
                select(DiscordGuildCharacterDB)
                .join(CharacterDB)
                .filter(CharacterDB.name == name, DiscordGuildCharacterDB.discord_guild_id == discord_guild_id)
            )
            result = await session.execute(query)
            existing_discord_guild_character = result.scalar()
            if existing_discord_guild_character:
                return existing_discord_guild_character
            else:
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_character_by_name_realm_and_discord_guild(name: str, realm: str, discord_guild_id: int) -> Optional[CharacterDB]:
    try:
        async with async_session_scope() as session:
            query = (
                select(CharacterDB)
                .join(DiscordGuildCharacterDB)
                .filter(CharacterDB.name == name, CharacterDB.realm == realm, DiscordGuildCharacterDB.discord_guild_id == discord_guild_id)
            )
            result = await session.execute(query)
            existing_character = result.scalar()
            if existing_character:
                return existing_character
            else:
                return None
            
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_game_guild_by_name_realm(name: str, realm: str) -> Optional[GameGuildDB]:
    try:
        async with async_session_scope() as session:
            query = select(GameGuildDB).filter(GameGuildDB.name == name, GameGuildDB.realm == realm)
            result = await session.execute(query)
            existing_game_guild = result.scalar()
            if existing_game_guild:
                return existing_game_guild
            return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_discord_guild_by_id(discord_guild_id: int) -> Optional[DiscordGuildDB]:
    """Look up a specific discord guild in the database.

    Args:
        discord_guild_id (integer): The discord guild id to look up.

    Returns:
        existing_guild: returns a guild object if found, otherwise returns None.
    """
    try:
        async with async_session_scope() as session:
            existing_guild_query = select(DiscordGuildDB).filter(DiscordGuildDB.id == int(discord_guild_id))
            result = await session.execute(existing_guild_query)
            existing_guild = result.scalar()
            if not existing_guild:
                return None
            else:
                return existing_guild
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_character_by_name_realm(name: str, realm: str) -> Optional[CharacterDB]:
    """Look up a specific character in the database.

    Args:
        name (string): The name of the character to look up.
        realm (string): The realm of the character to look up.

    Returns:
        existing_character: returns a character object if found, otherwise returns None.
    """
    try:
        async with async_session_scope() as session:
            existing_character_query = (
                select(CharacterDB)
                .options(joinedload(CharacterDB.discord_guild_characters))
                .join(DiscordGuildCharacterDB)
                .filter(CharacterDB.name == name, CharacterDB.realm == realm)
                )
            result = await session.execute(existing_character_query)
            existing_character = result.scalar()
            if existing_character is None:
                return None
            else:
                return existing_character
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_run_by_id(run_id: int, season:str) -> Optional[DungeonRunDB]:
    """Look up a specific run in the database.

    Args:
        run_id (integer): The run id to look up.

    Returns:
        existing_run: returns a run object if found, otherwise returns None.
    """
    try:
        async with async_session_scope() as session:
            run_query = (
                select(DungeonRunDB)
                .options(joinedload(DungeonRunDB.character_runs))
                .filter(DungeonRunDB.dungeon_id == run_id, DungeonRunDB.season == season)
                )
            result = await session.execute(run_query)
            existing_run = result.scalar()
            return existing_run
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_character_run_by_character_run(character: CharacterDB, run: DungeonRunDB) -> CharacterRunDB:
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

async def get_discord_user_character_by_guild_user(discord_user_id) -> DiscordUserCharacterDB:
    """Lookup a default character from the database.

    Returns:
        DiscordUserCharacterDB: Returns a DiscordUserCharacterDB.py object if the relationship exists, otherwise returns None.
    """
    
    try:
        async with async_session_scope() as session:
            discord_user_character_query = select(DiscordUserCharacterDB).filter(DiscordUserCharacterDB.discord_user_id == discord_user_id)
            result = await session.execute(discord_user_character_query)
            discord_user_character = result.scalar()
            if discord_user_character is not None:   
                character_query = select(CharacterDB).filter(CharacterDB.id == discord_user_character.character_id)
                characer_result = await session.execute(character_query)
                discord_user_character.character = characer_result.scalar()
                
                # Return the existing discord_user_character object
                return discord_user_character
            elif discord_user_character is None:
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_next_announcement_by_guild_id(discord_guild_id: int) -> AnnouncementDB:
    try:
        async with async_session_scope() as session:
            
            #timedelta for one week ago
            one_week_ago = datetime.now() - timedelta(days=7)
            #retreive guild announcements for runs completed in the last week
            query = (
                select(AnnouncementDB)
                .options(joinedload(AnnouncementDB.dungeon_run))  # eager load dungeon_run                
                .join(DungeonRunDB.announcements)
                .filter(AnnouncementDB.discord_guild_id == discord_guild_id, DungeonRunDB.completed_at >= one_week_ago, AnnouncementDB.has_been_sent == False)
                .order_by(DungeonRunDB.completed_at.desc())
            )
            result = await session.execute(query)
            announcement = result.scalar()
            return announcement
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None            

#-------------------------Create Functions------------------------------#

async def add_discord_guild_character(discord_guild: DiscordGuildDB, character: CharacterDB):
    try:
        async with async_session_scope() as session:
            guild_query = select(DiscordGuildDB).filter(DiscordGuildDB.id == discord_guild.id)
            guild_result = await session.execute(guild_query)
            existing_guild = guild_result.scalar()
            
            if existing_guild:
                
                character_query = select(CharacterDB).filter(CharacterDB.id == character.id)
                character_result = await session.execute(character_query)
                existing_character = character_result.scalar()
                
                if existing_character:
                    
                    guild_character_query = (
                        select(DiscordGuildCharacterDB.id)
                        .filter(DiscordGuildCharacterDB.discord_guild_id == existing_guild.id, DiscordGuildCharacterDB.character_id == existing_character.id)
                        
                    )
                    guild_character_result = await session.execute(guild_character_query)
                    existing_guild_character = guild_character_result.scalar()
                    if existing_guild_character:
                        return existing_guild_character
                    else:
                        discord_guild_character = DiscordGuildCharacterDB(discord_guild_id=existing_guild.id, character_id=existing_character.id)
                        session.add(discord_guild_character)
                        return discord_guild_character
                    
                else:
                    return None
            else:
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None
    
async def add_discord_guild_run(discord_guild: DiscordGuildDB, dungeon_run: DungeonRunDB) -> DiscordGuildRunDB:
    try:
        async with async_session_scope() as session:
            guild_query = select(DiscordGuildDB).filter(DiscordGuildDB.id == discord_guild.id)
            guild_result = await session.execute(guild_query)
            existing_guild = guild_result.scalar()
            
            if existing_guild:
                
                run_query = select(DungeonRunDB).filter(DungeonRunDB.id == dungeon_run.id)
                run_result = await session.execute(run_query)
                existing_run = run_result.scalar()
                
                if existing_run:
                    
                    guild_run_query = select(DiscordGuildRunDB).filter(DiscordGuildRunDB.discord_guild_id == discord_guild.id, DiscordGuildRunDB.dungeon_run_id == dungeon_run.id)
                    guild_run_result = await session.execute(guild_run_query)
                    existing_guild_run = guild_run_result.scalar()
                    
                    if existing_guild_run:
                        return existing_guild_run
                    
                    else:
                        new_guild_run = DiscordGuildRunDB(discord_guild_id = discord_guild.id, dungeon_run_id = dungeon_run.id)
                        session.add(new_guild_run)
                        return new_guild_run
            else:
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None           

async def add_discord_guild(discord_guild : DiscordGuildDB) -> DiscordGuildDB:
    """Add a discord guild to the database.

    Args:
        discord_guild_id (int): The discord guild to add to the database.

    Returns:
        DiscordGuildDB: Returns a DiscordGuildDB.py object if the guild was added to the database, otherwise returns None.
    """
    try:
        async with async_session_scope() as session:
            query = select(DiscordGuildDB).filter(DiscordGuildDB.id == discord_guild.id)
            result = await session.execute(query)
            existing_guild = result.scalar()
            if not existing_guild:                
                new_discord_guild = session.add(discord_guild)               
                return new_discord_guild
            else:
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def add_game_guild(game_guild: GameGuildDB) -> GameGuildDB:
    """Add a game guild to the database.

    Args:
        game_guild (GameGuildDB): The game guild to add to the database.

    Returns:
        GameGuildDB: A copy of the GameGuildDB.py object that was added to the database.
    """
    try:
        async with async_session_scope() as session:
            query = select(GameGuildDB).filter(GameGuildDB.id == game_guild.id)
            result = await session.execute(query)
            existing_guild = result.scalar()
            if not existing_guild:
                new_game_guild = session.add(game_guild)
                return new_game_guild
            else:
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def add_discord_game_guild(discord_game_guild: DiscordGameGuildDB) -> DiscordGameGuildDB:
    try:
        async with async_session_scope() as session:
            query = select(DiscordGameGuildDB).filter(DiscordGameGuildDB.discord_guild_id == discord_game_guild.discord_guild_id, DiscordGameGuildDB.game_guild_id == discord_game_guild.game_guild_id)
            result = await session.execute(query)
            existing_game_guild = result.scalar()
            if not existing_game_guild:
                new_discord_game_guild = session.add(discord_game_guild)
                return new_discord_game_guild
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
            query = select(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm)
            result = await session.execute(query)
            existing_character = result.scalar()
            if existing_character is None:
                new_character = session.add(character)
                return new_character
            else:
                return existing_character
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
            character_history = CharacterHistoryDB( name = character.name,
                                                    realm = character.realm,
                                                    faction = character.faction,
                                                    region = character.region,
                                                    role = character.role,
                                                    spec_name = character.spec_name,
                                                    class_name = character.class_name,
                                                    achievement_points = character.achievement_points,
                                                    item_level = character.item_level,
                                                    score = character.score,
                                                    rank = character.rank,
                                                    thumbnail_url = character.thumbnail_url,
                                                    url = character.url,
                                                    last_crawled_at = character.last_crawled_at)
            character_history.character = character
            session.add(character_history)
            return character_history
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def add_dungeon_run(dungeon_run: DungeonRunDB) -> DungeonRunDB:
    """Add a dungeon run to the database.

    Args:
        character (characterDB): The CharacterDB.py object for the character that completed the dungeon run.
        run (DungeonRun): The DungeonRun.py object to add to the database.

    Returns:
        bool: Returns True if the dungeon run was added to the database, otherwise returns False.
    """
    try:
        if type(dungeon_run.dungeon_id) == str:
            dungeon_run.dungeon_id = int(dungeon_run.dungeon_id)
        async with async_session_scope() as session:
            query = (
                select(DungeonRunDB)
                .filter(DungeonRunDB.dungeon_id == int(dungeon_run.dungeon_id), DungeonRunDB.season == dungeon_run.season)
            )
            result = await session.execute(query)
            existing_dungeon_run = result.scalar()
            if existing_dungeon_run is None:
                dungeon_run.dungeon_id = int(dungeon_run.dungeon_id)
                session.add(dungeon_run)
                return dungeon_run
            elif existing_dungeon_run.dungeon_id == dungeon_run.dungeon_id:
                return existing_dungeon_run
            else:
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

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

async def add_discord_user_character(discord_user_character: DiscordUserCharacterDB) -> DiscordUserCharacterDB:
    """Add a default character to the database.

    Returns:
        bool: Returns True if the character was added to the database, otherwise returns False.
    """
    try:
        async with async_session_scope() as session:
            er_query = select(DiscordUserCharacterDB).filter(DiscordUserCharacterDB.discord_user_id == discord_user_character.discord_user_id)
            er_result = await session.execute(er_query)
            existing_relationship = er_result.scalar()
            if existing_relationship is None:
                new_discord_user_character = session.add(discord_user_character)
                return new_discord_user_character
            else:
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

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

async def update_discord_guild(discord_guild: DiscordGuildDB) -> DiscordGuildDB:
    """Update an existing discord guild in the database.

    Args:
        discord_guild (DiscordGuildDB): The DiscordGuildDB.py object to update in the database.

    Returns:
        DiscordGuildDB: Returns the updated DiscordGuildDB object if the guild was updated in the database, otherwise returns None.
    """
    try:
        async with async_session_scope() as session:
            
            existing_guild_query = select(DiscordGuildDB).filter(DiscordGuildDB.id == discord_guild.id)
            
            existing_guild_result = await session.execute(existing_guild_query)
            
            existing_guild = existing_guild_result.scalar()
            
            if not existing_guild:                
                return None
            
            else:                
                existing_guild.discord_guild_name = discord_guild.discord_guild_name
                existing_guild.announcement_channel_id = discord_guild.announcement_channel_id
                existing_guild.players_per_run = discord_guild.players_per_run                
                
                if discord_guild.announcement_channel_id:
                    existing_guild.is_announcing = True
                
                else: 
                    existing_guild.is_announcing = False
                    
                return existing_guild
            
    except IntegrityError as error:
        print(f'Integrit Error while updating the guild: {error}')
        return None
    except SQLAlchemyError as error:
        print(f'SQLAlchemy Error while querying the database: {error}')
        return None
    except Exception as error:
        print(f'Error while updating the guild: {error}')
        return None
    
async def update_discord_guild_character(discord_guild_character = DiscordGuildCharacterDB) -> DiscordGuildCharacterDB:
    """Update an existing discord guild character in the database.

    Args:
        discord_guild_character (_type_, optional): _description_. Defaults to DiscordGuildCharacterDB.

    Returns:
        DiscordGuildCharacterDB: _description_
    """
    
    try: 
        async with async_session_scope() as session:
            query = select(DiscordGuildCharacterDB).filter(DiscordGuildCharacterDB.discord_guild_id == discord_guild_character.discord_guild_id,
                                                              DiscordGuildCharacterDB.character_id == discord_guild_character.character_id)
            result = await session.execute(query)
            existing_discord_guild_character = result.scalar()
            if not existing_discord_guild_character:
                return None
            else:
                existing_discord_guild_character.guild_character_score = discord_guild_character.guild_character_score
                existing_discord_guild_character.is_reporting = discord_guild_character.is_reporting
                
                return existing_discord_guild_character
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None
 
async def update_character(character: Character) -> CharacterDB:
    """Update an existing character in the database.

    Args:
        character (Character): The Character.py object to update in the database.

    Returns:
        bool: Returns True if the character was updated in the database, otherwise returns False.
    """
    try:
        async with async_session_scope() as session:
            
            existing_character_query = (
                select(CharacterDB)
                .filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm)
                )
            result = await session.execute(existing_character_query)
            existing_character = result.scalars().first()
            if not existing_character:
                return None
            else:      
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
                
                #print('Tal_DB : updated character: ' + character.name + ' on realm: ' + character.realm)
                return existing_character
            
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
                    character_history = CharacterHistoryDB(name = existing_character.name,
                                                        realm = existing_character.realm,
                                                        faction = existing_character.faction,
                                                        region = existing_character.region,
                                                        role = existing_character.role,
                                                        spec_name = existing_character.spec_name,
                                                        class_name = existing_character.class_name,
                                                        achievement_points = existing_character.achievement_points,
                                                        item_level = existing_character.item_level,
                                                        score = existing_character.score,
                                                        rank = existing_character.rank,
                                                        thumbnail_url = existing_character.thumbnail_url,
                                                        url = existing_character.url,
                                                        last_crawled_at= existing_character.last_crawled_at)
                    character_history.character = existing_character
                    session.add(character_history)
                return True
            else:
                #print('Tal_DB : character not found: ' + character.name + ' on realm: ' + character.realm)
                return False
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return False

async def update_dungeon_run(dungeon_run : DungeonRunDB) -> Optional[DungeonRunDB]:
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
                return existing_dungeon_run
            else:
                return None          
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None  

async def update_discord_user_character(discord_user_id:int, character: CharacterDB) -> DiscordUserCharacterDB:
    """Update a default character in the database or create a new one if not exists.

    Args:
        discord_user_character (DiscordUserCharacterDB): _description_

    Returns:
        Tuple[DiscordUserCharacterDB, bool]: Returns a tuple with the updated or created default character and a boolean indicating if the default character was updated (True) or created (False).
    """
    try: 
        async with async_session_scope() as session:
            
            er_query = select(DiscordUserCharacterDB).filter(DiscordUserCharacterDB.discord_user_id == discord_user_id)
            er_result = await session.execute(er_query)
            existing_relationship = er_result.scalar()
            
            nc_query = select(CharacterDB).filter(CharacterDB.name == character.name, CharacterDB.realm == character.realm)
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
                discord_user_character = DiscordUserCharacterDB(discord_user_id, character.id)
                session.add(discord_user_character)
                character_name = new_character.name
                character_realm = new_character.realm
                return discord_user_character, character_name, character_realm

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
    
#-------------------------Bulk Update Functions------------------------------#



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

async def remove_discord_user_character(discord_user_character: DiscordUserCharacterDB) -> bool:
    """Remove a default character from the database.

    Returns:
        bool: Returns True if the character was removed from the database, otherwise returns False.
    """
    try:
        async with async_session_scope() as session:
            query = select(DiscordUserCharacterDB).filter(DiscordUserCharacterDB.discord_guild_id == discord_user_character.discord_guild_id,
                                                                             DiscordUserCharacterDB.discord_user_id == discord_user_character.discord_user_id)
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

async def get_all_daily_runs(discord_guild_id: int) -> Optional[List[DungeonRunDB]]:
    try:
        async with async_session_scope() as session:
            #get all runs from the last 24 hours for a particular guild
            subquery = (
                select(DungeonRunDB.id, DungeonRunDB.score)  # Select only the id column
                .join(CharacterRunDB.dungeon_run)
                .join(CharacterDB, CharacterDB.id == CharacterRunDB.character_id)
                .join(DiscordGuildCharacterDB, DiscordGuildCharacterDB.character_id == CharacterDB.id)
                .filter(DungeonRunDB.completed_at > datetime.utcnow() - timedelta(days=1), DiscordGuildCharacterDB.discord_guild_id == discord_guild_id)
                .order_by(desc(DungeonRunDB.score))                
                .distinct()
            )
            
            subquery_alias = subquery.subquery().alias()  # Add this line to create the alias
           
            query = (
                select(DungeonRunDB)                
                .where(DungeonRunDB.id.in_(select(subquery_alias.c.id)))
                .order_by(desc(DungeonRunDB.score))
                .distinct()# Use a select() construct explicitly
            )
            result = await session.execute(query)
            result = result.scalars().all()
            
            return result
            
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None
    
async def get_all_weekly_runs(discord_guild_id: int) -> Optional[List[DungeonRunDB]]:
    try:
        async with async_session_scope() as session:
            #get all runs from the last 24 hours for a particular guild
            subquery = (
                select(DungeonRunDB.id, DungeonRunDB.score)  # Select only the id column
                .join(CharacterRunDB.dungeon_run)
                .join(CharacterDB, CharacterDB.id == CharacterRunDB.character_id)
                .join(DiscordGuildCharacterDB, DiscordGuildCharacterDB.character_id == CharacterDB.id)
                .filter(DungeonRunDB.completed_at > datetime.utcnow() - timedelta(weeks=1), DiscordGuildCharacterDB.discord_guild_id == discord_guild_id)
                .order_by(desc(DungeonRunDB.score))                
                .distinct()
            )
            
            subquery_alias = subquery.subquery().alias()  # Add this line to create the alias
           
            query = (
                select(DungeonRunDB)                
                .where(DungeonRunDB.id.in_(select(subquery_alias.c.id)))
                .order_by(desc(DungeonRunDB.score))
                .distinct()# Use a select() construct explicitly
            )
            result = await session.execute(query)
            result = result.scalars().all()
            
            return result
            
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None
    
async def get_daily_guild_runs(discord_guild_id: int) -> Optional[DefaultDict[List[DungeonRunDB], List[CharacterDB]]]:
    try:
        async with async_session_scope() as session:
            subquery = (
                select(DungeonRunDB.id, DungeonRunDB.score)
                .join(DiscordGuildRunDB.dungeon_run)                
                .filter(DungeonRunDB.completed_at > datetime.utcnow() - timedelta(days=1), DiscordGuildRunDB.discord_guild_id == discord_guild_id)
                .order_by(desc(DungeonRunDB.score))
                .limit(5)
            )
            subquery_alias = subquery.subquery().alias()
            
            query = (
                select(DungeonRunDB, CharacterRunDB)
                .options(joinedload(DungeonRunDB.character_runs))
                .options(joinedload(CharacterRunDB.character))
                .join(CharacterRunDB.dungeon_run)
                .join(CharacterDB, CharacterDB.id == CharacterRunDB.character_id)
                .join(DiscordGuildCharacterDB, DiscordGuildCharacterDB.character_id == CharacterDB.id)
                .where(DungeonRunDB.id.in_(select(subquery_alias.c.id)))
                .order_by(desc(DungeonRunDB.score))
                .distinct()# Use a select() construct explicitly
            )

            result = await session.execute(query)
            result = result.unique()
            grouped_result = defaultdict(list)
            for dungeon_run, character in result:
                grouped_result[dungeon_run].append(character)

            dungeon_runs_with_characters = list(grouped_result.items())
            return dungeon_runs_with_characters
        
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_daily_non_guild_runs(discord_guild_id: int, number_of_runs: int) -> Optional[DefaultDict[List[DungeonRunDB], List[CharacterDB]]]:
    try:
        async with async_session_scope() as session:
            subquery = (
                select(DungeonRunDB.id, DungeonRunDB.score)  # Select only the id column
                .join(CharacterRunDB.dungeon_run)
                .join(CharacterDB, CharacterDB.id == CharacterRunDB.character_id)
                .join(DiscordGuildCharacterDB, DiscordGuildCharacterDB.character_id == CharacterDB.id)
                .filter(DungeonRunDB.completed_at > datetime.utcnow() - timedelta(days=1), DiscordGuildCharacterDB.discord_guild_id == discord_guild_id)
                .order_by(desc(DungeonRunDB.score))
                .limit(number_of_runs)
                .distinct()
            )

            subquery_alias = subquery.subquery().alias()  # Add this line to create the alias

            query = (
                select(DungeonRunDB, CharacterRunDB)
                .options(joinedload(DungeonRunDB.character_runs))
                .options(joinedload(CharacterRunDB.character))
                
                .join(CharacterRunDB.dungeon_run)
                .join(CharacterDB, CharacterDB.id == CharacterRunDB.character_id)
                .join(DiscordGuildCharacterDB, DiscordGuildCharacterDB.character_id == CharacterDB.id)
                .where(DungeonRunDB.id.in_(select(subquery_alias.c.id)))
                .order_by(desc(DungeonRunDB.score))
                .distinct()# Use a select() construct explicitly
            )

            result = await session.execute(query)
            result = result.unique()

            grouped_result = defaultdict(list)
            for dungeon_run, character in result:
                grouped_result[dungeon_run].append(character)

            dungeon_runs_with_characters = list(grouped_result.items())
            return dungeon_runs_with_characters
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None
    
async def get_weekly_non_guild_runs(discord_guild_id: int, number_of_runs: int) -> Optional[DefaultDict[List[DungeonRunDB], List[CharacterDB]]]:
    try:
        async with async_session_scope() as session:
            subquery = (
                select(DungeonRunDB.id, DungeonRunDB.score)  # Select only the id column
                .join(CharacterRunDB.dungeon_run)
                .join(CharacterDB, CharacterDB.id == CharacterRunDB.character_id)
                .join(DiscordGuildCharacterDB, DiscordGuildCharacterDB.character_id == CharacterDB.id)
                .filter(DungeonRunDB.completed_at > datetime.utcnow() - timedelta(weeks=1), DiscordGuildCharacterDB.discord_guild_id == discord_guild_id)
                .order_by(desc(DungeonRunDB.score))
                .limit(number_of_runs)
                .distinct()
            )

            subquery_alias = subquery.subquery().alias()  # Add this line to create the alias

            query = (
                select(DungeonRunDB, CharacterRunDB)
                .options(joinedload(DungeonRunDB.character_runs))
                .options(joinedload(CharacterRunDB.character))
                
                .join(CharacterRunDB.dungeon_run)
                .join(CharacterDB, CharacterDB.id == CharacterRunDB.character_id)
                .join(DiscordGuildCharacterDB, DiscordGuildCharacterDB.character_id == CharacterDB.id)
                .where(DungeonRunDB.id.in_(select(subquery_alias.c.id)))
                .order_by(desc(DungeonRunDB.score))
                .distinct()# Use a select() construct explicitly
            )

            result = await session.execute(query)
            result = result.unique()

            grouped_result = defaultdict(list)
            for dungeon_run, character in result:
                grouped_result[dungeon_run].append(character)

            dungeon_runs_with_characters = list(grouped_result.items())
            return dungeon_runs_with_characters
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None
    
async def get_all_weekly_guild_runs(discord_guild_id: int) -> Optional[DefaultDict[List[DungeonRunDB], List[CharacterDB]]]:
    try:
        async with async_session_scope() as session:
            subquery = (
                select(DungeonRunDB.id, DungeonRunDB.score)
                .join(DiscordGuildRunDB.dungeon_run)                
                .filter(DungeonRunDB.completed_at > datetime.utcnow() - timedelta(weeks=1), DiscordGuildRunDB.discord_guild_id == discord_guild_id)
                .order_by(desc(DungeonRunDB.score))
                
            )
            subquery_alias = subquery.subquery().alias()
            
            query = (
                select(DungeonRunDB, CharacterRunDB)
                .options(joinedload(DungeonRunDB.character_runs))
                .options(joinedload(CharacterRunDB.character))
                .join(CharacterRunDB.dungeon_run)
                .join(CharacterDB, CharacterDB.id == CharacterRunDB.character_id)
                .join(DiscordGuildCharacterDB, DiscordGuildCharacterDB.character_id == CharacterDB.id)
                .where(DungeonRunDB.id.in_(select(subquery_alias.c.id)))
                .order_by(desc(DungeonRunDB.score))
                .distinct()# Use a select() construct explicitly
            )

            result = await session.execute(query)
            result = result.unique()
            grouped_result = defaultdict(list)
            for dungeon_run, character in result:
                grouped_result[dungeon_run].append(character)

            dungeon_runs_with_characters = list(grouped_result.items())
            return dungeon_runs_with_characters
        
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None   

async def get_all_characters_by_game_guild(game_guild: GameGuildDB) -> Optional[List[CharacterDB]]:
    try:
        async with async_session_scope() as session:
            query = (
                select(CharacterDB)
                .join(DiscordGuildCharacterDB)
                .join(DiscordGuildDB)
                .join(GameGuildDB)
                .filter(GameGuildDB.id == game_guild.id)
            )
            result = await session.execute(query)
            return result.scalars().unique().all()
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_all_discord_guild_characters(discord_guild_id: int) -> Optional[List[CharacterDB]]:
    try:
        async with async_session_scope() as session:
            query = (
                select(CharacterDB)
                .options(joinedload(CharacterDB.discord_guild_characters))
                .join(DiscordGuildCharacterDB)
                .filter(DiscordGuildCharacterDB.discord_guild_id == discord_guild_id)
            )
            result = await session.execute(query)
            characters = result.scalars().unique().all()                   
            return characters
        
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None
    
async def get_characters_by_names_realms_and_discord_guild(names: List[str], realms: List[str], discord_guild_id: int) -> Optional[List[CharacterDB]]:
    try:
        async with async_session_scope() as session:
            query = (
                select(CharacterDB)
                .options(joinedload(CharacterDB.discord_guild_characters))
                .join(DiscordGuildCharacterDB)
                .filter(DiscordGuildCharacterDB.discord_guild_id == discord_guild_id,
                        CharacterDB.name.in_(names),
                        CharacterDB.realm.in_(realms))
            )
            result = await session.execute(query)
            characters = result.scalars().unique().all()
            
            for character in characters:
                character.discord_guild_characters = [dgc for dgc in character.discord_guild_characters if dgc.discord_guild_id == discord_guild_id]
                    
            return characters
        
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_all_game_guilds_by_discord_id(discord_guild_id: int) -> Optional[List[GameGuildDB]]:
    """Look up all game guilds associated with a specific discord guild in the database.

    Args:
        discord_guild_id (integer): The discord guild id to look up.

    Returns:
        existing_game_guilds: returns a list of game guild objects if found, otherwise returns None.
    """
    try:
        async with async_session_scope() as session:
            query = (
                select(GameGuildDB)
                .join(DiscordGameGuildDB)
                .filter(DiscordGameGuildDB.discord_guild_id == discord_guild_id)
            )
            result = await session.execute(query)
            existing_game_guilds = result.scalars().unique().all()
            
            return existing_game_guilds
        
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

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
            characters = result.scalars().unique().all()
            return characters
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_all_characters_in_guild_by_id(game_guild_id: int) -> List[CharacterDB]:
    """Get all of the characters in a guild from the database.

    Args:
        guild_id (int): The id of the guild to get the characters for.

    Returns:
        List[CharacterDB]: A list of the characters in the guild.
    """
    try:
        async with async_session_scope() as session:
            characters_query = (select(CharacterDB)
                                .join(CharacterDB.game_guild)
                                .filter(GameGuildDB.id == game_guild_id))
            result = await session.execute(characters_query)
            characters = result.scalars().unique().all()
            return characters
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
            
            return characters
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
            
            return characters
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
            return runs
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_all_run_ids() -> List[int]:
    """Get all of the run ids from the database.

    Returns:
        List[int]: A list of all of the run ids in the database.
    """
    try:
        async with async_session_scope() as session:
            runs_query = select(DungeonRunDB.dungeon_id)
            result = await session.execute(runs_query)
            runs = result.scalars().unique().all()            
            return runs
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None
    
async def get_all_run_ids_by_season(season: str) -> List[int]:
    """Get all of the run ids from the database.

    Returns:
        List[int]: A list of all of the run ids in the database.
    """
    try:
        async with async_session_scope() as session:
            runs_query = select(DungeonRunDB.dungeon_id).filter(DungeonRunDB.season == season)
            result = await session.execute(runs_query)
            runs = result.scalars().unique().all()            
            return runs
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
            
            return runs
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None
    
async def get_all_characters_for_run(run_id: int, season: str) -> List[CharacterRunDB]:
    """Get all characters for a run.

    Args:
        run (DungeonRunDB): The DungeonRunDB.py object to lookup in the database.

    Returns:
        List[CharacterRunDB]: Returns a list of CharacterRunDB.py objects if the character run exists, otherwise returns None.
    """
    try:
        async with async_session_scope() as session:
            
            query = select(DungeonRunDB).filter(DungeonRunDB.dungeon_id == run_id, DungeonRunDB.season == season)
            result = await session.execute(query)
            existing_run = result.scalar()
            
            if existing_run is None:
                return None
            
            else:
                
                existing_character_runs_query = select(CharacterRunDB).filter(CharacterRunDB.dungeon_run_id == existing_run.id)
                excresult = await session.execute(existing_character_runs_query)
                existing_character_runs = excresult.scalars().all()
                
                existing_characters = select(CharacterDB).filter(CharacterDB.id.in_([char.character_id for char in existing_character_runs]))
                ec_result = await session.execute(existing_characters)
                existing_characters = ec_result.scalars().unique().all()
                
                print(f'Found {len(existing_characters)} characters for run {run_id}')
                return existing_characters
                
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 

async def get_top10_runs_for_character_by_score(character: CharacterDB) -> Optional[DefaultDict[List[DungeonRunDB], List[CharacterDB]]]:
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
                
                existing_character_runs_query = (
                                            select(CharacterRunDB)
                                            .join(DungeonRunDB, CharacterRunDB.dungeon_run_id == DungeonRunDB.id)
                                            .filter(CharacterRunDB.character_id == existing_character.id)
                                            .order_by(DungeonRunDB.score.desc())
                                            .limit(10)
                                        )
                result = await session.execute(existing_character_runs_query)
                existing_character_runs = result.scalars().unique().all()
                
                if not existing_character_runs:
                    return None
                
                else:
                    
                    existing_runs_query = (
                        select(DungeonRunDB, CharacterDB)
                        .join(CharacterRunDB, DungeonRunDB.id == CharacterRunDB.dungeon_run_id)
                        .join(CharacterDB, CharacterRunDB.character_id == CharacterDB.id)
                        .filter(DungeonRunDB.id.in_([run.dungeon_run_id for run in existing_character_runs]))
                        .order_by(DungeonRunDB.score.desc())
                        )
                    result = await session.execute(existing_runs_query)
                    
                    grouped_result = defaultdict(list)
                    for dungeon_run, character in result:
                        grouped_result[dungeon_run].append(character)

                    dungeon_runs_with_characters = list(grouped_result.items())
                    return dungeon_runs_with_characters           
                                    
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 

async def get_top10_character_by_achievement(discord_guild_id: int) -> List[CharacterDB]:
    """Get the top 10 characters by achievement points.

    Returns:
        List[CharacterDB]: Returns a list of the top 10 characters by achievement points.
    """
    try:
        async with async_session_scope() as session:
            query = (
                select(CharacterDB)
                .join(DiscordGuildCharacterDB)
                .filter(DiscordGuildCharacterDB.discord_guild_id == discord_guild_id)
                .order_by(CharacterDB.achievement_points.desc())
                .limit(10)
                )            
            result = await session.execute(query)
            characters = result.scalars().unique().all()
            
            return characters
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 

async def get_top10_character_by_mythic_plus(discord_guild_id: int) -> List[CharacterDB]:
    """Get the top 10 characters by mythic plus score.

    Returns:
        List[CharacterDB]: Returns a list of the top 10 characters by mythic plus score.
    """
    try:
        async with async_session_scope() as session:
            query = (
                    select(CharacterDB)
                    .join(DiscordGuildCharacterDB)
                    .filter(DiscordGuildCharacterDB.discord_guild_id == discord_guild_id)
                    .order_by(CharacterDB.score.desc())
                    .limit(10)
                    )
            result = await session.execute(query)
            characters = result.scalars().unique().all()
            
            return characters
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 

async def get_top10_character_by_highest_item_level(discord_guild_id: int) -> List[CharacterDB]:
    """Get the top 10 characters by highest item level.

    Returns:
        List[CharacterDB]: Returns a list of the top 10 characters by highest item level.
    """
    try:
        async with async_session_scope() as session:
            
            query = (
                    select(CharacterDB)
                    .join(DiscordGuildCharacterDB)
                    .filter(DiscordGuildCharacterDB.discord_guild_id == discord_guild_id)
                    .order_by(CharacterDB.item_level.desc())
                    .limit(10)
                    )
            result = await session.execute(query)
            characters = result.scalars().unique().all()
            
            return characters
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None 

async def get_top10_guild_runs_this_week(discord_guild_id: int, season: str = 'season-df-2') -> Optional[DefaultDict[List[DungeonRunDB], List[CharacterDB]]]:
    try: 
        async with async_session_scope() as session:
            one_week_ago = datetime.now() - timedelta(weeks=1)
            
            top_runs_subquery = (
                select(DungeonRunDB.id)
                .join(DiscordGuildRunDB)
                .filter(DiscordGuildRunDB.discord_guild_id == discord_guild_id,
                        DungeonRunDB.num_keystone_upgrades >= 1,
                        DungeonRunDB.completed_at >= one_week_ago,
                        DungeonRunDB.season == season)
                .order_by(DungeonRunDB.score.desc()).limit(7)
            )
            
            subquery_alias = top_runs_subquery.subquery().alias()
            
            query = (
                select(DungeonRunDB, CharacterRunDB)
                .options(joinedload(DungeonRunDB.character_runs))
                .options(joinedload(CharacterRunDB.character))
                .join(CharacterRunDB.dungeon_run)
                .join(CharacterDB, CharacterDB.id == CharacterRunDB.character_id)
                .join(DiscordGuildCharacterDB, DiscordGuildCharacterDB.character_id == CharacterDB.id)
                .where(DungeonRunDB.id.in_(select(subquery_alias.c.id)))
                .order_by(desc(DungeonRunDB.score))
                .distinct()# Use a select() construct explicitly
            )

            result = await session.execute(query)
            result = result.unique()
            
            grouped_result = defaultdict(list)
            for dungeon_run, character in result:
                grouped_result[dungeon_run].append(character)

            dungeon_runs_with_characters = list(grouped_result.items())
            return dungeon_runs_with_characters
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None

async def get_top5_guild_runs_all_time(discord_guild_id: int, season: str = 'season-df-2') -> List[DungeonRunDB]:
    try: 
        async with async_session_scope() as session:
            
            top_runs_subquery = (
                select(DungeonRunDB.id)
                .join(DiscordGuildRunDB)
                .filter(DiscordGuildRunDB.discord_guild_id == discord_guild_id,
                        DungeonRunDB.num_keystone_upgrades >= 1,
                        DungeonRunDB.season == season)
                .order_by(DungeonRunDB.score.desc()).limit(7)
            ).alias("top_runs")
            
            
            
            query = (
                select(DungeonRunDB, CharacterDB)
                .join(top_runs_subquery, top_runs_subquery.c.id == DungeonRunDB.id)
                .join(CharacterRunDB, CharacterRunDB.dungeon_run_id == DungeonRunDB.id)
                .join(CharacterDB, CharacterRunDB.character_id == CharacterDB.id)
                .order_by(DungeonRunDB.score.desc()))
                
            result = await session.execute(query)
            
            grouped_result = defaultdict(list)
            for dungeon_run, character in result:
                grouped_result[dungeon_run].append(character)

            dungeon_runs_with_characters = list(grouped_result.items())
            return dungeon_runs_with_characters
  
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

async def check_run_for_guild_run(discord_guild_id: int, dungeon_run_id: int) -> Optional[DiscordGuildRunDB]:
    try: 
        async with async_session_scope() as session:
            
            dungeon_query = (
                select(DungeonRunDB.id)
                .filter(DungeonRunDB.dungeon_id == dungeon_run_id)
            )
            dungeon_run_result = await session.execute(dungeon_query)
            dungeon_run_id = dungeon_run_result.scalar()

            subquery = (
                select(CharacterRunDB.character_id)
                .filter(CharacterRunDB.dungeon_run_id == dungeon_run_id)
            )

            query = (
                select(func.count(DiscordGuildCharacterDB.character_id))
                .filter(
                    DiscordGuildCharacterDB.character_id.in_(subquery),
                    DiscordGuildCharacterDB.discord_guild_id == discord_guild_id)
            )
            guild_character_count = await session.execute(query)
            guild_character_count_value = guild_character_count.scalar()
            #print("Subquery result: ", guild_character_count_value)

            players_per_run = await session.execute(
                select(DiscordGuildDB.players_per_run)
                .filter(DiscordGuildDB.id == discord_guild_id)
            )

            players_per_run_value = players_per_run.scalar()

            if guild_character_count_value >= players_per_run_value:
                guild_run_exists = await session.execute(
                    select(DiscordGuildRunDB.id)
                    .filter(
                        DiscordGuildRunDB.discord_guild_id == discord_guild_id,
                        DiscordGuildRunDB.dungeon_run_id == dungeon_run_id)
                )
                guild_run_exists = guild_run_exists.scalars().first()
                if not guild_run_exists:
                    new_guild_run = DiscordGuildRunDB(discord_guild_id=discord_guild_id, dungeon_run_id=dungeon_run_id)
                    session.add(new_guild_run)
                    
                    print(f'New GuildRun created for guild ID {discord_guild_id} and run ID {dungeon_run_id}.')
                    return new_guild_run
                else:
                    #print(f'GuildRun already exists for guild ID {discord_guild_id} and run ID {dungeon_run_id}.')
                    return guild_run_exists
            else:
                #print(f'Not enough characters ({guild_character_count_value}/{players_per_run_value}) for guild ID {discord_guild_id} and run ID {dungeon_run_id}.')
                return None
    except SQLAlchemyError as error:
        print(f'Error while querying the database: {error}')
        return None
