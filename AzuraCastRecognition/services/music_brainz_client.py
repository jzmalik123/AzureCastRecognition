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

    def get_band_details(self, band_name):
        params = {
            "query": f"artist:{band_name}",
            "fmt": "json",
        }
        response = requests.get(f"{self.BASE_URL}/artist", headers=self.headers, params=params)
        data = response.json()

        for artist in data.get("artists", []):
            if artist.get("type") == "Group":
                return {
                    "id": artist.get("id"),
                    "name": artist.get("name"),
                    "country": artist.get("country"),
                    "tags": [tag["name"] for tag in artist.get("tags", [])],
                    "life_span": artist.get("life-span"),
                    "relations": artist.get("relations", []),
                }
        return None


    def get_artist_bands(self, artist_id):
        url = f"https://musicbrainz.org/ws/2/artist/{artist_id}"
        params = {"inc": "artist-rels", "fmt": "json"}
        response = requests.get(url, params=params)
        data = response.json()

        # Extract bands/groups the artist is a member of
        bands = [
            {
                "band_name": relation["artist"]["name"],
                "band_id": relation["artist"]["id"]
            }
            for relation in data.get("relations", [])
            if relation.get("type") == "member of band"
        ]
        return bands