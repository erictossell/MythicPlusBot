from datetime import datetime
import time
import db
from objects.raiderIO.raiderIOService import RaiderIOService
from objects.raiderIO.raiderIOService import getScoreColors
from objects.raiderIO.member import Member

class RaiderIOCrawler:
    def __init__():
        self = self

    def crawlCharacters():
        try:
            print('trying to crawl characters')
            characters = db.getAllCharacters()            
            for character in characters:
                time.sleep(0.3)
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
        print('Crawler: trying to crawl guild members')
        try:             
            members = RaiderIOService.getMembers()
            counter = 0
            print(len(members))
            for member in members:
                print(member.name)              
                      
            for member in members:
                db_character = db.lookupCharacter(member.name, 'Area-52')
                time.sleep(0.3)
                
                print('Crawler: calling RIO Service for: ' + member.name)
                score_colors = getScoreColors()
                character = RaiderIOService.getCharacter(str(member.name), 'Area-52', score_colors)
                
                if character == None:
                    print("Crawler: Character not found: " + member.name)
                elif character != None and db_character == None:
                    print('Crawler: This is where I would add this character' + character.name)
                    new_character = db.CharacterDB(173958345022111744, character.name, character.realm, character.faction, character.region, character.role, character.spec_name, character.class_name, character.achievement_points, character.item_level, character.score, character.rank, character.thumbnail_url, character.url, datetime.strptime(character.last_crawled_at,'%Y-%m-%dT%H:%M:%S.%fZ' ), True, [])
                    print(type(new_character))
                    print(new_character)
                    db.addCharacter(new_character) 
                else:
                    print("Crawler: Character already exists: " + member.name)
                counter += 1    
                print(counter)        
        except Exception as e:
            print(e)
            return False
        finally:
            print('Crawler: finished crawling guild members')
    def crawlRuns():
        try:
           print('executing crawl runs')
        except Exception as e:
            print(e)
            return False         