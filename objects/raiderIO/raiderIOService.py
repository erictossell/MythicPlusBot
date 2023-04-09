import re
import requests

import json
from util.binarySearch import binary_search_score_colors
from util.searchMembers import search_member
from objects.raiderIO.affix import Affix
from objects.raiderIO.character import Character
from objects.raiderIO.dungeonRun import DungeonRun
from objects.raiderIO.scoreColor import ScoreColor
from objects.raiderIO.member import Member


def get_score_colors():
        scoreColors = []
        try:        
            request = requests.get('https://raider.io/api/v1/mythic-plus/score-tiers')            
            for score in request.json():
                scoreColors.append(ScoreColor(score['score'], score['rgbHex'])) 
        except:
            print('Error: Score colors not found.')
        return scoreColors    
    
class RaiderIOService:
    def __init__(self):
        self = self
                
    async def get_character(name, realm='Area-52', scoreColors=get_score_colors()):
        region = 'us'
        print('RIO Service: Looking up character: ' + name)
               
        try:
            request = requests.get('https://raider.io/api/v1/characters/profile?region='+region+'&realm='+realm+'&name='+name+'&fields=gear,mythic_plus_scores_by_season:current,mythic_plus_ranks,mythic_plus_best_runs,mythic_plus_recent_runs') 
            if request.status_code == 200:
                print('RIO Service: 200')
                faction = request.json()['faction'] 
                print('Faction: ' + faction)
                role = request.json()['active_spec_role']
                print('Role: ' + role)          
                spec = request.json()['active_spec_name']
                print('Spec: ' + spec)
                playerClass = request.json()['class']
                print('Class: ' + playerClass)
                achievementPoints = request.json()['achievement_points']
                print('Achievement Points: ' + str(achievementPoints))
                item_level = request.json()['gear']['item_level_equipped']    
                print('Item Level: ' + str(item_level))            
                score = request.json()['mythic_plus_scores_by_season'][0]['scores']['all']
                print('Score: ' + str(score))
                rank = request.json()['mythic_plus_ranks']['class']['realm']
                print('Rank: ' + str(rank))
                best_runs = []
                recent_runs = []
                for run in request.json()['mythic_plus_best_runs']:
                    affixes = []
                    for affix in run['affixes']:
                        affixes.append(Affix(affix['name'], affix['description'], affix['wowhead_url']))
                    best_runs.append(DungeonRun(run['dungeon'], run['short_name'], run['mythic_level'], run['completed_at'], run['clear_time_ms'], run['par_time_ms'], run['num_keystone_upgrades'], run['score'], affixes, run['url']))
                #print('Best Runs: ' + str(len(best_runs)))
                for run in request.json()['mythic_plus_recent_runs']:
                    affixes = []
                    for affix in run['affixes']:
                        affixes.append(Affix(affix['name'], affix['description'], affix['wowhead_url']))
                    recent_runs.append(DungeonRun(run['dungeon'], run['short_name'], run['mythic_level'], run['completed_at'], run['clear_time_ms'], run['par_time_ms'], run['num_keystone_upgrades'], run['score'], affixes, run['url']))
                #print('Recent Runs: ' + str(len(recent_runs)))
                
                score_color = binary_search_score_colors(scoreColors, int(score))
                print('Score Color: ' + score_color)
                thumbnail = request.json()['thumbnail_url']
                print('Thumbnail: ' + thumbnail)
                url = request.json()['profile_url']
                print('URL: ' + url)
                last_crawled_at = request.json()['last_crawled_at']
                print('Last Crawled At: ' + last_crawled_at)              
                
                character = Character(name,realm, faction, role, spec, playerClass, achievementPoints, item_level, score, score_color, rank, best_runs, recent_runs,thumbnail, url, last_crawled_at )
                print('Character found: ' + character.name)
                return character
            elif request.status_code == 404:
                print('Character not found: ' + name)
                return None
            elif request.status_code == 429:
                print('Too many requests.')
                return None 
            elif request.status_code == 500:
                print('Internal server error.')
                return None        
            else:
                print('Error: Character not found.')
                return None   
        except Exception as e:
            print(e)
            return None
                     
    async def get_members():        
        try:
            pattern = re.compile(r'^[^0-9]*$')
            members = []           
            request = requests.get('https://raider.io/api/v1/guilds/profile?region=us&realm=Area-52&name=Take%20A%20Lap&fields=members')
            for member in request.json()['members']:
                if member['rank'] <= 8:    
                    if pattern.search(str(member['character']['name'])):
                        members.append(Member(member['rank'], str(member['character']['name']), member['character']['class'], member['character']['last_crawled_at'], member['character']['profile_url']))
                    else:                     
                        print('Found a character with a number in the name ' + member['character']['name'])
        except Exception as e:
            print(e)
            print('Error: Guild not found.')
        finally:
            print('Finished grabbing members.')
            return members
              
    async def get_mythic_plus_affixes():
        try:        
            request = requests.get('https://raider.io/api/v1/mythic-plus/affixes?region=us&locale=en')        
            affixes = []
            for affix in request.json()['affix_details']:
                affixes.append(Affix(affix['name'], affix['description'], affix['wowhead_url']))            
        except:
            print('Error: Affixes not found.')
            return       
        return affixes 
    
    async def get_guild_run(id, season):
        try:
            request = requests.get('https://raider.io/api/v1/mythic-plus/run-details?season='+season+'&id='+id)
                
            data = json.loads(request.text)
            
            guild_member_counter = 0
            
            for roster in data['roster']:                            
                if roster['guild']['id'] == 1616915:
                    guild_member_counter += 1
                    print('Guild member found: ' + roster['character']['name'])
                elif search_member(roster['character']['name'], roster['character']['realm']):
                    guild_member_counter += 1
                    print('Guild member found: ' + roster['character']['name'])
            if guild_member_counter >= 5:
                print('Guild run found: ' + id)
                
                #run = DungeonRun(data['dungeon'], data['short_name'], data['mythic_level'], data['completed_at'], data['clear_time_ms'], data['par_time_ms'], data['num_keystone_upgrades'], data['score'], data['affixes'], data['url'])
                return True
                
            else:
                print('Guild run not found: ' + id)
                return None           
        except:
            print('Error: Run not found.')
            return