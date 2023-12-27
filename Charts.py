import altair as alt
import streamlit as st


class ChartGenerator:

    @classmethod
    def get_chart(cls, data, option):
        hover = alt.selection_single(
            fields=["Gameweek"],
            nearest=True,
            on="mouseover",
            empty="none"
        )

        lines = (
            alt.Chart(data, title=f"{option} per game")
            .mark_line()
            .encode(
                x="Gameweek",
                y=f'{option}',
            )
        )

        points = lines.transform_filter(hover).mark_circle(size=65)

        tooltips = (
            alt.Chart(data)
            .mark_rule()
            .encode(
                x="Gameweek",
                y=f'{option}',
                opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                tooltip=[
                    alt.Tooltip("Gameweek", title="Gameweek"),
                    alt.Tooltip(f'{option}', title=f'{option}'),
                ],
            )
            .add_selection(hover)
        )

        return lines + points + tooltips
    @classmethod
    def line_chart(cls, data):
        return st.line_chart(data, x="Gameweek", y="Points")

    @classmethod
    def scatter_plot(cls, data, option):
        return st.scatter_chart(data, x="Gameweek", y=f"{option}")

    @classmethod
    def altair_chart(cls, data, option):
        chart = cls.get_chart(data, option)
        return st.altair_chart(chart, use_container_width=True)

    @classmethod
    def get_compare_chart(cls, data, name1, name2):
        hover = alt.selection_single(
            fields=["Gameweek"],
            nearest=True,
            on="mouseover",
            empty="none"
        )

        lines = (
            alt.Chart(data)
            .transform_fold(
                [f'{name1}', f'{name2}'],
                as_=['Player', 'Points']
            )
            .mark_line()
            .encode(
                x='Gameweek',
                y='Points:Q',
                color='Player:N'
            )
            .properties(title="Points per game")
        )

        points = lines.transform_filter(hover).mark_circle(size=65)

        tooltips = (
            alt.Chart(data)
            .mark_rule()
            .encode(
                x="Gameweek",
                y='Points:Q',
                opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                tooltip=[
                    alt.Tooltip("Gameweek", title="Gameweek"),
                    alt.Tooltip('Points:Q', title="Points")
                ],
            )
            .add_selection(hover)
        )

        return lines + points + tooltips

    @classmethod
    def compare_altair_chart(cls, data, name1, name2):
        chart = cls.get_compare_chart(data, name1, name2)
        return st.altair_chart(chart, use_container_width=True)