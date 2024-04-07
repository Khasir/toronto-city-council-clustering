import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html

# Generate DF with the notebook provided: cluster_councillors.ipynb
try:
    df = pd.read_csv('./plotly_df.csv')
except FileNotFoundError:
    df = pd.read_csv('./notebooks/output/plotly_df.csv')

app = Dash(__name__)
app.title = "Toronto City Councillors by Voting Records"
server = app.server  # Workaround for gunicorn with Dash
default_text_style = {'textAlign': 'center', 'fontFamily': 'Roboto'}
figure = go.Figure(px.scatter_3d(
    df,
    x='x',
    y='y',
    z='z',
    hover_name='councillor',
    color='cluster',
    symbol='mayor',
    width=None,
    height=600,
    hover_data={'x': False, 'y': False, 'z': False},
    opacity=0.75,
    labels={
        'x': 'x-axis',
        'y': 'y-axis',
        'z': 'z-axis'
    },
    category_orders={'mayor': ['Was mayor', 'Was not mayor']}
))
# Workaround to hide axes
figure.update_layout(
    scene={
        'xaxis': {
            'nticks': 1,
            'tickfont': {'size': 1}
        },
        'yaxis': {
            'nticks': 1,
            'tickfont': {'size': 1}
        },
        'zaxis': {
            'nticks': 1,
            'tickfont': {'size': 1}
        }
    },
    legend={
        'yanchor': 'top',
        'y': 0.95,
        'xanchor': 'left',
        'x': 0.05,
        'title': 'Legend'
    }
)

app.layout = html.Div([
    html.H1(children="Toronto City Councillors by Voting Records", style=default_text_style),
    html.P(children="Last updated April 6, 2024.", style={'textAlign': 'center', 'fontFamily': 'Roboto', 'font-style': 'italic'}),
    html.P(children="Click and drag to rotate. Scroll to zoom.", style=default_text_style),
    dcc.Graph(figure=figure, style={'width': '80%', 'height': '100%', 'margin': '0 auto', 'border': '0.5px black solid'}),
    html.P(children=["Data from ", html.A("2006 – 2024", href="https://open.toronto.ca/dataset/members-of-toronto-city-council-voting-record/"), " // Made by Khasir 2024"], style=default_text_style),
])

if __name__ == '__main__':
    app.run(debug=True)
