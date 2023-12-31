from API import APICalls
from Charts import ChartGenerator
from NFLteam import Team
import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO


def input_handler(name):  # converts spaces to underscores
    norm_input = ""
    for c in name:
        if c == " ":
            c = "_"
        norm_input += c
    return norm_input


def mod_color(hex_code, contrast=10):  # add contrast to background image of headshot
    red = int(hex_code[1:3], 16)
    green = int(hex_code[3:5], 16)
    blue = int(hex_code[5:7], 16)

    red = max(0, min(255, red + contrast))
    green = max(0, min(255, green + contrast))
    blue = max(0, min(255, blue + contrast))

    adjusted_hex_code = f'#{red:02x}{green:02x}{blue:02x}'
    return adjusted_hex_code


def random_pixel(image_url):  # generate background image of headshot from headshot pixel
    response = requests.get(image_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Open the image using PIL
        image = Image.open(BytesIO(response.content))

        # Get the width and height of the image
        width, height = image.size

        # Define the coordinates for the lower middle portion
        right_x = int(width * 0.8)  # For example, selecting a point 90% towards the right
        lower_middle_y = int(height * 0.75)  # Adjust the ratio to fit the lower middle area

        # Get the color of the pixel further to the right
        pixel = image.getpixel((right_x, lower_middle_y))

        # Generate the hex code from the pixel's RGB values
        hex_code = '#{:02x}{:02x}{:02x}'.format(pixel[0], pixel[1], pixel[2])
        return mod_color(hex_code, 50)
    else:
        return "#FFFFFF"


if __name__ == '__main__':

    team_dict = {}

    team_data = APICalls.get_nfl_teams()

    for team in team_data["body"]:  # host all team info in team_dict, primarily to get team logo
        team_abv = team.get("teamAbv")
        team_instance = Team.from_api_response(team)
        team_dict[team_abv] = team_instance

    st.title("NFL Data Visualizer")

    col1, col2 = st.columns([4, 1])

    with col1:

        st.text_input("Player name", key="name")

        name = input_handler(st.session_state.name)

    with col2:
        scoring_type = st.radio(
            "Select Scoring Type:",
            ["PPR", "halfPPR", "standard"],
            label_visibility="collapsed",
            index=0
        )

    if APICalls.valid_player(name) is False:  # handles non-players and non-inputs
        if name == "":
            st.write()
        else:
            st.write("Player not found")

    else:
        player = APICalls.pull_player(name)
        APICalls.pull_fantasy_info(player, scoring_type)

        col1, col2, col3 = st.columns([2, 3, 1])

        with col1:
            hex_code = random_pixel(player.headshot)

            st.markdown(
                f"""
                    <div style="background-color: {hex_code}; padding: -500px; border-radius: 0px; display: inline-block;">
                    <img src="{player.headshot}" style="width: 100%; border-radius: 0px; object-fit: cover; height: 200px;">
                    </div>
                    """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <h1 style='margin-top: -30px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;'>
                    <span style='font-size: 36px;'>
                        {player.name} #{player.num}
                    </span>
                </h1>
                <h4 style='margin-top: -30px; margin-bottom: 0px;'>{team_dict[player.team].teamCity} {team_dict[player.team].teamName}</h2>
                <h4 style='margin-top: -30px; margin-bottom: 0px;'>{player.pos}</h2>
                <h4 style='margin-top: -30px; margin-bottom: 0px;'>{player.age} years old</h2>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<hr>", unsafe_allow_html=True)  # Adding a horizontal rule for separation

        with col3:
            st.image(team_dict[player.team].espnLogo1, width=80)

        completed_team_games, all_team_games = APICalls.store_team_games(player.team)

        # establish positional dataframes

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

        #generate table

        st.dataframe(table_data, hide_index=True)

        st.markdown("<hr>", unsafe_allow_html=True)  # Adding a horizontal rule for separation

        player_stats_dict = {  # allow variable inputs based on dropdown
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

        option = st.selectbox(  # dropdown menu
            "What would you like to sort by?",
            (list(player_stats_dict.keys())),
            label_visibility="collapsed",
            index=0,
            placeholder="Select sort metric",
        )

        chart_data = pd.DataFrame(
            {
                "Gameweek": range(1, len(completed_team_games) + 1),
                f"{option}": player_stats_dict[option],
            }
        )

        news_list = APICalls.player_news_stack(player, option, player_stats_dict)
        clickable_df = pd.DataFrame(news_list, columns=["Gameweek", "Points", "title", "link"])

        tab1, tab2, tab3 = st.tabs([f"{option} Per Week", "Scatterplot", "Player Comparison"])

        with tab1:
            ChartGenerator.altair_chart(chart_data, option, clickable_df)

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

                completed_team_games2, all_team_games2 = APICalls.store_team_games(player2.team)

                data = pd.DataFrame({
                    'Gameweek': range(1, len(completed_team_games) + 1),
                    f'{player.name}': player.fantasy_points,
                    f'{player2.name}': player2.fantasy_points,
                })

                ChartGenerator.compare_altair_chart(data, player.name, player2.name)

