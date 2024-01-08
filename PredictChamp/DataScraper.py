import requests

class DataScraper:
    def __init__(self, url):
        self.url = url

    def get_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def scrape(self):
        content = self.get_content()
        if content:
            self.save_to_file()
            print(content)

    def save_to_file(self):
        return None

url_to_scrape = "https://pl.wikipedia.org/wiki/Liga_Mistrz%C3%B3w_UEFA"
scraper = DataScraper(url_to_scrape)
scraper.scrape()
