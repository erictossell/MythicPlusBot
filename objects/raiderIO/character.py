import discord

from util.util import convertMillis

class Character:
    def __init__(self, url, name, realm, faction, class_name, spec_name, role, thumbnail_url, achievement_points, last_crawled_at,score, rank, best_runs, recent_runs, item_level):
        self.region = 'us'        
        self.url = url
        self.name = name
        self.realm = realm                               
        self.faction = faction
        self.class_name = class_name
        self.spec_name = spec_name
        self.role = role
        self.thumbnail_url = thumbnail_url
        self.achievement_points = achievement_points
        self.last_crawled_at = last_crawled_at
        self.score = score
        self.rank = rank        
        self.best_runs = best_runs
        self.recent_runs = recent_runs
        self.item_level = item_level
        
    def getBestRunsEmbed(self):
        title = self.name+"'s Best Mythic+ Runs"         
            
        embed = discord.Embed(title=title, description= '', color=discord.Color.green(), url=self.url)
        embed.add_field(name='Class', value=self.class_name, inline=True)
        embed.add_field(name='Last Spec', value=self.spec_name, inline=True)
        embed.add_field(name='Last Role', value=self.role, inline=True)        
        embed.add_field(name='Achievement Points', value=str(self.achievement_points), inline=True)    
        embed.set_thumbnail(url=self.thumbnail_url)            

        for run in self.best_runs:
            time = convertMillis(run.clear_time_ms)
            name = run.name + ' - ' + str(run.mythic_level)    
            value = 'Time: **' + time + '** | Score: ' + str(run.score) +"\n" + run.affixes[0].name + ', ' + run.affixes[1].name + ', ' + run.affixes[2].name
                        
            embed.add_field(name=name, value=value, inline=False)
        embed.set_footer(text='Last updated ' + self.last_crawled_at)
        return embed
    
    def getRecentRunsEmbed(self):        
        title = self.name+"'s Recent Mythic+ Runs"                
        embed = discord.Embed(title=title, description= '', color=discord.Color.green(), url=self.url)
        embed.add_field(name='Class', value=self.class_name, inline=True)
        embed.add_field(name='Last Spec', value=self.spec_name, inline=True)
        embed.add_field(name='Last Role', value=self.role, inline=True)        
        embed.add_field(name='Achievement Points', value=str(self.achievement_points), inline=True)    
        embed.set_thumbnail(url=self.thumbnail_url)             

        for run in self.recent_runs:
            time = convertMillis(run.clear_time_ms)
            name = run.name + ' - ' + str(run.mythic_level)    
            value = 'Time: **' + time + '** | Score: ' + str(run.score) + "\n" + run.affixes[0].name + ', ' + run.affixes[1].name + ', ' + run.affixes[2].name
                        
            embed.add_field(name=name, value=value, inline=False)
        embed.set_footer(text='Last updated ' + self.last_crawled_at) 
        return embed
          