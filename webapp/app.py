from dash import Dash, html, page_container

from utils import default_text_style


app = Dash(__name__, use_pages=True)
app.title = "Toronto City Councillors by Voting Records"
server = app.server  # Workaround for gunicorn with Dash
default_text_style = {'textAlign': 'center', 'fontFamily': 'Roboto, Arial, sans-serif'}

app.layout = html.Div([
    html.H1(children="Toronto City Councillors by Voting Records", style=default_text_style),
    html.P(children="Last updated April 6, 2024.", style={'textAlign': 'center', 'fontFamily': 'Roboto, Arial, sans-serif', 'font-style': 'italic'}),
    page_container,
    html.Hr(style={'align': 'center', 'width': '15%', 'size': '0.5'}),
    html.P(
        children=[
            "Data from ",
            html.A("2006 – 2024", href="https://open.toronto.ca/dataset/members-of-toronto-city-council-voting-record/", target="_blank"),
            " // Made by ",
            html.A("Khasir", href="mailto:khasir.hean@gmail.com"),
            " 2024"
        ],
        style=default_text_style
    ),
])

if __name__ == '__main__':
    app.run(debug=True)
