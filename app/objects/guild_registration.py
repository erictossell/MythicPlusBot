import discord
from discord.ui import Button, View, Modal, InputText
import app.db as db


class RegisterGuildView(View):
    """Creates the register and unregister buttons."""

    def __init__(self, discord_guild_id: int, *args, **kwargs) -> None:
        """The constructor for the RegisterButton class.

        Args:
            discord_guild_id (int): The discord guild id.
        """
        super().__init__(*args, **kwargs)
        self.discord_guild_id = discord_guild_id       
        self.add_item(RegisterGuildButton(discord_guild_id=self.discord_guild_id))
        
   
class RegisterGuildButton(Button):
    def __init__(self, discord_guild_id: int):
        super().__init__(label='Register', style=discord.ButtonStyle.green, emoji='📄')
        self.discord_guild_id = discord_guild_id
        
    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_modal(RegisterGuildModal(title="Register your guild", discord_guild_id=self.discord_guild_id))
            
        except Exception as exception:
            print('Error occurred:', exception)
            await interaction.message.delete()
            await interaction.response.send_message("Error occurred while processing your request. Please try again later.", ephemeral=True)

class RegisterGuildModal(Modal):
    def __init__(self, discord_guild_id:int, *args, **kwargs) -> None:
        """The constructor for the RegisterModal class."""
        super().__init__(*args, **kwargs)
        self.discord_guild_id = discord_guild_id
        self.add_item(InputText(label="World of Warcraft Guild Name", required=True))
        self.add_item(InputText(label="Guild realm", required=True))
        self.add_item(InputText(label="Guild region", required=True))
        self.add_item(InputText(label="Announcement Channel ID", required=False))
        
    async def callback(self, interaction: discord.Interaction) -> None:
        """Register a guild to the database.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        try:
            wow_guild_name = self.children[0].value.capitalize()
            wow_realm = self.children[1].value.capitalize()
            wow_region = self.children[2].value.lower()
            announcement_channel_id = self.children[3].value
            if announcement_channel_id == '':
                announcement_channel_id = None
            
            if not wow_guild_name:
                await interaction.response.send_message("Guild name is required.", ephemeral=True)
                return
            elif not wow_realm:
                await interaction.response.send_message("Guild realm is required.", ephemeral=True)
                return
            elif not wow_region:
                await interaction.response.send_message("Guild region is required.", ephemeral=True)
                return
            else: 
                existing_guild = await db.get_discord_guild_by_id(int(self.discord_guild_id))
                if existing_guild:
                    
                    if announcement_channel_id is None:
                        updated_guild = db.DiscordGuildDB(id=int(self.discord_guild_id),
                                                      discord_guild_name=existing_guild.discord_guild_name,
                                                      wow_guild_name=wow_guild_name,
                                                      wow_realm=wow_realm,
                                                      wow_region=wow_region)
                    else:
                        updated_guild = db.DiscordGuildDB(id=int(self.discord_guild_id),
                                                      discord_guild_name=existing_guild.discord_guild_name,
                                                      wow_guild_name=wow_guild_name,
                                                      wow_realm=wow_realm,
                                                      wow_region=wow_region,
                                                      announcement_channel_id=int(announcement_channel_id))
                    await db.update_discord_guild(updated_guild)
                    
                    embed = discord.Embed(title=f"{updated_guild.discord_guild_name} WoW Guild Updated",
                                          description=f"Your guild has been updated to {updated_guild.wow_guild_name} - {updated_guild.wow_realm} in the {updated_guild.wow_region.upper()} region.",
                                          color=0x00ff00)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as exception:
            print('Error occurred:', exception)
            await interaction.message.delete()
            await interaction.response.send_message("Error occurred while processing your request. Please try again later.", ephemeral=True)