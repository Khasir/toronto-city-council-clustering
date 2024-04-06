import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Generate DF with the notebook provided: cluster_councillors.ipynb
try:
    df = pd.read_csv('./plotly_df.csv')
except FileNotFoundError:
    df = pd.read_csv('./notebooks/output/plotly_df.csv')

app = Dash(__name__)
server = app.server  # Workaround for gunicorn with Dash
app.layout = html.Div([
    html.H1(children="Toronto City Councillors by Voting Records", style={'textAlign': 'center', 'fontFamily': 'Roboto'}),
    html.P(children="Click and drag to rotate. Scroll to zoom.", style={'textAlign': 'center', 'fontFamily': 'Roboto'}),
    dcc.Graph(figure=px.scatter_3d(df, x='x', y='y', z='z', hover_name='councillor', color='cluster', symbol='mayor'))
])

if __name__ == '__main__':
    app.run(debug=True)
