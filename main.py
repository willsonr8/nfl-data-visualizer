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

        scoring_type = st.radio(
            "Select Scoring Type:",
            ["PPR", "halfPPR", "standard"],
            label_visibility="collapsed",
            index=0
        )

        player = APICalls.pull_player(name)

        APICalls.pull_fantasy_info(player, scoring_type)

        st.write(player.name)

        st.image(player.headshot)

        completed_team_games, all_team_games = APICalls.store_team_games(player.team)

        if player.pos == "RB":
            table_data = pd.DataFrame(
                {
                    "Gameweek": [i for i, _ in all_team_games],
                    "Matchup": [j for _, j in all_team_games],
                    "Points": player.fantasy_points,
                    "Carries": player.carries,
                    "Rush Yards": player.rush_yards,
                    "Rush TD": player.rush_td,
                    "Rush Avg": player.rush_avg,
                    "Long Rush": player.long_rush,
                    "Fumbles": player.fumbles,
                    "Targets": player.targets,
                    "Receptions": player.receptions,
                    "Rec Yards": player.rec_yards,
                    "Rec TD": player.rec_td,
                    "Rec Avg": player.rec_avg,
                    "Long Rec": player.long_rec,
                    "Two Point Conversions": player.two_point_conversions,
                    "Pass Attempts": player.pass_attempts,
                    "Pass Completions": player.pass_completions,
                    "Pass Yards": player.pass_yds,
                    "Pass TD": player.pass_td,
                    "Pass Avg": player.pass_avg,
                    "Interceptions": player.interceptions,
                }
            )

        elif player.pos == "QB":
            table_data = pd.DataFrame(
                {
                    "Gameweek": [i for i, _ in all_team_games],
                    "Matchup": [j for _, j in all_team_games],
                    "Points": player.fantasy_points,
                    "Pass Attempts": player.pass_attempts,
                    "Pass Completions": player.pass_completions,
                    "Pass Yards": player.pass_yds,
                    "Pass TD": player.pass_td,
                    "Pass Avg": player.pass_avg,
                    "Interceptions": player.interceptions,
                    "Carries": player.carries,
                    "Rush Yards": player.rush_yards,
                    "Rush TD": player.rush_td,
                    "Rush Avg": player.rush_avg,
                    "Long Rush": player.long_rush,
                    "Fumbles": player.fumbles,
                    "Targets": player.targets,
                    "Receptions": player.receptions,
                    "Rec Yards": player.rec_yards,
                    "Rec TD": player.rec_td,
                    "Rec Avg": player.rec_avg,
                    "Long Rec": player.long_rec,
                    "Two Point Conversions": player.two_point_conversions,
                }
            )

        else:
            table_data = pd.DataFrame(
                {
                    "Gameweek": [i for i, _ in all_team_games],
                    "Matchup": [j for _, j in all_team_games],
                    "Points": player.fantasy_points,
                    "Targets": player.targets,
                    "Receptions": player.receptions,
                    "Rec Yards": player.rec_yards,
                    "Rec TD": player.rec_td,
                    "Rec Avg": player.rec_avg,
                    "Long Rec": player.long_rec,
                    "Two Point Conversions": player.two_point_conversions,
                    "Rush Yards": player.rush_yards,
                    "Rush TD": player.rush_td,
                    "Rush Avg": player.rush_avg,
                    "Long Rush": player.long_rush,
                    "Fumbles": player.fumbles,
                    "Pass Attempts": player.pass_attempts,
                    "Pass Completions": player.pass_completions,
                    "Pass Yards": player.pass_yds,
                    "Pass TD": player.pass_td,
                    "Pass Avg": player.pass_avg,
                    "Interceptions": player.interceptions,
                }
            )

        st.dataframe(table_data, hide_index=True)

        player_stats_dict = {
            "Points": player.fantasy_points,
            "Targets": player.targets,
            "Receptions": player.receptions,
            "Rec Yards": player.rec_yards,
            "Rec TD": player.rec_td,
            "Rec Avg": player.rec_avg,
            "Long Rec": player.long_rec,
            "Two Point Conversions": player.two_point_conversions,
            "Rush Yards": player.rush_yards,
            "Rush TD": player.rush_td,
            "Rush Avg": player.rush_avg,
            "Long Rush": player.long_rush,
            "Fumbles": player.fumbles,
            "Pass Attempts": player.pass_attempts,
            "Pass Completions": player.pass_completions,
            "Pass Yards": player.pass_yds,
            "Pass TD": player.pass_td,
            "Pass Avg": player.pass_avg,
            "Interceptions": player.interceptions,
        }

        option = st.selectbox(
            "What would you like to sort by?",
            (list(player_stats_dict.keys())),
            label_visibility="collapsed",
            index=0,
            placeholder="Select sort metric",
        )

        chart_data = pd.DataFrame(
            {
                "Gameweek": range(1, len(completed_team_games) + 1),
                f"{option}": player_stats_dict[option]
            }
        )

        tab1, tab2, tab3 = st.tabs([f"{option} Per Week", "Scatterplot", "Player Comparison"])

        with tab1:
            ChartGenerator.altair_chart(chart_data, option)

        with tab2:
            ChartGenerator.scatter_plot(chart_data, option)

        with tab3:
            st.text_input("Compare player", key="compare_name")

            compare_name = input_handler(st.session_state.compare_name)

            chart_data2 = None

            if APICalls.valid_player(compare_name) is False:
                if compare_name == "":
                    st.write()
                else:
                    st.write("Player not found")

            else:

                player2 = APICalls.pull_player(compare_name)

                APICalls.pull_fantasy_info(player2, scoring_type)

                st.write(player2.name)

                completed_team_games2, all_team_games2 = APICalls.store_team_games(player2.team)

                chart_data2 = pd.DataFrame(
                    {
                        "Gameweek": range(1, len(completed_team_games2) + 1),
                        "Points": player.fantasy_points,
                        "Points2": player2.fantasy_points
                    }
                )
                if chart_data2 is not None:

                    ChartGenerator.altair_chart(chart_data2, option)
                else:
                    st.write("Whoops")

