
import asyncio
import discord
from discord.ext import commands, tasks
from datetime import time

import db
import raiderIO


class Announcement(commands.Cog):
    """This cog contains commands for announcements.

    Args:
        commangs (_type_): _description_
    """
    def __init__(self, bot):
        self.bot = bot
        print("Announcement cog is initializing....")
        self.announcement_channel_id = 1074546599239356498
        self.bg_task = self.bot.loop.create_task(self.send_announcements())
        self.is_closed = bot.is_closed
    
    @tasks.loop(time=time(hour=22, minute=5, second=0))
    async def send_announcements(self):
        await self.bot.wait_until_ready()
        channel_id = self.announcement_channel_id   
        while not self.is_closed():
            announcement = db.lookup_next_announcement(804157941732474901)
            
            if announcement is None:
                print("No announcement found.")
                await asyncio.sleep(60)
                continue

            channel = self.bot.get_channel(channel_id)
            embed = discord.Embed(title=announcement.title, description=announcement.description, color=discord.Color.green())
            embed.add_field(name=f'Announcement ID: {announcement.id}', value=f'Created at : {announcement.created_at}')
            embed.add_field(name='Announcement Message', value=announcement.message)
            
            db.update_announcement_has_been_sent(announcement.id)
            await channel.send(embed=embed)
            await asyncio.sleep(60)
    
    @tasks.loop(time=time(hour=0, minute=0, second=0))
    async def small_crawl_characters(self):
        await self.bot.wait_until_ready()
        channel_id = self.announcement_channel_id
        while not self.is_closed():
            raiderIO.crawl
            
            
            await asyncio.sleep(60)
            continue
        
            
                
def setup(bot):
    bot.add_cog(Announcement(bot))    
    print("Admin cog is loaded successfully.")
    