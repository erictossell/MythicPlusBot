class DungeonRunIO:
    def __init__(self, name, short_name, mythic_level, completed_at, clear_time_ms, par_time_ms, num_keystone_upgrades, score, affixes, url):
        self.name = name
        self.short_name = short_name
        self.mythic_level = mythic_level
        self.completed_at = completed_at
        self.clear_time_ms = clear_time_ms
        self.par_time_ms = par_time_ms
        self.num_keystone_upgrades = num_keystone_upgrades
        self.score = score
        self.affixes = affixes
        self.url = url
        start_index = url.find("/season-df-1/") + len("/season-df-1/")    
        self.id = url[start_index:].split("-")[0]
        start_index = url.find("/mythic-plus-runs/") + len("/mythic-plus-runs/")
        self.season = url[start_index:].split("/")[0]