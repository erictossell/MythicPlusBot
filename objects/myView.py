import discord

from objects.myModal import MyModal

class MyView(discord.ui.View):
    @discord.ui.button(label='Click me!', style=discord.ButtonStyle.green, emoji='👍')
    async def my_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:            
            print('button clicked')    
            
            await interaction.response.send_modal(MyModal(title="You clicked the button!"))
            
        except Exception as e:
            print('Error occured:', e)
            await interaction.message.delete()
            await interaction.response.send_message("Error occured while processing your request. Please try again later.", ephemeral=True)     
   
   