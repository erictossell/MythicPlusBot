
import asyncio
from discord.ext import commands, tasks
from datetime import time
import app.db as db
from app.objects.embed_builder import announce_guild_run_embed
import app.raiderIO as raiderIO
import app.util as util


class Announcement(commands.Cog):
    """This cog contains commands for announcements.

    Args:
        commangs (_type_): _description_
    """
    def __init__(self, bot):
        self.bot = bot
        print("Announcement cog is initializing....")
       
        self.announcement_task = self.bot.loop.create_task(self.send_announcements())
        self.crawl_task = self.bot.loop.create_task(self.crawl_for_data())
        self.is_closed = bot.is_closed

    @tasks.loop(time=time(hour=22, minute=5, second=0))
    async def send_announcements(self):
        await self.bot.wait_until_ready()
        
        
        await asyncio.sleep(600)
        while not self.is_closed():
            
            for guild in self.bot.guilds:
                
                discord_guild_db = await db.get_discord_guild_by_id(guild.id)
                
                if discord_guild_db is None:
                    await db.add_discord_guild(db.DiscordGuildDB(id = guild.id,
                                                                 discord_guild_name = guild.name))
            
                elif discord_guild_db.is_announcing is False:
                    continue
                
                elif discord_guild_db.announcement_channel_id is None:
                    continue
                
                announcement = await db.get_next_announcement_by_guild_id(guild.id)
                
                if announcement is None:
                    print("No announcement found.")
                    await asyncio.sleep(300)
                    continue
                
                else:
                    characters_list = await db.get_all_characters_for_run(announcement.dungeon_run.id)
                    
                    embed = announce_guild_run_embed(announcement=announcement,
                                                    dungeon_run=announcement.dungeon_run,
                                                    characters = characters_list)
                    await db.update_announcement_has_been_sent(announcement.id)
                    
                    channel = self.bot.get_channel(discord_guild_db.announcement_channel_id)
                    await channel.send(embed=embed)
                
            await asyncio.sleep(300)

    @tasks.loop(time=time(hour=0, minute=0, second=0))
    async def crawl_for_data(self):
        await self.bot.wait_until_ready()
        
        while not self.is_closed():
            await asyncio.sleep(600)
            
            for guild in self.bot.guilds:            
                discord_guild = await db.get_discord_guild_by_id(guild.id)
                
                if discord_guild is None:
                    await db.add_discord_guild(db.DiscordGuildDB(id = guild.id,
                                                                 discord_guild_name=guild.name))
                    
                elif discord_guild.is_announcing is False:
                    continue
                
                elif discord_guild.announcement_channel_id is None:
                    continue
                                
                else:       
                    
                    game_guilds = db.get_all_game_guilds_by_discord_id(guild.id)
                    channel = self.bot.get_channel(discord_guild.announcement_channel_id)
                    
                    guild_crawl = await raiderIO.crawl_discord_guild_members(discord_guild.id)
                                      
                    await channel.send(guild_crawl)
                    
                    character_crawl = await raiderIO.crawl_characters(discord_guild.id)
                    
                    await channel.send(character_crawl)
                    
            if util.seconds_until(0,0) < 1200:
                        # If it's less than 20 minutes until midnight, run this code.
                        print("It's less than 20 minutes until midnight.")         
            await asyncio.sleep(3600*3)
            
                    
                    

def setup(bot):
    bot.add_cog(Announcement(bot))
    print("Admin cog is loaded successfully.")
    