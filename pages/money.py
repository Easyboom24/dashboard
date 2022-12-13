import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/money',title='Финансы')
df = pd.read_csv('stadiums.csv', encoding='windows-1251')
stadsUnique = df['name'].unique()
stadiums = df.loc[df['audience']!=0]
moneyDF = stadiums[['name','game','tour','audience']]
ticketPrice = pd.read_csv('tickets.csv', encoding='windows-1251')

for name, value in moneyDF.iterrows():
    if value['game'] == 'Катар - Эквадор':
        moneyDF.loc[name,'audience'] = float(value['audience'] * ticketPrice['class2'][0])/3.64
    elif 'Группа' in value['tour']:
        moneyDF.loc[name,'audience'] = float(value['audience'] * ticketPrice['class2'][1])/3.64
    elif '1/8' in value['tour']:
        moneyDF.loc[name,'audience'] = float(value['audience'] * ticketPrice['class2'][2])/3.64
    elif '1/4' in value['tour']:
        moneyDF.loc[name,'audience'] = float(value['audience'] * ticketPrice['class2'][3])/3.64
    elif '1/2' in value['tour']:
        moneyDF.loc[name,'audience'] = float(value['audience'] * ticketPrice['class2'][4])/3.64
    elif 'место' in value['tour']:
        moneyDF.loc[name,'audience'] = float(value['audience'] * ticketPrice['class2'][5])/3.64
    elif 'Финал' in value['tour']:
        moneyDF.loc[name,'audience'] = float(value['audience'] * ticketPrice['class2'][6])/3.64


newMoneyDF = moneyDF.groupby('name')['audience']

lines = go.Figure()
lines.add_trace(go.Bar(x=newMoneyDF.sum().values*10, y=newMoneyDF.sum().keys(), orientation='h'))
lines.update_layout(margin=dict(l=0, r=0, t=30, b=0),xaxis_range=[400000000,2000000000])
layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
            html.H3("Средняя выручка с прожади билетов по стадионам",style={'text-align': 'center'}),
            dcc.Graph(figure=lines)
            ],
                style={'border-radius':'15px','padding':'15px','margin':'20px','box-shadow':'10px 15px 5px #eaeaea'})
        ],width=12, style={'padding':'0','margin':'0'}),
    ], style={'margin':'0'})
], style={'height':'100vh'})


