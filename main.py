from API import APICalls
from Charts import ChartGenerator
import streamlit as st
import pandas as pd


def input_handler(name):
    norm_input = ""
    for c in name:
        if c == " ":
            c = "_"
        norm_input += c
    return norm_input


if __name__ == '__main__':

    st.title("NFL Data Visualizer")

    st.text_input("Player name", key="name")

    name = input_handler(st.session_state.name)

    if APICalls.valid_player(name) is False:
        if name == "":
            st.write()
        else:
            st.write("Player not found")

    else:

        player = APICalls.pull_player(name)

        APICalls.pull_fantasy_info(player)

        st.write(player.name)

        st.image(player.headshot)

        completed_team_games, all_team_games = APICalls.store_team_games(player.team)

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

