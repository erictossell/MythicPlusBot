import requests

class getMythicPlusBestRuns:
    def __init__(self, name, realm):
        self.region = 'us'
        self.realm = realm
        self.name = name        
        self.character = requests.get('https://raider.io/api/v1/characters/profile?region='+self.region+'&realm='+self.realm+'&name='+self.name+'&fields=mythic_plus_best_runs')
        self.bestRuns = self.character.json()['mythic_plus_best_runs']
        self.url = self.character.json()['profile_url']         
        
        self.region = self.character.json()['region']
        self.faction = self.character.json()['faction']
        self.class_name = self.character.json()['class']
        self.spec_name = self.character.json()['active_spec_name']
        self.role = self.character.json()['active_spec_role']
        self.thumbnail_url = self.character.json()['thumbnail_url']
        self.achievement_points = self.character.json()['achievement_points']
        self.last_crawled_at = self.character.json()['last_crawled_at']
        
    def getBestRuns(self):
        return self.bestRuns