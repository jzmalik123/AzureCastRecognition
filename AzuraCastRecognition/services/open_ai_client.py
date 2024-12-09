import openai

class OpenAIClient:

    API_KEY = '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'

    def __init__(self, model="gpt-4"):
        """
        Initialize the OpenAI client.

        :param model: OpenAI model to use (e.g., "gpt-4" or "gpt-3.5-turbo").
        """
        self.api_key = self.API_KEY
        self.model = model
        openai.api_key = self.api_key

    def get_band_information(self, artist_name):
        """
        Fetch band information for a given artist using OpenAI's API.

        :param artist_name: Name of the artist.
        :return: A string containing band information or an error message.
        """
        prompt = (
            f"Given the artist name '{artist_name}', provide details about their associated band(s). "
            "If they are solo, mention that as well. Provide clear and concise details."
            "If there is no artist with this name then return empty string as content"
        )

        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a music expert."},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error while fetching information: {e}"