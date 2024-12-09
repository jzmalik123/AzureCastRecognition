import requests

class GeniusClient:
    BASE_URL = "https://api.genius.com"
    ACCESS_TOKEN = "YvJeSEH6ns1GHj0JRkUt3UN0wYoR7Zbyb07CZ8SYcJcd5GJ9xzxylM6n9w2QLfex"

    def __init__(self):

        self.headers = {
            "Authorization": f"Bearer {self.ACCESS_TOKEN}"
        }

    def search_song(self, song_title):
        params = {
            "q": song_title,
        }
        response = requests.get(f"{self.BASE_URL}/search", headers=self.headers, params=params)
        return response.json()

    def get_song_lyrics(self, song_id):
        response = requests.get(f"{self.BASE_URL}/songs/{song_id}", headers=self.headers)
        return response.json()
