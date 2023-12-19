import http.client
import json
import streamlit as st
from Player import Player_Info
import pandas as pd
from Charts import ChartGenerator

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

    print(parsed_data)

    player_games = []

    seen_games = set()

    completed_team_games, all_team_games = storeTeamGames(player.team)

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
            all_team_games.insert(i + 1, ("Bye", "Bye"))

    for val in all_team_games:
        print(str(val) + " ")
    for val in completed_team_games:
        print(str(val) + " ")

    return completed_team_games, all_team_games


if __name__ == '__main__':

    st.title("NFL Data Visualizer")

    st.text_input("Player name", key="name")

    name = inputHandler(st.session_state.name)

    if validPlayer(name) is False:
        if name == "":
            st.write()
        else:
            st.write("Player not found")

    else:

        player = pullPlayer(name)

        pullFantasyInfo(player)

        st.write(player.name)

        st.image(player.headshot)

        completed_team_games, all_team_games = storeTeamGames(player.team)

        table_data = pd.DataFrame(
            {
                "Gameweek": [i for i, _ in all_team_games],
                "Matchup": [j for _, j in all_team_games],
                "Points": [k for k in player.fantasy_points]

            }

        )

        st.dataframe(table_data, hide_index=True)

        chart_data = pd.DataFrame(
            {
                "Gameweek": range(1, len(completed_team_games) + 1),
                "Points": player.fantasy_points
            }
        )

        tab1, tab2 = st.tabs(["Fantasy Points Per Week", "Scatterplot"])

        with tab1:
            ChartGenerator.altair_chart(chart_data)

        with tab2:
            ChartGenerator.scatter_plot(chart_data)

