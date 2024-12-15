import requests
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

from .services.azuracast_client import AzuraCastClient
from .services.music_info_client import MusicInfoClient
from .services.open_ai_client import *
import tweepy
import os
import json
from dotenv import load_dotenv

# Create your views here.
def home(request):
    if not request.user.id:
        return redirect(reverse("login"))
    social_account = request.user.socialaccount_set.filter(provider='twitter').first()
    image_url = social_account.extra_data["profile_image_url"]
    return render(request, 'home.html', {"username":request.user.username, "image_url":image_url})

def login(request):
    return render(request, 'login.html')

def song_detection():
    now_playing = AzuraCastClient().now_playing()
    song_name = now_playing['title']
    artist_name = now_playing['artist']

    music_client = MusicInfoClient()
    artist_details = music_client.get_artist_data(artist_name)
    artist_details = artist_details['lastfm'] or artist_details['wikipedia'] or artist_details['openai'] or artist_name

    song_details = music_client.get_song_data(artist_name, song_name)
    song_details = song_details['lastfm'] or song_details['openai'] or song_name

    band_details = music_client.get_band_data(artist_name)
    band_details = band_details['open_ai']

    album_art_url = music_client.get_song_art_url(song_name, artist_name)

    context = {
        "song_details" : song_details,
        "artist_details" : artist_details,
        "band_details" : band_details,
        "album_art_url": album_art_url
    }

    return context


def manual_detection(request):

    if request.method == 'GET':

        context = song_detection()

        return render(request, 'manual_detection.html', context)


def preview_tweet(request, type):
    if type == "manual":
        context = {
            "song_details": request.POST['song-details'],
            "artist_details": request.POST['artist-details'],
            "band_details": request.POST['band-details'],
            "album_art_url": request.POST['album-art-url']
        }
    else:
        context = song_detection()
    summarized_tweet = OpenAIClient().summarize_for_tweet(context)
    return render(request, 'preview_tweet.html', { "summarized_tweet": summarized_tweet, "album_art_url": context["album_art_url"]})


def post_tweet(request):
    if request.method == "POST":
        summarized_tweet = request.POST["tweet-field"]
        image_url = request.POST.get("album_art_url", None)  # Image URL passed from form (optional)

        # Get user's Twitter social account tokens
        social_account = request.user.socialaccount_set.filter(provider='twitter').first()
        if not social_account:
            raise Exception("User is not connected to Twitter")

        access_token = social_account.socialtoken_set.first().token
        access_token_secret = social_account.socialtoken_set.first().token_secret

        load_dotenv()

        # Initialize Tweepy API
        auth = tweepy.OAuth1UserHandler(
            consumer_key=os.getenv("CONSUMER_KEY"),
            consumer_secret=os.getenv("CONSUMER_SECRET"),
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        api = tweepy.API(auth)

        # Upload image if provided
        error = False
        media_id = None
        if image_url:
            try:
                # Download the image from the URL
                image_response = requests.get(image_url, stream=True)
                image_response.raise_for_status()
                with open("temp_image.jpg", "wb") as img_file:
                    for chunk in image_response.iter_content(chunk_size=1024):
                        img_file.write(chunk)

                # Upload the image to Twitter
                media = api.media_upload(filename="temp_image.jpg")
                media_id = media.media_id_string
            except requests.exceptions.RequestException as e:
                print(f"Error downloading image: {e}")
                error = True
            except Exception as e:
                print(f"Error uploading image to Twitter: {e}")
                error = True

        # Post the tweet with or without media
        try:
            if media_id:
                tweet = api.update_status(status=summarized_tweet, media_ids=[media_id])
            else:
                tweet = api.update_status(status=summarized_tweet)

            tweet_url = f"https://twitter.com/{request.user.username}/status/{tweet.id}"
        except Exception as e:
            print(e)
            error = True

        # Fetch the oEmbed HTML to embed the tweet
        if not error:
            api_url = f"https://publish.twitter.com/oembed?url={tweet_url}"
            try:
                embed_response = requests.get(api_url)
                embed_response.raise_for_status()
                embed_html = embed_response.json().get("html", "")
            except requests.exceptions.RequestException as e:
                error = True
                embed_html = f"<p>Error loading tweet: {e}</p>"
        else:
            embed_html = None
            tweet_url = None

        return render(request, "show_tweet.html", {"embed_html": embed_html, "tweet_url": tweet_url, "error": error})