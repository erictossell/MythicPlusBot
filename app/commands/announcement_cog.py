import asyncio
import os
from discord.ext import commands, tasks
from datetime import time

from dotenv import load_dotenv
from app import visualizer
import app.db as db
from app.objects.embed_builder import announce_guild_run_embed, daily_guild_report_embed
import app.raiderIO as raiderIO
import app.util as util

load_dotenv('configurations/main.env')
SUPPORT_SERVER_ID = os.getenv('SUPPORT_SERVER_ID')
SUPPORT_CHANNEL_ID = os.getenv('SUPPORT_CHANNEL_ID')

class Announcement(commands.Cog):
    """This cog contains commands for announcements.

    Args:
        commangs (_type_): _description_
    """
    def __init__(self, bot):
        self.bot = bot
        print("Announcement cog is initializing....")
       
        # self.announcement_task = self.bot.loop.create_task(self.send_announcements())
        self.crawl_task = self.bot.loop.create_task(self.crawl_for_data())
        self.daily_report_task = self.bot.loop.create_task(self.send_daily_report())
        self.is_closed = bot.is_closed
        self.time_until_daily_report = util.time_until_target(hour=20, minute=0)
          
    @tasks.loop()
    async def send_daily_report(self):
        await self.bot.wait_until_ready()
        
        while not self.is_closed(): 
            
            self.time_until_daily_report = util.time_until_target(hour=0, minute=0)
            await asyncio.sleep(self.time_until_daily_report)
            
            for guild in self.bot.guilds:
                
                discord_guild_db = await db.get_discord_guild_by_id(guild.id)
                
                if discord_guild_db is None:
                    await db.add_discord_guild(db.DiscordGuildDB(id = guild.id,
                                                                 discord_guild_name = guild.name))
            
                elif discord_guild_db.is_announcing is False:
                    continue
                
                elif discord_guild_db.announcement_channel_id is None:
                    continue
                
                else:
                    channel = self.bot.get_channel(discord_guild_db.announcement_channel_id)
                                        
                    guild_run_list = await db.get_daily_guild_runs(discord_guild_db.id)
                    bot_user = await self.bot.fetch_user(1073958413488369794)

                    
                    previous_run_count = len(guild_run_list)
                    run_list = await db.get_daily_non_guild_runs(discord_guild_id=discord_guild_db.id, number_of_runs= (8-previous_run_count))
                    
                    all_runs = await db.get_all_daily_runs(discord_guild_id=discord_guild_db.id)
                
                    
                    
                    graph = await visualizer.daily_guild_runs_plot(all_runs, discord_guild_id=discord_guild_db.id)
                    
                    embed = daily_guild_report_embed(discord_guild_db=discord_guild_db,
                                                            guild_run_list=guild_run_list,
                                                            non_guild_run_list=run_list,
                                                            bot_user=bot_user)
                    if graph is not None:
                        embed.set_image(url=f'attachment://{graph.filename}')
                        await channel.send(file=graph, embed=embed)
                    else:
                        await channel.send(embed=embed)

    
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
                    characters_list = await db.get_all_characters_for_run(announcement.dungeon_run_id)
                    
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
                    
                    channel = self.bot.get_channel(int(SUPPORT_CHANNEL_ID))
                    
                    try:
                        
                        guild_crawl = await asyncio.wait_for(raiderIO.crawl_discord_guild_members(discord_guild.id), timeout=1200)
                        await channel.send(guild_crawl)
                        
                        character_crawl = await asyncio.wait_for(raiderIO.crawl_characters(discord_guild.id), timeout=1200)
                        await channel.send(character_crawl)
                    
                    except TimeoutError:
                        print(f"Timeout occurred when trying to crawl data for guild id: {discord_guild.id}")
                        continue
                    except Exception:
                        print(f"An error occurred when trying to crawl data for guild id: {discord_guild.id}")
                        continue
                    
            if util.seconds_until(0,0) < 1200:
                        # If it's less than 20 minutes until midnight, run this code.
                        print("It's less than 20 minutes until midnight.")
            await asyncio.sleep(3600*1)
            
    

def setup(bot):
    bot.add_cog(Announcement(bot))
    print("Announcement cog has loaded successfully.")
    