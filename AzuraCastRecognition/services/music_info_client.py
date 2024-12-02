from .wikipedia_client import *
from.last_fm_client import *
from .genius_client import *
from .music_brainz_client import *

class MusicInfoClient:
    def __init__(self, lastfm_api_key, genius_access_token):
        self.lastfm_client = LastFmClient(lastfm_api_key)
        self.musicbrainz_client = MusicBrainzClient()
        self.wikipedia_client = WikipediaClient()
        self.genius_client = GeniusClient(genius_access_token)

    def get_artist_data(self, artist_name):
        lastfm_data = self.lastfm_client.get_artist_info(artist_name)
        musicbrainz_data = self.musicbrainz_client.get_artist_info(artist_name)
        wikipedia_summary = self.wikipedia_client.search(artist_name)

        return {
            "lastfm": lastfm_data,
            "musicbrainz": musicbrainz_data,
            "wikipedia": wikipedia_summary,
        }

    def get_song_data(self, artist_name, song_name):
        lastfm_data = self.lastfm_client.get_song_info(artist_name, song_name)
        musicbrainz_data = self.musicbrainz_client.get_song_info(song_name)
        genius_data = self.genius_client.search_song(song_name)

        return {
            "lastfm": lastfm_data,
            "musicbrainz": musicbrainz_data,
            "genius": genius_data,
        }
