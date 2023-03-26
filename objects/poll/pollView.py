import discord

class PollView(discord.ui.View):          
    
    @discord.ui.select(
        placeholder = 'Select a poll type',
        min_values = 1,
        max_values = 1,
        options = [
        discord.SelectOption(
            label= 'Yes/No',
            description= 'Yes or No',
        ),
        discord.SelectOption(
            label= 'Multiple Choice',
            description=    'Multiple Choice',
        )               
        ]
    )
    async def select_poll_option(self, select, interaction):
        await interaction.response.send_message('You voted for {}'.format(select.values[0]))
        