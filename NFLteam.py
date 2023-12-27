class Team:
    def __init__(self, team_abv, team_city, team_schedule, loss, team_name,
                 nfl_com_logo1, team_id, tie, pa, pf, espn_logo1, wins, team_stats):
        self.teamAbv = team_abv
        self.teamCity = team_city
        self.teamSchedule = team_schedule
        self.loss = loss
        self.teamName = team_name
        self.nflComLogo1 = nfl_com_logo1
        self.teamID = team_id
        self.tie = tie
        self.pa = pa
        self.pf = pf
        self.espnLogo1 = espn_logo1
        self.wins = wins
        self.teamStats = team_stats

    @classmethod
    def from_api_response(cls, parsed_data):
        team_info = parsed_data
        team_abv = team_info.get("teamAbv")
        team_city = team_info.get("teamCity")
        team_schedule = team_info.get("teamSchedule")
        loss = team_info.get("loss")
        team_name = team_info.get("teamName")
        nfl_com_logo1 = team_info.get("nflComLogo1")
        team_id = team_info.get("teamID")
        tie = team_info.get("tie")
        pa = team_info.get("pa")
        pf = team_info.get("pf")
        espn_logo1 = team_info.get("espnLogo1")
        wins = team_info.get("wins")
        team_stats = team_info.get("teamStats")

        return cls(team_abv, team_city, team_schedule, loss, team_name,
                   nfl_com_logo1, team_id, tie, pa, pf, espn_logo1, wins, team_stats)