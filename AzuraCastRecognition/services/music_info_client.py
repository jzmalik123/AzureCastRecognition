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
        openai_summary = self.open_ai_client.get_artist_information(artist_name)

        return {
            "lastfm": lastfm_data,
            "wikipedia": wikipedia_summary,
            "openai": openai_summary
        }

    def get_song_data(self, artist_name, song_name):
        lastfm_data = self.lastfm_client.get_song_info(artist_name, song_name).get('track', {}).get('wiki', {}).get('content', None)
        openai_data = self.open_ai_client.get_song_information(song_name)

        return {
            "lastfm": lastfm_data,
            "openai": openai_data
        }

    def get_band_data(self, artist_name):
        open_ai_data = self.open_ai_client.get_band_information(artist_name)
        return {
            "open_ai": open_ai_data
        }

    def get_song_art_url(self, song_name, artist_name=None):
        """
        Fetch artwork URL for a song. Prioritizes album artwork, falls back to artist image.

        :param song_name: The name of the song.
        :param artist_name: The name of the artist (optional but recommended for better accuracy).
        :return: A string with the image URL or None if no image is available.
        """
        album_artwork = None
        artist_image = None

        # Step 1: Fetch song metadata to get album artwork
        try:
            song_info = (
                self.lastfm_client.get_song_info(artist_name, song_name)
                if artist_name
                else self.lastfm_client.get_song_info(song_name)
            )
            album_artwork = song_info.get('track', {}).get('album', {}).get('image', [{}])[-1].get('#text', None)
        except Exception as e:
            print(f"Error fetching song metadata from Last.fm: {e}")

        # Step 2: Fetch artist image if album artwork is unavailable
        if not album_artwork:
            try:
                artist_info = self.lastfm_client.get_artist_info(artist_name)
                artist_image = artist_info.get('artist', {}).get('image', [{}])[-1].get('#text', None)
            except Exception as e:
                print(f"Error fetching artist metadata from Last.fm: {e}")

        # Return album artwork if available, otherwise artist image
        return album_artwork or artist_image
