class Member:
    """This class represents a member of a guild in World of Warcraft with data from RaiderIO."""

    def __init__(self, rank, name, class_name, last_crawled_at, profile_url, realm):
        self.rank = rank
        self.name = name
        self.class_name = class_name
        self.last_crawled_at = last_crawled_at
        self.profile_url = profile_url
        self.realm = realm
