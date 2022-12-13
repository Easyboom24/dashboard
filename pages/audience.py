import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


dash.register_page(__name__, path='/audience',title='Статистика посещаемости')

stadiums = pd.read_csv('stadiums.csv', encoding='windows-1251')
stad = stadiums.loc[stadiums['audience']!=0]

games = stadiums.loc[stadiums['score']!='– : –']

sortedStads = stad.sort_values(by=['audience'], ascending=False)


lines = go.Figure()
lines.add_trace(go.Bar(x=games['game'], y=games['audience'],))
lines.update_layout(margin=dict(l=0, r=0, t=30, b=0), yaxis_range=[30000,100000])

layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
            html.H3("Показатель посещаемости по матчам",style={'text-align': 'center'}),
            dcc.Graph(figure=lines)],
                style={'border-radius':'15px','padding':'4px','margin':'20px','box-shadow':'10px 15px 5px #eaeaea'})
        ],width=7, style={'padding':'0'}),
        dbc.Col([
            dbc.Card([
                    html.H3("Средняя посещаемость стадионов", style={'text-align': 'center','padding':'0'}),
                    dcc.Dropdown(stad['name'].unique(), stad['name'][0], id='stadium_drop', clearable=False),
                    dcc.Graph(id='stadium_pie', style={'padding':'5px'})],style={'border-radius':'15px','margin':'20px','padding':'31px','box-shadow':'10px 15px 5px #eaeaea'})
        ],width=5, style={'padding':'0'}),
    ], style={'margin':'0'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.B('Наиболее посещаемый матч'),
                html.B(f"{sortedStads.iloc[0]['game']}",style={'height':'50px','font-size':'30px'}), 
                html.Span(f"{sortedStads.iloc[0]['audience']} зрителей", style={'font-size':'30px'})],
            style={'height':'200px','text-align':'center', 'justify-content':'center','margin':'5px 20px 0px 20px', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'})
        ],width=4, style={'padding':'0'}),
        dbc.Col([
           dbc.Card([
            html.B('Наименее посещаемый матч'),
            html.B(f"{sortedStads.iloc[-1]['game']}",style={'height':'50px', 'font-size':'30px'}), 
            html.Span(f"{sortedStads.iloc[-1]['audience']} зрителей", style={'font-size':'30px'})],
            style={'height':'200px','text-align':'center', 'justify-content':'center','margin':'5px 20px 0px 20px', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'})
        ],width=4, style={'padding':'0'}),
        dbc.Col([
            dbc.Card([
                html.B("Количество зрителей за прошедшие матчи на стадионе"),
                dcc.Dropdown(stad['name'].unique(), stad['name'][0], id='stadium_audience_drop', clearable=False, style={'margin':'5px','padding':'0 40px'}),
                html.Div(id='stadium_audience_output')
            ],style={'height':'200px','text-align':'center', 'justify-content':'center','margin':'5px 20px 0px 20px', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'})
        ],width=4, style={'padding':'0'}),
    ],style={'margin':'0'} ),
],style={'margin':'0', 'height':'100vh'})


@callback(
 	   Output('stadium_pie', 'figure'),
    [	Input('stadium_drop', 'value')]
)
def generate_pie_chart_stadium(value):
    stadium = stad.loc[stad['name'] == value, 'audience'].sum() / stad.loc[stad['name']== value].count()
    capacity = stad.loc[stad['name'] == value]['capacity'].head(1)
    fig = go.Figure(layout=go.Layout(height=350), data=go.Pie(marker=dict(colors=['#97db52','red']),labels=["Посещаемость","Свободные места"],values=[int(stadium['audience']),int(capacity-stadium['audience'])]))
    fig.update_layout(annotations=[dict(text=f'Стадион "{value}"', x=0.5, y=-0.3, font_size=20, showarrow=False)], showlegend=False)
    fig.update_traces(textinfo='value')
    return fig

@callback(
 	   Output('stadium_audience_output', 'children'),
    [	Input('stadium_audience_drop', 'value')]
)
def generate_audience_stadium(value):
    stadium = stad.loc[stad['name'] == value, 'audience'].sum()
    return html.Span(f"{stadium} зрителей",style={'font-size':'30px'})
