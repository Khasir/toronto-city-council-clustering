import dash

from utils import default_text_style


dash.register_page(__name__)

info_text = ''
with open('./pages/info.md', 'r', encoding='utf-8') as file:
    info_text = file.read()

layout = dash.html.Div([
    dash.html.H1("More Information", style=default_text_style),
    dash.dcc.Markdown(info_text, style={'fontFamily': 'Roboto, Arial, sans-serif', 'width': '50%', 'height': '100%', 'margin': '0 auto'}),
    dash.html.P(dash.dcc.Link("Back to graph", href="/"), style=default_text_style),
])
