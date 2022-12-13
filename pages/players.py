import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/players',title='Игроки')
df = pd.read_csv('players_info.csv', encoding='windows-1251')
countries = df['country'].unique()
players = df.loc[df['role']!='тренер']
playersCount = df.loc[df['role']!='тренер','country'].value_counts().reset_index()  # index -название страны, country - количество игроков

lines = go.Figure()
lines.add_trace(go.Bar(x=playersCount['index'], y=playersCount['country'],))
lines.update_layout(margin=dict(l=0, r=0, t=30, b=0),yaxis_range=[15,30])


layout = html.Div([
    dbc.Row([
        # dbc.Col([
        #     dbc.Card([
        #         dcc.Dropdown(countries, countries[0], id='country', clearable=False),
        #         html.Div(id='out_country')
        #     ],
        #         style={'border-radius':'15px','padding':'4px','margin':'20px','box-shadow':'10px 15px 5px #eaeaea'})
        # ],width=6, style={'padding':'0','margin':'0'}),

        dbc.Col([
            dbc.Card([
                html.H3('Сравнить двух игроков',style={'text-align':'center'}),
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(players['name'], players['name'][0], id='first_player', clearable=False),
                    ],width=6),
                    dbc.Col([
                        dcc.Dropdown(players['name'], players['name'][1], id='second_player', clearable=False),
                    ],width=6),
                ],style={'padding':'4px'}),
                html.Div(id='output_players')
                

            ],
                style={'border-radius':'15px','padding':'4px','margin':'20px','box-shadow':'10px 15px 5px #eaeaea'})
        ],width=12, style={'padding':'0','margin':'0'}),
    ], style={'margin':'0'})
], style={'height':'100vh'})


@callback(
 	   Output('output_players', 'children'),
    [	Input('first_player', 'value'),
        Input('second_player', 'value')]
)
def generate_stat_for_players(first_player,second_player):
    first = players.loc[players['name']==first_player]
    second = players.loc[players['name']==second_player]
    labels = ['Желтые','Дубли','Ассисты','Голы','Игры']
    f= first[['yellow','doubles','passes','goals','games']]
    s = second[['yellow','doubles','passes','goals','games']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name=first['name'].values[0],y=labels,x=f.values[0],orientation='h'))
    fig.add_trace(go.Bar(name=second['name'].values[0],y=labels,x=s.values[0],orientation='h'))
    fig.update_layout(title="Статистика игроков", title_x = 0.5,)
    return html.Div([
        html.Br(),
        html.B('Сборная'),html.Br(),
        html.Span(f'{first["country"].values[0]} - {second["country"].values[0]}'),
        html.Br(),
        html.B('Амплуа'),html.Br(),
        html.Span(f'{first["role"].values[0]} - {second["role"].values[0]}'),
        html.Br(),
        html.B('Минут на поле'),html.Br(),
        html.Span(f'{first["minutes"].values[0]}м. - {second["minutes"].values[0]}м.'),
        dcc.Graph(figure=fig, style={'height':'400px','margin':'0 10px','padding':'0','border-radius':'15px'})
    ],style={'text-align':'center','align-items':'center'})


# @callback(
#  	   Output('out_country', 'children'),
#     [	Input('country', 'value')]
# )
# def search_players(value):
#     nationalPlayers = players.loc[players['country']==value]

#     return  