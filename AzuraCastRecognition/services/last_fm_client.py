import requests

class LastFmClient:
    BASE_URL = "http://ws.audioscrobbler.com/2.0/"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_artist_info(self, artist_name):
        params = {
            "method": "artist.getinfo",
            "artist": artist_name,
            "api_key": self.api_key,
            "format": "json",
        }
        response = requests.get(self.BASE_URL, params=params)
        return response.json()

    def get_song_info(self, artist_name, track_name):
        params = {
            "method": "track.getinfo",
            "artist": artist_name,
            "track": track_name,
            "api_key": self.api_key,
            "format": "json",
        }
        response = requests.get(self.BASE_URL, params=params)
        return response.json()
