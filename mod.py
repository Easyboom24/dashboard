from bs4 import BeautifulSoup
import csv
import requests
import pandas as pd

hdr = {'User-Agent': 'Mozila/5.0'}
res1 = requests.get("https://www.championat.com/football/_worldcup/tournament/4949/stadiums/10543/", headers=hdr)
res2 = requests.get("https://www.championat.com/football/_worldcup/tournament/4949/stadiums/1618/", headers=hdr)
res3 = requests.get("https://www.championat.com/football/_worldcup/tournament/4949/stadiums/9469/", headers=hdr)
res4 = requests.get("https://www.championat.com/football/_worldcup/tournament/4949/stadiums/10549/", headers=hdr)
res5 = requests.get("https://www.championat.com/football/_worldcup/tournament/4949/stadiums/9073/", headers=hdr)
res6 = requests.get("https://www.championat.com/football/_worldcup/tournament/4949/stadiums/10545/", headers=hdr)
res7 = requests.get("https://www.championat.com/football/_worldcup/tournament/4949/stadiums/10547/", headers=hdr)
res8 = requests.get("https://www.championat.com/football/_worldcup/tournament/4949/stadiums/1644/", headers=hdr)
responses = [res1,res2,res3,res4,res5,res6,res7,res8]

with open('stadiums.csv', 'w', newline='') as file:
    headers = ['name','tour','date','game','score','audience','capacity']
    file_writer = csv.DictWriter(file, delimiter = ",", lineterminator="\r", fieldnames=headers)
    file_writer.writeheader()
    for res in responses:
        stadium = BeautifulSoup(res.text,'html.parser')
        name = stadium.find('div',class_="entity-header__title-name").text.strip()
        table = stadium.find_all('table')[1].find('tbody').find_all('tr')
        capacity = stadium.find('ul', class_="entity-header__facts").find_all("li",recursive=False)[2].text.strip()
        cap = capacity.split('                            ')[1].split(' ')
        total = ''.join(cap[:2])
        for tr in table:
            trs = tr.find_all('td')
            info = trs[3].find('a')['title'].split('. ')[0].split(', ')
            try:
                date = info[1]
            except IndexError:
                date = trs[1].text.strip()
            try:
                audienceList = trs[5].text.strip().split(' ')
                audience = int(''.join(audienceList))
            except:
                audience = 0
            file_writer.writerow({'name':name,'tour':trs[0].text.strip(),'date':date,'game':info[0],
            'score':trs[3].find('span').text.strip(),'audience':audience,'capacity':total})
    file.close()
