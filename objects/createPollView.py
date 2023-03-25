import discord

from objects.myView import MyView

class PollView(discord.ui.View):
    @discord.ui.select(
        placeholder = 'Select a poll type',
        min_values = 1,
        max_values = 1,
        options = [
         discord.SelectOption(
             label= 'Yes/No',
             description= 'A simple yes/no poll',
         ),
         discord.SelectOption(
             label= 'Multiple Choice',
             description= 'A poll with multiple choices',
         ),
         discord.SelectOption(
             label= 'Rating',
             description = ('A poll with a rating scale')
         )   
            
        ]
    )
    async def select_poll_type(self, select, interaction):
        await interaction.response.send_message('You selected {}'.format(select.values[0]), view = MyView(), ephemeral=True)
        