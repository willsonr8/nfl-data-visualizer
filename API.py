import http.client
from Player import Player_Info
import json


class APICalls:
    url = "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
    headers = {
        'X-RapidAPI-Key': "00d7863507msh695c4dd7170a696p12d9efjsnfe4d06584f4b",
        'X-RapidAPI-Host': url
    }

    @classmethod
    def make_request(cls, endpoint):
        conn = http.client.HTTPSConnection(cls.url)
        conn.request("GET", endpoint, headers=cls.headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        parsed_data = json.loads(data)
        return parsed_data

    @classmethod
    def get_single_player_stats(cls, player_id):  # Get NFL Games and Stats for Single Player

        endpoint = f"/getNFLGamesForPlayer?playerID={player_id}&fantasyPoints=true&twoPointConversions=2&" \
                   f"passYards=.04&passTD=4&passInterceptions=-2&pointsPerReception=1&carries=.2&rushYards=.1&" \
                   f"rushTD=6&fumbles=-2&receivingYards=.1&receivingTD=6&targets=0&defTD=6"

        return cls.make_request(endpoint)

    @classmethod
    def get_player_info(cls, player_name):  # Get Player Information

        endpoint = f"/getNFLPlayerInfo?playerName={player_name}&getStats=true"

        return cls.make_request(endpoint)

    @classmethod
    def get_weekly_schedule(cls, week):

        endpoint = f"/getNFLGamesForWeek?week={week}&seasonType=reg&season=2023"

        return cls.make_request(endpoint)

    @classmethod
    def get_team_schedule(cls, team_abv):

        endpoint = f"/getNFLTeamSchedule?teamAbv={team_abv}&season=2023"

        return cls.make_request(endpoint)

    @classmethod
    def get_game_info(cls, game_id):

        endpoint = f"/getNFLGameInfo?gameID={game_id}"

        return cls.make_request(endpoint)


    @classmethod
    def valid_player(cls, player_name):

        data = cls.get_player_info(player_name)

        if "error" in data:
            return False
        else:
            return True

    @classmethod
    def pull_fantasy_info(cls, player):  # uses Get NFL Games and Stats For a Single Player

        parsed_data = cls.get_single_player_stats(player.ID)

        fantasy_points = []

        print(parsed_data)

        player_games = []

        seen_games = set()

        completed_team_games, all_team_games = cls.store_team_games(player.team)

        for key in parsed_data["body"].keys():
            game_ID = parsed_data["body"][key]["gameID"]
            player_games.append(game_ID)

        for game in completed_team_games:
            if game in player_games:  # handles games where points accrued
                game_points = float(parsed_data["body"][game]["fantasyPointsDefault"]["PPR"])
                fantasy_points.append(game_points)
                seen_games.add(game)
            elif game is None:  # handles bye weeks
                fantasy_points.append(None)
            else:  # handles games where no points accrued
                fantasy_points.append(0.0)

        for game in player_games:
            if game not in seen_games:

                if int(game[0:8]) > 20230827:  # should be a way to clean this up
                    game_week = cls.get_game_week(game)

                    if game_week <= len(fantasy_points):
                        fantasy_points[game_week - 1] = float(parsed_data["body"][game]["fantasyPointsDefault"]["PPR"])

        player.fantasy_points = fantasy_points

    @classmethod
    def pull_player(cls, name):  # uses Get Player Information API endpoint
        if name == "":
            return

        parsed_data = cls.get_player_info(name)

        player = Player_Info.from_api_response(parsed_data)

        return player

    @classmethod
    def store_team_games(cls, teamAbv):

        parsed_data = cls.get_team_schedule(teamAbv)

        print(parsed_data)

        completed_team_games = []

        all_team_games = []

        game_weeks = []

        for game_data in parsed_data["body"]["schedule"]:
            game_type = game_data.get("seasonType")
            game_status = game_data.get("gameStatus")
            game_ID = game_data.get("gameID")
            game_string = game_data.get('away') + ' @ ' + game_data.get('home')

            if game_type == "Regular Season" and game_data.get('away') != game_data.get('home'):
                if game_status == "Completed":
                    completed_team_games.append(game_ID)
                else:
                    completed_team_games.append(None)

                game_week = int(game_data.get("gameWeek")[5:])
                game_weeks.append(game_week)
                all_team_games.append((game_week, game_string))

        indices_to_remove = []

        for i in range(len(game_weeks) - 1):

            if game_weeks[i] == game_weeks[i + 1]:
                if i + 2 < len(completed_team_games):  # Check if index exists
                    indices_to_remove.append(i + 2)
                else:
                    indices_to_remove.append(i + 1)

        for index in sorted(indices_to_remove, reverse=True):
            del completed_team_games[index]
            del all_team_games[index]

        for i in range(len(game_weeks) - 1):
            if (game_weeks[i] + 1) != (game_weeks[i + 1]):
                completed_team_games.insert(i + 1, None)
                all_team_games.insert(i + 1, (i + 2, "Bye"))

        for val in all_team_games:
            print(str(val) + " ")
        for val in completed_team_games:
            print(str(val) + " ")

        return completed_team_games, all_team_games

    @classmethod
    def get_game_week(cls, game_id):

        parsed_data = cls.get_game_info(game_id)

        game_week = int(parsed_data["body"]["gameWeek"][5:])

        return game_week
