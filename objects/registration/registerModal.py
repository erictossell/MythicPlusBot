from datetime import datetime
import discord 
import csv
import db
from db import Session
from db import characterDB
from objects.raiderIO.raiderIOService import RaiderIOService
filename = './members.csv'

class RegisterModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="What is your character name?", required= True))
        self.add_item(discord.ui.InputText(label="Character realm: (Default is Area-52)", required= False))
        
    async def callback(self, interaction: discord.Interaction):
        
        try:
            name = self.children[0].value.capitalize()  
            realm = self.children[1].value.capitalize()
            userID = interaction.user.id
            userName = interaction.user.name
            
            if self.children[1].value == '':
                realm = 'Area-52'
            character = RaiderIOService.getCharacter(name, realm)
            existingCharacter = db.lookupCharacter(name, realm)
            if character == None:
                await interaction.response.send_message('Character '+ name +' on ' + realm + ' not found', ephemeral=True)
                return
            elif existingCharacter != None and existingCharacter.discord_user_id != userID:
                await interaction.response.send_message('Character '+ name +' on ' + realm + ' is already registered to another user', ephemeral=True)
                return
            elif existingCharacter != None:
                await interaction.response.send_message('Character '+ name +' on ' + realm + ' is already registered', ephemeral=True)
                return            
            else:                
                new_character = db.CharacterDB(userID, name, realm, character.faction, character.region, character.role, character.spec_name, character.class_name, character.achievement_points, character.item_level, character.score, character.rank, character.thumbnail_url, character.url, datetime.strptime(character.last_crawled_at,'%Y-%m-%dT%H:%M:%S.%fZ' ), True, [])
                        
                await interaction.response.send_message('You have registered the character ' + name + ' on realm ' + realm + ' for Tal-Bot reporting.', ephemeral=True)
                    
        except Exception as e:
            print(e)