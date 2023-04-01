import time
import requests
import csv

from objects.raiderIO.raiderIOService import RaiderIOService
membersFile = './members.csv'
guildRunsFile = './guild_runs_queue.csv'
class RaiderIOCrawler():
    def __init__(self):
        self = self
        
    def crawl_members():
        
        with open(membersFile, mode='r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            data = list(reader)
            
            for row in data: 
                name = row[0]
                realm = row[1]
                print(name,realm)
                character = RaiderIOService.getCharacter(name, realm)
                for run in character.best_runs:
                    print(run.name)
                    print(run.mythic_level)                    
                    print(run.url)
                    print(run.id)
                    print('-------------------------')
                    with open(guildRunsFile, mode='a', newline='') as csv_file:
                        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow([run.id, run.season, run.name, run.mythic_level, run.url])
                
    
    def crawl_runs():
        with open(guildRunsFile, mode='r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            data = list(reader)            
            for row in data:
                time.sleep(1)
                runID = row[0]
                runSeason = row[1]               
                
                if RaiderIOService.getGuildRun(runID,runSeason) != None:
                    print('Guild Run')
                    with open('guild_runs.csv', mode='a', newline='') as csv_file:
                        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow([row[0], row[1], row[2], row[3], row[4]])
                    
                
                           
        
        

