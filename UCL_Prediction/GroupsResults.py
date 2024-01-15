from bs4 import BeautifulSoup
from GetContent import GetContent
from AssociationRanking import AssociationRanking
from SaveToFile import SaveToFile

class GroupsResults(GetContent):
    def scrape(self, year):
        content = self.get_content()

        if content:
            soup = BeautifulSoup(content, 'lxml')
            products = soup.find_all('div', class_='footballbox')

            for product in products:
                score = self.getScore(product)
                team_A = self.getTeamA(product)
                team_B = self.getTeamB(product)
                nationality = self.getNationality(product)

                if score is not None and team_A is not None and team_B is not None and nationality is not None:
                    #normalizing data
                    score_text = score.text.strip()
                    result = self.interpret_score(score_text)
                    team_A_text = self.strip(team_A)
                    team_B_text = self.strip(team_B)
                    nationalityA_text = team_A.find('img')['alt']
                    nationalityB_text = team_B.find_next('img')['alt']
                    rankA = self.relu_scaled(float(self.initAssociationRanking(nationalityA_text, year)))
                    rankB = self.relu_scaled(float(self.initAssociationRanking(nationalityB_text, year)))

                    #saving
                    to_file = f'{team_A_text}|{nationalityA_text}|{rankA}|{team_B_text}|{nationalityB_text}|{rankB}|{result}'
                    saveObject = SaveToFile()
                    saveObject.save(to_file)

    def getTeamA(self, product):
        team_A = product.find('th', class_='fhome')
        return team_A

    def getTeamB(self, product):
        team_B = product.find('th', class_='faway')
        return team_B

    def getNationality(self, product):
        nationality = product.find('span', class_='mw-image-border')
        return nationality

    def getScore(self, product):
        score = product.find('th', class_='fscore')
        return score

    def interpret_score(self, score):
        score_values = [int(value) for value in score.split("–")]
        if score_values[0] > score_values[1]:
            return 0
        elif score_values[0] == score_values[1]:
            return 1
        else:
            return 2

    def associationURL(self, year):
        if year < 2009:
            ranking = AssociationRanking(f"https://kassiesa.net/uefa/data/method3/crank{year}.html")
        elif 2009 <= year < 2018:
            ranking = AssociationRanking(f"https://kassiesa.net/uefa/data/method4/crank{year}.html")
        elif year >= 2018:
            ranking = AssociationRanking(f"https://kassiesa.net/uefa/data/method5/crank{year}.html")
        return ranking

    def strip(self, item):
        item = item.text.strip()
        return item

    def initAssociationRanking(self, nationality, year):
        ranking = self.associationURL(year)
        rank = ranking.scrape(nationality)
        return rank

    def relu_scaled(self, x):
        return max(0, x) / 100.0

