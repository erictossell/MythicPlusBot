import requests

class getMythicPlusAffixes:
    def __init__(self):
        self.region = 'us'
        self.affixes = requests.get('https://raider.io/api/v1/mythic-plus/affixes?region='+self.region)
        self.affixes = self.affixes.json()['affix_details']
        
    def getAffixes(self):
        return self.affixes