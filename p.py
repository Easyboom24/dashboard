import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import csv

res = requests.get("https://soccer365.ru/?c=competitions&a=tab_tablesorter_players&cp_ss=4355823&cl=0&page=1&size=0&col[1]=1&col[4]=0")
jsonPlayers = json.loads(res.text)['rows']
with open('players_info.csv', 'w', newline='') as file:
    headers = ['name','country','role','number','goals','passes','games','minutes',
    'g+p','penalties','doubles','hattrick','autogoals','yellow','doubleYellow','red','fairPlay']
    file_writer = csv.DictWriter(file, delimiter = ",", lineterminator="\r", fieldnames=headers)
    file_writer.writeheader()
    for player in jsonPlayers:
        playerHTML = BeautifulSoup(player[0], 'html.parser')
        name = playerHTML.find("span").text
        try:
            country = playerHTML.find_all("a")[1]['title']
        except:
            continue
        numberAndAmplua = playerHTML.find("div",attrs={"class":"tb_pl_club"}).text
        try:
            numAmpl = numberAndAmplua.split('#')[1].split(' ')
            number = numAmpl[0] or '-'
            amplua = numAmpl[1] or 'тренер'
        except IndexError:
            number = '-'
            amplua = 'тренер'
        goals = 0 if player[1] == "&nbsp;" else  int(player[1])
        passes = 0 if player[2] == "&nbsp;" else  int(player[2])
        games = 0 if player[3] == "&nbsp;" else  int(player[3])
        minutes = 0 if player[4] == "&nbsp;" else  int(player[4])
        goalPlusPass = 0 if player[5] == "&nbsp;" else  int(player[5])
        penalty = 0 if player[6] == "&nbsp;" else  int(player[6])
        doubles = 0 if player[7] == "&nbsp;" else  int(player[7])
        hattrick = 0 if player[8] == "&nbsp;" else  int(player[8])
        autogoal = 0 if player[9] == "&nbsp;" else  int(player[9])
        yellow = 0 if player[10] == "&nbsp;" else  int(player[10])
        twoYellow = 0 if player[11] == "&nbsp;" else  int(player[11])
        red = 0 if player[12] == "&nbsp;" else  int(player[12])
        fairPlay = 0 if player[13] == "&nbsp;" else  int(player[13])

        file_writer.writerow({'name':name,'country':country,'role':amplua,'number':number,'goals':goals,
        'passes':passes,'games':games,'minutes':minutes,'g+p': goalPlusPass,'penalties':penalty,'doubles':doubles,
        'hattrick':hattrick,'autogoals':autogoal,'yellow': yellow,'doubleYellow':twoYellow,'red':red,'fairPlay':fairPlay})
    file.close()