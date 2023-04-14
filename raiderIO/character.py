from datetime import datetime
from typing import List
import discord
from raiderIO.dungeonRun import DungeonRun
from raiderIO.scoreColor import ScoreColor


from util import convert_millis, hex_to_rgb

class Character:
    """The character class represents a character from the Raider.IO API."""
    def __init__(self,
                 name: str,
                 realm: str,
                 guild_name: str,
                 faction: str,
                 role: str,
                 spec_name: str,
                 class_name: str,
                 achievement_points: int,
                 item_level: int,
                 score: int,
                 score_color: ScoreColor,
                 rank: int,
                 best_runs: List[DungeonRun],
                 recent_runs: List[DungeonRun],
                 thumbnail_url: str,
                 url: str,
                 last_crawled_at: datetime):
        """The init method for the Character class."""
        self.name = name
        self.realm = realm
        self.guild_name = guild_name
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
    def get_character_embed(self) -> discord.Embed:
        """Retrieves the character embed for the character.

        Returns:
            discord.Embed: A discord embed object containing the character information.
        """
        print('Character info embed created for ' + self.name + ' on ' + self.realm)
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
        embed.set_footer(text= 'Last crawled at: '+ self.last_crawled_at)
        return embed
                
    def get_best_runs_embed(self) -> discord.Embed:
        """Retrieves the best runs embed for the character.

        Returns:
            discord.Embed: A discord embed object containing the character's best runs.
        """
        title = self.name.capitalize()+"'s Best Mythic+ Runs"
        embed = discord.Embed(title=title, description= '', color=discord.Color.from_rgb(*hex_to_rgb(self.score_color)), url=self.url)
        embed.add_field(name='Class', value=self.class_name, inline=True)
        embed.add_field(name='Last Spec', value=self.spec_name, inline=True)
        embed.add_field(name='Last Role', value=self.role, inline=True)        
        #embed.add_field(name='Achievement Points', value=str(self.achievement_points), inline=True)
        embed.set_thumbnail(url=self.thumbnail_url)            

        for run in self.best_runs:
            time = convert_millis(run.clear_time_ms)
            name = run.name + ' - ' + str(run.mythic_level)    
            value = f'Time: ** {time} + ** | Score: {run.score} \n  {run.affixes[0].name} ,  {run.affixes[1].name} ,  {run.affixes[2].name}'
                        
            embed.add_field(name=name, value=value, inline=False)
        embed.set_footer(text='Last updated ' + self.last_crawled_at)
        return embed
    
    def get_recent_runs_embed(self) -> discord.Embed:
        """Retrieves the recent runs embed for the character.

        Returns:
            discord.Embed: A discord embed object containing the character's recent runs.
        """
        title = self.name.capitalize()+"'s Recent Mythic+ Runs"                
        embed = discord.Embed(title=title, description= '', color=discord.Color.from_rgb(*hex_to_rgb(self.score_color)), url=self.url)
        embed.add_field(name='Class', value=self.class_name, inline=True)
        embed.add_field(name='Last Spec', value=self.spec_name, inline=True)
        embed.add_field(name='Last Role', value=self.role, inline=True)        
        #embed.add_field(name='Achievement Points', value=str(self.achievement_points), inline=True)
        embed.set_thumbnail(url=self.thumbnail_url)             

        for run in self.recent_runs:
            time = convert_millis(run.clear_time_ms)
            name = run.name + ' - ' + str(run.mythic_level)    
            value = f'Time: ** {time} + ** | Score: {run.score} \n  {run.affixes[0].name} ,  {run.affixes[1].name} ,  {run.affixes[2].name}'
                        
            embed.add_field(name=name, value=value, inline=False)
        embed.set_footer(text='Last updated ' + self.last_crawled_at) 
        return embed
