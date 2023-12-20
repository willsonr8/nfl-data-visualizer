import json
class Player_Info:
    def __init__(self, name, ID, headshot, team):
        self.name = name
        self.ID = str(ID)
        self.headshot = headshot
        self.team = team
        self.fantasy_points = []
        self.rush_yards = []
        self.carries = []
        self.rushTD = []

    @classmethod
    def from_api_response(cls, parsed_data):

        player_info = parsed_data["body"][0]
        name = player_info.get("espnName")
        ID = player_info.get("playerID")
        headshot = player_info.get("espnHeadshot")
        team = player_info.get("team")

        return cls(name, ID, headshot, team)