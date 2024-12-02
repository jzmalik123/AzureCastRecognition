import requests

class GeniusClient:
    BASE_URL = "https://api.genius.com"

    def __init__(self, access_token):
        self.headers = {
            "Authorization": f"Bearer {access_token}"
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
