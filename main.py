import http.client
import json
from Player import Player_Info
import pandas as pd
import numpy as np

def validPlayer(name):
    conn = http.client.HTTPSConnection("tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "00d7863507msh695c4dd7170a696p12d9efjsnfe4d06584f4b",
        'X-RapidAPI-Host': "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
    }

    conn.request("GET", f"/getNFLPlayerInfo?playerName={name}&getStats=true", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    if "error" in data:
        return False
    else:
        return True

def inputHandler(name):
    normInput = ""
    for c in name:
        if c == " ":
            c = "_"
        normInput += c
    return normInput

def pullPlayer(name):
    if name == "":
        return
    conn = http.client.HTTPSConnection("tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "00d7863507msh695c4dd7170a696p12d9efjsnfe4d06584f4b",
        'X-RapidAPI-Host': "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
    }

    conn.request("GET", f"/getNFLPlayerInfo?playerName={name}&getStats=true", headers=headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")  # Decode the response to a string

    player = Player_Info.from_api_response(data)

    return player

def getGameWeek(game_ID):
    import http.client

    conn = http.client.HTTPSConnection("tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "00d7863507msh695c4dd7170a696p12d9efjsnfe4d06584f4b",
        'X-RapidAPI-Host': "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
    }

    conn.request("GET", f"/getNFLGameInfo?gameID={game_ID}", headers=headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")
    parsed_data = json.loads(data)

    game_week = int(parsed_data["body"]["gameWeek"][5:])

    return game_week


def pullFantasyInfo(player):
    conn = http.client.HTTPSConnection("tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "00d7863507msh695c4dd7170a696p12d9efjsnfe4d06584f4b",
        'X-RapidAPI-Host': "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
    }

    conn.request("GET",
                 f"/getNFLGamesForPlayer?playerID={player.ID}&fantasyPoints=true&twoPointConversions=2&passYards=.04&"
                 f"passTD=4&passInterceptions=-2&pointsPerReception=1&carries=.2&rushYards=.1&rushTD=6&fumbles=-2&"
                 f"receivingYards=.1&receivingTD=6&targets=0&defTD=6",
                 headers=headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")
    fantasy_points = []

    parsed_data = json.loads(data)

    player_games = []

    seen_games = set()

    team_games = storeTeamGames(player.team)

    for key in parsed_data["body"].keys():
        game_ID = parsed_data["body"][key]["gameID"]
        player_games.append(game_ID)

    for game in team_games:
        if game in player_games:  # handles games where points accrued
            game_points = float(parsed_data["body"][game]["fantasyPointsDefault"]["PPR"])
            fantasy_points.append(game_points)
            seen_games.add(game)
        elif game == np.NaN:  # handles bye weeks
            fantasy_points.append(np.NaN)
        else:  # handles games where no points accrued
            fantasy_points.append(0.0)

    for game in player_games:
        if game not in seen_games:

            if int(game[0:8]) > 20230827:  # should be a way to clean this up
                game_week = getGameWeek(game)

                if game_week <= len(fantasy_points):
                    fantasy_points[game_week - 1] = float(parsed_data["body"][game]["fantasyPointsDefault"]["PPR"])

    player.fantasy_points = fantasy_points

def storeTeamGames(teamAbv):

    conn = http.client.HTTPSConnection("tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "00d7863507msh695c4dd7170a696p12d9efjsnfe4d06584f4b",
        'X-RapidAPI-Host': "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
    }

    conn.request("GET", f"/getNFLTeamSchedule?teamAbv={teamAbv}&season=2023", headers=headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")
    parsed_data = json.loads(data)

    print(parsed_data)

    team_games = []

    game_weeks = []


    for game_data in parsed_data["body"]["schedule"]:
        game_type = game_data.get("seasonType")
        game_status = game_data.get("gameStatus")

        if (game_type == "Regular Season"):
            game_ID = game_data.get("gameID")
            team_games.append(game_ID)
            game_week = int(game_data.get("gameWeek")[5:])
            game_weeks.append(game_week)

    for i in range(len(game_weeks) - 1):
        if game_weeks[i] == game_weeks[i + 1]:
            del team_games[i + 2]
            continue
        if (game_weeks[i] + 1) != (game_weeks[i + 1]):
            team_games.insert(i + 1, np.NaN)

    for val in team_games:
        print(str(val) + " ")

    return team_games



if __name__ == '__main__':


    window = True

    while window:

        user_input = input("Enter a player: ")

        name = inputHandler(user_input)

        if validPlayer(name) is False:

            print("Player does not exist")

        else:

            player = pullPlayer(name)

            if isinstance(player, Player_Info):

                pullFantasyInfo(player)

                print(player.name)

                chart_data = pd.DataFrame(
                    {
                        "week": range(1, len(player.fantasy_points) + 1),
                        "points": player.fantasy_points
                    }
                )

                for val in player.fantasy_points:
                    print(str(val) + " ")
            else:
                print("Error: Player info retrieval failed")

