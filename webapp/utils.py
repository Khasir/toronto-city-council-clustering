import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


default_text_style = {'textAlign': 'center', 'fontFamily': 'Roboto, Arial, sans-serif'}
df_cache = {}  # Serialized parameters -> Filename TODO


def reduce_dimensionality(df: pd.DataFrame, num_dimensions: int) -> pd.DataFrame:
    pca = PCA(n_components=num_dimensions)
    pca.fit(df)
    reduced_df = pca.transform(df)
    return reduced_df


def generate_clusters(df: pd.DataFrame, num_clusters: int, random_state: int) -> np.ndarray:
    kmeans = KMeans(n_clusters=num_clusters, random_state=random_state, n_init="auto").fit(df)
    return kmeans.labels_


def prepare_plotly_df(councillor_names: list, points: pd.DataFrame, clusters: np.ndarray) -> pd.DataFrame:
    # Prepare dataframe specifically for visualization
    plotly_rows = []

    if points.shape[1] == 3:
        headers = ['councillor', 'x', 'y', 'z', 'cluster', 'mayor']
    else:
        headers = ['councillor', 'x', 'y', 'cluster', 'mayor']
    past_mayors = 'Olivia Chow', 'John Tory', 'Rob Ford', 'David Miller'
    for i, name in enumerate(councillor_names):
        row = [name] + list(points[i])
        row.append(f"Cluster {clusters[i] + 1}")
        row.append('Was mayor' if name in past_mayors else 'Was not mayor')
        plotly_rows.append(row)
    plotly_df = pd.DataFrame(plotly_rows, columns=headers)
    return plotly_df


def create_figure(df: pd.DataFrame, num_dimensions: int) -> go.Figure:
    if num_dimensions == 3:
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
                'x': '',
                'y': '',
                'z': ''
            },
            category_orders={
                'mayor': ['Was mayor', 'Was not mayor'],
                'cluster': [f'Cluster {i + 1}' for i in range(num_dimensions)]
            }
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
            hover_name='councillor',
            color='cluster',
            symbol='mayor',
            width=None,
            height=600,
            hover_data={'x': False, 'y': False},
            opacity=0.75,
            labels={
                'x': '',
                'y': '',
            },
            category_orders={'mayor': ['Was mayor', 'Was not mayor']}
        ))
        # Workaround to hide axes
        figure.update_layout(
            scene={
                'xaxis': {
                    'nticks': 1,
                    'tickfont': {'size': 1},
                    'showticklabels': False,
                },
                'yaxis': {
                    'nticks': 1,
                    'tickfont': {'size': 1},
                    'showticklabels': False,
                    'visible': False,
                    'ticks': '',
                    'showline': False
                },
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

    return figure


def generate_graph(councillor_votes_df: pd.DataFrame, num_dimensions: int, num_clusters: int, random_state: int = 42) -> go.Figure:
    assert num_dimensions in (2, 3), "Currently only 2- and 3-dimensional graphs are supported."
    reduced_df = reduce_dimensionality(councillor_votes_df, num_dimensions)
    clusters = generate_clusters(reduced_df, num_clusters, random_state)
    plotly_df = prepare_plotly_df(councillor_votes_df.index.to_list(), reduced_df, clusters)
    figure = create_figure(plotly_df, num_dimensions)
    return figure
