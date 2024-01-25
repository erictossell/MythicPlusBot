from bot.db.models.character_run_db import CharacterRunDB
from bot.db.models.dungeon_run_db import DungeonRunDB
from bot.raiderIO.models.character import Character
from bot.raiderIO.models.dungeon_run import DungeonRun


def dungeon_run_io(run: DungeonRun) -> DungeonRunDB:
    return DungeonRunDB(
        dungeon_id=run.id,
        season=run.season,
        name=run.name,
        short_name=run.short_name,
        mythic_level=run.mythic_level,
        completed_at=run.completed_at,
        clear_time_ms=run.clear_time_ms,
        par_time_ms=run.par_time_ms,
        num_keystone_upgrades=run.num_keystone_upgrades,
        score=run.score,
        url=run.url,
    )


def character_run_io(
    character_db: Character,
    dungeon_run_db: DungeonRun,
    rio_character_id: int = None,
    spec_name: str = None,
    role: str = None,
    rank_world: int = None,
    rank_region: int = None,
    rank_realm: int = None,
) -> CharacterRunDB:
    return CharacterRunDB(
        character=character_db,
        dungeon_run=dungeon_run_db,
        rio_character_id=rio_character_id,
        spec_name=spec_name,
        role=role,
        rank_world=rank_world,
        rank_region=rank_region,
        rank_realm=rank_realm,
    )
