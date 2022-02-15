from dash import Dash, html, dcc, Input, Output
import altair as alt
from vega_datasets import data


# Read in global data
countries = data.countries()

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
                    className="line-graph",
                    id="scatter",
                ),
                dcc.Dropdown(
                    className="dropdown",
                    id="xcol-widget",
                    value="country",  # REQUIRED to show the plot on the first page load
                    options=[
                        {"label": col, "value": col}
                        for col in countries.columns
                    ],
                ),
            ],
        ),
    ]
)

# Set up callbacks/backend
@app.callback(Output("scatter", "srcDoc"), Input("xcol-widget", "value"))
def plot_altair(xcol):
    chart = (
        alt.Chart(countries)
        .mark_point()
        .encode(x=xcol, y="year", tooltip="country")
        .interactive()
    )
    return chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)
