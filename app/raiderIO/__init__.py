import asyncio
from tqdm import tqdm
from datetime import datetime
import re
from typing import List, Optional

import requests
import app.db as db
from app.db.models.dungeon_run_db import DungeonRunDB
from app.raiderIO.models.affix import Affix
from app.raiderIO.models.character import Character
from app.raiderIO.models.dungeon_run import DungeonRun
from app.raiderIO.models.member import Member

from app.raiderIO.models.score_color import ScoreColor
import app.util as util

API_URL = 'https://raider.io/api/v1/'

def get_score_colors() -> Optional[List[ScoreColor]]:
    """This method gets the score colors from the Raider.IO API.

    Returns:
        Optional[List[ScoreColor]]: Returns a list of ScoreColor objects or None if an error occurs.
    """
    score_colors = []
    try:        
        response = requests.get('https://raider.io/api/v1/mythic-plus/score-tiers')
        for score in response.json():
            score_colors.append(ScoreColor(score['score'], score['rgbHex'])) 
        return score_colors 
    except Exception as exception:
        print(exception)
        return None

async def get_character(name: str,
                            realm='Area-52',
                            scoreColors=get_score_colors(),
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
    #print('RIO Service: Looking up character: ' + name)            
    try:
        response = requests.get(API_URL + 'characters/profile?region='+region+'&realm='+realm+'&name='+name+'&fields=guild,gear,mythic_plus_scores_by_season:current,mythic_plus_ranks,mythic_plus_best_runs,mythic_plus_recent_runs') 
        if response.status_code == 404:
            #print('Character not found: ' + name)
            return None
        elif response.status_code == 429:
            #print('Too many requests.')
            return None 
        elif response.status_code == 500:
            #print('Internal server error.')
            return None
        elif response.status_code == 200:
            #print('RIO Service: 200')
            guild_name = response.json()['guild']['name']
            faction = response.json()['faction'] 
            #print('Faction: ' + faction)
            role = response.json()['active_spec_role']
            #print('Role: ' + str(role))          
            spec = response.json()['active_spec_name']
            #print('Spec: ' + spec)
            playerClass = response.json()['class']
            #print('Class: ' + playerClass)
            achievementPoints = response.json()['achievement_points']
            #print('Achievement Points: ' + str(achievementPoints))
            item_level = response.json()['gear']['item_level_equipped']    
            #print('Item Level: ' + str(item_level))            
            score = response.json()['mythic_plus_scores_by_season'][0]['scores']['all']
            #print('Score: ' + str(score))
            rank = response.json()['mythic_plus_ranks']['class']['realm']
            #print('Rank: ' + str(rank))
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
            #print('Best Runs: ' + str(len(best_runs)))
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
            #print('Recent Runs: ' + str(len(recent_runs)))
            score_color = util.binary_search_score_colors(scoreColors, int(score))
            #print('Score Color: ' + score_color)
            thumbnail = response.json()['thumbnail_url']
            #print('Thumbnail: ' + thumbnail)
            url = response.json()['profile_url']
            #print('URL: ' + url)
            last_crawled_at = response.json()['last_crawled_at']
            #print('Last Crawled At: ' + last_crawled_at)              
            character = Character(name,
                                    realm,
                                    guild_name,
                                    faction,
                                    role,
                                    spec,
                                    playerClass,
                                    achievementPoints,
                                    item_level,
                                    score,
                                    score_color,
                                    rank,
                                    best_runs,
                                    recent_runs,
                                    thumbnail,
                                    url,
                                    last_crawled_at)
            #print('Character found: ' + character.name)
            return character    
        else:
            print('Error: Character not found.')
            return None   
    except Exception as exception:
        print(exception)
        return None

async def get_members() -> Optional[List[Member]]:
    """Get a list of members from the Raider.IO API."""    
    try:
        pattern = re.compile(r'^[^0-9]*$')
        members = []           
        request = requests.get(API_URL+'guilds/profile?region=us&realm=Area-52&name=Take%20A%20Lap&fields=members')
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
    except Exception as e:
        print(e)
        print('Error: Guild not found.')
    finally:
        print('Finished grabbing members.')

async def get_mythic_plus_affixes() -> Optional[List[Affix]]:
    """Get a list of affixes from the Raider.IO API.

    Returns:
        Optional[List[Affix]]: Returns a list of affixes or none if an error occurs.
    """
    try:        
        request = requests.get(API_URL+'mythic-plus/affixes?region=us&locale=en')
        affixes = []
        for affix in request.json()['affix_details']:
            affixes.append(Affix(affix['name'],
                                    affix['description'],
                                    affix['wowhead_url']))
        if len(affixes) > 0:
            return affixes
        else:
            #print('Error: No affixes found.')
            return None
    except Exception as exception:
        print(exception)
        return None    

async def get_run_details(run_id: int, season: str):
    """Get a specific run's details from the Raider.IO API.
    """    
    try:
        request = requests.get(API_URL+f'mythic-plus/run-details?season={season}&id={run_id}')
        #print(request.json())
        
    except Exception as exception:
        print(exception)

async def is_guild_run(dungeon_run : DungeonRunDB) -> Optional[bool]:
    """Get a guild run from the Raider.IO API.

    Args:
        id (int): The RaiderIO id of the run.
        season (string): A string representing the season. 
        Examples: 'season-bfa-4'
                    'season-df-1'

    Returns:
        Optional[bool]: True if a guild run is found, False if not.
    """
    try:
        request = requests.get(API_URL +f'mythic-plus/run-details?season={dungeon_run.season}&id={dungeon_run.id}')
        if request.status_code != 200:
            #print('RaiderIO : Error: Run not found.')
            return None
        elif request.status_code == 200:
            guild_member_counter = 0
            if request.json()['roster'] is None:
                #print('RaiderIO : No roster found for run: ' + str(run_id))
                return False
            for roster in request.json()['roster']:                    
                #print('is_Guild_Run: Searching for ' + roster['character']['name'])
                character_db = db.lookup_character(roster['character']['name'],
                                                    roster['character']['realm']['slug'])                      
                if character_db is not None:
                    guild_member_counter += 1
                    #print('RaiderIO : Guild member found: ' + roster['character']['name'])
                    db.add_character_run(character_db, dungeon_run)
            if guild_member_counter >= 4:
                #print('RaiderIO : Guild run found: ' + str(run_id))
                return True
            else:
                #print('RaiderIO : Guild run not found: ' + str(run_id))
                return False           
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
    try:
        #print('trying to crawl characters')        
        characters_list = db.get_all_characters()
        print('RaiderIO Crawler: Crawling ' + str(len(characters_list)) + ' characters.')
        for character in tqdm(characters_list):
            await asyncio.sleep(0.2)
            characters_crawled += 1
            if character.is_reporting is True:
                character_io = await get_character(character.name,
                                                    character.realm)
                for run in character_io.best_runs:
                    if run is None:
                        return f'Error: An error occurred while crawling {character.name}'
                    if run is not None and db.lookup_run(run.id) is None:
                        #print('Adding run: ' + str(run.id))
                        run.completed_at = datetime.strptime(run.completed_at,
                                                                '%Y-%m-%dT%H:%M:%S.%fZ')
                        db.add_dungeon_run(run)
                        run_counter += 1
                   
                for run in character_io.recent_runs:
                    if run is None:
                        return f'Error: An error occurred while crawling {character.name}'
                    elif run is not None and db.lookup_run(run.id) is None:
                        #print('Adding run: ' + str(run.id))
                        run.completed_at = datetime.strptime(run.completed_at,
                                                                '%Y-%m-%dT%H:%M:%S.%fZ')
                        db.add_dungeon_run(run)
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
                    db.update_character(character)
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
        members_list = await get_members()
        counter = 0
        print('RaiderIO Crawler: Crawling ' + str(len(members_list)) + ' guild members.')
        for member in tqdm(members_list):
            db_character = db.lookup_character(member.name, 'Area-52')
            if db_character is None:
                #print('Crawler: Character already in database: ' + member.name)                
                #print('Crawler: calling RIO Service for: ' + member.name)
                score_colors_list = get_score_colors()
                character = await get_character(str(member.name),
                                                                'Area-52', score_colors_list)
                new_character = db.CharacterDB(173958345022111744,
                                                discord_guild_id,
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
                                                datetime.strptime(character.last_crawled_at,
                                                                    '%Y-%m-%dT%H:%M:%S.%fZ'),
                                                True)  
                db.add_character(new_character)
                counter += 1
                await asyncio.sleep(0.2)
                #print(f'Crawler: Character number: {counter} has been crawled.')
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
        runs_list = db.get_all_runs_not_crawled()
        if runs_list is None:
            return 'No runs to crawl.'
        print('RaiderIO Crawler: Crawling runs.')
        for run in tqdm(runs_list):
            await asyncio.sleep(0.2)
            is_guild = await is_guild_run(run)
            runs_crawled += 1
            if is_guild is True:
                run.is_guild_run = True
                db.update_dungeon_run(run)
                announcement = db.AnnouncementDB(discord_guild_id=discord_guild_id,
                                                guild_name='Take a Lap',
                                                announcement_channel_id=1074546599239356498,
                                                title=f'🧙‍♂️ New guild run:{run.mythic_level} - {run.name} on {run.completed_at}',
                                                description=f'**{run.name}** completed on {run.completed_at} by Take a Lap.\n\n**Dungeon:** {run.short_name}\n**Score:** {run.score}\n**URL:** {run.url}',
                                                message="Message",
                                                dungeon_run_id=run.id)
                print(f"Created announcement with dungeon_run_id: {announcement.dungeon_run_id}")  # Print statement to verify dungeon_run_id
                db.add_announcement(announcement)

                guild_run_counter += 1
            else:
                run.is_guild_run = False
                db.update_dungeon_run(run)  
        #print('Finished crawling runs.')
        return f'Runs crawled: {runs_crawled}  | Identified {guild_run_counter} guild runs.'
    except Exception as exception:
        print(exception)
        return 'Error: An error occurred while crawling runs.'
