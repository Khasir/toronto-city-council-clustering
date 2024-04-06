import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Generate DF with the notebook provided: cluster_councillors.ipynb
df = pd.read_csv('./notebooks/output/plotly_df.csv')

app = Dash(__name__)
app.layout = html.Div([
    html.H1(children="Toronto City Councillors by Voting Records", style={'textAlign': 'center', 'fontFamily': 'Roboto'}),
    dcc.Graph(figure=px.scatter_3d(df, x='x', y='y', z='z', hover_name='councillor', color='cluster', symbol='mayor'))
])

if __name__ == '__main__':
    app.run(debug=True)
