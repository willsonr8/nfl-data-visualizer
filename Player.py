import json
class Player_Info:
    def __init__(self, name, stats):
        self.name = name
        self.stats = stats
        self.error = False

    @classmethod
    def from_api_response(cls, api_response):
        parsed_data = json.loads(api_response)
        name = parsed_data.get("name")
        stats = parsed_data.get("stats")
        error = "error" in parsed_data
        if error:
            return cls(None, None)  # Return None for name and stats if error
        else:
            return cls(name, stats)