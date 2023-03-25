from discord.ext import commands
from objects.createPollView import PollView

from objects.dice import Dice
from objects.myView import MyView
   
      
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
        await ctx.send('This is a button', view=view)
        
    @commands.command(name='testPoll', help='Sends a poll to the channel.')
    async def testPoll (self,ctx):
        print('testPoll command called')
        view = PollView()
        await ctx.send('This is a poll', view=view)
    
def setup(bot):
    bot.add_cog(generalCog(bot))