from dash import Dash, html, dcc, Input, Output
import altair as alt
import pandas as pd
from vega_datasets import data


# Read in global data
url = "https://raw.githubusercontent.com/UofTCoders/workshops-dc-py/master/data/processed/world-data-gapminder.csv"
gm = pd.read_csv(url, parse_dates=["year"])


def plot_altair(xmax):
    chart = (
        alt.Chart(
            gm[gm["year"] == str(xmax) + "-01-01"],
            title="Year " + str(xmax),
        )
        .mark_circle()
        .encode(
            alt.X(
                "children_per_woman",
                title="Children per Woman",
                scale=alt.Scale(domain=[0, 9]),
            ),
            alt.Y(
                "life_expectancy",
                scale=alt.Scale(domain=[0, 90]),
                title="Life Expectancy",
            ),
            alt.Color("region", title="Region"),
            alt.Size(
                "population",
                title="Population",
                scale=alt.Scale(range=(20, 1000)),
            ),
        )
        .configure_axis(titleFontSize=14)
    )
    return chart.to_html()


# Setup app and layout/frontend
app = Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            className="app-header",
            children=[
                html.Div("Gapminder Dashboard", className="app-header--title")
            ],
        ),
        html.Div(
            className="plot",
            children=[
                html.Iframe(
                    className="bubble-chart",
                    id="scatter",
                ),
                dcc.Slider(
                    className="slider",
                    id="xslider",
                    min=1800,
                    max=2000,
                    updatemode="drag",
                    value=1950,
                    # step=10,
                    marks={i: str(i) for i in range(1800, 2010, 20)},
                ),
            ],
        ),
    ]
)

# Set up callbacks/backend
@app.callback(Output("scatter", "srcDoc"), Input("xslider", "value"))
def update_output(xmax):
    return plot_altair(xmax)


if __name__ == "__main__":
    app.run_server(debug=True)
