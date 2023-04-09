import asyncio
from datetime import datetime
import time
import db

from objects.raiderIO.raiderIOService import RaiderIOService
from objects.raiderIO.raiderIOService import get_score_colors
from objects.raiderIO.member import Member
from StringProgressBar import progressBar

class RaiderIOCrawler:
    def __init__():
        self = self

    async def crawl_characters(ctx):
        try:
            print('trying to crawl characters')
            
            characters_list = db.get_all_characters()
                     
            for character in characters_list:
                await asyncio.sleep(0.3)
                if character.is_reporting == True and character.score > 0:
                    
                    character_io = await RaiderIOService.get_character(character.name, character.realm)
                    
                    for run in character_io.best_runs:
                        if run == None:
                            return
                        elif run != None and db.lookup_run(run.id) == None:
                            run.completed_at = datetime.strptime(run.completed_at,'%Y-%m-%dT%H:%M:%S.%fZ')
                            db.add_dungeon_run(character, run)
                        else:
                            print("No best runs for " + character.name)
                    for run in character_io.recent_runs:
                        if run == None:
                            return
                        elif run != None and db.lookup_run(run.id) == None:
                            run.completed_at = datetime.strptime(run.completed_at,'%Y-%m-%dT%H:%M:%S.%fZ')
                            db.add_dungeon_run(character, run)
                        else:
                            print("No recent runs for " + character.name)
                            
        except Exception as e:
            print(e)
            return False
    
    async def crawl_guild_members():
        print('Crawler: trying to crawl guild members')
        try:             
            members_list = await RaiderIOService.get_members()
            counter = 0
            print(len(members_list))
            for member in members_list:
                print(member.name)              
                      
            for member in members_list:
                db_character = db.lookup_character(member.name, 'Area-52')
                await asyncio.sleep(0.3)
                
                print('Crawler: calling RIO Service for: ' + member.name)
                score_colors_list = await get_score_colors()
                character = await RaiderIOService.get_character(str(member.name), 'Area-52', score_colors_list)
                
                if character == None:
                    print("Crawler: Character not found: " + member.name)
                elif character != None and db_character == None:
                    print('Crawler: This is where I would add this character' + character.name)
                    new_character = db.CharacterDB(173958345022111744, character.name, character.realm, character.faction, character.region, character.role, character.spec_name, character.class_name, character.achievement_points, character.item_level, character.score, character.rank, character.thumbnail_url, character.url, datetime.strptime(character.last_crawled_at,'%Y-%m-%dT%H:%M:%S.%fZ' ), True, [])
                    print(type(new_character))
                    print(new_character)
                    db.add_character(new_character) 
                else:
                    print("Crawler: Character already exists: " + member.name)
                counter += 1    
                print(counter)        
        except Exception as e:
            print(e)
            return False
        finally:
            print('Crawler: finished crawling guild members')
    def crawl_runs():
        try:
           print('executing crawl runs')
        except Exception as e:
            print(e)
            return False         