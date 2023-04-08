import discord
import time
import datetime

import util.util as util
from util.util import hex_to_rgb
class Character:
    def __init__(self, name, realm, faction, role, spec_name, class_name, achievement_points, item_level, score, score_color, rank, best_runs, recent_runs, thumbnail_url, url, last_crawled_at):
        self = self
        self.name = name       
        self.realm = realm                                       
        self.faction = faction.capitalize()
        self.region = 'us'
        self.role = role
        self.spec_name = spec_name
        self.class_name = class_name       
        self.achievement_points = achievement_points
        self.item_level = item_level
        self.score = score
        self.score_color = score_color
        self.rank = rank        
        self.best_runs = best_runs
        self.recent_runs = recent_runs
        self.thumbnail_url = thumbnail_url
        self.url = url
        
        self.last_crawled_at = last_crawled_at   
    
    def getCharacterEmbed(self):        
        title = self.name.capitalize() + ' - ' + self.realm.capitalize() + ' - ' + self.faction.capitalize() 
        color = discord.Color.from_rgb(*hex_to_rgb(self.score_color))    
        embed = discord.Embed(title=title, description='', color=color, url=self.url)
        embed.add_field(name='Mythic + Score', value=str(self.score), inline=False)
        embed.add_field(name='Class Rank on ' + self.realm, value=str(self.rank), inline=False)
        embed.add_field(name='Item Level', value=str(self.item_level), inline=False)
        embed.add_field(name='Class', value=self.class_name, inline=False)
        embed.add_field(name ='Last Spec', value=self.spec_name, inline=False)
        embed.add_field(name='Last Role', value=self.role, inline=False)
        embed.add_field(name='Achievement Points', value=str(self.achievement_points), inline=False)     
        embed.set_thumbnail(url=self.thumbnail_url)             
        embed.set_footer(text= 'Last crawled at: ' + self.last_crawled_at)
        
        return embed
                
    def getBestRunsEmbed(self):
        title = self.name.capitalize()+"'s Best Mythic+ Runs"
        
        embed = discord.Embed(title=title, description= '', color=discord.Color.from_rgb(*hex_to_rgb(self.score_color)), url=self.url)
        embed.add_field(name='Class', value=self.class_name, inline=True)
        embed.add_field(name='Last Spec', value=self.spec_name, inline=True)
        embed.add_field(name='Last Role', value=self.role, inline=True)        
        #embed.add_field(name='Achievement Points', value=str(self.achievement_points), inline=True)    
        embed.set_thumbnail(url=self.thumbnail_url)            

        for run in self.best_runs:
            time = util.convertMillis(run.clear_time_ms)
            name = run.name + ' - ' + str(run.mythic_level)    
            value = 'Time: **' + time + '** | Score: ' + str(run.score) +"\n" + run.affixes[0].name + ', ' + run.affixes[1].name + ', ' + run.affixes[2].name
                        
            embed.add_field(name=name, value=value, inline=False)
        embed.set_footer(text='Last updated ' + self.last_crawled_at)
        return embed
    
    def getRecentRunsEmbed(self):        
        title = self.name.capitalize()+"'s Recent Mythic+ Runs"                
        embed = discord.Embed(title=title, description= '', color=discord.Color.from_rgb(*hex_to_rgb(self.score_color)), url=self.url)
        embed.add_field(name='Class', value=self.class_name, inline=True)
        embed.add_field(name='Last Spec', value=self.spec_name, inline=True)
        embed.add_field(name='Last Role', value=self.role, inline=True)        
        #embed.add_field(name='Achievement Points', value=str(self.achievement_points), inline=True)    
        embed.set_thumbnail(url=self.thumbnail_url)             

        for run in self.recent_runs:
            time = util.convertMillis(run.clear_time_ms)
            name = run.name + ' - ' + str(run.mythic_level)    
            value = 'Time: **' + time + '** | Score: ' + str(run.score) + "\n" + run.affixes[0].name + ', ' + run.affixes[1].name + ', ' + run.affixes[2].name
                        
            embed.add_field(name=name, value=value, inline=False)
        embed.set_footer(text='Last updated ' + self.last_crawled_at) 
        return embed
          