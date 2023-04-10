class Member:
    """This class represents a member of a guild in World of Warcraft with data from RaiderIO.
    """
    def __init__(self, rank, name, wow_class, last_crawled_at,profile_url):
        self.rank = rank
        self.name = name
        self. wow_class = wow_class
        self. last_crawled_at = last_crawled_at
        self. profile_url = profile_url