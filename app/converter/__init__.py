import app.db as db
import app.raiderIO as raiderIO

def convert_character_io(character: raiderIO.Character, discord_user_id: int, discord_guild_id: int) -> db.Character:
    character_db = db.CharacterDB(discord_user_id = discord_user_id,
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

def convert_dungeon_run_io(run: raiderIO.DungeonRun) -> db.DungeonRun:
    return db.DungeonRunDB(id = run.id,
                           season = run.season,
                           name = run.name,
                           short_name = run.short_name,
                           mythic_level =    run.mythic_level,
                           completed_at = run.completed_at,
                           clear_time_ms =run.clear_time_ms,
                           par_time_ms = run.par_time_ms,
                           num_keystone_upgrades = run.num_keystone_upgrades,
                           score = run.score,
                           url = run.url,
                           is_guild_run = False,
                           is_crawled = False,
                           character_runs = [])