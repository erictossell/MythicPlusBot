from datetime import datetime
import discord 
import db
import raiderIO as RaiderIO

filename = './members.csv'

class RegisterModal(discord.ui.Modal):
    """The modal that is used to register a character.

    Args:
        discord (ui.Modal): Represents a Discord modal.
    """
    def __init__(self, *args, **kwargs) -> None:
        """The constructor for the RegisterModal class.
        """
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="What is your character name?", required= True))
        self.add_item(discord.ui.InputText(label="Character realm: (Default is Area-52)", required= False))
        
    async def callback(self, interaction: discord.Interaction) -> None:
        """Call back for the register modal.

        Args:
            interaction (discord.Interaction): The interaction that was triggered.
        """
        try:
            name = self.children[0].value.capitalize()  
            realm = self.children[1].value.capitalize()
            userID = interaction.user.id
            
            if self.children[1].value == '':
                realm = 'Area-52'
            character = await RaiderIO.get_character(name, realm)
            existing_character = db.lookup_character(name, realm)            
                        
            if character is None:
                await interaction.response.send_message('Character '+ name +' on ' + realm + ' not found.', ephemeral=True)
                return 
            
            elif existing_character is None:
                new_character = db.CharacterDB(userID, character.name, character.realm, character.faction, character.region, character.role, character.spec_name, character.class_name, character.achievement_points, character.item_level, character.score, character.rank, character.thumbnail_url, character.url, datetime.strptime(character.last_crawled_at,'%Y-%m-%dT%H:%M:%S.%fZ' ), True, [])
                db.add_character(new_character)        
                await interaction.response.send_message('You have registered the character ' + new_character.name + ' on realm ' + new_character.realm + ' for Tal-Bot reporting.', ephemeral=True)
                return 
            elif existing_character.is_reporting is False:
                db.update_character_reporting(existing_character)
                await interaction.response.send_message('You have registered the character ' + existing_character.name + ' on realm ' + existing_character.realm + ' for Tal-Bot reporting.', ephemeral=True)
            else: 
                await interaction.response.send_message('The character ' + existing_character.name + ' on realm ' + existing_character.realm + ' has already been registered for Tal-Bot reporting.', ephemeral=True)                   
        except Exception as e:
            print(e)