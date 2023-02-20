from discord.ext import commands
from objects.dice import Dice

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
  
async def setup(bot):
    await bot.add_cog(generalCog(bot))