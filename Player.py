import json
class Player_Info:
    def __init__(self, name, school, headshot):
        self.name = name
        self.school = school
        self.headshot = headshot

    @classmethod
    def from_api_response(cls, api_response):

        parsed_data = json.loads(api_response)
        if "error" in parsed_data:
            return cls(None, None)

        player_info = parsed_data["body"][0]
        name = player_info.get("espnName")
        school = player_info.get("school")
        headshot = player_info.get("espnHeadshot")

        return cls(name, school, headshot)