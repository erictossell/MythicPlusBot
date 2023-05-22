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
SUPPORT_CHANNEL_ID = os.getenv('SUPPORT_CHANNEL_ID')

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Admin cog is initializing....")
        
    admin = SlashCommandGroup("admin", description="Admin commands for the bot.")
    
    @admin.command(name="register")
    async def register(self,ctx):
        """Register a World of Warcraft guild for reporting in this Discord Server.

        Args:
            ctx (context): The current discord context.
        """
        try:
            
            print('register command called')
            await ctx.respond(view=RegisterGuildView(discord_guild_id=ctx.guild.id))
        except Exception as e:
            print(e)
            await ctx.respond('Something went wrong :( Talk to Eriim about this error. ')
            error_channel = await ctx.bot.fetch_guild(int(SUPPORT_SERVER_ID)).fetch_channel(int(SUPPORT_CHANNEL_ID))           
           
            await error_channel.send(f'Error in !register command: {e}')
    
       
    @admin.command(name='set_announcement_channel')
    async def set_announcement_channel(self, ctx):
        """Set the channel you call this command in to be the announcement channel for your server.

        Args:
            ctx (_type_): _description_
        """
        discord_guild = await db.get_discord_guild_by_id(ctx.guild.id)
        
        if discord_guild is None:
            await ctx.respond('This command can only be used by admins within a Discord Server.')
            return

        discord_guild.announcement_channel_id = ctx.channel.id
        
        await db.update_discord_guild(discord_guild)
        
        await ctx.respond(f'Announcement channel set to {ctx.channel.name}.')
    
    @admin.command(name='disable_announcements')
    async def disable_announcements(self, ctx):
        """Turn off Mythic+ Bot announcements for this Discord Server.

        Args:
            ctx (context): the current discord context
        """
        discord_guild = await db.get_discord_guild_by_id(ctx.guild.id)
        
        if discord_guild is None:
            await ctx.respond('This command can only be used by admins within a Discord Server.')
            return

        discord_guild.announcement_channel_id = None
        
        await db.update_discord_guild(discord_guild)
        
        await ctx.respond('Announcements disabled.')    
    
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
        await guild.system_channel.send('Hello! I am Mythic+ Bot. I provide advanced Discord reporting for Mythic+ data.\nPlease go to https://www.mythicplusbot.dev/ if you would like guidance setting some of my features up 😊.') 
     
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            
            print(error)
            await ctx.respond('Something went wrong :( Talk to Eriim about this error. ')
            error_channel = await ctx.bot.fetch_guild(int(SUPPORT_SERVER_ID)).fetch_channel(int(SUPPORT_CHANNEL_ID))           
           
            await error_channel.send(f'Error in !register command: {error}')
            
def setup(bot):
    bot.add_cog(Admin(bot))    
    print("Admin cog is loaded successfully.")
    