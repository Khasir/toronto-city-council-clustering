import dash

from utils import default_text_style


dash.register_page(__name__)
default_text_style = {'textAlign': 'center', 'fontFamily': 'Roboto, Arial, sans-serif'}

layout = dash.html.Div([
    dash.html.H2("More Information", style=default_text_style),
    dash.html.P("This is info lorem ipsum etc etc", style=default_text_style),
    dash.html.P(dash.dcc.Link("Back to graph", href="/"), style=default_text_style),
])
