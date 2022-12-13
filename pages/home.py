import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import requests
from bs4 import BeautifulSoup


dash.register_page(__name__, path='/', title="Общая статистика ЧМ-2022")


df = pd.read_csv('players_info.csv', encoding='windows-1251')
stadiums = pd.read_csv('stadiums.csv', encoding='windows-1251')
stad = stadiums.loc[stadiums['audience']!=0]
countries = df['country'].unique()
allGoals = df.loc[df['goals']>=0]['goals'].sum()
allYellowCards = df['yellow'].sum()
allRedCards = df['red'].sum()

colors = ['green','red']
res = requests.get("https://soccer365.ru/competitions/742/results/")
games = BeautifulSoup(res.text, 'html.parser').find_all("div",class_='game_block')

ticketPrice = pd.read_csv('tickets.csv', encoding='windows-1251')
amount = 0
for name, value in stad.iterrows():
    if value['game'] == 'Катар - Эквадор':
        amount = amount + value['audience'] * ticketPrice['class2'][0]
    elif 'Группа' in value['tour']:
        amount = amount + value['audience'] * ticketPrice['class2'][1]
    elif '1/8' in value['tour']:
        amount = amount + value['audience'] * ticketPrice['class2'][2]
    elif '1/4' in value['tour']:
        amount = amount + value['audience'] * ticketPrice['class2'][3]
    elif '1/2' in value['tour']:
        amount = amount + value['audience'] * ticketPrice['class2'][4]
    elif 'место' in value['tour']:
        amount = amount + value['audience'] * ticketPrice['class2'][5]
    elif 'Финал' in value['tour']:
        amount = amount + value['audience'] * ticketPrice['class2'][6]

amountDollars = float('{:.3}'.format(amount/3.64/100000000))

countPlayers = df.loc[df['role']!='тренер']['name'].count()

allAudience = float(stadiums.loc[stadiums['audience']!=0]['audience'].sum()/1000000)
allAudience = float('{:.3}'.format(allAudience))
gamesPie = go.Figure(layout=go.Layout(height=400), data=go.Pie(marker=dict(colors=colors),labels=["Сыграно","Осталось"],values=[len(games),64-len(games)],hole=.9, textinfo='none'))
gamesPie.update_layout(annotations=[dict(text=f"{len(games)} из 64<br>матчей<br>сыграно", x=0.5, y=0.5, font_size=26, showarrow=False)],showlegend=False)
layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Col(dcc.Link(
                    dbc.Card([html.B(f'{allAudience}M',style={'height':'50px'}),html.Span('зрителей', style={'font-size':'30px'})], 
                    style={'height':'200px','text-align':'center','justify-content':'center','border-radius':'15px','padding':'0', 'box-shadow': '10px 15px 5px #eaeaea'}),href='/audience', style={'text-decoration':'none','color':'black'}), 
                style={'text-align':'center','font-size':'46px','margin':'20px'}),
                dbc.Col(dcc.Link(
                    dbc.Card([html.B(f'{(allGoals)}',style={'height':'50px'}),html.Span('голов', style={'font-size':'30px'})],
                    style={'height':'200px', 'text-align':'center','justify-content':'center', 'border-radius':'15px','padding':'0', 'box-shadow': '10px 15px 5px #eaeaea'}),href='/game-stats', style={'text-decoration':'none','color':'black'}), 
                style={'text-align':'center', 'font-size':'46px','margin':'20px'}),
            ],width=3, style={'padding':'0'}),
            dbc.Col(dbc.Card(dcc.Graph(figure=gamesPie),
                style={'margin':'20px 10px','padding':'10px', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}),
            width=6, style={'padding':'0','height':'460px'}),
            dbc.Col([
                dbc.Col(dcc.Link(
                    dbc.Card([html.B(f'{allYellowCards}',style={'height':'50px'}), html.Span('желтых', style={'font-size':'30px'})], 
                    style={'height':'200px','text-align':'center', 'justify-content':'center', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}),href='/yellow-cards', style={'text-decoration':'none','color':'black'}),  
                style={'text-align':'center', 'font-size':'46px','margin':'20px', 'padding':'0',}),
                dbc.Col(dcc.Link(
                    dbc.Card([html.B(f'{allRedCards}',style={'height':'50px'}), html.Span('красных', style={'font-size':'30px'})],
                    style={'height':'200px','text-align':'center', 'justify-content':'center', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}),href='/red-cards', style={'text-decoration':'none','color':'black'}),   
                style={'text-align':'center', 'font-size':'46px','margin':'20px', 'padding':'0'}),
            ],width=3, style={'padding':'0'}),
        ],justify='center', align='center', style={'margin':'0', 'padding':'0'}),
        dbc.Row([
            dbc.Col(dcc.Link(
                dbc.Card([html.B(f'{amountDollars}млрд. $',style={'height':'60px'}), html.Span('в среднем с билетов', style={'font-size':'30px'})], 
                    style={'height':'200px','text-align':'center', 'justify-content':'center','margin':'20px', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}),href='/money', style={'text-decoration':'none','color':'black'}), 
                style={'text-align':'center', 'font-size':'46px','margin':'0px', 'padding':'0'}
            ,width=3),
            dbc.Col(dcc.Link(
                dbc.Card([html.B(f'32',style={'height':'50px'}), html.Span('сборных', style={'font-size':'30px'})], 
                    style={'height':'200px','text-align':'center', 'justify-content':'center','margin':'20px 20px 20px 10px', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}),href='/countries', style={'text-decoration':'none','color':'black'}), 
                style={'text-align':'center', 'font-size':'46px','margin':'0px', 'padding':'0',}
            , width=3),
            dbc.Col(dcc.Link(
                dbc.Card([html.B(f'{countPlayers}',style={'height':'50px'}), html.Span('игроков', style={'font-size':'30px'})], 
                    style={'height':'200px','text-align':'center', 'justify-content':'center','margin':'20px', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}),href='/players', style={'text-decoration':'none','color':'black'}), 
                style={'text-align':'center', 'font-size':'46px','margin':'0px', 'padding':'0',}
            , width=3),
            dbc.Col(
                dbc.Card([html.B(f'8',style={'height':'50px'}), html.Span('стадионов', style={'font-size':'30px'})], 
                    style={'height':'200px','text-align':'center', 'justify-content':'center','margin':'20px', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}), 
                style={'text-align':'center', 'font-size':'46px','margin':'0px', 'padding':'0',}
            , width=3),
        ],align='center', style={'margin':'0', 'padding':'0'}),
    ], style={'padding':'0', 'margin':'0','height':'100vh'}),
])