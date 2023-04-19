from datetime import datetime
import discord
from discord.ui import Button, View, Modal, InputText
import app.db as db
import app.raiderIO as raiderIO

class RegisterView(View):
    """Creates the register and unregister buttons."""

    def __init__(self, discord_guild_id: int, *args, **kwargs) -> None:
        """The constructor for the RegisterButton class.

        Args:
            discord_guild_id (int): The discord guild id.
        """
        super().__init__(*args, **kwargs)
        self.discord_guild_id = discord_guild_id
        
        self.add_item(UnregisterButton())
        self.add_item(RegisterButton(discord_guild_id=self.discord_guild_id))

class UnregisterButton(Button):
    def __init__(self):
        super().__init__(label='Unregister', style=discord.ButtonStyle.red, emoji='🗑️')
        
    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_modal(UnregisterModal(title="Unregister your character"))
        except Exception as exception:
            print('Error occurred:', exception)
            await interaction.message.delete()
            await interaction.response.send_message("Error occurred while processing your request. Please try again later.", ephemeral=True)

class RegisterButton(Button):
    def __init__(self, discord_guild_id: int):
        super().__init__(label='Register', style=discord.ButtonStyle.green, emoji='📄')
        self.discord_guild_id = discord_guild_id
        
    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_modal(RegisterModal(title="Register your character", discord_guild_id=self.discord_guild_id))
        except Exception as exception:
            print('Error occurred:', exception)
            await interaction.message.delete()
            await interaction.response.send_message("Error occurred while processing your request. Please try again later.", ephemeral=True)

class RegisterModal(Modal):
    """The modal that is used to register a character."""

    def __init__(self, discord_guild_id:int, *args, **kwargs) -> None:
        """The constructor for the RegisterModal class."""
        super().__init__(*args, **kwargs)
        self.discord_guild_id = discord_guild_id
        self.add_item(InputText(label="What is your character name?", required=True))
        self.add_item(InputText(label="Character realm: (Default is Area-52)", required=False))
        
    async def callback(self, interaction: discord.Interaction) -> None:
        """Callback for the register modal.

        Args:
            interaction (discord.Interaction): The interaction that was triggered.
        """
        try:
            name = self.children[0].value.capitalize()  
            realm = self.children[1].value.capitalize() if self.children[1].value else 'Area-52'
            user_id = interaction.user.id
            
            character = await raiderIO.get_character(name, realm)
            existing_character = db.lookup_character(name, realm)
                        
            if character is None:
                await interaction.response.send_message(f'Character {name} on {realm} not found.', ephemeral=True)
                return
            
            elif existing_character is None:
                new_character = db.CharacterDB(
                    user_id, self.discord_guild_id, character.guild_name,
                    character.name, character.realm.lower(), character.faction,
                    character.region, character.role, character.spec_name,
                    character.class_name, character.achievement_points,
                    character.item_level, character.score, character.rank,
                    character.thumbnail_url, character.url,
                    datetime.strptime(character.last_crawled_at, '%Y-%m-%dT%H:%M:%S.%fZ'), True)
                                               
                db.add_character(new_character)
                await interaction.response.send_message(f'You have registered the character {new_character.name} on realm {new_character.realm.capitalize()} for Tal-Bot reporting.', ephemeral=True)
                return

            elif not existing_character.is_reporting:
                db.update_character_reporting(existing_character)
                await interaction.response.send_message(f'You have registered the character {existing_character.name} on realm {existing_character.realm.capitalize()} for Tal-Bot reporting.', ephemeral=True)
            else:
                await interaction.response.send_message(f'The character {existing_character.name} on realm {existing_character.realm.capitalize()} has already been registered for Tal-Bot reporting.', ephemeral=True)                   
        except Exception as e:
            print(e)
            
class UnregisterModal(Modal):
    """The modal that is used to unregister a character."""

    def __init__(self, *args, **kwargs) -> None:
        """The constructor for the UnregisterModal class."""
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Which character do you want to unregister?", required=True))
        self.add_item(InputText(label="Character Realm: (Defaults to Area-52)", required=False))
        
    async def callback(self, interaction: discord.Interaction) -> None:
        """The callback for the unregister modal.

        Args:
            interaction (discord.Interaction): A Discord interaction.
        """
        try:
            name = self.children[0].value.capitalize()
            realm = self.children[1].value.capitalize() if self.children[1].value else 'Area-52'
            user_id = interaction.user.id           
            
            character = raiderIO.get_character(name, realm)
            
            if character is None:
                await interaction.response.send_message(f'Character {name} on {realm} not found', ephemeral=True)
                return

            existing_character = db.lookup_character(name, realm)

            if existing_character is None:
                await interaction.response.send_message('This character is not registered.', ephemeral=True)
                return

            if existing_character.discord_user_id != user_id:                        
                await interaction.response.send_message('You do not have permission to unregister this character. Contact an admin if you believe this is an error.', ephemeral=True)
                return

            if existing_character.discord_user_id == user_id and existing_character.is_reporting:
                existing_character.is_reporting = False  
                db.update_character_reporting(existing_character)                
                await interaction.response.send_message(f'You have unregistered the character {name} on realm {realm} for Tal-Bot reporting.', ephemeral=True)
                return

            if existing_character.discord_user_id == user_id and not existing_character.is_reporting:
                await interaction.response.send_message('This character is not registered.', ephemeral=True)
                return

            await interaction.response.send_message('An unexpected error has occurred, contact Eriim with a timestamp.', ephemeral=True)
                         
        except Exception as e:
            print(e)