import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


default_text_style = {'textAlign': 'center', 'fontFamily': 'Roboto, Arial, sans-serif'}
title_text_style = {'textAlign': 'center', 'fontFamily': 'Roboto, Arial, sans-serif', 'color': '#144475'}
CACHE_DIR = './.cache/'  # Contains cached Dataframes
BLANK_PROFILE_PIC = 'assets/blank-profile-picture-973460_640.png'
PAST_MAYORS = 'Olivia Chow', 'John Tory', 'Rob Ford', 'David Miller'


def reduce_dimensionality(df: pd.DataFrame, num_dimensions: int) -> pd.DataFrame:
    pca = PCA(n_components=num_dimensions)
    pca.fit(df)
    reduced_df = pca.transform(df)
    return reduced_df


def generate_clusters(df: pd.DataFrame, num_clusters: int, random_state: int) -> np.ndarray:
    kmeans = KMeans(n_clusters=num_clusters, random_state=random_state, n_init="auto").fit(df)
    return kmeans.labels_


def prepare_plotly_df(councillor_names: list, points: pd.DataFrame, clusters: np.ndarray, select_councillor: str = None) -> pd.DataFrame:
    """Prepare a dataframe specifically for visualization."""
    plotly_rows = []

    if points.shape[1] == 3:
        headers = ['Councillor', 'x', 'y', 'z', 'Cluster', 'Mayor', 'Selected', 'Colour']
    else:
        headers = ['Councillor', 'x', 'y', 'Cluster', 'Mayor', 'Selected', 'Colour']
    for i, name in enumerate(councillor_names):
        was_mayor = 'Was mayor' if name in PAST_MAYORS else 'Was not mayor'
        selected = True if name == select_councillor else False
        colour = 0
        if was_mayor == 'Was mayor':
            colour = 1
        if selected:
            colour = 2

        row = [name] + list(points[i])
        row.append(f"Cluster {clusters[i] + 1}")
        row.append(was_mayor)
        row.append(selected)
        row.append(colour)
        plotly_rows.append(row)
    plotly_df = pd.DataFrame(plotly_rows, columns=headers)
    return plotly_df


def create_figure(df: pd.DataFrame, num_dimensions: int) -> go.Figure:
    df['point_size'] = df['Mayor'].map(lambda x: 5 if x == 'Was mayor' else 3)
    if num_dimensions == 3:
        figure = go.Figure(px.scatter_3d(
            df,
            x='x',
            y='y',
            z='z',
            hover_name='Councillor',
            # color='Cluster',
            # color='Mayor',
            color='colour',
            symbol='Mayor',
            size='point_size',
            width=None,
            height=600,
            hover_data={'x': False, 'y': False, 'z': False, 'point_size': False, 'colour': False},
            opacity=0.75,
            labels={
                'x': '',
                'y': '',
                'z': ''
            },
            category_orders={
                'Mayor': ['Was mayor', 'Was not mayor'],
                # 'Cluster': [f'Cluster {i + 1}' for i in range(num_dimensions)]
            },
            # color_discrete_sequence=px.colors.qualitative.G10,
        ))
        # Workaround to hide axes
        figure.update_layout(
            scene={
                'xaxis': {
                    # 'nticks': 1,
                    'tickfont': {'size': 1},
                    # 'visible': False,
                },
                'yaxis': {
                    # 'nticks': 1,
                    # 'tickfont': {'size': 1},
                    'visible': False,
                },
                'zaxis': {
                    # 'nticks': 1,
                    # 'tickfont': {'size': 1},
                    'visible': False,
                }
            },
            legend={
                'yanchor': 'top',
                'y': 0.95,
                'xanchor': 'left',
                'x': 0.02,
                'title': 'Legend',
                'font': {'family': 'Roboto, Arial'}
            },
        )

    elif num_dimensions == 2:
        figure = go.Figure(px.scatter(
            df,
            x='x',
            y='y',
            hover_name='Councillor',
            # color='Cluster',
            # color='Mayor',
            color='colour',
            symbol='Mayor',
            size='point_size',
            width=None,
            height=600,
            hover_data={'x': False, 'y': False, 'point_size': False, 'colour': False},
            opacity=0.75,
            labels={
                'x': '',
                'y': '',
            },
            category_orders={'Mayor': ['Was mayor', 'Was not mayor']},
            # color_discrete_sequence=px.colors.qualitative.G10,
        ))
        figure.update_layout(
            xaxis={
                'visible': False,
                'showticklabels': False,
            },
            yaxis={
                'visible': False,
                'showticklabels': False,
            },
            legend={
                'yanchor': 'top',
                'y': 1.0,
                'xanchor': 'left',
                'x': -0.25,
                'title': 'Legend',
                'font': {'family': 'Roboto, Arial'}
            },
            plot_bgcolor='white',
            # plot_bgcolor='#ebdec7',
        )

    return figure


def serialize_for_cache(num_dimensions: int, num_clusters: int, min_year: int, max_year: int) -> str:
    serialized = f'nd-{num_dimensions}-nc-{num_clusters}-{min_year}-{max_year}.csv'
    return serialized


def load_df_cache(num_dimensions: int, num_clusters: int, min_year: int, max_year: int) -> pd.DataFrame:
    """Return the dictionary containing references to the cached Dataframes."""
    try:
        cached_files = os.listdir(CACHE_DIR)
    except FileNotFoundError:
        return None
    serialized = serialize_for_cache(num_dimensions, num_clusters, min_year, max_year)
    if serialized in cached_files:
        return pd.read_csv(os.path.join(CACHE_DIR, serialized))
    return None


def cache_df(df: pd.DataFrame, num_dimensions: int, num_clusters: int, min_year: int, max_year: int) -> None:
    """Cache a Dataframe, overwriting any existing one."""
    serialized = serialize_for_cache(num_dimensions, num_clusters, min_year, max_year)
    os.makedirs(CACHE_DIR, exist_ok=True)
    df.to_csv(os.path.join(CACHE_DIR, serialized))


def generate_graph(councillor_votes_df: pd.DataFrame, num_dimensions: int, num_clusters: int, min_year: int, max_year: int, select_councillor: str = None, random_state: int = 42, return_councillors: bool = False) -> go.Figure:
    """
    Generate a figure for Plotly/Dash.

    Args:
        councillor_votes_df (pd.DataFrame): DataFrame containing councillor votes, where rows are councillors and columns are voting records.
        num_dimensions (int): Number of dimensions to generate the figure in.
        num_clusters (int): Number of clusters to group the councillors into.
        min_year (int): Only consider voting records from this year and later.
        max_year (int): Only consider voting records from this year and earlier.
        select_councillor (str, optional): Selected councillor to highlight.
        random_state (int, optional): Random seed for clustering. Defaults to 42.
        return_councillors (bool, optional): Also return a Series of the councillor names. Defaults to False.

    Returns:
        go.Figure: The figure for display on Plotly/Dash.
        pandas.Series (optional): List of councillors in the figure.
    """
    assert num_dimensions in (2, 3), "Only 2- and 3-dimensional graphs are supported."

    plotly_df = load_df_cache(num_dimensions, num_clusters, min_year, max_year)
    if plotly_df is None:
        # Limit agenda items to min and max years
        columns_to_drop = []
        for column in councillor_votes_df:
            year = int(column[:4])  # The year is encoded in the agenda item name
            if not (min_year <= year <= max_year):
                columns_to_drop.append(column)
        councillor_votes_filtered_years_df = councillor_votes_df.drop(columns=columns_to_drop)

        # Drop councillors who did not vote in the years applicable
        # TODO for now, we'll drop if absent as well. We should try to keep absences and only drop N/A in the future.
        councillors_to_drop = []
        for councillor_name in councillor_votes_filtered_years_df.index:
            if councillor_votes_filtered_years_df.loc[councillor_name].isin([-1.]).all():  # -1 -> N/A or absent
                councillors_to_drop.append(councillor_name)
        councillor_votes_filtered_years_df.drop(index=councillors_to_drop, inplace=True)

        # Process for visualization
        reduced_df = reduce_dimensionality(councillor_votes_filtered_years_df, num_dimensions)
        clusters = generate_clusters(reduced_df, num_clusters, random_state)
        plotly_df = prepare_plotly_df(councillor_votes_filtered_years_df.index.to_list(), reduced_df, clusters)
        cache_df(plotly_df, num_dimensions, num_clusters, min_year, max_year)

    # Add colour here based on mayors and councillor selected
    plotly_df['selected'] = np.where(plotly_df['Councillor'] == select_councillor, True, False)
    plotly_df['colour'] = '0'#'#1F77B4'
    plotly_df['colour'] = np.where(plotly_df['Mayor'] == 'Was mayor', '1', plotly_df['colour'])
    plotly_df['colour'] = np.where(plotly_df['selected'], '2', plotly_df['colour'])

    # Prepare figure for display
    figure = create_figure(plotly_df, num_dimensions)
    if return_councillors:
        return figure, plotly_df['Councillor']
    return figure
