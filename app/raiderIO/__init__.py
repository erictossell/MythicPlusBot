from tqdm import tqdm
from datetime import datetime
import re
import asyncio
from typing import List, Optional
from ratelimit import limits, sleep_and_retry
import httpx
from app import convert
import app.db as db
from app.db.models.dungeon_run_db import DungeonRunDB
from app.raiderIO.models.affix import Affix
from app.raiderIO.models.character import Character
from app.raiderIO.models.dungeon_run import DungeonRun
from app.raiderIO.models.member import Member

from app.raiderIO.models.score_color import ScoreColor
import app.util as util


API_URL = 'https://raider.io/api/v1/'
CALLS = 295
RATE_LIMIT=60
TIMEOUT = 10
RETRIES = 3
BACKOFF_FACTOR = 2

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def get_score_colors() -> List[ScoreColor]:
    """This method gets the score colors from the Raider.IO API.

    Returns:
        Optional[List[ScoreColor]]: Returns a list of ScoreColor objects or None if an error occurs.
    """
    score_colors = []
    for retry in range(RETRIES):
        try:
            with httpx.Client() as client:
                response = client.get('https://raider.io/api/v1/mythic-plus/score-tiers')
            
                for score in response.json():
                    score_colors.append(ScoreColor(score['score'], score['rgbHex'])) 
                return score_colors 
        except httpx.ReadTimeout:
                    print("Timeout occurred while fetching character data.")
                    
                    if retry == RETRIES - 1:
                        asyncio.sleep(BACKOFF_FACTOR ** retry)
                    else:
                        raise 
        except Exception as exception:
            print(exception)
            return None
    
@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
async def get_character(name: str,
                            realm='Area-52',
                            score_colors=get_score_colors(),
                            region='us') -> Optional[Character]:
    """Get a specific character from the Raider.IO API.

    Args:
        name (string): The name of the character.
        realm (str, optional): The realm of the character. Defaults to 'Area-52'.
        scoreColors (List[ScoreColor], optional): A list of the current score colors.
            Pass this value into the method to avoid making multiple requests to the Raider.IO API.
        
            Defaults to get_score_colors().

    Returns:
        Character: Returns a Character object or None if an error occurs.
    """   
    for retry in range(RETRIES):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(API_URL + 'characters/profile?region='+region+'&realm='+realm+'&name='+name+'&fields=guild,gear,mythic_plus_scores_by_season:current,mythic_plus_ranks,mythic_plus_best_runs,mythic_plus_recent_runs', timeout=TIMEOUT) 
                if response.status_code == 404:
                    return None
                elif response.status_code == 429:
                    return None 
                elif response.status_code == 500:
                    return None
                elif response.status_code == 200:
                    if response.json()['guild'] is None:
                        guild_name = None
                    else:
                        guild_name = response.json()['guild']['name']
                    faction = response.json()['faction'] 
                    role = response.json()['active_spec_role']
                    spec = response.json()['active_spec_name']
                    player_class = response.json()['class']
                    achievement_points = response.json()['achievement_points']
                    item_level = response.json()['gear']['item_level_equipped']    
                    score = response.json()['mythic_plus_scores_by_season'][0]['scores']['all']
                    rank = response.json()['mythic_plus_ranks']['class']['realm']
                    best_runs = []
                    recent_runs = []
                    for run in response.json()['mythic_plus_best_runs']:
                        affixes = []
                        for affix in run['affixes']:
                            affixes.append(Affix(affix['name'],
                                                    affix['description'],
                                                    affix['wowhead_url']))
                        best_runs.append(DungeonRun(run['dungeon'],
                                                    run['short_name'],
                                                    run['mythic_level'],
                                                    run['completed_at'],
                                                    run['clear_time_ms'],
                                                    run['par_time_ms'],
                                                    run['num_keystone_upgrades'],
                                                    run['score'],
                                                    affixes, run['url']))
                    for run in response.json()['mythic_plus_recent_runs']:
                        affixes = []
                        for affix in run['affixes']:
                            affixes.append(Affix(affix['name'],
                                                    affix['description'],
                                                    affix['wowhead_url']))
                        recent_runs.append(DungeonRun(run['dungeon'],
                                                        run['short_name'],
                                                        run['mythic_level'],
                                                        run['completed_at'],
                                                        run['clear_time_ms'],
                                                        run['par_time_ms'],
                                                        run['num_keystone_upgrades'],
                                                        run['score'],
                                                        affixes,
                                                        run['url']))
                    score_color = util.binary_search_score_colors(score_colors, int(score))
                    thumbnail = response.json()['thumbnail_url']
                    url = response.json()['profile_url']
                    last_crawled_at = response.json()['last_crawled_at']
                    character = Character(name,
                                            realm,
                                            guild_name,
                                            faction,
                                            role,
                                            spec,
                                            player_class,
                                            achievement_points,
                                            item_level,
                                            score,
                                            score_color,
                                            rank,
                                            best_runs,
                                            recent_runs,
                                            thumbnail,
                                            url,
                                            last_crawled_at)
                    return character    
                else:
                    print('Error: Character not found.')
                    return None
        except httpx.ReadTimeout:
            print("Timeout occurred while fetching character data.")
            
            if retry == RETRIES - 1:
                await asyncio.sleep(2 ** retry)
            else:
                raise
            
        except Exception as exception:
            print(exception)
            return None

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
async def get_members(discord_guild_id: int ) -> Optional[List[Member]]:
    """Get a list of members from the Raider.IO API."""
    for retry in range(RETRIES):
        try:
            discord_guild = await db.get_discord_guild_by_id(discord_guild_id)
            pattern = re.compile(r'^[^0-9]*$')
            members = []
            async with httpx.AsyncClient() as client:        
                request = await client.get(API_URL+f'guilds/profile?region={discord_guild.wow_region}&realm={discord_guild.wow_realm}&name={discord_guild.wow_guild_name}&fields=members')
                for member in request.json()['members']:
                    if member['rank'] <= 8:    
                        if pattern.search(str(member['character']['name'])):
                            members.append(Member(member['rank'],
                                                    str(member['character']['name']),
                                                    member['character']['class'],
                                                    member['character']['last_crawled_at'],
                                                    member['character']['profile_url']))
                if len(members) > 0:
                    return members
                elif len(members) == 0:
                    return None
        except httpx.ReadTimeout:
                    print("Timeout occurred while fetching character data.")
                    
                    if retry == RETRIES - 1:
                        await asyncio.sleep(BACKOFF_FACTOR ** retry)
                    else:
                        raise 
        except Exception as e:
            print(e)
            print('Error: Guild not found.')
        finally:
            print('Finished grabbing members.')

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
async def get_mythic_plus_affixes() -> Optional[List[Affix]]:
    """Get a list of affixes from the Raider.IO API.

    Returns:
        Optional[List[Affix]]: Returns a list of affixes or none if an error occurs.
    """
    for retry in range(RETRIES):
        try:
            async with httpx.AsyncClient() as client:
                request = await client.get(API_URL+'mythic-plus/affixes?region=us&locale=en')
                affixes = []
                for affix in request.json()['affix_details']:
                    affixes.append(Affix(affix['name'],
                                            affix['description'],
                                            affix['wowhead_url']))
                if len(affixes) > 0:
                    return affixes
                else:
                    return None
        except httpx.ReadTimeout:
                print("Timeout occurred while fetching character data.")
                
                if retry == RETRIES - 1:
                    await asyncio.sleep(BACKOFF_FACTOR ** retry)
                else:
                    raise 
        except Exception as exception:
            print(exception)
            return None    

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
async def get_run_details(dungeon_run : DungeonRunDB) -> Optional[bool]:
    """Get a guild run from the Raider.IO API.

    Args:
        id (int): The RaiderIO id of the run.
        season (string): A string representing the season. 
        Examples: 'season-bfa-4'
                    'season-df-1'

    Returns:
        Optional[bool]: True if a guild run is found, False if not.
    """
    for retry in range(RETRIES):
        try:
            async with httpx.AsyncClient() as client:
                request = await client.get(API_URL +f'mythic-plus/run-details?season={dungeon_run.season}&id={dungeon_run.id}', timeout=TIMEOUT)
                if request.status_code != 200:
                    return None
                elif request.status_code == 200:
                    guild_member_counter = 0
                    if request.json()['roster'] is None:
                        return False
                    for roster in request.json()['roster']:                    
                        character_db = await db.get_character_by_name_realm(roster['character']['name'],
                                                            roster['character']['realm']['slug'])                      
                        if character_db is not None:
                            guild_member_counter += 1
                            character_id = roster['character']['id']
                            spec_name = roster['character']['spec']['name']
                            role = roster['character']['spec']['role']
                            rank_world = roster['ranks']['world']
                            rank_region = roster['ranks']['region']
                            rank_realm = roster['ranks']['realm']
                            character_run = convert.character_run_io(character_db= character_db,
                                                            dungeon_run_db = dungeon_run,
                                                            rio_character_id = character_id,
                                                            spec_name = spec_name,
                                                            role = role,
                                                            rank_world = rank_world,
                                                            rank_region = rank_region,
                                                            rank_realm = rank_realm)
                            await db.add_character_run(character_run)
                            
                    if guild_member_counter >= 4:
                        return True
                    else:
                        return False
        except httpx.ReadTimeout:
                print("Timeout occurred while fetching character data.")
                
                if retry == RETRIES - 1:
                    await asyncio.sleep(BACKOFF_FACTOR ** retry)
                else:
                    raise      
        except Exception as exception:
            print('RaiderIO : Error: ' + exception)
            return None   

async def crawl_characters(discord_guild_id: int) -> str:
    """Crawl the Raider.IO API for new data on characters in the database.\n
    This method has a 0.3 second delay between each API call to avoid rate limiting.
    This method will only crawl characters with a score greater than 0
    and that rows that are flagged for reporting.
    """
    characters_crawled = 0
    run_counter = 0
    update_character_counter = 0
    colors = get_score_colors()
    try:
        
        characters_list = await db.get_all_characters_in_guild_by_id(int(discord_guild_id))
        print('RaiderIO Crawler: Crawling ' + str(len(characters_list)) + ' characters.')
        for character in tqdm(characters_list):
            characters_crawled += 1
            if character.is_reporting is True:
                character_io = await get_character(name=character.name,
                                                    realm=character.realm,
                                                    score_colors=colors)
                if not character_io:
                    return f'Error: An error occurred while crawling {character.name}'
                for run in character_io.best_runs:
                    if run is None:
                        return f'Error: An error occurred while crawling {character.name}'
                    if run is not None and await db.get_run_by_id(int(run.id)) is None:
                        run.completed_at = datetime.strptime(run.completed_at,
                                                                '%Y-%m-%dT%H:%M:%S.%fZ')
                        await db.add_dungeon_run(convert.dungeon_run_io(run))
                        run_counter += 1
                   
                for run in character_io.recent_runs:
                    if run is None:
                        return f'Error: An error occurred while crawling {character.name}'
                    elif run is not None and await db.get_run_by_id(int(run.id)) is None:
                        run.completed_at = datetime.strptime(run.completed_at,
                                                                '%Y-%m-%dT%H:%M:%S.%fZ')
                        await db.add_dungeon_run(convert.dungeon_run_io(run))
                        run_counter += 1
                    
                if character.name == character_io.name and character.realm == character_io.realm:
                
                    character.last_crawled_at = datetime.strptime(character_io.last_crawled_at,
                                                                    '%Y-%m-%dT%H:%M:%S.%fZ')
                    character.score = character_io.score
                    character.item_level = character_io.item_level
                    character.achievement_points = character_io.achievement_points
                    character.spec_name = character_io.spec_name
                    character.role = character_io.role
                    character.rank = character_io.rank
                    character.discord_guild_id = discord_guild_id
                    character.guild_name = character_io.guild_name
                    await db.update_character(character)
                    update_character_counter += 1
        return f'Characters crawled: {characters_crawled} |  Updated {update_character_counter} characters and added {run_counter} runs.'
    
    except Exception as exception:
        print(exception)
    finally:
        print('Finished crawling characters.')  

async def crawl_guild_members(discord_guild_id) -> None:
    """Crawl the Raider.IO API for new guild members. \n
    This method has a 0.3 second delay between each API call to avoid rate limiting.
    """
    print('Crawler: trying to crawl guild members')
    try:   
        score_colors_list = get_score_colors()          
        members_list = await get_members(discord_guild_id)
        counter = 0
        print('RaiderIO Crawler: Crawling ' + str(len(members_list)) + ' guild members.')
        for member in tqdm(members_list):
            db_character = await db.get_character_by_name_realm(member.name, 'Area-52')
            if db_character is None:
                
                character = await get_character(str(member.name),
                                                                'Area-52', score_colors_list)
                new_character = db.CharacterDB(discord_user_id=173958345022111744,
                                                discord_guild_id = discord_guild_id,
                                                guild_name = character.guild_name,
                                                name = character.name,
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
                                                last_crawled_at = datetime.strptime(character.last_crawled_at,
                                                                    '%Y-%m-%dT%H:%M:%S.%fZ'),
                                                is_reporting = True)  
                await db.add_character(new_character)
                counter += 1
    except Exception as exception:
        print(exception)
        return False
    finally:
        print('Crawler: finished crawling guild members')

async def crawl_runs(discord_guild_id: int) -> str:
    """Crawl all runs in the database that have not been crawled.\n

    Args:
        discord_guild_id (int): The guild ID of the discord server.

    Returns:
        str: The result of the crawl.
    """
    runs_crawled = 0
    guild_run_counter = 0
    try:
        runs_list = await db.get_all_runs_not_crawled()
        if runs_list is None:
            return 'No runs to crawl.'
        print('RaiderIO Crawler: Crawling runs.')
        for run in tqdm(runs_list):
            is_guild = await get_run_details(run)
            runs_crawled += 1
            if is_guild is True:
                announcement = db.AnnouncementDB(discord_guild_id=discord_guild_id,
                                                announcement_channel_id=1074546599239356498,
                                                title=f'🧙‍♂️ New guild run: {run.mythic_level} - {run.name} on {run.completed_at}',
                                                content=f'**{run.name}** completed on {run.completed_at} by Take a Lap.\n\n**Dungeon:** {run.short_name}\n**Score:** {run.score}\n**URL:** {run.url}',
                                                dungeon_run_id=run.id)
                print(f"Created announcement with dungeon_run_id: {announcement.dungeon_run_id}")  # Print statement to verify dungeon_run_id
                await db.add_announcement(announcement)
                run.is_crawled = True
                run.is_guild_run = True
                await db.update_dungeon_run(run)
                
                guild_run_counter += 1
            else:
                run.is_crawled = True
                run.is_guild_run = False
                await db.update_dungeon_run(run)
             
        return f'Runs crawled: {runs_crawled}  | Identified {guild_run_counter} guild runs.'
    except Exception as exception:
        print(exception)
        return 'Error: An error occurred while crawling runs.'
