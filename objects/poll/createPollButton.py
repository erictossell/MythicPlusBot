import discord
from objects.poll.createPollModal import CreatePollModal

class CreatePollButton(discord.ui.View):
    """Generate the create poll button.

    Args:
        discord (ui.View): Provides the parent class for the view.
    """
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, emoji='✖️')
    async def cancel_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        """When the cancel button is clicked, delete the message.

        Args:
            button (discord.ui.Button): Provides the parent class for the button.
            interaction (discord.Interaction): Provides the parent class for the interaction.
        """
        try:            
            print('button clicked')   
            await interaction.message.delete()
        except Exception as e:
            print('Error occured:', e)
            await interaction.message.delete()
            await interaction.response.send_message("Error occured while processing your request. Please try again later.", ephemeral=True)
    @discord.ui.button(label='Create Poll', style=discord.ButtonStyle.green, emoji='📄')
    async def createPoll_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        """When the create poll button is clicked, open the create poll modal.

        Args:
            button (discord.ui.Button): Provides the parent class for the button.
            interaction (discord.Interaction): Provides the parent class for the interaction.
        """
        try:
            print('button clicked')    
            
            await interaction.response.send_modal(CreatePollModal(title="Create a Poll"))

        except Exception as e:
            print('Error occured:', e)
            await interaction.message.delete()
            await interaction.response.send_message("Error occured while processing your request. Please try again later.", ephemeral=True)
            