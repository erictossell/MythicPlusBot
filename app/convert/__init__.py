


from app.db.models.character_db import CharacterDB
from app.db.models.character_run_db import CharacterRunDB
from app.db.models.dungeon_run_db import DungeonRunDB
from app.raiderIO.models.character import Character
from app.raiderIO.models.dungeon_run import DungeonRun


def character_io(character: Character, discord_user_id: int, discord_guild_id: int) -> Character:
    character_db = CharacterDB(discord_user_id = discord_user_id,
                          discord_guild_id = discord_guild_id,
                          guild_name = character.guild_name,
                          name = character.name,
                          realm = character.realm,
                          faction = character.faction,
                          region = character.region,
                          role = character.role,
                          spec_name=  character.spec_name,
                          class_name= character.class_name,
                          achievement_points= character.achievement_points,
                          item_level= character.item_level,
                          score= character.score,
                          rank= character.rank,
                          thumbnail_url= character.thumbnail_url,
                          url= character.url,
                          last_crawled_at= character.last_crawled_at,
                          is_reporting= True)
    return character_db

def dungeon_run_io(run: DungeonRun) -> DungeonRunDB:
    return DungeonRunDB(dungeon_id = run.id,
                           season = run.season,
                           name = run.name,
                           short_name = run.short_name,
                           mythic_level =    run.mythic_level,
                           completed_at = run.completed_at,
                           clear_time_ms =run.clear_time_ms,
                           par_time_ms = run.par_time_ms,
                           num_keystone_upgrades = run.num_keystone_upgrades,
                           score = run.score,
                           url = run.url)
    
    
def character_run_io(character_db: Character,
                             dungeon_run_db: DungeonRun,
                             rio_character_id: int = None,
                             spec_name: str = None,
                             role : str = None,
                             rank_world: int = None,
                             rank_region: int = None,
                             rank_realm: int = None) -> CharacterRunDB:
    return CharacterRunDB(character = character_db,
                             dungeon_run= dungeon_run_db,
                             rio_character_id= rio_character_id,
                             spec_name= spec_name,
                             role= role,
                             rank_world= rank_world,
                             rank_region= rank_region,
                             rank_realm= rank_realm)
    