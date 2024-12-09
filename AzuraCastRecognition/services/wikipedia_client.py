import requests


class WikipediaClient:
    """
    A client for interacting with the Wikipedia API.
    """

    BASE_URL = "https://en.wikipedia.org/w/api.php"

    def __init__(self):
        pass

    def search(self, query):
        """
        Fetches the first paragraph of a Wikipedia page for the given query.

        :param query: The topic to search for.
        :return: Extracted summary text or error message.
        """
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": query,
        }
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            pages = data.get("query", {}).get("pages", {})
            for page_id, page_info in pages.items():
                if page_id != "-1":  # "-1" means no page found
                    return page_info.get("extract", '')
            return None
        except requests.RequestException as e:
            return None
