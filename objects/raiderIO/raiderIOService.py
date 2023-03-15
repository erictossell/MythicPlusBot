from discord import Member
import requests

import requests
from objects.raiderIO.affix import Affix
from objects.raiderIO.character import Character
from objects.raiderIO.dungeonRun import DungeonRun

from objects.raiderIO.scoreColor import ScoreColor

class RaiderIOService:
    def __init__(self):
        self = self  
        
    def getCharacter(name, realm='Area-52'):
        region = 'us'        
        try:
            request = requests.get('https://raider.io/api/v1/characters/profile?region='+region+'&realm='+realm+'&name='+name+'&fields=gear,mythic_plus_scores_by_season:current,mythic_plus_ranks,mythic_plus_best_runs,mythic_plus_recent_runs') 
            score = request.json()['mythic_plus_scores_by_season'][0]['scores']['all']
            best_runs = []
            recent_runs = []
            for run in request.json()['mythic_plus_best_runs']:
                affixes = []
                for affix in run['affixes']:
                    affixes.append(Affix(affix['name'], affix['description'], affix['wowhead_url']))
                best_runs.append(DungeonRun(run['dungeon'], run['short_name'], run['mythic_level'], run['completed_at'], run['clear_time_ms'], run['par_time_ms'], run['num_keystone_upgrades'], run['score'], affixes, run['url']))
            for run in request.json()['mythic_plus_recent_runs']:
                affixes = []
                for affix in run['affixes']:
                    affixes.append(Affix(affix['name'], affix['description'], affix['wowhead_url']))
                recent_runs.append(DungeonRun(run['dungeon'], run['short_name'], run['mythic_level'], run['completed_at'], run['clear_time_ms'], run['par_time_ms'], run['num_keystone_upgrades'], run['score'], affixes, run['url']))
            rank = request.json()['mythic_plus_ranks']['class']['realm']                        
            character = Character(
                request.json()['profile_url'],
                request.json()['name'],
                request.json()['realm'],
                request.json()['faction'],
                request.json()['class'],
                request.json()['active_spec_name'],
                request.json()['active_spec_role'],
                request.json()['thumbnail_url'],
                request.json()['achievement_points'],
                request.json()['last_crawled_at'],
                score,
                rank,
                best_runs,
                recent_runs,
                request.json()['gear']['item_level_equipped']
            )            
        except:
            print('Error: Character not found.')
            return
        return character
       
    
    def getScoreColors():
        scoreColors = []
        try:        
            request = requests.get('https://raider.io/api/v1/mythic-plus/score-colors')
            for score in request.json():
                scoreColors.append(ScoreColor(score['score'], score['color']))
        except:
            print('Error: Score colors not found.')
        return scoreColors   
        
                
    def getMembers():        
        try:
            members = []
            request = request.get('https://raider.io/api/v1/guilds/profile?region=us&realm=Area-52&name=Take%20A%20Lap&fields=members')
            for member in request.json()['members']:
                if member['rank'] > 8:
                    members.append(Member(member['rank'], member['name'], member['class'], member['last_crawled_at'], member['profile_url']))
        except:
            print('Error: Guild not found.')
            return
        return members  
              
            
    def getMythicPlusAffixes():
        try:        
            request = requests.get('https://raider.io/api/v1/mythic-plus/affixes?region=us&locale=en')        
            affixes = []
            for affix in request.json()['affix_details']:
                affixes.append(Affix(affix['name'], affix['description'], affix['wowhead_url']))            
        except:
            print('Error: Affixes not found.')
            return       
        return affixes 