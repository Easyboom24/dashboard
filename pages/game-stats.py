import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/game-stats',title='Статистика игроков')
df = pd.read_csv('players_info.csv', encoding='windows-1251')
countries = df['country'].unique()

layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.H2("Доля показателя гол+пас по игрокам в выбранной сборной", style={'text-align': 'center'}),
                    dcc.Dropdown(countries, countries[3], id='country_drop', clearable=False),
                    dcc.Graph(id='output_pie')
            ], style={'border-radius':'15px', 'margin':'20px','box-shadow':'10px 15px 5px #eaeaea', 'padding':'10px'})], style={'padding':'0'}),
            dbc.Col([
                dbc.Card([
                    html.H2("Топ-10 игроков ЧМ-2022 по выбранным действиям", style={'text-align': 'center'}),
                    dcc.Dropdown(options=[
                        {'label':'Голы','value':'goals'},
                        {'label':'Пасы','value':'passes'},
                        {'label':'Гол+Пас','value':'g+p'},
                        {'label':'Желтые карточки','value':'yellow'},
                        {'label':'Красные карточки','value':'red'},
                    ],value='goals', id='action_drop', clearable=False),
                    dcc.Graph(id='output_h_bar'),
        ], style={'border-radius':'15px', 'margin':'20px','box-shadow':'10px 15px 5px #eaeaea', 'padding':'10px'})], style={'padding':'0'}),
        ], style={'margin':'0'})
    ])
], style={'height':'100vh','display':'flex','align-items':'center'})


@callback(
 	   Output('output_pie', 'figure'),
    [	Input('country_drop', 'value')]
)
def generate_pie_chart(value):
    allInCountry = df.loc[df['country']==value]
    result = allInCountry.loc[allInCountry['g+p']!=0]
    fig = px.pie(result,names=result['name'],values=result['g+p'],hole=.3)
    fig.update_traces(textinfo='value+percent')
    return fig


@callback(
 	   Output('output_h_bar', 'figure'),
    [	Input('action_drop', 'value')]
)
def generate_horizontal_bar(value):
    if value == 'yellow' or value == 'red':
        result = df.loc[df[value] != 0].sort_values(by=value, ascending=False)[:10]
    else:
        result = df.loc[df['role']!='вратарь'].sort_values(by=value, ascending=False)[:10]

    fig = px.bar(x=result[value] ,y=result['name'],orientation='h')
    fig.update_layout(yaxis=dict(autorange="reversed"),yaxis_title="Имя",xaxis_title="Показатель")
    return fig