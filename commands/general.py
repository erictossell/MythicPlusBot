#---------------Take a Lap Discord Bot-----------------
# Description: This file contains the general commands for the bot.
# Author: Eriim

import time
import asyncio
from StringProgressBar import progressBar
from discord.ext import commands
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
    @commands.has_role("Guild Masters")   
    async def crawl(self, ctx):
        async with ctx.typing():
            print('crawl command called')
            start_time = time.time()
            await ctx.send('Crawling Raider.IO characters...')
            
            await RaiderIOCrawler.crawl_characters(ctx)
            end_time = time.time()
            elapsed_time = end_time - start_time
            await ctx.send('Finished crawling Raider.IO guild members for new runs after ' + str(elapsed_time) + ' seconds.')
    
    @commands.command(name="crawlGuild")
    @commands.has_role("Guild Masters")      
    async def crawlGuild(self, ctx):
        async with ctx.typing():
            print('crawl guild command called')
            start_time = time.time()
            await ctx.send('Crawling Raider.IO guild members...')
            
            result = await RaiderIOCrawler.crawl_guild_members()
            end_time = time.time()
            elapsed_time = end_time - start_time
            await ctx.send('Finished crawling Raider.IO guild members after ' + str(elapsed_time) + ' seconds.')
        
    @commands.command(name="crawlRuns")    
    @commands.has_role("Guild Masters")  
    async def crawlRuns(self, ctx):
        async with ctx.typing():
            print('crawl runs command called')
            await ctx.send('Crawling Raider.IO guild runs...')
            
            start_time = time.time()
            result = await RaiderIOCrawler.crawl_runs()
            end_time = time.time()
            elapsed_time = end_time - start_time
            await ctx.send('Finished crawling Raider.IO guild runs after ' + str(elapsed_time) + ' seconds.')
        
def setup(bot):
    bot.add_cog(generalCog(bot))