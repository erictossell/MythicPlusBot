import os
from dotenv import load_dotenv
import time
from discord.ext import commands
from discord.commands import SlashCommandGroup
from app.objects.guild_registration import RegisterGuildView

import app.raiderIO as raiderIO
import app.db as db

load_dotenv('configurations/main.env')
SUPPORT_SERVER_ID = os.getenv('SUPPORT_SERVER_ID')
SUPPORT_SERVER_CHANNEL_ID = os.getenv('SUPPORT_SERVER_CHANNEL_ID')

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Admin cog is initializing....")
        
    admin = SlashCommandGroup("admin", description="Admin commands for the bot.")
    
    @admin.command(name="register")
    async def register(self,ctx):
        """This command registers the guild with the bot.

        Args:
            ctx (context): The current discord context.
        """
        try:
            print('register command called')
            await ctx.respond(view=RegisterGuildView(discord_guild_id=ctx.guild.id))
        except Exception as e:
            print(e)
            await ctx.respond('Something went wrong :( Talk to Eriim about this error. ')
            error_channel = await ctx.bot.fetch_guild(SUPPORT_SERVER_ID).fetch_channel(SUPPORT_SERVER_CHANNEL_ID)
           
            await error_channel.send(f'Error in !register command: {e}')
       
    @admin.command(name="crawl")    
    async def crawl(self, ctx):
        """Crawl the guild for new runs.

        Args:
            ctx (context): the current discord context.
        """
        discord_guild_id = int(ctx.guild.id)        
        async with ctx.typing():
            print('crawl command called')
            start_time = time.time()
            await ctx.respond('Crawling Raider.IO characters...')
            output = await raiderIO.crawl_characters(discord_guild_id)
            await ctx.respond(output)
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            await ctx.respond('Finished crawling Raider.IO guild members for new runs after ' + str(elapsed_time) + ' seconds.')
    
    @admin.command(name="crawlguild")
    async def crawl_guild(self, ctx):
        """Crawl the guild for new members.

        Args:
            ctx (context): The current discord context.
        """
        discord_guild_id = int(ctx.guild.id)        
        async with ctx.typing():
            print('crawl guild command called')
            start_time = time.time()
            await ctx.respond('Crawling Raider.IO guild members...')
            await raiderIO.crawl_guild_members(discord_guild_id)
            end_time = time.time()
            elapsed_time = end_time - start_time
            await ctx.respond('Finished crawling Raider.IO guild members after ' + str(elapsed_time) + ' seconds.')
    
    @admin.command(name="crawlruns")
    async def crawl_runs(self, ctx):
        """Compare runs to the database and update the database.

        Args:
            ctx (context): The current discord context.
        """
        discord_guild_id = int(ctx.guild.id) 
        async with ctx.typing():
            print('crawl runs command called')
            await ctx.respond('Crawling Raider.IO guild runs...')
            start_time = time.time()
            output = await raiderIO.crawl_runs(discord_guild_id)
            await ctx.respond(output)
            end_time = time.time()
            elapsed_time = end_time - start_time
            await ctx.respond('Finished crawling Raider.IO guild runs after ' + str(elapsed_time) + ' seconds.')
     
    @commands.Cog.listener()
    async def on_ready(self):
        print('Connected to Discord as {0.user}'.format(self.bot))
        await db.create_schema()
        for guild in self.bot.guilds:
            
            await db.add_discord_guild(db.DiscordGuildDB(id = guild.id, discord_guild_name=guild.name))
            print(f'{self.bot.user} is connected to the following guild:\n'
                  f'{guild.name}(id: {guild.id})')
            
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f'{self.bot.user} has joined the following guild:\n'
              f'{guild.name}(id: {guild.id})')
        await db.add_discord_guild(db.DiscordGuildDB(id = guild.id, discord_guild_name=guild.name))
        await guild.system_channel.send('Hello! I am a bot that tracks your guild\'s runs on Raider.IO. '
                                        'Type /help to see a list of commands.') 
     
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.respond('Something went wrong :( Talk to Eriim about this error. ')
            user = await ctx.bot.fetch_user(173958345022111744)
            channel = await user.create_dm()
            await channel.send(f'Error in !leaderboard command: {error}')
            
def setup(bot):
    bot.add_cog(Admin(bot))    
    print("Admin cog is loaded successfully.")
    