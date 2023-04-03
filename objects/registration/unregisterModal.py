import csv
import discord
import db


from objects.raiderIO.raiderIOService import RaiderIOService
filename = './members.csv'
class UnregisterModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
        self.add_item(discord.ui.InputText(label="Which character do you want to unregister?", required= True))
        self.add_item(discord.ui.InputText(label="Character Realm: (Defaults to Area-52)", required= False))
        
    async def callback(self, interaction: discord.Interaction):
        try:
            name = self.children[0].value.capitalize()
            realm = self.children[1].value.capitalize()
            userID = interaction.user.id           
            
            if self.children[1].value == '':
                realm = 'Area-52'
            character = RaiderIOService.getCharacter(name, realm)
            
            if character == None:
                await interaction.response.send_message('Character '+ name +' on ' + realm + ' not found', ephemeral=True)
                return
            existingCharacter = db.lookupCharacter(name, realm)                    
            if existingCharacter == None:
                await interaction.response.send_message('This character is not registered.', ephemeral=True)
                return
            elif existingCharacter.discord_user_id != userID:                        
                await interaction.response.send_message('You do not have permission to unregister this character. Contact an admin if you believe this is an error.', ephemeral=True)
                return               
            
            elif existingCharacter.discord_user_id == userID:
                existingCharacter.is_reporting = False  
                db.updateCharacterReporting(existingCharacter)                
                await interaction.response.send_message('You have unregistered the character ' + name + ' on realm ' + realm + ' for Tal-Bot reporting.', ephemeral=True)
                return
            
            else:
                await interaction.response.send_message('An unexpected error has occured, contact Eriim with a time stamp.', ephemeral=True)
                
                    
                    
                    
                        
        except Exception as e:
            print(e)