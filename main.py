import streamlit as st
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
        st.write()
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


def pullFantasyInfo(ID):
    conn = http.client.HTTPSConnection("tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "00d7863507msh695c4dd7170a696p12d9efjsnfe4d06584f4b",
        'X-RapidAPI-Host': "tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com"
    }

    conn.request("GET",
                 f"/getNFLGamesForPlayer?playerID={ID}&fantasyPoints=true&twoPointConversions=2&passYards=.04&passTD=4&passInterceptions=-2&pointsPerReception=1&carries=.2&rushYards=.1&rushTD=6&fumbles=-2&receivingYards=.1&receivingTD=6&targets=0&defTD=6",
                 headers=headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")
    fantasy_points = []

    parsed_data = json.loads(data)

    print(parsed_data)

    for key in parsed_data["body"].keys():
        fantasy_points.append(parsed_data["body"][key].get("fantasyPointsDefault").get("PPR"))

    return fantasy_points




if __name__ == '__main__':

    st.title("NFL Data Visualizer")

    st.text_input("Player name", key="name")

    name = inputHandler(st.session_state.name)

    if validPlayer(name) is False:
        st.write("Player not found")

    else:

        player = pullPlayer(name)

        player.fantasy_points = pullFantasyInfo(player.ID)

        st.write(player.name)

        st.write(player.ID)

        st.image(player.headshot)

        print(player.fantasy_points[0])

        st.line_chart(player.fantasy_points)
