import json
class Player_Info:
    def __init__(self, name, ID, headshot, team):
        self.name = name
        self.ID = str(ID)
        self.headshot = headshot
        self.team = team
        self.fantasy_points = []

    @classmethod
    def from_api_response(cls, api_response):

        parsed_data = json.loads(api_response)

        player_info = parsed_data["body"][0]
        name = player_info.get("espnName")
        ID = player_info.get("playerID")
        headshot = player_info.get("espnHeadshot")
        team = player_info.get("team")

        return cls(name, ID, headshot, team)
