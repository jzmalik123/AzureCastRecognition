import openai
import os
from dotenv import load_dotenv

class OpenAIClient:


    def __init__(self, model="gpt-4"):
        """
        Initialize the OpenAI client.

        :param model: OpenAI model to use (e.g., "gpt-4" or "gpt-3.5-turbo").
        """
        load_dotenv()
        self.api_key = os.getenv('OPEN_AI_API_KEY')
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

    def get_artist_information(self, artist_name):
        """
        Fetch detailed information about an artist using OpenAI's API.

        :param artist_name: Name of the artist.
        :return: A string containing artist information or an error message.
        """
        prompt = (
            f"Provide detailed information about the artist '{artist_name}', including their career highlights, "
            "musical style, notable achievements, and any other relevant details. "
            "If there is no artist with this name, then return an empty string as content."
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
            return f"Error while fetching artist information: {e}"

    def get_song_information(self, song_title):
        """
        Fetch detailed information about a song using OpenAI's API.

        :param song_title: Title of the song.
        :return: A string containing song information or an error message.
        """
        prompt = (
            f"Provide detailed information about the song '{song_title}', including its release date, "
            "artist, genre, background story, and any notable achievements. "
            "If there is no song with this title, then return an empty string as content."
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
            return f"Error while fetching song information: {e}"

    def summarize_for_tweet(self, context):
        """
        Summarize the given context into a tweet format using OpenAI.

        :param context: Dictionary containing song_details, artist_details, and band_details.
        :return: A string containing the summarized tweet or an error message.
        """
        prompt = (
            "Based on the provided details, generate a concise and engaging tweet "
            "that highlights the song, artist, and band information. The tweet should be within 280 characters "
            "and formatted to capture attention. Use the following context:\n\n"
            f"Song Details: {context.get('song_details', 'N/A')}\n"
            f"Artist Details: {context.get('artist_details', 'N/A')}\n"
            f"Band Details: {context.get('band_details', 'N/A')}"
        )

        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a social media expert and music enthusiast."},
                    {"role": "user", "content": prompt},
                ],
            )
            tweet = response.choices[0].message.content.strip()
            if len(tweet) > 280:
                tweet = tweet[:277] + "..."  # Truncate if it exceeds the limit
            return tweet
        except Exception as e:
            return f"Error while summarizing for tweet: {e}"
