import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import string
from functions import r_scrapper, season_list, link_creator, team_stats_scrapper

base_url='https://www.transfermarkt.pl/uefa-champions-league/teilnehmer/pokalwettbewerb/CL/saison_id/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'}

ready_links=pd.read_csv('ready_team_links')
team_stats_scrapper(ready_links, headers)