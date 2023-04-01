import discord

from objects.registration.registerModal import RegisterModal
from objects.registration.unregisterModal import UnregisterModal

class RegisterButton(discord.ui.View):    
    
    @discord.ui.button(label='Unregister', style=discord.ButtonStyle.red, emoji='🗑️')
    async def unregister_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        try: 
            await interaction.response.send_modal(UnregisterModal(title="Unregister your character"))
            
        except Exception as e:
            print('Error occured:', e)
            await interaction.message.delete()
            await interaction.response.send_message("Error occured while processing your request. Please try again later.", ephemeral=True)
    
    @discord.ui.button(label='Register', style=discord.ButtonStyle.green, emoji='📄')
    async def register_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:     
            await interaction.response.send_modal(RegisterModal(title="Register your character"))
            
            
        except Exception as e:
            print('Error occured:', e)
            await interaction.message.delete()
            await interaction.response.send_message("Error occured while processing your request. Please try again later.", ephemeral=True)