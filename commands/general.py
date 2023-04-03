from discord.ext import commands
import db

from objects.dice import Dice
from objects.poll.createPollButton import CreatePollButton
from objects.raiderIO.raiderIOCrawler import RaiderIOCrawler


   
      
class generalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("General cog is initialized")
        
    @commands.command(name='ping', help='Pings the bot to see if it is online. (Latency in ms)')
    async def ping(self,ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
              

    @commands.command(name='roll', help='Rolls a dice with the specified number of sides.')
    async def roll(self,ctx, num_sides):
        try:
            dice = Dice(int(num_sides))
            await ctx.send(dice.roll())
        except Exception as e:
            await ctx.channel.send('@Eriim needs to fix this particular command :(')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !roll command: {e}')
    
        
    @commands.command(name='testPoll', help='Sends a poll to the channel.')
    async def testPoll (self,ctx):
        print('testPoll command called')
        view = CreatePollButton()
        await ctx.send('Take a Lap Discord Poll', view=view)
        
    @commands.command(name="crawl")
    async def crawl(self, ctx):
        print('crawl command called')
        RaiderIOCrawler.crawlCharacters()
    
    @commands.command(name="crawlRuns")
    async def crawlRuns(self, ctx):
        print('crawl runs command called')
        return
        
    
def setup(bot):
    bot.add_cog(generalCog(bot))