from datetime import datetime
from typing import List
import discord
from app.raiderIO.models.dungeon_run import DungeonRun
from app.raiderIO.models.score_color import ScoreColor


from app.util import convert_millis, hex_to_rgb

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
    
                
    
