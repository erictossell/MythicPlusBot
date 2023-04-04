from datetime import datetime
import time
import db
from objects.raiderIO.raiderIOService import RaiderIOService
from objects.raiderIO.member import Member

class RaiderIOCrawler:
    def __init__():
        self = self

    def crawlCharacters():
        try:
            print('trying to crawl characters')
            characters = db.getAllCharacters()            
            for character in characters:
                time.sleep(1)
                if character.is_reporting == True and character.score > 0:
                    
                    characterIO = RaiderIOService.getCharacter(character.name, character.realm)
                    
                    for run in characterIO.best_runs:
                        if run == None:
                            return
                        elif run != None and db.lookupRun(run.id) == None:
                            run.completed_at = datetime.strptime(run.completed_at,'%Y-%m-%dT%H:%M:%S.%fZ')
                            db.addDungeonRun(character, run)
                        else:
                            print("No best runs for " + character.name)
                    for run in characterIO.recent_runs:
                        if run == None:
                            return
                        elif run != None and db.lookupRun(run.id) == None:
                            run.completed_at = datetime.strptime(run.completed_at,'%Y-%m-%dT%H:%M:%S.%fZ')
                            db.addDungeonRun(character, run)
                        else:
                            print("No recent runs for " + character.name)
                                
        except Exception as e:
            print(e)
            return False
    
    def crawlGuildMembers():
        try: 
            print('trying to crawl guild members')
            members = RaiderIOService.getMembers()
            print(len(members))
            for member in members:
                time.sleep(1)
                if db.lookupCharacter(member.name, 'area-52') == None:
                    character = RaiderIOService.getCharacter(member.name, 'area-52')
                    if character == None:
                        print("Character not found: " + member.name)
                    else:
                        new_character = db.CharacterDB(173958345022111744, character.name, character.realm, character.faction, character.region, character.role, character.spec_name, character.class_name, character.achievement_points, character.item_level, character.score, character.rank, character.thumbnail_url, character.url, datetime.strptime(character.last_crawled_at,'%Y-%m-%dT%H:%M:%S.%fZ' ), True, [])
                        db.addCharacter(new_character) 
            
        except Exception as e:
            print(e)
            return False
        
    def crawlRuns():
        try:
           print('executing crawl runs')
        except Exception as e:
            print(e)
            return False         