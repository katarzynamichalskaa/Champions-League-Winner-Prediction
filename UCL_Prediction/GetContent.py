import requests

class GetContent():
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
