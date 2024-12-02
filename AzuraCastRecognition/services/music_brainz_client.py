import requests

class MusicBrainzClient:
    BASE_URL = "https://musicbrainz.org/ws/2"

    def __init__(self):
        self.headers = {
            "User-Agent": "DjangoMusicApp/1.0 (youremail@example.com)"
        }

    def get_artist_info(self, artist_name):
        params = {
            "query": artist_name,
            "fmt": "json",
        }
        response = requests.get(f"{self.BASE_URL}/artist/", headers=self.headers, params=params)
        return response.json()

    def get_song_info(self, recording_name):
        params = {
            "query": recording_name,
            "fmt": "json",
        }
        response = requests.get(f"{self.BASE_URL}/recording/", headers=self.headers, params=params)
        return response.json()
