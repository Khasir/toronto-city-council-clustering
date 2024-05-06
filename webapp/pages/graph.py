import dash
import pandas as pd

from utils import default_text_style, generate_graph


dash.register_page(
    __name__,
    path='/',
    title='Toronto City Councillors by Voting Records',
    description="Visualize Toronto's city councillors based on how closely they vote with one another."
)

# Generate DF with the notebook provided: cluster_councillors.ipynb
try:
    df = pd.read_csv('./raw_councillor_df.csv', index_col=0)
except FileNotFoundError:
    df = pd.read_csv('../notebooks/output/raw_councillor_df.csv', index_col=0)
    # df = pd.read_csv('../notebooks/output/raw_councillor_df_absent_0.5_na_0.5.csv', index_col=0)

layout = dash.html.Div([
    dash.html.Div([
        dash.html.P(children="Councillors closer together vote together more often on municipal items.", style=default_text_style),
        dash.html.P(children="Click and drag to rotate. Scroll to zoom. Right-click and drag to pan.", style=default_text_style),
    ]),

    # Figure, buttons and sliders
    dash.html.Div([

        # Main graph
        dash.html.Div([
            dash.dcc.Loading(
                dash.dcc.Graph(
                    id='figure-1',
                    style={'border': '0.5px black dotted'}
                    # style={'width': '80%', 'height': '100%', 'margin': '0 auto', 'border': '0.5px black solid'}
                ),
                type='dot'
            ),
        ], style={'width': '89%', 'display': 'inline-block'}),

        # Options
        dash.html.Div([
            # 2D / 3D
            dash.dcc.RadioItems([
                    {'label': '2D', 'value': 2},
                    {'label': '3D', 'value': 3},
                    # {'label': '4D', 'value': 4, 'disabled': True, 'title': 'JK'}
                ],
                value=2,
                id='dimension-selector',
                labelStyle=default_text_style
            ),
            # Year slider
            dash.dcc.RangeSlider(
                2009, 2024, 1,
                value=[2014, 2023],
                id='year-slider',
                marks={
                    year: {'label': str(year), 'style': default_text_style} for year in range(2009, 2025)
                    # 2009: {'label': '2009', 'style': default_text_style},
                    # 2010: {'label': '2010', 'style': default_text_style},
                    # 2011: {'label': '2011', 'style': default_text_style},
                    # 2012: {'label': '2012', 'style': default_text_style},
                    # 2013: {'label': '2013', 'style': default_text_style},
                    # 2014: {'label': '2014', 'style': default_text_style},
                    # 2015: {'label': '2015', 'style': default_text_style},
                    # 2016: {'label': '2016', 'style': default_text_style},
                    # 2017: {'label': '2017', 'style': default_text_style},
                    # 2018: {'label': '2018', 'style': default_text_style},
                    # 2019: {'label': '2019', 'style': default_text_style},
                    # 2020: {'label': '2020', 'style': default_text_style},
                    # 2021: {'label': '2021', 'style': default_text_style},
                    # 2022: {'label': '2022', 'style': default_text_style},
                    # 2023: {'label': '2023', 'style': default_text_style},
                    # 2024: {'label': '2024', 'style': default_text_style},
                },
                vertical=True,
            ),
        ], style={'width': '9%', 'height': '100%', 'display': 'grid'}),

    ], style={'width': '80%', 'display': 'flex', 'margin': '0 auto', 'border': '1px black solid', 'padding': '1em'}),
    dash.html.P(dash.dcc.Link("More info", href="/info"), style=default_text_style),
])

@dash.callback(
    dash.Output('figure-1', 'figure'),
    dash.Input('year-slider', 'value'),
    dash.Input('dimension-selector', 'value')
)
def update_figure(years: list, dimensions: int):
    min_year, max_year = min(years), max(years)
    figure = generate_graph(df, dimensions, 5, min_year, max_year)
    return figure
