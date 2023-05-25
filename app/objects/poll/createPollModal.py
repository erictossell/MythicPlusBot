import discord

class CreatePollModal(discord.ui.Modal):
    """This is a modal that allows users to create a poll.

    Args:
        discord (ui.Modal): Inherets the parent class Modal.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="What are you polling for?", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Option 1", required= True))
        self.add_item(discord.ui.InputText(label="Option 2", required= True))
        self.add_item(discord.ui.InputText(label="Option 3", required= False))
        self.add_item(discord.ui.InputText(label="Option 4", required = False))

    async def callback(self, interaction: discord.Interaction) -> None:  
        """This is the callback function that is called when the modal is submitted."""
        embed = discord.Embed(title=self.children[0].value, color=discord.Color.green(), description='Poll created by ' + interaction.user.mention)     
        
        for i, child in enumerate(self.children[1:]):           
            if child.value:
                embed.add_field(name=chr(0x1F1E6 + i), value=child.value)
                
        message = await interaction.channel.send(embed=embed)
               
        for i, child in enumerate(self.children[1:]):
            if child.value:
                await message.add_reaction(chr(0x1F1E6 + i))
        
        await interaction.response.send_message('Vote now!')
                
       
                