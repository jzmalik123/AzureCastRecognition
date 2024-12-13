from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

from .services.azuracast_client import AzuraCastClient
from .services.music_info_client import MusicInfoClient
from .services.open_ai_client import *
from django.conf import settings
import tweepy
import os
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

def automatic_detection(request):
    now_playing = AzuraCastClient().now_playing()
    song_name = now_playing['title']
    artist_name = now_playing['artist']

    music_client = MusicInfoClient()
    artist_details = music_client.get_artist_data(artist_name)
    artist_details = artist_details['lastfm'] or artist_details['wikipedia'] or artist_details['openai'] or artist_name

    song_details = music_client.get_song_data(artist_name, song_name)
    song_details = song_details['lastfm'] or song_details['openai'] or song_name

    band_details = music_client.get_band_data(artist_name)

    context = {
        "song_details" : song_details,
        "artist_details" : artist_details,
        "band_details" : band_details
    }
    summarized_tweet = OpenAIClient().summarize_for_tweet(context)
    redirect_uri = post_tweet(request.user, summarized_tweet)
    return redirect(redirect_uri)


def manual_detection(request):

    if request.method == 'GET':
        now_playing = AzuraCastClient().now_playing()
        song_name = now_playing['title']
        artist_name = now_playing['artist']

        music_client = MusicInfoClient()
        artist_details = music_client.get_artist_data(artist_name)
        artist_details = artist_details['lastfm'] or artist_details['wikipedia'] or artist_details['openai'] or artist_name

        song_details = music_client.get_song_data(artist_name, song_name)
        song_details = song_details['lastfm'] or song_details['openai'] or song_name

        band_details = music_client.get_band_data(artist_name)['open_ai']

        context = {
            "song_details": song_details,
            "artist_details": artist_details,
            "band_details": band_details
        }

        return render(request, 'manual_detection.html', context)
    else:
        context = {
            "song_details": request.POST['song-details'],
            "artist_details": request.POST['artist-details'],
            "band_details": request.POST['band-details']
        }
        summarized_tweet = OpenAIClient().summarize_for_tweet(context)
        redirect_uri = post_tweet(request.user, summarized_tweet)
        return redirect(redirect_uri)

def post_tweet(user, tweet_content):
    # Retrieve user's tokens
    social_account = user.socialaccount_set.filter(provider='twitter').first()
    if not social_account:
        raise Exception("User is not connected to Twitter")

    access_token = social_account.socialtoken_set.first().token
    access_token_secret = social_account.socialtoken_set.first().token_secret

    load_dotenv()
    # Initialize Tweepy client
    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # Post tweet
    response = client.create_tweet(text=tweet_content)
    return f"https://twitter.com/{user.username}/status/{response.data['id']}"


