import altair as alt
import streamlit as st

class ChartGenerator:

    @classmethod
    def get_chart(cls, data):
        hover = alt.selection_single(
            fields=["Gameweek"],
            nearest=True,
            on="mouseover",
            empty="none"
        )

        lines = (
            alt.Chart(data, title="Points per game")
            .mark_line()
            .encode(
                x="Gameweek",
                y="Points"
            )
        )

        points = lines.transform_filter(hover).mark_circle(size=65)

        tooltips = (
            alt.Chart(data)
            .mark_rule()
            .encode(
                x="Gameweek",
                y="Points",
                opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                tooltip=[
                    alt.Tooltip("Gameweek", title="Gameweek"),
                    alt.Tooltip("Points", title="Points"),
                ],
            )
            .add_selection(hover)
        )
        return (lines + points + tooltips).interactive()
    @classmethod
    def line_chart(cls, data):
        return st.line_chart(data, x="Gameweek", y="Points")

    @classmethod
    def scatter_plot(cls, data):
        return st.scatter_chart(data, x="Gameweek", y="Points")

    @classmethod
    def altair_chart(cls, data):
        chart = cls.get_chart(data)
        return st.altair_chart(chart.interactive(), use_container_width=True)