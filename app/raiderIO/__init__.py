import ssl
from tqdm import tqdm
from datetime import datetime
import re
import asyncio
from typing import List, Optional, Set
from ratelimit import limits, sleep_and_retry
import httpx

import app.db as db
from app.db.models.dungeon_run_db import DungeonRunDB
from app.raiderIO.models.affix import Affix
from app.raiderIO.models.character import Character
from app.raiderIO.models.dungeon_run import DungeonRun
from app.raiderIO.models.member import Member
from app import convert

from app.raiderIO.models.score_color import ScoreColor
import app.util as util

API_URL = 'https://raider.io/api/v1/'
CALLS = 200
RATE_LIMIT=60
TIMEOUT = 10
RETRIES = 5
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
                
                response = await client.get(API_URL + f'characters/profile?region={region}&realm={realm}&name={name}&fields=guild,gear,mythic_plus_scores_by_season:current,mythic_plus_ranks,mythic_plus_best_runs,mythic_plus_recent_runs', timeout=TIMEOUT) 
                
                if response.status_code == 404:
                    return 
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
                    spec_name = response.json()['active_spec_name']
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
                            affixes.append(Affix(name = affix['name'],
                                                 description= affix['description'],
                                                 wowhead_url= affix['wowhead_url']))
                        best_runs.append(DungeonRun(name = run['dungeon'],
                                                    short_name = run['short_name'],
                                                    mythic_level = run['mythic_level'],
                                                    completed_at = run['completed_at'],
                                                    clear_time_ms = run['clear_time_ms'],
                                                    par_time_ms = run['par_time_ms'],
                                                    num_keystone_upgrades = run['num_keystone_upgrades'],
                                                    score =run['score'],
                                                    affixes = affixes,
                                                    url = run['url']))
                    for run in response.json()['mythic_plus_recent_runs']:
                        affixes = []
                        for affix in run['affixes']:
                            affixes.append(Affix(name = affix['name'],
                                                 description= affix['description'],
                                                 wowhead_url= affix['wowhead_url']))
                        recent_runs.append(DungeonRun(name = run['dungeon'],
                                                    short_name = run['short_name'],
                                                    mythic_level = run['mythic_level'],
                                                    completed_at = run['completed_at'],
                                                    clear_time_ms = run['clear_time_ms'],
                                                    par_time_ms = run['par_time_ms'],
                                                    num_keystone_upgrades = run['num_keystone_upgrades'],
                                                    score =run['score'],
                                                    affixes = affixes,
                                                    url = run['url']))
                    if score_colors[0].score is None:
                        score_color = score_colors[0].color
                    elif score_colors is None:
                        score_color = '#c300ff'
                    else:
                        score_color = util.binary_search_score_colors(score_colors, int(score))
                    thumbnail_url = response.json()['thumbnail_url']
                    url = response.json()['profile_url']
                    last_crawled_at = response.json()['last_crawled_at']
                    character = Character(name = name,
                                          realm = realm,
                                          guild_name= guild_name,
                                          faction = faction,
                                          role = role,
                                          spec_name = spec_name,
                                          class_name = player_class,
                                          achievement_points= achievement_points,
                                          item_level= item_level,
                                          score = score,
                                          score_color=  score_color,
                                          rank= rank,
                                          best_runs= best_runs,
                                          recent_runs = recent_runs,
                                          thumbnail_url = thumbnail_url,
                                          url= url,
                                          last_crawled_at= last_crawled_at)
                    return character
                else:
                    print('Error: Character not found.')
                    return None       
            
        except (httpx.TimeoutException, httpx.ReadTimeout, ssl.SSLWantReadError):
            if retry == RETRIES - 1:
                raise
            else:
                await asyncio.sleep(BACKOFF_FACTOR * (2 ** retry))

        except Exception as exception:
            print(exception)
            return None

async def get_characters(names: List[str], realms: List[str], region='us') -> List[Optional[Character]]:
    if len(names) != len(realms):
        raise ValueError("names and realms lists must have the same length")

    characters = []
    score_colors = get_score_colors()

    for name, realm in tqdm(zip(names, realms)):
        retries = 3
        character = None
        while retries > 0:
            try:
                character = await get_character(name, realm, score_colors, region)
                characters.append(character)
                
            except (httpx.ReadTimeout, ssl.SSLWantReadError):
                    await asyncio.sleep(2 ** (3 - retries))
                    print(f'Retrying {name}-{realm}...')
                    retries -= 1
        
        if character is None:
            print(f'Error: {name}-{realm} not found.')
            continue           
        
        character = await get_character(name, realm, score_colors, region)
        characters.append(character)

    return characters

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
async def get_guild_members(name: str, realm: str, region: str ) -> Optional[List[Member]]:
    """Get a list of members from the Raider.IO API."""
    for retry in range(RETRIES):
        try:
            pattern = re.compile(r'^[^0-9]*$')
            members = []
            async with httpx.AsyncClient() as client:               
                
                request = await client.get(API_URL+f'guilds/profile?region={region}&realm={realm}&name={name}&fields=members')
                for member in request.json()['members']:
                    if pattern.search(str(member['character']['name'])):
                        realm = member['character']['profile_url'].split('/')[5]
                        members.append(Member(rank = member['rank'],
                                                name= str(member['character']['name']),
                                                class_name = member['character']['class'],
                                                last_crawled_at= member['character']['last_crawled_at'],
                                                profile_url= member['character']['profile_url'],
                                                realm = realm.capitalize()))
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
            return None

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
                    affixes.append(Affix(name = affix['name'],
                                         description= affix['description'],
                                         wowhead_url= affix['wowhead_url']))
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
async def get_run_details(dungeon_run: DungeonRun , discord_guild_id, players_per_run: int) -> Optional[bool]:
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
                    if request.json()['roster'] is None:
                        return False                    
                    
                    
                    dungeon_db = await db.get_run_by_id(int(dungeon_run.id), dungeon_run.season)
                                      
                    # Retrieve all characters involved in the run at once and store them in a dictionary
                    character_names = [str(roster['character']['name']).capitalize() for roster in request.json()['roster']]
                    character_realms = [str(roster['character']['realm']['slug']).capitalize() for roster in request.json()['roster']]
                    characters = await db.get_characters_by_names_realms_and_discord_guild(character_names, character_realms, discord_guild_id)
                    characters_dict = {(character.name, character.realm): character for character in characters}

                    guild_member_counter = 0
                    discord_guild_character_list = []
                    for roster in request.json()['roster']:
                        character_db = characters_dict.get((str(roster['character']['name']).capitalize(), str(roster['character']['realm']['slug']).capitalize()))

                        if character_db is not None:
                            guild_member_counter += 1
                            character_id = roster['character']['id']
                            spec_name = roster['character']['spec']['name']
                            role = roster['character']['spec']['role']
                            rank_world = roster['ranks']['world']
                            rank_region = roster['ranks']['region']
                            rank_realm = roster['ranks']['realm']
                            character_run = convert.character_run_io(character_db= character_db,
                                                            dungeon_run_db = dungeon_db,
                                                            rio_character_id = character_id,
                                                            spec_name = spec_name,
                                                            role = role,
                                                            rank_world = rank_world,
                                                            rank_region = rank_region,
                                                            rank_realm = rank_realm)
                            await db.add_character_run(character_run)
                            discord_guild_character = await db.get_discord_guild_character_by_name(discord_guild_id=discord_guild_id, name=character_db.name)
                            
                            discord_guild_character_list.append(discord_guild_character)
                    if guild_member_counter >= players_per_run:
                        
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
    """Crawl the Raider.IO API for a given discord guild to identify new discord_guild_runs.\n
    
    This method crawls all characters in a given discord guild and checks if they have any new runs.\n
    
    Any new runs are validated for guild membership and then added to the database.\n 
    """
    characters_crawled = 0
    run_counter = 0
    runs_crawled = 0
    update_character_counter = 0
    guild_run_counter = 0
    colors = get_score_colors()
    
    try:
        
        discord_guild = await db.get_discord_guild_by_id(discord_guild_id)
        db_characters_list = await db.get_all_discord_guild_characters(discord_guild_id)
        
        for character in db_characters_list:
                character.discord_guild_characters = [dgc for dgc in character.discord_guild_characters if dgc.discord_guild_id == discord_guild_id]
                
        runs = set()
        print('RaiderIO Crawler: Crawling ' + str(len(db_characters_list)) + ' characters.')
        for character in tqdm(db_characters_list):
            characters_crawled += 1

            if character.discord_guild_characters[0].is_reporting is False:
                continue
            character_io = None
            retries = 3
            while retries > 0:
                try:
                    character_io = await get_character(str(character.name),
                                                    str(character.realm),
                                                    colors)
                    break
                except (httpx.ReadTimeout, ssl.SSLWantReadError):
                    await asyncio.sleep(2 ** (3 - retries))
                    retries -= 1

            if character_io is None:
                print(f"Could not fetch character {character.name}. Skipping.")
                continue
            elif character.discord_guild_characters[0].is_reporting is False:
                print(f"Character {character.name} is not reporting. Skipping.")
                continue
            
            
            character.last_crawled_at = datetime.strptime(character_io.last_crawled_at,
                                                                '%Y-%m-%dT%H:%M:%S.%fZ')
            character.score = character_io.score
            character.item_level = character_io.item_level
            character.achievement_points = character_io.achievement_points
            character.spec_name = character_io.spec_name
            character.role = character_io.role
            character.rank = character_io.rank
            await db.update_character(character)
            update_character_counter += 1
            
            if character.item_level < 300:
                continue

            for run in character_io.best_runs:

                if run is None:
                    return f'Error: An error occurred while crawling {character.name} for new runs.'
                
                if run not in runs:
                    runs.add(run)                  
            for run in character_io.recent_runs:
                
                if run is None:
                    return f'Error: An error occurred while crawling {character.name} for new runs.'
                
                
                if run not in runs:
                    runs.add(run)
        
        if len(runs) > 0:

            season = runs.pop().season
            db_run_ids = await db.get_all_run_ids_by_season(season)
            
            db_run_id_set = set(db_run for db_run in db_run_ids)
            runs_id_set = set(int(run.id) for run in runs)
            
            new_run_ids = runs_id_set - db_run_id_set
            
            new_runs = [run for run in runs if int(run.id) in new_run_ids]
            
            for run in tqdm(new_runs):       
                
                if run is not None:               
                    
                    run.completed_at = datetime.strptime(run.completed_at,
                                                            '%Y-%m-%dT%H:%M:%S.%fZ')                            
                    db_run = await db.add_dungeon_run(convert.dungeon_run_io(run))
                    
                    run_counter += 1

                    is_guild_run = None
                    retries = 3
                    while retries > 0:
                        try:
                            is_guild_run = await get_run_details(run, discord_guild.id, discord_guild.players_per_run)
                            break
                        except (httpx.ReadTimeout, ssl.SSLWantReadError):
                            await asyncio.sleep(2 ** (3 - retries))
                            retries -= 1

                    if is_guild_run is None:
                        print(f"Could not fetch run details for run ID:{run}. Skipping.")
                        continue
                    
                    runs_crawled += 1
                    
                    if is_guild_run is True:
                        
                        db_run.is_crawled = True
                        db_run.is_guild_run = True
                        db_run = await db.update_dungeon_run(db_run)
                        await db.add_discord_guild_run(discord_guild=discord_guild,
                                                        dungeon_run=db_run)

                        guild_run_counter += 1

        return f'{discord_guild.discord_guild_name} Characters crawled: {characters_crawled} |  Updated {update_character_counter} characters and added {run_counter} runs and found {guild_run_counter} guild runs.'

    except Exception as exception:
        print(exception)
    finally:
        print('Finished crawling characters.')  

async def crawl_discord_guild_members(discord_guild_id) -> None:
    
    print('Crawler: trying to crawl guild members')
    try:
        
        score_colors_list = None
        retries = 3
        while retries > 0:
            try:
                score_colors_list = get_score_colors()
                break
            except (httpx.ReadTimeout, ssl.SSLWantReadError):
                await asyncio.sleep(2 ** (3 - retries))
                retries -= 1
               
        discord_guild = await db.get_discord_guild_by_id(discord_guild_id)
        game_guild_list = await db.get_all_game_guilds_by_discord_id(discord_guild_id)
        return_string = ""
        
        for game_guild in game_guild_list:
            
            discord_game_guild = await db.get_discord_game_guild_by_guild_ids(discord_guild_id, game_guild.id)

            if discord_game_guild is None or not discord_game_guild.is_crawlable:
                continue

            member_list = await get_guild_members(game_guild.name, game_guild.realm, game_guild.region)

            if member_list is None:
                continue
            
            db_member_list = await db.get_all_characters_by_game_guild(game_guild)
            
            # Convert member set and db_member_set to a set of tuples with name and realm
            member_set = {(member.name, member.realm) for member in member_list}
            db_member_set = {(character.name, character.realm) for character in db_member_list}

            # Find new members
            new_members = member_set - db_member_set

            counter = 0
            for new_member_name, new_member_realm in tqdm(new_members):
                new_member = next(member for member in member_set if (member.name, member.realm) == (new_member_name, new_member_realm))
                
                character = None
                retries = 5
                while retries > 0:
                    try:
                        character = await get_character(str(new_member.name),
                                                        str(new_member.realm),
                                                        score_colors_list)
                        break
                    except (httpx.ReadTimeout, ssl.SSLWantReadError):
                        await asyncio.sleep(2 ** (3 - retries))
                        retries -= 1

                if character is None:
                    print(f"Could not fetch character {new_member.name}. Skipping.")
                    continue
                                    
                new_character = db.CharacterDB(game_guild_id = game_guild.id,
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
                                                                    '%Y-%m-%dT%H:%M:%S.%fZ'))
                
                added_character = await db.add_character(new_character)
                
                if added_character is None:
                    character = await db.get_character_by_name_realm(character.name, character.realm)
                    await db.add_discord_guild_character(discord_guild=discord_guild, character=character)
                else:
                    await db.add_discord_guild_character(discord_guild=discord_guild,
                                                        character=added_character)
                    
                counter += 1
            return_string += f'Crawler: verified {counter}  characters to the database for the guild {game_guild.name}.\n'
        
        if return_string == "":
            return_string = "Crawler: no new characters were added to the database."
        return return_string
    except Exception as exception:
        print(exception)
        return False
    finally:
        print('Crawler: finished crawling guild members')
        