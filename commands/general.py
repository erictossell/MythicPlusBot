import discord
from discord.ext import commands

from objects.dice import Dice

class MyView(discord.ui.View):
    @discord.ui.button(label='Click me!', style=discord.ButtonStyle.green, emoji='👍')
    async def my_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:            
            print('button clicked')        
            await interaction.response.send_message("You clicked the button!")
            await interaction.message.delete()
        except Exception as e:
            print('Error occured:', e)
            await interaction.message.delete()
            await interaction.response.send_message("Error occured while processing your request. Please try again later.")     
      
      
class generalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("General cog is initialized")
        
    @commands.command(name='ping', help='Pings the bot to see if it is online. (Latency in ms)')
    async def ping(self,ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
              

    @commands.command(name='roll', help='Rolls a dice with the specified number of sides.')
    async def roll(self,ctx, num_sides):
        dice = Dice(int(num_sides))
        await ctx.send(dice.roll())
    
    @commands.command(name='button', help='Sends a button to the channel.')
    async def button(self,ctx):
        print('button command called')
        view = MyView()
        
        #view.add_item(discord.ui.Button(label='Click me!', style=discord.ButtonStyle.green, emoji='👍'))        
        await ctx.send('This is a button', view=view)
    
def setup(bot):
    bot.add_cog(generalCog(bot))