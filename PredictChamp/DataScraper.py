import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import os
import re

class DataScraper:
    def __init__(self, url):
        self.url = url

    def get_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.text

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def scrape(self):

        content = self.get_content()

        if content:
            soup = BeautifulSoup(content, 'lxml')
            products = soup.find_all('div', class_='footballbox')

            for product in products:

                score_element = product.find('th', class_='fscore')
                team_A = product.find('th', class_='fhome')
                team_B = product.find('th', class_='faway')

                if score_element is not None and team_A is not None and team_B is not None:

                    score_text = score_element.text.strip()

                    result = self.interpret_score(score_text)

                    team_A_text = team_A.text.strip()
                    team_B_text = team_B.text.strip()
                    to_file = f'{team_A_text}|{team_B_text}|{result}'
                    self.save_to_file(to_file)


    def interpret_score(self, score):

        score_values = [int(value) for value in score.split("–")]

        if score_values[0] > score_values[1]:
            return 0
        elif score_values[0] == score_values[1]:
            return 1
        else:
            return 2

    def save_to_file(self, text_to_save):
        cleaned_text = re.sub(r'[^a-zA-Z0-9| ]', '', text_to_save)
        df = pd.read_csv(StringIO(cleaned_text), sep='|', header=None, names=['teamA', 'teamB', 'score'])
        file_path = f'SEASONS20052023.csv'
        df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)


years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

for year in years:
    url_to_scrape = f"https://en.wikipedia.org/wiki/{year}%E2%80%93{str((year + 1))[-2:]}_UEFA_Champions_League_group_stage?fbclid=IwAR1e5VgehDiy3rmX4QJAWOpNecrLKPgOIt-NCgrCEuV0zclPVTyqZh706Ro"
    scraper = DataScraper(url_to_scrape)
    scraper.scrape()
