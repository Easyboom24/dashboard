import dash
from dash import html
import dash_bootstrap_components as dbc


external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.themes.GRID]
app = dash.Dash(__name__,use_pages=True,meta_tags=[{"name": "viewport", "content": "width=device-width"}], external_stylesheets=external_stylesheets)

app.layout = html.Div(lang='RU', style={'backgroundColor':'#f5f2f5','height':'100vh'}, children=[
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)
