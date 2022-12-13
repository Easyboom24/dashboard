import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/countries',title='Сборные')
df = pd.read_csv('players_info.csv', encoding='windows-1251')
countries = df['country'].unique()
playersCount = df.loc[df['role']!='тренер','country'].value_counts().reset_index()  # index -название страны, country - количество игроков



lines = go.Figure()
lines.add_trace(go.Bar(x=playersCount['index'], y=playersCount['country'],))
lines.update_layout(margin=dict(l=0, r=0, t=30, b=0),yaxis_range=[15,30])


layout = html.Div([
    dbc.Row([
        dbc.Col([
        dbc.Card([
            html.H3('Показатели выбранной сборной', style={'text-align':'center'}),
            dcc.Dropdown(countries, countries[3], id='input_country', clearable=False,style={'margin':'5px'}),
            html.Div(id='output_country', style={'margin':'0','padding':'0'}),
        ], style={'border-radius':'15px','padding':'4px','margin':'5px 20px','box-shadow':'10px 15px 5px #eaeaea'}),
    ], style={'padding':'0','margin':'0'})
    ], style={'margin':'0'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
            html.H3("Количество игроков в сборных",style={'text-align': 'center'}),
            dcc.Graph(figure=lines)
            ],
                style={'border-radius':'15px','padding':'3px','margin':'5px 20px','box-shadow':'10px 15px 5px #eaeaea'})
        ], style={'padding':'0','margin':'0'}),
    ], style={'margin':'0'})
], style={'height':'100vh'})




@callback(
 	   Output('output_country', 'children'),
    [	Input('input_country', 'value')]
)
def generate_pie_chart(value):
    allInCountry = df.loc[df['country']==value]
    goals = allInCountry.loc[allInCountry['goals']>=0]['goals'].sum()
    games = allInCountry['games'].max()
    selfGoals = allInCountry.loc[allInCountry['goals']<=0]['goals'].sum()
    yellowCards = allInCountry['yellow'].sum()

    return dbc.Row([
        dbc.Col([
            dbc.Card(dbc.Card([html.B(f'{goals}',style={'height':'45px'}), html.Span('забитых голов', style={'font-size':'30px'})], 
                style={'text-align':'center', 'justify-content':'center', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}), 
            style={'text-align':'center','border':'none', 'font-size':'46px','margin':'20px 5px', 'padding':'0',})
        ],width=3, style={'padding':'0','margin':'0'}),
        dbc.Col([
            dbc.Card(dbc.Card([html.B(f'{games}',style={'height':'45px'}), html.Span('сыгранных матчей', style={'font-size':'30px'})], 
                style={'text-align':'center', 'justify-content':'center', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}), 
            style={'text-align':'center','border':'none', 'font-size':'46px','margin':'20px 5px', 'padding':'0',})
        ],width=3, style={'padding':'0','margin':'0'}),
        dbc.Col([
            dbc.Card(dbc.Card([html.B(f'{selfGoals*-1}',style={'height':'45px'}), html.Span('пропущенных мячей', style={'font-size':'30px'})], 
                style={'text-align':'center', 'justify-content':'center', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}), 
            style={'text-align':'center','border':'none', 'font-size':'46px','margin':'20px 5px', 'padding':'0',})
        ],width=3, style={'padding':'0','margin':'0'}),
        dbc.Col([
            dbc.Card(dbc.Card([html.B(f'{yellowCards}',style={'height':'45px'}), html.Span('желтых карточек', style={'font-size':'30px'})], 
                style={'text-align':'center', 'justify-content':'center', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}), 
            style={'text-align':'center','border':'none', 'font-size':'46px','margin':'20px 5px', 'padding':'0',})
        ],width=3, style={'padding':'0','margin':'0'}),
    ], style={'margin':'0'})
