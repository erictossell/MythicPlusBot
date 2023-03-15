class DungeonRun:
    def __init__(self, name, short_name, mythic_level, completed_at, clear_time_ms, par_time_ms, num_keystone_upgrades, score, affixes, url):
        self.name = name
        self.short_name = short_name
        self.mythic_level = mythic_level
        self.completed_at = completed_at
        self.clear_time_ms = clear_time_ms
        self.part_time_ms = par_time_ms
        self.num_keystone_upgrades = num_keystone_upgrades
        self.score = score
        self.affixes = affixes
        self.url = url