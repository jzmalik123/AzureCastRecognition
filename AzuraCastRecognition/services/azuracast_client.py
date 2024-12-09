import requests

class AzuraCastClient:

    BASE_URL = "https://radioislanegra.org/api/"

    def __init__(self, api_key=''):
        """
        Initialize the AzuraCastClient.

        :param api_key: API key for authenticating requests.
        """
        self.base_url = self.BASE_URL.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {api_key}',  # Optional Bearer token
            'X-API-Key': api_key,                 # Add X-API-Key header
            'Content-Type': 'application/json',
        }

    def _make_request(self, method, endpoint, data=None, params=None):
        """
        A helper method for making HTTP requests.

        :param method: HTTP method (GET, POST, PUT, DELETE).
        :param endpoint: API endpoint to call (relative to the base URL).
        :param data: Request body (for POST/PUT).
        :param params: Query parameters (for GET).
        :return: JSON response or error message.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.request(
                method, url, headers=self.headers, json=data, params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {'error': str(e), 'status_code': getattr(e.response, 'status_code', None)}

    def now_playing(self):
        """
        Fetch the now playing information for all stations.

        :return: A list of dictionaries containing now playing data for all stations.
        """
        response = self._make_request('GET', '/nowplaying')
        if 'error' in response:
            return response

        # Parse the now playing data
        parsed_response = []
        for station in response:
            now_playing = station.get('now_playing', {})
            parsed_response.append({
                "station_name": station.get('station', {}).get('name', 'Unknown Station'),
                "song_id": now_playing.get('song', {}).get('id', ''),
                "title": now_playing.get('song', {}).get('title', ''),
                "artist": now_playing.get('song', {}).get('artist', ''),
                "album": now_playing.get('song', {}).get('album', ''),
                "art_url": now_playing.get('song', {}).get('art', ''),
                "duration": now_playing.get('duration', 0),
                "elapsed": now_playing.get('elapsed', 0),
                "remaining": now_playing.get('remaining', 0),
                "playlist": now_playing.get('playlist', '')
            })
        return parsed_response[0]
