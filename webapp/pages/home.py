import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.callbacks import Points, InputDeviceState

from utils import default_text_style, generate_graph


dash.register_page(__name__, path='/')

# Generate DF with the notebook provided: cluster_councillors.ipynb
try:
    df = pd.read_csv('./raw_councillor_df.csv', index_col=0)
except FileNotFoundError:
    df = pd.read_csv('../notebooks/output/raw_councillor_df.csv', index_col=0)

layout = dash.html.Div([
    dash.html.P(children="Councillors closer together vote together more often on municipal items.", style=default_text_style),
    dash.html.P(children="Hover over points. Click and drag to rotate. Scroll to zoom.", style=default_text_style),
    dash.dcc.Loading(
        dash.dcc.Graph(figure=generate_graph(df, 3, 5), id='figure-1', style={'width': '80%', 'height': '100%', 'margin': '0 auto', 'border': '0.5px black solid'}),
        type='default'
    ),
    dash.html.P(dash.dcc.Link("Explanation", href="/info"), style=default_text_style),
])
