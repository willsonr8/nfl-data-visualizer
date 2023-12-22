import json
class Player_Info:
    def __init__(self, name, ID, pos, headshot, team):
        self.name = name
        self.ID = str(ID)
        self.pos = pos
        self.headshot = headshot
        self.team = team
        self.fantasy_points = []
        # "Rushing"
        self.rush_avg = []
        self.rush_yards = []
        self.carries = []
        self.long_rush = []
        self.rush_td = []
        # "Defense"
        self.fumbles = []
        self.fumbles_lost = []
        # "Receiving"
        self.receptions = []
        self.rec_td = []
        self.long_rec = []
        self.targets = []
        self.rec_yards = []
        self.rec_avg = []
        self.two_point_conversions = []
        # "Passing"
        self.pass_attempts = []
        self.pass_avg = []
        self.pass_td = []
        self.pass_yds = []
        self.interceptions = []
        self.pass_completions = []

    @classmethod
    def from_api_response(cls, parsed_data):

        player_info = parsed_data["body"][0]
        name = player_info.get("espnName")
        ID = player_info.get("playerID")
        pos = player_info.get("pos")
        headshot = player_info.get("espnHeadshot")
        team = player_info.get("team")

        return cls(name, ID, pos, headshot, team)