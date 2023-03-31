import csv
import discord

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
            userName = interaction.user.name
            
            if self.children[1].value == '':
                realm = 'Area-52'
            character = RaiderIOService.getCharacter(name, realm)
            
            if character == None:
                await interaction.response.send_message('Character '+ name +' on ' + realm + ' not found', ephemeral=True)
                return
            
            else:
                with open(filename, mode='r') as csv_file:
                    reader = csv.reader(csv_file, delimiter=',')
                    data = list(reader)
                    
                for row in data:
                    if row[0] == name and row[1] == realm and row[2] != str(userID):
                        
                        await interaction.response.send_message('You do not have permission to unregister this character. Contact an admin if you believe this is an error.', ephemeral=True)
                        break
                    elif row[0] == name and row[1] == realm and row[2] == str(userID):
                        data.remove(row)
                        with open(filename, mode='w', newline='') as csv_file:
                            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            writer.writerows(data)
                        
                        await interaction.response.send_message('You have unregistered the character ' + name + ' on realm ' + realm + ' for Tal-Bot reporting.', ephemeral=True)
                        break
                else:
                    
                    await interaction.response.send_message('This character is not registered.', ephemeral=True)
                    
                        
        except Exception as e:
            print(e)