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
          