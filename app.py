import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import requests
import base64
from bs4 import BeautifulSoup

external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.themes.GRID]
app = dash.Dash(__name__,meta_tags=[{"name": "viewport", "content": "width=device-width"}], external_stylesheets=external_stylesheets,)

colors = ['green','red']
res = requests.get("https://soccer365.ru/competitions/742/results/")
games = BeautifulSoup(res.text, 'html.parser').find_all("div",class_='game_block')


df = pd.read_csv('players_info.csv', encoding='windows-1251')
stadiums = pd.read_csv('stadiums.csv', encoding='windows-1251')
countries = df['country'].unique()
allGoals = df.loc[df['goals']>=0]['goals'].sum()
allYellowCards = df['yellow'].sum()
allRedCards = df['red'].sum()


stad = stadiums.loc[stadiums['audience']!=0]
allAudience = float(stad['audience'].sum()/1000000)
allAudience = float('{:.3}'.format(allAudience))
games = stadiums.loc[stadiums['score']!='– : –']

stadium1 = stad.loc[stad['name'] == 'Стэдиум 974', 'audience'].sum() / stad.loc[stad['name']== 'Стэдиум 974'].count()
capacity1 = stad.loc[stad['name'] == 'Стэдиум 974']['capacity'].head(1)[0]
stadium2 = stad.loc[stad['name'] == 'Халифа Интернейшнл', 'audience'].sum() / stad.loc[stad['name'] == 'Халифа Интернейшнл'].count()
capacity2 = stad.loc[stad['name'] == 'Халифа Интернейшнл']['capacity'].head(1)
stadium3 = stad.loc[stad['name'] == 'Ахмед бин Али', 'audience'].sum() / stad.loc[stad['name'] == 'Ахмед бин Али'].count()
capacity3 = stad.loc[stad['name'] == 'Ахмед бин Али']['capacity'].head(1)
stadium4 = stad.loc[stad['name'] == 'Лусаил Айконик', 'audience'].sum() / stad.loc[stad['name'] == 'Лусаил Айконик'].count()
capacity4 = stad.loc[stad['name'] == 'Лусаил Айконик']['capacity'].head(1)
stadium5 = stad.loc[stad['name'] == 'Эдьюкейшн Сити', 'audience'].sum() / stad.loc[stad['name'] == 'Эдьюкейшн Сити'].count()
capacity5 = stad.loc[stad['name'] == 'Эдьюкейшн Сити']['capacity'].head(1)
stadium6 = stad.loc[stad['name'] == 'Эль-Байт', 'audience'].sum() / stad.loc[stad['name'] == 'Эль-Байт'].count()
capacity6 = stad.loc[stad['name'] == 'Эль-Байт']['capacity'].head(1)
stadium7 = stad.loc[stad['name'] == 'Эль-Джануб', 'audience'].sum() / stad.loc[stad['name'] == 'Эль-Джануб'].count()
capacity7 = stad.loc[stad['name'] == 'Эль-Джануб']['capacity'].head(1)
stadium8 = stad.loc[stad['name'] == 'Эль-Тумама', 'audience'].sum() / stad.loc[stad['name'] == 'Эль-Тумама'].count()
capacity8 = stad.loc[stad['name'] == 'Эль-Тумама']['capacity'].head(1)

stadium1Pie = go.Figure(layout=go.Layout(height=350),
    data=go.Pie(marker=dict(colors=['#97db52','red']),
    labels=["Посещаемость","Свободные места"],
    values=[int(stadium1['audience']),int(capacity1-stadium1['audience'])]))
stadium1Pie.update_layout(annotations=[dict(text='Стадион "Стэдиум 974"', x=0.5, y=-0.3, font_size=20, showarrow=False)], showlegend=False)
stadium2Pie = go.Figure(layout=go.Layout(height=350), data=go.Pie(marker=dict(colors=['#97db52','red']),labels=["Посещаемость","Свободные места"],values=[int(stadium2['audience']),int(capacity2-stadium2['audience'])]))
stadium2Pie.update_layout(annotations=[dict(text='Стадион "Халифа Интернейшнл"', x=0.5, y=-0.3, font_size=20, showarrow=False)], showlegend=False)
stadium3Pie = go.Figure(layout=go.Layout(height=350), data = go.Pie(marker=dict(colors=['#97db52','red']),labels=["Посещаемость","Свободные места"],values=[int(stadium3['audience']),int(capacity3-stadium3['audience'])]))
stadium3Pie.update_layout(annotations=[dict(text='Стадион "Ахмед бин Али"', x=0.5, y=-0.3, font_size=20, showarrow=False)], showlegend=False)
stadium4Pie = go.Figure(layout=go.Layout(height=350), data=go.Pie(marker=dict(colors=['#97db52','red']),labels=["Посещаемость","Свободные места"],values=[int(stadium4['audience']),int(capacity4-stadium4['audience'])]))
stadium4Pie.update_layout(annotations=[dict(text='Стадион "Лусаил Айконик"', x=0.5, y=-0.3, font_size=20, showarrow=False)], showlegend=False)
stadium5Pie = go.Figure(layout=go.Layout(height=350), data = go.Pie(marker=dict(colors=['#97db52','red']),labels=["Посещаемость","Свободные места"],values=[int(stadium5['audience']),int(capacity5-stadium5['audience'])]))
stadium5Pie.update_layout(annotations=[dict(text='Стадион "Эдьюкейшн Сити"', x=0.5, y=-0.3, font_size=20, showarrow=False)], showlegend=False)
stadium6Pie = go.Figure(layout=go.Layout(height=350), data = go.Pie(marker=dict(colors=['#97db52','red']),labels=["Посещаемость","Свободные места"],values=[int(stadium6['audience']),int(capacity6-stadium6['audience'])]))
stadium6Pie.update_layout(annotations=[dict(text='Стадион "Эль-Байт"', x=0.5, y=-0.3, font_size=20, showarrow=False)], showlegend=False)
stadium7Pie = go.Figure(layout=go.Layout(height=350),data = go.Pie(marker=dict(colors=['#97db52','red']),labels=["Посещаемость","Свободные места"],values=[int(stadium7['audience']),int(capacity7-stadium7['audience'])]))
stadium7Pie.update_layout(annotations=[dict(text='Стадион "Эль-Джануб"', x=0.5, y=-0.3, font_size=20, showarrow=False)],showlegend=False)
stadium8Pie = go.Figure(layout=go.Layout(height=350),data=go.Pie(marker=dict(colors=['#97db52','red']),labels=["Посещаемость","Свободные места"],values=[int(stadium8['audience']),int(capacity8-stadium8['audience'])]))
stadium8Pie.update_layout(annotations=[dict(text='Стадион "Эль-Тумама"', x=0.5, y=-0.3, font_size=20, showarrow=False)],showlegend=False)
stadium1Pie.update_traces(textinfo='value')
stadium2Pie.update_traces(textinfo='value')
stadium3Pie.update_traces(textinfo='value')
stadium4Pie.update_traces(textinfo='value')
stadium5Pie.update_traces(textinfo='value')
stadium6Pie.update_traces(textinfo='value')
stadium7Pie.update_traces(textinfo='value')
stadium8Pie.update_traces(textinfo='value')

gamesPie = go.Figure(layout=go.Layout(height=400), data=go.Pie(marker=dict(colors=colors),labels=["Сыграно","Осталось"],values=[len(games),64-len(games)],hole=.9, textinfo='none'))
gamesPie.update_layout(annotations=[dict(text=f"{len(games)} из 64<br>матчей<br>сыграно", x=0.5, y=0.5, font_size=26, showarrow=False)],showlegend=False)

lines = go.Figure()
lines.add_trace(go.Bar(x=games['game'], y=games['audience'],))
lines.update_layout(margin=dict(l=0, r=0, t=30, b=0), yaxis_range=[30000,100000])

app.layout = html.Div(lang='RU', style={'backgroundColor':'#f5f2f5'}, children=[
    html.Div(
        dbc.Row([
            dbc.Col([
                dbc.Col(dbc.Card([html.B(f'{allAudience}M',style={'height':'50px'}),html.Span('зрителей', style={'font-size':'30px'})], 
                    style={'height':'200px','text-align':'center','justify-content':'center','border-radius':'15px','padding':'0', 'box-shadow': '10px 15px 5px #eaeaea'}), 
                style={'text-align':'center','font-size':'46px','margin':'20px'}),
                dbc.Col(dbc.Card([html.B(f'{(allGoals)}',style={'height':'50px'}),html.Span('голов', style={'font-size':'30px'})],
                    style={'height':'200px', 'text-align':'center','justify-content':'center', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}), 
                style={'text-align':'center', 'font-size':'46px','margin':'20px'}),
            ],width=3, style={'padding':'0'}),
            dbc.Col(dbc.Card(dcc.Graph(figure=gamesPie),
                style={'margin':'20px 10px','padding':'10px', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}),
            width=6, style={'padding':'0'}),
            dbc.Col([
                dbc.Col(dbc.Card([html.B(f'{allYellowCards}',style={'height':'50px'}), html.Span('желтых', style={'font-size':'30px'})], 
                    style={'height':'200px','text-align':'center', 'justify-content':'center', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}), 
                style={'text-align':'center', 'font-size':'46px','margin':'20px', 'padding':'0',}),
                dbc.Col(dbc.Card([html.B(f'{allRedCards}',style={'height':'50px'}), html.Span('красных', style={'font-size':'30px'})],
                    style={'height':'200px','text-align':'center', 'justify-content':'center', 'border-radius':'15px', 'box-shadow': '10px 15px 5px #eaeaea'}), 
                style={'text-align':'center', 'font-size':'46px','margin':'20px', 'padding':'0'}),
            ],width=3, style={'padding':'0'}),
        ],justify='center', align='center', style={'margin':'0', 'padding':'0'}), 
        style={'padding':'0', 'margin':'0'}
    ),
    html.Div([
        dbc.Card([
            dbc.Row([
                html.H3("Средняя посещаемость стадионов ЧМ-2022", style={'text-align': 'center','padding':'0'}),
                dbc.Col(dbc.Card(dcc.Graph(figure=stadium1Pie), style={'border-radius':'15px','padding':'4px','box-shadow':'10px 15px 5px #eaeaea'}), width=3),
                dbc.Col(dbc.Card(dcc.Graph(figure=stadium2Pie), style={'border-radius':'15px','padding':'4px','box-shadow':'10px 15px 5px #eaeaea'}), width=3),
                dbc.Col(dbc.Card(dcc.Graph(figure=stadium3Pie), style={'border-radius':'15px','padding':'4px','box-shadow':'10px 15px 5px #eaeaea'}), width=3),
                dbc.Col(dbc.Card(dcc.Graph(figure=stadium4Pie), style={'border-radius':'15px','padding':'4px','box-shadow':'10px 15px 5px #eaeaea'}), width=3)
            ], style={'margin': '0 0 20px 0'}),
            dbc.Row([ 
                dbc.Col(dbc.Card(dcc.Graph(figure=stadium5Pie), style={'border-radius':'15px','padding':'4px','box-shadow':'10px 15px 5px #eaeaea'}), width=3),
                dbc.Col(dbc.Card(dcc.Graph(figure=stadium6Pie), style={'border-radius':'15px','padding':'4px','box-shadow':'10px 15px 5px #eaeaea'}), width=3),
                dbc.Col(dbc.Card(dcc.Graph(figure=stadium7Pie), style={'border-radius':'15px','padding':'4px','box-shadow':'10px 15px 5px #eaeaea'}), width=3),
                dbc.Col(dbc.Card(dcc.Graph(figure=stadium8Pie), style={'border-radius':'15px','padding':'4px','box-shadow':'10px 15px 5px #eaeaea'}), width=3)
        ], style={'margin': '0 0 20px 0'}),
        ],  className="border-0 bg-transparent"),  
    ], style={'margin':'0'}),

    html.Div(
        dbc.Card([
            html.H3("Показатель посещаемости по матчам",style={'text-align': 'center'}),
            dcc.Graph(figure=lines)],style={'padding':'15px','margin':'20px','box-shadow':'10px 15px 5px #eaeaea', 'border-radius':'15px'}),
            
    ),
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
    ]),
])

@app.callback(
 	   Output('output_pie', 'figure'),
    [	Input('country_drop', 'value')]
)
def generate_pie_chart(value):
    allInCountry = df.loc[df['country']==value]
    result = allInCountry.loc[allInCountry['g+p']!=0]
    fig = px.pie(result,names=result['name'],values=result['g+p'],hole=.3)
    fig.update_traces(textinfo='value+percent')
    return fig


@app.callback(
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


if __name__ == '__main__':
    app.run_server(debug=True)
