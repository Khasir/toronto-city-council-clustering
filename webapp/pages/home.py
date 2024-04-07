import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import default_text_style


dash.register_page(__name__, path='/')
# default_text_style = {'textAlign': 'center', 'fontFamily': 'Roboto, Arial, sans-serif'}

# Generate DF with the notebook provided: cluster_councillors.ipynb
try:
    df = pd.read_csv('./plotly_df.csv')
except FileNotFoundError:
    df = pd.read_csv('../notebooks/output/plotly_df.csv')

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
        'title': 'Legend',
        'font': {'family': 'Roboto,Arial'}
    }
)

layout = dash.html.Div([
    dash.html.P(children="Click and drag to rotate. Scroll to zoom.", style=default_text_style),
    dash.dcc.Graph(figure=figure, style={'width': '80%', 'height': '100%', 'margin': '0 auto', 'border': '0.5px black solid'}),
    dash.html.P(dash.dcc.Link("More info", href="/info", style=default_text_style), style=default_text_style),
    # dash.html.P(dash.html.A("More info", href="/info"), style=default_text_style)
])
