
from datetime import datetime
import db
from objects.raiderIO.raiderIOService import RaiderIOService


class RaiderIOCrawler:
    def __init__():
        self = self

    def crawlCharacters():
        try:
            print('trying to crawl characters')
            characters = db.getAllCharacters()
            print(len(characters))
            for character in characters:
                if character.is_reporting == True:
                    print(character.name)
                    characterIO = RaiderIOService.getCharacter(character.name, character.realm)
                    print(characterIO.name)
                    for run in characterIO.best_runs:
                        if run != None:
                            print(run.id)
                            run.completed_at = datetime.strptime(run.completed_at,'%Y-%m-%dT%H:%M:%S.%fZ')
                            db.addDungeonRun(character, run)
                        else:
                            print("No best runs for " + character.name)
                    for run in characterIO.recent_runs:
                        if run != None:
                            run.completed_at = datetime.strptime(run.completed_at,'%Y-%m-%dT%H:%M:%S.%fZ')
                            db.addDungeonRun(character, run)
                        else:
                            print("No recent runs for " + character.name)
                    
                    
        except Exception as e:
            print(e)
            return False