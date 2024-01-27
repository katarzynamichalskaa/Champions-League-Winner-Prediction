import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import string
import requests
from bs4 import BeautifulSoup

season_list=['2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015',
           '2016','2017','2018','2019','2020','2021','2022','2023']

def r_scrapper(base_url, headers, season_list):
    team_season_link = []
    for year in season_list:
        current_url = base_url+year
        r = requests.get(current_url, headers=headers)
        page_soup = BeautifulSoup(r.content, 'lxml')
        all_teams = page_soup.find_all("td", {"class": "zentriert no-border-rechts"})
        for single_team in all_teams:
            team_link = single_team.find("a")["href"]
            data_vector=[team_link,year]
            team_season_link.append(data_vector)
        time.sleep(10)
    teams_link_dataframe = pd.DataFrame(team_season_link, columns=['Team link','Year'],index=None)
    teams_link_dataframe.to_csv('links_to_convert')


def link_creator(base_url, dataframe):
    ready_links=[]
    for index, row in dataframe.iterrows():
        team_part=row['Team link']
        year=str(row['Year'])
        team_part=team_part.replace("startseite","kader")
        second_part='/plus/0/galerie/0?saison_id='
        #year=str(2005)
        full_url=base_url+team_part+second_part+year
        data_vector=[full_url,year]
        ready_links.append(data_vector)
    teams_link_dataframe = pd.DataFrame(ready_links, columns=['Team link', 'Year'], index=None)
    teams_link_dataframe.to_csv('ready_team_links')


def team_stats_scrapper(dataframe, headers):
    x=1
    teams_stats=[]
    stats_list=[]
    column_names = ['Team name','Year','GK_avg_age', 'GK_value', 'Def_avg_age', 'Def_value', 'Mid_avg_age', 'Mid_value', 'Att_avg_age','Att_value']


    for index, row in dataframe.iterrows():
        link=row['Team link']
        year=str(row['Year'])
        time.sleep(5.5)

        r = requests.get(link, headers=headers)
        page_soup = BeautifulSoup(r.content, 'lxml')

        print(link)
        team_name = page_soup.find("h1", {"class": "data-header__headline-wrapper data-header__headline-wrapper--oswald"}).text.strip()

        squad_details_box = page_soup.find("div", {"class": "large-4 columns"})
        table = squad_details_box.find("table")
        tr_table = table.find_all("tr")
        avg_age_stats = []
        formation_value_stats = []

        #transfermarkt is broken - in midfielder column there is no <tr>:)

        zenziert_values=table.find_all('td',{"class":"zentriert"})
        rechts_values=table.find_all('td',{"class":"rechts"})
        midfielder_avg_age=zenziert_values[3].text
        midfielder_value=rechts_values[3].text.replace("€", '').replace('m', '').replace('-','0')
        if "k" in midfielder_value:
            midfielder_value=midfielder_value.replace('k','')
            midfielder_value=float(midfielder_value)/1000



        print(table)
        for i in range(1, 4):
            table = tr_table[i]
            average_formation_age = table.find("td", {"class": "zentriert"}).text
            avg_age_stats.append(float(average_formation_age))
            formation_value = table.find("td", {"class": "rechts"}).text.replace("€", '').replace('m', '').replace('-','0')
            if "k" in formation_value:
                formation_value = formation_value.replace('k', '')
                formation_value = float(formation_value)/1000

            formation_value_stats.append(float(formation_value))

        values = [team_name, year, avg_age_stats[0], formation_value_stats[0], avg_age_stats[1], formation_value_stats[1], midfielder_avg_age, midfielder_value,
                  avg_age_stats[2], formation_value_stats[2]]
        stats_list.append(values)
        stats_df=pd.DataFrame(stats_list,columns=column_names)
        stats_df.to_csv("stats.csv")
        print("Zescrapowano już ",x," zespolow")
        x=x+1



















