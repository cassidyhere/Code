class V:
    def __init__(self):
        self.name = None
        self.desc = None
        self.follow_count = 0
        self.follower_count = 0
        self.profile_url = None

    def __repr__(self):
        return '{}: {} 粉丝: {}'.format(self.name, self.desc, self.follower_count)

