import requests
import json
from util.binarySearch import binary_search_score_colors
from util.searchMembers import search_member
from objects.raiderIO.affix import Affix
from objects.raiderIO.characterIO import CharacterIO
from objects.raiderIO.dungeonRunIO import DungeonRun
from objects.raiderIO.scoreColor import ScoreColor
from objects.raiderIO.member import Member


def getScoreColors():
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
              
    def getCharacter(name, realm='Area-52'):
        region = 'us'        
        try:
            request = requests.get('https://raider.io/api/v1/characters/profile?region='+region+'&realm='+realm+'&name='+name+'&fields=gear,mythic_plus_scores_by_season:current,mythic_plus_ranks,mythic_plus_best_runs,mythic_plus_recent_runs') 
            scoreColors = getScoreColors()
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
            
            score_color = binary_search_score_colors(scoreColors, score)
            
            character = CharacterIO(
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
                request.json()['gear']['item_level_equipped'],
                score_color                
            )
            print('Character found: ' + character.name)            
        except:
            print('Error: Character not found.')
            return
        return character
                   
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
    
    def getGuildRun(id, season):
        try:
            request = requests.get('https://raider.io/api/v1/mythic-plus/run-details?season='+season+'&id='+id)
                
            data = json.loads(request.text)
            
            guildMemberCounter = 0
            
            for roster in data['roster']:                            
                if roster['guild']['id'] == 1616915:
                    guildMemberCounter += 1
                    print('Guild member found: ' + roster['character']['name'])
                elif search_member(roster['character']['name'], roster['character']['realm']):
                    guildMemberCounter += 1
                    print('Guild member found: ' + roster['character']['name'])
            if guildMemberCounter >= 5:
                print('Guild run found: ' + id)
                
                #run = DungeonRun(data['dungeon'], data['short_name'], data['mythic_level'], data['completed_at'], data['clear_time_ms'], data['par_time_ms'], data['num_keystone_upgrades'], data['score'], data['affixes'], data['url'])
                return True
                
            else:
                print('Guild run not found: ' + id)
                return None           
        except:
            print('Error: Run not found.')
            return