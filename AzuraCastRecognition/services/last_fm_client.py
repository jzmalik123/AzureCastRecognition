import requests

class LastFmClient:
    BASE_URL = "http://ws.audioscrobbler.com/2.0/"
    API_KEY = '30e3d45ef05b0d5aca474922f9c3cc12'

    def __init__(self):
        self.api_key = self.API_KEY

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
