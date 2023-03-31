import discord 
import csv
from objects.raiderIO.raiderIOService import RaiderIOService
filename = './members.csv'

class RegisterModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="What is your character name?", required= True))
        self.add_item(discord.ui.InputText(label="What is your realm?", required= False))
        
    async def callback(self, interaction: discord.Interaction):
        
        try:
            name = self.children[0].value.capitalize()  
            realm = self.children[1].value.capitalize()
            if self.children[1].value == '':
                realm = 'Area-52'
            character = RaiderIOService.getCharacter(name, realm)
            
            if character == None:
                await interaction.response.send_message('Character '+ name +' on ' + realm + ' not found', ephemeral=True)
                return
            
            else:            
                with open(filename, mode='r')as csv_file:
                    reader = csv.reader(csv_file, delimiter=',')
                    for row in reader:
                        if row[0] == name and row[1] == realm:
                            await interaction.response.send_message(name + ' on realm ' + realm + ' has already been registered', ephemeral=True)
                            break
                    else:
                        with open(filename, mode='a', newline='') as csv_file:
                            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            writer.writerow([name, realm])            
                        await interaction.response.send_message('You have registered the character ' + name + ' on realm ' + realm, ephemeral=True)
                    
        except Exception as e:
            user = await self.ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !register command: {e}')