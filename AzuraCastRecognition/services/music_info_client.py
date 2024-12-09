from .wikipedia_client import *
from.last_fm_client import *
from .genius_client import *
from .music_brainz_client import *
from .open_ai_client import *

class MusicInfoClient:
    def __init__(self):
        self.lastfm_client = LastFmClient()
        self.musicbrainz_client = MusicBrainzClient()
        self.wikipedia_client = WikipediaClient()
        self.open_ai_client = OpenAIClient()


    def get_artist_data(self, artist_name):
        lastfm_data = self.lastfm_client.get_artist_info(artist_name).get('artist', {}).get('bio', {}).get('content', None)
        wikipedia_summary = self.wikipedia_client.search(artist_name)

        return {
            "lastfm": lastfm_data,
            "wikipedia": wikipedia_summary,
        }

    def get_song_data(self, artist_name, song_name):
        lastfm_data = self.lastfm_client.get_song_info(artist_name, song_name).get('track', {}).get('wiki', {}).get('content', None)

        return {
            "lastfm": lastfm_data
        }

    def get_band_data(self, artist_name):
        open_ai_data = self.open_ai_client.get_band_information(artist_name)
        return {
            "open_ai": open_ai_data
        }
