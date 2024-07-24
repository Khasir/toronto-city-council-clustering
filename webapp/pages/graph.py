import os

import dash
import pandas as pd

from utils import default_text_style, generate_graph, BLANK_PROFILE_PIC


dash.register_page(
    __name__,
    path='/',
    title='Toronto City Councillors by Voting Records',
    description="Visualize Toronto's city councillors based on how closely they vote with one another."
)

# Generate DF with the notebook provided: cluster_councillors.ipynb
try:
    raw_councillor_df = pd.read_csv('./raw_councillor_df.csv', index_col=0)
except FileNotFoundError:
    raw_councillor_df = pd.read_csv('../notebooks/output/raw_councillor_df.csv', index_col=0)
    # df = pd.read_csv('../notebooks/output/raw_councillor_df_absent_0.5_na_0.5.csv', index_col=0)

biographies_df = pd.read_csv('assets/biographies.csv')

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
        ], style={'width': '75%', 'display': 'inline-block', 'height': '100%'}),

        # Options
        dash.html.Div([
            dash.html.Div([
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
                ]),
                # Councillor list
                dash.html.Div([
                    dash.dcc.Dropdown(
                        [],
                        placeholder='Search for a councillor...',
                        id='councillor-dropdown',
                        maxHeight=300,
                        style={'fontFamily': 'Roboto, Arial, sans-serif'},
                    )
                ]),
                # Profile pic
                dash.html.Div([
                    dash.html.Img(
                        src=BLANK_PROFILE_PIC,
                        id='profile-picture',
                        width='100%',
                    )
                ]),
                # Biographical blurb
                dash.html.Div([''],
                    id='bio-text'
                )
            ], style={'width': '80%', 'height': '100%'}),
            dash.html.Div(None, style={'width': '5%', 'height': '100%'}),
            dash.html.Div([
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
                    tooltip={
                        'template': 'Click and drag',
                        'style': default_text_style
                    },
                    vertical=True,
                    verticalHeight=580,
                ),
            ], style={'width': '15%', 'height': '100%'})
        ], style={'width': '24%', 'height': '100%', 'display': 'flex'}),

    ], style={'width': '80%', 'height': '650px', 'display': 'flex', 'margin': '0 auto', 'border': '1px black solid', 'padding': '1em'}),
    dash.html.P(dash.dcc.Link("More info", href="/info"), style=default_text_style),
])

@dash.callback(
    dash.Output('figure-1', 'figure'),
    dash.Output('councillor-dropdown', 'options'),
    dash.Output('councillor-dropdown', 'value'),
    dash.Input('year-slider', 'value'),
    dash.Input('dimension-selector', 'value')
)
def update_figure(years: list, dimensions: int):
    min_year, max_year = min(years), max(years)
    figure, councillors = generate_graph(raw_councillor_df, dimensions, 1, min_year, max_year, return_councillors=True)
    dropdown_options = []
    councillors = set(councillors)
    for councillor in sorted(raw_councillor_df.index):
        disabled = councillor not in councillors
        option = {
            'label': councillor,
            'value': councillor,
            'disabled': disabled
        }
        dropdown_options.append(option)

    return figure, dropdown_options, None

@dash.callback(
    # dash.Output('figure-1', 'figure'),
    dash.Output('profile-picture', 'src'),
    dash.Output('bio-text', 'children'),
    dash.Input('councillor-dropdown', 'value')
)
def show_councillor_info(councillor: str):
    if councillor is None:
        return BLANK_PROFILE_PIC, ['']
        
    # Pic
    councillor_profile_pic = f'assets/{councillor}.jpg'

    # Text
    query = pd.DataFrame([councillor], columns=['councillor'])
    search_result = pd.merge(biographies_df, query, how='inner', left_on='Councillor', right_on='councillor')
    assert not search_result.empty
    bio_text = dash.html.P(
        search_result.iloc[0]['Biography'],
        style={'fontFamily': 'Roboto, Arial, sans-serif'},
    )

    # Link
    link = dash.html.P([
        dash.dcc.Link('More info ↗', href=search_result.iloc[0]['Wikipedia'], target='_blank'),
    ], style = default_text_style)

    # Children
    children = [bio_text, link]

    # Return
    if os.path.exists(councillor_profile_pic):
        return councillor_profile_pic, children
    return BLANK_PROFILE_PIC, children
